# -*- coding: utf-8 -*-
"""重绘 0209 藏宝阁（床下 1.5×2m 密室）与 0101 PSK 主产品展示（卡片式 PSK）的插图与拆解图。

为什么重绘：ALIGN_0009.md 把这两个模块的文案按真实项目改了——
0209 从“印第安帐篷 + 帘子 + 盘腿坐”改成“架空床下能坐直写字的密室”；
0101 主打产品从“掀盖 110° 的生存盒 + 27 件物件”改成“信用卡大小的卡片式 PSK”。
画面必须跟着改。画风（滤镜 / 排线 / id 前缀 / 签名）严格沿用原文件。

用法：cd /home/claude/vision && python3 redraw_0209_0101.py
"""
from sk import *
from redraw_08 import SH, along, finish, flow, poster

COMIC = "'Comic Sans MS','Segoe Print','Bradley Hand',cursive"


def sign_comic(svg):
    return svg.replace(f'font-family="{HAND}" font-size="10"', f'font-family="{COMIC}" font-size="10"')


def ln(x1, y1, x2, y2, sw=0.7, dash=""):
    """不加滤镜的细线（尺寸线 / 引线用）"""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="#1c1c1c" '
            f'stroke-width="{sw}" fill="none"{d} filter="none" stroke-linecap="round"/>')


def tick(x, y, dx, dy, sw=0.8):
    return (f'<path d="M{x-dx:.1f} {y-dy:.1f} L{x+dx:.1f} {y+dy:.1f}" stroke="#1c1c1c" '
            f'stroke-width="{sw}" fill="none" filter="none" stroke-linecap="round"/>')


# =========================================================================
#  0209 藏宝阁 · 插图：架空床下 1.5×2m、净高 1.7m 的密室剖视（从南往北看进去）
# =========================================================================
BW0, BW1, BH0, BH1 = 148.0, 272.0, 52.0, 192.0   # 北端短墙（后墙）在画布上的矩形
LAM = 0.40                                        # 剖切面 / 后墙 的缩放比
SX = (BW1 - BW0) / 2 / LAM - (BW1 - BW0) / 2      # 侧墙横向展开量
SY = 70.0 / LAM - 70.0                            # 纵向展开量
DF = 2.0 / (1.0 / LAM - 1.0)                      # 视点到剖切面的距离（m）
DB = DF + 2.0                                     # 视点到后墙的距离


def sdep(d):
    """真实进深 d（m，0=北端短墙）→ 线性插值参数 s（0..1）"""
    return (d / (DB - d)) / (1.0 / LAM - 1.0)


def P0(w, h, d):
    """房间坐标 → 画布坐标。w 0(西)~1.5(东)，h 0~1.7(高)，d 0(北)~2.0(南)"""
    s = sdep(d)
    x0, x1 = BW0 - SX * s, BW1 + SX * s
    y0, y1 = BH0 - SY * s, BH1 + SY * s
    return (x0 + (w / 1.5) * (x1 - x0), y1 - (h / 1.7) * (y1 - y0))


K = 0.92           # 整体缩放，给四周留出标注余地
KCX, KCY = 210.0, 140.0
KTX, KTY = 206.0, 142.0


def P(w, h, d):
    x, y = P0(w, h, d)
    return (KTX + (x - KCX) * K, KTY + (y - KCY) * K)


def seg(a, b):
    return f"M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f}"


def quad(a, b, c, d, fill=None, sw=1.0):
    p = f"M{a[0]:.0f} {a[1]:.0f} L{b[0]:.0f} {b[1]:.0f} L{c[0]:.0f} {c[1]:.0f} L{d[0]:.0f} {d[1]:.0f} Z"
    if fill:
        return f'<path d="{p}" fill="{fill}" stroke="none"/>'
    return f'<path d="{p}" stroke-width="{sw}"/>'


def wave(a, b, amp=4.0, n=8, sw=0.9):
    s = f"M{a[0]:.0f} {a[1]:.0f} "
    for i in range(1, n + 1):
        t = i / n
        s += (f"Q{a[0]+(b[0]-a[0])*(t-0.5/n):.0f} {a[1]+(b[1]-a[1])*(t-0.5/n)+(amp if i%2 else -amp):.0f} "
              f"{a[0]+(b[0]-a[0])*t:.0f} {a[1]+(b[1]-a[1])*t:.0f} ")
    return f'<path d="{s}" stroke-width="{sw}"/>'



def compact(body):
    """把相邻的、只有 stroke-width 的纯描边 path 合并成一条，压文件体积"""
    import re
    lines = [l for l in body.split("\n") if l.strip()]
    out, buf, bw = [], [], None
    pat = re.compile(r'^<path d="([^"]+)" stroke-width="([0-9.]+)"/>$')
    def flush():
        if buf:
            out.append(f'<path d="{" ".join(buf)}" stroke-width="{bw}"/>')
    for l in lines:
        m = pat.match(l.strip())
        if m and (bw is None or m.group(2) == bw):
            bw = m.group(2); buf.append(m.group(1))
        elif m:
            flush(); buf = [m.group(1)]; bw = m.group(2)
        else:
            flush(); buf = []; bw = None; out.append(l)
    flush()
    return "\n".join(out)

def pth(pts, sw=1.2, close=False, fill=None):
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts) + (" Z" if close else "")
    if fill:
        return f'<path d="{d}" fill="{fill}" stroke="none"/>'
    return f'<path d="{d}" stroke-width="{sw}"/>'


YTOP = 30.0        # 画面上沿：所有构件在这条线上做“撕开”断口


def dclip(w, h, dmax):
    """沿进深方向裁到画面上沿"""
    if P(w, h, dmax)[1] >= YTOP:
        return dmax
    lo, hi = 0.0, dmax
    for _ in range(26):
        mid = (lo + hi) / 2
        if P(w, mid and h or h, mid)[1] >= YTOP:
            lo = mid
        else:
            hi = mid
    return lo


def hclip(w, d, hmax):
    """沿高度方向裁到画面上沿"""
    if P(w, hmax, d)[1] >= YTOP:
        return hmax
    lo, hi = 0.0, hmax
    for _ in range(26):
        mid = (lo + hi) / 2
        if P(w, mid, d)[1] >= YTOP:
            lo = mid
        else:
            hi = mid
    return lo


