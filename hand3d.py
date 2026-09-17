"""hand3d — 用真实三维几何渲染铅笔风拆解图（PNG）。

流程：建模(真实尺寸, mm) → 透视相机 → z-buffer 消隐 → 铅笔化描边/排线 → 纸纹底 → 标注。
比手码 SVG 路径强的地方：透视、比例、遮挡关系都是算出来的，不是画出来的。
"""
import numpy as np, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PAPER = (249, 246, 239)
INK = (61, 61, 61)
INK2 = (42, 42, 42)
GREY = (138, 138, 138)
SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SANS_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- 几何 ----------
def _np(p): return np.asarray(p, dtype=float)

class Solid:
    """faces: (N,4,3) 四边形；edges: [(p0,p1)] 特征线；shade: 面是否排线"""
    def __init__(self, faces, edges, name="", shade=True):
        self.faces = [np.asarray(f, float) for f in faces]
        self.edges = [(np.asarray(a, float), np.asarray(b, float)) for a, b in edges]
        self.name, self.shade = name, shade
    def moved(self, d):
        d = _np(d)
        return Solid([f + d for f in self.faces], [(a + d, b + d) for a, b in self.edges], self.name, self.shade)

def box(size, pos=(0, 0, 0), name=""):
    w, d, h = size; x, y, z = pos
    p = [(x, y, z), (x+w, y, z), (x+w, y+d, z), (x, y+d, z),
         (x, y, z+h), (x+w, y, z+h), (x+w, y+d, z+h), (x, y+d, z+h)]
    F = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (1,2,6,5), (2,3,7,6), (3,0,4,7)]
    E = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    return Solid([[p[i] for i in f] for f in F], [(p[a], p[b]) for a, b in E], name)

def extrusion(length, axis="x", pos=(0,0,0), sec=20, name="型材"):
    """欧标铝型材：外形方管 + 四面 T 槽线"""
    s = sec
    size = {"x": (length, s, s), "y": (s, length, s), "z": (s, s, length)}[axis]
    b = box(size, pos, name)
    x, y, z = pos; w, d, h = size
    e = list(b.edges)
    # 槽线：沿长度方向两条
    def ln(a, bb): e.append((_np(a), _np(bb)))
    g = s * 0.28
    if axis == "x":
        for zz in (z + s/2 - g, z + s/2 + g):
            ln((x, y, zz), (x+length, y, zz)); ln((x, y+d, zz), (x+length, y+d, zz))
        for yy in (y + s/2 - g, y + s/2 + g):
            ln((x, yy, z+h), (x+length, yy, z+h)); ln((x, yy, z), (x+length, yy, z))
    elif axis == "y":
        for zz in (z + s/2 - g, z + s/2 + g):
            ln((x, y, zz), (x, y+length, zz)); ln((x+w, y, zz), (x+w, y+length, zz))
        for xx in (x + s/2 - g, x + s/2 + g):
            ln((xx, y, z+h), (xx, y+length, z+h)); ln((xx, y, z), (xx, y+length, z))
    else:
        for xx in (x + s/2 - g, x + s/2 + g):
            ln((xx, y, z), (xx, y, z+length)); ln((xx, y+d, z), (xx, y+d, z+length))
        for yy in (y + s/2 - g, y + s/2 + g):
            ln((x, yy, z), (x, yy, z+length)); ln((x+w, yy, z), (x+w, yy, z+length))
    return Solid(b.faces, e, name)

