"""0303 常驻帐篷 — 三张硬件爆炸图
0303-1 常驻双人帐篷总成 / 0303-2 5V 帐篷灯光组 / 0303-3 天窗电动遮光帘
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, seg_tube, cone,
                     arc_pts, gable, label, audit, ROOF)

TW, TD, THG = 2350.0, 2160.0, 1150.0       # 帐篷 235×216cm，脊高 1.15m


def arch_sec(w, h, n=14, flat=0.10):
    """帐篷断面：底边平、顶上一段拱。返回 (y,z) 点列。"""
    pts = [(0, 0)]
    for i in range(n + 1):
        t = math.pi * i / n
        y = w / 2 - (w / 2) * math.cos(t)
        z = h * math.sin(t) ** 0.78
        pts.append((y, max(z, 0) + (flat * h if 0 < i < n else 0) * 0))
    pts.append((w, 0))
    return pts


def dome_poles(x0, y0, z0, w, d, h, r=9, name="铝杆"):
    """两根交叉铝杆：一根跨 Y、一根跨 X，顶部交于中心。"""
    o = []
    a = [(x0 + w / 2, y0 + d / 2 - (d / 2) * math.cos(math.pi * i / 14),
          z0 + h * math.sin(math.pi * i / 14) ** 0.78) for i in range(15)]
    b = [(x0 + w / 2 - (w / 2) * math.cos(math.pi * i / 14), y0 + d / 2,
          z0 + h * math.sin(math.pi * i / 14) ** 0.78) for i in range(15)]
    o.append(path_tube(a, r, 8, name))
    o.append(path_tube(b, r, 8, name))
    return o


# ---------------------------------------------------------------- 0303-1
def fig1():
    S = []
    S.append(floor(8200, 3200, (-4400, -700, 0)))
    BX = -3980.0                               # 睡眠系统三层爆炸到帐篷西侧

    # ② 底层 3cm 泡沫拼接地垫（四块）
    for i in range(2):
        for j in range(2):
            S.append(box((1180, 1080, 30), (BX + i * 1190, j * 1090, 0), "泡沫拼接地垫"))
            S.append(box((60, 26, 30), (BX + i * 1190 + 560, j * 1090 + 1080, 0), "拼接凸榫"))

    # ③ 5cm 自充气垫 ×2 + 羽绒睡袋 ×2
    ZP = 400.0
    for yy in (180.0, 1060.0):
        S.append(box((1950, 680, 50), (BX + 200, yy, ZP), "自充气垫"))
        S.append(box((44, 680, 46), (BX + 2150, yy, ZP + 2), "充气阀侧"))
    ZB = 790.0
    for yy in (230.0, 1110.0):
        S.append(box((1700, 580, 200), (BX + 330, yy, ZB), "羽绒睡袋"))
        S.append(cyl(150, 580, "y", (BX + 330, yy, ZB + 100), 16, "睡袋头罩"))
        S.append(box((1700, 24, 150), (BX + 330, yy + 290, ZB + 30), "睡袋拉链"))

    # ① 铝杆内帐（不挂外帐）：断面拱形，沿 X 拉伸
    ZT = 820.0
    S.append(prism(arch_sec(TD, THG), TW, "x", (0, 0, ZT), "内帐"))
    S.append(box((TW, TD, 16), (0, 0, ZT - 16), "帐底布"))
    # 门（朝东南，开在 +X 端面）：拱形门框 + 拉链
    dr = [(TW + 12, 500 + 560 - 560 * math.cos(math.pi * i / 12),
           ZT + 900 * math.sin(math.pi * i / 12) ** 0.8) for i in range(13)]
    S.append(path_tube(dr, 18, 6, "门框"))
    S.append(path_tube([(TW + 15, 1060, ZT), (TW + 15, 1060, ZT + 880)], 11, 6, "门拉链"))
    # ④ 侧网兜（从内帐侧壁爆炸出来）
    S.append(box((560, 40, 320), (1240, -520, ZT + 240), "侧网兜"))
    for i in range(4):
        S.append(box((9, 44, 320), (1270 + i * 140, -522, ZT + 240), "网格"))

    # 交叉铝杆：爆炸到内帐上方
    ZG = ZT + THG + 430
    S += dome_poles(0, 0, ZG, TW, TD, THG, 13)
    for c in ((60, 60), (TW - 60, 60), (60, TD - 60), (TW - 60, TD - 60)):
        S.append(box((80, 80, 44), (c[0] - 40, c[1] - 40, ZG - 44), "杆脚扣"))

    # ⑤ 门口地毯 + 拖鞋
    S.append(box((900, 640, 26), (TW + 400, 720, 0), "门口地毯"))
    for sx in (0, 300):
        S.append(box((150, 320, 70), (TW + 600 + sx, 860, 26), "拖鞋"))
        S.append(cone(72, 42, 60, (TW + 675 + sx, 880, 96), 14, "鞋头"))

    items = [("\u2460", "\u94dd\u6746\u5185\u5e10 235\u00d7216cm\uff0c\u4e0d\u6302\u5916\u5e10", (TW * 0.40, TD / 2, ZT + THG - 30)),
             ("\u2461", "\u5e95\u5c42 3cm \u6ce1\u6cab\u62fc\u63a5\u5730\u57ab", (BX + 1780, 1620, 30)),
             ("\u2462", "5cm \u81ea\u5145\u6c14\u57ab + \u7fbd\u7ed2\u7761\u888b", (BX + 900, 1400, ZB + 195)),
             ("\u2463", "\u4fa7\u7f51\u515c\u653e\u4e66\u548c\u8033\u673a", (1520, -520, ZT + 400)),
             ("\u2464", "\u95e8\u671d\u4e1c\u5357\u5bf9\u5929\u7a97\uff0c\u95e8\u53e3\u5730\u6bef + \u62d6\u978b", (TW + 470, 1290, 26))]
    audit(items, S, -46, 20)
    print("saved", draw("0303-1", "\u5e38\u9a7b\u53cc\u4eba\u5e10\u7bf7\u603b\u6210", items, S,
                        note="\u642d\u5728\u9601\u697c\u95f4\u53ef\u7ad9\u7acb\u6838\u5fc3\u533a\u504f\u897f\uff0c\u6c38\u8fdc\u4e0d\u62c6\uff1b\u5ba4\u5185\u4e0d\u7528\u9632\u98ce\u9632\u96e8\uff0c\u53ea\u642d\u8f7b\u91cf\u94dd\u6746\u5185\u5e10\uff0c\u5929\u7a97\u7684\u5149\u548c\u96e8\u58f0\u76f4\u63a5\u900f\u8fdb\u6765",
                        sig="\u8bbe\u60f3 \u00b7 0303", az=-46, el=20, fov=27))


# ---------------------------------------------------------------- 0303-2
def fig2():
    S = []
    XA = 1175.0                                  # 灯带所在的那道拱
    EY = -1750.0                                 # 整组灯沿 -Y 爆炸出帐篷

    def arc(x, y, scale=1.0, n=14):
        return [(x, TD / 2 - (TD / 2) * scale * math.cos(math.pi * i / n) + y,
                 60 + THG * scale * math.sin(math.pi * i / n) ** 0.78) for i in range(n + 1)]

    # 帐篷顶内侧：两道拱肋 + 一条脊线（背景件）
    for x in (150.0, TW - 150):
        S.append(ghost(path_tube(arc(x, 0), 15, 6, "帐篷拱肋")))
    S.append(ghost(path_tube([(150, TD / 2, 60 + THG), (TW - 150, TD / 2, 60 + THG)], 13, 6, "帐篷脊")))
    S.append(ghost(box((TW, TD, 14), (0, 0, 46), "帐底布")))

    # 1 WS2812 灯带 5 米：沿顶内侧一道拱走，整条爆炸出来；带上 LED 灯珠
    path = arc(XA, EY)
    S.append(path_tube(path, 9, 6, "WS2812 灯带"))
    fine = arc(XA, EY, 1.0, 34)
    for i, q in enumerate(fine):
        if i % 2:
            S.append(box((30, 26, 26), (q[0] - 15, q[1] - 13, q[2] + 6), "LED 灯珠"))
    # 3 磁吸挂钩：把灯带扣在拱肋上
    for i in (2, 5, 9, 12):
        q = path[i]
        S.append(cyl(44, 30, "x", (q[0] - 60, q[1], q[2] + 30), 14, "磁吸挂钩"))
        S.append(cyl(14, 62, "x", (q[0] - 60, q[1], q[2] + 30), 10, "钩杆"))
    HK = path[5]

    # 2 ESP32 刷 WLED（接在灯带一端）
    EX, EY2, EZ = XA - 300, EY - 40, 120.0
    S.append(box((230, 150, 70), (EX - 115, EY2 - 75, EZ), "ESP32 控制盒"))
    S.append(box((140, 70, 26), (EX - 70, EY2 - 35, EZ + 70), "ESP32 模块"))
    S.append(box((60, 40, 34), (EX - 100, EY2 - 20, EZ + 18), "USB 口"))
    S.append(path_tube([(EX + 115, EY2, EZ + 40), (XA - 90, path[0][1] - 60, 110),
                        (path[0][0], path[0][1], path[0][2] + 40)], 11, 6, "灯带引线"))

    # 4 露营灯：顶部主光，爆炸下落
    LX, LY, LZ = XA + 120, EY + TD / 2, 520.0
    S.append(cyl(155, 210, "z", (LX, LY, LZ), 20, "露营灯"))
    S.append(cone(155, 96, 92, (LX, LY, LZ + 210), 18, "灯顶"))
    S.append(path_tube(arc_pts((LX, LY, LZ + 322), 88, 10, 170, 10, "xz"), 10, 6, "提环"))
    S.append(cyl(130, 22, "z", (LX, LY, LZ - 22), 20, "灯面"))
    S.append(box((66, 26, 22), (LX - 33, LY - 166, LZ + 56), "三档旋钮"))

    # 5 储能 USB 输出口
    UX, UY = TW + 520, EY + TD - 520
    S.append(box((430, 310, 330), (UX, UY, 0), "储能 USB 输出"))
    S.append(box((330, 16, 210), (UX + 50, UY - 16, 60), "面板"))
    for i in range(3):
        S.append(box((52, 22, 26), (UX - 22, UY + 70 + i * 78, 150), "USB 口"))
    S.append(path_tube([(UX - 22, UY + 92, 163), (UX - 900, UY - 700, 260),
                        (EX + 115, EY2, EZ + 40)], 12, 6, "5V 线"))

    items = [("\u2460", "WS2812 \u706f\u5e26 5 \u7c73\uff0c\u6cbf\u9876\u5185\u4fa7\u8d70", (path[7][0], path[7][1], path[7][2] + 19)),
             ("\u2461", "ESP32 \u5237 WLED\uff0c\u624b\u673a\u8c03\u8272\u8c03\u4eae\u5ea6", (EX, EY2 - 40, EZ + 83)),
             ("\u2462", "\u78c1\u5438\u6302\u94a9\u56fa\u5b9a\uff0c\u4e0d\u7c98\u4e0d\u9489", (HK[0] - 60, HK[1] - 44, HK[2] + 30)),
             ("\u2463", "\u9732\u8425\u706f\u505a\u4e3b\u5149\uff0c\u4e09\u6863\u6700\u4f4e\u5f53\u591c\u706f", (LX, LY - 155, LZ + 110)),
             ("\u2464", "\u6574\u7ec4 <10W\uff0c\u5168\u4ece\u50a8\u80fd USB \u53d6\u7535", (UX, UY + 148, 163))]
    audit(items, S, -54, 20)
    print("saved", draw("0303-2", "5V \u5e10\u7bf7\u706f\u5149\u7ec4", items, S,
                        note="\u5e10\u7bf7\u91cc\u6240\u6709\u706f\u90fd\u8d70 5V USB\u3001\u4e0d\u8fdb 220V\uff1b\u6574\u7ec4\u529f\u7387\u4e0d\u5230 10W\uff0c\u4e00\u665a\u4e0a\u7528\u4e0d\u5230 0.05 \u5ea6\u7535",
                        sig="\u8bbe\u60f3 \u00b7 0303", az=-54, el=20, fov=27))


# ---------------------------------------------------------------- 0303-3
def fig3():
    S = []
    EAVE, R2 = 2400.0, math.sqrt(2) / 2

    def toroof(s):
        return mv(rot(s, 135, "x", (0, 0, 0)), (0, EAVE, 0))

    def P(u, v, w):
        return (u, EAVE - R2 * (v + w), R2 * (v - w))

    OW, OH = 600.0, 800.0                    # 天窗洞口 600×800
    V0 = 900.0                               # 洞口下沿在坡面上的位置
    # 屋面：洞口四周四块板（只给够用的一圈，留出洞口）
    plates = [box((330, OH + 680, 60), (-330, V0 - 340, -60), "屋面"),
              box((330, OH + 680, 60), (OW, V0 - 340, -60), "屋面"),
              box((OW, 340, 60), (0, V0 - 340, -60), "屋面"),
              box((OW, 340, 60), (0, V0 + OH, -60), "屋面")]
    S += [ghost(x) for x in toroof(plates)]
    # 天窗框 + 玻璃
    fr = [box((OW + 120, 60, 130), (-60, V0 - 60, 0)), box((OW + 120, 60, 130), (-60, V0 + OH, 0)),
          box((60, OH + 120, 130), (-60, V0 - 60, 0)), box((60, OH + 120, 130), (OW, V0 - 60, 0))]
    S.append(merge(toroof(fr), "天窗框"))
    S.append(ghost(toroof(box((OW, OH, 8), (0, V0, 30), "天窗玻璃"))))

    # ③ 卷轴 + 卷帘布（帘布放下一半）
    WR = 190.0                               # 帘组离玻璃面的爆炸距离
    S.append(toroof(cyl(34, OW, "x", (0, V0 + OH - 70, WR), 18, "卷轴")))
    S.append(toroof(box((OW, 430, 6), (0, V0 + OH - 500, WR - 34), "遮光帘布")))
    S.append(toroof(box((OW, 34, 26), (0, V0 + OH - 506, WR - 50), "帘布下压杆")))
    # ⑤ 手拉拉绳（断电时手动）
    p0 = P(OW - 60, V0 + OH - 506, WR - 64)
    S.append(path_tube([p0, (p0[0], p0[1] - 40, p0[2] - 330)], 9, 6, "手拉绳"))
    S.append(cyl(30, 60, "z", (p0[0], p0[1] - 40, p0[2] - 390), 12, "拉珠"))

    # ② 3D 打印卷轴接头 + 电机支架（沿 +X 爆炸出卷轴端）
    S.append(toroof(cyl(36, 70, "x", (OW + 130, V0 + OH - 70, WR), 16, "卷轴接头")))
    S.append(toroof(cyl(14, 40, "x", (OW + 210, V0 + OH - 70, WR), 12, "接头轴")))
    S.append(toroof(box((26, 150, 150), (OW + 270, V0 + OH - 145, WR - 75), "电机支架")))
    S.append(toroof(box((110, 26, 150), (OW + 270, V0 + OH - 145, WR - 75), "支架耳")))
    # ① 28BYJ-48 + ULN2003
    S.append(toroof(cyl(14, 20, "x", (OW + 320, V0 + OH - 70, WR), 14, "28BYJ-48")))
    S.append(toroof(cyl(14, 22, "x", (OW + 340, V0 + OH - 70, WR), 14, "减速箱")))
    S.append(toroof(box((14, 60, 8), (OW + 340, V0 + OH - 100, WR - 4), "电机法兰")))
    S.append(toroof(box((6, 35, 32), (OW + 430, V0 + OH - 88, WR - 16), "ULN2003 驱动板")))
    for i in range(4):
        S.append(toroof(box((6, 6, 6), (OW + 432, V0 + OH - 84 + i * 8, WR - 12), "指示灯")))
    # ④ ESP32（跑 ESPHome，记忆两端点）
    S.append(toroof(box((16, 74, 46), (OW + 500, V0 + OH - 107, WR - 23), "ESP32")))
    S.append(toroof(path_tube([(OW + 440, V0 + OH - 70, WR), (OW + 500, V0 + OH - 70, WR)], 4, 6, "驱动线")))

    items = [("①", "28BYJ-48 步进 + ULN2003 驱动板", P(OW + 350, V0 + OH - 70, WR + 14)),
             ("②", "3D 打印卷轴接头与电机支架", P(OW + 165, V0 + OH - 70, WR + 36)),
             ("③", "卷轴 + 遮光帘布，记忆上下两端点", P(OW / 2, V0 + OH - 300, WR - 40)),
             ("④", "ESP32 跑 ESPHome，早 7 点自动卷起", P(OW + 508, V0 + OH - 70, WR + 23)),
             ("⑤", "手拉备用：断电时可手动卷帘", (p0[0], p0[1] - 40, p0[2] - 360))]
    audit(items, S, -62, 8)
    print("saved", draw("0303-3", "天窗电动遮光帘", items, S,
                        note="天窗在帐篷门的东南向 ≈1m；卷帘由气象站联动，雨天关上、早 7 点卷起让阳光进帐篷",
                        sig="设想 · 0303", az=-62, el=8, fov=27))


fig1()
fig2()
fig3()
