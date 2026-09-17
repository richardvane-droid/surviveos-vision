"""0504 自动种植架 — 三张硬件爆炸图（hand3d 管线）
0504-1 镀锌管四层种植架 / 0504-2 滴灌供水单元 / 0504-3 墨水屏状态面板
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, patch, gravel, seedling, dripper, solenoid, valve,
                     disc_filter, esp_box, epaper_panel)

RW, RD, RH = 2000.0, 600.0, 1800.0     # 架子 2m 宽 ×0.6m 深 ×1.8m 高
PR = 12.5                              # 25mm 镀锌管
SZ = (120.0, 670.0, 1120.0, 1520.0)    # 四层层板标高：层高 55/45/40/35cm
BOXW, BOXD, BOXH = 320.0, 400.0, 250.0


def clamp(pos, axis="z", name="铸铁卡扣"):
    x, y, z = pos
    return merge([cyl(PR * 1.75, 56, axis, (x, y, z), 12, name),
                  cyl(PR * 1.75, 56, "y" if axis != "y" else "z", (x, y, z), 12, name)], name)


def grow_box(pos, name="种植箱"):
    """40cm 种植箱：四壁 + 箱底 + 一圈边沿。"""
    x, y, z = pos
    o = [box((BOXW, BOXD, 18), (x, y, z), name)]
    o.append(box((BOXW, 16, BOXH), (x, y, z), name))
    o.append(box((BOXW, 16, BOXH), (x, y + BOXD - 16, z), name))
    o.append(box((16, BOXD, BOXH), (x, y, z), name))
    o.append(box((16, BOXD, BOXH), (x + BOXW - 16, y, z), name))
    for (ox, oy, ow, od) in ((-10, -10, BOXW + 20, 20), (-10, BOXD - 10, BOXW + 20, 20),
                             (-10, 10, 20, BOXD - 20), (BOXW - 10, 10, 20, BOXD - 20)):
        o.append(box((ow, od, 16), (x + ox, y + oy, z + BOXH), name + "边沿"))
    return merge(o, name)


# ---------------------------------------------------------------- 0504-1
def fig1():
    S = []
    S.append(patch(3200, 2200, (-500, -1100, 0), 60))

    # ① 25mm 镀锌管骨架 + 铸铁卡扣
    fr = []
    for (dx, dy) in ((0.0, 0.0), (RW, 0.0), (0.0, RD), (RW, RD)):
        fr.append(cyl(PR, RH, "z", (dx, dy, 0), 12, "25mm 镀锌立管"))
        fr.append(box((70, 70, 16), (dx - 35, dy - 35, -16), "管脚垫片"))
    for z in SZ + (RH,):
        for dy in (0.0, RD):
            fr.append(cyl(PR, RW, "x", (0, dy, z), 12, "25mm 镀锌横管"))
        for dx in (0.0, RW):
            fr.append(cyl(PR, RD, "y", (dx, 0, z), 12, "25mm 镀锌横管"))
    S.append(merge(fr, "25mm 镀锌管骨架"))
    for z in SZ + (RH,):
        for (dx, dy) in ((0.0, 0.0), (RW, 0.0), (0.0, RD), (RW, RD)):
            S.append(clamp((dx, dy, z - 28), "z", "铸铁卡扣"))

    # ② 每层一块防腐木板 + 6 个 40cm 种植箱；第三层的箱子整排向前爆炸
    OUT = 900.0
    for k, z in enumerate(SZ):
        S.append(box((RW + 60, RD - 30, 26), (-30, 15, z + PR), "防腐木层板"))
        yy = 40.0 - (OUT if k == 2 else 0.0)
        zz = z + PR + 26 + (240.0 if k == 2 else 0.0)
        for i in range(6):
            S.append(grow_box((22 + i * 330, yy, zz), "40cm 种植箱"))
            if k != 2:
                S.append(seedling((22 + i * 330 + BOXW / 2, yy + BOXD / 2, zz + BOXH - 30),
                                  180 + 60 * (3 - k), "菜苗"))
    # 每箱两个可调滴头 + 每层 16mm 主管
    for k, z in enumerate(SZ):
        if k == 2:
            continue
        zt = z + PR + 26 + BOXH + 30
        S.append(cyl(8, RW, "x", (0, 200, zt), 10, "16mm 滴灌主管"))
        for i in range(6):
            for d in (100.0, 230.0):
                S.append(dripper((22 + i * 330 + d, 200, zt - 20), "可调滴头"))

    # ④ 架顶横管兼遮阳网导轨（遮阳网卷起来挂在顶上）
    S.append(cyl(46, RW - 120, "x", (60, RD / 2, RH + 130), 14, "遮阳网卷"))
    for dx in (200.0, 1000.0, 1800.0):
        S.append(seg_tube((dx, RD / 2, RH + 130), (dx, RD / 2, RH + 14), 8, 6, "吊环"))
    S.append(box((RW - 200, 10, 420), (100, RD / 2 + 40, RH - 300), "遮阳网"))

    # ⑤ 侧立管挂墨水屏与液肥桶
    S.append(merge(epaper_panel((RW + 30, RD / 2 - 90, 1180)), "墨水屏"))
    S.append(seg_tube((RW, RD / 2, 1210), (RW + 30, RD / 2 - 60, 1210), 10, 6, "抱箍"))
    S.append(merge([cone(150, 170, 400, (RW + 260, RD / 2 - 40, 520), 16, "液肥桶"),
                    cyl(180, 24, "z", (RW + 260, RD / 2 - 40, 896), 16, "桶口")], "液肥桶"))
    S.append(path_tube(arc_pts((RW + 260, RD / 2 - 40, 920), 175, 14, 166, 8, "xz"), 10, 5, "桶提手"))

    items = [("①", "25mm 镀锌管 + 卡扣，不用焊接", (RW, RD, 900)),
             ("②", "每层 6 个 40cm 种植箱", (22 + 2 * 330, 40 - OUT, SZ[2] + PR + 26 + 240 + BOXH / 2)),
             ("③", "层高 55/45/40/35cm，矮的放上面", (1832, 40, 880)),
             ("④", "架顶横管做遮阳网导轨，35℃ 放下", (1000, RD / 2, RH + 176)),
             ("⑤", "侧立管挂墨水屏与液肥桶", (RW + 260, RD / 2 - 210, 720))]
    audit(items, S, -62, 16)
    print("saved", draw("0504-1", "镀锌管四层种植架", items, S,
                        note="摆在庭院东边界靠北一段，背对草地面朝院子；底层茄果、二层香草、三层叶菜、顶层新苗，谁也不挡谁的光",
                        sig="设想 · 0504", az=-62, el=16, fov=27))


# ---------------------------------------------------------------- 0504-2
def fig2():
    """架子底层那条水路：球阀 → 120 目过滤 → 12V 加压泵 → 4 路电磁阀 → 四层主管。"""
    S = []
    S.append(patch(3600, 1500, (-900, -800, 0), 60))
    # 架子底层层板与两截立管（够用就行）
    BZ0 = 300.0
    for dx in (-680.0, 2100.0):
        for dy in (0.0, 460.0):
            S.append(cyl(PR, BZ0, "z", (dx, dy, 0), 12, "架子立管"))
    S.append(box((3000, 520, 26), (-760, -30, BZ0), "防腐木层板"))
    ZT = BZ0 + 26

    # 来水：雨水罐 → 球阀
    S.append(seg_tube((-900, 300, ZT + 90), (-640, 300, ZT + 90), 16, 8, "雨水罐来水"))
    S.append(merge([cyl(30, 150, "x", (-640, 300, ZT + 90), 12, "球阀"),
                    box((34, 34, 40), (-582, 282, ZT + 118), "球阀"),
                    box((150, 26, 18), (-600, 291, ZT + 158), "球阀手柄")], "球阀"))

    # ① 120 目叠片过滤器（立着装）
    FX, FY = -300.0, 300.0
    fo = [cyl(58, 320, "z", (FX, FY, ZT), 16, "120 目叠片过滤器"),
          cyl(40, 54, "z", (FX, FY, ZT + 320), 14, "滤壳口")]
    for k in range(5):
        fo.append(cyl(66, 14, "z", (FX, FY, ZT + 50 + k * 46), 16, "叠片"))
    S.append(merge(fo, "120 目叠片过滤器"))
    S.append(seg_tube((-500, FY, ZT + 90), (FX - 40, FY, ZT + 90), 15, 8, "接管"))

    # ② 12V 隔膜加压泵 4L/min
    PX, PY = 40.0, 200.0
    S.append(box((280, 180, 160), (PX, PY, ZT), "12V 隔膜泵"))
    S.append(cyl(70, 150, "x", (PX + 280, PY + 90, ZT + 80), 16, "泵电机"))
    S.append(box((110, 70, 44), (PX + 20, PY - 70, ZT + 40), "泵进水口"))
    S.append(seg_tube((FX + 44, FY, ZT + 260), (PX + 80, FY, ZT + 260), 15, 8, "接管"))
    S.append(seg_tube((PX + 80, FY, ZT + 260), (PX + 80, PY - 30, ZT + 62), 15, 8, "接管"))

    # ③ 4 路电磁阀歧管
    MX, MY = 560.0, 210.0
    S.append(cyl(28, 700, "x", (MX, MY + 70, ZT + 70), 14, "歧管"))
    S.append(seg_tube((PX + 430, MY + 70, ZT + 70), (MX, MY + 70, ZT + 70), 16, 8, "泵出口"))
    for k in range(4):
        x0 = MX + 90 + k * 170
        S.append(merge([cyl(26, 160, "z", (x0, MY + 70, ZT + 70), 12, "12V 电磁阀"),
                        cyl(40, 96, "z", (x0, MY + 70, ZT + 148), 14, "线圈"),
                        box((30, 22, 18), (x0 - 15, MY + 44, ZT + 244), "接线")], "12V 电磁阀"))

    # ④ 四路 16mm 主管顺着后立管上去，末端快接口 + 可调滴头
    for k in range(4):
        x0 = MX + 90 + k * 170
        zt = ZT + 320 + k * 200
        S.append(path_tube([(x0, MY + 70, ZT + 254), (x0, 430, ZT + 254), (x0, 430, zt),
                            (x0 + 430, 430, zt)], 9, 6, "16mm 主管"))
        S.append(box((46, 42, 42), (x0 + 410, 409, zt - 21), "快接口"))
        S.append(dripper((x0 + 320, 430, zt - 18), "可调滴头"))

    # ⑤ 防水配电箱：箱体在右端，箱门向前爆炸，板件向上爆炸
    BX, BY = 1500.0, 40.0
    S.append(box((620, 300, 420), (BX, BY, ZT), "防水配电箱"))
    S.append(box((580, 16, 380), (BX + 20, BY - 560, ZT + 20), "箱门"))
    S.append(box((50, 12, 30), (BX + 540, BY - 572, ZT + 190), "箱扣"))
    S.append(box((380, 150, 120), (BX + 110, BY + 80, ZT + 40), "12V 电源"))
    S.append(box((440, 140, 26), (BX + 90, BY + 40, ZT + 700), "8 路继电器板"))
    for k in range(8):
        S.append(box((42, 70, 66), (BX + 100 + k * 52, BY + 70, ZT + 726), "继电器"))
    S.append(box((210, 120, 26), (BX + 200, BY + 50, ZT + 1060), "ESP32"))
    S.append(box((64, 20, 9), (BX + 250, BY + 40, ZT + 1086), "天线"))

    items = [("①", "120 目叠片过滤器，每月拆洗", (FX, FY - 66, ZT + 190)),
             ("②", "12V 隔膜泵 4L/min", (PX, PY + 90, ZT + 160)),
             ("③", "4 路电磁阀分层，断电即关", (MX + 90 + 170 - 40, MY + 70, ZT + 200)),
             ("④", "16mm 主管末端留快接口，冬季排空", (MX + 90 + 3 * 170 + 410, 409, ZT + 320 + 3 * 200 + 21)),
             ("⑤", "ESP32 + 8 路继电器，装防水箱", (BX + 90, BY + 40, ZT + 726))]
    audit(items, S, -68, 16)
    print("saved", draw("0504-2", "滴灌供水单元", items, S,
                        note="水从东墙那边 1500L 雨水罐接过来；分层控制让茄果多、新苗少，断网也照常工作，只是曲线暂时不上传",
                        sig="设想 · 0504", az=-68, el=16, fov=27))


# ---------------------------------------------------------------- 0504-3
def fig3():
    """挂在侧立管上的 2.9 寸墨水屏：外壳分件爆炸。"""
    S = []
    # 架子侧立管一小段 + 抱箍
    S.append(cyl(PR, 430, "z", (0, 0, -140), 14, "25mm 侧立管"))
    S.append(merge([cyl(PR * 1.9, 46, "z", (0, 0, 60), 14, "抱箍"),
                    box((70, 26, 40), (-35, 0, 64), "抱箍耳")], "抱箍"))

    STEP = 168.0

    def Y(k):
        return -46.0 - k * STEP

    # ⑤ 后壳（带抱箍座）
    S.append(box((104, 22, 78), (-52, Y(0), 34), "3D 打印后壳"))
    S.append(box((30, 26, 30), (-15, Y(0) + 20, 58), "抱箍座"))
    # ④ 18650 电池 + 支架
    S.append(cyl(9.2, 65, "x", (-32, Y(1) + 11, 66), 14, "18650 电池"))
    S.append(box((86, 24, 26), (-43, Y(1), 44), "电池支架"))
    # ③ ESP32 小板
    S.append(box((92, 6, 52), (-46, Y(2), 46), "ESP32"))
    for i in range(2):
        S.append(box((8, 5, 38), (-46 + i * 84, Y(2) - 5, 53), "排针"))
    S.append(box((22, 5, 9), (18, Y(2) - 5, 84), "天线"))
    # ② 2.9 寸墨水屏 296×128
    S.append(box((96, 5, 42), (-48, Y(3), 50), "2.9 寸墨水屏"))
    S.append(box((84, 3, 32), (-42, Y(3) - 3, 55), "显示区"))
    for i in range(4):
        S.append(box((62, 1.6, 2.4), (-32, Y(3) - 5, 60 + i * 7), "读数"))
    # ① 前壳 + 亚克力挡雨片
    fr = [box((112, 12, 92), (-56, Y(4), 28), "3D 打印前壳")]
    fr.append(box((100, 6, 30), (-50, Y(4) - 6, 116), "挡雨檐"))
    S.append(merge(fr, "3D 打印前壳"))
    S.append(box((106, 4, 66), (-53, Y(5), 40), "亚克力挡雨片"))

    items = [("①", "3D 打印外壳 + 亚克力挡雨片", (-53, Y(5), 90)),
             ("②", "2.9 寸墨水屏 296×128，阳光下可读", (-42, Y(3) - 3, 66)),
             ("③", "ESP32 每 10 分钟拉一次 HA 数据", (-46, Y(2), 86)),
             ("④", "18650 电池，续航约 3 个月", (-32, Y(1) + 2, 75)),
             ("⑤", "后壳抱箍直接卡在 25mm 侧立管上", (-52, Y(0), 92))]
    audit(items, S, -40, 20)
    print("saved", draw("0504-3", "墨水屏状态面板", items, S,
                        note="显示每层土壤湿度、上次浇水时间、今日是否浇水；不刷新时零功耗，拉完数据就深睡",
                        sig="设想 · 0504", az=-40, el=20, fov=27))


if __name__ == "__main__":
    w = sys.argv[1:] or ["1", "2", "3"]
    if "1" in w: fig1()
    if "2" in w: fig2()
    if "3" in w: fig3()