def m0209():
    pfx = "m0209"
    H = f"url(#{pfx}-hatch)"; HL = f"url(#{pfx}-hatchl)"
    B = []
    DCUT = 1.60          # 地面在这里断开（波浪断线）
    T = 0.74             # 写字台台面高
    HW = 1.68            # 墙体净高上沿
    DCEIL = dclip(0, 1.7, 2.0)

    # ---------- 地面 ----------
    B.append(pth([P(0, 0, 0), P(1.5, 0, 0)], 1.5))
    B.append(pth([P(0, 0, 0), P(0, 0, DCUT)], 1.3))
    B.append(pth([P(1.5, 0, 0), P(1.5, 0, DCUT)], 1.3))
    for d in (0.60, 1.10, 1.46):
        B.append(pth([P(0, 0, d), P(1.5, 0, d)], 0.4))
    B.append(wave(P(0, 0, DCUT), P(1.5, 0, DCUT), 4.5))

    # ---------- 床板（顶）：板厚 50 + 底面板缝 ----------
    B.append(pth([P(0, 1.7, 0), P(1.5, 1.7, 0)], 1.6))
    B.append(pth([P(0, 1.75, 0), P(1.5, 1.75, 0)], 1.3))
    B.append(quad(P(0, 1.7, 0), P(0, 1.75, 0), P(1.5, 1.75, 0), P(1.5, 1.7, 0), fill=H))
    B.append(pth([P(0, 1.7, 0), P(0, 1.7, DCEIL)], 1.2))
    B.append(pth([P(1.5, 1.7, 0), P(1.5, 1.7, DCEIL)], 1.2))
    for w in (0.38, 0.75, 1.12):
        B.append(pth([P(w, 1.7, 0), P(w, 1.7, DCEIL)], 0.45))
    B.append(wave(P(0, 1.7, DCEIL), P(1.5, 1.7, DCEIL), 3.0))

    # ---------- 后墙（北端短墙）两条竖边 ----------
    B.append(pth([P(0, 0, 0), P(0, 1.7, 0)], 1.4))
    B.append(pth([P(1.5, 0, 0), P(1.5, 1.7, 0)], 1.4))

    # ---------- 两侧墙的上沿撕开断口 ----------
    for w in (0.0, 1.5):
        pts = []
        for i2 in range(13):
            d = DCEIL + (DCUT - DCEIL) * i2 / 12.0
            pts.append(P(w, hclip(w, d, HW), d))
        dd = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        B.append(f'<path d="{dd}" stroke-width="0.9"/>')

    # ---------- 东侧长墙：木饰面板缝 ----------
    for d in (0.35, 0.70, 1.02):
        B.append(pth([P(1.5, 0, d), P(1.5, hclip(1.5, d, HW), d)], 0.4))

    # ---------- 西侧长墙：一整排连续浅书格（进深 180） ----------
    SHELVES = [0.06, 0.38, 0.64, 0.96, 1.22, 1.54]
    LIP = 0.18 / 1.5
    for h in SHELVES:
        de = dclip(LIP, h, DCUT)
        B.append(pth([P(0, h, 0.04), P(0, h, de)], 0.9))
        B.append(pth([P(LIP, h, 0.04), P(LIP, h, de)], 0.75))
        B.append(pth([P(0, h, 0.04), P(LIP, h, 0.04)], 0.7))
    B.append(pth([P(0, HW, 0.04), P(0, HW, dclip(0, HW, DCUT))], 0.8))
    for d in (0.04, 0.44, 0.86, 1.28, 1.56):
        ht = hclip(LIP, d, HW)
        if ht < 0.10:
            continue
        B.append(pth([P(0, 0.06, d), P(0, ht, d)], 0.75))
        B.append(pth([P(0, 0.06, d), P(LIP, 0.06, d)], 0.5))
        if ht > HW - 0.01:
            B.append(pth([P(0, HW, d), P(LIP, HW, d)], 0.5))
    bk = []
    for (h0, h1) in ((0.06, 0.38), (0.38, 0.64), (0.64, 0.96), (0.96, 1.22), (1.22, 1.54)):
        for d0, d1 in ((0.08, 0.40), (0.48, 0.82), (0.90, 1.24)):
            if P(LIP, h1, d1)[1] < YTOP + 4:
                continue
            for i2 in range(4):
                dd2 = d0 + (d1 - d0) * (i2 + 0.5) / 4
                x1, ya = P(LIP * 0.5, h0 + 0.02, dd2)
                x2, yb = P(LIP * 0.5, h1 - 0.04, dd2)
                bk.append(f'M{x1:.0f} {ya:.0f} L{x2:.0f} {yb:.0f}')
    B.append(f'<path d="{" ".join(bk)}" stroke-width="0.6"/>')
    # 尽端一格：铁皮宝箱
    c0, c1 = P(0.01, 0.10, 1.30), P(0.01, 0.33, 1.30)
    c2, c3 = P(0.01, 0.33, 1.54), P(0.01, 0.10, 1.54)
    B.append(quad(c0, c1, c2, c3, fill=HL))
    B.append(pth([c0, c1, c2, c3], 1.1, close=True))
    B.append(pth([((c0[0] + c1[0]) / 2, (c0[1] + c1[1]) / 2), ((c3[0] + c2[0]) / 2, (c3[1] + c2[1]) / 2)], 0.6))

    # ---------- 顶部 360° 环绕洗墙灯带 + 顺墙往下淌的光 ----------
    B.append(pth([P(0, 1.63, 0.03), P(0, 1.63, dclip(0, 1.63, DCEIL))], 1.1))
    B.append(pth([P(0, 1.63, 0.03), P(1.5, 1.63, 0.03)], 1.1))
    B.append(pth([P(1.5, 1.63, 0.03), P(1.5, 1.63, dclip(1.5, 1.63, DCEIL))], 1.1))
    lt = []
    for w in (0.10, 0.32, 0.54, 0.76, 0.98, 1.20, 1.42):
        lt.append(seg(P(w, 1.60, 0.03), P(w, 1.30, 0.03)))
    for d in (0.16, 0.42, 0.70):
        lt.append(seg(P(1.5, 1.60, d), P(1.5, 1.32, d)))
    B.append(f'<path d="{" ".join(lt)}" stroke-width="0.45"/>')

    # ---------- 北墙海报墙（名言 / 电影 / 对话） ----------
    for (w0, w1, h0, h1) in [(0.10, 0.44, 1.02, 1.58), (0.50, 0.90, 1.16, 1.58),
                             (0.96, 1.42, 1.22, 1.58), (0.52, 0.88, 0.88, 1.10),
                             (0.96, 1.42, 0.88, 1.16)]:
        B.append(pth([P(w0, h0, 0), P(w0, h1, 0), P(w1, h1, 0), P(w1, h0, 0)], 1.0, close=True))
    q = []
    for w in (0.16, 0.24, 0.32, 0.38):
        q.append(seg(P(w, 1.52, 0), P(w, 1.08, 0)))
    for h in (1.52, 1.44, 1.36, 1.30):
        q.append(seg(P(1.02, h, 0), P(1.36, h, 0)))
    for h in (1.10, 1.03, 0.96):
        q.append(seg(P(1.00, h, 0), P(1.38, h, 0)))
    for h in (1.04, 0.97):
        q.append(seg(P(0.56, h, 0), P(0.84, h, 0)))
    B.append(f'<path d="{" ".join(q)}" stroke-width="0.45"/>')
    mx, my = P(0.70, 1.30, 0)
    B.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.6" stroke-width="0.8"/>')
    B.append(pth([P(0.70, 1.26, 0), P(0.70, 1.32, 0)], 0.8))
    B.append(pth([P(0.52, 1.24, 0), P(0.88, 1.24, 0)], 0.6))

    # ---------- 1.5m 写字台（台面 740，进深 600） ----------
    tp = [P(0.05, T, 0), P(1.45, T, 0), P(1.45, T, 0.60), P(0.05, T, 0.60)]
    B.append(pth(tp, 1.0, close=True, fill="#fff"))
    B.append(pth(tp, 1.5, close=True))
    B.append(pth([P(0.05, 0.68, 0.60), P(1.45, 0.68, 0.60)], 1.1))
    B.append(pth([P(0.05, T, 0.60), P(0.05, 0.68, 0.60)], 1.0))
    B.append(pth([P(1.45, T, 0.60), P(1.45, 0.68, 0.60)], 1.0))
    B.append(quad(P(0.05, 0.68, 0.60), P(1.45, 0.68, 0.60), P(1.45, T, 0.60), P(0.05, T, 0.60), fill=HL))
    for w in (0.11, 1.39):
        B.append(pth([P(w, 0.68, 0.56), P(w, 0, 0.56)], 1.0))
    nb = [P(0.64, T, 0.10), P(1.06, T, 0.10), P(1.10, T, 0.40), P(0.60, T, 0.40)]
    B.append(pth(nb, 0.9, close=True, fill="#fff"))
    B.append(pth(nb, 0.9, close=True))
    B.append(pth([P(0.85, T, 0.10), P(0.85, T, 0.40)], 0.6))

    # ---------- 台角明放的瓷银茶器 ----------
    trx = [P(1.08, T, 0.08), P(1.44, T, 0.08), P(1.44, T, 0.32), P(1.08, T, 0.32)]
    B.append(pth(trx, 0.8, close=True))
    tx, ty = P(1.19, T, 0.18)
    pot = f'M{tx-7:.1f} {ty:.1f} q0 -10 7.5 -10 q7.5 0 7.5 10 Z'
    B.append(f'<path d="{pot}" stroke-width="1.1" fill="#fff"/>')
    B.append(f'<path d="{pot}" stroke-width="1.1"/>')
    B.append(f'<path d="M{tx+1:.1f} {ty-9.6:.1f} q2.5 -4 5.5 -3.2 M{tx-7:.1f} {ty-5:.1f} q-5 1.5 -4 5 M{tx-1.5:.1f} {ty-10:.1f} v-3" stroke-width="0.85"/>')
    for (ww, dd3) in ((1.36, 0.14), (1.36, 0.28)):
        cx2, cy2 = P(ww, T, dd3)
        cup = f'M{cx2-3.6:.1f} {cy2-4.2:.1f} q0 4.6 3.6 4.6 q3.6 0 3.6 -4.6 Z'
        B.append(f'<path d="{cup}" stroke-width="0.85" fill="#fff"/>')
        B.append(f'<path d="{cup}" stroke-width="0.85"/>')

    # ---------- 人体工学椅（总高 ≤1300）+ 坐直了写字的人 ----------
    DCH = 0.94
    sx, sy = P(0.76, 0, DCH)
    _, y13 = P(0.76, 1.30, DCH)
    k = (sy - y13) / 1.30

    def zh(h):
        return sy - h * k
    # 五星脚 + 滚轮
    B.append(f'<path d="M{sx-22:.1f} {sy-1:.1f} L{sx:.1f} {sy-9:.1f} L{sx+22:.1f} {sy-1:.1f} M{sx-11:.1f} {sy+4:.1f} L{sx:.1f} {sy-9:.1f} L{sx+11:.1f} {sy+4:.1f}" stroke-width="1.0"/>')
    for ddx in (-22, -11, 11, 22):
        B.append(f'<circle cx="{sx+ddx:.1f}" cy="{sy+2:.1f}" r="2.4" stroke-width="0.8"/>')
    # 气压杆
    B.append(f'<path d="M{sx-2.6:.1f} {sy-9:.1f} V{zh(0.45):.1f} M{sx+2.6:.1f} {sy-9:.1f} V{zh(0.45):.1f}" stroke-width="1.1"/>')
    # 头枕（总高 1300，画在人后面）
    hrw = 0.085 * k
    hd = f'M{sx-hrw:.1f} {zh(1.30):.1f} h{2*hrw:.1f} v{0.13*k:.1f} h-{2*hrw:.1f} Z'
    B.append(f'<path d="{hd}" stroke-width="1.1" fill="#fff"/>')
    B.append(f'<path d="{hd}" stroke-width="1.1"/>')
    B.append(f'<path d="M{sx-2:.1f} {zh(1.17):.1f} V{zh(1.06):.1f} M{sx+2:.1f} {zh(1.17):.1f} V{zh(1.06):.1f}" stroke-width="0.8"/>')
    # 椅背（网背，画在人后面，比人肩略窄）
    bw = 0.225 * k
    bk2 = (f'M{sx-bw:.1f} {zh(0.50):.1f} V{zh(0.98):.1f} q{bw:.1f} -{0.06*k:.1f} {2*bw:.1f} 0 V{zh(0.50):.1f} Z')
    B.append(f'<path d="{bk2}" stroke-width="1.2" fill="#fff"/>')
    B.append(f'<path d="{bk2}" stroke-width="1.2"/>')
    B.append(f'<path d="M{sx-bw+1:.1f} {zh(0.88):.1f} h{2*bw-2:.1f} M{sx-bw+1:.1f} {zh(0.74):.1f} h{2*bw-2:.1f} M{sx-bw+1:.1f} {zh(0.62):.1f} h{2*bw-2:.1f}" stroke-width="0.4"/>')
    # 坐垫
    B.append(f'<path d="M{sx-19:.1f} {zh(0.45):.1f} h38 v6 h-38 Z" stroke-width="1.2" fill="#fff"/>')
    B.append(f'<path d="M{sx-19:.1f} {zh(0.45):.1f} h38 v6 h-38 Z" stroke-width="1.2"/>')
    # 扶手
    for sgn in (-1, 1):
        ax3 = sx + sgn * (bw + 3)
        B.append(f'<path d="M{ax3:.1f} {zh(0.50):.1f} V{zh(0.64):.1f} h{sgn*7:.1f}" stroke-width="1.0"/>')
    # 人：背影，坐直，双臂伸到台面上
    tws, twh = 0.20 * k, 0.15 * k
    tor = (f'M{sx-twh:.1f} {zh(0.50):.1f} L{sx-tws:.1f} {zh(0.88):.1f} '
           f'q0 {-0.07*k:.1f} {0.06*k:.1f} {-0.08*k:.1f} h{2*tws-0.12*k:.1f} '
           f'q{0.06*k:.1f} {0.01*k:.1f} {0.06*k:.1f} {0.08*k:.1f} L{sx+twh:.1f} {zh(0.50):.1f} Z')
    B.append(f'<path d="{tor}" stroke-width="1.3" fill="#fff"/>')
    B.append(f'<path d="{tor}" stroke-width="1.3"/>')
    B.append(f'<path d="M{sx-twh*0.8:.1f} {zh(0.62):.1f} L{sx+twh*0.8:.1f} {zh(0.62):.1f}" stroke-width="0.4"/>')
    # 手臂：肩 → 肘 → 台面上的手
    lh = P(0.40, T + 0.035, 0.50); rh = P(1.06, T + 0.035, 0.30)
    for (sgn, hh) in ((-1, lh), (1, rh)):
        shx, shy = sx + sgn * tws, zh(0.90)
        elx, ely = sx + sgn * (tws + 0.045 * k), zh(0.74)
        B.append(f'<path d="M{shx:.1f} {shy:.1f} L{elx:.1f} {ely:.1f} L{hh[0]:.1f} {hh[1]:.1f}" stroke-width="1.25"/>')
        B.append(f'<path d="M{hh[0]-3.4:.1f} {hh[1]-1:.1f} q3.4 4 6.8 0" stroke-width="0.9"/>')
    B.append(f'<path d="M{rh[0]+1:.1f} {rh[1]+1:.1f} l5 -7" stroke-width="0.9"/>')
    # 颈 + 头
    hr = 0.088 * k
    hx, hy = sx, zh(1.10)
    B.append(f'<path d="M{hx-2.2:.1f} {hy+hr-1:.1f} V{zh(0.96):.1f} M{hx+2.2:.1f} {hy+hr-1:.1f} V{zh(0.96):.1f}" stroke-width="1.0"/>')
    B.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr:.1f}" stroke-width="1.3" fill="#fff"/>')
    B.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{hr:.1f}" stroke-width="1.3"/>')
    B.append(f'<path d="M{hx-hr+1.5:.1f} {hy-hr+2.6:.1f} q{hr-1.5:.1f} -3.6 {2*hr-3:.1f} 0" stroke-width="0.7"/>')


    # ---------- 东侧长墙靠南：40cm 帆布滑动门（半开） ----------
    D0, D1 = 1.08, 1.48
    HT, HB = 1.50, 0.04
    B.append(pth([P(1.5, HT + 0.04, 0.90), P(1.5, HT + 0.04, 1.52)], 1.4))
    B.append(pth([P(1.5, HT, 0.90), P(1.5, HT, 1.52)], 0.9))
    op = [P(1.5, HB - 0.05, D0), P(1.5, HT, D0), P(1.5, HT, D1), P(1.5, HB - 0.05, D1)]
    B.append(quad(*op, fill=HL))
    B.append(pth(op, 1.4, close=True))
    F0, F1 = 1.06, 1.28
    fan = [P(1.5, HT, F0), P(1.5, HT, F1), P(1.5, HB, F1), P(1.5, HB, F0)]
    B.append(quad(*fan, fill="#fff"))
    B.append(pth(fan, 1.5, close=True))
    fold = []
    for d in (1.105, 1.15, 1.195, 1.24):
        xa, ya = P(1.5, HT - 0.03, d); xb, yb = P(1.5, HB + 0.04, d)
        fold.append(f'M{xa:.1f} {ya:.1f} Q{xa+2.4:.1f} {(ya+yb)/2:.1f} {xb:.1f} {yb:.1f}')
    B.append(f'<path d="{" ".join(fold)}" stroke-width="0.6"/>')
    wa, wb = P(1.5, HB, F0), P(1.5, HB, F1)
    B.append(f'<path d="M{wa[0]:.1f} {wa[1]:.1f} L{wb[0]:.1f} {wb[1]:.1f}" stroke-width="2.4"/>')
    for d in (F0 + 0.035, F1 - 0.035):
        xa, ya = P(1.5, HT + 0.025, d)
        B.append(f'<circle cx="{xa:.1f}" cy="{ya:.1f}" r="1.9" stroke-width="0.8"/>')

    body = compact("\n".join(B))

    # ================= 标注 =================
    L = []
    fx, fy = P(0, 0, 0.10); _, cy = P(0, 1.7, 0.10); _, ty2 = P(0, 1.75, 0.10)
    XD, XD2 = 110, 94
    L += [ln(XD, fy, fx - 2, fy, 0.5, "3 3"), ln(XD, cy, fx - 2, cy, 0.5, "3 3"),
          ln(XD2, ty2, fx - 2, ty2, 0.5, "3 3"),
          ln(XD, fy, XD, cy, 0.8), tick(XD, fy, 3, 2.4), tick(XD, cy, 3, 2.4),
          ln(XD2, ty2, XD2, fy, 0.7), tick(XD2, ty2, 3, 2.4), tick(XD2, fy, 3, 2.4),
          label(XD - 5, (fy + cy) / 2 + 3, "净高 1700", 8, "end"),
          label(XD2 - 4, ty2 + 12, "床板 1750", 8, "end")]
    a, b = P(0.06, 0, 1.48), P(1.44, 0, 1.48)
    L += [ln(a[0], a[1] + 9, b[0], b[1] + 9, 0.6), tick(a[0], a[1] + 9, 2, 3), tick(b[0], b[1] + 9, 2, 3),
          label((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 19, "1.5m（进深 2.0m）", 8, "middle")]
    e, f = P(1.5, HB - 0.13, D0), P(1.5, HB - 0.13, D1)
    L += [ln(e[0] + 5, e[1] + 3, f[0] + 5, f[1] + 3, 0.6), tick(e[0] + 5, e[1] + 3, 2, 3), tick(f[0] + 5, f[1] + 3, 2, 3),
          ln(f[0] + 7, f[1] + 5, 342, 240, 0.5, "3 3"), label(345, 242, "400", 7.5, "start")]

    px, py = P(1.42, 1.40, 0)
    bx2, by2 = P(0, 1.06, 0.80)
    cx2, cy2 = P(0.02, 0.22, 1.44)
    dx2, dy2 = P(0.07, T, 0.56)
    chx, chy = sx + bw, zh(0.80)
    tex, tey = P(1.34, T + 0.05, 0.18)
    dox, doy = P(1.5, 1.20, 1.26)
    lab = [
        label(200, 18, "顶部 360° 环绕洗墙灯带 2700K · 光贴着墙往下淌", 8.5, "middle"),
        label(16, 96, "西侧长墙", 8), label(16, 107, "一整排连续浅书格", 7.5), label(16, 117, "进深 180", 7.5),
        ln(66, 113, bx2 - 2, by2, 0.5, "3 3"),
        label(16, 208, "尽端一格：铁皮宝箱", 7.5),
        ln(72, 204, cx2 - 2, cy2, 0.5, "3 3"),
        label(16, 244, "1.5m 写字台 · 台面 740", 7.5),
        ln(82, 240, dx2 - 1, dy2 + 2, 0.5, "3 3"),
        label(390, 70, "海报墙", 8, "end"), label(390, 81, "名言 / 电影 / 对话", 7.5, "end"),
        ln(320, 77, px + 2, py, 0.5, "3 3"),
        label(390, 130, "东侧长墙靠南", 7.5, "end"), label(390, 141, "40cm 帆布滑门（半开）", 7.5, "end"),
        label(390, 152, "隐藏滑轨 + 下沿配重杆", 7.5, "end"),
        ln(322, 137, dox + 2, doy, 0.5, "3 3"),
        label(390, 184, "台角明放瓷银茶器", 7.5, "end"),
        ln(320, 180, tex + 3, tey - 3, 0.5, "3 3"),
        label(390, 212, "人体工学椅 总高 ≤1300", 7.5, "end"),
        label(390, 223, "头顶离床板还有一截", 7.5, "end"),
        ln(306, 208, chx + 2, chy, 0.5, "3 3"),
        label(200, 282, "0209 藏宝阁：床下 1.5×2m、净高 1700，一间能坐直了写字的密室", 9.5, "middle", "#1c1c1c"),
    ]
    labels = "\n".join(x for x in (L + lab) if x)
    return sign_comic(illo(pfx, body, "0209", seed=7).replace("</svg>", labels + "\n</svg>"))


# =========================================================================
#  0101 PSK 主产品展示 · 插图：挂墙展台上一块黑胡桃托盘
#  左边一张收起态的卡，右边是它展开后的十来件小件；梁底射灯低角度掠射拉出长影
# =========================================================================
def m0101():
    pfx = "m0101"
    H = f"url(#{pfx}-hatch)"; HL = f"url(#{pfx}-hatchl)"
    B = []
    LX, LY = 52.0, 118.0          # 射灯出光口（压得很低，光几乎贴着台面走）

    # ---------- 木板墙 + 地面 ----------
    for y in (16, 40, 64):
        B.append(f'<path d="M14 {y} H386" stroke-width="0.4"/>')
    for y in (112, 142):
        B.append(f'<path d="M14 {y} H40 M312 {y} H386" stroke-width="0.4"/>')
    B.append('<path d="M12 268 H388" stroke-width="1.5"/>')
    B.append('<path d="M60 273 q22 -3 44 0 M210 273 q26 -3 52 0" stroke-width="0.5"/>')

    # ---------- 0102 作品九宫格 ----------
    for r in range(3):
        for c in range(3):
            x = 134 + c * 50; y = 10 + r * 22
            B.append(f'<path d="M{x} {y} h42 v18 h-42 Z" stroke-width="1.0"/>')
            B.append(f'<path d="M{x+3} {y+3} h36 v12 h-36 Z" stroke-width="0.5"/>')
    B.append(f'<path d="M137 13 h36 v12 h-36 Z" fill="{HL}" stroke="none"/>')
    B.append(f'<path d="M237 57 h36 v12 h-36 Z" fill="{HL}" stroke="none"/>')

    # ---------- 梁 + 梁底射灯：灯头压到很低的角度 ----------
    B.append('<path d="M14 82 H330 V94 H14 Z" stroke-width="1.6"/>')
    B.append(f'<path d="M16 89 H328 V93 H16 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M38 94 h18 v5 h-18 Z" stroke-width="1.2"/>')            # 可旋转安装座
    B.append('<path d="M47 99 v4" stroke-width="1.1"/>')
    B.append('<circle cx="47" cy="105" r="3.2" stroke-width="1.0"/>')           # 云台关节
    B.append('<path d="M38 104 l16 -4 l8 13 l-16 6 Z" stroke-width="1.4"/>')    # 灯体
    B.append(f'<path d="M40 105 l13 -3 l6 10 l-13 5 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M55 100 l7 11 M58 99 l7 11" stroke-width="0.7"/>')       # 蜂窝防眩罩
    # 掠射光线：几乎贴着托盘走
    for (ex, ey) in ((132, 158), (176, 163), (216, 168), (254, 173)):
        B.append(f'<path d="M{LX} {LY} L{ex} {ey}" stroke-width="0.55"/>')
    B.append(f'<path d="M{LX} {LY} L102 143 L104 152 Z" fill="{HL}" stroke="none"/>')

    # ---------- 挂墙展台（135×35 悬挑，台面高 900，前低后高 12°） ----------
    B.append('<path d="M96 132 H292 L302 196 H86 Z" stroke-width="1.8"/>')
    B.append('<path d="M97 134 H291" stroke-width="0.7"/>')
    B.append('<path d="M86 196 h216 v5 h-216 Z" stroke-width="1.5"/>')
    B.append('<path d="M86 201 V222 H302 V201" stroke-width="1.6"/>')
    B.append(f'<path d="M86 216 H302 V222 H86 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M94 203 h52 v15 h-52 Z" stroke-width="1.1"/>')           # 7 寸小屏
    B.append('<path d="M97 205 h46 v11 h-46 Z" stroke-width="0.6"/>')
    B.append('<path d="M115 208 l8 3 l-8 3 Z" stroke-width="0.8"/>')
    B.append('<path d="M158 202 h136 v17 h-136 Z" stroke-width="1.0"/>')        # 薄抽屉
    B.append('<path d="M216 211 h20" stroke-width="1.6"/>')
    B.append(f'<path d="M160 204 h132 v13 h-132 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M108 222 V246 L138 222" stroke-width="1.4"/>')           # 手刨胡桃木托架
    B.append('<path d="M280 222 V246 L250 222" stroke-width="1.4"/>')
    B.append(f'<path d="M110 224 v18 l14 -18 Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M278 224 v18 l-14 -18 Z" fill="{H}" stroke="none"/>')

    # ---------- 黑胡桃托盘 30×20 ----------
    B.append('<path d="M130 142 H258 L270 188 H118 Z" stroke-width="1.5"/>')
    B.append('<path d="M136 147 H252 L262 183 H126 Z" stroke-width="0.9"/>')
    B.append(f'<path d="M130 142 H258 L270 188 H118 Z M136 147 H252 L262 183 H126 Z" fill="{HL}" stroke="none" fill-rule="evenodd"/>')

    # ---------- 左半：收起态的一张卡 85.6×54 ----------
    # 1.5mm 薄毛毡卡槽（只压四边）
    B.append('<path d="M137 150 H186 L191 176 H132 Z" stroke-width="0.8"/>')
    B.append(f'<path d="M137 150 H186 L191 176 H132 Z M140.5 152.5 H183 L187 173.5 H135.6 Z" fill="{H}" stroke="none" fill-rule="evenodd"/>')
    # 卡（薄，微微翘起一点厚度）
    B.append('<path d="M140.5 152.5 H183 L187 173.5 H135.6 Z" stroke-width="1.5" fill="#fff"/>')
    B.append('<path d="M140.5 152.5 H183 L187 173.5 H135.6 Z" stroke-width="1.5"/>')
    B.append('<path d="M135.6 173.5 L136 176.5 H188 L187 173.5" stroke-width="1.1"/>')
    # 卡面：锯齿边 / 开瓶口 / 火石槽 / 刻度
    B.append('<path d="M144 157 h20 M144 161 h14 M144 165 h17" stroke-width="0.45"/>')
    B.append('<path d="M168 155 l2.6 2 l2.6 -2 l2.6 2 l2.6 -2 l2.6 2 l2.6 -2" stroke-width="0.6"/>')
    B.append('<path d="M146 170 a4 3 0 0 0 7.4 0" stroke-width="0.7"/>')
    B.append('<path d="M162 167 h16 v3.4 h-16 Z" stroke-width="0.55"/>')
    B.append('<path d="M165 167 v3.4 M169 167 v3.4 M173 167 v3.4" stroke-width="0.4"/>')
    # 18mm 指槽
    B.append('<path d="M153 176.5 a8 4.6 0 0 0 14 0" stroke-width="1.1"/>')
    # 掠射拉出的长影子
    B.append(f'<path d="M187 173.5 L225 179 L226 181.6 L136.5 181.6 L136 176.5 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M187 173.6 L225 179" stroke-width="0.5"/>')

    # ---------- 右半：展开后的十来件小件（按爆炸图排开）+ 各自的长影 ----------
    def shadow(x, y, w):
        return f'<path d="M{x} {y} l{w} 2 l0 2 l-{w} -2 Z" fill="{HL}" stroke="none"/>'
    sh, it = [], []
    it.append('<path d="M198 151 h16 v4 h-16 Z M200 151 v4 M204 151 v4" stroke-width="0.9"/>')        # 火石条
    sh.append(shadow(214, 155, 14))
    it.append('<path d="M222 151.6 h16 v3.6 h-16 Z M223 151.6 l1.6 -2 l1.6 2 l1.6 -2 l1.6 2 l1.6 -2 l1.6 2 l1.6 -2 l1.6 2 l1.6 -2 l1.6 2" stroke-width="0.7"/>')  # 锯齿条
    sh.append(shadow(238, 155.2, 13))
    it.append('<path d="M246 150.4 h12 v4.6 h-12 Z M249.6 150.4 v2.4 h4.8 v-2.4" stroke-width="0.8"/>')  # 开瓶口
    sh.append(shadow(258, 155, 12))
    it.append('<path d="M194 163 h18 M194 164.6 l-3 -0.8 l3 -0.8" stroke-width="0.8"/><circle cx="214" cy="163" r="1.8" stroke-width="0.7"/>')  # 针
    sh.append(shadow(216, 164.8, 13))
    it.append('<path d="M222 160.6 h14 M222 163.4 h14 M222 166.2 h14" stroke-width="0.8"/>')            # 防水火柴 ×3
    for yy in (160.6, 163.4, 166.2):
        it.append(f'<circle cx="221" cy="{yy}" r="1.3" stroke-width="0.6"/>')
    sh.append(shadow(236, 166.4, 12))
    it.append('<circle cx="250" cy="163" r="5.4" stroke-width="0.9"/><circle cx="250" cy="163" r="3" stroke-width="0.6"/><path d="M255 161 l5 -1.6" stroke-width="0.7"/>')  # 凯夫拉线
    sh.append(shadow(255.4, 165.6, 11))
    it.append('<path d="M200 174 l6 -5.4 l6 5.4 Z M203 174 h6" stroke-width="0.8"/>')                   # 刀片
    sh.append(shadow(212, 174, 12))
    it.append('<path d="M219 169 h12 a2.2 2.2 0 0 1 0 4.4 h-12 a2.2 2.2 0 0 1 0 -4.4 Z" stroke-width="0.7"/>')  # 别针
    sh.append(shadow(234, 173.6, 11))
    it.append('<path d="M241 169.4 h14 v4 h-14 Z M244 169.4 v4 M247 169.4 v2.4 M250 169.4 v4 M253 169.4 v2.4" stroke-width="0.7"/>')  # 小尺
    sh.append(shadow(255, 173.4, 10))
    it.append('<path d="M196 158 l9 3.4 M196 159.4 l9 2" stroke-width="0.7"/>')                          # 镊子
    B += sh + it
    # 一收一开的对照虚线
    B.append('<path d="M191 158 H196 M192 164 H190 M191 170 H197" stroke-width="0.5" stroke-dasharray="2 2"/>')
    B.append('<path d="M188 156 H197 M188 167 H193" stroke-width="0.5" stroke-dasharray="2 2"/>')

    # ---------- 托盘右后角：可翻的三倍放大压片 ----------
    B.append('<path d="M254 142 h34 v4 h-34 Z" stroke-width="1.1"/>')
    B.append('<path d="M256 142 L276 114 H302 L290 142 Z" stroke-width="1.4" fill="#fff"/>')
    B.append('<path d="M256 142 L276 114 H302 L290 142 Z" stroke-width="1.4"/>')
    B.append('<path d="M262 138 q12 -14 26 -18 M266 140 q12 -15 26 -19" stroke-width="0.5"/>')
    B.append('<path d="M277 127 a8 8 0 1 0 0.1 0" stroke-width="0.7"/>')
    B.append('<path d="M254 120 q-16 10 -18 30" stroke-width="0.7" stroke-dasharray="3 3"/>')
    B.append('<path d="M234 145 l2.4 7 l6 -4.6" stroke-width="0.8"/>')

    # ---------- 台面左前角：黄铜铭牌 ----------
    B.append('<path d="M94 182 H124 L127 192 H96 Z" stroke-width="1.2"/>')
    B.append('<path d="M98 185.6 h22 M99 188.6 h15" stroke-width="0.5"/>')

    # ---------- 左下角：柴火炉 + 右下角：高脚凳 ----------
    B.append('<path d="M14 244 h34 v24 h-34 Z" stroke-width="1.3"/>')
    B.append('<circle cx="31" cy="256" r="7" stroke-width="1.0"/>')
    B.append('<path d="M27 258 l3.4 -5 l3 3.4 l3.4 -4.4" stroke-width="0.7"/>')
    B.append('<path d="M28 244 V222" stroke-width="1.2"/>')
    B.append('<path d="M24 218 q4 -7 8 -3.4 M22 212 q6 -9 11 -4.4" stroke-width="0.6"/>')
    B.append('<path d="M322 236 h40 v5 h-40 Z M328 241 V268 M356 241 V268 M330 256 h24" stroke-width="1.2"/>')

    body = compact("\n".join(B))

    # ================= 标注 =================
    L = []
    # 台面高 900
    L += [ln(74, 268, 84, 268, 0.5, "3 3"), ln(74, 198, 86, 198, 0.5, "3 3"),
          ln(74, 198, 74, 268, 0.8), tick(74, 198, 3, 2.4), tick(74, 268, 3, 2.4),
          label(70, 236, "台面 900", 8, "end")]
    # 135 × 进深 35
    L += [ln(86, 254, 158, 254, 0.7), ln(232, 254, 302, 254, 0.7),
          tick(86, 254, 2.4, 3), tick(302, 254, 2.4, 3),
          ln(86, 224, 86, 256, 0.4, "3 3"), ln(302, 224, 302, 256, 0.4, "3 3"),
          label(194, 258, "135 × 进深 35 · 悬挑不落地", 8, "middle")]
    # 掠射入射角 15~25°
    L += [ln(LX, LY, LX + 58, LY, 0.5, "3 3"),
          '<path d="M96 118 a44 44 0 0 0 -39 -19" stroke="#1c1c1c" stroke-width="0.6" fill="none" filter="none"/>',
          label(44, 142, "15~25°", 7.5, "start")]

    lab = [
        label(16, 40, "0102 作品九宫格", 8), ln(84, 36, 130, 36, 0.5, "3 3"),
        label(16, 60, "梁底 3000K 射灯", 8), label(16, 71, "灯头压到很低的角度", 7.5),
        ln(56, 75, 48, 96, 0.5, "3 3"),
        label(172, 114, "一收一开：左边收起态的卡，右边它展开后的十来件", 7.5, "middle"),
        ln(130, 118, 150, 148, 0.5, "3 3"), ln(214, 118, 226, 148, 0.5, "3 3"),
        label(390, 100, "可翻的三倍放大压片", 7.5, "end"), ln(306, 108, 300, 118, 0.5, "3 3"),
        label(390, 128, "光几乎贴着托盘掠过去", 7.5, "end"), label(390, 139, "影子把刻痕拉出厚度", 7.5, "end"),
        ln(314, 143, 240, 178, 0.5, "3 3"),
        label(390, 166, "1.5mm 薄毛毡卡槽", 7.5, "end"), label(390, 177, "留 18mm 指槽好抠卡", 7.5, "end"),
        ln(312, 186, 189, 180, 0.5, "3 3"),
        label(390, 204, "薄抽屉：历代原型卡", 7.5, "end"), ln(310, 208, 298, 210, 0.5, "3 3"),
        label(74, 186, "铜牌刻", 7.5, "end"), label(74, 196, "PSK Card No.1", 7.5, "end"),
        ln(76, 190, 93, 187, 0.5, "3 3"),
        label(70, 212, "7 寸小屏", 7.5, "end"), ln(72, 209, 93, 208, 0.5, "3 3"),
        label(200, 282, "0101：一张 85.6×54 的卡，和它展开后的十来件小件，一收一开摆在同一块托盘上", 9, "middle", "#1c1c1c"),
    ]
    labels = "\n".join(x for x in (L + lab) if x)
    return sign_comic(illo(pfx, body, "0101", seed=7).replace("</svg>", labels + "\n</svg>"))


# =========================================================================
#  拆解图公用外壳
# =========================================================================
def ex2(pfx, title, sig, seed, legend, note, items, leaders, axis="M96 318 L392 40", extra=""):
    """items: [(frag_fn, pos_or_None)]；leaders: [(dx, dy)]（相对该零件的锚点）"""
    n = len(items)
    B, L, C = [], [], []
    pos = []
    for i2, (frag, ap) in enumerate(items):
        x, y = ap if ap else along(i2, n)
        pos.append((x, y))
        B.append(frag(x, y))
    for i2, (dx, dy) in enumerate(leaders):
        x, y = pos[i2]
        l, c = leader(x + dx, y + dy, x + dx - 34, y + dy - 6, i2 + 1)
        L.append(l); C.append(c)
    svg = exploded(pfx, title, "", "\n".join(B), sig, axis=axis, seed=seed, leaders="\n".join(L))
    svg = finish(svg, legend, C, note)
    if extra:
        svg = svg.replace("</svg>", extra + "\n</svg>")
    return svg


# =========================================================================
#  0209-1 hw 床下密室与帆布滑门
# =========================================================================
def p0209_1():
    pfx = "p0209-1"; SHD = SH(pfx)
    def f1(x, y):   # 地面基准面 1.5×2m
        return (f'<path d="M{x-56} {y} l34 -20 h74 l-34 20 Z" stroke-width="1.5"/>'
                f'<path d="M{x-52} {y-2} l30 -17 h64 l-30 17 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-56} {y} v4 h74 v-4 M{x+18} {y} l34 -20 v4" stroke-width="0.9"/>')
    def f2(x, y):   # 轻钢龙骨围合框架（三面）
        return (f'<path d="M{x-54} {y+8} l34 -20 M{x-54} {y+8} v-38 l34 -20 v38 M{x+20} {y+8} v-38 l34 -20 v38 h-74 M{x-54} {y-30} h74" stroke-width="1.2"/>'
                f'<path d="M{x-40} {y+2} v-34 M{x-24} {y-6} v-34 M{x-8} {y+8} v-38 M{x+8} {y+8} v-38 M{x+34} {y-4} v-34" stroke-width="0.7"/>'
                f'<path d="M{x-54} {y-12} h74 M{x-20} {y-12} l34 -20" stroke-width="0.6"/>')
    def f3(x, y):   # 9mm 木饰面板
        return (f'<path d="M{x-52} {y+4} h68 v-30 h-68 Z M{x-52} {y+4} l10 -6 h68 l-10 6 M{x+16} {y+4} l10 -6 v-30 l-10 6" stroke-width="1.3"/>'
                f'<path d="M{x-42} {y-2} h68 v-30" stroke-width="0.5" stroke-dasharray="3 3"/>'
                f'<path d="M{x-36} {y+4} v-30 M{x-20} {y+4} v-30 M{x-4} {y+4} v-30" stroke-width="0.5"/>'
                f'<path d="M{x+15} {y+3} l9 -5 v-28 l-9 5 Z" fill="{SHD}" stroke="none"/>')
    def f4(x, y):   # 隐藏滑轨 + 滑车 ×2
        return (f'<path d="M{x-52} {y} h76 v9 h-76 Z M{x-52} {y} l8 -5 h76 l-8 5 M{x+24} {y} l8 -5 v9 l-8 5" stroke-width="1.3"/>'
                f'<path d="M{x-48} {y+9} h68 v3 h-68 Z" stroke-width="0.7"/>'
                f'<path d="M{x+23} {y+1} l7 -4 v7 l-7 4 Z" fill="{SHD}" stroke="none"/>'
                f'<circle cx="{x-30}" cy="{y+4.5}" r="3" stroke-width="0.9"/><circle cx="{x+2}" cy="{y+4.5}" r="3" stroke-width="0.9"/>'
                f'<path d="M{x-30} {y+7.5} v5 M{x+2} {y+7.5} v5" stroke-width="0.9"/>')
    def f5(x, y):   # 40cm 帆布门帘 + 下沿配重杆
        b = [f'<path d="M{x-26} {y-34} h34 v54 h-34 Z" stroke-width="1.4"/>']
        for i2 in range(1, 6):
            b.append(f'<path d="M{x-26+i2*5.7} {y-34} q3 27 0 54" stroke-width="0.6"/>')
        b.append(f'<path d="M{x-28} {y+20} h38 v5 h-38 Z" stroke-width="1.6"/>')
        b.append(f'<path d="M{x-26} {y+21} h34 v3 h-34 Z" fill="{SHD}" stroke="none"/>')
        b.append(f'<path d="M{x-26} {y-40} h34 M{x-22} {y-40} v6 M{x+4} {y-40} v6" stroke-width="0.8"/>')
        b.append(f'<path d="M{x-26} {y-34} l-18 -4 M{x+8} {y-34} l18 -4" stroke-width="0.5" stroke-dasharray="2 2"/>')
        return "".join(b)
    def f6(x, y):   # 床板 1750
        return (f'<path d="M{x-58} {y} l34 -20 h74 l-34 20 Z" stroke-width="1.5"/>'
                f'<path d="M{x-58} {y} v7 h74 v-7 M{x+16} {y} l34 -20 v7 l-34 20" stroke-width="1.3"/>'
                f'<path d="M{x+17} {y+1} l32 -19 v5 l-32 19 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-40} {y-10} h74 M{x-26} {y-18} h74" stroke-width="0.5"/>'
                f'<path d="M{x-58} {y+7} l-16 0 M{x-74} {y+7} v-8 l16 0" stroke-width="0.6"/>')
    legend = [(1, "地面基准面 1.5×2m（床下净高 1700）"),
              (2, "轻钢龙骨围合框架 · 三面，不承重可拆"),
              (3, "9mm 木饰面板 · 拆掉不影响床体"),
              (4, "隐藏滑轨 + 滑车 ×2（东侧长墙靠南）"),
              (5, "40cm 帆布门帘 + 下沿配重杆"),
              (6, "床板 1750 —— 这间密室的天花")]
    items = [(f1, None), (f2, None), (f3, None), (f4, None), (f5, None), (f6, None)]
    lead = [(-50, -10), (-50, -18), (-48, -12), (-48, 2), (-30, -12), (-52, -10)]
    return ex2(pfx, "床下密室与帆布滑门", "0209-1", 3, legend,
               "1700 开不下平开门，入口只做侧身宽度的一道滑门", items, lead)


# =========================================================================
#  0209-2 hw 写字台与连续书格
# =========================================================================
def p0209_2():
    pfx = "p0209-2"; SHD = SH(pfx)
    def f1(x, y):   # 写字台钢架 + 1.5m 台面（740）
        return (f'<path d="M{x-52} {y} h78 v6 h-78 Z M{x-52} {y} l12 -7 h78 l-12 7 M{x+26} {y} l12 -7 v6 l-12 7" stroke-width="1.4"/>'
                f'<path d="M{x+25} {y+1} l10 -6 v4 l-10 6 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-46} {y+6} v26 M{x+20} {y+6} v26 M{x-34} {y-1} v26 M{x+32} {y-1} v26 M{x-46} {y+32} h66" stroke-width="1.0"/>')
    def f2(x, y):   # 人体工学椅（总高 ≤1300）
        return (f'<path d="M{x-16} {y+16} l16 -7 l16 7 M{x-9} {y+20} l9 -11 l9 11" stroke-width="1.0"/>'
                f'<circle cx="{x-16}" cy="{y+17}" r="2.2" stroke-width="0.7"/><circle cx="{x+16}" cy="{y+17}" r="2.2" stroke-width="0.7"/>'
                f'<circle cx="{x-9}" cy="{y+21}" r="2.2" stroke-width="0.7"/><circle cx="{x+9}" cy="{y+21}" r="2.2" stroke-width="0.7"/>'
                f'<path d="M{x-2} {y+9} v-10 M{x+2} {y+9} v-10" stroke-width="1.1"/>'
                f'<path d="M{x-14} {y-5} h28 v5 h-28 Z" stroke-width="1.2"/>'
                f'<path d="M{x-11} {y-5} v-26 q11 -4 22 0 v26" stroke-width="1.2"/>'
                f'<path d="M{x-8} {y-12} h16 M{x-9} {y-20} h18" stroke-width="0.5"/>'
                f'<path d="M{x-7} {y-34} h14 v6 h-14 Z" stroke-width="1.0"/>'
                f'<path d="M{x-6} {y-33} h12 v4 h-12 Z" fill="{SHD}" stroke="none"/>')
    def f3(x, y):   # 书格立筋 ×5
        b = []
        for i2 in range(5):
            xx = x - 44 + i2 * 20
            b.append(f'<path d="M{xx} {y} v-30 l7 -4 v30 Z" stroke-width="1.1"/>')
        b.append(f'<path d="M{x-44} {y} h80" stroke-width="0.5" stroke-dasharray="3 3"/>')
        return "".join(b)
    def f4(x, y):   # 书格层板（进深 180，层高 320 / 260）
        b = []
        for i2 in range(3):
            yy = y - i2 * 11
            b.append(f'<path d="M{x-48} {yy} h80 l10 -6 h-80 Z" stroke-width="1.2"/>')
            b.append(f'<path d="M{x-46} {yy-1} h74 l7 -4 h-74 Z" fill="{SHD}" stroke="none"/>')
        b.append(f'<path d="M{x+36} {y-24} l10 -6 M{x+42} {y-30} v4 M{x+42} {y-26} l-4 -2" stroke-width="0.7"/>')
        return "".join(b)
    def f5(x, y):   # 铁皮宝箱（尽端一格）
        return (f'<path d="M{x-20} {y} h34 v20 h-34 Z M{x-20} {y} l9 -6 h34 l-9 6 M{x+14} {y} l9 -6 v20 l-9 6" stroke-width="1.4"/>'
                f'<path d="M{x+13} {y+1} l7 -5 v18 l-7 5 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-20} {y+7} h34 M{x-4} {y+7} h6 v6 h-6 Z" stroke-width="0.9"/>'
                f'<path d="M{x-20} {y} q17 -12 34 0" stroke-width="1.0"/>')
    def f6(x, y):   # 瓷银茶器（台角明放）
        return (f'<path d="M{x-24} {y} h44 l6 -4 h-44 Z" stroke-width="1.0"/>'
                f'<path d="M{x-16} {y-2} q0 -13 9 -13 q9 0 9 13 Z" stroke-width="1.3"/>'
                f'<path d="M{x-4} {y-14.6} q3 -5 7 -4 M{x-16} {y-8} q-6 2 -5 6 M{x-8} {y-15} v-4" stroke-width="0.8"/>'
                f'<path d="M{x+4} {y-2} q0 6 5 6 q5 0 5 -6 Z M{x+14} {y-2} q0 6 5 6 q5 0 5 -6 Z" stroke-width="0.9"/>'
                f'<path d="M{x-14} {y-4} q7 3 14 0" stroke-width="0.5"/>')
    legend = [(1, "写字台钢架 + 1.5m 台面板，台面高 740"),
              (2, "人体工学椅 · 总高 ≤1300，升到顶不碰床板"),
              (3, "书格立筋 ×5，贴既有结构上墙"),
              (4, "书格层板：进深 180，层高 320 / 260 两档"),
              (5, "尽端一格的铁皮宝箱"),
              (6, "台角明放的瓷银茶器（认了磕碰与氧化）")]
    items = [(f1, None), (f2, None), (f3, None), (f4, None), (f5, None), (f6, None)]
    lead = [(-48, 2), (-22, -18), (-42, -14), (-44, -18), (-24, 6), (-20, -12)]
    return ex2(pfx, "写字台与连续书格", "0209-2", 4, legend,
               "浅格逼着书脊全部朝外，只放最近常翻的书", items, lead)


# =========================================================================
#  0101-1 hw 胡桃木展台与黑胡桃托盘
# =========================================================================
def p0101_1():
    pfx = "p0101-1"; SHD = SH(pfx)
    def f1(x, y):   # 手刨胡桃木托架 ×2
        return (f'<path d="M{x-44} {y} l-14 -32 l26 -4 l10 36 Z M{x+8} {y-8} l-14 -32 l26 -4 l10 36 Z" stroke-width="1.5"/>'
                f'<path d="M{x-42} {y-2} l-10 -25 l17 -3 l8 28 Z" fill="{SHD}" stroke="none"/>'
                f'<circle cx="{x-50}" cy="{y-20}" r="2" stroke-width="0.8"/><circle cx="{x+2}" cy="{y-28}" r="2" stroke-width="0.8"/>'
                f'<path d="M{x-60} {y-32} h-10 M{x-6} {y-40} h-10" stroke-width="0.6" stroke-dasharray="2 2"/>')
    def f2(x, y):   # 薄抽屉层（历代原型卡）
        return (f'<path d="M{x-58} {y+6} h96 l24 -14 h-96 Z" stroke-width="1.5"/>'
                f'<path d="M{x-58} {y+6} v12 h96 v-12 M{x+38} {y+18} l24 -14 v-12" stroke-width="1.2"/>'
                f'<path d="M{x+39} {y+17} l22 -13 v-11 l-22 13 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-12} {y+12} h12" stroke-width="1.3"/>'
                f'<path d="M{x-34} {y-2} h16 l6 -4 h-16 Z M{x-14} {y-6} h16 l6 -4 h-16 Z M{x+6} {y-10} h16 l6 -4 h-16 Z" stroke-width="0.8"/>')
    def f3(x, y):   # 倾斜 12° 台面（台高 900）
        return (f'<path d="M{x-60} {y+8} h96 l24 -14 h-96 Z" stroke-width="1.5"/>'
                f'<path d="M{x-60} {y+8} v5 h96 v-5 M{x+36} {y+13} l24 -14 v-5" stroke-width="1.1"/>'
                f'<path d="M{x-56} {y+2} l7 -12 M{x+28} {y+2} l7 -12" stroke-width="0.6" stroke-dasharray="2 2"/>'
                f'<path d="M{x-56} {y+2} a16 16 0 0 1 7 -12" stroke-width="0.6"/>')
    def f4(x, y):   # 黑胡桃托盘 30×20
        return (f'<path d="M{x-46} {y+6} h72 l20 -12 h-72 Z" stroke-width="1.4"/>'
                f'<path d="M{x-40} {y+3} h62 l14 -8 h-62 Z" stroke-width="0.9"/>'
                f'<path d="M{x-46} {y+6} h72 l20 -12 h-72 Z M{x-40} {y+3} h62 l14 -8 h-62 Z" fill="{SHD}" stroke="none" fill-rule="evenodd"/>'
                f'<path d="M{x-10} {y+2} l14 -8" stroke-width="0.6" stroke-dasharray="3 3"/>')
    def f5(x, y):   # 1.5mm 薄毛毡内衬 + 18mm 指槽
        return (f'<path d="M{x-42} {y+4} h64 l18 -10 h-64 Z" stroke-width="1.2"/>'
                f'<path d="M{x-38} {y+2} h32 l12 -7 h-32 Z" stroke-width="0.8"/>'
                f'<path d="M{x-42} {y+4} h64 l18 -10 h-64 Z M{x-38} {y+2} h32 l12 -7 h-32 Z" fill="{SHD}" stroke="none" fill-rule="evenodd"/>'
                f'<path d="M{x-26} {y+4} a7 3 0 0 0 12 0" stroke-width="1.1"/>'
                f'<path d="M{x-2} {y-1} h14 l8 -5 h-14 Z M{x+14} {y-2} h6" stroke-width="0.7"/>')
    def f6(x, y):   # PSK 卡 85.6×54 + 黄铜铭牌
        b = [f'<path d="M{x-34} {y+4} h40 l14 -8 h-40 Z" stroke-width="1.5"/>',
             f'<path d="M{x-34} {y+4} v3 h40 v-3 M{x+6} {y+7} l14 -8 v-3" stroke-width="1.0"/>',
             f'<path d="M{x-28} {y+1} h18 M{x-28} {y-1} h12" stroke-width="0.45"/>',
             f'<path d="M{x-6} {y-2} l2 1.6 l2 -1.6 l2 1.6 l2 -1.6 l2 1.6" stroke-width="0.55"/>',
             f'<path d="M{x-24} {y+3} a3 2 0 0 0 5 0" stroke-width="0.6"/>',
             f'<path d="M{x-4} {y+2} h10 v2 h-10 Z" stroke-width="0.5"/>',
             f'<path d="M{x+14} {y+12} h22 v8 h-22 Z" stroke-width="1.1"/>',
             f'<path d="M{x+17} {y+15} h16 M{x+17} {y+18} h10" stroke-width="0.5"/>',
             f'<path d="M{x+15} {y+13} h18 v6 h-18 Z" fill="{SHD}" stroke="none"/>']
        return "".join(b)
    legend = [(1, "手刨胡桃木托架 ×2（膨胀螺栓咬墙）"),
              (2, "薄抽屉层：放历代原型卡，一张一格"),
              (3, "前低后高倾斜 12° 台面，台面高 900"),
              (4, "黑胡桃托盘 30×20：左卡位 / 右小件位"),
              (5, "1.5mm 薄毛毡内衬，只压四边 + 18mm 指槽"),
              (6, "PSK 卡 85.6×54 + 黄铜铭牌 PSK Card No.1")]
    items = [(f1, None), (f2, None), (f3, None), (f4, None), (f5, None), (f6, None)]
    lead = [(-62, -18), (-64, -2), (-66, -2), (-52, 0), (-48, 0), (-40, -4)]
    return ex2(pfx, "胡桃木展台与黑胡桃托盘", "0101-1", 41, legend,
               "卡极薄，毛毡才要做到 1.5mm，并留一个指槽",
               items, lead, axis="M100 318 L392 40")


# =========================================================================
#  0101-2 hw 掠射射灯与放大压片
# =========================================================================
def p0101_2():
    pfx = "p0101-2"; SHD = SH(pfx)
    def f1(x, y):   # 梁底可旋转安装座
        return (f'<path d="M{x-30} {y} h60 v12 h-60 Z M{x-30} {y} l16 -10 h60 l-16 10 M{x+30} {y} l16 -10 v12 l-16 10" stroke-width="1.5"/>'
                f'<path d="M{x+31} {y+1} l14 -9 v9 l-14 9 Z" fill="{SHD}" stroke="none"/>'
                f'<circle cx="{x-18}" cy="{y+6}" r="2" stroke-width="0.9"/><circle cx="{x+18}" cy="{y+6}" r="2" stroke-width="0.9"/>'
                f'<path d="M{x} {y-10} v-6 M{x-6} {y-14} a6 3 0 0 1 12 0" stroke-width="1.0"/>'
                f'<path d="M{x-12} {y-20} a12 6 0 0 1 24 0" stroke-width="0.6" stroke-dasharray="2 2"/>')
    def f2(x, y):   # 0-10V 恒流驱动器
        return (f'<path d="M{x-24} {y} h48 v20 h-48 Z M{x-24} {y} l12 -8 h48 l-12 8 M{x+24} {y} l12 -8 v20 l-12 8" stroke-width="1.5"/>'
                f'<path d="M{x+25} {y+1} l10 -7 v17 l-10 7 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-18} {y+7} h20 M{x-18} {y+13} h14" stroke-width="0.6"/>'
                f'<path d="M{x+24} {y+11} q12 2 14 10 M{x-24} {y+9} q-8 0 -10 6" stroke-width="0.8"/>')
    def f3(x, y):   # 俯仰云台关节（压到 15~25°）
        return (f'<path d="M{x-18} {y-16} v22 a18 8 0 0 0 36 0 v-22" stroke-width="1.4"/>'
                f'<circle cx="{x-18}" cy="{y}" r="3" stroke-width="1.0"/><circle cx="{x+18}" cy="{y}" r="3" stroke-width="1.0"/>'
                f'<path d="M{x} {y-20} v-10" stroke-width="1.2"/><circle cx="{x}" cy="{y-33}" r="3.5" stroke-width="1.2"/>'
                f'<path d="M{x-16} {y-26} a16 16 0 0 1 32 0" stroke-width="0.7" stroke-dasharray="2 2"/>'
                f'<path d="M{x-16} {y+6} a18 8 0 0 0 32 2 v3 a18 8 0 0 1 -32 -2 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x-30} {y+2} l-14 8 M{x-44} {y+10} l6 0 M{x-44} {y+10} l2 -5" stroke-width="0.8"/>')
    def f4(x, y):   # COB 灯体 3000K Ra≥95 12W + 散热鳍
        return (f'<ellipse cx="{x}" cy="{y-20}" rx="22" ry="8" stroke-width="1.5"/>'
                f'<path d="M{x-22} {y-20} v20 a22 8 0 0 0 44 0 v-20" stroke-width="1.4"/>'
                f'<path d="M{x-21} {y-14} h42 M{x-21} {y-8} h42 M{x-20} {y-2} h40" stroke-width="0.6"/>'
                f'<path d="M{x-20} {y-6} a22 8 0 0 0 40 2 v4 a22 8 0 0 1 -40 -2 Z" fill="{SHD}" stroke="none"/>'
                f'<circle cx="{x}" cy="{y-20}" r="6" stroke-width="1.0"/>'
                f'<circle cx="{x}" cy="{y-20}" r="2.5" stroke-width="0.8"/>')
    def f5(x, y):   # 15° 蜂窝防眩罩
        b = [f'<ellipse cx="{x}" cy="{y}" rx="20" ry="7" stroke-width="1.4"/>',
             f'<path d="M{x-20} {y} v6 a20 7 0 0 0 40 0 v-6" stroke-width="1.1"/>',
             f'<path d="M{x-18} {y+3} a20 7 0 0 0 36 2 v3 a20 7 0 0 1 -36 -2 Z" fill="{SHD}" stroke="none"/>']
        for (cx2, cy2) in ((-8, -2), (-2, -3), (4, -3), (10, -2), (-11, 1), (-5, 2), (1, 2), (7, 2), (13, 1)):
            b.append(f'<circle cx="{x+cx2}" cy="{y+cy2}" r="1.6" stroke-width="0.6"/>')
        return "".join(b)
    def f6(x, y):   # 毫米波存在传感器小板
        return (f'<path d="M{x-14} {y} h28 v16 h-28 Z" stroke-width="1.3"/>'
                f'<path d="M{x-10} {y+4} h8 v6 h-8 Z" stroke-width="0.8"/>'
                f'<path d="M{x-10} {y+4} h8 v6 h-8 Z" fill="{SHD}" stroke="none"/>'
                f'<path d="M{x+2} {y+5} h8 M{x+2} {y+8} h8 M{x+2} {y+11} h6" stroke-width="0.6"/>'
                f'<path d="M{x+18} {y+3} a7 7 0 0 1 0 10 M{x+22} {y} a11 11 0 0 1 0 16" stroke-width="0.8"/>')
    def f7(x, y):   # 可翻三倍放大压片（轴外）
        return (f'<path d="M{x-28} {y} h56 v5 h-56 Z" stroke-width="1.1"/>'
                f'<path d="M{x-24} {y} l10 -30 h44 l-8 30 Z" stroke-width="1.4"/>'
                f'<path d="M{x-18} {y-6} q10 -16 26 -20 M{x-13} {y-3} q10 -17 26 -21" stroke-width="0.5"/>'
                f'<circle cx="{x+2}" cy="{y-16}" r="8" stroke-width="0.8"/>'
                f'<path d="M{x-30} {y-22} q-14 10 -14 26 M{x-46} {y} l2 6 l6 -4" stroke-width="0.7" stroke-dasharray="3 3"/>')
    legend = [(1, "梁底可旋转安装座（350°）"),
              (2, "恒流驱动器 · 0-10V 调光，2 秒渐亮渐暗"),
              (3, "俯仰云台关节 ±45°：把入射角压到 15~25° 掠射"),
              (4, "COB 灯体 3000K · Ra≥95 · 12W + 散热鳍"),
              (5, "蜂窝防眩罩 · 15° 窄光束"),
              (6, "毫米波存在传感器小板"),
              (7, "可翻三倍放大压片，翻下时距卡面约 25mm")]
    items = [(f1, None), (f2, None), (f3, None), (f4, None), (f5, None), (f6, None), (f7, (108, 316))]
    # 前 6 件在爆炸轴上，第 7 件放左下空地
    n = 6
    pos6 = [along(i2, n) for i2 in range(6)]
    items = [(f1, pos6[0]), (f2, pos6[1]), (f3, pos6[2]), (f4, pos6[3]), (f5, pos6[4]), (f6, pos6[5]),
             (f7, (330, 300))]
    lead = [(-42, 2), (-36, 8), (-40, -30), (-34, -14), (-32, 2), (-20, 4), (26, -18)]
    return ex2(pfx, "掠射射灯与放大压片", "0101-2", 4, legend,
               "卡太薄，顶光直打只剩一片反光",
               items, lead, axis="M90 322 L416 26")


# =========================================================================
#  逻辑：流程图 + 海报
# =========================================================================
FLOW_NODES = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44), ("step", 30, 130, 110, 40),
              ("dia", 172, 128, 116, 48), ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
              ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40), ("pill", 175, 312, 130, 30)]
