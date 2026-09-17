"""p56util — 区域 05（庭院）/ 06（草地）拆解图脚本共用的户外小构件。
不改动 hand3d / props / partdraw / p01util / p34util，只在自己这层拼零件。

户外场景的两条规矩：
  1. 地面只给装配体周围的一小块（`patch()` 已设 shade=False），要露埋深就用 `cut_soil()`
     切一小块土体剖面，把埋管 / 埋灯 / 根球露出来。
  2. 草、砾石、灌木这类只做少量简化实体示意（`tuft` / `gravel` / `shrub`），
     绝不铺满整片草地——面数一多 z-buffer 就慢，画面也糊。
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from p34util import (merge, rot, mv, prism, ghost, path_tube, seg_tube, cone,  # noqa: F401
                     arc_pts, s_hook, bucket, grate, louver, label, gauge,
                     audit, screw, rope)

_R = np.random.default_rng(20250915)


# ---------------------------------------------------------------- 地面 / 土体
def patch(w, d, pos=(0, 0, 0), t=60, name="地面"):
    """装配体周围的一小块地面（不排线，只做背景）。pos[2] 是地表标高。"""
    s = box((w, d, t), (pos[0], pos[1], pos[2] - t), name)
    s.shade = False
    return s


def cut_soil(w, d, h, pos, name="土体剖面"):
    """剖开的一小块土体：排线的实心块，用来露出埋深。pos 是最小角。"""
    return box((w, d, h), pos, name)


def gravel(pos, w, d, n=26, r=34, h=26, name="碎石"):
    """一小撮碎石/河卵石：扁圆柱随机撒在 w×d 的范围里，合成一个 Solid。"""
    o = []
    for i in range(n):
        x = pos[0] + _R.uniform(0, w)
        y = pos[1] + _R.uniform(0, d)
        rr = r * _R.uniform(0.62, 1.25)
        o.append(cyl(rr, h * _R.uniform(0.7, 1.3), "z", (x, y, pos[2]), 7, name))
    return merge(o, name)


# ---------------------------------------------------------------- 植物示意
def tuft(pos, h=520, r=140, n=7, w=16, name="草丛"):
    """一丛草：n 根从同一点斜着散开的细杆。"""
    o = []
    for i in range(n):
        a = i * 2 * math.pi / n + _R.uniform(-.3, .3)
        lean = _R.uniform(0.45, 1.0)
        tip = (pos[0] + math.cos(a) * r * lean, pos[1] + math.sin(a) * r * lean,
               pos[2] + h * _R.uniform(0.7, 1.15))
        o.append(seg_tube(pos, tip, w, 5, name))
    return merge([s for s in o if s is not None], name)


def grass_row(p0, p1, n=6, h=520, r=140, name="草丛"):
    """沿一条线撒 n 丛草。"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    o = []
    for i in range(n):
        t = (i + 0.5) / n
        p = p0 + (p1 - p0) * t
        p = p + np.array([_R.uniform(-90, 90), _R.uniform(-90, 90), 0])
        o.append(tuft(tuple(p), h * _R.uniform(0.75, 1.2), r, 6, 16, name))
    return merge(o, name)


def shrub(pos, r=260, h=380, name="灌木"):
    """一丛低灌木：三个错开的扁球（用圆台近似）。"""
    o = []
    for i in range(3):
        a = i * 2.1
        o.append(cone(r * 0.9, r * 0.35, h,
                      (pos[0] + math.cos(a) * r * 0.32, pos[1] + math.sin(a) * r * 0.32, pos[2]),
                      12, name))
    return merge(o, name)


def leafy(pos, r=70, n=5, name="叶"):
    """一小簇叶片：n 片薄斜板，用来示意藤蔓/菜苗，别当真。"""
    o = []
    for i in range(n):
        a = i * 2 * math.pi / n
        bl = box((r * 1.7, r * 1.1, 8), (pos[0] - r * .85, pos[1] - r * .55, pos[2] + i * 14), name)
        o.append(rot(bl, math.degrees(a) * 0.3 + 18, "y", pos))
    return merge(o, name)


