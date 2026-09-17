"""0207 影音室 — 硬件爆炸图
0207-1 98 寸电视挂墙总成 / 0207-2 低音炮减震座
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

TVW, TVH, TVT = 2200, 1240, 62       # 98 寸：宽约 220cm
Z0 = 760                             # 电视下沿


# ---------------------------------------------------------------- 0207-1
def fig1():
    S = []
    wl = box((2500, 240, 2320), (-150, 0, -20), "南侧砖隔墙"); wl.shade = False; S.append(wl)
    fl = box((2900, 2500, 40), (-350, -2300, -40), "地面"); fl.shade = False; S.append(fl)

    # ② 钢制壁挂底板 + M10 膨胀螺栓 ×4
    YB = -520
    S.append(box((860, 12, 620), (TVW / 2 - 430, YB, Z0 + 300), "钢制壁挂底板"))
    for dx in (90, 770):
        for dz in (90, 530):
            S += screw((TVW / 2 - 430 + dx, YB + 12, Z0 + 300 + dz), 10, 190, "y", "M10 膨胀螺栓")
    for i in range(6):
        S.append(box((820, 14, 26), (TVW / 2 - 410, YB - 2, Z0 + 340 + i * 90), "底板加强筋"))

    # ③ VESA 800×400 挂臂（两根立轨 + 上下挂钩）
    YA = -1060
    arm = []
    for dx in (-400, 400):
        arm.append(box((70, 60, 560), (TVW / 2 + dx - 35, YA, Z0 + 330), "VESA 立轨"))
        for dz in (0, 400):
            arm.append(box((150, 40, 60), (TVW / 2 + dx - 75, YA - 40, Z0 + 430 + dz), "VESA 挂钩"))
    arm.append(box((880, 50, 70), (TVW / 2 - 440, YA + 5, Z0 + 700), "挂臂横梁"))
    S.append(merge(arm, "VESA 800×400 挂臂"))

    # ④ 电视背面 WS2812 灯带（约 300 颗）
    YL = -1560
    for (w, d, h, ox, oz) in ((TVW - 260, 16, 22, 130, 90), (TVW - 260, 16, 22, 130, TVH - 112),):
        S.append(box((w, d, h), (ox, YL, Z0 + oz), "WS2812 灯带"))
    for oz in (0,):
        S.append(box((22, 16, TVH - 260), (130, YL, Z0 + 130), "WS2812 灯带"))
        S.append(box((22, 16, TVH - 260), (TVW - 152, YL, Z0 + 130), "WS2812 灯带"))
    for i in range(26):
        S.append(box((26, 20, 12), (150 + i * 74, YL - 4, Z0 + 84), "灯珠"))

    # ① 98 寸电视（往 -Y 爆炸到最外）
    YT = -2000
    S.append(box((TVW, TVT, TVH), (0, YT, Z0), "98 寸 4K 电视"))
    S.append(box((TVW - 110, 12, TVH - 110), (55, YT - 12, Z0 + 55), "屏面"))
    S.append(box((820, 30, 420), (TVW / 2 - 410, YT + TVT, Z0 + 400), "VESA 背板"))

    # ⑤ 220×40 实木矮机柜 + 暗管
    S.append(box((2200, 400, 420), (0, -420, 0), "实木矮机柜"))
    for i in range(3):
        S.append(box((700, 16, 110), (60 + i * 720, -436, 90 + (i % 2) * 180), "功放 / 播放器 / 唱盘"))
    S.append(box((2200, 400, 30), (0, -420, 420), "柜面"))
    S.append(cyl(40, Z0 + 340 - 450, "z", (TVW / 2 + 620, 120, 450), 14, "隔墙暗管"))
    S.append(cyl(40, -420, "y", (TVW / 2 + 620, 120, 450), 14, "暗管入口"))

    items = [("①", "98 寸 4K 电视，宽 220、约 60kg", (TVW * .42, YT - 10, Z0 + TVH * .62)),
             ("②", "钢制底板 + M10 膨胀螺栓 ×4", (TVW / 2 + 430, YB - 2, Z0 + 700)),
             ("③", "VESA 800×400 挂臂，可前倾几度", (TVW / 2 + 400 - 75, YA - 40, Z0 + 860)),
             ("④", "背面约 300 颗 WS2812 供跟色灯", (TVW - 130, YL, Z0 + 620)),
             ("⑤", "220×40 实木矮机柜，线走隔墙暗管", (TVW, -300, 230))]
    audit(items, S, -44, 16)
    p = draw("0207-1", "98 寸电视挂墙总成", items, S,
             note="南侧梁下隔墙、梁底 2400 以下的地堡一侧；正对北边沙发，观影距离 ≈2.5m，地堡没窗够黑，普通 4K 面板反而更准",
             sig="设想 · 0207", az=-44, el=16, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0207-2
def fig2():
    S = []
    A = 400                                     # 占地 ≈40×40
    fl = box((1300, 1300, 40), (-450, -450, -40), "地面"); fl.shade = False; S.append(fl)
    wl = box((1100, 60, 700), (-350, 460, -20), "墙角"); wl.shade = False; S.append(wl)

    # ① 橡胶减震垫 20mm（隔开水泥地）
    S.append(box((A, A, 20), (0, 0, 0), "橡胶减震垫 20mm"))
    for i in range(5):
        S.append(box((A, 18, 6), (0, 30 + i * 84, 20), "防滑纹"))

    # ② 木箱底座填干砂（≈25kg 配重）
    ZB = 250
    bx = [box((A, 16, 300), (0, 0, ZB), "木箱底座"), box((A, 16, 300), (0, A - 16, ZB), "木箱底座"),
          box((16, A - 32, 300), (0, 16, ZB), "木箱底座"), box((16, A - 32, 300), (A - 16, 16, ZB), "木箱底座"),
          box((A, A, 16), (0, 0, ZB), "箱底")]
    S.append(merge(bx, "木箱底座"))
    for i in range(4):                          # 干砂
        S.append(box((A - 60, A - 60, 26), (30, 30, ZB + 26 + i * 30), "干砂配重"))

    # ③ 弹簧减震器 ×4
    ZS = 740
    for dx, dy in ((60, 60), (A - 120, 60), (60, A - 120), (A - 120, A - 120)):
        S.append(box((80, 80, 12), (dx - 10, dy - 10, ZS), "弹簧座"))
        for k in range(6):
            S.append(cyl(30, 9, "z", (dx + 30, dy + 30, ZS + 16 + k * 18), 14, "弹簧减震器"))
        S.append(box((80, 80, 12), (dx - 10, dy - 10, ZS + 124), "弹簧压板"))

    # ④ 18mm 多层板托板
    ZP = 1010
    S.append(box((A, A, 18), (0, 0, ZP), "18mm 多层板托板"))
    for i in range(7):
        S.append(box((A, 6, 2), (0, 24 + i * 52, ZP + 18), "多层板层线"))

    # ⑤ 低音炮
    ZW = 1260
    S.append(box((360, 360, 400), (20, 20, ZW), "低音炮"))
    S.append(cyl(130, 30, "y", (200, 20, ZW + 200), 24, "低音单元"))
    S.append(cyl(96, 16, "y", (200, 10, ZW + 200), 20, "防尘罩"))
    S.append(box((200, 20, 90), (100, 380, ZW + 60), "功放板"))

    items = [("①", "橡胶减震垫 20mm 隔开水泥地", (A * .5, 0, 10)),
             ("②", "木箱底座填干砂，约 25kg 配重", (A * .5, 0, ZB + 160)),
             ("③", "弹簧减震器 ×4，托 18mm 多层板", (350, 90, ZS + 130)),
             ("④", "18mm 多层板托板，占地 ≈40×40", (A * .5, 0, ZP + 9)),
             ("⑤", "低音炮不落地，低频不走墙体", (200, 10, ZW + 200 + 96))]
    audit(items, S, -54, 22)
    p = draw("0207-2", "低音炮减震座", items, S,
             note="塞在电视矮机柜西端旁、写字台南头的角落；低频从地板传上来是胸口发麻的震动，而不是墙壁的轰鸣",
             sig="设想 · 0207", az=-54, el=22, fov=27)
    print("saved", p)


fig1(); fig2()