FLOW_EDGES_A = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
                ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
                ("M85 170 V228", True), ("M285 250 H328", False), ("M390 270 V327 H307", False),
                ("M85 270 V327 H173", True)]
FLOW_EDGES_B = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
                ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
                ("M85 170 V228", True), ("M230 270 V310", False), ("M390 270 V327 H307", False),
                ("M85 270 V327 H173", True)]


def p0209_3():
    t = [(85, 73, "滑门磁簧 · 落座存在", False),
         (230, 74, "WLED 预设", False), (230, 87, "迎接/写字/收工", True),
         (85, 147, "滑门一推", False), (85, 161, "两路给 40% 迎接光", False),
         (230, 149, "人落座了？", False), (230, 162, "座位存在传感器", True),
         (390, 147, "是 → 切写字档", False), (390, 161, "书格 25%／海报 60%", False),
         (85, 247, "手动调过亮度", False), (85, 261, "1 小时内不干预", False),
         (230, 247, "否 → 保持迎接档", False), (230, 261, "离位 15 分钟渐暗", False),
         (390, 247, "渐暗到 5% 夜灯", False), (390, 261, "再 30 分钟全灭", False),
         (240, 331, "写进 HA · 每日进入次数", False),
         (305, 146, "是", True), (236, 200, "否", True), (92, 200, "已手动", True)]
    return flow("p0209-3", "环绕洗墙调光", FLOW_NODES, FLOW_EDGES_A, t, "0209-3", 5)


