"""0501 柴火堆墙 — 三张硬件爆炸图（hand3d 管线）
0501-1 杉木柴架总成 / 0501-2 分格标牌与引火兜 / 0501-3 柴堆回潮探头
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl
from props import wall
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, cone, audit,
                     patch, gravel, log, log_stack, corrugate, plaque, tuft)

POST = 100.0          # 10cm 方杉木柱
DEEP = 400.0          # 柴架进深 0.4m
HIGH = 1600.0         # 柴架高 1.6m
XS = [0.0, 850.0, 1700.0, 2550.0, 3400.0]    # 5 根柱 → 4 格 ×0.8m，总长 3.5m


# ---------------------------------------------------------------- 0501-1
def fig1():
    S = []
    S.append(patch(4900, 1700, (-800, -560, -150), 60))
    # 北头就是木屋南墙（柴架离它 30cm）
    S.append(wall(1400, 1900, 80, (-380, -400, -150), "y", "木屋南墙"))

    # ① 碎石带 15cm（铺在地面上，柴架立在上面）
    S.append(box((3900, 760, 150), (-200, -180, -150), "碎石带"))
    S.append(gravel((-180, -160, 0), 3860, 720, 30, 46, 26, "碎石"))

    # ② 两根横木（柴离地 20cm）
    for yy in (40.0, 240.0):
        S.append(box((3500, 150, 200), (0, yy, 0), "横木"))

    # ③ 杉木立柱 ×5 对 + 前后横档
    posts = []
    for x in XS:
        posts.append(box((POST, POST, HIGH), (x, 0, 0), "杉木立柱"))
        posts.append(box((POST, POST, HIGH), (x, DEEP - POST, 0), "杉木立柱"))
    for yy in (0.0, DEEP - 80):
        posts.append(box((3500, 80, 90), (0, yy, 1180), "横档"))
    S.append(merge(posts, "杉木立柱"))

    # ④ 四格柴火：整体向上爆炸 560
    UP = 560.0
    for i in range(4):
        x0, x1 = XS[i] + POST, XS[i + 1]
        S.append(log_stack(x0 + 10, x1 - 10, 200 + UP, 1500 + UP, 20, 360, 4, 5, "柴火"))

    # ⑤ 顶盖波浪瓦：前后各出檐 20cm，整体向上爆炸 1250
    RZ = HIGH + 1250
    roof = corrugate(3900, 800, (-200, -200, RZ), 7, 48, "波浪瓦")
    S.append(rot(roof, 7, "x", (1750, 200, RZ)))
    for x in (200.0, 1700.0, 3200.0):
        S.append(box((80, 820, 60), (x, -210, RZ - 70), "瓦下檩条"))

    items = [("①", "10cm 方杉木柱，4 格 ×0.8m", (1750, 0, 900)),
             ("②", "底铺 15cm 碎石带，防潮防白蚁", (1000, -180, -70)),
             ("③", "两根横木架空，柴火离地 20cm", (2300, 40, 120)),
             ("④", "四格码柴，切面朝东对着院子", (1250, 20, 1500 + UP - 60)),
             ("⑤", "旧波浪瓦前后出檐 20cm，只挡雨", (900, -140, RZ + 130))]
    audit(items, S, -64, 20)
    print("saved", draw("0501-1", "杉木柴架总成", items, S,
                        note="沿庭院西边界一字排开，总长 3.5m、高 1.6m；北头挨木屋南门，离木屋外墙至少 30cm",
                        sig="设想 · 0501", az=-64, el=20, fov=27))


# ---------------------------------------------------------------- 0501-2
def fig2():
    """柴架北端一格的细部：烙字木牌 + 旧渔网引火兜 + 侧面小黑板。"""
    S = []
    S.append(patch(2900, 1600, (-1000, -1100, 0), 60))

    # 一格骨架：柱 ×2 对 + 前后横档 + 两根横木
    fr = []
    for x in (0.0, 850.0):
        fr.append(box((POST, POST, HIGH), (x, 0, 0), "杉木立柱"))
        fr.append(box((POST, POST, HIGH), (x, DEEP - POST, 0), "杉木立柱"))
    for yy in (0.0, DEEP - 80):
        fr.append(box((950, 80, 90), (0, yy, 1180), "横档"))
    fr.append(box((950, 150, 200), (0, 40, 0), "横木"))
    fr.append(box((950, 150, 200), (0, 240, 0), "横木"))
    S.append(merge(fr, "杉木柴架"))

    # ⑤ 这一格是待烧区：香樟柴
    S.append(log_stack(120, 830, 200, 980, 20, 360, 4, 4, "香樟柴"))

    # ① 烙字杉木牌 12×6cm ×2：连麻绳整体爆炸到架子左前方的空处
    PY, PZ = -380.0, 700.0
    for x in (-790.0, -440.0):
        S.append(plaque((x, PY, PZ), 120, 60, 20, "烙字木牌"))
        S.append(seg_tube((x + 14, PY + 10, PZ + 210), (x + 106, PY + 10, PZ + 210), 6, 6, "麻绳"))

    # ② 旧渔网引火兜：向前爆炸到格子外
    BX, BY, BZ = 430.0, -800.0, 240.0
    _c = cone(150, 300, 460, (BX, BY, BZ), 14, "旧渔网兜"); _c.shade = False
    bag = [_c]
    for zz, rr in ((BZ + 6, 152.0), (BZ + 118, 189.0), (BZ + 230, 226.0),
                   (BZ + 342, 262.0), (BZ + 452, 298.0)):
        pts = [(BX + rr * math.cos(t), BY + rr * math.sin(t), zz) for t in np.linspace(0, 2 * math.pi, 19)]
        bag.append(path_tube(pts, 10, 5, "网箍"))
    for i in range(12):
        t = i * 2 * math.pi / 12
        t2 = t + 0.5
        bag.append(seg_tube((BX + 298 * math.cos(t), BY + 298 * math.sin(t), BZ + 452),
                            (BX + 152 * math.cos(t2), BY + 152 * math.sin(t2), BZ), 8, 5, "网绳"))
    bag.append(seg_tube((BX, BY, BZ + 452), (BX + 60, BY + 700, 1180), 10, 6, "吊绳"))
    S.append(merge([b for b in bag if b is not None], "旧渔网兜"))
    # 兜里的引火松枝和竹片
    twigs = []
    for i in range(12):
        a = i * 1.05
        p0 = (BX + math.cos(a) * 110, BY + math.sin(a) * 110, BZ + 330)
        p1 = (p0[0] + math.cos(a * 1.6) * 250, p0[1] + math.sin(a * 1.6) * 160, BZ + 760 + (i % 3) * 110)
        twigs.append(seg_tube(p0, p1, 14, 6, "引火松枝"))
    S.append(merge([t for t in twigs if t is not None], "引火松枝与竹片"))

    # ③ 侧面小黑板：钉在柱外侧，向 +X 爆炸
    BBX = 1330.0
    S.append(box((30, 420, 560), (BBX, 20, 560), "小黑板"))
    S.append(box((14, 356, 496), (BBX + 30, 52, 592), "板面"))
    S.append(box((26, 90, 26), (BBX + 26, 180, 528), "粉笔槽"))
    for zz in (700.0, 1000.0):
        S.append(seg_tube((BBX + 6, 210, zz), (960, 210, zz), 8, 6, "固定钉"))

    items = [("①", "烙字杉木牌 12×6cm，麻绳挂横档", (-440, PY, PZ + 34)),
             ("②", "旧渔网兜引火松枝与竹片", (BX, BY - 290, BZ + 300)),
             ("③", "架侧小黑板，粉笔记入库月份", (BBX + 44, 210, 800)),
             ("④", "麻绳系在前后两道横档上", (600, 0, 1225)),
             ("⑤", "待烧区紧挨木屋南门，取柴 8 步内", (500, 20, 900))]
    audit(items, S, -58, 17)
    print("saved", draw("0501-2", "分格标牌与引火兜", items, S,
                        note="四格按树种分开：香樟 / 栎木 / 竹子 / 引火松枝；黑板上的入库月份就是干燥计时的数据源",
                        sig="设想 · 0501", az=-58, el=17, fov=27))


# ---------------------------------------------------------------- 0501-3
def fig3():
    """柴堆中层缝隙里的小米温湿度计 + 架顶对照探头（放大到探头尺度）。"""
    S = []
    # 柴堆一角：3 列 ×3 层，中间缺一根就是塞探头的缝
    lg = []
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            lg.append(cyl(50 - (i % 2) * 5, 300, "y", (i * 118 + 60, 0, j * 128 + 60), 12, "柴火"))
    S.append(merge(lg, "柴堆中层"))

    # ① 透气小盒：盒体（四壁 + 底），沿 -Y 爆炸出缝隙
    BX, BY, BZ = 132.0, -430.0, 140.0
    bd = [box((96, 76, 12), (BX, BY, BZ), "透气小盒")]
    for s in (0, 1):
        bd.append(box((96, 8, 62), (BX, BY + s * 68, BZ + 12), "盒壁"))
        bd.append(box((8, 76, 62), (BX + s * 88, BY, BZ + 12), "盒壁"))
    S.append(merge(bd, "透气小盒"))

    # ② 盒盖 + 透气孔（向上爆炸）
    LZ = BZ + 300
    lid = [box((108, 88, 11), (BX - 6, BY - 6, LZ), "盒盖")]
    for i in range(4):
        for j in range(3):
            lid.append(cyl(7, 16, "z", (BX + 18 + i * 22, BY + 20 + j * 22, LZ - 3), 8, "透气孔"))
    S.append(merge(lid, "盒盖与透气孔"))

    # ③ LYWSD03MMC 43×43×12：立着放在盒里（爆炸到盒与盖之间）
    SX, SY, SZ = BX + 26, BY + 16, BZ + 140
    S.append(box((43, 12, 43), (SX, SY, SZ), "LYWSD03MMC"))
    S.append(box((33, 3, 26), (SX + 5, SY - 3, SZ + 10), "LCD 屏"))
    for i in range(3):
        S.append(box((22, 1.6, 2.4), (SX + 10, SY - 5, SZ + 15 + i * 7), "读数"))

    # ④ CR2032 纽扣电池：从背面拆出来，往 -X 爆炸
    CX, CY, CZ = SX - 165, SY + 6, SZ + 96
    S.append(cyl(20, 6, "y", (CX, CY, CZ), 18, "CR2032"))
    S.append(cyl(13, 3, "y", (CX, CY + 6, CZ), 14, "正极面"))
    S.append(box((34, 3, 10), (CX - 17, CY - 18, CZ - 28), "电池仓触片"))

    # ⑤ 架顶对照探头：柴堆上方一小段横档 + 同款小盒
    RX, RZ2 = -20.0, 420.0
    S.append(box((420, 90, 70), (RX, 10, RZ2), "架顶横档"))
    S.append(box((96, 76, 72), (RX + 250, -60, RZ2 + 70), "对照探头盒"))
    S.append(box((33, 3, 26), (RX + 276, -63, RZ2 + 102), "对照 LCD"))

    items = [("①", "透气小盒塞进柴堆中层缝隙", (BX + 88, BY + 38, BZ + 42)),
             ("②", "盒盖打透气孔，读的是柴缝空气", (BX + 48, BY + 40, LZ + 11)),
             ("③", "小米 LYWSD03MMC 刷 ATC 固件", (SX + 21, SY, SZ + 34)),
             ("④", "CR2032 纽扣电池，续航约一年", (CX + 20, CY + 3, CZ)),
             ("⑤", "架顶另放一颗，对照外界空气", (RX + 298, -60, RZ2 + 120))]
    audit(items, S, -54, 15)
    SL = [("", "", (66, 770)), ("", "", (66, 232)), ("", "", (66, 578)),
          ("", "", (66, 408)), ("", "", (1134, 300))]
    print("saved", draw("0501-3", "柴堆回潮探头", items, S, slots=SL,
                        note="蓝牙广播直连 HomeAssistant，每分钟一次温湿度；7 日均湿度 <70% 且入库满 8 个月才算可烧",
                        sig="设想 · 0501", az=-54, el=15, fov=27))


if __name__ == "__main__":
    import sys
    w = sys.argv[1:] or ["1", "2", "3"]
    if "1" in w: fig1()
    if "2" in w: fig2()
    if "3" in w: fig3()
