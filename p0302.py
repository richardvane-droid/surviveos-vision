"""0302 装备墙与整备区 — 两张硬件爆炸图
0302-1 斜墙松木挂板墙 / 0302-2 睡袋格子柜与整备区
阁楼西侧低矮带：45° 坡顶朝 +Y 下坡，檐口在 y=EAVE，站立带在 -Y（相机侧）。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, s_hook,
                     gable, label, audit, ROOF)

EAVE = 1600.0          # 檐口（屋面落到 z=0）的 y 坐标
R2 = math.sqrt(2) / 2


def toroof(s):
    """局部 (u 沿檐口, v 沿坡面向上, w 沿坡面内法线) → 世界坐标。"""
    return mv(rot(s, 135, "x", (0, 0, 0)), (0, EAVE, 0))


def P(u, v, w):
    """局部点 → 世界点。"""
    return (u, EAVE - R2 * (v + w), R2 * (v - w))


def pack(pos, w, d, h, name="登山包"):
    """登山包：包体 + 圆顶盖 + 前袋 + 两条肩带 + 提环。"""
    x, y, z = pos
    o = [box((w, d, h * 0.80), (x - w / 2, y - d / 2, z), name),
         cyl(d * 0.5, w, "x", (x - w / 2, y, z + h * 0.80), 14, name + "顶盖"),
         box((w * 0.60, d * 0.42, h * 0.34), (x - w * 0.30, y - d * 0.92, z + h * 0.14), name + "前袋")]
    for s in (-1, 1):
        o.append(box((w * 0.18, d * 0.26, h * 0.46), (x + s * w * 0.24 - w * 0.09, y + d * 0.34, z + h * 0.3), "肩带"))
    o.append(path_tube([(x, y + d * 0.1, z + h * 0.80 + d * 0.45),
                        (x, y + d * 0.1, z + h * 0.80 + d * 0.45 + 70)], 7, 6, "提环"))
    return [merge(o, name)]


# ---------------------------------------------------------------- 0302-1
def fig1():
    S = []
    S.append(floor(3500, 1900, (-250, -800, 0)))
    S.append(gable((-420, EAVE - ROOF, 0), ROOF, 60, False, "45° 斜顶"))

    UW = 3000.0
    # ② 龙骨：三根，打进屋架，留在坡面里
    rafters = []
    for u in (200.0, 1350.0, 2600.0):
        rafters.append(box((90, 2500, 100), (u, 140, -100), "龙骨"))
    S += toroof(rafters)

    # ① 松木条 60×20，缝 30 → 坡面上 90 一格，整排沿内法线爆炸出来
    WE = 340.0                                   # 爆炸量（沿坡面内法线）
    slats = []
    for k in range(25):
        v = 200 + k * 90.0
        slats.append(box((UW, 60, 20), (0, v, WE), "松木条 60×20"))
    S += toroof(slats)

    # ③ S 钩（挂在爆炸后的条上）+ ④ 三只登山包
    HW, HR = WE + 34, 46.0
    packs = {}
    for u, (pw, pd, ph) in ((430, (300, 200, 460)), (1050, (340, 240, 580)), (1740, (380, 280, 720))):
        hx, hy, hz = P(u, 2010, HW)
        S.append(s_hook((hx, hy, hz), HR, 8, "S 钩"))
        zb = hz - 3 * HR - ph
        S += pack((hx + 2 * HR, hy - 190, zb), pw, pd, ph)
        packs[u] = (hx + 2 * HR, hy - 190 - pd * 0.75, zb + ph * 0.34)
    HOOK3 = P(1740, 2010, HW)
    # ⑤ 下排：登山杖 + 水袋
    px, py, pz = P(2340, 1720, HW)
    S.append(s_hook((px, py, pz), HR, 8, "S 钩"))
    for dx in (-30.0, 14.0):
        S.append(cyl(12, 640, "z", (px + 2 * HR + dx, py - 150, pz - 3 * HR - 640), 10, "登山杖"))
        S.append(cyl(17, 110, "z", (px + 2 * HR + dx, py - 150, pz - 3 * HR - 750), 10, "杖握把"))
    bx, by, bz = P(2740, 1720, HW)
    S.append(s_hook((bx, by, bz), HR, 8, "S 钩"))
    S.append(box((250, 74, 420), (bx + 2 * HR - 125, by - 190, bz - 3 * HR - 420), "水袋"))
    S.append(path_tube([(bx + 2 * HR, by - 190, bz - 3 * HR - 400),
                        (bx + 2 * HR + 160, by - 260, bz - 3 * HR - 560),
                        (bx + 2 * HR + 120, by - 280, bz - 3 * HR - 700)], 10, 6, "水袋吸管"))

    items = [("①", "松木条 60×20，间距 30mm", P(760, 2300, WE + 20)),
             ("②", "龙骨打进屋架，整面可拆不留洞", P(1395, 2480, -50)),
             ("③", "大号不锈钢 S 钩，单钩 ≥10kg", (HOOK3[0] + 3 * HR, HOOK3[1], HOOK3[2] - 2 * HR)),
             ("④", "三只登山包 20 / 38 / 65L 由小到大", packs[1740]),
             ("⑤", "登山杖与水袋挂下排", (px + 2 * HR - 30, py - 150, pz - 3 * HR - 300))]
    audit(items, S, -56, 10)
    print("saved", draw("0302-1", "斜墙松木挂板墙", items, S,
                        note="阁楼西侧低矮带的 45° 斜顶面：受力顺龙骨传到屋架；松木透气，潮气未干的背包挂上去也不闷",
                        sig="设想 · 0302", az=-56, el=10, fov=27))


# ---------------------------------------------------------------- 0302-2
def fig2():
    S = []
    T = 22.0
    CW = CH = 300.0                       # 格子 30×30cm
    CD = 400.0                            # 进深 40cm
    NX = 6
    W = NX * CW + (NX + 1) * T
    Y0 = 250.0                            # 柜体前沿（后面就是檐口最矮处）
    S.append(floor(3000, 2600, (-500, -1300, 0)))
    S.append(gable((-420, 1750 - ROOF, 0), ROOF, 60, False, "45° 斜顶"))

    # 柜体：底排斜格 + 上两排正格
    ZS = 300.0                            # 斜格顶面
    body = [box((W, CD, T), (0, Y0, ZS)), box((W, CD, T), (0, Y0, ZS + CH + T)),
            box((W, CD, T), (0, Y0, ZS + 2 * (CH + T))), box((W, T, ZS + 2 * (CH + T) + T), (0, Y0 + CD - T, 0))]
    for i in range(NX + 1):
        x = i * (CW + T)
        body.append(box((T, CD, 2 * (CH + T) + T), (x, Y0, ZS)))
        body.append(box((T, CD, ZS), (x, Y0, 0)))
    S.append(merge(body, "木格子柜"))
    # 底排斜格隔板（鞋头朝外）
    for i in range(NX):
        x = T + i * (CW + T)
        sl = box((CW, CD, 14), (x, Y0, 60))
        S.append(rot(sl, -16, "x", (x + CW / 2, Y0 + CD / 2, 70)))

    # ① 睡袋 / 防潮垫松卷立放：从上排格子里爆炸抬起
    for i in range(NX):
        x = T + i * (CW + T) + CW / 2
        for r, (zc, lift) in enumerate(((ZS + T, 520.0), (ZS + CH + 2 * T, 700.0))):
            rr = 132 if (i + r) % 2 == 0 else 118
            S.append(cyl(rr, 360, "z", (x, Y0 + CD / 2, zc + lift), 18, "睡袋松卷" if r else "防潮垫卷"))
            S.append(cyl(rr * 0.35, 366, "z", (x, Y0 + CD / 2, zc + lift - 3), 12, "卷芯"))
    # 每格标签
    for i in range(NX):
        S.append(label((T + i * (CW + T) + 100, Y0 - 4, ZS + CH - 60), 90, 34, 4, "标签"))
        S.append(label((T + i * (CW + T) + 100, Y0 - 4, ZS + 2 * CH - 20), 90, 34, 4, "标签"))

    # ③ 底排登山鞋（斜格里往外爆炸）+ 烘鞋器
    for i in (1, 2, 4):
        x = T + i * (CW + T) + CW / 2
        for s in (-70, 70):
            S.append(box((110, 250, 90), (x + s - 55, Y0 - 420, 120), "登山鞋"))
            S.append(cone(54, 30, 70, (x + s, Y0 - 470, 122), 14, "鞋头"))
    DX = T + 5 * (CW + T) + CW / 2
    S.append(box((220, 200, 150), (DX - 110, Y0 - 430, 40), "烘鞋器"))
    for s in (-55, 55):
        S.append(cyl(32, 260, "z", (DX + s, Y0 - 330, 190), 14, "烘鞋管"))

    # ④ 1 米宽整备地垫
    S.append(box((W + 200, 1000, 26), (-100, Y0 - 1480, 0), "整备地垫"))

    items = [("①", "格子 30×30×40cm，每格贴标签", (T + 2 * (CW + T) + 150, Y0 + 20, ZS + CH + 120)),
             ("②", "睡袋松卷立放，不压缩保蓬松", (T + 3 * (CW + T) + CW / 2, Y0 + CD / 2, ZS + CH + 2 * T + 880)),
             ("③", "底排斜格放鞋，鞋头朝外", (T + 2 * (CW + T) + CW / 2, Y0 - 330, 165)),
             ("④", "旁边共用一台小烘鞋器", (DX, Y0 - 330, 120)),
             ("⑤", "1 米宽整备地垫，先晾干再上墙", (W / 2, Y0 - 980, 26))]
    audit(items, S, -66, 22)
    print("saved", draw("0302-2", "睡袋格子柜与整备区", items, S,
                        note="阁楼西侧檐口最矮处一排；柜前留 1 米宽地垫做整备区，每样东西只有一个家，格满即停",
                        sig="设想 · 0302", az=-66, el=22, fov=27))


fig1()
fig2()
