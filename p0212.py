"""0212 哑铃 — 硬件爆炸图
0212-1 可调哑铃与铃架 / 0212-2 墙装单杠与折叠仰卧板
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, extrusion, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw


# ---------------------------------------------------------------- 0212-1
def fig1():
    S = []
    # ⑤ 2cm 折叠橡胶垫 1×2m（铺在地毯上）
    S.append(box((2000, 1000, 20), (-500, -260, 0), "2cm 折叠橡胶垫"))
    for i in range(3):
        S.append(box((10, 1000, 24), (-500 + (i + 1) * 500, -260, 0), "折叠缝"))
    wl = box((1500, 60, 1000), (-250, 700, 0), "南墙"); wl.shade = False; S.append(wl)

    # ④ 方管 40×40 焊接铃架：两层
    RW, RD, RH = 1000, 420, 720
    rk = []
    for dx in (0, RW - 40):
        for dy in (0, RD - 40):
            rk.append(extrusion(RH, "z", (dx, dy, 20), 40, "40×40 方管"))
    for zz in (330, RH - 20):
        rk.append(extrusion(RW - 80, "x", (40, 0, zz), 40, "40×40 方管"))
        rk.append(extrusion(RW - 80, "x", (40, RD - 40, zz), 40, "40×40 方管"))
        rk.append(extrusion(RD - 80, "y", (0, 40, zz), 40, "40×40 方管"))
        rk.append(extrusion(RD - 80, "y", (RW - 40, 40, zz), 40, "40×40 方管"))
    for lv in (370, RH + 20):
        rk.append(box((RW, RD, 22), (0, 0, lv), "架层板"))
    S.append(merge(rk, "方管铃架"))
    for dx in (20, RW - 60):
        for dy in (20, RD - 60):
            S.append(box((60, 60, 20), (dx - 10, dy - 10, 0), "橡胶脚垫"))

    # 下层壶铃
    for i, r in enumerate((80, 96)):
        cx = 260 + i * 400
        S.append(cyl(r, 150, "z", (cx, RD * .5, 392), 18, "壶铃"))
        S.append(box((36, 130, 70), (cx - 110, RD * .5 - 65, 542), "壶铃把"))
        S.append(box((36, 130, 70), (cx + 74, RD * .5 - 65, 542), "壶铃把"))
        S.append(box((150, 130, 36), (cx - 75, RD * .5 - 65, 612), "壶铃把"))

    # ② 底座（配重片的停车位，带槽位）+ ③ 配重片
    BX, BY, BZ = 90, RD * .5 - 115, RH + 42
    S.append(box((520, 230, 70), (BX, BY, BZ), "哑铃底座"))
    for i in range(9):
        S.append(box((10, 230, 90), (BX + 40 + i * 52, BY, BZ + 70), "底座槽位"))
    for i in range(8):                                  # 铸铁配重片 + 橡胶包边
        hh = 150 if i < 3 else 120
        S.append(box((40, 190, hh), (BX + 52 + i * 52, BY + 20, BZ + 78), "铸铁配重片"))
        S.append(box((44, 20, hh), (BX + 50 + i * 52, BY + 16, BZ + 78), "橡胶包边"))
        S.append(box((44, 20, hh), (BX + 50 + i * 52, BY + 194, BZ + 78), "橡胶包边"))

    # ① 可调哑铃：握把 + 两端选重旋钮 + 咬住的卡爪（往上爆炸）
    ZD = BZ + 600
    CY = BY + 115
    db = [cyl(22, 340, "x", (BX + 90, CY, ZD), 14, "握把")]
    for i in range(10):
        db.append(cyl(25, 8, "x", (BX + 100 + i * 32, CY, ZD), 14, "滚花"))
    for xx in (BX + 40, BX + 430):
        db.append(cyl(44, 50, "x", (xx, CY, ZD), 16, "选重旋钮"))
        for k in range(8):
            a = k * math.pi / 4
            db.append(box((50, 16, 16), (xx, CY + math.cos(a) * 44 - 8, ZD + math.sin(a) * 44 - 8), "旋钮齿"))
    S.append(merge(db, "可调哑铃"))
    for sgn, xx in ((1, BX + 66), (-1, BX + 366)):      # 卡爪咬住的片
        for i in range(2):
            S.append(box((36, 176, 136), (xx + sgn * i * 44, CY - 88, ZD - 68), "咬住的配重片"))

    items = [("①", "可调哑铃 2~32kg，旋钮选重", (BX + 230, CY - 25, ZD + 22)),
             ("②", "底座槽位定位，对准才能换重", (BX + 520, BY + 115, BZ + 40)),
             ("③", "配重片铸铁 + 橡胶包边", (BX + 52 + 6 * 52 + 40, BY + 110, BZ + 190)),
             ("④", "方管 40×40 焊接铃架，两层", (RW, 20, 500)),
             ("⑤", "2cm 折叠橡胶垫 1×2m", (-380, -200, 20))]
    audit(items, S, -50, 20)
    p = draw("0212-1", "可调哑铃与铃架", items, S,
             note="地堡东南角门口那一小片：一副可调哑铃顶一整排，2~32kg 十几个档位只占一个底座的位置",
             sig="设想 · 0212", az=-50, el=20, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0212-2
def fig2():
    S = []
    DH, DW = 2000, 900                    # 东南角 90×90 对外开门
    # 东墙（开门洞）+ 南墙：只给够用的一块
    for b in (box((70, 500, 2500), (-70, 0, 0), "东墙"),
              box((70, 420, 2500), (-70, DW + 500, 0), "东墙"),
              box((70, DW, 500), (-70, 500, DH), "东墙"),
              box((1950, 70, 2500), (0, -70, 0), "南墙"),
              box((2020, 1820, 40), (-70, -70, -40), "地面")):
        b.shade = False; S.append(b)

    # ② 三角支架 ×2 + M12 膨胀螺栓 ×4（往 +X 爆炸）
    XA = 330
    for yy in (560, 1340):
        tri = prism([(0, 0), (240, 0), (0, -260)], 60, "y", (XA, yy, 2160), "三角支架")
        S.append(tri)
        S.append(box((26, 60, 320), (XA - 26, yy, 1900), "贴墙板"))
    for yy in (560, 1340):
        for dz in (1960, 2170):
            S += screw((XA - 120, yy + 30, dz), 11, 150, "x", "M12 膨胀螺栓")

    # ① 单杠 32mm 钢管，离地 2.1m（最外层）
    XB = 700
    S.append(cyl(16, 1100, "y", (XB, 400, 2100), 18, "32mm 单杠"))
    for i in range(22):
        S.append(cyl(18, 6, "y", (XB, 460 + i * 40, 2100), 14, "滚花"))
    for yy in (560, 1340):
        S.append(box((150, 70, 70), (XB - 75, yy - 5, 2065), "杆座"))

    # ③ 折叠仰卧板：铰链上墙 + 板面 + 撑杆
    HB = 520
    brd = box((640, 1360, 60), (300, 0, HB), "折叠仰卧板")
    brd = rot(brd, -7, "x", (600, 0, HB))
    S.append(brd)
    for dx in (340, 880):
        S.append(cyl(16, 90, "x", (dx, 10, HB), 12, "铰链"))
    S.append(box((160, 60, 130), (350, 200, HB + 60), "腿垫"))
    S.append(box((160, 60, 130), (350, 360, HB + 60), "腿垫"))
    S.append(cyl(18, -330, "z", (620, 1240, HB - 110), 12, "撑杆"))
    S.append(box((240, 70, 40), (500, 1210, 60), "撑杆脚"))

    # ④ 60×180 窄镜 + 镜顶灯带（南墙，往 +Y 爆炸）
    YM = 380
    S.append(box((600, 14, 1800), (1180, YM, 300), "60×180 窄镜"))
    S.append(box((560, 6, 1760), (1200, YM - 6, 320), "镜面"))
    S.append(box((620, 60, 50), (1170, YM - 20, 2110), "镜顶灯带"))
    for i in range(7):
        S.append(box((60, 20, 16), (1190 + i * 84, YM - 34, 2118), "灯珠"))

    # ⑤ 木凳 + 水壶架 + 毛巾钩（挤在墙角）
    S.append(box((340, 300, 40), (90, 1470, 440), "木凳"))
    for dx, dy in ((110, 1490), (400, 1490), (110, 1730), (400, 1730), ):
        S.append(cyl(18, 440, "z", (dx, dy, 0), 10, "凳腿"))
    S.append(box((70, 280, 26), (0, 1470, 1050), "水壶架"))
    S.append(cyl(46, 190, "z", (60, 1610, 1076), 16, "水壶"))
    for i in range(3):
        S.append(cyl(10, 110, "x", (0, 1500 + i * 90, 1320), 10, "毛巾钩"))

    items = [("①", "单杠 32mm 钢管，离地 2.1m", (XB, 900, 2116)),
             ("②", "三角支架 + M12 膨胀螺栓 ×4", (XA + 120, 1340 + 60, 2100)),
             ("③", "折叠仰卧板铰链上墙，收起 10cm", (620, 700, HB + 120)),
             ("④", "60×180 窄镜 + 镜顶灯带", (1480, YM - 6, 1300)),
             ("⑤", "木凳 + 水壶架 + 毛巾钩一体挂墙", (106, 1610, 1160))]
    audit(items, S, 48, 16)
    p = draw("0212-2", "墙装单杠与折叠仰卧板", items, S,
             note="单杠装在东南角 90×90 门框上方（净高 2660 够引体，头顶还有 30cm）；窄镜贴南墙朝北，与朝西的 0802 屏墙成 90° 不互相反光",
             sig="设想 · 0212", az=48, el=16, fov=27)
    print("saved", p)


fig1(); fig2()