def p0209_3p():
    main = "\n".join([
        # 左：滑门 + 磁簧
        '<path d="M44 150 h30 v104 h-30 Z" stroke-width="1.4"/>',
        '<path d="M50 150 q3 52 0 104 M56 150 q3 52 0 104 M62 150 q3 52 0 104 M68 150 q3 52 0 104" stroke-width="0.6"/>',
        '<path d="M42 254 h34 v5 h-34 Z" stroke-width="1.6"/>',
        '<path d="M40 144 h38" stroke-width="1.2"/><circle cx="78" cy="152" r="4" stroke-width="1.1"/>',
        '<path d="M82 148 a7 7 0 0 1 0 8" stroke-width="0.7"/>',
        # 中：控制器（两路）
        '<path d="M108 186 h46 v30 h-46 Z" stroke-width="1.4"/>',
        '<path d="M113 192 h20 M113 198 h14" stroke-width="0.6"/>',
        '<path d="M154 195 h12 M154 207 h12" stroke-width="1.0"/>',
        '<path d="M88 200 h18" stroke-width="1" stroke-dasharray="3 3"/><path d="M102 197 l5 3 l-5 3" stroke-width="1"/>',
        # 右：顶部灯带 + 顺墙淌下的光 + 书格 / 海报墙
        '<path d="M176 146 H320" stroke-width="1.6"/>',
        '<path d="M176 152 H320" stroke-width="0.8"/>',
        "".join(f'<path d="M{x} 154 v22" stroke-width="0.5"/>' for x in range(182, 320, 12)),
        '<path d="M178 180 h60 v76 h-60 Z" stroke-width="1.3"/>',
        '<path d="M178 196 h60 M178 212 h60 M178 228 h60 M178 244 h60" stroke-width="0.9"/>',
        "".join(f'<path d="M{182+i*5} 183 v10 M{182+i*5} 199 v10 M{182+i*5} 215 v10" stroke-width="0.5"/>' for i in range(9)),
        '<path d="M252 180 h30 v34 h-30 Z M288 180 h30 v34 h-30 Z M252 222 h66 v34 h-66 Z" stroke-width="1.3"/>',
        '<path d="M258 190 h18 M258 197 h14 M294 188 h18 M294 196 h12 M258 232 h54 M258 240 h44 M258 248 h50" stroke-width="0.5"/>',
        '<path d="M166 201 h10" stroke-width="1" stroke-dasharray="3 3"/><path d="M172 198 l5 3 l-5 3" stroke-width="1"/>',
        '<path d="M40 268 H320" stroke-width="1.2"/>',
        # 坐着的人（座位存在传感）
        '<circle cx="118" cy="222" r="7" stroke-width="1.3"/>',
        '<path d="M118 229 V250 h16 M126 250 v16 M112 250 v14 M118 236 l14 8" stroke-width="1.3"/>',
        '<path d="M104 250 h20 v4 h-20 Z M106 254 v12" stroke-width="1.0"/>',
    ])
    return poster("p0209-3p", "0209 · L3", "环绕洗墙调光", "光贴着墙往下淌，一盏都不照眼睛", main,
                  "滑门磁簧 + 落座存在 → 两路亮度配比 → 离位渐暗 → 全灭",
                  ["推门先给 40% 迎接光，坐下自动切写字档",
                   "书格与海报墙两路独立，光只打在墙面上",
                   "手动调过一次，一小时内自动逻辑不插手"],
                  "跑在：ESP32 + WLED · ESPHome 读磁簧 · 数据出口：HA 两个 light 实体",
                  "wled/WLED · esphome/esphome", 9)