def cyl(r, length, axis="z", pos=(0,0,0), seg=20, name="", cap=True):
    """pos 为底面圆心"""
    x, y, z = pos
    th = np.linspace(0, 2*math.pi, seg, endpoint=False)
    if axis == "z": ring = lambda t: np.stack([x + r*np.cos(t), y + r*np.sin(t), np.full_like(t, z)], -1); dvec = _np((0,0,length))
    elif axis == "x": ring = lambda t: np.stack([np.full_like(t, x), y + r*np.cos(t), z + r*np.sin(t)], -1); dvec = _np((length,0,0))
    else: ring = lambda t: np.stack([x + r*np.cos(t), np.full_like(t, y), z + r*np.sin(t)], -1); dvec = _np((0,length,0))
    a = ring(th); b = a + dvec
    faces, edges = [], []
    for i in range(seg):
        j = (i+1) % seg
        faces.append([a[i], a[j], b[j], b[i]])
        edges.append((a[i], a[j])); edges.append((b[i], b[j]))
    if cap:
        faces.append(list(a[::-1])); faces.append(list(b))
    # 少量母线
    for i in range(0, seg, max(1, seg//6)):
        edges.append((a[i], b[i]))
    return Solid(faces, edges, name)

def plate(size, pos=(0,0,0), name=""):
    return box(size, pos, name)

def holes_marks(pts, r=3):
    """孔位小圈（当作特征线，贴在面上）"""
    E = []
    for c in pts:
        c = _np(c); th = np.linspace(0, 2*math.pi, 13)
        pp = [c + np.array([r*math.cos(t), r*math.sin(t), 0]) for t in th]
        E += [(pp[i], pp[i+1]) for i in range(len(pp)-1)]
    return E

# ---------- 相机 ----------
class Cam:
    def __init__(self, eye, target, up=(0,0,1), fov=32, W=1200, H=900, cx=None, cy=None):
        self.e = _np(eye); t = _np(target); u = _np(up)
        f = t - self.e; f /= np.linalg.norm(f)
        s = np.cross(f, u); s /= np.linalg.norm(s)
        v = np.cross(s, f)
        self.R = np.stack([s, v, f])         # 世界→相机
        self.f = (H/2) / math.tan(math.radians(fov)/2)
        self.W, self.H = W, H
        self.cx = W/2 if cx is None else cx
        self.cy = H/2 if cy is None else cy
    def proj(self, P):
        P = np.atleast_2d(np.asarray(P, float))
        c = (P - self.e) @ self.R.T
        z = np.clip(c[:, 2], 1e-6, None)
        x = self.cx + self.f * c[:, 0] / z
        y = self.cy - self.f * c[:, 1] / z
        return np.stack([x, y, z], -1)

# ---------- 光栅：z-buffer ----------
def zbuffer(cam, solids, sup=1):
    W, H = cam.W*sup, cam.H*sup
    Z = np.full((H, W), np.inf, np.float32)
    for s in solids:
        for f in s.faces:
            p = cam.proj(f); p[:, :2] *= sup
            if np.any(p[:, 2] <= 1e-5): continue
            for tri in [(0,1,2), (0,2,3)][:max(1, len(f)-2)]:
                if max(tri) >= len(p): continue
                _raster(Z, p[list(tri)], W, H)
    return Z

def _raster(Z, tri, W, H):
    x0 = max(int(np.floor(tri[:,0].min())), 0); x1 = min(int(np.ceil(tri[:,0].max()))+1, W)
    y0 = max(int(np.floor(tri[:,1].min())), 0); y1 = min(int(np.ceil(tri[:,1].max()))+1, H)
    if x1 <= x0 or y1 <= y0: return
    xs = np.arange(x0, x1) + 0.5; ys = np.arange(y0, y1) + 0.5
    X, Y = np.meshgrid(xs, ys)
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = tri
    den = (by-cy)*(ax-cx) + (cx-bx)*(ay-cy)
    if abs(den) < 1e-9: return
    w0 = ((by-cy)*(X-cx) + (cx-bx)*(Y-cy)) / den
    w1 = ((cy-ay)*(X-cx) + (ax-cx)*(Y-cy)) / den
    w2 = 1 - w0 - w1
    m = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
    if not m.any(): return
    zz = w0*az + w1*bz + w2*cz
    sub = Z[y0:y1, x0:x1]
    upd = m & (zz < sub)
    sub[upd] = zz[upd].astype(np.float32)

# ---------- 铅笔化描边 ----------
def _jit(pts, amp, rng):
    """给折线加低频抖动"""
    n = len(pts)
    if n < 2: return pts
    ph = [rng.uniform(0, 6.28) for _ in range(3)]; fr = [rng.uniform(0.6, 1.8) for _ in range(3)]
    out = []
    for i, (x, y) in enumerate(pts):
        t = i / max(1, n-1)
        dx = sum(math.sin(ph[k] + fr[k]*t*6.283) for k in range(3)) / 3
        dy = sum(math.cos(ph[k]*1.3 + fr[k]*t*6.283) for k in range(3)) / 3
        out.append((x + dx*amp, y + dy*amp))
    return out

class Pencil:
    def __init__(self, W, H, seed=3):
        self.W, self.H = W, H
        self.img = Image.new("L", (W, H), 255)
        self.d = ImageDraw.Draw(self.img)
        self.rng = random.Random(seed)
    def stroke(self, pts, width=2.0, dark=70, passes=2, amp=1.1, over=0.0):
        """铅笔笔触：低频抖动 + 多遍叠加 + 端部出头（手绘的过冲）"""
        if len(pts) < 2: return
        if over > 0 and len(pts) >= 2:
            (x0, y0), (x1, y1) = pts[0], pts[1]
            d = math.hypot(x1-x0, y1-y0) or 1
            pts = [(x0 - (x1-x0)/d*over*self.rng.uniform(.3, 1), y0 - (y1-y0)/d*over*self.rng.uniform(.3, 1))] + list(pts)
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            d = math.hypot(xb-xa, yb-ya) or 1
            pts = list(pts) + [(xb + (xb-xa)/d*over*self.rng.uniform(.3, 1), yb + (yb-ya)/d*over*self.rng.uniform(.3, 1))]
        for k in range(passes-1, -1, -1):
            p = _jit(pts, amp * (0.55 + 0.7*k), self.rng)
            off = (self.rng.uniform(-0.7, 0.7), self.rng.uniform(-0.7, 0.7))
            p = [(x+off[0], y+off[1]) for x, y in p]
            w = max(1, int(round(width * (1.0 if k == 0 else 0.75))))
            self.d.line(p, fill=min(255, max(0, dark + k*48 + self.rng.randint(-12, 12))), width=w, joint="curve")
    def dash(self, pts, width=1.4, dark=150, seg=9, gap=7):
        if len(pts) < 2: return
        acc, on, cur = 0.0, True, [pts[0]]
        for a, b in zip(pts, pts[1:]):
            d = math.hypot(b[0]-a[0], b[1]-a[1]); t = 0.0
            while t < d:
                lim = (seg if on else gap) - acc
                step = min(lim, d - t)
                q = (a[0] + (b[0]-a[0])*(t+step)/d, a[1] + (b[1]-a[1])*(t+step)/d)
                if on: cur.append(q)
                t += step; acc += step
                if acc >= (seg if on else gap) - 1e-9:
                    if on and len(cur) > 1: self.stroke(cur, width, dark, 1, 0.5)
                    on = not on; acc = 0.0; cur = [q]
        if on and len(cur) > 1: self.stroke(cur, width, dark, 1, 0.5)

def visible_polyline(cam, Z, a, b, sup=1, bias=0.997, n=None):
    """把一条三维线段按可见性切成若干屏幕折线"""
    pa, pb = cam.proj(a)[0], cam.proj(b)[0]
    if pa[2] <= 1e-5 and pb[2] <= 1e-5: return []
    L = math.hypot(pb[0]-pa[0], pb[1]-pa[1])
    n = n or max(2, min(160, int(L/3)+2))
    ts = np.linspace(0, 1, n)
    P = np.array([a, b], float)
    pts3 = P[0] + (P[1]-P[0])*ts[:, None]
    pr = cam.proj(pts3)
    H, W = Z.shape
    out, cur = [], []
    for (x, y, z) in pr:
        xi, yi = int(x*sup), int(y*sup)
        vis = False
        if 0 <= xi < W and 0 <= yi < H:
            zb = Z[yi, xi]
            vis = (z <= zb / bias) or not np.isfinite(zb)
        elif 0 <= x < cam.W and 0 <= y < cam.H:
            vis = True
        else:
            vis = False
        if vis: cur.append((x, y))
        else:
            if len(cur) > 1: out.append(cur)
            cur = []
    if len(cur) > 1: out.append(cur)
    return out

def hatch_face(cam, Z, face, pen, ang=38, step=7, dark=170, sup=1):
    """对一个面按固定角度排线（只画可见部分）"""
    p = cam.proj(face)
    if np.any(p[:, 2] <= 1e-5): return
    xy = p[:, :2]
    cx, cy = xy[:, 0].mean(), xy[:, 1].mean()
    a = math.radians(ang); dirv = (math.cos(a), math.sin(a)); nor = (-math.sin(a), math.cos(a))
    proj_n = [(x-cx)*nor[0] + (y-cy)*nor[1] for x, y in xy]
    lo, hi = min(proj_n), max(proj_n)
    k = lo + step
    poly = [tuple(q) for q in xy]
    while k < hi:
        # 求扫描线与多边形交点
        P0 = (cx + nor[0]*k, cy + nor[1]*k)
        ts = []
        for (x1, y1), (x2, y2) in zip(poly, poly[1:]+poly[:1]):
            d1 = (x1-P0[0])*nor[0] + (y1-P0[1])*nor[1]
            d2 = (x2-P0[0])*nor[0] + (y2-P0[1])*nor[1]
            if (d1 > 0) != (d2 > 0) and abs(d1-d2) > 1e-9:
                u = d1/(d1-d2)
                ix, iy = x1 + (x2-x1)*u, y1 + (y2-y1)*u
                ts.append((ix-P0[0])*dirv[0] + (iy-P0[1])*dirv[1])
        ts.sort()
        for i in range(0, len(ts)-1, 2):
            A = (P0[0]+dirv[0]*ts[i], P0[1]+dirv[1]*ts[i])
            B = (P0[0]+dirv[0]*ts[i+1], P0[1]+dirv[1]*ts[i+1])
            # 按 z-buffer 过滤：取中点深度
            pen.stroke([A, B], 1.3, dark, 1, 0.8, over=1.5)
        k += step

def face_normal(f):
    f = np.asarray(f, float)
    n = np.cross(f[1]-f[0], f[2]-f[0])
    ln = np.linalg.norm(n)
    return n/ln if ln > 1e-9 else n

# ---------- 场景绘制 ----------
def draw_solids(cam, solids, pen, Z=None, sup=1, light=(-0.5, -0.8, 0.9), hatch_step=8, lw=2.0):
    if Z is None: Z = zbuffer(cam, solids, sup)
    L = _np(light); L = L/np.linalg.norm(L)
    # 1) 排线：背光且朝向相机的面
    for s in solids:
        if not s.shade: continue
        for f in s.faces:
            n = face_normal(f)
            c = np.asarray(f, float).mean(0)
            if np.dot(n, cam.e - c) <= 0: continue        # 背面
            lit = np.dot(n, L)
            if lit > 0.34: continue                        # 只给最受光的面留白
            dark = 196 if lit > -0.25 else 168
            step = hatch_step + (3 if lit > -0.35 else 0)
            hatch_face(cam, Z, f, pen, 38, step, dark, sup)
    # 2) 描边
    for s in solids:
        for a, b in s.edges:
            for poly in visible_polyline(cam, Z, a, b, sup):
                pen.stroke(poly, lw, 62, 2, 1.0, over=3.5)
    return Z

def paper(W, H, seed=1):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 3.2, (H, W))
    base = np.clip(np.array(PAPER, float)[None, None, :] + g[:, :, None], 0, 255)
    return Image.fromarray(base.astype(np.uint8))

def compose(pen_img, W, H, seed=1):
    """铅笔层（L, 白底）叠到纸上"""
    ink = pen_img.filter(ImageFilter.GaussianBlur(0.4))
    bg = paper(W, H, seed)
    a = np.asarray(bg, float)
    m = 1.0 - np.asarray(ink, float)[:, :, None]/255.0     # 墨量
    ink_col = np.array(INK, float)[None, None, :]
    out = a*(1-m) + ink_col*m
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def sheet(img, title, legend, note, sig, W, H, scale=1.0):
    """在已合成的图上加标题 / 图例 / 注脚 / 签名（矢量感文字）"""
    d = ImageDraw.Draw(img)
    s = scale
    f_t = font(SANS_B, int(23*s)); f_l = font(SANS, int(16*s)); f_n = font(SANS, int(15*s)); f_s = font(SERIF, int(19*s))
    d.text((int(30*s), int(26*s)), title, font=f_t, fill=INK2)
    for i, (n, t) in enumerate(legend):
        d.text((int(30*s), int(64*s) + i*int(25*s)), f"{n} {t}", font=f_l, fill=(70, 70, 70))
    if note:
        d.text((int(30*s), H - int(52*s)), note, font=f_n, fill=(105, 105, 105))
    if sig:
        tw = d.textlength(sig, font=f_s)
        d.text((W - int(30*s) - tw, H - int(50*s)), sig, font=f_s, fill=(100, 100, 100))
    return img

def numcircle(d, x, y, n, r, f, col=INK2):
    d.ellipse([x-r, y-r, x+r, y+r], outline=col, width=max(1, int(r/6)))
    w = d.textlength(str(n), font=f)
    d.text((x - w/2, y - r*0.72), str(n), font=f, fill=col)

# ---------- 轮廓（每个零件的可见外轮廓，加粗） ----------
import cv2
def silhouettes(cam, solids, Z, pen, sup=1, lw=3.6, dark=28, eps=1.2, minlen=14):
    for s in solids:
        Zs = zbuffer(cam, [s], sup)
        vis = np.isfinite(Zs) & (Zs <= Z * 1.004)
        m = (vis * 255).astype(np.uint8)
        if m.max() == 0: continue
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for c in cs:
            if cv2.arcLength(c, True) < minlen: continue
            ap = cv2.approxPolyDP(c, eps, True).reshape(-1, 2).astype(float) / sup
            if len(ap) < 2: continue
            pts = [tuple(p) for p in ap] + [tuple(ap[0])]
            pen.stroke(pts, lw, dark, 2, 0.9, over=0)

def render_parts(cam, solids, W, H, seed=5, lw_edge=2.0, lw_sil=3.6, hatch_step=7, sup=1, light=(-0.5,-0.8,0.9)):
    """一次性：z-buffer → 排线 → 特征线 → 轮廓"""
    pen = Pencil(W, H, seed)
    Z = zbuffer(cam, solids, sup)
    L = _np(light); L = L/np.linalg.norm(L)
    for s in solids:
        if not s.shade: continue
        for f in s.faces:
            n = face_normal(f); c = np.asarray(f, float).mean(0)
            if np.dot(n, cam.e - c) <= 0: continue
            lit = float(np.dot(n, L))
            if lit > 0.34: continue
            dark = 152 if lit > -0.25 else 124
            hatch_face(cam, Z, f, pen, 38, hatch_step + (3 if lit > -0.25 else 0), dark, sup)
    for s in solids:
        for a, b in s.edges:
            for poly in visible_polyline(cam, Z, a, b, sup):
                pen.stroke(poly, lw_edge, 64, 2, 1.0, over=2.5)
    silhouettes(cam, solids, Z, pen, sup, lw_sil)
    return pen, Z

# ---------- 引线与编号 ----------
def leaders_and_nums(img, cam, items, scale=1.0, r=13, dashed=True):
    """items: [(编号, 三维锚点, (屏幕x, 屏幕y))]；在图上画虚线引线 + 编号圈"""
    d = ImageDraw.Draw(img)
    f = font(SANS_B, int(r*1.15))
    pen = Pencil(img.width, img.height, seed=11)
    for n, anchor, (tx, ty) in items:
        p = cam.proj(anchor)[0]
        if dashed: pen.dash([(p[0], p[1]), (tx, ty)], 1.6, 120, 8, 6)
        else: pen.stroke([(p[0], p[1]), (tx, ty)], 1.4, 120, 1, .6)
    lay = np.asarray(pen.img, float)
    base = np.asarray(img, float)
    m = (1 - lay/255.0)[:, :, None]
    out = base*(1-m) + np.array(INK, float)[None, None, :]*m
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for n, anchor, (tx, ty) in items:
        d.ellipse([tx-r, ty-r, tx+r, ty+r], fill=PAPER, outline=INK2, width=2)
        w = d.textlength(str(n), font=f)
        d.text((tx - w/2, ty - r*0.78), str(n), font=f, fill=INK2)
    return img

def axis_line(img, p0, p1):
    pen = Pencil(img.width, img.height, seed=7)
    pen.dash([p0, p1], 1.6, 150, 10, 8)
    lay = np.asarray(pen.img, float); base = np.asarray(img, float)
    m = (1-lay/255.0)[:, :, None]
    out = base*(1-m) + np.array(GREY, float)[None, None, :]*m
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


# ---------- 自动取景 ----------
def all_pts(solids):
    P = []
    for s in solids:
        for f in s.faces: P.append(np.asarray(f, float))
        for a, b in s.edges: P.append(np.array([a, b], float))
    return np.vstack(P)

def fit_cam(solids, W, H, rect=(0.05, 0.16, 0.96, 0.90), az=38, el=26, fov=28, up=(0, 0, 1), margin=1.0):
    """自动选相机距离与主点，使整个装配落进 rect（比例坐标）。"""
    P = all_pts(solids)
    c = (P.min(0) + P.max(0)) / 2
    rad = float(np.linalg.norm(P.max(0) - P.min(0)) / 2) or 1.0
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.cos(e)*math.cos(a), math.cos(e)*math.sin(a), math.sin(e)])
    x0, y0, x1, y1 = rect[0]*W, rect[1]*H, rect[2]*W, rect[3]*H
    tw, th = (x1-x0)*margin, (y1-y0)*margin
    lo, hi = rad*1.05, rad*60
    best = None
    for _ in range(46):
        dist = (lo+hi)/2
        cam = Cam(c + d*dist, c, up, fov, W, H)
        p = cam.proj(P)
        if np.any(p[:, 2] <= 1e-6): lo = dist; continue
        bw = p[:, 0].max()-p[:, 0].min(); bh = p[:, 1].max()-p[:, 1].min()
        if bw <= tw and bh <= th: hi = dist; best = (cam, p)
        else: lo = dist
    if best is None:
        cam = Cam(c + d*rad*8, c, up, fov, W, H); p = cam.proj(P); best = (cam, p)
    cam, p = best
    cx = cam.cx + ((x0+x1)/2 - (p[:, 0].min()+p[:, 0].max())/2)
    cy = cam.cy + ((y0+y1)/2 - (p[:, 1].min()+p[:, 1].max())/2)
    return Cam(cam.e, c, up, fov, W, H, cx, cy)

