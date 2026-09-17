"""0305 自建 Voron 2.4 — 两张硬件爆炸图（0305-1 已单独出图）
0305-2 铝型材工作站与人体工学高度 / 0305-3 腔体排风与耗材干燥
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl, extrusion
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, spool,
                     louver, label, audit)

FW = FD = 500.0                # 工作站占地 0.5×0.5m
VC = 330.0                     # Voron 2.4 腔体外廓（250 行程 + 型材）
ZS = 985.0                     # 放打印机的 2020 层板顶面 → 腔口中心 1150


def voron(z0, name="Voron 2.4 打印仓"):
    """简化的 Voron 腔体：铝型材立方 + 热床 + 龙门 + 打印头 + 前门。"""
    o, S2 = [], 20.0
    for z in (z0, z0 + VC - S2):
        o += [extrusion(VC, "x", (0, 0, z), S2), extrusion(VC, "x", (0, VC - S2, z), S2),
              extrusion(VC - 2 * S2, "y", (0, S2, z), S2), extrusion(VC - 2 * S2, "y", (VC - S2, S2, z), S2)]
    for (x, y) in ((0, 0), (VC - S2, 0), (0, VC - S2), (VC - S2, VC - S2)):
        o.append(extrusion(VC - 2 * S2, "z", (x, y, z0 + S2), S2))
    o.append(box((250, 250, 8), (40, 40, z0 + 110), "热床"))
    o.append(extrusion(VC - 2 * S2, "x", (S2, VC / 2 - 10, z0 + 230), S2, "X 梁"))
    o.append(box((70, 58, 62), (VC / 2 - 35, VC / 2 - 29, z0 + 250), "打印头"))
    o.append(box((VC - 40, 6, VC - 60), (20, -6, z0 + 30), "前门亚克力"))
    return [merge(o, name)]


# ---------------------------------------------------------------- 0305-2
def fig2():
    S = []
    S.append(floor(2000, 1600, (-680, -1180, 0)))

    # ① 3030 立柱 ×4 + 横梁；② 2020 层板
    P = 30.0
    for (dx, dy) in ((0, 0), (FW - P, 0), (0, FD - P), (FW - P, FD - P)):
        S.append(extrusion(1700, "z", (dx, dy, 0), P, "3030 立柱"))
        S.append(box((54, 54, 26), (dx - 12, dy - 12, -26), "可调地脚"))
    for z in (140.0, 520.0, ZS - 20, 1700.0 - P):
        for pos, ax, L in (((0, 0, z), "x", FW), ((0, FD - 20, z), "x", FW),
                           ((0, 20, z), "y", FD - 40), ((FW - 20, 20, z), "y", FD - 40)):
            S.append(extrusion(L, ax, pos, 20, "2020 层板梁"))

    # ④ 台面木板（从 2020 层板上抬起 320）
    S.append(box((FW + 60, FD + 60, 22), (-30, -30, ZS + 320), "台面木板"))
    S.append(box((FW + 20, FD + 20, 18), (-10, -10, 560), "下层木板"))

    # ② 打印仓：坐在 2020 层板上，整机爆炸抬到工作站上方
    S += voron(2020.0)
    S.append(ghost(box((VC, VC, 8), (85, 85, ZS + 20), "打印仓落位")))

    # ③ 侧板铰链 + 磁扣：两片可翻侧板向外爆炸
    for sx, s in ((-680.0, -1), (FW + 680.0, 1)):
        S.append(box((8, FD, 1050), (sx, 0, 560), "可翻侧板"))
        for zz in (700.0, 1350.0):
            S.append(cyl(22, 90, "y", (sx + 4, 30, zz), 12, "铰链"))
            S.append(box((30, 44, 44), (sx - 18 if s < 0 else sx - 4, FD - 70, zz - 200), "磁扣"))

    # ⑤ 下层：耗材干燥箱位 + 工具抽屉 + 可整块抽出的接屑盘
    S.append(box((FW - 40, FD - 60, 300), (20, -420, 620), "耗材干燥箱"))
    S.append(box((FW - 90, 14, 180), (45, -434, 680), "干燥箱视窗"))
    S.append(box((FW - 40, FD - 60, 210), (20, -760, 220), "工具抽屉"))
    S.append(cyl(10, 200, "x", (150, -774, 325), 10, "抽屉拉手"))
    S.append(box((FW + 40, FD - 40, 50), (-20, -1000, 60), "接屑盘"))

    items = [("①", "3030 做立柱横梁，2020 做层板", (P / 2, P / 2, 1250)),
             ("②", "打印仓坐在层板上，占地 0.5×0.5m", (VC * 0.4, 0, 2020 + VC * 0.5)),
             ("③", "侧板铰链 + 磁扣，整块翻开清碎屑", (-680 + 4, 200, 1100)),
             ("④", "台面与摩擦面覆木板，防划伤露白", (FW * 0.4, FD * 0.4, ZS + 342)),
             ("⑤", "下层：干燥箱 / 抽屉 / 可抽接屑盘", (FW / 2, -434, 770))]
    audit(items, S, -54, 20)
    print("saved", draw("0305-2", "铝型材工作站与人体工学高度", items, S,
                        note="欧标喷砂黑型材（0805 定标）；腔口中心抬到 1100～1200，站着平视就能看进打印仓，不用蹲下去",
                        sig="设想 · 0305", az=-54, el=20, fov=27))


# ---------------------------------------------------------------- 0305-3
def fig3():
    S = []
    # 腔体（背景件，只给一个轮廓）+ 顶部 100mm 排风口
    S += [ghost(x) for x in voron(900.0)]
    PX, PY = 165.0, 165.0
    S.append(cyl(58, 90, "z", (PX, PY, 1230), 18, "100mm 排风口"))
    S.append(box((190, 190, 14), (PX - 95, PY - 95, 1230), "排风口法兰"))

    # 100mm 铝箔管：出腔顶 → 上到天花 → 横过 1.5m → 天窗边排气口
    ZC = 1780.0
    S.append(path_tube([(PX, PY, 1400), (PX, PY, ZC)], 52, 14, "铝箔排风管"))
    S.append(path_tube([(PX, PY, ZC), (760, PY, ZC)], 52, 14, "铝箔排风管"))
    S.append(path_tube([(1180, PY, ZC), (1560, PY, ZC)], 52, 14, "铝箔排风管"))
    S.append(path_tube([(1900, PY, ZC), (2260, PY, ZC)], 52, 14, "铝箔排风管"))
    # ② 12V 静音管道风扇（从管路中段爆炸抬起）
    FZ = ZC + 520
    S.append(cyl(66, 300, "x", (880, PY, FZ), 20, "12V 静音管道风扇"))
    S.append(box((120, 150, 150), (940, PY - 75, FZ - 75), "风扇电机"))
    S.append(box((60, 40, 30), (1000, PY - 100, FZ - 40), "12V 接线"))
    S.append(path_tube([(860, PY, FZ), (820, PY, ZC + 60)], 10, 6, "定位线"))
    # ③ 活性炭滤棉（从接口爆炸出来）
    S.append(cyl(58, 46, "x", (1620, PY, FZ - 260), 20, "活性炭滤棉"))
    S.append(box((46, 116, 116), (1620, PY - 58, FZ - 318), "滤棉框"))
    S.append(cyl(64, 24, "x", (1700, PY, FZ - 260), 20, "快卡箍"))
    # ④ 天窗边排气口（防雨百叶）
    S += louver((2260, PY - 130, ZC - 130), 120, 260, 220, 5, "排气口百叶")
    S.append(box((30, 300, 300), (2240, PY - 150, ZC - 150), "排气口板"))

    # ⑤ 下层加热耗材干燥箱（从工作站下层爆炸到 -Y）
    DX, DY, DZ = 40.0, -900.0, 480.0
    S.append(box((520, 380, 330), (DX, DY, DZ), "加热耗材干燥箱"))
    S.append(box((430, 16, 210), (DX + 45, DY - 16, DZ + 60), "干燥箱视窗"))
    S += spool((DX + 130, DY + 100, DZ + 640), 100, 66, "耗材盘")
    S += spool((DX + 370, DY + 100, DZ + 640), 100, 66, "耗材盘")
    S.append(box((110, 20, 70), (DX + 200, DY - 20, DZ + 250), "温湿度表"))
    S.append(box((470, 320, 40), (DX + 25, DY + 30, DZ - 40), "加热底板"))
    S.append(path_tube([(DX + 130, DY + 133, DZ + 740), (DX + 260, DY + 520, 1000),
                        (PX + 40, PY - 60, 1010)], 11, 6, "PTFE 导料管"))

    items = [("①", "腔顶 100mm 排风口 + 铝箔管", (PX, PY, 1290)),
             ("②", "12V 静音管道风扇，打印开始联动", (940, PY - 75, FZ)),
             ("③", "活性炭滤棉，3 个月一换", (1642, PY - 58, FZ - 260)),
             ("④", "横过天花 1.5m，排气口在天窗边", (2240, PY, ZC)),
             ("⑤", "下层加热干燥箱，边烘边打 <15% RH", (DX + 260, DY - 16, DZ + 165))]
    audit(items, S, -60, 19)
    print("saved", draw("0305-3", "腔体排风与耗材干燥", items, S,
                        note="排风未装好前一律不打 ABS，只打 PLA；打印开始自动开风扇，结束后再抽十分钟",
                        sig="设想 · 0305", az=-60, el=19, fov=27))


fig2()
fig3()
