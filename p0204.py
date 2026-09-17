"""0204 系统设计工作台 — 硬件爆炸图
0204-1 整板工作台 / 0204-2 三屏弧形支架
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, extrusion, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

DX, DY, TH, HT = 800, 1600, 40, 740      # 桌面东西 800、南北 1600、整板 40 厚、台面高 740


# ---------------------------------------------------------------- 0204-1
def fig1():
    S = []
    wl = box((70, DY + 1600, 1560), (-140, -1450, -30), "西墙"); wl.shade = False; S.append(wl)
    fl = box((DX + 700, DY + 1700, 40), (-140, -1500, -40), "地面"); fl.shade = False; S.append(fl)

    # ① 胡桃木整板 1600×800×40（往上爆炸）
    ZT = HT + 430
    S.append(box((DX, DY, TH), (0, 0, ZT), "胡桃木整板"))
    for yy in (18, DY - 30):                     # 两端伸缩缝
        S.append(box((DX, 12, 10), (0, yy, ZT - 10), "伸缩缝"))
    S.append(box((DX - 120, DY - 160, 6), (60, 80, ZT + TH), "硬蜡油面"))

    # ② 40×40 黑色方管支架（两副门形 + 后横梁）+ 可调地脚
    fr = []
    for yy in (120, DY - 160):
        fr.append(extrusion(HT - 60, "z", (60, yy, 60), 40, "40×40 方管"))
        fr.append(extrusion(HT - 60, "z", (DX - 100, yy, 60), 40, "40×40 方管"))
        fr.append(extrusion(DX - 160, "x", (60, yy, HT - 40), 40, "40×40 方管"))
    fr.append(extrusion(DY - 320, "y", (DX - 100, 160, HT - 90), 40, "后横梁"))
    S.append(merge(fr, "40×40 方管支架"))
    for xx in (60, DX - 100):
        for yy in (120, DY - 160):
            S.append(cyl(22, 60, "z", (xx + 20, yy + 20, 0), 12, "可调地脚"))
            S.append(cyl(34, 16, "z", (xx + 20, yy + 20, 0), 14, "脚垫"))

    # ③ 走线槽 + 1000VA UPS（挂桌面背沿下方，往 -X 拉出来）
    GY = -1250
    S.append(box((190, 1000, 150), (40, GY, HT - 210), "走线槽"))
    S.append(box((190, 1000, 16), (40, GY, HT - 210), "槽盖"))
    for i in range(4):
        S.append(box((90, 70, 46), (70, GY + 120 + i * 220, HT - 164), "变压器"))
        S.append(cyl(8, 110, "z", (115, GY + 155 + i * 220, HT - 210), 8, "线"))
    S.append(box((250, 430, 190), (10, GY + 260, HT - 520), "1000VA UPS"))
    S.append(box((90, 160, 70), (260, GY + 390, HT - 460), "UPS 面板"))

    # ④ 桌下 ESPHome 按键板（3 键）往下爆炸
    BX_, BY_ = 300, 90
    S.append(box((BX_, BY_, 22), (320, -280, HT - 300), "ESPHome 按键板"))
    for i in range(3):
        S.append(cyl(28, 26, "z", (370 + i * 100, -280 + BY_ / 2, HT - 278), 14, "按键"))

    # ⑤ 南端样件托盘 ≈30cm
    S.append(box((DX - 160, 300, 26), (80, DY - 330, ZT + TH + 8), "样件托盘"))
    for (dx, dy, w, d, h) in ((60, 40, 110, 90, 130), (220, 70, 80, 80, 90), (380, 30, 140, 120, 70)):
        S.append(box((w, d, h), (80 + dx, DY - 330 + dy, ZT + TH + 34), "3D 打印件"))

    items = [("①", "胡桃木整板 1600×800×40", (DX, DY * .45, ZT + TH * .5)),
             ("②", "40×40 黑方管支架 + 可调地脚", (DX - 60, DY - 150, HT * .45)),
             ("③", "走线槽 + 1000VA UPS 撑 15 分钟", (260, GY + 470, HT - 430)),
             ("④", "桌下 ESPHome 按键板：3 键", (470, -235, HT - 252)),
             ("⑤", "南端 30cm 样件托盘放打印件", (DX - 100, DY - 50, ZT + TH + 26))]
    audit(items, S, 34, 20)
    p = draw("0204-1", "整板工作台", items, S,
             note="西墙、衣架再往南：桌面东西 800、南北 1600，南端离南墙 ≈35cm，图纸挂在桌前那面西墙上",
             sig="设想 · 0204", az=34, el=20, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0204-2
def fig2():
    S = []
    E, ZE = 150, 660                               # 屏幕往 +X 一点、主要往上爆炸
    PX = 110                                       # 快拆板所在的 x
    tb = box((280, 1700, 40), (-140, -850, 700), "桌板 20~60 厚"); tb.shade = False; S.append(tb)

    # ① 桌夹 + Φ35 立柱
    S.append(box((150, 160, 40), (-140, -80, 700), "C 形夹"))
    S.append(box((34, 160, 150), (-140, -80, 620), "C 形夹"))
    S.append(box((110, 120, 26), (-130, -60, 640), "夹板"))
    S.append(cyl(24, 60, "z", (-40, 0, 610), 12, "夹紧旋钮"))
    S.append(cyl(18, 620, "z", (-60, 0, 740), 16, "Φ35 立柱"))
    for zz in (900, 1090, 1230):
        S.append(cyl(26, 14, "z", (-60, 0, zz - 8), 14, "柱环"))

    specs = [(+700, "27 寸竖屏", 340, 600, -25, 1240),
             (0,    "34 寸带鱼屏", 810, 350, 0, 1050),
             (-700, "27 寸竖屏", 340, 600, 25, 1145)]
    for (yc, nm, sw, sh, ang, zz) in specs:
        # ② 气弹簧臂：柱套 + 沿 Y 的大臂 + 肘 + 沿 X 的小臂
        S.append(cyl(30, 90, "z", (-60, 0, zz - 45), 14, "臂座"))
        if yc:
            g = 1 if yc > 0 else -1
            S.append(box((46, abs(yc), 54), (-83, min(0, yc), zz - 27), "气弹簧大臂"))
            S.append(cyl(27, 80, "z", (-60, yc, zz - 40), 12, "肘关节"))
            S.append(box((30, abs(yc) - 60, 16), (-70, min(0, yc) + 30 * g if yc < 0 else 30, zz - 6), "气弹簧筒"))
        S.append(box((PX + 60, 46, 50), (-60, yc - 23, zz - 25), "气弹簧小臂"))
        # ⑤ VESA 快拆板 + 拔销（留在臂端）
        pl = merge([box((18, 160, 160), (PX, -80, zz - 80), "VESA 快拆板"),
                    box((40, 22, 22), (PX - 40, -11, zz - 11), "拔销")], "VESA 快拆板")
        S.append(rot(pl, ang, "z", (PX, 0, zz)).moved((0, yc, 0)))
        # ③④ 屏幕（显示面朝 +X，背座朝 -X），往 +X 爆炸
        zb = zz - sh * .45 + ZE
        scr = [box((46, sw, sh), (PX + E, -sw / 2, zb), nm),
               box((10, sw - 46, sh - 46), (PX + E + 46, -sw / 2 + 23, zb + 23), "显示面"),
               box((74, 150, 150), (PX + E - 74, -75, zz - 75 + ZE), "VESA 背座")]
        S.append(rot(merge(scr, nm), ang, "z", (PX + E, 0, zz + ZE)).moved((0, yc, 0)))

    items = [("①", "桌夹立柱 Φ35，夹 20~60mm 桌板", (-42, 0, 830)),
             ("②", "气弹簧臂 ×3，各承重 2~9kg", (-37, 400, 1250)),
             ("③", "34 寸带鱼屏 3440×1440 居中", (PX + E + 56, 0, 1050 + ZE + 40)),
             ("④", "竖屏 27 寸 ×2，内收 25°", (PX + E + 56, -700, 1145 + ZE + 160)),
             ("⑤", "VESA 75/100 快拆板，一键拔销", (PX + 18, 700, 1240 + 60))]
    audit(items, S, 26, 18)
    p = draw("0204-2", "三屏弧形支架", items, S,
             note="三块屏排成一段弧、正好落在左右各 30° 的舒适视野里；转头看侧屏不用重新对焦",
             sig="设想 · 0204", az=26, el=18, fov=27)
    print("saved", p)


fig1(); fig2()
