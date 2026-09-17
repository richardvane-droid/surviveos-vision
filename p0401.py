"""0401 过道工具墙 — 0401-2 WORX 20V 电池平台与割草四件套（0401-1 已单独出图）"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import floor
from partdraw import draw
from p34util import (merge, rot, mv, prism, ghost, path_tube, cone, battery_pack,
                     label, audit)

CW, CD, CH = 2000.0, 420.0, 900.0        # 下区功能柜（图示 2.0m 一段）


def fig2():
    S = []
    S.append(floor(3200, 2800, (-420, -2500, 0)))
    S.append(ghost(box((2500, 70, 1560), (-220, CD, 0), "过道北侧隔断")))

    # 柜体
    body = [box((CW, CD, 40), (0, 0, 0)), box((CW, CD, 40), (0, 0, CH - 40)),
            box((CW, CD, 40), (0, 0, 480)), box((CW, 30, CH), (0, CD - 30, 0))]
    for x in (0.0, 1000.0, CW - 30):
        body.append(box((30, CD, CH), (x, 0, 0)))
    S.append(merge(body, "下区功能柜"))
    S.append(box((CW, 90, 40), (0, 40, -40), "柜踢脚"))

    # ① 一组充电位 ×4（柜右半边）+ WORX 20V 大脚板电池爆炸抬起
    BAT = []
    for i in range(4):
        x = 1070 + i * 215
        S.append(box((170, 300, 70), (x, 60, 520), "充电座"))
        S.append(box((150, 20, 34), (x + 10, 46, 556), "充电指示"))
        S += battery_pack((x + 26, 110, 1180 + (i % 2) * 150))
        BAT.append((x + 85, 110, 1180 + (i % 2) * 150 + 50))
        S.append(label((x + 20, -6, 620), 130, 44, 5, "荧光绿黑标签"))
    S.append(label((1080, -6, 760), 700, 60, 6, "充电位标签条"))

    # ⑤ 柜左半边：型材配件分箱（槽 6mm / 槽 8mm），抽屉拉出
    for k, z in enumerate((540.0, 120.0)):
        S.append(box((900, CD - 60, 310), (50, -520, z), "配件分箱抽屉"))
        S.append(box((940, 26, 350), (30, -546, z - 20), "抽屉面板"))
        S.append(cyl(11, 260, "x", (370, -570, z + 155), 10, "拉手"))
        for i in range(4):
            S.append(box((200, 74, 20), (80 + i * 205, -500, z + 290), "分格隔板"))
        S.append(label((120, -550, z + 60), 180, 46, 5, "槽 6 / 槽 8 标签"))

    # 割草四件套：平放在柜前的地垫上，头朝 -Y
    TY = -880.0
    # ② 电动打草机：轴 + 打草头 + 护罩 + D 形握把 + 电池位
    tx = 320.0
    S.append(cyl(28, 1250, "y", (tx, TY - 1250, 130), 14, "打草机轴"))
    S.append(box((175, 195, 175), (tx - 87, TY - 1430, 60), "打草机头"))
    S.append(cyl(180, 30, "z", (tx, TY - 1340, 40), 20, "打草护罩"))
    S.append(cyl(54, 60, "z", (tx, TY - 1340, 70), 16, "打草线盘"))
    S.append(box((170, 60, 90), (tx - 85, TY - 780, 130), "D 形握把"))
    S += battery_pack((tx - 59, TY - 210, 130), 118, 76, 98, "打草机电池")
    S.append(box((120, 150, 90), (tx - 60, TY - 160, 120), "打草机机身"))

    # ③ 吹叶机 WU231.9：机身 + 长喷嘴 + 电池位
    bx = 1000.0
    S.append(box((290, 430, 280), (bx - 145, TY - 430, 60), "吹叶机机身"))
    S.append(cone(125, 88, 270, (bx, TY - 430, 190), 18, "涡壳"))
    S.append(cyl(84, 540, "y", (bx, TY - 950, 190), 16, "吹管"))
    S.append(cone(84, 54, 160, (bx, TY - 1110, 190), 16, "扁嘴"))
    S.append(box((130, 190, 80), (bx - 65, TY - 200, 120), "吹叶机握把"))
    S += battery_pack((bx - 59, TY - 120, 60), 118, 76, 98, "吹叶机电池")
    S.append(label((bx - 90, TY - 432, 210), 180, 50, 6, "WU231.9 标签"))

    # ④ 手动修枝剪 + 手拔草器
    sx = 1560.0
    for s2 in (-1, 1):
        S.append(box((30, 300, 26), (sx + s2 * 22, TY - 700, 70), "修枝剪柄"))
        S.append(box((26, 230, 16), (sx + s2 * 8, TY - 930, 76), "修枝剪刃"))
    S.append(cyl(12, 60, "x", (sx - 30, TY - 700, 83), 10, "剪轴"))
    wx = 1920.0
    S.append(cyl(17, 880, "y", (wx, TY - 1000, 90), 14, "手拔草器杆"))
    S.append(box((190, 60, 60), (wx - 95, TY - 130, 70), "T 形握把"))
    for i in range(4):
        S.append(box((16, 130, 16), (wx - 40 + i * 24, TY - 1130, 66), "拔草爪"))

    items = [("①", "WORX 20V 大脚板电池 ×4，柜内轮充", BAT[2]),
             ("②", "电动打草机：轴 + 打草头 + 护罩", (tx, TY - 1340, 130)),
             ("③", "吹叶机 WU231.9，8.6～11.6 m³/min", (bx, TY - 432, 240)),
             ("④", "手拔 + 手动修枝剪，不吃电", (sx, TY - 930, 84)),
             ("⑤", "柜左半边：型材配件分箱（槽 6 / 8mm）", (210, -550, 600))]
    audit(items, S, -66, 23)
    print("saved", draw("0401-2", "WORX 20V 电池平台与割草四件套", items, S,
                        note="同一规格电池在打草机、吹叶机之间通用，之后添工具只买裸机；首批四件套够覆盖 0601 那条 100㎡ 长草地",
                        sig="设想 · 0401", az=-66, el=23, fov=27))


fig2()