def p0209_4():
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
             ("M85 170 V228", True), ("M230 270 V310", False), ("M390 270 V327 H307", False),
             ("M85 270 V327 H173", True)]
    t = [(85, 73, "手机随手记进 memos", False),
         (230, 74, "三类标签", False), (230, 87, "名言/电影/对话", True),
         (85, 147, "按标签分流归档", False), (85, 161, "攒满一季度", False),
         (230, 149, "到换季了？", False), (230, 162, "每季度筛一批", True),
         (390, 147, "是 → 打字机字体", False), (390, 161, "牛皮纸打印上墙", False),
         (85, 247, "另一条：CO2 兜底", False), (85, 261, "顶角一颗，不装通风", False),
         (230, 247, "否 → 继续攒素材", False), (230, 261, "下季度再说", False),
         (390, 247, "换下来的按日期", False), (390, 261, "收进铁皮宝箱", False),
         (240, 331, "超 1200ppm 推送提醒开门", False),
         (305, 146, "是", True), (236, 200, "否", True), (92, 200, "并行", True)]
    return flow("p0209-4", "换墙与透气", FLOW_NODES, edges, t, "0209-4", 6)


def p0209_4p():
    main = "\n".join([
        # 左：手机 memos + 三类标签
        '<path d="M40 150 h44 v64 h-44 Z M45 156 h34 v50 h-34 Z" stroke-width="1.4"/>',
        '<path d="M50 164 h24 M50 172 h20 M50 180 h24 M50 188 h16" stroke-width="0.6"/>',
        '<path d="M38 228 h36 l6 8 l-6 8 h-36 Z M38 250 h36 l6 8 l-6 8 h-36 Z" stroke-width="1.1"/>',
        '<path d="M44 236 h22 M44 240 h14 M44 258 h22 M44 262 h14" stroke-width="0.5"/>',
        '<path d="M62 214 v10" stroke-width="1" stroke-dasharray="3 3"/><path d="M59 220 l3 5 l3 -5" stroke-width="1"/>',
        # 中：打印机 → 牛皮纸
        '<path d="M108 178 h60 v26 h-60 Z" stroke-width="1.4"/>',
        '<path d="M118 178 v-14 h40 v14" stroke-width="1.0"/>',
        '<path d="M120 204 v18 h36 v-18" stroke-width="1.2"/>',
        '<path d="M126 210 h24 M126 216 h18" stroke-width="0.5"/>',
        '<path d="M90 190 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M100 187 l5 3 l-5 3" stroke-width="1"/>',
        '<path d="M172 190 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M182 187 l5 3 l-5 3" stroke-width="1"/>',
        # 右：海报墙（三类）+ 铁皮宝箱
        '<path d="M194 150 h56 v44 h-56 Z M258 150 h58 v44 h-58 Z M194 200 h56 v40 h-56 Z M258 200 h58 v40 h-58 Z" stroke-width="1.3"/>',
        '<path d="M202 160 v26 M210 160 v26 M218 160 v26 M226 160 v20" stroke-width="0.5"/>',
        '<circle cx="286" cy="164" r="6" stroke-width="0.8"/><path d="M266 186 h40 M286 170 v10" stroke-width="0.6"/>',
        '<path d="M202 210 h40 M202 218 h32 M202 226 h38" stroke-width="0.5"/>',
        '<path d="M266 210 h40 M266 218 h28 M266 226 h36" stroke-width="0.5"/>',
        # 铁皮宝箱（旧海报归档）
        '<path d="M206 254 h56 v22 h-56 Z M206 254 q28 -14 56 0 M228 262 h12 v8 h-12 Z" stroke-width="1.3"/>',
        '<path d="M250 246 l16 -8" stroke-width="0.9" stroke-dasharray="3 3"/><path d="M262 236 l5 1 l-2 5" stroke-width="0.9"/>',
        # CO2 传感器（顶角）
        '<path d="M282 246 h34 v26 h-34 Z" stroke-width="1.3"/>',
        '<path d="M287 252 h24 M287 257 h24 M287 262 h16" stroke-width="0.7"/>',
        '<path d="M299 246 v-8 M290 240 a12 12 0 0 1 18 0 M286 234 a18 18 0 0 1 26 0" stroke-width="0.7"/>',
        '<path d="M40 284 H320" stroke-width="1.2"/>',
    ])
    return poster("p0209-4p", "0209 · L4", "换墙与透气", "每季度换一批句子，顺便看一眼 CO2", main,
                  "memos 三类标签 → 每季度筛一批 → 打印上墙 → 旧的收进宝箱",
                  ["名言、电影、对话三类分流，换季各挑几张",
                   "换下来的按日期收进尽端那格铁皮宝箱",
                   "不装通风，只靠一颗 CO2 传感器提醒推门"],
                  "跑在：memos + ESPHome(SCD40) · 数据出口：HA CO2 曲线",
                  "usememos/memos · esphome/esphome", 10)


