"""0210 防灾食品 — 硬件爆炸图
0210-1 斜滑轨罐头架 / 0210-2 NFC 密封米桶
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

RKW, RKD, RKH = 2400, 460, 2000      # 镀锌钢架 ≈2.4m 长 × 2m 高
LV = 5                               # 5 层


# ---------------------------------------------------------------- 0210-1
def fig1():
    S = []
    wl = box((RKW + 400, 60, 2300), (-200, RKD + 50, -20), "储藏室东墙"); wl.shade = False; S.append(wl)
    fl = box((RKW + 400, 1700, 40), (-200, -1150, -40), "地面"); fl.shade = False; S.append(fl)

    # ① 镀锌钢架：四根立柱 + 5 层层板
    rk = []
    for dx in (0, RKW - 60):
        for dy in (0, RKD - 60):
            rk.append(box((60, 60, RKH), (dx, dy, 0), "镀锌立柱"))
            for i in range(9):
                rk.append(box((64, 20, 14), (dx - 2, dy + 20, 120 + i * 220), "调节孔位"))
    ZS = [40, 470, 900, 1330, 1760]
    for i, zz in enumerate(ZS):
        if i == 2:       # 中间这层的层板跟着导轨一起往外爆炸，这里不画
            continue
        rk.append(box((RKW, RKD, 26), (0, 0, zz), "镀锌层板"))
        rk.append(box((RKW, 26, 60), (0, -26, zz - 34), "层板前翻边"))
    S.append(merge(rk, "镀锌钢架"))

    # ⑤ 底层 12 桶 18L 水
    for i in range(6):
        for j in range(2):
            S.append(cyl(130, 330, "z", (180 + i * 380, 130 + j * 200, 66), 16, "18L 水桶"))
            S.append(cyl(64, 34, "z", (180 + i * 380, 130 + j * 200, 396), 14, "桶盖"))

    # ② 中间层的镀锌层板（往 -Y 前方爆炸）
    YE, ZE = -640, 0
    S.append(box((RKW, RKD, 26), (0, YE, ZS[2] + ZE), "镀锌层板"))

    # ③ 3D 打印 PETG 导轨：15° 斜度，两根一组夹住一列罐头（再往前上方爆炸）
    YR, ZR = -1180, 300
    NR, PIT = 8, 290
    for k in range(NR):
        x0 = 60 + k * PIT
        for dx in (0, 190):
            rail = prism([(0, 0), (RKD - 40, (RKD - 40) * math.tan(math.radians(15))),
                          (RKD - 40, (RKD - 40) * math.tan(math.radians(15)) + 46), (0, 46)],
                         26, "x", (x0 + dx, YR, ZS[2] + ZR), "PETG 导轨")
            S.append(rail)
        for m in range(3):                       # 罐头横躺在导轨上
            yy = YR + 60 + m * 130
            zz = ZS[2] + ZR + 60 + (yy - YR) * math.tan(math.radians(15))
            S.append(cyl(42, 110, "x", (x0 + 40, yy, zz), 16, "罐头"))
            S.append(cyl(45, 8, "x", (x0 + 40, yy, zz), 16, "罐顶"))

    # ④ 前挡条 + 标签夹（最外层）
    YF = -1900
    S.append(box((RKW, 30, 70), (0, YF, ZS[2] + ZR + 20), "前挡条"))
    for k in range(NR):
        S.append(box((150, 40, 60), (40 + k * PIT, YF - 40, ZS[2] + ZR - 60), "标签夹"))
        S.append(box((130, 6, 44), (50 + k * PIT, YF - 46, ZS[2] + ZR - 52), "日期标签"))

    items = [("①", "镀锌钢架 2.4m×2m，层板承 150kg", (RKW - 60, -26, 1420)),
             ("②", "架体离墙 5cm 通风，5 层", (RKW * .4, YE, ZS[2] + 26)),
             ("③", "PETG 导轨 15°，罐头自重滚向前", (60 + 3 * PIT + 95, YR + 60, ZS[2] + ZR + 118)),
             ("④", "前挡条 + 标签夹，先进先出", (RKW * .3, YF - 46, ZS[2] + ZR - 30)),
             ("⑤", "底层专放 12 桶 18L 水", (180 + 130, 130, 200))]
    audit(items, S, -52, 16)
    p = draw("0210-1", "斜滑轨罐头架", items, S,
             note="储藏室东墙一整面，架前只留 ≈1m 过道；从后面补新罐头、从前面取旧罐头，物理结构本身就保证先进先出",
             sig="设想 · 0210", az=-52, el=16, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0210-2
def fig2():
    S = []
    R, BH = 130, 300                     # 食品级 PP 密封桶 10L

    # ⑤ 塑料托盘（桶下垫着，不直接接触水泥地）
    S.append(box((2 * R + 120, 2 * R + 120, 40), (-R - 60, -R - 60, -260), "塑料托盘"))
    for i in range(5):
        S.append(box((2 * R + 80, 20, 14), (-R - 40, -R - 40 + i * 62, -220), "托盘条"))

    # ① 下面那只桶（叠放两层的下层）
    bk = [cyl(R, BH, "z", (0, 0, -140), 24, "PP 密封桶")]
    S.append(merge(bk, "PP 密封桶"))
    S.append(cyl(R + 10, 26, "z", (0, 0, 134), 24, "桶口沿"))

    # ② 真空米砖 5kg（从桶里往上爆炸）
    for i in range(3):
        S.append(box((200, 150, 74), (-100, -75, 300 + i * 104), "5kg 真空米砖"))
        S.append(box((180, 8, 8), (-90, -76, 334 + i * 104), "热封边"))
    # ③ 脱氧剂
    S.append(box((90, 70, 26), (-45, -35, 620), "脱氧剂 100cc"))

    # ④ 硅胶圈盖 + NTAG213 NFC 贴纸
    ZL = 740
    S.append(cyl(R + 12, 40, "z", (0, 0, ZL), 24, "密封桶盖"))
    S.append(cyl(R + 2, 16, "z", (0, 0, ZL - 22), 24, "硅胶圈"))
    S.append(cyl(46, 5, "z", (0, 0, ZL + 40), 20, "NTAG213 贴纸"))
    for i in range(3):
        S.append(box((70 - i * 18, 4, 4), (-35 + i * 9, -2, ZL + 45 + i * 6), "NFC 线圈"))
    S.append(box((70, 34, 30), (R - 20, -17, ZL + 6), "提手耳"))

    # 叠放的第二只桶（示意可叠两层）
    for zz in (-220, 120):
        S.append(cyl(R, BH, "z", (600, 60, zz), 24, "第二只桶"))
        S.append(cyl(R + 12, 40, "z", (600, 60, zz + BH), 24, "第二只桶盖"))
    S.append(box((2 * R + 120, 2 * R + 120, 40), (600 - R - 60, 60 - R - 60, -260), "塑料托盘"))

    items = [("①", "食品级 PP 密封桶 10L，半透明", (R, 0, 0)),
             ("②", "真空米砖 5kg，常温保质 24 个月", (0, -75, 370)),
             ("③", "脱氧剂 100cc 一包，开桶换新", (0, -35, 632)),
             ("④", "NTAG213 贴纸写 Grocy 商品页", (0, -2, ZL + 51)),
             ("⑤", "桶下垫塑料托盘让空气流通", (R + 40, -R - 40, -230))]
    audit(items, S, -46, 22)
    p = draw("0210-2", "NFC 密封米桶", items, S,
             note="储藏室没窗湿度大：真空米砖 + 桶里一包脱氧剂双层保险，手机一碰桶盖就弹出入库日期、保质期和剩余数量",
             sig="设想 · 0210", az=-46, el=22, fov=27)
    print("saved", p)


fig1(); fig2()
