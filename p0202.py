"""0202 卫生间灯箱系统 — 硬件爆炸图
0202-1 天花板灯箱总成 / 0202-2 六面镜光箱 / 0202-3 污水提升泵检修柜
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

RW, RD = 1650, 1250        # 卫生间 ≈1.65×1.25m
BX, BY = 1000, 1000        # 灯箱 1000×1000


# ---------------------------------------------------------------- 0202-1
def fig1():
    S = []
    X0, Y0 = (RW - BX) / 2, (RD - BY) / 2
    ZS, ZB, ZL, ZD, ZG = 2390, 1900, 1570, 700, 380

    # 小天花板（只给灯箱外一圈，纯背景）
    c = box((RW, RD, 80), (0, 0, ZS), "天花板"); c.shade = False; S.append(c)

    # ② 顶部散热缝 + Φ100 通风道
    duct = [cyl(52, 230, "z", (X0 + 700, Y0 + 560, ZB + 194), 18, "Φ100 通风道"),
            cyl(52, 1020, "x", (X0 + 700, Y0 + 560, ZB + 424), 18, "通风道"),
            cyl(62, 70, "x", (X0 + 1720, Y0 + 560, ZB + 424), 18, "风口")]
    S.append(merge(duct, "Φ100 通风道"))

    # ① 镀锌板箱体 1000×1000×180：四壁 + 顶板（顶板上开 7 道散热缝）
    sh = [box((BX, 26, 180), (X0, Y0, ZB), "镀锌板箱体"),
          box((BX, 26, 180), (X0, Y0 + BY - 26, ZB), "镀锌板箱体"),
          box((26, BY - 52, 180), (X0, Y0 + 26, ZB), "镀锌板箱体"),
          box((26, BY - 52, 180), (X0 + BX - 26, Y0 + 26, ZB), "镀锌板箱体")]
    for i in range(7):
        sh.append(box((BX, 62, 14), (X0, Y0 + 66 + i * 128, ZB + 180), "顶板散热缝"))
    sh.append(box((BX, 66, 14), (X0, Y0, ZB + 180), "顶板"))
    sh.append(box((BX, 68, 14), (X0, Y0 + BY - 68, ZB + 180), "顶板"))
    S.append(merge(sh, "镀锌板箱体"))

    # ③ 浴霸灯泡 275W ×4 + 陶瓷灯座（四角散开到箱体外沿，免得被顶板挡住）
    SPR = 790
    for ix in (-1, 1):
        for iy in (-1, 1):
            px = X0 + BX / 2 + ix * SPR
            py = Y0 + BY / 2 + iy * SPR
            S.append(box((170, 170, 66), (px - 85, py - 85, ZL + 150), "陶瓷灯座"))
            S.append(cyl(40, 70, "z", (px, py, ZL + 84), 14, "灯头"))
            S.append(cyl(86, 140, "z", (px, py, ZL - 60), 20, "275W 浴霸灯泡"))

    # ④ 亚克力柔光板 8mm 乳白 + 压条
    S.append(box((BX - 40, BY - 40, 8), (X0 + 20, Y0 + 20, ZD), "亚克力柔光板 8mm"))
    for oy in (20, BY - 44):
        S.append(box((BX - 40, 24, 30), (X0 + 20, Y0 + oy, ZD - 30), "压条"))

    # ⑤ 四周 5cm 天光缝 + 双色温灯带
    ring, W2 = [], 50
    for (w, d, ox, oy) in ((BX + 2 * W2, W2, -W2, -W2), (BX + 2 * W2, W2, -W2, BY),
                           (W2, BY, -W2, 0), (W2, BY, BX, 0)):
        ring.append(box((w, d, 44), (X0 + ox, Y0 + oy, ZG), "5cm 天光缝"))
    S.append(merge(ring, "5cm 天光缝"))
    for (w, d, ox, oy) in ((BX + 2 * W2, 18, -W2, -W2 + 16), (BX + 2 * W2, 18, -W2, BY + 16),
                           (18, BY, -W2 + 16, 0), (18, BY, BX + 16, 0)):
        S.append(box((w, d, 16), (X0 + ox, Y0 + oy, ZG + 44), "双色温灯带"))

    items = [("①", "镀锌板箱体 1000×1000×180", (X0 + BX, Y0 + 500, ZB + 96)),
             ("②", "顶部散热缝 + Φ100 通风道", (X0 + 1600, Y0 + 560, ZB + 476)),
             ("③", "浴霸灯泡 275W ×4，陶瓷灯座", (X0 + BX / 2 - SPR, Y0 + BY / 2 - SPR - 86, ZL + 10)),
             ("④", "亚克力柔光板 8mm，透光 60%", (X0 + BX - 44, Y0 + BY / 2, ZD + 8)),
             ("⑤", "四周 5cm 天光缝嵌双色温灯带", (X0 + 500, Y0 - W2, ZG + 44))]
    audit(items, S, -56, 26)
    p = draw("0202-1", "天花板灯箱总成", items, S,
             note="卫生间 ≈1.65×1.25m，灯箱嵌在这块小天花板正中、几乎占满；1000W 的热必须从顶缝和通风道走掉，不然亚克力会软",
             sig="设想 · 0202", az=-56, el=26, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0202-2
def fig2():
    S = []
    MW, MH, SD = 900, 700, 300      # 主镜 900×700，侧 / 顶镜进深 300
    Z0, YW = 1080, 480              # 主镜下沿 / 墙面
    EY, ES, ET = 320, 400, 340      # 前后 / 两侧 / 向上的爆炸间距

    # 洗手台 + 台盆 + 隔墙（背景）
    for b in (box((MW + 140, 520, 40), (-70, 0, 860), "洗手台"),
              box((MW + 380, 30, 600), (-190, YW, 300), "隔墙")):
        b.shade = False; S.append(b)
    S.append(cyl(190, 130, "z", (MW / 2, 250, 900), 22, "台盆"))
    S.append(cyl(16, 190, "z", (MW / 2, 420, 900), 12, "龙头"))
    S.append(cyl(16, -130, "y", (MW / 2, 420, 1082), 12, "出水嘴"))

    # ⑤ 防潮基板（贴墙，最里层）
    S.append(box((MW + 80, 16, MH + 80), (-40, YW - 16, Z0 - 40), "防潮基板"))
    # ② 电热除雾膜 40W：覆盖主镜中央 60%，本层往 +X 挪开露出来
    FW, FH, FX = int(MW * .6), int(MH * .6), 520
    S.append(box((FW, 4, FH), (MW * .2 + FX, YW - EY * .48, Z0 + MH * .2), "电热除雾膜 40W"))
    for i in range(7):
        S.append(box((10, 5, FH - 40), (MW * .2 + FX + 30 + i * 72, YW - EY * .48 - 1, Z0 + MH * .2 + 20), "发热丝"))
    S.append(box((90, 6, 44), (MW * .2 + FX - 90, YW - EY * .48, Z0 + MH * .2 + 40), "膜引线"))
    # ① 主镜 5mm 银镜（往 -Y 爆炸）
    S.append(box((MW, 5, MH), (0, YW - EY, Z0), "主镜 900×700"))
    S.append(box((MW - 44, 3, MH - 44), (22, YW - EY - 3, Z0 + 22), "镜面"))

    # ③ 两侧壁镜 300 宽 + 顶面镜同宽
    for sgn, x in ((-1, -5), (1, MW)):
        S.append(box((5, SD, MH), (x + sgn * ES, YW - SD, Z0), "侧壁镜 300"))
    S.append(box((MW, SD, 5), (0, YW - SD, Z0 + MH + ET), "顶面镜"))

    # ④ 镜前灯带：藏在镜与镜的夹角
    for sgn, x in ((-1, 0), (1, MW - 24)):
        S.append(box((24, SD - 40, 24), (x + sgn * ES * .55, YW - SD + 20, Z0 + MH - 28), "镜前灯带"))
    S.append(box((MW - 60, 24, 24), (30, YW - SD + 20, Z0 + MH + ET * .55), "镜前灯带"))

    items = [("①", "主镜 900×700，5mm 银镜", (MW * .42, YW - EY - 3, Z0 + MH * .76)),
             ("②", "电热除雾膜 40W，覆盖中央 60%", (MW * .2 + FX + FW - 60, YW - EY * .48, Z0 + MH * .5)),
             ("③", "两侧壁镜 300 宽，顶面镜同宽", (MW + ES, YW - SD * .4, Z0 + MH * .62)),
             ("④", "镜前灯带 2700~5000K，藏夹角", (MW / 2, YW - SD + 26, Z0 + MH + ET * .55 + 12)),
             ("⑤", "防潮基板 + 防霉胶收边，可整块换", (MW + 36, YW - 16, Z0 + MH * .94))]
    audit(items, S, -68, 18)
    p = draw("0202-2", "六面镜光箱", items, S,
             note="洗手台三面围成开口朝人的光箱，灯箱落下来的光在几面镜子之间来回反射，脸上不留阴影",
             sig="设想 · 0202", az=-68, el=18, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0202-3
def fig3():
    S = []
    CW, CD, CH = 760, 560, 900          # 检修柜：柜内留 30cm 检修空间

    fl = box((2100, CD + 760, 40), (-560, -600, -40), "地面"); fl.shade = False; S.append(fl)
    wl = box((1900, 60, 1060), (-400, CD, -20), "马桶后隔墙"); wl.shade = False; S.append(wl)

    # 柜体（开口朝 -Y）
    car = [box((22, CD, CH), (0, 0, 0), "检修柜"), box((22, CD, CH), (CW - 22, 0, 0), "检修柜"),
           box((CW, CD, 22), (0, 0, 0), "检修柜"), box((CW, CD, 22), (0, 0, CH - 22), "检修柜"),
           box((CW, 22, CH), (0, CD - 22, 0), "检修柜背板")]
    S.append(merge(car, "检修柜"))

    # ⑤ 磁吸镜面柜门（往 -Y 爆炸）
    S.append(box((CW, 26, CH), (0, -560, 0), "磁吸镜面柜门"))
    S.append(box((CW - 80, 5, CH - 80), (40, -566, 40), "镜面"))
    for zz in (CH * .27, CH * .73):
        S.append(box((34, 52, 60), (CW - 80, -34, zz), "磁吸块"))

    # ① 40L 密封 PE 集水箱（往 +X 抽出柜外）
    TW, TD, TH = 470, 380, 330
    tx, ty, tz = 1000, 70, 0
    tk = [box((TW, 22, TH), (tx, ty, tz), "40L 集水箱"), box((TW, 22, TH), (tx, ty + TD - 22, tz), "40L 集水箱"),
          box((22, TD - 44, TH), (tx, ty + 22, tz), "40L 集水箱"), box((22, TD - 44, TH), (tx + TW - 22, ty + 22, tz), "40L 集水箱"),
          box((TW, TD, 22), (tx, ty, tz), "40L 集水箱底")]
    S.append(merge(tk, "40L 集水箱"))
    S.append(box((TW, TD, 22), (tx, ty, tz + TH + 520), "密封箱盖"))
    S.append(cyl(46, 120, "z", (tx + 90, ty + 300, tz + TH + 542), 16, "活性炭排气阀"))

    # ② 切割式潜污泵 600W（从箱里往上爆炸）
    ZP = tz + TH + 180
    PCX, PCY = tx + TW * .40, ty + TD / 2
    S.append(cyl(92, 190, "z", (PCX, PCY, ZP), 20, "600W 潜污泵"))
    S.append(cyl(104, 48, "z", (PCX, PCY, ZP - 48), 20, "切割刀盘"))
    for i in range(6):
        a = i * math.pi / 3
        S.append(box((84, 18, 28), (PCX + math.cos(a) * 26, PCY + math.sin(a) * 26 - 9, ZP - 42), "切割刀"))
    S.append(cyl(28, 110, "z", (PCX, PCY, ZP + 190), 14, "泵出口"))

    # ③ 双浮球：低位启停 + 高位报警
    for zz, nm in ((tz + 90, "低位浮球"), (tz + 250, "高位浮球")):
        S.append(cyl(54, 78, "z", (tx + TW + 200, ty + TD * .3, zz), 16, nm))
        S.append(cyl(6, 430 - (zz - tz), "z", (tx + TW + 200, ty + TD * .3, zz + 78), 8, "浮球线"))
    S.append(box((40, 44, 120), (tx + TW + 180, ty + TD * .3 - 22, tz + 430), "浮球支架"))

    # ④ 出水 DN40：止回阀 + 检修球阀
    XV, YV = tx + TW + 460, ty + TD * .72
    S.append(cyl(24, 760, "z", (XV, YV, tz + 60), 14, "DN40 出水管"))
    S.append(box((96, 96, 130), (XV - 48, YV - 48, tz + 250), "DN40 止回阀"))
    S.append(cyl(36, 120, "z", (XV, YV, tz + 500), 14, "检修球阀"))
    S.append(box((130, 36, 36), (XV - 65, YV - 18, tz + 560), "球阀手柄"))
    S.append(cyl(24, -400, "x", (XV, YV, tz + 790), 14, "接原有下水口"))

    items = [("①", "40L 密封 PE 集水箱", (tx + TW, ty + TD / 2, tz + TH * .55)),
             ("②", "切割式潜污泵 600W，扬程 4m", (PCX + 92, PCY, ZP + 110)),
             ("③", "双浮球：低位启停 + 高位报警", (tx + TW + 200, ty + TD * .3 - 54, tz + 280)),
             ("④", "DN40 止回阀 + 检修球阀", (XV + 48, YV - 48, tz + 320)),
             ("⑤", "磁吸镜面柜门，柜内留 30cm", (CW * .5, -566, CH * .58))]
    audit(items, S, -62, 20)
    p = draw("0202-3", "污水提升泵检修柜", items, S,
             note="藏在马桶后的柜子里：淋浴、洗手盆和 0203 的冷凝水靠重力流不走，先汇进集水箱再绞碎顶进原有下水口",
             sig="设想 · 0202", az=-62, el=20, fov=27)
    print("saved", p)


fig1(); fig2(); fig3()