def p0101_3():
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V200 H85 V228", False), ("M390 170 V228", False),
             ("M330 250 H287", False), ("M230 270 V310", False), ("M85 270 V327 H173", False),
             ("M450 250 Q470 250 470 160 Q470 140 452 140", True)]
    t = [(85, 73, "毫米波每 200ms 上报", False),
         (230, 74, "HA 实体", False), (230, 87, "occupancy·lx", True),
         (85, 147, "读展台前 3m 有没有人", False), (85, 161, "读环境照度", False),
         (230, 149, "有人且 &lt; 30lx？", False), (230, 162, "白天不打扰", True),
         (390, 147, "是 → 掠射射灯 2 秒", False), (390, 161, "渐亮到 80%", False),
         (85, 247, "否 → 保持关闭", False), (85, 261, "卡留在暗处", False),
         (230, 247, "无人后计时 3 分钟", False), (230, 261, "5 秒渐暗到 0", False),
         (390, 247, "凑近不动也算有人", False), (390, 261, "检测到即续期", False),
         (240, 331, "回到候客状态，等下一个人", False),
         (305, 146, "是", True), (238, 192, "否", True),
         (390, 104, "传感器离线兜底：按日落到 23 点定时常亮", True)]
    return flow("p0101-3", "人近感应亮灯", FLOW_NODES, edges, t, "0101-3", 5)


