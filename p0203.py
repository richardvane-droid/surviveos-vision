"""0203 控温控湿 — 硬件爆炸图
0203-1 隐藏除湿机柜 / 0203-2 指针温湿度表盘
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw


# ---------------------------------------------------------------- 0203-1
def fig1():
    S = []
    CW, CD, CH = 780, 760, 1500          # 柜体（开口朝 -Y，爆炸方向也是 -Y）

    fl = box((1500, 3800, 40), (-260, -2700, -40), "地面"); fl.shade = False; S.append(fl)
    wl = box((1500, 70, 1700), (-260, CD, -20), "卫生间隔墙"); wl.shade = False; S.append(wl)

    car = [box((24, CD, CH), (0, 0, 0), "柜体"), box((24, CD, CH), (CW - 24, 0, 0), "柜体"),
           box((CW, CD, 24), (0, 0, 0), "柜体"), box((CW, CD, 24), (0, 0, CH - 24), "柜体"),
           box((CW, 24, CH), (0, CD - 24, 0), "柜体背板")]
    S.append(merge(car, "柜体"))

    # ② 隔音棉 30mm 内衬（整片拉出柜外）+ 橡胶减震垫 ×4
    S.append(box((CW - 40, 30, CH - 60), (20, -520, 30), "隔音棉 30mm"))
    for i in range(5):
        for j in range(9):
            S.append(box((100, 5, 100), (60 + i * 140, -525, 110 + j * 150), "绗缝格"))
    for dx, dy in ((190, -1560), (610, -1560), (190, -1200), (610, -1200)):
        S.append(box((150, 150, 50), (dx - 75, dy - 75, 0), "橡胶减震垫"))

    # ① 工业除湿机 50L/天（拉出柜外、架在减震垫上方）
    MW, MD, MH = 520, 400, 960
    mx, my, mz = 130, -1660, 330
    S.append(box((MW, MD, MH), (mx, my, mz), "50L/天 除湿机"))
    S.append(box((MW * .70, 26, MH * .32), (mx + MW * .15, my - 26, mz + MH * .54), "控制面板"))
    for i in range(9):
        S.append(box((10, MD - 90, 24), (mx + 70 + i * 42, my + 45, mz + 130), "回风格栅"))
    for dx, dy in ((70, 60), (MW - 70, 60), (70, MD - 60), (MW - 70, MD - 60)):
        S.append(cyl(36, 70, "z", (mx + dx, my + dy, mz - 70), 12, "机脚"))

    # ④ Φ100 风管软接 + 风管（机顶接出，沿天花板绕房间）
    TX, TY = mx + MW * .5, my + MD * .5
    S.append(cyl(58, 60, "z", (TX, TY, mz + MH), 18, "软接"))
    for i in range(5):
        S.append(cyl(64, 28, "z", (TX, TY, mz + MH + 60 + i * 32), 18, "软接波纹"))
    S.append(cyl(52, 380, "z", (TX, TY, mz + MH + 220), 18, "Φ100 风管"))
    S.append(cyl(52, 1500, "y", (TX, TY, mz + MH + 560), 18, "Φ100 风管"))

    # ③ DN25 冷凝水管：坡度 ≥2% 穿隔墙直排提升泵
    px, pz = mx + MW - 70, mz + 60
    S.append(cyl(20, -260, "z", (px, my + MD - 60, pz), 12, "DN25 冷凝水管"))
    S.append(box((110, 110, 74), (px - 55, my + MD - 115, pz - 300), "存水弯"))
    S.append(cyl(20, 430, "x", (px, my + MD - 60, pz - 250), 12, "DN25 冷凝水管"))
    S.append(cyl(20, 2040, "y", (px + 430, my + MD - 60, pz - 250), 12, "DN25 冷凝水管"))
    S.append(cyl(20, 140, "y", (px + 430, my + MD + 1980, pz - 320), 12, "DN25 冷凝水管"))

    # ⑤ 柜门整面进风格栅（最外层）
    dz = -2560
    dr = [box((CW, 30, CH), (0, dz, 0), "柜门")]
    for i in range(12):
        dr.append(box((CW - 90, 46, 58), (45, dz - 24, 70 + i * 116), "进风格栅"))
    S.append(merge(dr, "柜门进风格栅"))

    items = [("①", "工业除湿机 50L/天，压缩机式", (mx + MW * .5, my - 26, mz + MH * .70)),
             ("②", "隔音棉 30mm + 橡胶减震垫", (CW * .5, -524, 30 + (CH - 60) * .62)),
             ("③", "冷凝水 DN25，坡度 ≥2% 直排", (px + 430, my + MD + 700, pz - 230)),
             ("④", "Φ100 风管软接，送到四个角落", (TX, TY + 900, mz + MH + 612)),
             ("⑤", "柜门整面进风格栅，柜外 <40dB", (CW * .5, dz - 24, CH * .46))]
    audit(items, S, -28, 20)
    p = draw("0203-1", "隐藏除湿机柜", items, S,
             note="塞在东侧储藏室靠北一角、紧挨卫生间隔墙；柜门就是进风口，冷凝水就近排进隔壁 0202 的提升泵集水箱",
             sig="设想 · 0203", az=-28, el=20, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0203-2
def fig2():
    S = []
    R = 60                                   # 表盘 Φ120
    Y0, Y1, Y2, Y3, Y4, Y5 = 0, -120, -212, -320, -400, -486

    # 表壳后壳（贴墙那头）
    S.append(cyl(R + 6, 54, "y", (0, Y0, 0), 26, "表壳后壳"))
    S.append(cyl(R + 6, -8, "y", (0, Y0, 0), 26, "后盖"))
    S.append(box((26, 40, 26), (-13, Y0 + 14, -R - 30), "穿线口"))

    # ③ ESP32 板
    S.append(box((96, 1.6, 74), (-48, Y1 + 3, -37), "驱动板"))
    S.append(box((58, 5, 28), (-29, Y1 - 2, -14), "ESP32"))
    for dx, dz in ((-36, 24), (30, 24), (-36, -30)):
        S.append(box((14, 5, 9), (dx, Y1 + 4.6, dz), "板上元件"))

    # ② X27 微型步进表针 ×2
    for sgn in (-1, 1):
        S.append(box((36, 26, 34), (sgn * 26 - 18, Y2, -17), "X27 步进"))
        S.append(cyl(4, -26, "y", (sgn * 26, Y2, 0), 10, "表针轴"))

    # ① 表盘面 Φ118 + 刻度 + 45~65% 绿色舒适区
    S.append(cyl(R - 2, 8, "y", (0, Y3, 0), 30, "表盘面"))
    def sector(a0, a1, r0, r1, n=14):
        pts = [(math.cos(math.radians(a0 + (a1 - a0) * k / n)) * r1,
                math.sin(math.radians(a0 + (a1 - a0) * k / n)) * r1) for k in range(n + 1)]
        pts += [(math.cos(math.radians(a1 - (a1 - a0) * k / n)) * r0,
                 math.sin(math.radians(a1 - (a1 - a0) * k / n)) * r0) for k in range(n + 1)]
        return pts
    tk = []
    for i in range(21):                                   # 刻度：径向小条
        a, dw = 200 + i * 7, 0.9 if i % 5 else 1.8
        L = 8 if i % 5 else 15
        tk.append(prism(sector(a - dw, a + dw, R - 6 - L, R - 6, 2), 6, "y", (0, Y3 - 6, 0), "刻度"))
    S.append(merge(tk, "刻度"))
    S.append(prism(sector(248, 304, R - 30, R - 20), 6, "y", (0, Y3 - 6, 0), "45~65% 绿区"))

    # 指针 ×2
    for sgn, ang in ((-1, 34), (1, -58)):
        nd = box((46, 4, 8), (0, Y4, -4), "指针")
        S.append(rot(nd, ang, "y", (0, Y4, 0)).moved((sgn * 26, 0, 0)))
        S.append(cyl(8, -7, "y", (sgn * 26, Y4, 0), 12, "针帽"))

    # ⑤ 玻璃表镜 + 黄铜圈
    S.append(cyl(R - 3, 8, "y", (0, Y5 + 46, 0), 30, "玻璃表镜"))
    ring = []
    for i in range(30):
        a0, a1 = i * 2 * math.pi / 30, (i + 1) * 2 * math.pi / 30
        rr0, rr1 = R - 1, R + 9
        q = [(math.cos(a0) * rr0, math.sin(a0) * rr0), (math.cos(a0) * rr1, math.sin(a0) * rr1),
             (math.cos(a1) * rr1, math.sin(a1) * rr1), (math.cos(a1) * rr0, math.sin(a1) * rr0)]
        ring.append(prism(q, 20, "y", (0, Y5, 0), "黄铜圈"))
    S.append(merge(ring, "黄铜圈"))

    # ④ SHT31 探头 ×4（床头 / 墙角 / 柜内 / 风管出口）竖着一串，I²C 总线回表壳
    for i in range(4):
        ax, az_ = 116 + (i % 2) * 86, -158 + (i // 2) * 86
        S.append(box((56, 38, 44), (ax, Y0 - 6, az_), "SHT31 探头"))
        for j in range(3):
            S.append(box((44, 6, 5), (ax + 6, Y0 - 10, az_ + 9 + j * 11), "百叶罩"))
        S.append(cyl(3, -(ax - 62), "x", (ax, Y0 + 12, az_ + 22), 8, "I²C 总线"))
    S.append(box((54, 36, 26), (58, Y0 - 4, -104), "总线接线端"))
    S.append(cyl(3, -64, "z", (62, Y0 + 12, -40), 8, "I²C 总线"))

    items = [("①", "表盘 Φ120，45~65% 绿色舒适区", (math.cos(math.radians(276)) * 40, Y3 - 3, math.sin(math.radians(276)) * 40)),
             ("②", "X27 微型步进表针 ×2", (26, Y2, 17)),
             ("③", "ESP32 + ESPHome，数据同步 HA", (0, Y1 - 2, -6)),
             ("④", "SHT31 探头 ×4，I²C 总线", (230, Y0 - 10, -106)),
             ("⑤", "黄铜圈 + 玻璃表镜", (0, Y5 + 12, R + 4))]
    audit(items, S, -40, 20)
    p = draw("0203-2", "指针温湿度表盘", items, S,
             note="挂在储藏室隔墙外侧、0802 屏旁；四个探头分别在床头、墙角、柜内和风管出口，指针比液晶屏安静也更有工作室气质",
             sig="设想 · 0203", az=-40, el=20, fov=27)
    print("saved", p)


fig1(); fig2()
