"""0503 盆栽 — 三张硬件爆炸图（hand3d 管线）
0503-1 三层松木阶梯花架 / 0503-2 粗陶盆与身份竹签 / 0503-3 陶缸小水景
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from props import wall
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, patch, gravel, tuft, seedling, s_hook)

FW, FD = 1200.0, 900.0        # 花架宽 1.2m、深 0.9m
TZ = (320.0, 620.0, 920.0)    # 三层层面标高，层高差 30cm
TY = (-900.0, -600.0, -300.0)  # 三层前沿 Y，后高前低、每层深 30cm


# --------------------------------------------------------------- 小构件
def water_can(pos, name="浇水壶"):
    """浇水壶：壶身 + 长壶嘴 + 提梁。"""
    x, y, z = pos
    o = [cyl(88, 190, "z", (x, y, z), 16, name),
         cyl(62, 26, "z", (x, y, z + 190), 14, name + "口")]
    o.append(seg_tube((x - 70, y, z + 30), (x - 230, y, z + 210), 16, 7, name + "嘴"))
    o.append(path_tube(arc_pts((x, y, z + 190), 92, 10, 170, 8, "xz"), 9, 5, name + "提梁"))
    return merge([q for q in o if q is not None], name)


def shears(pos, name="剪刀"):
    """剪刀：两片刃 + 两个圆把。"""
    x, y, z = pos
    o = []
    for sgn in (-1, 1):
        bl = box((14, 22, 170), (x - 7 + sgn * 9, y, z), name + "刃")
        o.append(rot(bl, sgn * 7, "y", (x, y + 11, z + 170)))
        o.append(path_tube(arc_pts((x + sgn * 34, y + 11, z - 44), 34, 0, 360, 10, "xz"), 7, 5, name + "把"))
    return merge([q for q in o if q is not None], name)


def clay_pot(pos, rb, rt, h, name="粗陶盆"):
    """无釉粗陶盆：上大下小的圆台 + 口沿。"""
    x, y, z = pos
    return merge([cone(rb, rt, h, (x, y, z), 20, name),
                  cyl(rt * 1.07, 26, "z", (x, y, z + h - 26), 20, name + "口沿")], name)


def cutaway_jar(pos, r, h, t=26, a0=-24.0, a1=204.0, seg=16, name="旧陶缸"):
    """剖开小半边的陶缸：只画 a0→a1 那段缸壁 + 缸底，正面敞开好看内部。"""
    x, y, z = pos
    th = np.radians(np.linspace(a0, a1, seg + 1))
    ro, ri = r, r - t
    F, E = [], []

    def ring(rad, zz):
        return [np.array([x + rad * math.cos(a), y + rad * math.sin(a), zz]) for a in th]
    o0, o1 = ring(ro, z), ring(ro, z + h)
    i0, i1 = ring(ri, z), ring(ri, z + h)
    for k in range(seg):
        F.append([o0[k], o0[k + 1], o1[k + 1], o1[k]])          # 外壁
        F.append([i1[k], i1[k + 1], i0[k + 1], i0[k]])          # 内壁
        F.append([o1[k], o1[k + 1], i1[k + 1], i1[k]])          # 口沿
        E += [(o0[k], o0[k + 1]), (o1[k], o1[k + 1]), (i1[k], i1[k + 1])]
    for k in (0, seg):
        F.append([o0[k], o1[k], i1[k], i0[k]])                  # 剖切端面
        E += [(o0[k], o1[k]), (i0[k], i1[k]), (o1[k], i1[k]), (o0[k], i0[k])]
    base = cyl(ro, t, "z", (x, y, z), 20, name + "底")
    s = Solid(F, E, name)
    return merge([s, base], name)


def fish(pos, L=110, name="黑鱼"):
    """一条小黑鱼：纺锤形身子 + 尾鳍。"""
    x, y, z = pos
    body = merge([cone(4, 22, L * 0.45, (x, y, z), 10, name),
                  cone(22, 5, L * 0.55, (x, y, z + L * 0.45), 10, name)], name)
    body = rot(body, 90, "y", (x, y, z))
    tail = prism([(0, -26), (-40, -42), (-40, 42), (0, 26)], 4, "y", (x - 4, y - 2, z), name + "尾")
    return merge([body, tail], name)


# ---------------------------------------------------------------- 0503-1
def fig1():
    S = []
    S.append(wall(2400, 2300, 140, (-500, 0, 0), "x", "木屋南墙"))
    S.append(merge([box((900, 70, 80), (150, -70, 980), "窗框"),
                    box((900, 70, 80), (150, -70, 1900), "窗框"),
                    box((80, 70, 920), (150, -70, 980), "窗框"),
                    box((80, 70, 920), (970, -70, 980), "窗框")], "窗框"))
    S.append(patch(2600, 2100, (-700, -1600, 0), 60))

    # ② 两侧阶梯形松木侧板（40mm 板，桐油两遍）+ 背面横撑
    step = [(0, 0), (0, 960), (-300, 960), (-300, 660), (-600, 660), (-600, 360), (-900, 360), (-900, 0)]
    for x in (0.0, FW - 40):
        S.append(prism(step, 40, "x", (x, 0, 0), "松木侧板"))
    S.append(box((FW - 80, 40, 90), (40, -40, 840), "横撑"))
    S.append(box((FW - 80, 40, 90), (40, -640, 240), "横撑"))

    # ①③ 三层层板：下两层原位摆盆，最上层整块抬起来露出榫接与排水孔
    UP = (0.0, 0.0, 420.0)
    for k in range(3):
        z = TZ[k] + UP[k]
        S.append(box((FW, 300, 40), (0, TY[k], z), "松木层板"))
        for i2 in range(7):
            S.append(cyl(13, 46, "z", (110 + i2 * 165, TY[k] + 150, z - 3), 8, "排水孔"))
        if UP[k]:
            for x in (-34.0, FW):
                S.append(box((34, 120, 26), (x, TY[k] + 90, z + 7), "榫头"))
    # 最上层的榫眼（露在侧板上）
    for x in (6.0, FW - 34):
        S.append(box((28, 120, 32), (x, TY[2] + 90, TZ[2] + 2), "榫眼"))

    # 下两层的陶盆（原位）
    for k in (0, 1):
        for i2 in range(3):
            px = 230 + i2 * 380
            S.append(clay_pot((px, TY[k] + 150, TZ[k] + 40), 100, 130, 170, "粗陶盆"))
            S.append(seedling((px, TY[k] + 150, TZ[k] + 200), 220, "盆栽"))

    # ④ 侧面挂钩：浇水壶 / 剪刀 / 竹签筒（整组向 +X 前方爆炸）
    HX = FW + 520
    for i2, dz in enumerate((320.0, 640.0, 920.0)):
        S.append(cyl(9, 150, "x", (FW - 40, -250 - i2 * 120, dz), 8, "铸铁挂钩"))
        S.append(box((22, 24, 64), (FW + 104, -262 - i2 * 120, dz - 40), "挂钩头"))
    S.append(water_can((HX + 40, -300, 240), "浇水壶"))
    S.append(shears((HX + 20, -430, 640), "剪刀"))
    S.append(merge([cyl(52, 160, "z", (HX, -560, 880), 14, "竹签筒")] +
                   [cyl(5, 220, "z", (HX - 30 + i2 * 24, -560 + (i2 % 2) * 26, 930), 6, "竹签")
                    for i2 in range(5)], "竹签筒"))

    items = [("①", "三层，宽 1.2m，层高差 30cm", (FW / 2, TY[2] + 300, TZ[2] + UP[2] + 40)),
             ("②", "40mm 松木板，桐油刷两遍", (FW, -180, 820)),
             ("③", "层板钻排水孔，托盘不积水", (770, TY[2] + 150, TZ[2] + UP[2] + 40)),
             ("④", "侧面挂钩：浇水壶 / 剪刀 / 竹签", (HX + 126, -300, 360)),
             ("⑤", "不固定，可整体搬到墙根避风", (FW, -880, 180))]
    audit(items, S, -56, 18)
    print("saved", draw("0503-1", "三层松木阶梯花架", items, S,
                        note="靠在木屋南墙下、南门东侧的窗前，宽 1.2m 深 0.9m 占地 ≈1㎡；后高前低，每一盆都晒得到太阳",
                        sig="设想 · 0503", az=-56, el=18, fov=27))


# ---------------------------------------------------------------- 0503-2
def fig2():
    S = []
    S.append(box((2260, 800, 40), (-560, -400, -40), "层板"))
    for i in range(5):
        S.append(cyl(13, 46, "z", (-420 + i * 320, 0, -43), 8, "排水孔"))

    # ① 三种口径：20 / 28 / 36cm，右边两只原样摆着
    S.append(clay_pot((820, 60, 0), 78, 100, 150, "φ20 粗陶盆"))
    S.append(seedling((820, 60, 150), 230, "薄荷"))
    S.append(clay_pot((1340, -60, 0), 140, 180, 250, "φ36 粗陶盆"))
    S.append(seedling((1340, -60, 250), 330, "绣球"))

    # ② 左边这只 φ28 整只拆开：托盘 → 三只陶脚 → 盆 → 土球 → 竹签
    CX, CY = 60.0, 0.0
    S.append(merge([cyl(170, 34, "z", (CX, CY, -10), 20, "托盘"),
                    cyl(152, 22, "z", (CX, CY, 24), 20, "托盘内底")], "托盘"))
    for i in range(3):
        a = i * 2 * math.pi / 3 + 0.4
        S.append(cyl(22, 40, "z", (CX + math.cos(a) * 92, CY + math.sin(a) * 92, 260), 10, "陶脚"))
    S.append(clay_pot((CX, CY, 500), 110, 140, 210, "φ28 粗陶盆"))
    ball = [cone(72, 118, 96, (CX, CY, 1000), 18, "土球"),
            cone(118, 96, 70, (CX, CY, 1096), 18, "土球"),
            cone(96, 34, 44, (CX, CY, 1166), 18, "土球")]
    for i2 in range(5):
        a = i2 * 1.27
        ball.append(seg_tube((CX + math.cos(a) * 30, CY + math.sin(a) * 30, 1010),
                             (CX + math.cos(a) * 96, CY + math.sin(a) * 96, 960), 6, 5, "根"))
    S.append(merge([q for q in ball if q is not None], "土球"))
    tree = [cyl(19, 360, "z", (CX, CY, 1196), 12, "罗汉松")]
    for i2 in range(6):
        a = i2 * 1.05
        h0 = 1290 + (i2 % 3) * 90
        tree.append(seg_tube((CX, CY, h0), (CX + math.cos(a) * 150, CY + math.sin(a) * 150, h0 + 110), 11, 6, "枝"))
        tree.append(prism([(u * 52, v * 52) for u, v in
                           ((0, -1), (.8, -.2), (1, .6), (0, 1.1), (-1, .6), (-.8, -.2))],
                          6, "z", (CX + math.cos(a) * 190, CY + math.sin(a) * 190, h0 + 120), "叶"))
    S.append(merge([q for q in tree if q is not None], "罗汉松"))

    # ③ 身份竹签：正面烙名字、背面写入院日期（向前爆炸）
    TGX, TGY, TGZ = CX + 40, CY - 470, 700.0
    S.append(box((26, 5, 190), (TGX, TGY, TGZ), "身份竹签"))
    S.append(prism([(0, 0), (13, -22), (26, 0)], 5, "y", (TGX, TGY, TGZ), "竹签尖"))
    for i in range(3):
        S.append(box((17, 2, 4), (TGX + 4, TGY - 2, TGZ + 120 + i * 18), "烙字"))
    # 另外两只盆里各插一根
    for (px, py, pz) in ((820.0, -20.0, 150.0), (1340.0, -150.0, 250.0)):
        S.append(box((26, 5, 190), (px, py, pz), "身份竹签"))

    items = [("①", "无釉粗陶，统一 20 / 28 / 36cm", (1160, -180, 190)),
             ("②", "三只陶脚垫高 2cm，盆底通风", (CX + 92, CY, 280)),
             ("③", "托盘不积水，梅雨季两天就烂根", (CX + 150, CY - 78, 16)),
             ("④", "竹签正面烙名字，背面写入院日期", (TGX + 13, TGY, TGZ + 150)),
             ("⑤", "盆号对应养护记录里的一条植物", (CX + 19, CY, 1330))]
    audit(items, S, -62, 17)
    print("saved", draw("0503-2", "粗陶盆与身份竹签", items, S,
                        note="无釉陶壁会呼吸，多余的水从盆壁蒸发；缺点是干得快，浇水逻辑要盯紧它",
                        sig="设想 · 0503", az=-62, el=17, fov=27))


# ---------------------------------------------------------------- 0503-3
def fig3():
    S = []
    S.append(patch(1550, 1200, (-640, -600, 0), 60))
    S.append(wall(1050, 700, 140, (-380, 380, 0), "x", "木屋南墙"))

    R, H = 300.0, 620.0        # φ60cm 旧陶缸
    JX, JY = 0.0, 0.0
    # ① 缸体：剖开小半边，看得见塘泥、水面和菖蒲
    S.append(cutaway_jar((JX, JY, 0), R, H, 26, 6, 234, 16, "旧陶缸"))
    # ④ 缸沿溢流缺口
    S.append(box((90, 60, 46), (JX + 250, JY - 120, H - 46), "溢流缺口"))

    # ② 缸底 10cm 塘泥
    S.append(cyl(R - 26, 100, "z", (JX, JY, 26), 20, "10cm 塘泥"))
    # ③ 水面：留三分之二空着（水面在 2/3 高处）
    S.append(cyl(R - 30, 10, "z", (JX, JY, H * 0.66), 20, "水面"))
    # 菖蒲一丛（从塘泥里长出来，挑出缸口）
    for i2 in range(7):
        a = i2 * 0.92 + 0.3
        L = 560 + 90 * (i2 % 3)
        bl = prism([(-24, 0), (-15, L * 0.2), (-7, L * 0.9), (0, L),
                    (7, L * 0.9), (15, L * 0.2), (24, 0)], 5, "y", (0, 0, 0), "菖蒲")
        bl = rot(bl, 14 + 9 * (i2 % 3), "y", (0, 0, 0))          # 叶子往外倒
        bl = rot(bl, math.degrees(a), "z", (0, 0, 0))            # 绕一圈散开
        S.append(bl.moved((JX + math.cos(a) * 48, JY + math.sin(a) * 48, 120)))
    # 两条本地黑鱼（挂在剖开的那一侧，看得见）
    S.append(rot(fish((JX - 130, JY - 195, H * 0.52), 175, "黑鱼"), 12, "z", (JX - 130, JY - 195, 0)))
    S.append(rot(fish((JX - 40, JY - 150, H * 0.32), 150, "黑鱼"), -35, "z", (JX - 40, JY - 150, 0)))
    # 水面上的落叶
    S.append(prism([(0, -60), (52, -18), (75, 33), (27, 66), (0, 43), (-27, 66), (-75, 33), (-52, -18)],
                   5, "z", (JX - 120, JY - 90, H * 0.66 + 10), "落叶"))

    # ⑤ 溢流排向花架旁的碎石带
    S.append(box((480, 320, 130), (JX + 340, JY - 300, -130), "碎石带"))
    S.append(gravel((JX + 350, JY - 290, 0), 460, 300, 18, 38, 26, "河卵石"))
    S.append(seg_tube((JX + 300, JY - 90, H - 30), (JX + 430, JY - 110, 30), 10, 6, "溢流水线"))

    # 缸口略高出地面：砖垫
    S.append(box((760, 760, 60), (JX - 380, JY - 380, -60), "砖垫"))

    items = [("①", "旧陶缸 φ60cm，不透光不容易爆藻", (JX - 212, JY - 212, H - 190)),
             ("②", "缸底 10cm 塘泥，种一丛菖蒲", (JX - 215, JY - 95, 96)),
             ("③", "水面留三分之二空着，两条黑鱼", (JX - 45, JY - 190, H * 0.52 + 24)),
             ("④", "缸沿留溢流缺口，排向碎石带", (JX + 285, JY - 120, H - 24)),
             ("⑤", "冬天结薄冰无妨，菖蒲地下茎越冬", (JX + 46, JY - 239, 434))]
    audit(items, S, -60, 20)
    print("saved", draw("0503-3", "陶缸小水景", items, S,
                        note="放在阶梯花架东侧靠墙；两条本地黑鱼吃孑孓，一个夏天不用管，落叶漂着就让它漂着",
                        sig="设想 · 0503", az=-60, el=25, fov=27))


if __name__ == "__main__":
    w = sys.argv[1:] or ["1", "2", "3"]
    if "1" in w: fig1()
    if "2" in w: fig2()
    if "3" in w: fig3()
