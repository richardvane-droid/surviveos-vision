"""0301 核心区小制作 — 两张硬件爆炸图
0301-1 核心区松木工具台 / 0301-2 桌面 CNC 工位
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl, extrusion, hammer, wrench, plier, driver, tape
from partdraw import draw
from p34util import (merge, rot, prism, ghost, path_tube, cone, bucket, label,
                     wall_piece, audit, seg_tube)

TW, TD, TH = 1880.0, 840.0, 850.0          # 松木台面 188×84cm，高 85cm


# ---------------------------------------------------------------- 0301-1
def fig1():
    S = []
    # 背后的隔断（通往 0401 过道）+ 头顶 2060 平顶的一条边
    S.append(wall_piece(2360, 2060, (-240, 0, 0), 70, "隔断"))
    S.append(ghost(box((2360, 150, 60), (-240, -150, 2060), "2060 平顶")))

    # ① 松木台面 188×84，高 850：台面爆炸抬到 1250
    ZT = 1250.0
    S.append(box((TW, TD, 40), (0, -TD - 40, ZT), "松木台面"))
    S.append(box((TW + 40, 26, 60), (-20, -TD - 66, ZT - 20), "台面前沿"))
    for dx in (40, TW - 110):
        for dy in (-TD + 10, -150):
            S.append(box((70, 70, TH), (dx, dy - 40, 0), "松木台腿"))
    S.append(box((TW - 160, 60, 60), (80, -300, 260), "横撑"))

    # ② 洞洞板四分区：拆 / 量 / 切 / 焊，整块往外爆炸
    PY, PZ, PW, PH = -430.0, 1120.0, 1800.0, 880.0
    S.append(box((PW, 22, PH), (40, PY, PZ), "洞洞板"))
    for i in (1, 2, 3):                                   # 四分区的分隔描边
        S.append(box((10, 26, PH - 60), (40 + PW * i / 4 - 5, PY - 4, PZ + 30), "分区线"))
    # 板上工具（再往外一点，挂在板前）
    ty = PY - 150
    S += (hammer((250, ty, PZ + 300), 300) + plier((470, ty, PZ + 330))
          + tape((760, ty, PZ + 480)) + wrench((1000, ty, PZ + 300))
          + driver((1290, ty, PZ + 320)) + driver((1440, ty, PZ + 300)))
    # 焊区：烙铁（柄 + 细头）
    S.append(cyl(16, 190, "z", (1680, ty, PZ + 250), 12, "烙铁柄"))
    S.append(cone(9, 2.5, 110, (1680, ty, PZ + 440), 12, "烙铁头"))

    # ③ 两层浅抽屉 + Gridfinity 分格盒（抽屉沿 -Y 拉出）
    DO = 470.0
    for k, zz in enumerate((560.0, 350.0)):
        S.append(box((820, 640, 150), (170 + k * 880, -TD - DO, zz), "浅抽屉"))
        S.append(box((860, 24, 190), (150 + k * 880, -TD - DO - 24, zz - 20), "抽屉面板"))
        S.append(cyl(9, 220, "x", (400 + k * 880, -TD - DO - 46, zz + 75), 10, "拉手"))
    bins = []
    for i in range(6):
        for j in range(4):
            bins.append(box((84, 84, 62), (200 + i * 92, -TD - DO + 60 + j * 92, 880), "分格盒"))
    S.append(merge(bins, "Gridfinity 分格盒"))

    # ④ 臂灯（夹在抬起的台面右后角）+ 智能计量插座
    LX, LY, LZ = 1770.0, -180.0, ZT + 40
    S.append(cyl(46, 80, "z", (LX, LY, LZ), 16, "臂灯夹座"))
    S.append(path_tube([(LX, LY, LZ + 80), (LX - 40, LY - 250, LZ + 500),
                        (LX - 520, LY - 700, LZ + 560)], 16, 8, "臂灯臂"))
    S.append(cone(58, 104, 128, (LX - 560, LY - 720, LZ + 410), 18, "臂灯罩"))
    S.append(box((110, 40, 150), (1990, -30, 640), "计量插座"))
    S.append(path_tube([(2045, -30, 640), (2045, -230, 980), (LX, LY, LZ)], 7, 6, "灯线"))

    # ⑤ 碎屑桶 5 升（从台下爆炸到右前方）
    S += bucket((2120, -760, 0), 155, 330, "碎屑桶")

    items = [("①", "松木台面 188×84cm，高 850", (620, -TD - 40 + 420, ZT + 40)),
             ("②", "洞洞板四分区：拆 / 量 / 切 / 焊", (1000, PY, PZ + PH - 120)),
             ("③", "两层浅抽屉 + Gridfinity 分格盒", (430, -TD - DO + 200, 912)),
             ("④", "臂灯接智能计量插座，坐下亮", (LX - 560, LY - 720, LZ + 490)),
             ("⑤", "台下碎屑桶 5 升，随手扫进去", (2120, -760, 190))]
    audit(items, S, -52, 21)
    print("saved", draw("0301-1", "核心区松木工具台", items, S,
                        note="阁楼间可站立核心区北缘、紧挨 0401 过道的隔断；头顶就是 2060 平顶，站着、坐高脚凳都不撞头",
                        sig="设想 · 0301", az=-52, el=21, fov=27))


# ---------------------------------------------------------------- 0301-2
def fig2():
    S = []
    FW, FD = 520.0, 430.0                 # 机架外廓
    # ① 橡胶减震垫（最底层）
    S.append(box((FW + 70, FD + 70, 20), (-35, -35, 0), "橡胶减震垫"))

    # ② 铝型材机架（抬起 200）
    Z0 = 200.0
    for (x, y) in ((0, 0), (FW - 20, 0), (0, FD - 20), (FW - 20, FD - 20)):
        S.append(extrusion(150, "z", (x, y, Z0), 20, "3030 立柱"))
    for z in (Z0, Z0 + 130):
        S.append(extrusion(FW, "x", (0, 0, z), 20, "机架"))
        S.append(extrusion(FW, "x", (0, FD - 20, z), 20, "机架"))
        S.append(extrusion(FD - 40, "y", (0, 20, z), 20, "机架"))
        S.append(extrusion(FD - 40, "y", (FW - 20, 20, z), 20, "机架"))
    # Y 向导轨 + 滑块
    for x in (60.0, FW - 80.0):
        S.append(box((20, FD - 40, 16), (x, 20, Z0 + 150), "Y 导轨"))
        S.append(box((44, 70, 26), (x - 12, 140, Z0 + 166), "滑块"))
    # GRBL 控制板（爆炸到左前方外侧）
    GX, GY = -545.0, 130.0
    S.append(box((200, 140, 14), (GX, GY, Z0 + 20), "GRBL 控制板"))
    for i in range(4):
        S.append(box((34, 34, 30), (GX + 18 + i * 42, GY + 16, Z0 + 34), "驱动模块"))
    S.append(box((74, 48, 40), (GX + 112, GY + 76, Z0 + 34), "接线端子"))

    # ③ T 槽夹具板 + 压板（抬到 520）
    ZB = 520.0
    S.append(box((360, 280, 18), (80, 75, ZB), "T 槽夹具板"))
    for i in range(5):                                  # T 槽线
        S.append(box((10, 280, 6), (108 + i * 78, 75, ZB + 18), "T 槽"))
    S.append(box((210, 150, 12), (155, 140, ZB + 24), "工件"))
    for x in (150.0, 350.0):
        S.append(box((56, 26, 16), (x, 205, ZB + 36), "压板"))
        S.append(cyl(6, 46, "z", (x + 28, 218, ZB + 36), 10, "压板螺栓"))

    # ④ 龙门 + 主轴 + 吸尘罩（抬到 760）
    ZG = 760.0
    for x in (20.0, FW - 50.0):
        S.append(extrusion(300, "z", (x, FD / 2 - 15, ZG), 30, "龙门立柱"))
    S.append(extrusion(FW - 40, "x", (20, FD / 2 - 15, ZG + 300), 30, "横梁"))
    S.append(box((150, 26, 160), (215, FD / 2 - 45, ZG + 150), "Z 轴滑座"))
    SX, SY = 290.0, FD / 2 - 62
    S.append(cyl(36, 190, "z", (SX, SY, ZG + 120), 18, "主轴"))
    S.append(cone(30, 15, 56, (SX, SY, ZG + 64), 16, "ER11 夹头"))
    S.append(cyl(3.2, 62, "z", (SX, SY, ZG + 2), 10, "3.175 铣刀"))
    # 吸尘罩（套在铣刀外）+ 软管到碎屑桶
    S.append(cone(88, 30, 100, (SX, SY, ZG - 96), 18, "吸尘罩"))
    S.append(path_tube([(SX + 60, SY, ZG - 20), (SX + 300, SY - 170, ZG - 90),
                        (SX + 520, SY - 230, 470), (SX + 560, SY - 240, 330)], 30, 8, "吸尘软管"))
    S += bucket((SX + 560, SY - 240, 60), 130, 280, "碎屑桶")

    # ⑤ 亚克力防护罩：三片向外爆炸（罩壁只到 360 高，不挡机器）
    E, PH2 = 560.0, 320.0
    S.append(ghost(box((6, FD, PH2), (-E, 0, Z0 + 120), "亚克力罩")))
    S.append(ghost(box((6, FD, PH2), (FW + E, 0, Z0 + 120), "亚克力罩")))
    S.append(ghost(box((FW, 6, PH2), (0, -E - 60, Z0 + 120), "亚克力前罩")))

    items = [("①", "铝型材机架 + GRBL 板，行程 30×18cm", (GX + 100, GY + 70, Z0 + 34)),
             ("②", "T 槽夹具板 + 压板，一夹就固定", (240, 160, ZB + 18)),
             ("③", "主轴夹 3.175mm 铣刀，上万转", (SX, SY, ZG + 200)),
             ("④", "吸尘罩接碎屑桶，木屑不落地", (SX + 560, SY - 240, 200)),
             ("⑤", "亚克力防护罩挡飞屑、压噪音", (FW * 0.5, -E - 57, Z0 + 280))]
    audit(items, S, -58, 23)
    print("saved", draw("0301-2", "桌面 CNC 工位", items, S,
                        note="放在松木台面的桌角，是这张台子唯一的机器；整机坐橡胶减震垫，专刻 PSK 扣件、木牌与亚克力标牌",
                        sig="设想 · 0301", az=-58, el=23, fov=27))


fig1()
fig2()
