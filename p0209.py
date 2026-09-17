"""0209 藏宝阁 — 0209-1 床下密室与帆布滑门（0209-2 见 p0209_2.py）"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

RW, RD, RH = 1500, 2000, 1700        # 密室 1.5×2m、净高 1700
DY0, DW = 1480, 400                  # 帆布滑门：东侧长墙靠南，宽 40cm


def fig1():
    S = []
    # 地面 + 西侧既有结构 + 北端短墙 + 床板（天花）
    for b in (box((RW, RD, 40), (0, 0, -40), "地面"),
              box((60, RD, RH), (-60, 0, 0), "西侧既有结构"),
              box((RW, 60, RH), (0, RD, 0), "北端短墙")):
        b.shade = False; S.append(b)
    S.append(box((RW + 260, RD + 200, 60), (-80, -100, RH + 50), "床板 1750"))
    for dx, dy in ((-60, -100), (RW + 100, -100), (-60, RD + 60), (RW + 100, RD + 60)):
        S.append(box((80, 80, RH + 50), (dx, dy, 0), "架空床柱"))
    # 密室里的家具（交代这是间书房，不是帐篷）
    S.append(box((1400, 560, 30), (60, RD - 620, 710), "写字台"))
    for dx, dy in ((100, RD - 600), (1380, RD - 600), (100, RD - 120), (1380, RD - 120)):
        S.append(box((40, 40, 710), (dx, dy, 0), "台腿"))
    for i in range(5):
        S.append(box((180, 1000, 24), (10, 500, 300 + i * 320), "连续书格"))

    # ② 轻钢龙骨（东侧长墙，往 +X 爆炸）
    XK = RW + 300
    kg = [box((60, RD, 40), (XK, 0, 0), "下导轨"), box((60, RD, 40), (XK, 0, RH - 40), "上导轨")]
    for i in range(6):
        yy = i * 380
        if DY0 <= yy <= DY0 + DW:   # 门洞位置不排龙骨
            continue
        kg.append(box((50, 46, RH - 80), (XK + 5, yy, 40), "C 型竖龙骨"))
    kg.append(box((50, 46, RH - 80), (XK + 5, DY0 - 60, 40), "门洞边龙骨"))
    kg.append(box((50, 46, RH - 80), (XK + 5, DY0 + DW + 14, 40), "门洞边龙骨"))
    kg.append(box((60, DW + 74, 50), (XK, DY0 - 60, RH - 260), "门洞过梁"))
    S.append(merge(kg, "轻钢龙骨"))

    # ③ 9mm 木饰面板（再往 +X 爆炸）
    XP = RW + 800
    S.append(box((9, DY0 - 40, RH), (XP, 0, 0), "9mm 木饰面板"))
    S.append(box((9, RD - DY0 - DW - 40, RH), (XP, DY0 + DW + 40, 0), "9mm 木饰面板"))
    S.append(box((9, DW + 80, RH - 230), (XP, DY0 - 40, 0), "门洞下段饰面"))
    for i in range(4):
        S.append(box((7, 16, RH), (XP - 7, 330 + i * 330, 0), "板缝"))

    # ④⑤ 帆布滑门 + 隐藏滑轨 + 配重杆（最外层）
    XD = RW + 1240
    S.append(box((70, DW + 420, 70), (XD - 10, DY0 - 240, RH - 150), "隐藏滑轨"))
    for dy in (DY0 - 180, DY0 + DW + 120):
        S.append(cyl(24, 60, "y", (XD + 25, dy, RH - 180), 12, "滑轮"))
    S.append(box((14, DW, RH - 260), (XD, DY0, 60), "帆布滑门"))
    for i in range(7):
        S.append(box((10, DW, 8), (XD - 8, DY0, 140 + i * 200), "帆布褶"))
    S.append(cyl(26, DW, "y", (XD + 7, DY0, 40), 14, "下沿配重杆"))
    S.append(box((60, 90, 40), (XD - 22, DY0 + DW - 200, 700), "拉手"))

    items = [("①", "平面 1.5×2m、净高 1700", (750, 30, 0)),
             ("②", "轻钢龙骨围合，不承重、可拆", (XK + 60, 380, RH * .5)),
             ("③", "9mm 木饰面板，拆掉不动床体", (XP + 9, 600, RH * .62)),
             ("④", "40cm 帆布滑门 + 隐藏滑轨", (XD + 60, DY0 - 120, RH - 120)),
             ("⑤", "下沿配重杆，合上贴墙压光", (XD + 7, DY0 + DW * .5, 40 + 26))]
    audit(items, S, -62, 18)
    p = draw("0209-1", "床下密室与帆布滑门", items, S,
             note="西北角 200×120 架空床的床下：床板 1750 就是它的天花；1700 开不下平开门，入口做成侧身宽度的帆布滑门",
             sig="设想 · 0209", az=-62, el=18, fov=27)
    print("saved", p)


fig1()
