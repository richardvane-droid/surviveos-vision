"""0205 生态鱼缸 — 硬件爆炸图
0205-1 吧台缸体与过滤总成 / 0205-2 水质监测探头盒
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, extrusion, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

TW, TD, TH = 800, 400, 500        # 缸体 800×400×500
CW, CD, CH = 950, 520, 900        # 吧台矮柜段 900 高


# ---------------------------------------------------------------- 0205-1
def fig1():
    S = []
    wl = box((1700, 60, 2000), (-200, CD, -20), "木屋北墙"); wl.shade = False; S.append(wl)
    fl = box((1700, 2000, 40), (-200, -1400, -40), "地面"); fl.shade = False; S.append(fl)

    # ② 吧台矮柜段：方钢框架 + 实木面板
    fr = []
    for dx in (20, CW - 60):
        for dy in (20, CD - 60):
            fr.append(extrusion(CH - 40, "z", (dx, dy, 0), 40, "40 方钢"))
    for zz in (20, CH - 80):
        fr.append(extrusion(CW - 120, "x", (40, 20, zz), 40, "40 方钢"))
        fr.append(extrusion(CW - 120, "x", (40, CD - 60, zz), 40, "40 方钢"))
        fr.append(extrusion(CD - 120, "y", (20, 40, zz), 40, "40 方钢"))
        fr.append(extrusion(CD - 120, "y", (CW - 60, 40, zz), 40, "40 方钢"))
    S.append(merge(fr, "方钢框架"))
    S.append(box((30, CD, CH), (-30, 0, 0), "实木面板"))
    S.append(box((30, CD, CH), (CW, 0, 0), "实木面板"))
    S.append(box((CW + 180, CD + 90, 44), (-90, -40, CH), "吧台台面"))

    # ③ 底滤仓三段（从柜里往 -Y 抽出来）
    SY, SZ = -1080, 70
    S.append(box((680, 420, 30), (150, SY, SZ), "底滤仓底"))
    for i, nm in enumerate(("过滤棉", "陶瓷环", "变频水泵")):
        x0 = 150 + i * 226
        S.append(box((10, 420, 300), (x0, SY, SZ + 30), "隔板"))
        if i == 0:
            for k in range(3):
                S.append(box((196, 380, 54), (x0 + 16, SY + 20, SZ + 60 + k * 66), nm))
        elif i == 1:
            for k in range(14):
                S.append(cyl(26, 46, "y", (x0 + 50 + (k % 4) * 46, SY + 60 + (k // 4) * 84, SZ + 80 + (k % 3) * 52), 10, nm))
        else:
            S.append(cyl(80, 200, "z", (x0 + 110, SY + 200, SZ + 40), 18, nm))
            S.append(cyl(26, 150, "y", (x0 + 110, SY + 200, SZ + 150), 12, "泵出口"))
    S.append(box((10, 420, 300), (150 + 678, SY, SZ + 30), "隔板"))

    # ① 缸体 800×400×500 超白玻璃（往上爆炸）+ 造景
    ZG = CH + 44 + 480
    gl = [box((TW, 10, TH), (80, 60, ZG), "超白玻璃"), box((TW, 10, TH), (80, 60 + TD - 10, ZG), "超白玻璃"),
          box((10, TD - 20, TH), (80, 70, ZG), "超白玻璃"), box((10, TD - 20, TH), (80 + TW - 10, 70, ZG), "超白玻璃"),
          box((TW, TD, 12), (80, 60, ZG), "缸底")]
    S.append(merge(gl, "超白玻璃缸体"))
    S.append(box((TW - 30, TD - 30, 60), (95, 75, ZG + 12), "矮珍珠底床"))
    for (dx, dy, r, h) in ((150, 120, 46, 240), (330, 250, 34, 300), (560, 150, 40, 210)):
        S.append(cyl(r, h, "z", (80 + dx, 60 + dy, ZG + 72), 12, "沉木"))
    S.append(cyl(40, 460, "z", (80 + TW - 70, 60 + TD - 60, ZG + 12), 14, "溢流管"))

    # ④ 水草灯 PWM 调光
    S.append(box((TW - 60, 180, 70), (110, 170, ZG + TH + 300), "水草灯"))
    for i in range(6):
        S.append(box((80, 140, 14), (140 + i * 118, 190, ZG + TH + 286), "灯珠条"))
    S.append(cyl(16, 300, "z", (80 + TW - 40, 60 + TD - 40, ZG + TH), 10, "灯支架"))

    # ⑤ 做旧木窗框收边（往 -Y 爆炸）
    FY = -620
    wf = [box((TW + 120, 60, 80), (20, FY, ZG - 60), "做旧木窗框"),
          box((TW + 120, 60, 80), (20, FY, ZG + TH), "做旧木窗框"),
          box((80, 60, TH + 60), (20, FY, ZG - 60), "做旧木窗框"),
          box((80, 60, TH + 60), (20 + TW + 40, FY, ZG - 60), "做旧木窗框"),
          box((40, 50, TH + 60), (20 + TW / 2 - 20, FY + 5, ZG - 60), "窗棂")]
    S.append(merge(wf, "做旧木窗框"))

    items = [("①", "缸体 800×400×500 超白玻璃", (80 + TW, 60 + TD * .5, ZG + TH * .5)),
             ("②", "柜内方钢框架独立承重 160kg", (CW - 20, 40, CH * .5)),
             ("③", "底滤三段：棉 → 陶瓷环 → 水泵", (150 + 452 + 110 + 80, SY + 200, SZ + 140)),
             ("④", "水草灯 PWM 调光，缸后留 10cm", (110 + TW - 60, 260, ZG + TH + 330)),
             ("⑤", "做旧木窗框收边，像窗不像设备", (20 + TW + 120, FY, ZG + TH * .5))]
    audit(items, S, -34, 20)
    p = draw("0205-1", "吧台缸体与过滤总成", items, S,
             note="缸不在地堡：坐在隔墙木屋一侧北墙吧台台面东段、照片墙正下方，只有探头数据线穿隔墙接进地堡 0802 大屏",
             sig="设想 · 0205", az=-34, el=20, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0205-2
def fig2():
    S = []
    BW, BD, BH = 220, 160, 110         # IP65 防水盒
    # 盒体
    bd = [box((BW, 8, BH), (0, 0, 0), "IP65 防水盒"), box((BW, 8, BH), (0, BD - 8, 0), "IP65 防水盒"),
          box((8, BD - 16, BH), (0, 8, 0), "IP65 防水盒"), box((8, BD - 16, BH), (BW - 8, 8, 0), "IP65 防水盒"),
          box((BW, BD, 8), (0, 0, 0), "盒底")]
    S.append(merge(bd, "IP65 防水盒"))

    # ⑤ 上盖 + 小屏窗（往上爆炸）
    ZL = BH + 250
    S.append(box((BW, BD, 12), (0, 0, ZL), "上盖"))
    S.append(box((110, 62, 16), (55, 49, ZL + 12), "小屏窗"))
    S.append(box((96, 50, 4), (62, 55, ZL + 28), "读数屏"))
    for dx, dy in ((14, 14), (BW - 22, 14), (14, BD - 22), (BW - 22, BD - 22)):
        S += screw((dx + 4, dy + 4, ZL + 12), 5, 46, "z", "盖螺丝")

    # ③ ESP32 + ESPHome（盒内最上一层）
    S.append(box((170, 110, 2), (25, 25, BH + 150), "主板"))
    S.append(box((58, 28, 12), (60, 66, BH + 152), "ESP32"))
    S.append(box((40, 22, 9), (130, 40, BH + 152), "电源模块"))
    for dx in (34, 150):
        S.append(box((14, 40, 8), (dx, 38, BH + 152), "接线端子"))

    # ② BNC 放大板 + TDS 板
    S.append(box((90, 70, 2), (22, 30, BH + 56), "BNC 放大板"))
    S.append(cyl(16, 34, "z", (52, 64, BH + 58), 14, "BNC 座"))
    S.append(box((26, 20, 8), (30, 36, BH + 58), "运放"))
    S.append(box((80, 60, 2), (126, 40, BH + 56), "TDS 板"))
    S.append(box((30, 18, 8), (140, 62, BH + 58), "TDS 芯片"))

    # ④ 穿线接头 ×3（盒侧）
    for i in range(3):
        S.append(cyl(18, 46, "y", (44 + i * 66, -46, 46), 14, "穿线接头"))
        S.append(cyl(22, 14, "y", (44 + i * 66, -12, 46), 14, "压帽"))

    # ① 三根探头（从穿线接头往 -Y 拉出来，横着摆）
    PY = -350
    S.append(cyl(10, 200, "y", (44, PY, 46), 14, "DS18B20"))
    S.append(cyl(14, -40, "y", (44, PY, 46), 14, "不锈钢探头尖"))
    S.append(cyl(4, 108, "y", (44, PY + 200, 46), 8, "探头线"))
    S.append(cyl(15, 230, "y", (110, PY, 46), 16, "pH 玻璃电极"))
    S.append(cyl(15, -32, "y", (110, PY, 46), 12, "玻璃球"))
    S.append(cyl(12, 56, "y", (110, PY + 230, 46), 14, "BNC 头"))
    S.append(cyl(4, 22, "y", (110, PY + 286, 46), 8, "探头线"))
    S.append(box((32, 200, 26), (161, PY, 33), "TDS 探头"))
    S.append(box((20, -44, 15), (167, PY, 38), "电极片"))
    S.append(cyl(4, 108, "y", (176, PY + 200, 46), 8, "探头线"))

    items = [("①", "DS18B20 / pH 电极 / TDS 三探头", (110, PY + 60, 46 + 15)),
             ("②", "pH 需 BNC 放大板，TDS 测导电率", (52 + 16, 64, BH + 74)),
             ("③", "ESP32 + ESPHome，每分钟发 HA", (89, 80, BH + 158)),
             ("④", "穿线接头密封，盒体 IP65", (110, -46, 46 + 18)),
             ("⑤", "上盖开小屏窗，路过抬眼就看到", (110, 80, ZL + 30))]
    audit(items, S, -48, 22)
    p = draw("0205-2", "水质监测探头盒", items, S,
             note="三路信号汇到一块 ESP32，pH 每季度校准一次；软水目标 100~200ppm，数值每分钟发给 HomeAssistant",
             sig="设想 · 0205", az=-48, el=22, fov=27)
    print("saved", p)


fig1(); fig2()
