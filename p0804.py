"""0804 全屋存储 + 全屋智能 — 两张硬件爆炸图（hand3d 管线）
0804-1 三机型材机架 / 0804-2 存储与冷备盘组

机架在地堡东侧储藏室隔墙背后：60×40cm、1.2m 高的 2020 喷砂黑型材架，
正面敞开朝 -Y（相机一侧），三面打孔铝板围住防灰。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl, extrusion
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, capped_cyl, disc)

RW, RD, RH, FT = 600.0, 400.0, 1200.0, 100.0        # 机架 60×40×120cm，离地 10cm


def perf(origin, du, dv, nu, nv, r=6, name="打孔铝板"):
    """一片板面上的圆孔特征线（du/dv 是两个方向的步进向量）。"""
    o = np.asarray(origin, float); u = np.asarray(du, float); v = np.asarray(dv, float)
    uu, vv = u / np.linalg.norm(u), v / np.linalg.norm(v)
    E = []
    for i in range(nu):
        for j in range(nv):
            c = o + u * i + v * j
            pp = [c + uu * r * math.cos(t) + vv * r * math.sin(t)
                  for t in np.linspace(0, 2 * math.pi, 9)]
            E += [(pp[k], pp[k + 1]) for k in range(8)]
    return Solid([], E, name)


# ---------------------------------------------------------------- 0804-1
def fig1():
    S = []
    fl = box((1500, 1100, 30), (-450, -500, -30), "储藏室地面"); fl.shade = False
    S.append(fl)

    # ① 2020 喷砂黑欧标型材机架，离地 10cm
    for dx, dy in ((0, 0), (RW - 20, 0), (0, RD - 20), (RW - 20, RD - 20)):
        S.append(extrusion(RH, "z", (dx, dy, FT), 20, "2020 喷砂黑型材"))
        S.append(box((44, 44, FT), (dx - 12, dy - 12, 0), "调平脚"))
    for z in (FT, FT + RH - 20):
        S.append(extrusion(RW - 40, "x", (20, 0, z), 20, "2020 喷砂黑型材"))
        S.append(extrusion(RW - 40, "x", (20, RD - 20, z), 20, "2020 喷砂黑型材"))
        S.append(extrusion(RD - 40, "y", (0, 20, z), 20, "2020 喷砂黑型材"))
        S.append(extrusion(RD - 40, "y", (RW - 20, 20, z), 20, "2020 喷砂黑型材"))
    LZ = (140.0, 470.0, 720.0, 960.0)
    for z in LZ:
        S.append(extrusion(RW - 40, "x", (20, 0, z), 20, "层横梁"))
        S.append(extrusion(RW - 40, "x", (20, RD - 20, z), 20, "层横梁"))
        S.append(box((RW - 40, RD, 16), (20, 0, z + 20), "层板"))

    # ⑤ 打孔铝板三面围（沿各自法向拉开），正面敞开
    S.append(box((14, RD + 40, RH - 60), (-260, -20, FT + 30), "打孔铝板"))
    S.append(perf((-252, 40, FT + 110), (0, 62, 0), (0, 0, 92), 6, 11, 7))
    S.append(box((14, RD + 40, RH - 60), (RW + 246, -20, FT + 30), "打孔铝板"))
    S.append(perf((RW + 254, 40, FT + 110), (0, 62, 0), (0, 0, 92), 6, 11, 7))
    S.append(box((RW + 40, 14, RH - 60), (-20, RD + 300, FT + 30), "打孔铝板"))
    S.append(perf((60, RD + 308, FT + 110), (64, 0, 0), (0, 0, 92), 9, 11, 7))

    # ② 层 1：四盘位 NAS + 小 UPS（沿 -Y 拉出）
    E1 = -560.0
    S.append(box((230, 250, 180), (40, E1, LZ[0] + 36), "四盘位 NAS"))
    for i in range(4):
        S.append(box((48, 10, 150), (50 + i * 55, E1 - 10, LZ[0] + 51), "盘位"))
    S.append(box((250, 250, 180), (320, E1, LZ[0] + 36), "小 UPS"))
    S.append(box((140, 10, 50), (370, E1 - 10, LZ[0] + 110), "UPS 面板"))

    # ③ 层 2：Windows 笔记本（合上盖子）
    E2 = -900.0
    S.append(box((380, 270, 28), (110, E2, LZ[1] + 36), "Windows 笔记本"))
    S.append(box((340, 8, 14), (130, E2 - 8, LZ[1] + 44), "笔记本前沿"))
    S.append(box((60, 40, 6), (270, E2 + 40, LZ[1] + 64), "转轴"))

    # ④ 层 3：M1 Mac mini + 2.5GbE 交换机
    E3 = -1240.0
    S.append(box((200, 200, 40), (60, E3, LZ[2] + 36), "M1 Mac mini"))
    S.append(disc(60, (160, E3, LZ[2] + 56), "y", 20, "Mac mini 前面"))
    S.append(box((220, 120, 32), (330, E3 + 40, LZ[2] + 36), "2.5GbE 交换机"))
    for i in range(5):
        S.append(box((28, 10, 20), (344 + i * 40, E3 + 30, LZ[2] + 42), "网口"))

    # 层 4：光猫 + 理线板（留在架上）
    S.append(box((210, 160, 38), (60, 90, LZ[3] + 36), "光猫"))
    S.append(box((260, 70, 60), (320, 60, LZ[3] + 36), "理线板"))
    for i in range(4):
        S.append(path_tube([(350 + i * 60, 90, LZ[3] + 96), (350 + i * 60, 260, LZ[3] + 40),
                            (300, 300, LZ[2] + 60)], 8, 6, "跳线"))
    # PDU（带浪涌保护），竖在后立柱旁
    S.append(box((70, 70, 700), (RW - 96, RD - 96, FT + 120), "PDU 浪涌保护"))
    for i in range(6):
        S.append(box((44, 10, 44), (RW - 83, RD - 106, FT + 180 + i * 96), "PDU 插位"))

    items = [("①", "2020 喷砂黑欧标型材 60×40×120cm", (RW - 20, 0, FT + 700)),
             ("②", "层 1 四盘位 NAS，离地 10cm 防潮", (155, E1 - 10, LZ[0] + 126)),
             ("③", "层 2 Windows 笔记本，电池当 UPS", (300, E2 - 8, LZ[1] + 50)),
             ("④", "层 3 M1 Mac mini + 2.5GbE 交换机", (160, E3, LZ[2] + 56)),
             ("⑤", "打孔铝板三面围，正面敞开走风道", (-252, 350, FT + 660))]
    audit(items, S, -58, 18)
    print("saved", draw("0804-1", "三机型材机架", items, S,
                        note="机架在地堡储藏室隔墙背后：三面打孔铝板围住防灰、正面敞开留风道，风自下而上；一根 2.5GbE 穿隔墙到 0802 屏墙",
                        sig="设想 · 0804", az=-58, el=18, fov=27))


# ---------------------------------------------------------------- 0804-2
def fig2():
    """四盘位竖插盘架依次拉出，右边是冷备盘与阁楼保险箱。"""
    S = []
    W, D, H = 250.0, 260.0, 200.0
    t = 10.0
    cs = [box((W, t, H), (0, D - t, 0), "NAS 机箱"),
          box((t, D, H), (0, 0, 0), "NAS 机箱"), box((t, D, H), (W - t, 0, 0), "NAS 机箱"),
          box((W, D, t), (0, 0, 0), "NAS 机箱"), box((W, D, t), (0, 0, H - t), "NAS 机箱")]
    S.append(merge(cs, "四盘位 NAS 机箱"))
    for i in range(5):
        S.append(box((6, D - 20, 6), (10 + i * 57, 0, 176), "盘位隔条"))
    for i in range(4):
        S.append(cyl(5, 18, "y", (38 + i * 57, -18, 186), 8, "盘位指示灯"))
    S.append(box((90, 10, 30), (W - 100, -10, 20), "NAS 前面板"))

    # ①② 四个竖插盘架沿 -Y 依次拉出：两块 8TB 镜像 + 两块 4TB 影音
    lab = ("8TB 镜像", "8TB 镜像", "4TB 影音", "4TB 影音")
    FY = []
    for i in range(4):
        x = -330.0 + (i % 2) * 180
        z0 = 620.0 if i < 2 else 30.0
        ey = -430.0
        tr = [box((46, 240, 14), (x, ey, z0), "热插拔盘架"),
              box((52, 14, 170), (x - 3, ey - 14, z0 - 10), "盘架面板"),
              box((14, 240, 40), (x, ey, z0 + 14), "盘架侧轨"),
              box((14, 240, 40), (x + 32, ey, z0 + 14), "盘架侧轨"),
              box((16, 26, 40), (x + 18, ey - 40, z0 + 80), "盘架手柄")]
        S.append(merge(tr, "热插拔盘架"))
        S.append(box((28, 150, 104), (x + 9, ey + 50, z0 + 14), "3.5 寸硬盘 · " + lab[i]))
        S.append(box((30, 4, 44), (x + 11, ey - 18, z0 + 40), lab[i] + " 标签"))
        FY.append((x, ey, z0))
    # 机箱里还留着的一条空导轨
    S.append(box((46, 230, 12), (14, 16, 16), "空盘位导轨"))

    # ⑤ 阁楼保险箱（和 NAS 不在同一个房间、不在同一路电上）
    SX, SY, SZ = 470.0, 170.0, 0.0
    S.append(merge([box((320, 280, 280), (SX, SY, SZ), "阁楼保险箱")], "阁楼保险箱"))
    S.append(box((300, 16, 260), (SX + 10, SY - 16, SZ + 10), "保险箱门"))
    S.append(capped_cyl(42, 22, "y", (SX + 100, SY - 38, SZ + 160), 18, "机械转盘"))
    S.append(disc(42, (SX + 100, SY - 38, SZ + 160), "y", 18, "机械转盘"))
    S.append(box((24, 24, 100), (SX + 230, SY - 32, SZ + 120), "把手"))

    # ④ USB 冷备 4TB（每周从 NAS 拷一次，然后拿到阁楼保险箱）
    CX, CY, CZ = 520.0, -60.0, 800.0
    S.append(box((150, 96, 32), (CX, CY, CZ), "USB 冷备 4TB"))
    S.append(box((110, 6, 12), (CX + 20, CY + 96, CZ + 10), "USB 口"))
    S.append(box((60, 4, 14), (CX + 46, CY - 4, CZ + 10), "冷备标签"))
    S.append(path_tube([(CX + 75, CY + 100, CZ + 16), (CX + 120, CY + 180, CZ - 40),
                        (CX + 60, CY + 240, CZ - 120)], 7, 6, "USB 线"))

    items = [("①", "镜像池 2×8TB：照片 / 快照 / 文档", (FY[0][0] + 26, FY[0][1] - 18, FY[0][2] + 62)),
             ("②", "单盘池 2×4TB：影音库，可再生", (FY[3][0] + 26, FY[3][1] - 18, FY[3][2] + 62)),
             ("③", "四盘位热插拔，坏一块换一块", (W - 55, -10, 35)),
             ("④", "USB 冷备 4TB，每周从 NAS 拷一次", (CX + 76, CY - 4, CZ + 17)),
             ("⑤", "存阁楼保险箱，不同房间不同电路", (SX + 100, SY - 38, SZ + 160))]
    slots = [("①", "", (66, 470)), ("②", "", (66, 800)), ("③", "", (1134, 812)),
             ("④", "", (1134, 260)), ("⑤", "", (1134, 600))]
    audit(items, S, -60, 28)
    print("saved", draw("0804-2", "存储与冷备盘组", items, S, slots=slots,
                        note="快照防误删、镜像防单盘坏、冷盘防火防水淹；三层各管一件事，缺一层就有一种事故救不回来",
                        sig="设想 · 0804", az=-60, el=28, fov=27))


if __name__ == "__main__":
    fig1(); fig2()