def p0101_3p():
    main = "\n".join([
        # 左：走近的人
        '<circle cx="66" cy="176" r="9" stroke-width="1.5"/>',
        '<path d="M66 185 V214 M66 194 L54 206 M66 194 L80 202 M66 214 L56 238 M66 214 L78 236" stroke-width="1.5"/>',
        '<path d="M48 200 q-4 8 0 16 M42 196 q-6 12 0 24" stroke-width="0.7" stroke-dasharray="2 2"/>',
        # 中：毫米波板
        '<path d="M120 150 h40 v24 h-40 Z M126 156 h10 v8 h-10 Z" stroke-width="1.4"/>',
        '<path d="M140 158 h12 M140 162 h12 M140 166 h8" stroke-width="0.7"/>',
        '<path d="M114 156 a10 10 0 0 0 0 12 M108 152 a15 15 0 0 0 0 20 M102 148 a20 20 0 0 0 0 28" stroke-width="0.9"/>',
        # 右：射灯压低角度 + 光掠过卡面 + 长影子
        '<path d="M196 134 v10" stroke-width="1.3"/>',
        '<path d="M186 144 l22 -5 l9 15 l-22 7 Z" stroke-width="1.4"/>',
        '<path d="M188 145 l18 -4 l7 12 l-18 6 Z" fill="url(#p0101-3p-shade)" stroke="none"/>',
        '<path d="M211 154 L292 226 M214 152 L300 214 M208 157 L286 236" stroke-width="0.7"/>',
        # 托盘 + 卡 + 小件
        '<path d="M180 240 h120 l14 24 h-148 Z" stroke-width="1.4"/>',
        '<path d="M196 246 h44 l6 14 h-48 Z" stroke-width="1.5"/>',
        '<path d="M200 250 h30 M200 254 h20 M232 249 l2 2 l2 -2 l2 2 l2 -2" stroke-width="0.5"/>',
        '<path d="M246 260 l40 4 l1 3 h-42 Z" fill="url(#p0101-3p-shade)" stroke="none"/>',
        '<path d="M246 260 L286 264" stroke-width="0.6"/>',
        '<path d="M256 246 h10 v3 h-10 Z M272 246 h9 v3 h-9 Z M286 247 h8 v3 h-8 Z M258 253 h9 v3 h-9 Z M274 253 h10 v3 h-10 Z" stroke-width="0.8"/>',
        '<path d="M268 249 l8 1 l0 2 l-8 -1 Z M283 250 l8 1 l0 2 l-8 -1 Z" fill="url(#p0101-3p-shade)" stroke="none"/>',
        '<path d="M96 168 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M106 165 l5 3 l-5 3" stroke-width="1"/>',
        '<path d="M166 162 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M176 159 l5 3 l-5 3" stroke-width="1"/>',
        '<path d="M40 276 H320" stroke-width="1.2"/>',
    ])
    return poster("p0101-3p", "0101 · L3", "人近感应亮灯", "你一走近，光就只落在那张卡上", main,
                  "毫米波存在 → 照度判断 → 掠射射灯 2 秒渐亮 → 3 分钟无人渐暗",
                  ["毫米波看得见凑近不动的人，不会看一半黑灯",
                   "环境亮度超过 30lx 的白天不打扰",
                   "传感器掉线自动退回日落定时常亮"],
                  "跑在：ESPHome + HA 自动化 · 数据出口：occupancy 实体 / 灯光状态",
                  "EverythingSmartHome/everything-presence-lite", 9)


