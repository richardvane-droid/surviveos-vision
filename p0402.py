"""0402 材料仓库 — 两张硬件爆炸图
0402-1 斜顶下长直木料架 / 0402-2 脚轮 A 字板材架
阁楼北条低矮带：45° 斜顶朝 +Y（北墙）下坡，站立带在 -Y（相机侧）。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, gable,
                     label, audit, ROOF)

SEG = 2400.0                    # 全长 7m，图示 3.6m 一段
EAVE = 1560.0                   # 檐口（净高 0）的 y 坐标


def fig1():
    S = []
    S.append(floor(3400, 2600, (-500, -900, 0)))
    S.append(gable((-560, EAVE - ROOF, 0), ROOF, 70, False, "45° 斜顶"))
    S.append(ghost(box((SEG + 700, 80, 400), (-500, EAVE, 0), "北墙")))

    # 立柱：三阶，越靠内越高（斜顶下 1.2m 净高那一线）
    TIERS = [(180.0, 1200.0, (170.0, 480.0, 800.0, 1120.0)),    # 阶三：最高，放 3m 长料
             (620.0, 820.0, (170.0, 470.0, 760.0)),             # 阶二
             (1060.0, 440.0, (170.0, 390.0))]                   # 阶一：最矮，放短料
    for y0, h, zs in TIERS:
        for i in range(5):
            x = i * 600.0
            S.append(box((60, 60, h), (x, y0, 0), "立柱"))
            # ② 托臂 40×40 木方，间距 600mm，挑向北墙
            for z in zs:
                S.append(box((40, EAVE - y0 - 20, 40), (x + 10, y0 + 60, z), "托臂 40×40"))
        S.append(box((SEG + 60, 60, 40), (0, y0, h - 40), "阶顶横梁"))

    # ① 木料：每层往上爆炸 200，层间垫木
    def stack(y0, z, ln, n, w, hh, name, lift):
        for k in range(n):
            S.append(box((ln, w, hh), (60 + k * (w + 40) * 0 + 40, y0 + 90 + k * (w + 46), z + lift), name))
        # ③ 每层垫木
        for xx in (300.0, 1500.0, 2700.0):
            S.append(box((90, (w + 46) * n, 36), (xx, y0 + 80, z + lift - 36), "垫木"))

    stack(180, 1120, 2300, 4, 90, 90, "3m 长方料", 260)
    stack(180, 800, 2380, 3, 150, 40, "长木板", 200)
    stack(620, 760, 1900, 4, 100, 60, "中长方料", 230)
    stack(620, 470, 2000, 3, 160, 34, "中长板", 180)
    stack(1060, 390, 1200, 4, 110, 70, "短料", 200)

    # ④ 踢脚板离地 100
    for y0, h, zs in TIERS:
        S.append(box((SEG + 60, 26, 100), (0, y0 - 26, 0), "踢脚板"))
    # ⑤ 每格标签
    for y0, h, zs in TIERS:
        for i in (0, 2, 4):
            S.append(label((i * 600 + 4, y0 - 30, h - 180), 54, 34, 5, "木种 / 厚度 / 年月标签"))

    items = [("①", "随斜顶分三阶，最高一阶 ≤1.2m", (1200, 300, 1120 + 260 + 90)),
             ("②", "托臂 40×40 木方，间距 600mm", (2430, 1320, 1140)),
             ("③", "每层垫木隔开，四面通风", (1545, 262, 1362)),
             ("④", "踢脚板离地 100mm，长料头朝通道", (1700, 1060 - 26, 50)),
             ("⑤", "每格标签：木种 / 厚度 / 购入年月", (1230, 152, 1037))]
    audit(items, S, -34, 26)
    print("saved", draw("0402-1", "斜顶下长直木料架", items, S,
                        note="顺 12.6m 长北墙做 7m 长料架（图示一段）；木料架空离地是防潮防变形的基本功，长料每 60cm 一个支点就不会弯",
                        sig="设想 · 0402", az=-34, el=26, fov=27))


def fig2():
    S = []
    BW, BD, AH = 1200.0, 600.0, 1180.0          # 底盘 1200×600，整架 \u22641.2m
    TILT = 10.0                                  # 靠背倾角 10\u00b0
    C0 = (BW / 2, BD / 2, 250.0)

    def rp(p, s2):
        """跟着靠背一起转 10\u00b0 的点。"""
        a2 = math.radians(-s2 * TILT)
        y, z = p[1] - C0[1], p[2] - C0[2]
        return (p[0], C0[1] + y * math.cos(a2) - z * math.sin(a2),
                C0[2] + y * math.sin(a2) + z * math.cos(a2))

    # 4 底盘 1200\u00d7600
    base = [box((BW, 80, 90), (0, 0, 150)), box((BW, 80, 90), (0, BD - 80, 150)),
            box((80, BD - 160, 90), (0, 80, 150)), box((80, BD - 160, 90), (BW - 80, 80, 150)),
            box((BW - 160, BD - 160, 40), (80, 80, 150))]
    S.append(merge(base, "\u5e95\u76d8 1200\u00d7600"))
    # 2 4 \u53ea 75mm \u5237\u8f66\u811a\u8f6e\uff08\u5411\u4e0b\u7206\u70b8\uff09
    CAS = []
    for (dx, dy) in ((70, 70), (BW - 70, 70), (70, BD - 70), (BW - 70, BD - 70)):
        S.append(box((120, 120, 26), (dx - 60, dy - 60, -130), "\u811a\u8f6e\u5e95\u677f"))
        S.append(box((46, 92, 74), (dx - 23, dy - 46, -204), "\u811a\u8f6e\u53c9"))
        S.append(cyl(40, 34, "x", (dx - 17, dy, -244), 18, "75mm \u811a\u8f6e"))
        S.append(box((84, 24, 30), (dx - 42, dy - 50, -290), "\u5237\u8f66\u7247"))
        CAS.append((dx - 17, dy - 40, -244))

    # A 字骨架：两组斜靠背，10\u00b0 倾角
    for s2 in (-1, 1):
        y0 = BD / 2 + s2 * 40
        for dx in (60.0, BW / 2 - 40, BW - 140):
            fr = box((80, 60, AH), (dx, y0 - (0 if s2 > 0 else 60), 240), "A 字立柱")
            S.append(rot(fr, -s2 * TILT, "x", C0))
        rail = box((BW, 60, 70), (0, y0 - (0 if s2 > 0 else 60), 240 + AH - 130), "靠背横杆")
        S.append(rot(rail, -s2 * TILT, "x", C0))

    # 1 板材：两侧各三张，沿 \u00b1Y 爆炸出来
    SH = {}
    for s2 in (-1, 1):
        for k in range(3):
            off = BD / 2 + s2 * (300 + k * 170) - (20 if s2 < 0 else 0)
            pl = box((BW - 120, 20, 1220), (60, off, 250), "多层板")
            S.append(rot(pl, -s2 * TILT, "x", C0))
            if k == 2:
                SH[s2] = rp((BW * 0.35, off + (20 if s2 > 0 else 0), 900), s2)
    # 3 中腔边角料（从中间空腔往上爆炸），按长度分 3 档
    for k, (ln, zz) in enumerate(((980.0, 1760.0), (680.0, 1610.0), (420.0, 1470.0))):
        for j in range(3):
            S.append(box((ln, 90, 28), (110 + k * 40, BD / 2 - 140 + j * 96, zz + j * 36), "\u8fb9\u89d2\u6599"))
    S.append(box((BW - 260, 300, 26), (130, BD / 2 - 150, 300), "\u4e2d\u8154\u5e95\u677f"))
    for dy in (BD / 2 - 150, BD / 2 + 124):
        S.append(box((BW - 260, 26, 280), (130, dy, 326), "\u4e2d\u8154\u9694\u677f"))

    items = [("\u2460", "\u4e24\u4fa7\u9760\u80cc\u503e\u89d2 10\u00b0\uff0c\u6574\u67b6\u9ad8 \u22641.2m", SH[-1]),
             ("\u2461", "4 \u53ea 75mm \u91cd\u578b\u5237\u8f66\u811a\u8f6e", CAS[0]),
             ("\u2462", "\u4e2d\u8154\u5b58\u8fb9\u89d2\u6599\uff0c\u6309\u957f\u5ea6\u5206 3 \u6863", (300, BD / 2 - 95, 1788)),
             ("\u2463", "\u5e95\u76d8 1200\u00d7600mm\uff0c\u6ee1\u8f7d 150kg \u5355\u4eba\u53ef\u63a8", (BW - 130, BD - 40, 240)),
             ("\u2464", "\u677f\u6750\u81ea\u91cd\u538b\u5411\u9760\u80cc\uff0c\u4e0d\u6ed1\u4e0d\u53d8\u5f62", rp((BW * 0.8, 960, 700), 1))]
    audit(items, S, -54, 22)
    print("saved", draw("0402-2", "\u811a\u8f6e A \u5b57\u677f\u6750\u67b6", items, S,
                        note="A \u5b57\u5f62\u8ba9\u677f\u6750\u4ee5 10\u00b0 \u503e\u89d2\u9760\u5728\u67b6\u4e0a\uff0c\u81ea\u91cd\u628a\u677f\u538b\u5411\u9760\u80cc\uff1b\u6574\u67b6\u9ad8\u5ea6\u538b\u5728 1.2m \u4ee5\u5185\uff0c\u9000\u8fdb\u659c\u9876\u4e0b\u90a3\u4e00\u7ebf",
                        sig="\u8bbe\u60f3 \u00b7 0402", az=-54, el=22, fov=27))


fig1()
fig2()
