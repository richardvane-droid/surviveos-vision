"""p34util — 区域 03（阁楼间）/ 04（阁楼仓库）拆解图脚本共用的小构件。
不改动 hand3d / props / partdraw，只在自己这层拼零件。
阁楼是 45° 坡顶、核心区净高 2060：坡顶一律用 gable() 画端面三角（放在装配体侧面），
不要在装配体正上方铺整块斜面，否则从上往下的相机会把主体全挡住。
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from p01util import merge, rot, mv, prism, audit, screw, rope  # noqa: F401  (转出去给各脚本用)

ROOF = 2060.0          # 阁楼核心区净高 / 45° 坡顶的直角边


def ghost(s):
    """标成背景件：不排线。接受单个 Solid 或列表。"""
    if isinstance(s, Solid):
        s.shade = False
        return s
    for x in s:
        x.shade = False
    return s


def gable(pos=(0, 0, 0), run=ROOF, t=50, flip=False, name="45° 斜顶"):
    """45° 坡顶端面三角（直角边 run），躺在 YZ 平面里，沿 X 厚 t。
    flip=False：直角在 (y0,z0)，斜边从 (y0, z0+run) 落到 (y0+run, z0)，即屋面朝 +Y 方向下坡。
    flip=True ：镜像，屋面朝 -Y 下坡。
    """
    if flip:
        sec = [(0, 0), (run, 0), (run, run)]
    else:
        sec = [(0, 0), (run, 0), (0, run)]
    s = prism(sec, t, "x", pos, name)
    s.shade = False
    return s


def slope_frame(solids, pitch=45.0, origin=(0, 0, 0)):
    """把在局部坐标（x 沿檐口、y 沿坡面向上、z 沿屋面外法线）里建好的零件贴到坡屋面上。"""
    return rot(solids, pitch, "x", origin)


def cone(r0, r1, h, pos=(0, 0, 0), seg=20, name="锥", cap=True):
    """圆台（Z 向）。pos 为底面圆心，r0 底半径、r1 顶半径。"""
    x, y, z = pos
    th = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    a = np.stack([x + r0 * np.cos(th), y + r0 * np.sin(th), np.full_like(th, z)], -1)
    b = np.stack([x + r1 * np.cos(th), y + r1 * np.sin(th), np.full_like(th, z + h)], -1)
    F, E = [], []
    for i in range(seg):
        j = (i + 1) % seg
        F.append([a[i], a[j], b[j], b[i]])
        E.append((a[i], a[j])); E.append((b[i], b[j]))
    if cap:
        F.append(list(a[::-1])); F.append(list(b))
    for i in range(0, seg, max(1, seg // 6)):
        E.append((a[i], b[i]))
    return Solid(F, E, name)


def seg_tube(a, b, r=8, seg=10, name="管"):
    """任意方向的一段圆管。"""
    a = np.asarray(a, float); b = np.asarray(b, float)
    d = b - a; L = float(np.linalg.norm(d))
    if L < 1e-6:
        return None
    yaw = math.degrees(math.atan2(d[1], d[0]))
    pitch = math.degrees(math.atan2(d[2], math.hypot(d[0], d[1])))
    c = cyl(r, L, "x", (0, 0, 0), seg, name)
    c = rot(c, -pitch, "y", (0, 0, 0))
    c = rot(c, yaw, "z", (0, 0, 0))
    return c.moved(a)


def path_tube(pts, r=8, seg=8, name="管"):
    """折线管，合成一个 Solid。"""
    o = []
    for i in range(len(pts) - 1):
        s = seg_tube(pts[i], pts[i + 1], r, seg, name)
        if s is not None:
            o.append(s)
    return merge(o, name)


def arc_pts(c, rad, a0, a1, n=12, plane="xz"):
    """圆弧采样点。plane 决定弧面：'xz' / 'yz' / 'xy'。"""
    out = []
    for i in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * i / n)
        u, v = rad * math.cos(t), rad * math.sin(t)
        if plane == "xz":
            out.append((c[0] + u, c[1], c[2] + v))
        elif plane == "yz":
            out.append((c[0], c[1] + u, c[2] + v))
        else:
            out.append((c[0] + u, c[1] + v, c[2]))
    return out


def s_hook(pos, rad=22, wire=4, name="S 钩"):
    """S 钩：上下两个反向半圆。pos 是上钩圆心。"""
    x, y, z = pos
    up = arc_pts((x, y, z), rad, -20, 200, 10, "xz")
    dn = arc_pts((x + 2 * rad, y, z - 2 * rad), rad, 160, -20, 10, "xz")
    return merge([path_tube(up, wire, 6, name), path_tube(dn, wire, 6, name)], name)


def bucket(pos, r=180, h=400, name="桶"):
    x, y, z = pos
    return [cone(r * 0.86, r, h, (x, y, z), 20, name),
            cyl(r * 1.05, 24, "z", (x, y, z + h - 24), 20, name + "口沿")]


def grate(pos, w, d, t=28, n=14, name="钢格栅"):
    """钢格栅台面：一排竖扁钢 + 两根边框。"""
    x, y, z = pos
    o = [box((w, 30, t), (x, y, z), name + "框"), box((w, 30, t), (x, y + d - 30, z), name + "框")]
    for i in range(n):
        xx = x + (w - 12) * i / (n - 1)
        o.append(box((12, d, t), (xx, y, z), name))
    return [merge(o, name)]


def louver(pos, w, h, d=110, n=6, name="防雨百叶"):
    """百叶：一叠 20° 斜片 + 外框。"""
    x, y, z = pos
    o = [box((w, 26, h), (x, y, z), name + "框")]
    for i in range(n):
        zz = z + 40 + (h - 80) * i / (n - 1)
        bl = box((w - 40, d, 12), (x + 20, y, zz), name)
        o.append(rot(bl, -22, "x", (x + w / 2, y + d / 2, zz + 6)))
    return [merge(o, name)]


def battery_pack(pos, w=118, d=76, h=98, name="20V 大脚板电池"):
    """WORX 20V 大脚板电池：电芯壳 + 底部滑轨大脚板 + 电量灯。"""
    x, y, z = pos
    return [box((w, d, h), (x, y, z), name),
            box((w + 26, d + 18, 20), (x - 13, y - 9, z - 20), name + "大脚板"),
            box((w * 0.44, 8, 14), (x + w * 0.28, y - 8, z + h * 0.6), "电量灯")]


def spool(pos, r=100, w=66, name="耗材盘"):
    """耗材盘：两片侧板 + 中间料卷。"""
    x, y, z = pos
    return [cyl(r, 8, "y", (x, y, z), 20, name),
            cyl(r, 8, "y", (x, y + w, z), 20, name),
            cyl(r * 0.72, w - 16, "y", (x, y + 8, z), 18, name + "料")]


def gauge(pos, r=52, t=30, name="指针表"):
    """指针圆表：表壳 + 表盘 + 一根指针。"""
    x, y, z = pos
    o = [cyl(r, t, "y", (x, y, z), 20, name),
         cyl(r * 0.86, 5, "y", (x, y - 5, z), 20, name + "盘")]
    o.append(path_tube([(x, y - 8, z), (x + r * 0.5, y - 8, z + r * 0.46)], 3.5, 6, "指针"))
    return [merge(o, name)]


def label(pos, w=64, h=26, t=3, name="标签"):
    x, y, z = pos
    return box((w, t, h), (x, y, z), name)


def wall_piece(w, h, pos=(0, 0, 0), t=70, name="隔断"):
    s = box((w, t, h), pos, name)
    s.shade = False
    return s