def p0101_4():
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V200 H85 V228", False), ("M390 170 V228", False),
             ("M330 250 H287", False), ("M230 270 V310", False), ("M85 270 V327 H173", False),
             ("M30 250 Q10 250 10 150 Q10 130 28 130", True)]
    t = [(85, 73, "树莓派上电自启", False),
         (230, 74, "U 盘 / 目录", False), (230, 87, "视频 + 分解图", True),
         (85, 147, "按文件名排序", False), (85, 161, "读入播放列表", False),
         (230, 149, "展台前有人？", False), (230, 162, "来自 HA 存在状态", True),
         (390, 147, "是 → 放野外实测视频", False), (390, 161, "有声 · 单集循环", False),
         (85, 247, "否 → 静音放分解图", False), (85, 261, "收起→展开每张 8 秒", False),
         (230, 247, "凌晨 4 点扫新文件", False), (230, 261, "热重载播放列表", False),
         (390, 247, "无人 30 分钟", False), (390, 261, "屏幕休眠省电", False),
         (240, 331, "下次有人靠近即唤醒", False),
         (305, 146, "是", True), (238, 192, "否", True), (14, 222, "每天重载", True)]
    return flow("p0101-4", "侧屏轮播调度", FLOW_NODES, edges, t, "0101-4", 6)


def p0101_4p():
    main = "\n".join([
        # 左：U 盘 + 共享目录
        '<path d="M40 168 h26 v14 h-26 Z M66 171 h12 v8 h-12 Z" stroke-width="1.3"/>',
        '<path d="M44 196 h16 l4 5 h22 v26 h-42 Z" stroke-width="1.3"/>',
        '<path d="M50 210 h28 M50 216 h20" stroke-width="0.6"/>',
        '<path d="M56 182 v12" stroke-width="0.9" stroke-dasharray="3 3"/>',
        # 中：树莓派
        '<path d="M116 178 h56 v36 h-56 Z" stroke-width="1.4"/>',
        '<path d="M122 184 h18 v10 h-18 Z" stroke-width="0.8"/>',
        '<path d="M122 184 h18 v10 h-18 Z" fill="url(#p0101-4p-shade)" stroke="none"/>',
        '<path d="M146 186 h20 M146 190 h20 M146 194 h14 M122 200 h44 M122 206 h30" stroke-width="0.6"/>',
        '<path d="M96 196 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M106 193 l5 3 l-5 3" stroke-width="1"/>',
        '<path d="M178 196 h14" stroke-width="1" stroke-dasharray="3 3"/><path d="M188 193 l5 3 l-5 3" stroke-width="1"/>',
        # 右：7 寸小屏，屏上放卡的收起→展开分解图
        '<path d="M200 152 h116 v78 h-116 Z" stroke-width="1.6"/>',
        '<path d="M206 158 h104 v66 h-104 Z" stroke-width="0.8"/>',
        '<path d="M214 176 h34 v22 h-34 Z" stroke-width="1.3"/>',
        '<path d="M218 181 h20 M218 186 h14 M240 175 l2 2 l2 -2 l2 2" stroke-width="0.5"/>',
        '<path d="M252 186 h14" stroke-width="0.8" stroke-dasharray="2 2"/><path d="M262 183 l4 3 l-4 3" stroke-width="0.8"/>',
        '<path d="M272 170 h10 v3 h-10 Z M290 170 h9 v3 h-9 Z M272 180 h8 v3 h-8 Z M288 180 h11 v3 h-11 Z M272 190 h12 v3 h-12 Z M290 190 h8 v3 h-8 Z" stroke-width="0.8"/>',
        '<path d="M214 208 h96" stroke-width="0.5"/>',
        '<path d="M220 214 h30 M258 214 h48" stroke-width="0.5"/>',
        '<path d="M246 230 h24 v16 h-24 Z M240 246 h36" stroke-width="1.2"/>',
        # 展台前的人（存在状态）
        '<circle cx="120" cy="240" r="8" stroke-width="1.3"/><path d="M120 248 v18 M120 254 l-10 8 M120 254 l10 8 M120 266 l-8 14 M120 266 l8 14" stroke-width="1.3"/>',
        '<path d="M134 250 h56" stroke-width="0.9" stroke-dasharray="3 3"/><path d="M186 247 l5 3 l-5 3" stroke-width="0.9"/>',
        '<path d="M40 284 H320" stroke-width="1.2"/>',
    ])
    return poster("p0101-4p", "0101 · L4", "侧屏轮播", "插电就放，没人管它也不会停", main,
                  "共享目录播放列表 → 树莓派循环 → 有人放实测视频 / 无人放分解图",
                  ["开机自启不用登录，新素材拷进目录就行",
                   "无人时静音循环这张卡的收起→展开分解图",
                   "无人 30 分钟屏幕休眠，来人 1 秒内唤醒"],
                  "跑在：树莓派 + Anthias · 数据出口：HA 媒体状态 / 播放日志",
                  "Screenly/Anthias", 10)


if __name__ == "__main__":
    open("illos/0209.svg", "w", encoding="utf-8").write(m0209())
    open("illos/0101.svg", "w", encoding="utf-8").write(m0101())
    for fn, name in ((p0209_1, "0209-1"), (p0209_2, "0209-2"), (p0101_1, "0101-1"), (p0101_2, "0101-2")):
        open(f"parts/{name}.svg", "w", encoding="utf-8").write(fn())
    for fn, name in ((p0209_3, "0209-3"), (p0209_3p, "0209-3-poster"), (p0209_4, "0209-4"),
                     (p0209_4p, "0209-4-poster"), (p0101_3, "0101-3"), (p0101_3p, "0101-3-poster"),
                     (p0101_4, "0101-4"), (p0101_4p, "0101-4-poster")):
        open(f"parts/{name}.svg", "w", encoding="utf-8").write(fn())
    print("ok all")
