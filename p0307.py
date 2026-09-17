"""0307 自建三轴龙门 CNC — 两张硬件爆炸图
0307-1 龙门机架与两条刚性路线 / 0307-2 主轴与变频选型（待定）
三轴龙门：底座矩形框 + 双立柱托横梁；龙门在 Y 向导轨走、主轴滑块在横梁 X 走、Z 轴挂滑块。
没有分度头、没有第四第五轴。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl, extrusion
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, label, audit)

BW, BD = 1000.0, 800.0          # 机器占地约 1.0×0.8m
BH = 1200.0                     # 整机高 1.2m


def hgr(pos, L, axis="y", name="HGR15 导轨", blocks=(0.25, 0.65)):
    """HGR15 导轨 + 两个滑块。"""
    x, y, z = pos
    o = [box((15, L, 15), (x, y, z), name) if axis == "y" else box((L, 15, 15), (x, y, z), name)]
    for t in blocks:
        if axis == "y":
            o.append(box((34, 55, 26), (x - 9.5, y + L * t, z + 15), name + "滑块"))
        else:
            o.append(box((55, 34, 26), (x + L * t, y - 9.5, z + 15), name + "滑块"))
    return o


def ballscrew(pos, L, axis="y", name="1605 滚珠丝杠"):
    x, y, z = pos
    o = [cyl(8, L, axis, pos, 12, name)]
    nx = {"y": (x, y + L * 0.45, z), "x": (x + L * 0.45, y, z)}[axis]
    o.append(box((44, 60, 44), (nx[0] - 22, nx[1] - 30, nx[2] - 22), "丝杠螺母"))
    return o


def stepper(pos, s=60.0, L=90.0, axis="y", name="闭环 42 步进"):
    x, y, z = pos
    size = {"x": (L, s, s), "y": (s, L, s), "z": (s, s, L)}[axis]
    o = [box(size, (x, y, z), name)]
    enc = {"x": (26, s, s), "y": (s, 26, s), "z": (s, s, 26)}[axis]
    off = {"x": (x + L, y, z), "y": (x, y + L, z), "z": (x, y, z + L)}[axis]
    o.append(box(enc, off, "编码器"))
    return o


# ---------------------------------------------------------------- 0307-1
def fig1():
    S = []
    S.append(floor(3000, 1700, (-1100, -540, 0)))

    # ① 底座矩形框（3030）+ 两侧立柱 + 横梁 —— 龙门式骨架
    P = 30.0
    for z in (0.0, 120.0):
        S.append(extrusion(BW, "x", (0, 0, z), P, "底座框"))
        S.append(extrusion(BW, "x", (0, BD - P, z), P, "底座框"))
        S.append(extrusion(BD - 2 * P, "y", (0, P, z), P, "底座框"))
        S.append(extrusion(BD - 2 * P, "y", (BW - P, P, z), P, "底座框"))
    for dx in (0.0, BW - P):
        for dy in (0.0, BD - P):
            S.append(extrusion(120, "z", (dx, dy, 0), P, "底座立角"))
    # ② Y 向 HGR15 导轨 + 1605 丝杠（龙门前后走）
    for dx in (60.0, BW - 100):
        S += hgr((dx, 40, 150), BD - 80, "y")
    S += ballscrew((BW / 2 - 4, 40, 165), BD - 80, "y")
    S += stepper((BW / 2 - 34, BD - 40, 135), 60, 90, "y")
    # 台面板
    S.append(box((BW - 160, BD - 120, 24), (80, 60, 430), "台面板"))

    # 龙门：双立柱 + 横梁（整体沿 +Z 爆炸抬起）
    GZ = 760.0
    for dx in (40.0, BW - 100):
        S.append(extrusion(560, "z", (dx, BD / 2 - 30, GZ), 60, "龙门立柱"))
        S.append(box((140, 160, 26), (dx - 40, BD / 2 - 50, GZ - 26), "立柱底板"))
    S.append(extrusion(BW - 80, "x", (40, BD / 2 - 30, GZ + 560), 60, "龙门横梁"))
    # ③ 横梁上的 X 导轨 + 滑块 + Z 轴（再往上爆炸）
    ZZ = GZ + 780
    S += hgr((60, BD / 2 - 8, ZZ), BW - 120, "x")
    S += ballscrew((60, BD / 2 + 44, ZZ + 26), BW - 120, "x")
    S += stepper((BW - 80, BD / 2 + 14, ZZ + 4), 60, 90, "x")
    ZX = BW * 0.46
    S.append(box((200, 30, 300), (ZX, BD / 2 + 70, ZZ + 60), "Z 轴滑板"))
    S += hgr((ZX + 30, BD / 2 + 100, ZZ + 60), 280, "x", blocks=(0.1,))
    S += stepper((ZX + 70, BD / 2 + 80, ZZ + 360), 60, 90, "z")
    S.append(box((150, 120, 120), (ZX + 25, BD / 2 + 100, ZZ + 110), "主轴夹座"))
    S.append(cyl(46, 220, "z", (ZX + 100, BD / 2 + 160, ZZ - 60), 18, "主轴（借用）"))

    # ④ 木 / 亚克力路线的截面样段（爆炸到 -X 外）
    AX = -760.0
    S.append(extrusion(420, "y", (AX, 80, 60), 20, "2020 样段"))
    S.append(extrusion(420, "y", (AX + 120, 80, 60), 30, "3030 样段"))
    S.append(box((260, 40, 40), (AX - 20, 520, 60), "角码"))
    S.append(box((70, 70, 26), (AX + 130, 520, 100), "内置角槽件"))
    # ⑤ 铝路线的截面样段 + 钢板加强底座（爆炸到 +X 外）
    BX = BW + 420.0
    S.append(extrusion(420, "y", (BX, 80, 130), 40, "4040 样段"))
    S.append(extrusion(420, "y", (BX + 120, 80, 130), 40, "4040 样段"))
    S.append(box((360, 480, 26), (BX - 20, 60, 60), "钢板加强底座"))
    for dx in (20.0, 300.0):
        for dy in (100.0, 480.0):
            S.append(cyl(9, 40, "z", (BX - 20 + dx, dy, 86), 10, "沉头螺栓"))

    items = [("①", "龙门式骨架：底座框 + 双立柱 + 横梁", (BW - 70, BD / 2, GZ + 300)),
             ("②", "Y 向 HGR15 + 1605 丝杠，龙门前后走", (BW - 100 + 7, 40 + (BD - 80) * 0.75, 158)),
             ("③", "横梁 X 滑块挂 Z 轴，闭环 42 步进 ×3", (ZX + 100, BD / 2 + 70, ZZ + 210)),
             ("④", "木 / 亚克力：2020+3030，行程 300×300×100", (AX + 135, 300, 90)),
             ("⑤", "铝：全 4040 + 钢板底座，行程 200×200×80", (BX + 20, 300, 170))]
    audit(items, S, -58, 20)
    print("saved", draw("0307-1", "龙门机架与两条刚性路线", items, S,
                        note="主切材料没拍板之前，截面和导轨规格都不定标；角部内置角槽件加角码双重锁定，整机目标 ≤60kg",
                        sig="设想 · 0307", az=-58, el=20, fov=27))


# ---------------------------------------------------------------- 0307-2
def fig2():
    S = []
    # 共用接口：Z 轴滑板 + 80mm 夹环（两条路线都接到这里）
    MZ = 700.0
    S.append(box((240, 34, 420), (-120, 60, MZ), "Z 轴滑板"))
    S.append(box((230, 150, 40), (-115, -90, MZ + 320), "夹环座"))
    S.append(box((230, 150, 40), (-115, -90, MZ + 90), "夹环座"))
    for zz in (MZ + 90, MZ + 320):
        S.append(path_tube([(-80, -60, zz + 20), (-80, -60, zz + 20)], 1, 4, "x"))
        S.append(cyl(52, 40, "z", (0, -14, zz), 20, "80mm 夹环"))
        S.append(cyl(40, 44, "z", (0, -14, zz - 2), 20, "夹环内孔"))

    # ---- A 路线（木 / 亚克力）：500W 风冷主轴 + ER11，爆炸到 -X
    AX = -820.0
    S.append(cyl(40, 300, "z", (AX, -14, MZ + 60), 20, "500W 风冷主轴"))
    for i in range(7):
        S.append(cyl(50, 10, "z", (AX, -14, MZ + 90 + i * 30), 20, "散热鳍"))
    S.append(cyl(28, 70, "z", (AX, -14, MZ + 360), 16, "风冷罩"))
    S.append(cone(34, 17, 60, (AX, -14, MZ), 16, "ER11 夹头"))
    S.append(cyl(3.2, 70, "z", (AX, -14, MZ - 70), 10, "铣刀"))
    S.append(box((160, 120, 210), (AX - 80, -260, MZ - 470), "A 路线控制盒"))
    S.append(box((110, 16, 70), (AX - 55, -276, MZ - 400), "调速面板"))
    S.append(path_tube([(AX, -14, MZ + 60), (AX, -140, MZ - 180), (AX, -200, MZ - 260)], 11, 6, "主轴线"))

    # ---- B 路线（铝）：1.5kW 水冷主轴 + VFD + 水箱，爆炸到 +X
    BX = 880.0
    S.append(cyl(50, 400, "z", (BX, -14, MZ + 40), 20, "1.5kW 水冷主轴"))
    S.append(cyl(54, 26, "z", (BX, -14, MZ + 430), 20, "水冷主轴尾盖"))
    for dz in (MZ + 90, MZ + 370):
        S.append(cyl(11, 90, "y", (BX - 50, -14, dz), 12, "水嘴"))
    S.append(cone(44, 22, 76, (BX, -14, MZ - 36), 16, "ER20 夹头"))
    S.append(cyl(5, 80, "z", (BX, -14, MZ - 116), 10, "铣刀"))
    # VFD 变频器
    VX, VZ = BX + 420, MZ - 120
    S.append(box((200, 330, 480), (VX, -180, VZ), "VFD 变频器"))
    S.append(box((130, 16, 90), (VX + 35, -196, VZ + 330), "VFD 显示"))
    S.append(cyl(30, 26, "z", (VX + 100, -120, VZ + 480), 14, "调速旋钮"))
    for i in range(6):
        S.append(box((150, 12, 10), (VX + 25, -186, VZ + 60 + i * 30), "散热栅"))
    S.append(path_tube([(BX, -14, MZ + 440), (VX + 60, -60, VZ + 480)], 12, 6, "主轴动力线"))
    S.append(path_tube([(VX + 20, -60, VZ + 120), (VX - 260, -300, VZ - 40)], 8, 6, "RS485 线"))
    # 水箱 + 进出水管
    WX, WY = BX + 40, -700.0
    S.append(box((420, 300, 260), (WX, WY, 0), "水箱"))
    S.append(box((300, 16, 120), (WX + 60, WY - 16, 70), "水位窗"))
    S.append(cyl(60, 130, "z", (WX + 340, WY + 150, 260), 16, "水泵"))
    for i, dz in enumerate((MZ + 90, MZ + 370)):
        S.append(path_tube([(BX - 50, -104, dz), (BX - 150, -320, 420 + i * 110),
                            (WX + 90 + i * 200, WY + 150, 260)], 13, 6, "冷却水管"))

    items = [("①", "Z 轴滑板 + 80mm 夹环：两路共用接口", (0, -66, MZ + 340)),
             ("②", "木 / 亚克力：500W 风冷 + ER11", (AX, -64, MZ + 210)),
             ("③", "铝：1.5kW 水冷主轴 + ER20", (BX, -64, MZ + 240)),
             ("④", "VFD 走 RS485 / Modbus 调速，不用旋钮", (VX + 100, -196, VZ + 375)),
             ("⑤", "水箱 + 进出水管，只有水冷路线要", (WX + 210, WY - 16, 130))]
    audit(items, S, -62, 18)
    print("saved", draw("0307-2", "主轴与变频选型（待定）", items, S,
                        note="主材未定前只租借试切、不采购主轴与变频器；两条路线的 VFD 型号、线径、电流保护都不一样",
                        sig="设想 · 0307", az=-62, el=18, fov=27))


fig1()
fig2()
