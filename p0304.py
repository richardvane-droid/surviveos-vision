"""0304 屋顶光伏与储能 — 三张硬件爆炸图
0304-1 屋顶光伏阵列 / 0304-2 储能主机与备用电池架 / 0304-3 监测与安全面板
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl, extrusion
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, gauge,
                     gable, label, slope_frame, audit, ROOF)

PW, PD, PT = 1650.0, 1000.0, 35.0          # 400W 单晶板


# ---------------------------------------------------------------- 0304-1
def fig1():
    L = []                                   # 先在坡面局部坐标里建（u 沿檐口 / v 上坡 / w 外法线）

    # 瓦面（够用的一块）+ 瓦垄
    deck = [box((3900, 2700, 70), (-120, -150, -70), "瓦面")]
    for i in range(9):
        deck.append(box((3900, 60, 26), (-120, -120 + i * 320, 0), "瓦垄"))
    L.append(merge(deck, "瓦面"))

    # 瓦面挂钩：L 形，卡在瓦垄上（沿外法线爆炸 200）
    HK = 1000.0
    for u in (240.0, 1520.0, 2800.0):
        for v in (520.0, 1720.0):
            L.append(box((70, 26, 130), (u, v, HK), "瓦面挂钩"))
            L.append(box((70, 200, 26), (u, v - 174, HK), "挂钩爪"))
            L.append(cyl(9, 60, "z", (u + 35, v + 13, HK + 130), 10, "导轨螺栓"))
    HKP = (2800 + 35, 520 + 13, HK + 130)

    # 铝合金导轨 ×2（爆炸 430）
    RW = 2200.0
    for v in (500.0, 1700.0):
        L.append(extrusion(3500, "x", (100, v, RW), 42, "铝合金导轨"))
        for u in (240.0, 1520.0, 2800.0):
            L.append(box((60, 70, 30), (u + 5, v - 14, RW + 42), "压块夹具"))

    # 4 × 400W 单晶板（2×2，爆炸 820）
    PZ = 3800.0
    for i, u0 in enumerate((80.0, 1880.0)):
        for j, v0 in enumerate((120.0, 1320.0)):
            L.append(box((PW, PD, PT), (u0, v0, PZ), "400W 单晶板"))
            L.append(box((PW, PD, 12), (u0, v0, PZ - 12), "边框"))
            for k in range(1, 4):
                L.append(box((PW, 8, PT + 3), (u0, v0 + PD * k / 4, PZ - 1), "栅线"))
            # 背面 MC4 接线盒
            L.append(box((150, 110, 44), (u0 + PW / 2 - 75, v0 + PD / 2 - 55, PZ - 56), "MC4 接线盒"))
    # 串联：板间 MC4 短线
    L.append(path_tube([(80 + PW / 2, 120 + PD / 2, PZ - 40), (80 + PW / 2, 1320 + PD / 2, PZ - 40)], 16, 6, "MC4 跳线"))
    L.append(path_tube([(1880 + PW / 2, 120 + PD / 2, PZ - 40), (1880 + PW / 2, 1320 + PD / 2, PZ - 40)], 16, 6, "MC4 跳线"))
    L.append(path_tube([(80 + PW / 2, 1320 + PD / 2, PZ - 40), (1880 + PW / 2, 1320 + PD / 2, PZ - 40)], 16, 6, "MC4 跳线"))

    # 6mm² 光伏线 + 穿顶防水套
    SLV = (3480.0, 420.0)
    L.append(cyl(72, 230, "z", (SLV[0], SLV[1], -30), 16, "防水穿线套"))
    L.append(cone(150, 76, 60, (SLV[0], SLV[1], -40), 16, "防水盘"))
    L.append(path_tube([(1880 + PW / 2, 120 + PD / 2, PZ - 40), (3480, 620, PZ - 120),
                        (SLV[0], SLV[1], 200), (SLV[0], SLV[1], -60)], 18, 6, "6mm² 光伏线"))

    S = slope_frame(L, 45, (0, 0, 0))

    def W(u, v, w):
        y = -math.sqrt(2) / 2 * (v + w) + math.sqrt(2) / 2 * (v - w) * 0
        return (u, (v * math.cos(math.radians(45)) - w * math.sin(math.radians(45))),
                (v * math.sin(math.radians(45)) + w * math.cos(math.radians(45))))

    items = [("①", "4 × 400W 单晶板，串联开路约 160V", W(1880 + PW * 0.5, 1320 + PD * 0.5, PZ + PT)),
             ("②", "铝合金导轨 + 压块，顺斜顶走", W(760, 500 + 21, RW + 42)),
             ("③", "瓦面挂钩卡瓦垄，不打穿瓦片", W(HKP[0], HKP[1], HKP[2] - 60)),
             ("④", "6mm² 光伏线 + MC4 接头", W(3480, 520, 1940)),
             ("⑤", "穿顶处防水套加密封胶", W(SLV[0], SLV[1], 60))]
    audit(items, S, -45, 15)
    print("saved", draw("0304-1", "屋顶光伏阵列", items, S,
                        note="贴在 45° 四坡屋面的南坡；板下留 10cm 空气层散热，板温越高发电效率越低，晴天日发电 3～5 度",
                        sig="设想 · 0304", az=-45, el=15, fov=27))


# ---------------------------------------------------------------- 0304-2
def fig2():
    S = []
    S.append(floor(2700, 1800, (-400, -960, 0)))
    # 45° 斜顶：三根坡椽 + 一根檩条（背景件），储能离斜顶 ≥50cm
    for rx in (-380.0, 740.0, 1820.0):
        rf = box((150, 1950, 130), (rx, 0, -130), "45° 坡椽")
        S.append(ghost(mv(rot(rf, 135, "x", (0, 0, 0)), (0, 1560, 0))))
    pur = box((2350, 130, 110), (-380, 1300, -110), "檩条")
    S.append(ghost(mv(rot(pur, 135, "x", (0, 0, 0)), (0, 1560, 0))))

    # 2kWh 储能主机（坐在一块木垫上，离斜顶 ≥50cm）
    BX, BY, BZ = 0.0, 250.0, 260.0
    S.append(box((260, 560, 60), (BX - 20, BY - 20, BZ - 60), "木垫台"))
    S.append(box((520, 350, 430), (BX, BY, BZ), "2kWh 储能主机"))
    S.append(box((330, 16, 190), (BX + 95, BY - 16, BZ + 180), "储能显示面板"))
    for i in range(3):
        S.append(box((54, 20, 30), (BX + 110 + i * 100, BY - 20, BZ + 70), "输出口"))
    S.append(box((120, 24, 60), (BX + 350, BY - 24, BZ + 60), "MPPT 光伏输入"))
    S.append(path_tube([(BX + 175, BY + 175, BZ + 430), (BX + 175, BY + 175, BZ + 560)], 16, 6, "提手"))
    # 光伏线从天窗旁穿顶下来
    S.append(path_tube([(BX + 410, BY - 24, BZ + 90), (BX + 640, BY + 330, 1050),
                        (BX + 700, BY + 380, 1330)], 17, 6, "6mm² 光伏线"))

    # 自焊木架：两层，放备用电池
    RX, RY = 900.0, 200.0
    RW, RD, RH = 780.0, 420.0, 900.0
    rack = []
    for (dx, dy) in ((0, 0), (RW - 60, 0), (0, RD - 60), (RW - 60, RD - 60)):
        rack.append(box((60, 60, RH), (RX + dx, RY + dy, 0), "木架立柱"))
    for z in (70.0, 470.0, RH - 40):
        rack.append(box((RW, RD, 40), (RX, RY, z), "木架层板"))
    rack.append(box((RW, 40, RH - 100), (RX, RY + RD - 40, 60), "木架背板"))
    S.append(merge(rack, "木架"))

    # ② 备用 LiFePO4 2×100Ah：沿 -Y 爆炸出架子
    OUT = 760.0
    BAT = []
    for k, z in enumerate((110.0, 510.0)):
        bx = RX + 60
        S.append(box((560, 280, 230), (bx, RY - OUT, z), "LiFePO4 100Ah"))
        S.append(box((110, 24, 60), (bx + 60, RY - OUT - 24, z + 140), "正负极柱"))
        S.append(cyl(16, 70, "z", (bx + 100, RY - OUT + 40, z + 230), 12, "极柱"))
        S.append(cyl(16, 70, "z", (bx + 460, RY - OUT + 40, z + 230), 12, "极柱"))
        # 魔术贴
        for xx in (bx + 140, bx + 380):
            S.append(box((40, 300, 14), (xx, RY - OUT - 10, z - 14), "魔术贴"))
        # ③ JK 保护板（BMS）：再往外爆炸
        S.append(box((330, 130, 26), (bx + 110, RY - OUT - 420, z + 330), "JK 保护板"))
        S.append(box((80, 70, 14), (bx + 150, RY - OUT - 390, z + 356), "BMS 主控"))
        for i in range(6):
            S.append(box((14, 14, 12), (bx + 260 + i * 24, RY - OUT - 400, z + 356), "均衡电阻"))
        S.append(path_tube([(bx + 275, RY - OUT - 355, z + 340), (bx + 200, RY - OUT + 30, z + 250)], 7, 6, "采样线"))
        BAT.append((bx + 280, RY - OUT - 10, z + 115))

    items = [("①", "2kWh 储能，内置 MPPT 光伏输入", (BX + 260, BY - 16, BZ + 275)),
             ("②", "备用 LiFePO4 2 × 100Ah 立在木架上", BAT[1]),
             ("③", "每块配一片 JK 保护板（BMS）", (RX + 230, RY - OUT - 400, 550 + 330)),
             ("④", "木架块间留 10cm 散热间隙", (RX + RW / 2, RY + 200, 490)),
             ("⑤", "USB / 12V / 220V 三口按优先级分配", (BX + 137, BY - 20, BZ + 85))]
    audit(items, S, -60, 21)
    print("saved", draw("0304-2", "储能主机与备用电池架", items, S,
                        note="放在阁楼间西侧低矮带南段；储能离斜顶至少 50cm，温度超过 40℃ 它会自动降速充电",
                        sig="设想 · 0304", az=-60, el=21, fov=27))


# ---------------------------------------------------------------- 0304-3
def fig3():
    S = []
    S.append(floor(2400, 1600, (-380, -1560, 0)))
    # 电池木架侧板（面板钉在这上面，背景件）
    S.append(ghost(box((1160, 60, 1240), (0, 0, 120), "电池木架侧板")))

    # 小木板面板：沿 -Y 爆炸出来
    S.append(box((920, 30, 680), (60, -560, 400), "面板小木板"))
    for xx in (130.0, 930.0):
        for zz in (450.0, 1030.0):
            S.append(cyl(10, 60, "y", (xx, -560, zz), 10, "面板螺丝"))

    EY = -1240.0                                       # 三件仪表再往外爆炸
    # 1 复古指针电流表 0~30A
    S += gauge((210, EY, 890), 105, 60, "指针电流表")
    S.append(cyl(116, 20, "y", (210, EY - 20, 890), 20, "表圈"))
    S.append(box((160, 10, 160), (130, EY - 8, 810), "表盘面"))
    for i in range(5):
        a2 = math.radians(200 + i * 35)
        S.append(cyl(5, 18, "y", (210 + 82 * math.cos(a2), EY - 14, 890 + 82 * math.sin(a2)), 8, "刻度"))
    # 2 小屏幕
    S.append(box((280, 40, 195), (430, EY - 10, 790), "小屏幕"))
    S.append(box((230, 14, 150), (455, EY - 22, 812), "屏面"))
    for i in range(3):
        S.append(box((180, 6, 14), (478, EY - 26, 834 + i * 40), "数据行"))
    # 3 独立烟感
    S.append(cyl(125, 50, "y", (930, EY - 24, 890), 20, "独立烟感"))
    S.append(cyl(70, 16, "y", (930, EY - 38, 890), 16, "烟感罩"))
    S.append(box((176, 10, 176), (842, EY - 30, 802), "烟感面"))
    S.append(box((28, 18, 28), (980, EY - 36, 950), "烟感指示灯"))

    # 4 分流器串在储能输出主线上（面板正下方）
    SX, SY, SZ = 300.0, -380.0, 170.0
    S.append(box((250, 86, 70), (SX, SY, SZ), "分流器"))
    for dx in (32.0, 186.0):
        S.append(cyl(19, 84, "z", (SX + dx, SY + 43, SZ + 70), 12, "接线柱"))
    S.append(path_tube([(-260, SY + 43, SZ + 35), (SX, SY + 43, SZ + 35)], 26, 8, "储能输出主线"))
    S.append(path_tube([(SX + 250, SY + 43, SZ + 35), (1000, SY + 43, SZ + 35)], 26, 8, "储能输出主线"))
    S.append(path_tube([(SX + 109, SY + 43, SZ + 154), (240, EY + 500, 620), (210, EY + 46, 830)], 10, 6, "分流采样线"))

    # 5 CO2 灭火器（紧挨储能，伸手就够到）
    FX, FY = 1420.0, -700.0
    S.append(cyl(122, 640, "z", (FX, FY, 0), 20, "CO2 灭火器"))
    S.append(cone(122, 56, 124, (FX, FY, 640), 18, "瓶肩"))
    S.append(cyl(44, 104, "z", (FX, FY, 764), 14, "阀体"))
    S.append(box((210, 64, 44), (FX - 42, FY - 32, 846), "压把"))
    S.append(path_tube([(FX - 44, FY, 816), (FX - 270, FY - 120, 700), (FX - 300, FY - 140, 500)], 21, 6, "喷管"))
    S.append(cone(52, 130, 205, (FX - 300, FY - 140, 295), 16, "喇叭喷头"))
    S.append(box((160, 30, 100), (FX - 80, FY - 152, 370), "瓶身标"))

    items = [("\u2460", "\u6307\u9488\u7535\u6d41\u8868 0\uff5e30A\uff0c\u8089\u773c\u53ef\u4fe1\u7684\u515c\u5e95", (210, EY - 4, 890)),
             ("\u2461", "\u5c0f\u5c4f\u5e55\u663e\u793a\u53d1\u7535 / \u5269\u4f59\uff0c\u6570\u636e\u6765\u81ea HA", (570, EY - 20, 880)),
             ("\u2462", "\u72ec\u7acb\u70df\u611f\uff0c\u4e0d\u4f9d\u8d56\u7f51\u7edc\u548c\u7a0b\u5e8f", (930, EY - 26, 890)),
             ("\u2463", "\u5206\u6d41\u5668\u4e32\u5728\u50a8\u80fd\u8f93\u51fa\u4e3b\u7ebf\u4e0a", (SX + 125, SY, SZ + 35)),
             ("\u2464", "CO2 \u706d\u706b\u5668\u7d27\u6328\u50a8\u80fd\uff0c\u4f38\u624b\u5c31\u591f\u5230", (FX, FY - 122, 420))]
    audit(items, S, -58, 18)
    print("saved", draw("0304-3", "\u76d1\u6d4b\u4e0e\u5b89\u5168\u9762\u677f", items, S,
                        note="\u9762\u677f\u79bb\u50a8\u80fd 30cm\uff0c\u65b9\u4fbf\u4f38\u624b\u62d4\u7ebf\uff1b\u6307\u9488\u8868\u662f\u7eaf\u7269\u7406\u7684\uff0c\u4e0d\u4f9d\u8d56\u4efb\u4f55\u7f51\u7edc\u548c\u7a0b\u5e8f",
                        sig="\u8bbe\u60f3 \u00b7 0304", az=-58, el=18, fov=27))


fig1()
fig2()
fig3()
