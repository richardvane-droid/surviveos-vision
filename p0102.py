"""0102 PSK 作品展示墙 — 两张硬件爆炸图（hand3d 管线）
0102-1 松木九宫格托架墙 / 0102-2 斜射藏光灯条
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import wall
from partdraw import draw
from p01util import merge, rot, prism, audit

PW = 1350                 # 拼板 1.35m 见方
Z0, Z1 = 1050, 2400       # 底边 / 梁底
CELL = 430                # 每格 ≈43cm
DEP = 150                 # 格深 15cm


# ---------------------------------------------------------------- 0102-1
def fig1():
    S = [wall(1680, 1500, 80, (-165, 0, 1010))]

    # ① 找平木龙骨（上下两根横龙骨比拼板宽出 220，露出来才看得见）
    for x0 in (55, 470, 880, 1250):
        S.append(box((48, 48, PW - 96), (x0, -48, Z0 + 48), "找平木龙骨"))
    for zz in (Z0, Z1 - 48):
        S.append(box((PW + 440, 48, 48), (-220, -48, zz), "找平木龙骨"))

    # ② 18mm 老松木拼板，7 块，板间留 3mm 缝
    YP = -258
    pl = []
    for i in range(7):
        pl.append(box((190, 18, PW), (i * 193, YP, Z0), "老松木拼板"))
    S.append(merge(pl, "18mm 老松木拼板"))

    # ③ 3×3 九格托架，深 150，格板 24
    YG = -560
    t = 24
    gr = []
    for i in range(4):
        gr.append(box((t, DEP, PW), (i * (CELL + t) * (PW - t) / (3 * CELL + 4 * t - t) if False else i * 442, YG - DEP, Z0), "竖格板"))
    for j in range(4):
        gr.append(box((PW, DEP, t), (0, YG - DEP, Z0 + j * 442), "横格板"))
    S += gr

    # ④ 前缘凸边 8mm（每排一条）
    YL = -880
    for j in range(3):
        S.append(box((PW, 20, 9), (0, YL, Z0 + j * 442 + t), "前缘凸边"))

    # ⑤ 历代 PSK 盒（每格两位，右下格留 2 空）+ 盒下牛皮纸标签
    YB = -1000
    bxs, tags = [], []
    for j in range(3):
        for i in range(3):
            if j == 0 and i == 2:            # 右下格：下一代，待定
                continue
            for k in range(2):
                x = i * 442 + 40 + k * 190
                z = Z0 + j * 442 + t + 40
                bxs.append(box((160, 112, 46), (x, YB - 112, z), "PSK 盒"))
                tags.append(box((62, 92, 3), (x + 48, YB - 220, z - 40), "牛皮纸标签"))
    S += bxs
    S.append(merge(tags, "牛皮纸标签"))

    items = [("①", "找平木龙骨，拼板贴梁底往下挂", (1500, -24, Z1 - 24)),
             ("②", "18mm 老松木拼板，板间留 3mm 缝", (1117, YP, 2160)),
             ("③", "3×3 九格各 43cm、深 15cm，微微前倾", (1000, YG - 80, 2390)),
             ("④", "前缘凸边 8mm，盒子不会滑出来", (1100, YL, Z0 + t + 5)),
             ("⑤", "历代 PSK 盒每格两位，右下留 2 空位", (120, YB - 112, 1585))]
    audit(items, S, -60, 20)
    p = draw("0102-1", "松木九宫格托架墙", items, S,
             note="北墙中段偏东，贴梁底 2400 往下的 1350 见方；不刷漆，钉眼虫洞都留着",
             sig="设想 · 0102", az=-60, el=20, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0102-2
def strip_row(z, y0, spread=0.0, tag=""):
    """一排：托架上沿木板 + 30° 楔形木条 + U 型铝槽 + COB 灯带 + 磨砂扩散罩。
    spread=0 为装好的状态；>0 沿 -Y / -Z 拉开。"""
    o = []
    o.append(box((PW, DEP, 24), (0, y0 - DEP, z), "托架上沿"))
    s = spread
    # 楔形木条：104 深 × 60 高，斜面 30°
    wy, wz = y0 - DEP + 6 - 190 * s, z - 66 - 90 * s
    o.append(prism([(0, 0), (-104, 0), (-104, -60)], PW, "x", (0, wy + 104, wz + 60), "30° 楔形木条"))
    # 下面三层都绕 X 转 30°，跟着斜面走
    def tilted(sol, cy, cz):
        return rot(sol, 30, "x", (PW / 2, cy, cz))
    cy, cz = wy - 170 * s, wz - 92 * s
    ch = [box((PW, 44, 4), (0, cy, cz), "U 型铝槽"),
          box((PW, 4, 24), (0, cy, cz), "U 型铝槽"),
          box((PW, 4, 24), (0, cy + 40, cz), "U 型铝槽")]
    o.append(tilted(merge(ch, "U 型铝槽"), cy + 22, cz + 12))
    ly, lz = cy - 170 * s, cz - 92 * s
    o.append(tilted(box((PW, 16, 5), (0, ly + 14, lz), "COB 灯带"), ly + 22, lz + 2))
    dy, dz = ly - 170 * s, lz - 92 * s
    o.append(tilted(box((PW, 34, 7), (0, dy + 5, dz), "磨砂扩散罩"), dy + 22, dz + 3))
    return o, dict(wedge=(1150, wy - 40, wz + 30), chan=(300, cy + 22, cz + 26),
                   led=(640, ly + 22, lz + 2), dif=(940, dy + 22, dz + 3))


def fig2():
    S = [wall(1560, 980, 80, (60, 0, 1380))]
    top, A = strip_row(2340, -560, 0.78)
    S += top
    for z in (1898, 1456):
        r, _ = strip_row(z, -560, 0.0)
        S += r
    # ESP32 控制盒 + 24V 电源（贴墙）
    S += [box((130, 86, 44), (1400, -130, 2180), "ESP32 控制盒"),
          cyl(4, 30, "z", (1430, -88, 2224), 8, "天线"),
          box((180, 76, 52), (1400, -120, 2000), "24V 电源"),
          box((60, 8, 22), (1440, -128, 2020), "端子")]

    items = [("①", "COB 灯带 2700K Ra≥90，10W/m，24V", A["led"]),
             ("②", "磨砂扩散罩，把光点抹平", A["dif"]),
             ("③", "U 型铝槽 1.35m 一根，兼作散热", A["chan"]),
             ("④", "30° 楔形木条，决定入射角", A["wedge"]),
             ("⑤", "ESP32 跑 WLED，三排分三段控制", (1465, -130, 2220))]
    audit(items, S, -37, 25)
    p = draw("0102-2", "斜射藏光灯条", items, S,
             note="每排格子上沿藏一条，从斜上方 30° 打下来盒子才有阴影；正面打光盒子是平的",
             sig="设想 · 0102", az=-37, el=25, fov=27)
    print("saved", p)


fig1()
fig2()
