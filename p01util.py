"""p01util — 区域 01 拆解图脚本共用的小构件（不改动 hand3d/props/partdraw）。"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl


def merge(solids, name="", shade=True):
    """把若干 Solid 合成一个，减少轮廓计算量。"""
    F, E = [], []
    for s in solids:
        F += [np.asarray(f, float) for f in s.faces]
        E += [(np.asarray(a, float), np.asarray(b, float)) for a, b in s.edges]
    m = Solid(F, E, name)
    m.shade = shade
    return m


def _M(s, M, c):
    c = np.asarray(c, float); M = np.asarray(M, float)
    F = [(np.asarray(f, float) - c) @ M.T + c for f in s.faces]
    E = [((np.asarray(a, float) - c) @ M.T + c, (np.asarray(b, float) - c) @ M.T + c) for a, b in s.edges]
    o = Solid(F, E, s.name); o.shade = s.shade
    return o


def rot(solids, ang, axis="x", center=(0, 0, 0)):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    M = {"x": [[1, 0, 0], [0, c, -s], [0, s, c]],
         "y": [[c, 0, s], [0, 1, 0], [-s, 0, c]],
         "z": [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[axis]
    one = isinstance(solids, Solid)
    out = [_M(x, M, center) for x in ([solids] if one else solids)]
    return out[0] if one else out


def mv(solids, d):
    one = isinstance(solids, Solid)
    out = [x.moved(d) for x in ([solids] if one else solids)]
    return out[0] if one else out


def prism(sec, length, axis="x", pos=(0, 0, 0), name="棱柱"):
    """任意截面棱柱。sec 是截面二维点列；axis='x' 时 sec 是 (y,z)，'y' 时 (x,z)，'z' 时 (x,y)。"""
    x, y, z = pos
    if axis == "x":
        a = [np.array([x, y + u, z + v], float) for u, v in sec]; d = np.array([length, 0, 0.])
    elif axis == "y":
        a = [np.array([x + u, y, z + v], float) for u, v in sec]; d = np.array([0, length, 0.])
    else:
        a = [np.array([x + u, y + v, z], float) for u, v in sec]; d = np.array([0, 0., length])
    b = [p + d for p in a]
    n = len(a)
    F = [[a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]] for i in range(n)]
    F.append(list(a[::-1])); F.append(list(b))
    E = [(a[i], a[(i + 1) % n]) for i in range(n)] + [(b[i], b[(i + 1) % n]) for i in range(n)] + \
        [(a[i], b[i]) for i in range(n)]
    return Solid(F, E, name)


def rope(p0, p1, sag=30, r=2.5, n=9, name="麻绳"):
    """微微下垂的绳：抛物线折成 n 段小圆柱（每段绕 Y 转到位），合成一个 Solid。"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    pts = []
    for i in range(n + 1):
        t = i / n
        p = p0 + (p1 - p0) * t
        p = p.copy(); p[2] -= 4 * sag * t * (1 - t)
        pts.append(p)
    segs = []
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        d = b - a; L = float(np.linalg.norm(d))
        c = cyl(r, L, "x", (0, 0, 0), 8, name)
        ang = math.degrees(math.atan2(-d[2], d[0]))
        c = rot(c, ang, "y", (0, 0, 0))
        segs.append(c.moved(a))
    return merge(segs, name)


def tube(pos, r, length, axis="z", wall=18, name="管"):
    """双层管：外管 + 露出的内管口。"""
    o = [cyl(r, length, axis, pos, 20, name)]
    return o


def jar(pos, r=55, h=150, name="玻璃罐"):
    x, y, z = pos
    return [cyl(r, h, "z", (x, y, z), 16, name),
            cyl(r * 0.78, 18, "z", (x, y, z + h), 14, name + "盖")]


def mug(pos, r=42, h=92, up=True, name="杯"):
    """杯子：杯身 + 一个 C 形把手（用三段小方料近似）。up=False 为倒挂。"""
    x, y, z = pos
    o = [cyl(r, h, "z", (x, y, z), 14, name)]
    hz = z + h * (0.55 if up else 0.30)
    o += [box((10, 12, 34), (x + r, y - 6, hz), name + "把"),
          box((26, 12, 10), (x + r, y - 6, hz + 34), name + "把"),
          box((26, 12, 10), (x + r, y - 6, hz - 10), name + "把")]
    return o


def screw(pos, r=5, L=60, axis="y", name="螺栓"):
    x, y, z = pos
    head = {"x": (10, 2.4 * r, 2.4 * r), "y": (2.4 * r, 10, 2.4 * r), "z": (2.4 * r, 2.4 * r, 10)}[axis]
    off = {"x": (x, y - 1.2 * r, z - 1.2 * r), "y": (x - 1.2 * r, y, z - 1.2 * r), "z": (x - 1.2 * r, y - 1.2 * r, z)}[axis]
    return [cyl(r, L, axis, pos, 10, name), box(head, off, name + "头")]


def audit(items, solids, az, el, fov=27, W=1200, H=900, rect=(0.05, 0.22, 0.96, 0.91)):
    """自检辅助：算出 partdraw.draw 会用的同一台相机，报告画面占比与每条引线实际指到的零件。"""
    import numpy as np
    from hand3d import fit_cam, zbuffer, all_pts
    cam = fit_cam(solids, W, H, rect=rect, az=az, el=el, fov=fov)
    P = cam.proj(all_pts(solids))
    h = (P[:, 1].max() - P[:, 1].min()) / H * 100
    w = (P[:, 0].max() - P[:, 0].min()) / W * 100
    print("  画面占比  高 %.0f%%  宽 %.0f%%   顶边 y=%.0f" % (h, w, P[:, 1].min()))
    Z = zbuffer(cam, solids)
    per = [(s.name or "?", zbuffer(cam, [s])) for s in solids]
    for n, t, a in items:
        p = cam.proj(a)[0]
        x, y = int(round(p[0])), int(round(p[1]))
        if not (0 <= x < W and 0 <= y < H):
            print("  %s 锚点出画 (%d,%d)" % (n, x, y)); continue
        zz = Z[y, x]
        if not np.isfinite(zz):
            print("  %s @(%d,%d) 指到空白" % (n, x, y)); continue
        best, bd = "?", 1e18
        for nm, zs in per:
            v = zs[y, x]
            if np.isfinite(v) and abs(v - zz) < bd:
                best, bd = nm, abs(v - zz)
        flag = "" if p[2] - zz < 40 else "  ← 被挡（差 %.0f）" % (p[2] - zz)
        print("  %s @(%d,%d) 指到「%s」%s" % (n, x, y, best, flag))
