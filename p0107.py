"""0107 小吧台 — 0107-2 柜内三层木架（0107-1 老榆木自然边吧台已出，不重做）"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from partdraw import draw
from p01util import merge, jar, mug, screw, audit

CW, CD, CH = 1100, 450, 840      # 矮柜一段：柜高 840 + 台面 → 900，深 45cm
SZ = (220, 470, 660)             # 三层隔板的标高


def fig2():
    S = []
    # 老榆木自然边台面（只给一段）
    S += [box((1280, 600, 62), (-90, -540, CH), "老榆木台面"),
          box((1280, 84, 28), (-90, -624, CH + 12), "自然边")]
    # 松木矮柜
    S += [box((22, CD, CH), (0, -CD, 0), "松木矮柜"),
          box((22, CD, CH), (CW - 22, -CD, 0), "松木矮柜"),
          box((CW, CD, 22), (0, -CD, 0), "松木矮柜"),
          box((CW, CD, 22), (0, -CD, CH - 22), "柜顶板"),
          box((CW, 18, CH), (0, -18, 0), "柜背板")]
    # 柜门（开到一边）
    S.append(box((500, 24, 740), (-640, -CD - 150, 50), "柜门"))
    S.append(cyl(11, 92, "y", (-410, -CD - 242, 420), 12, "铜把手"))

    # ① 榆木立柱 ×2，螺栓固定在柜侧板
    for x0 in (26, CW - 86):
        S.append(box((60, 60, 780), (x0, -780, 30), "榆木立柱"))
        for z in (180, 560):
            S += screw((x0 + 30, -780, z), 7, 128, "y", "固定螺栓")

    # ② 隔板 ×3，榫槽插进立柱（本层再各错开 90 看清榫头）
    for i, z in enumerate(SZ):
        y0 = -760 - i * 70
        S.append(box((900, 420, 26), (100, y0, z), "隔板"))
        for x0 in (100, CW - 226):
            S.append(box((126, 58, 15), (x0, y0 + 300, z - 15), "榫头"))

    # ③ 中层玻璃罐 ×8 + ⑤ 手写牛皮纸标签
    ZJ, YJ = SZ[1] + 26, -770
    jr, tg = [], []
    for i in range(8):
        x = 168 + i * 112
        jr += jar((x, YJ, ZJ), 48, 126, "玻璃罐")
        tg.append(box((52, 4, 38), (x - 26, YJ - 50, ZJ + 40), "牛皮纸标签"))
        tg.append(cyl(3, 96, "x", (x - 48, YJ, ZJ + 84), 8, "麻绳"))
    S += jr
    S.append(merge(tg, "牛皮纸标签"))

    # ④ 上层杯钩条：倒挂十几只杯子
    ZH, YH = 1080, -950
    S.append(box((860, 34, 22), (120, YH - 17, ZH), "杯钩条"))
    cups = []
    for i in range(6):
        x = 176 + i * 146
        cups.append(cyl(6, -40, "z", (x, YH, ZH), 8, "杯钩"))
        cups += mug((x, YH, ZH - 132), 40, 92, up=False, name="杯")
    S.append(merge(cups, "倒挂的杯子"))

    items = [("①", "榆木立柱 ×2，螺栓固定在柜侧板", (CW - 26, -750, 700)),
             ("②", "隔板 ×3 榫槽插进立柱，没有外露螺丝", (988, -900, SZ[2] + 26)),
             ("③", "中层玻璃罐 ×8：咖啡豆 / 桂花 / 陈皮 / 柠檬", (616 + 34, YJ - 34, ZJ + 80)),
             ("④", "上层杯钩条，倒挂十几只不同的杯子", (468 + 28, YH - 28, ZH - 100)),
             ("⑤", "手写牛皮纸标签 + 麻绳，罐内物一眼看清", (280, YJ - 50, ZJ + 58))]
    audit(items, S, -60, 18)
    p = draw("0107-2", "柜内三层木架", items, S,
             note="台面上方的墙要留给画框墙，架子全部收进柜里；台面永远只留电器，收拾只要三分钟",
             sig="设想 · 0107", az=-60, el=18, fov=27)
    print("saved", p)


fig2()
