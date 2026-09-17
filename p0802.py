"""0802 全屋中枢 / 全屋数据可视化屏 — 一张硬件爆炸图（hand3d 管线）
0802-1 指挥室屏墙总成

屏墙挂在地堡东侧储藏室的西隔墙（≈2.45m 长）上，面朝中央地毯和沙发；
隔墙在 +Y 一侧，屏幕沿 -Y（相机一侧）拉出；主机/UPS/网关藏在隔墙背后。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from props import wall
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, capped_cyl, disc)

WW, WH = 2450.0, 2150.0


def panel(pos, w, h, t=52, name="屏"):
    x, y, z = pos
    return [box((w, t, h), (x, y, z), name),
            box((w - 46, 8, h - 46), (x + 23, y - 8, z + 23), name + "面")]


def mount(pos, w, h, name="薄型壁挂支架"):
    """薄壁挂支架：墙板 + 两条挂条。"""
    x, y, z = pos
    o = [box((w, 26, h), (x, y, z), name)]
    for zz in (z + h * 0.16, z + h * 0.66):
        o.append(box((w + 40, 46, h * 0.16), (x - 20, y - 46, zz), name))
    return merge(o, name)


def fig1():
    S = []
    S.append(wall(WW, WH, 90, (0, 0, 0)))

    EY = -680.0        # 屏幕沿 -Y 拉出
    # ② 薄型壁挂支架（留在墙面上）
    S.append(mount((880, -26, 470), 690, 1330))
    S.append(mount((210, -26, 1020), 500, 300))
    S.append(mount((1740, -26, 1020), 500, 300))

    # ① 65 寸竖屏居中 + 两块 27 寸横屏
    S += panel((820, EY, 460), 810, 1430, 56, "65 寸竖屏")
    S += panel((150, EY, 1000), 620, 360, 44, "27 寸横屏")
    S += panel((1680, EY, 1000), 620, 360, 44, "27 寸横屏")
    # 中屏：整栋房子的等距地图
    for u, v in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (1, 2), (0, 2)):
        S.append(box((110, 6, 68), (1225 + (u - v) * 150 - 55, EY - 14, 900 + (u + v) * 96), "模块动态图标"))
    # 左屏：光照 / 温湿度曲线；右屏：水电柱状
    cur = []
    for i in range(11):
        cur.append(box((40, 5, 30 + 130 * abs(math.sin(i * 0.55))), (200 + i * 48, EY - 12, 1050), "曲线卡片"))
    S.append(merge(cur, "光照 / 温湿度曲线"))
    bar = []
    for i in range(7):
        bar.append(box((56, 5, 40 + 180 * (0.3 + 0.1 * ((i * 5) % 7))), (1740 + i * 76, EY - 12, 1040), "水电柱状"))
    S.append(merge(bar, "水电柱状图"))

    # ③ 屏下一排六个机械实体开关（ESP32 按键板）
    SY = EY + 140
    S.append(box((720, 120, 90), (865, SY, 300), "实体开关面板"))
    for i in range(6):
        S.append(capped_cyl(34, 46, "y", (930 + i * 118, SY - 46, 345), 14, "机械实体开关"))
    S.append(box((640, 90, 26), (905, SY + 20, 210), "ESP32 按键板"))

    # ④⑤ 隔墙背后储藏室里的带风扇浅机箱：主机 / UPS / 网关（放在墙的 +X 端外侧，便于看见）
    CX = 2640.0
    t = 18.0
    cs = [box((620, 420, t), (CX, 60, 700), "带风扇浅机箱"),
          box((620, 420, t), (CX, 60, 1302), "带风扇浅机箱"),
          box((t, 420, 620), (CX, 60, 700), "带风扇浅机箱"),
          box((t, 420, 620), (CX + 602, 60, 700), "带风扇浅机箱"),
          box((620, t, 620), (CX, 462, 700), "带风扇浅机箱背板")]
    S.append(merge(cs, "带风扇浅机箱"))
    for i in range(5):
        S.append(cyl(24, 30, "y", (CX + 110 + i * 100, 462, 1000), 10, "机箱风扇"))

    # 机箱里的三件沿 -Y 拉出来
    MY = -460.0
    S.append(box((300, 300, 64), (CX + 40, MY, 700), "N100 迷你主机"))
    S.append(box((150, 10, 24), (CX + 110, MY - 10, 730), "主机前面板"))
    S.append(box((420, 300, 190), (CX + 40, MY, 860), "300W UPS"))
    S.append(box((170, 12, 54), (CX + 90, MY - 12, 920), "UPS 面板"))
    S.append(box((230, 160, 40), (CX + 40, MY, 1160), "ESP32 网关板"))
    S.append(capped_cyl(16, 130, "z", (CX + 360, MY + 80, 1160), 12, "Zigbee 协调器"))
    S.append(path_tube([(CX + 300, 300, 1080), (1900, 300, 1080), (1300, 300, 1080)], 16, 8, "墙内暗管"))

    items = [("①", "65 寸竖屏居中 + 两块 27 寸横屏", (1225, EY - 14, 1700)),
             ("②", "薄型壁挂支架，线缆走墙内暗管", (1565, -26, 1600)),
             ("③", "屏下六个机械实体开关，按下有咔哒", (1166, SY - 46, 345)),
             ("④", "N100 迷你主机 16GB/512GB，15W", (CX + 185, MY - 10, 732)),
             ("⑤", "300W UPS 保 30 分钟 + Zigbee 协调器", (CX + 175, MY - 12, 920))]
    audit(items, S, -62, 12)
    print("saved", draw("0802-1", "指挥室屏墙总成", items, S,
                        note="挂在地堡东侧储藏室的西隔墙（≈2.45m）上，面朝中央地毯和沙发；主机、UPS 和网关装在隔墙背后的浅机箱里",
                        sig="设想 · 0802", az=-62, el=12, fov=27))


if __name__ == "__main__":
    fig1()