# ---------- 常用零件剪影（简化实体，用于墙面/工具/家具） ----------
def hammer(pos, L=300, face="-y"):
    x, y, z = pos
    return [cyl(11, L, "z", (x, y, z), 12, "柄"), box((96, 34, 46), (x-24, y-17, z+L-46), "锤头")]

def wrench(pos, L=260):
    x, y, z = pos
    o = [box((26, 16, L), (x-13, y-8, z), "杆")]
    for zz in (z+L-34, z):
        o.append(box((58, 16, 34), (x-29, y-8, zz), "口"))
    return o

def plier(pos, L=200):
    x, y, z = pos
    return [box((22, 14, L*0.62), (x-24, y-7, z), "柄"), box((22, 14, L*0.62), (x+2, y-7, z), "柄"),
            box((46, 14, L*0.38), (x-23, y-7, z+L*0.62), "钳头")]

def driver(pos, L=230):
    x, y, z = pos
    return [cyl(15, L*0.42, "z", (x, y, z), 12, "把"), cyl(5, L*0.58, "z", (x, y, z+L*0.42), 10, "杆")]

def tape(pos, r=52):
    x, y, z = pos
    return [cyl(r, 30, "y", (x, y, z), 20, "卷尺"), box((34, 34, 26), (x-17, y-2, z-r-8), "挂钩")]

