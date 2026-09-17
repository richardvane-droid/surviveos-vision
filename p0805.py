"""0805 全套方案材质总设计 — 两张硬件爆炸图（hand3d 管线）
0805-1 欧标 2020 型材配件套 / 0805-2 三材分层样板

D3 已定标：欧标体系、主力 2020（槽宽 6mm、M5 T 型螺母）、重载 3030/4040（槽宽 8mm，配件不通用）、
表面统一喷砂黑阳极氧化、壁厚默认 1.8mm。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, capped_cyl, disc)


def hexbolt(pos, r=2.5, L=26, hr=4.6, hh=5.0, name="M5 内六角螺栓"):
    """M5 内六角螺栓：杆 + 六角柱头（沿 -Z 拧下去，pos 是头的底面圆心）。"""
    x, y, z = pos
    o = [cyl(r, -L, "z", (x, y, z), 12, name), disc(r, (x, y, z - L), "z", 12, name),
         cyl(hr, hh, "z", (x, y, z), 6, name + "头"),
         disc(hr, (x, y, z + hh), "z", 6, name + "头"),
         cyl(2.0, 2.4, "z", (x, y, z + hh - 2.4), 6, name + "内六角孔")]
    return merge(o, name)


def tnut(pos, name="M5 T 型螺母"):
    """T 型螺母：槽内的 T 形块 + 中间螺孔。"""
    x, y, z = pos
    return merge([box((11.5, 6.4, 3.2), (x - 5.75, y - 3.2, z), name),
                  box((7.5, 6.4, 4.0), (x - 3.75, y - 3.2, z + 3.2), name),
                  cyl(2.6, 8, "z", (x, y, z), 10, name + "螺孔")], name)


def slider_nut(pos, name="滑块螺母"):
    x, y, z = pos
    return merge([box((16, 6.2, 5.0), (x - 8, y - 3.1, z), name),
                  cyl(2.6, 6, "z", (x, y, z), 10, name + "螺孔"),
                  cyl(1.6, 4, "z", (x - 5.5, y, z + 5), 8, name + "弹珠")], name)


def lbracket(pos, s=20.0, t=3.0, name="L 角码"):
    x, y, z = pos
    o = [box((s, s, t), (x, y, z), name), box((t, s, s), (x, y, z), name)]
    for c in ((s * 0.6, s * 0.5), ):
        o.append(cyl(2.6, t + 2, "z", (x + c[0], y + c[1], z - 1), 10, name + "孔"))
    o.append(cyl(2.6, t + 2, "x", (x - 1, y + s * 0.5, z + s * 0.6), 10, name + "孔"))
    return merge(o, name)


def hidden_corner(pos, name="内置角槽件"):
    """内置角槽件：藏在槽里的两段方块 + 一颗顶丝，外面看不到金属件。"""
    x, y, z = pos
    return merge([box((26, 6.0, 5.6), (x, y - 3, z), name),
                  box((5.6, 6.0, 26), (x + 20.4, y - 3, z), name),
                  cyl(2.2, 10, "x", (x + 4, y, z + 2.8), 8, name + "顶丝")], name)


def shelf_bracket(pos, name="层板托"):
    x, y, z = pos
    return merge([box((4, 22, 26), (x, y, z), name),
                  box((34, 22, 4), (x + 4, y, z), name),
                  box((34, 4, 8), (x + 4, y + 18, z + 4), name + "挡边"),
                  cyl(2.6, 6, "x", (x - 1, y + 11, z + 18), 8, name + "孔")], name)


# ---------------------------------------------------------------- 0805-1
def fig1():
    S = []
    # ① 主角：一段欧标 2020 喷砂黑型材，槽宽 6mm、壁厚 1.8mm
    S.append(extrusion(300, "x", (0, 0, 0), 20, "欧标 2020 喷砂黑型材"))
    S.append(box((300, 6, 2.4), (0, 7, 18.6), "6mm 槽口"))
    S.append(box((300, 2.4, 6), (0, 18.6, 7), "6mm 槽口"))

    # ② M5 T 型螺母 / 滑块螺母 + M5 内六角（沿 +Z 拆开，落进顶面的槽）
    S.append(tnut((52, 10, 32)))
    S.append(hexbolt((52, 10, 62)))
    S.append(slider_nut((92, 10, 32)))
    S.append(hexbolt((92, 10, 66)))

    # ③ L 角码（外露）与内置角槽件（隐藏）
    S.append(lbracket((140, 0, 44)))
    S.append(hexbolt((150, 10, 86)))
    S.append(hidden_corner((196, 10, 44)))
    S.append(box((26, 6, 5.6), (196, 7, 6), "槽内就位示意"))

    # ④ 端盖（沿 -X 拆开）与层板托
    S.append(box((20, 20, 2.6), (-42, 0, 0), "20×20 端盖"))
    for dx, dy in ((5, 5), (15, 15)):
        S.append(cyl(2.2, 6, "x", (-44, dx, dy), 8, "端盖卡脚"))
    S.append(shelf_bracket((252, 22, 26)))
    S.append(hexbolt((260, 30, 80)))

    # ⑤ 3030 / 4040 是另一套 8mm 槽的配件，必须分箱
    S.append(extrusion(210, "x", (0, 96, 0), 30, "欧标 3030 型材"))
    S.append(box((210, 8, 2.4), (0, 107, 28.6), "8mm 槽口"))
    S.append(extrusion(210, "x", (0, 186, 0), 40, "欧标 4040 型材"))
    S.append(box((210, 8, 2.4), (0, 202, 38.6), "8mm 槽口"))
    S.append(box((86, 58, 40), (244, 104, 0), "8mm 槽配件分箱"))
    S.append(box((66, 4, 20), (254, 102, 12), "分箱标签"))

    items = [("①", "欧标 2020，槽宽 6mm，壁厚 1.8mm", (150, 7, 19.8)),
             ("②", "M5 T 型螺母 / 滑块螺母 + M5 内六角", (52, 10, 33)),
             ("③", "L 角码外露 / 内置角槽件隐藏", (196, 10, 47)),
             ("④", "端盖与层板托，外面不见金属件", (-42, 10, 1.3)),
             ("⑤", "3030/4040 为 8mm 槽，配件单独分箱", (105, 202, 39))]
    audit(items, S, -56, 32)
    print("saved", draw("0805-1", "欧标 2020 型材配件套", items, S,
                        note="D3 定标后的最小采购单元：铝做骨、藏在木料后面；20 与 30/40 两档配件分箱存放，绝不混用",
                        sig="设想 · 0805", az=-56, el=32, fov=27))


# ---------------------------------------------------------------- 0805-2
def fig2():
    S = []
    # ① 底：2020 型材框 30×30cm
    S.append(extrusion(300, "x", (0, 0, 0), 20, "2020 型材框"))
    S.append(extrusion(300, "x", (0, 280, 0), 20, "2020 型材框"))
    S.append(extrusion(260, "y", (0, 20, 0), 20, "2020 型材框"))
    S.append(extrusion(260, "y", (280, 20, 0), 20, "2020 型材框"))

    # ② 内置角槽件连接（四角，沿 +Z 拆开一层）
    for x, y, a in ((20, 20, 0), (280, 20, 90), (280, 280, 180), (20, 280, 270)):
        hc = hidden_corner((0, 0, 0))
        hc = rot(hc, a, "z", (0, 0, 0))
        S.append(mv(hc, (x, y, 90)))

    # ③ 中：18mm 白蜡木面板，油蜡饰面（边缘留 2mm 让木头热胀）
    PZ = 210.0
    S.append(box((296, 296, 18), (2, 2, PZ), "18mm 白蜡木面板"))
    for i in range(7):
        S.append(box((296, 1.8, 0.8), (2, 34 + i * 38, PZ + 18), "木纹"))

    # ④ 背面固定不露钉：四颗 M5 从背面拧进面板
    for x, y in ((46, 46), (254, 46), (46, 254), (254, 254)):
        S.append(hexbolt((x, y, PZ - 34), 2.5, 22, 4.6, 5, "背面固定 M5"))

    # ⑤ 面：植鞣牛皮包角 8×8cm（只用在手长时间接触的表面）
    LZ = PZ + 130
    lt = [box((80, 80, 3.2), (218, 218, LZ), "植鞣牛皮包角"),
          box((80, 3.2, 26), (218, 296, LZ - 26), "牛皮包边"),
          box((3.2, 80, 26), (296, 218, LZ - 26), "牛皮包边")]
    S.append(merge(lt, "植鞣牛皮包角 8×8cm"))
    for i in range(5):
        S.append(cyl(1.6, 4, "z", (230 + i * 14, 300, LZ - 14), 8, "手缝线"))

    items = [("①", "底：2020 型材框 30×30cm", (150, 10, 20)),
             ("②", "内置角槽件连接，外面看不到金属", (28, 20, 95)),
             ("③", "中：18mm 白蜡木面板，油蜡饰面", (120, 148, PZ + 18)),
             ("④", "背面固定不露钉，边缘留 2mm 热胀", (200, 2, PZ + 6)),
             ("⑤", "面：植鞣牛皮包角 8×8cm 在手接触处", (258, 258, LZ + 3.2))]
    slots = [("①", "", (66, 740)), ("②", "", (66, 470)), ("③", "", (1134, 430)),
             ("④", "", (1134, 650)), ("⑤", "", (1134, 240))]
    audit(items, S, -58, 30)
    print("saved", draw("0805-2", "三材分层样板", items, S, slots=slots,
                        note="铝做骨、木做面、皮草做触感；常年放在木屋 0102 作品墙下的材质样板格里，采购前先摸一下、顺便对色",
                        sig="设想 · 0805", az=-58, el=30, fov=27))


if __name__ == "__main__":
    fig1(); fig2()