def seedling(pos, h=240, name="菜苗"):
    """一株菜苗：一根短茎 + 三片叶。"""
    o = [cyl(12, h, "z", pos, 8, name)]
    for i in range(3):
        a = i * 2.2
        o.append(rot(box((190, 90, 9), (pos[0] - 20, pos[1] - 45, pos[2] + h - 30 - i * 40), name),
                     22 + i * 9, "y", (pos[0], pos[1], pos[2] + h - 26 - i * 40)))
        o[-1] = rot(o[-1], math.degrees(a), "z", (pos[0], pos[1], pos[2]))
    return merge(o, name)


def vine(p0, p1, n=7, amp=140, r=12, name="藤蔓"):
    """一根蜿蜒的藤：在 p0→p1 之间左右摆动的折线管。"""
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    pts = []
    for i in range(n + 1):
        t = i / n
        p = p0 + (p1 - p0) * t
        pts.append((p[0] + math.sin(t * 7.5) * amp, p[1], p[2]))
    return path_tube(pts, r, 6, name)


# ---------------------------------------------------------------- 柴 / 木作
def log(pos, r=60, L=400, axis="y", name="柴"):
    return cyl(r, L, axis, pos, 12, name)


def log_stack(x0, x1, z0, z1, y=0.0, depth=400.0, nx=4, nz=5, name="柴火"):
    """一格柴：切面朝 -Y 的原木阵列，合成一个 Solid。"""
    o = []
    w = (x1 - x0) / nx
    hz = (z1 - z0) / nz
    r = min(w, hz) * 0.47
    for i in range(nx):
        for j in range(nz):
            rr = r * _R.uniform(0.74, 1.0)
            o.append(cyl(rr, depth * _R.uniform(0.86, 1.0),
                         "y", (x0 + w * (i + .5), y, z0 + hz * (j + .5)), 11, name))
    return merge(o, name)


def corrugate(w, d, pos, ridges=7, r=46, name="波浪瓦"):
    """一片波浪瓦：底板 + 一排沿 X 的半圆瓦垄，合成一个 Solid。"""
    x, y, z = pos
    o = [box((w, d, 22), (x, y, z), name)]
    for i in range(ridges):
        o.append(cyl(r, w, "x", (x, y + d * (i + .5) / ridges, z + 22), 9, name))
    return merge(o, name)


def post_base(pos, s=150, name="镀锌柱脚"):
    """镀锌柱脚：底板 + 两片夹板，把木柱架空 50。"""
    x, y, z = pos
    return [box((s + 80, s + 80, 14), (x - 40, y - 40, z - 50), name),
            box((10, s, 120), (x - 6, y, z - 36), name),
            box((10, s, 120), (x + s - 4, y, z - 36), name)]


def plaque(pos, w=120, h=60, t=12, name="烙字木牌"):
    """挂牌：牌面 + 两根麻绳（挂到 up 高度）。"""
    x, y, z = pos
    return merge([box((w, t, h), (x, y, z), name),
                  cyl(4, 150, "z", (x + 14, y + t / 2, z + h), 6, name + "绳"),
                  cyl(4, 150, "z", (x + w - 14, y + t / 2, z + h), 6, name + "绳")], name)


# ---------------------------------------------------------------- 水 / 电
def valve(pos, r=26, name="阀"):
    """球阀：阀体 + 手柄。"""
    x, y, z = pos
    return merge([cyl(r, 96, "y", (x, y, z), 12, name),
                  box((26, 26, 34), (x - 13, y + 34, z + r), name),
                  box((22, 130, 16), (x - 11, y + 20, z + r + 34), name + "手柄")], name)


def dripper(pos, name="滴头"):
    x, y, z = pos
    return merge([cyl(11, 26, "z", (x, y, z), 8, name),
                  cyl(6, 18, "z", (x, y, z - 18), 8, name)], name)


def solenoid(pos, name="电磁阀"):
    """12V 电磁阀：阀体 + 线圈 + 两端接口。"""
    x, y, z = pos
    return merge([cyl(24, 150, "y", (x, y, z), 12, name),
                  cyl(34, 76, "z", (x, y + 75, z + 10), 14, name + "线圈"),
                  box((26, 18, 14), (x - 13, y + 66, z + 86), name + "接线")], name)