def chair(pos, seatw=520, seath=460, backh=580):
    """人体工学椅：五星脚 + 气杆 + 坐垫 + 靠背 + 头枕"""
    x, y, z = pos
    o = [box((seatw, 480, 70), (x - seatw/2, y - 240, z + seath), "坐垫"),
         box((seatw*0.92, 70, backh), (x - seatw*0.46, y + 180, z + seath + 60), "靠背"),
         box((seatw*0.55, 60, 90), (x - seatw*0.275, y + 170, z + seath + 60 + backh), "头枕"),
         cyl(36, seath, "z", (x, y, z), 14, "气杆")]
    for i in range(5):
        a = i*2*math.pi/5 + 0.3
        dx, dy = math.cos(a), math.sin(a)
        L = 290
        pts = [(x, y, z+18), (x + dx*L, y + dy*L, z+18)]
        o.append(cyl(17, L, "x", (x, y, z+30), 8, "脚") if abs(dy) < 0.2 else
                 Solid([[(x-24*dy, y+24*dx, z+16), (x+24*dy, y-24*dx, z+16),
                         (x+dx*L+24*dy, y+dy*L-24*dx, z+34), (x+dx*L-24*dy, y+dy*L+24*dx, z+34)]],
                       [((x-24*dy, y+24*dx, z+16), (x+dx*L-24*dy, y+dy*L+24*dx, z+34)),
                        ((x+24*dy, y-24*dx, z+16), (x+dx*L+24*dy, y+dy*L-24*dx, z+34))], "脚"))
        o.append(cyl(30, 34, "z", (x + dx*L, y + dy*L, z), 10, "轮"))
    return o

def shelf_run(pos, w, h, d, n=5, name="书格"):
    x, y, z = pos
    o = [box((26, d, h), (x, y, z), name), box((26, d, h), (x+w-26, y, z), name)]
    for i in range(n):
        zz = z + (h-24) * i/(n-1)
        o.append(box((w, d, 24), (x, y, zz), name))
    return o
