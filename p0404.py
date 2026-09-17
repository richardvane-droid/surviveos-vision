"""0404 木工间集尘与工具墙 — 两张硬件爆炸图
0404-1 旋风集尘器与分路阀 / 0404-2 法式挂条工具墙
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl, extrusion
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, gable,
                     label, audit, ROOF)


# ---------------------------------------------------------------- 0404-1
def fig1():
    S = []
    S.append(floor(3600, 2600, (-1900, -1500, 0)))
    S.append(gable((-1830, 1100 - ROOF, 0), ROOF, 70, False, "45° 斜顶"))

    # ① 最下层：60L 集尘桶（带透明视窗）+ 桶车
    BR, BH = 250.0, 620.0
    S.append(cone(BR * 0.88, BR, BH, (0, 0, 130), 22, "60L 集尘桶"))
    S.append(cyl(BR * 1.06, 30, "z", (0, 0, 130 + BH - 30), 22, "桶口箍"))
    S.append(box((90, 30, 420), (-45, -BR - 4, 230), "透明视窗"))
    S.append(box((680, 680, 40), (-340, -340, 90), "桶车底板"))
    for (dx, dy) in ((-250, -250), (250, -250), (-250, 250), (250, 250)):
        S.append(cyl(45, 26, "x", (dx - 13, dy, 45), 16, "脚轮"))

    # ② 中层：旋风分离器（筒身 + 锥体），沿 +Z 爆炸
    CZ = 1060.0
    S.append(cone(250, 90, 360, (0, 0, CZ), 22, "旋风锥体"))
    S.append(cyl(250, 300, "z", (0, 0, CZ + 360), 22, "旋风筒身"))
    S.append(cyl(262, 26, "z", (0, 0, CZ + 660), 22, "筒顶法兰"))
    S.append(cyl(72, 240, "y", (170, -250, CZ + 540), 18, "切向进风口"))
    S.append(cyl(80, 360, "z", (0, 0, CZ + 420), 18, "中心出风管"))

    # ③ 上层：带滤芯的抽风电机，沿 +Z 再爆炸
    MZ = CZ + 1080
    S.append(cyl(210, 300, "z", (0, 0, MZ), 22, "褶皱滤芯"))
    for i in range(9):
        S.append(box((440, 22, 300), (-220, -110 + i * 26, MZ), "滤褶"))
    S.append(cyl(230, 26, "z", (0, 0, MZ + 300), 22, "滤芯压盖"))
    S.append(cyl(170, 280, "z", (0, 0, MZ + 326), 20, "抽风电机"))
    S.append(cone(170, 96, 110, (0, 0, MZ + 606), 18, "电机顶罩"))
    S.append(box((140, 90, 120), (-70, 150, MZ + 380), "电机接线盒"))

    # ④ 三路 100mm 管 + 舵机挡板阀（向外爆炸）
    VALVE = []
    for i, (ang, nm) in enumerate(((168, "台锯路"), (210, "带锯路"), (252, "刨床路"))):
        a = math.radians(ang)
        r0, r1 = 700.0, 1500.0
        p0 = (r0 * math.cos(a), r0 * math.sin(a), CZ + 540)
        p1 = (r1 * math.cos(a), r1 * math.sin(a), CZ + 540)
        S.append(path_tube([p0, p1], 52, 16, "100mm 管路"))
        # 阀体：短方盒 + 挡板 + 9g 舵机
        mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, p0[2])
        S.append(box((150, 150, 150), (mid[0] - 75, mid[1] - 75, mid[2] - 75), "挡板阀体"))
        S.append(box((120, 14, 120), (mid[0] - 60, mid[1] - 7, mid[2] - 60), "金属挡板"))
        S.append(box((44, 26, 52), (mid[0] - 22, mid[1] - 13, mid[2] + 90), "9g 舵机"))
        S.append(cyl(8, 40, "z", (mid[0], mid[1], mid[2] + 75), 10, "舵机摇臂"))
        S.append(label((mid[0] - 40, mid[1] - 90, mid[2] - 150), 90, 34, 5, nm))
        VALVE.append((mid[0], mid[1] - 80, mid[2] + 100))
    # 主进风：从三路汇合到旋风切向进风口
    S.append(path_tube([(560, -180, CZ + 540), (170, -250, CZ + 540)], 52, 14, "汇合管"))

    items = [("①", "集尘桶 60L，带透明视窗看余量", (0, -BR - 6, 440)),
             ("②", "旋风分离器分离 95% 以上木屑", (0, -250, CZ + 500)),
             ("③", "滤芯在上，极细粉尘才到达，很久不堵", (0, -215, MZ + 150)),
             ("④", "三路 100mm 阀门，9g 舵机驱动挡板", VALVE[1]),
             ("⑤", "管路直管为主，用哪台只开哪路", (1330 * math.cos(math.radians(252)), 1330 * math.sin(math.radians(252)) - 52, CZ + 540))]
    audit(items, S, -62, 18)
    print("saved", draw("0404-1", "旋风集尘器与分路阀", items, S,
                        note="木工间东北角斜顶下；木屑沿筒壁螺旋下落靠离心力甩进桶里，只有极细粉尘才到达滤芯",
                        sig="设想 · 0404", az=-62, el=18, fov=27))


# ---------------------------------------------------------------- 0404-2
def fig2():
    S = []
    WW, WH = 1700.0, 2060.0
    S.append(floor(2900, 2600, (-500, -2100, 0)))
    S.append(ghost(box((WW, 70, WH), (0, 0, 0), "西侧隔断 2060")))
    # 隔断立柱（龙骨）
    for x in (80.0, 1560.0):
        S.append(ghost(box((60, 20, WH), (x, -20, 0), "隔断立柱")))

    # ① 法式墙条：18mm 多层板 45° 斜切，90 宽，间距 100
    SEC = [(0, 0), (18, 0), (18, 36), (0, 90)]        # (y, z) 断面：斜面朝上
    for i in range(14):
        z = 520 + i * 100.0
        S.append(prism(SEC, WW - 120, "x", (60, -18, z), "墙条 18mm"))
        for x in (110.0, 810.0, 1510.0):
            S.append(cyl(6, 40, "y", (x, -40, z + 30), 8, "螺丝"))

    # 挂架：背面斜条 + 各自专属形式，沿 -Y 爆炸出来
    OUT = -1080.0

    def cleat_back(x, z, w):
        """挂架背面的斜条（斜面朝下，与墙条互扣）。"""
        return prism([(0, 0), (18, 0), (0, 90)], w, "x", (x, OUT + 18, z), "挂架斜条")

    # ③ 刨子搁板（放在视线平齐处）
    PX, PZ = 120.0, 1450.0
    S.append(cleat_back(PX, PZ, 620))
    S.append(box((620, 240, 24), (PX, OUT - 220, PZ - 24), "刨子搁板"))
    S.append(box((620, 24, 90), (PX, OUT - 244, PZ - 24), "搁板挡条"))
    S.append(box((620, 30, 150), (PX, OUT + 12, PZ - 150), "搁板背板"))
    for k, (ln, wd) in enumerate(((250.0, 62.0), (200.0, 52.0))):
        bx = PX + 90 + k * 300
        S.append(box((ln, wd, 70), (bx, OUT - 150, PZ), "刨子"))
        S.append(box((ln * 0.4, wd, 90), (bx + ln * 0.3, OUT - 150, PZ + 70), "刨手柄"))
        S.append(box((ln * 0.2, wd + 8, 20), (bx + ln * 0.4, OUT - 154, PZ - 14), "刨刀"))

    # ④ 凿子斜插槽
    CX, CZ2 = 900.0, 1820.0
    S.append(cleat_back(CX, CZ2, 420))
    S.append(box((420, 170, 60), (CX, OUT - 150, CZ2 - 60), "凿子插槽块"))
    S.append(box((420, 30, 160), (CX, OUT + 12, CZ2 - 160), "插槽背板"))
    for i in range(5):
        cx = CX + 50 + i * 78
        S.append(cyl(18, 190, "z", (cx, OUT - 70, CZ2), 12, "凿柄"))
        S.append(box((22, 22, 130), (cx - 11, OUT - 81, CZ2 - 190), "凿身"))
        S.append(cone(13, 4, 40, (cx, OUT - 70, CZ2 - 230), 10, "凿刃"))

    # ⑤ 木工夹横杆（重物放低层）
    FX, FZ = 180.0, 900.0
    S.append(cleat_back(FX, FZ, 1300))
    S.append(box((1300, 30, 140), (FX, OUT + 12, FZ - 140), "夹具架背板"))
    S.append(cyl(24, 1300, "x", (FX, OUT - 130, FZ - 60), 14, "夹具横杆"))
    for i in range(4):
        fx = FX + 110 + i * 250
        S.append(box((40, 40, 520), (fx, OUT - 150, FZ - 620), "F 夹主杆"))
        S.append(box((180, 50, 40), (fx - 140, OUT - 155, FZ - 160), "F 夹固定臂"))
        S.append(box((180, 50, 40), (fx - 140, OUT - 155, FZ - 500), "F 夹活动臂"))
        S.append(cyl(11, 120, "y", (fx - 120, OUT - 155, FZ - 480), 10, "夹紧丝杆"))

    items = [("①", "墙条 18mm 多层板 45° 斜切，间距 100mm", (1380, -18, 1265)),
             ("②", "挂架背面斜条一搭，越重越牢", (CX + 210, OUT + 18, CZ2 + 40)),
             ("③", "刨子搁板：常用工具放视线高度", (PX + 300, OUT - 150, PZ + 40)),
             ("④", "凿子斜插槽，刃口朝下不磕碰", (CX + 206, OUT - 81, CZ2 - 120)),
             ("⑤", "木工夹横杆挂 F 夹，重物放低层", (FX + 620, OUT - 155, FZ - 480))]
    audit(items, S, -66, 18)
    print("saved", draw("0404-2", "法式挂条工具墙", items, S,
                        note="墙上的条斜面朝上、挂架背面的条斜面朝下，两个斜面一搭，重力把挂架往墙里压，越重越牢",
                        sig="设想 · 0404", az=-66, el=18, fov=27))


fig1()
fig2()