def disc_filter(pos, r=56, L=290, name="叠片过滤器"):
    """叠片过滤器：透明筒 + 上下接口 + 一圈叠片纹。"""
    x, y, z = pos
    o = [cyl(r, L, "y", (x, y, z), 16, name),
         cyl(r * 0.55, 60, "y", (x, y - 60, z), 12, name + "进口"),
         cyl(r * 0.55, 60, "y", (x, y + L, z), 12, name + "出口")]
    for i in range(5):
        o.append(cyl(r * 1.06, 10, "y", (x, y + 40 + i * 42, z), 16, name + "叠片"))
    return merge(o, name)


def esp_box(pos, w=190, d=120, h=230, name="防水控制盒"):
    """IP54 控制盒：盒体 + 透明盖 + 两个进线防水接头。"""
    x, y, z = pos
    o = [box((w, d, h), (x, y, z), name),
         box((w - 24, 8, h - 24), (x + 12, y - 8, z + 12), name + "透明盖")]
    for dx in (w * 0.3, w * 0.7):
        o.append(cyl(13, 40, "z", (x + dx, y + d / 2, z - 40), 10, name + "防水接头"))
    return o


def epaper_panel(pos, w=296 * 0.62, h=128 * 0.62, name="墨水屏"):
    x, y, z = pos
    return [box((w, 8, h), (x, y, z), name),
            box((w * 0.9, 4, h * 0.82), (x + w * 0.05, y - 4, z + h * 0.09), name + "显示区")]


# ---------------------------------------------------------------- 端盖 / 壳片
def disc(r, pos, axis="z", seg=24, name="端盖"):
    """实心圆盘：用三角扇拼成，能真正进 z-buffer（hand3d 的 cyl 端盖只画了一小片）。"""
    from hand3d import Solid
    x, y, z = pos
    th = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    if axis == "z":
        P = [np.array([x + r * math.cos(t), y + r * math.sin(t), z]) for t in th]
    elif axis == "y":
        P = [np.array([x + r * math.cos(t), y, z + r * math.sin(t)]) for t in th]
    else:
        P = [np.array([x, y + r * math.cos(t), z + r * math.sin(t)]) for t in th]
    c = np.array([x, y, z], float)
    F = [[c, P[i], P[(i + 1) % seg], c] for i in range(seg)]
    E = [(P[i], P[(i + 1) % seg]) for i in range(seg)]
    return Solid(F, E, name)


def capped_cyl(r, L, axis, pos, seg=24, name="圆柱"):
    """带真端盖的圆柱：柱面 + 两端实心盘，合成一个 Solid。"""
    from hand3d import cyl as _cyl
    d = {"x": (L, 0, 0), "y": (0, L, 0), "z": (0, 0, L)}[axis]
    p1 = (pos[0] + d[0], pos[1] + d[1], pos[2] + d[2])
    return merge([_cyl(r, L, axis, pos, seg, name),
                  disc(r, pos, axis, seg, name), disc(r, p1, axis, seg, name)], name)


def shell_band(r, L, pos, a0, a1, axis="y", seg=14, t=22, name="壳片"):
    """一段圆柱壳（只画 a0→a1 那条弧的壳），用来示意罐顶之类，不画整个圆。"""
    from hand3d import Solid
    x, y, z = pos
    th = np.radians(np.linspace(a0, a1, seg + 1))

    def pt(rad, a, s):
        if axis == "y":
            return np.array([x + rad * math.cos(a), y + s, z + rad * math.sin(a)])
        return np.array([x + s, y + rad * math.cos(a), z + rad * math.sin(a)])
    F, E = [], []
    for k in range(seg):
        a, b = th[k], th[k + 1]
        oa0, ob0, oa1, ob1 = pt(r, a, 0), pt(r, b, 0), pt(r, a, L), pt(r, b, L)
        ia0, ib0, ia1, ib1 = pt(r - t, a, 0), pt(r - t, b, 0), pt(r - t, a, L), pt(r - t, b, L)
        F += [[oa0, ob0, ob1, oa1], [ia1, ib1, ib0, ia0],
              [oa0, ob0, ib0, ia0], [oa1, ob1, ib1, ia1]]
        E += [(oa0, ob0), (oa1, ob1)]
    for a in (th[0], th[-1]):
        o0, o1, i1, i0 = pt(r, a, 0), pt(r, a, L), pt(r - t, a, L), pt(r - t, a, 0)
        F.append([o0, o1, i1, i0])
        E += [(o0, o1), (i0, i1), (o0, i0), (o1, i1)]
    return Solid(F, E, name)
