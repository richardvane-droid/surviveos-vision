"""0801 物品数字孪生 — 两张硬件爆炸图（hand3d 管线）
0801-1 二维码收纳箱系统 / 0801-2 扫码入库站

硬件都在地堡东侧储藏室：货架靠墙，箱子开口朝 -Y（相机一侧）。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from props import wall
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, capped_cyl, disc)

_QR = np.random.default_rng(801)


def qr_label(pos, w=70, h=70, n=7, t=2.0, name="二维码"):
    """朝 -Y 的合成纸二维码标签：底板 + 一格格凸起的码点（含三个定位角）。"""
    x, y, z = pos
    o = [box((w + 12, 1.6, h + 12), (x - 6, y, z - 6), name)]
    m = _QR.integers(0, 2, (n, n))
    for i in range(n):
        for j in range(n):
            a, b = i < 3, j >= n - 3
            c, d = i < 3, j < 3
            if (a and b) or (c and d) or (i >= n - 3 and j < 3):
                on = (i % 3 != 1) or (j % 3 != 1) if False else 1
            else:
                on = m[i, j]
            if on:
                o.append(box((w / n * 0.86, t, h / n * 0.86), (x + i * w / n, y - t, z + j * h / n), name))
    return merge(o, name)


def pp_box(pos, lid=None, name="透明 PP 箱 40×30×24"):
    """透明 PP 箱 400×300×240：四壁 + 底 + 两侧提手凹口。"""
    x, y, z = pos
    t = 8.0
    o = [box((400, t, 240), (x, y, z), name), box((400, t, 240), (x, y + 300 - t, z), name),
         box((t, 300, 240), (x, y, z), name), box((t, 300, 240), (x + 400 - t, y, z), name),
         box((400, 300, t), (x, y, z), name + "底"),
         box((416, 316, 14), (x - 8, y - 8, z + 236), name + "口沿")]
    return merge(o, name)


# ---------------------------------------------------------------- 0801-1
def fig1():
    S = []
    w = wall(1500, 1280, 60, (-160, 380, 0)); S.append(w)

    # 货架（4 根立柱 + 3 层层板），格位就是"四级地址"里的第二级
    for dx, dy in ((0, 0), (1080, 0), (0, 320), (1080, 320)):
        S.append(box((40, 40, 1180), (dx, dy, 0), "货架立柱"))
    for z in (30.0, 600.0, 1150.0):
        S.append(box((1120, 360, 26), (0, 0, z), "货架层板"))
    # ④ 格位位置码
    for x in (150.0, 720.0):
        for z in (40.0, 610.0):
            S.append(qr_label((x, -4, z + 34), 56, 56, 5, 2, "格位位置码"))
            S.append(box((150, 3, 26), (x - 40, -3, z + 4), "格位手写标签"))

    # ① 透明 PP 箱：下层两只到位，上层一只到位、一只拉出来
    S.append(pp_box((60, 20, 56)))
    S.append(pp_box((620, 20, 56)))
    S.append(pp_box((60, 20, 626)))
    BX, BY, BZ = 1460.0, -440.0, 180.0
    S.append(pp_box((BX, BY, BZ)))
    # ② 箱侧二维码 + 手写标签
    S.append(qr_label((BX + 70, BY - 2, BZ + 70), 90, 90, 7, 2.4, "合成纸热敏二维码"))
    S.append(box((190, 3, 40), (BX + 190, BY - 3, BZ + 96), "手写标签"))

    # ⑤ 箱内物品按层记录：三层薄托盘沿 +Z 拉开
    for k in range(3):
        zz = BZ + 330 + k * 250
        S.append(box((376, 276, 12), (BX + 12, BY + 12, zz), "层 %d" % (k + 1)))
        for i in range(3):
            S.append(box((90, 70, 54), (BX + 30 + i * 118, BY + 40 + (i % 2) * 110, zz + 12), "箱内物品"))
    S.append(box((416, 316, 16), (BX - 8, BY - 8, BZ + 1140), "箱盖"))

    items = [("①", "透明 PP 箱 40×30×24cm，全屋一款", (BX + 330, BY, BZ + 200)),
             ("②", "合成纸热敏二维码，防水不掉色", (BX + 115, BY - 4, BZ + 115)),
             ("③", "四级地址：区域 → 格位 → 箱 → 层", (BX + 200, BY + 150, BZ + 1156)),
             ("④", "货架格位贴位置码，挪箱重扫即可", (178, -4, 62)),
             ("⑤", "箱内物品按层记录，扫码不用开箱", (BX + 75, BY + 150, BZ + 616))]
    slots = [("①", "", (1134, 760)), ("②", "", (1134, 590)), ("③", "", (1134, 250)),
             ("④", "", (66, 520)), ("⑤", "", (1134, 420))]
    audit(items, S, -62, 20)
    print("saved", draw("0801-1", "二维码收纳箱系统", items, S, slots=slots,
                        note="全屋统一一款 40×30×24cm 透明 PP 箱，二维码只编码箱号；箱里换了东西不换标签，改的是数据库",
                        sig="设想 · 0801", az=-62, el=20, fov=27))


# ---------------------------------------------------------------- 0801-2
def fig2():
    S = []
    S.append(wall(1240, 1320, 70, (-230, 60, 280)))

    # ⑤ 铝合金壁挂框 + 墙挂底板（走线藏在底板后）
    BPY = -120.0
    S.append(box((760, 22, 880), (0, BPY, 620), "墙挂底板"))
    for x in (-20.0, 740.0):
        S.append(extrusion(920, "z", (x, BPY - 40, 600), 40, "铝合金壁挂框"))
    for z in (600.0, 1500.0):
        S.append(extrusion(800, "x", (-20, BPY - 40, z), 40, "铝合金壁挂框"))
    S.append(box((700, 6, 40), (20, BPY - 6, 630), "暗藏线槽"))

    # ① 12.9 寸平板壁挂，常亮显示等距地图（沿 -Y 拉出）
    TY = BPY - 420
    S.append(box((580, 26, 440), (90, TY, 880), "12.9 寸平板"))
    S.append(box((540, 6, 400), (110, TY - 6, 900), "等距地图界面"))
    for u, v in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (1, 2)):
        S.append(box((62, 4, 40), (348 + (u - v) * 92 - 31, TY - 10, 960 + (u + v) * 56), "区域图标"))

    # ② N100 小主机（藏在隔墙背后的储藏室里，沿 +Y 拉到墙后）
    NY = 260.0
    S.append(box((230, 230, 60), (1090, NY, 780), "N100 小主机"))
    S.append(box((120, 8, 22), (1130, NY - 8, 810), "前面板"))
    for i in range(4):
        S.append(cyl(9, 26, "y", (1130 + i * 34, NY + 230, 806), 8, "网口/USB"))
    S.append(box((280, 260, 16), (1065, NY - 16, 720), "隔墙背后浅搁板"))

    # ③ 蓝牙扫码枪 + 挂座（从挂座里往 -Y 下方拉出）
    GY = BPY - 560
    gun = [box((70, 210, 60), (330, GY, 490), "蓝牙扫码枪"),
           box((66, 70, 130), (332, GY + 130, 380), "枪柄"),
           box((46, 12, 40), (342, GY - 12, 500), "扫码窗"),
           box((26, 30, 20), (352, GY + 120, 470), "扳机")]
    S.append(merge(gun, "蓝牙扫码枪"))
    S.append(box((130, 120, 90), (300, BPY - 120, 440), "扫码枪挂座"))
    S.append(box((130, 16, 150), (300, BPY - 16, 410), "挂座背板"))

    # ④ 热敏标签机 + 合成纸标签卷
    PY = BPY - 300
    S.append(box((230, 190, 150), (560, PY, 430), "热敏标签机"))
    S.append(capped_cyl(58, 150, "x", (580, PY + 90, 560), 16, "合成纸标签卷"))
    S.append(box((160, 8, 40), (590, PY - 8, 470), "出纸口"))
    S.append(box((150, 3, 36), (600, PY - 30, 452), "即打即贴标签"))
    S.append(box((280, 220, 20), (540, BPY - 220, 400), "壁挂小搁板"))

    items = [("①", "12.9 寸平板壁挂，常亮等距地图", (380, TY - 6, 1180)),
             ("②", "N100 小主机跑 Homebox + HA", (1205, NY - 8, 810)),
             ("③", "蓝牙扫码枪 + 挂座，30cm 内扫码", (365, GY - 12, 520)),
             ("④", "热敏标签机用合成纸卷，即打即贴", (675, PY - 8, 490)),
             ("⑤", "铝合金壁挂框，走线藏在底板后", (0, BPY - 40, 1460))]
    audit(items, S, -68, 14)
    print("saved", draw("0801-2", "扫码入库站", items, S,
                        note="挂在地堡储藏室门边隔墙上，紧邻 0802 屏墙南端；主机藏在隔墙背后，整站只需一路电源",
                        sig="设想 · 0801", az=-68, el=14, fov=27))


if __name__ == "__main__":
    fig1(); fig2()
