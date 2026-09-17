"""0803 miniduck — 两张硬件爆炸图（hand3d 管线）
0803-1 双足鸭身总成 / 0803-2 头部感知与表情模组

一只 25cm 高、约 800g 的双足电子鸭。单位 mm，Z=0 是地面，鸭子面朝 -Y（相机一侧）。
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import Solid, box, cyl
from partdraw import draw
from p56util import (merge, rot, mv, prism, path_tube, seg_tube, arc_pts, cone,
                     audit, capped_cyl, disc)

SV = (26.0, 15.0, 24.0)          # 总线舵机外形


def servo(pos, name="总线舵机"):
    x, y, z = pos
    w, d, h = SV
    return merge([box((w, d, h), (x, y, z), name),
                  box((w + 12, d, 5), (x - 6, y, z + h * 0.62), name + "耳"),
                  capped_cyl(5.5, 4, "y", (x + w * 0.28, y - 4, z + h * 0.5), 10, name + "输出轴")],
                 name)


def vshell(r, t, h, pos, a0, a1, n=14, name="壳"):
    """竖直方向的一段圆筒壳（做鸭身的前/后半壳）。"""
    sec = [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
           for a in np.linspace(a0, a1, n)]
    sec += [((r - t) * math.cos(math.radians(a)), (r - t) * math.sin(math.radians(a)))
            for a in np.linspace(a1, a0, n)]
    return prism(sec, h, "z", pos, name)


def duck_head(pos, s=1.0, name="头壳"):
    """鸭头：一个蛋形壳 + 扁扁的喙。"""
    x, y, z = pos
    o = [cone(20 * s, 30 * s, 20 * s, (x, y, z), 16, name),
         cyl(30 * s, 20 * s, "z", (x, y, z + 20 * s), 16, name),
         cone(30 * s, 14 * s, 18 * s, (x, y, z + 40 * s), 16, name),
         disc(14 * s, (x, y, z + 58 * s), "z", 16, name)]
    bill = prism([(0, 0), (-40 * s, 6 * s), (-40 * s, -6 * s)], 34 * s, "x",
                 (x - 17 * s, y, z + 26 * s), "鸭喙")
    o.append(bill)
    return o


# ---------------------------------------------------------------- 0803-1
def fig1():
    S = []
    fl = box((470, 380, 16), (-215, -200, -16), "地面"); fl.shade = False
    S.append(fl)

    # ---- 左腿：装好的状态（脚 → 踝 → 小腿 → 膝 → 大腿 → 髋）
    def leg(x0, spread=0.0, tag=""):
        o = []
        z = 0.0
        o.append(box((62, 42, 6), (x0 - 31, -24, 0), "脚底 TPU 防滑垫"))
        o.append(box((58, 38, 10), (x0 - 29, -22, 6), "PETG 脚板"))
        z = 16 + spread * 0
        o.append(servo((x0 - 13, -8, z), "踝舵机"))
        z2 = z + 24 + spread
        o.append(box((18, 16, 30), (x0 - 9, -7, z2), "小腿 PETG"))
        z3 = z2 + 30 + spread
        o.append(servo((x0 - 13, -8, z3), "膝舵机"))
        z4 = z3 + 24 + spread
        o.append(box((20, 18, 24), (x0 - 10, -8, z4), "大腿 PETG"))
        z5 = z4 + 24 + spread
        o.append(servo((x0 - 13, -8, z5), "髋舵机 pitch"))
        z6 = z5 + 24 + spread
        o.append(servo((x0 - 13, -8, z6), "髋舵机 roll"))
        return o, z6 + 24

    L, _ = leg(-34)
    S += L
    R, _ = leg(150, 16.0)       # 右腿整条拉到一边，并把五个舵机拉开
    S += R

    # ---- ① 总线舵机共 15 个：颈 3（在身体上方）
    NZ = 214.0
    for k in range(3):
        S.append(servo((-13, -8, NZ + k * 26), "颈舵机"))

    # ---- 身体：后半壳留在原位，前半壳沿 -Y 拉出
    BZ, BR = 116.0, 46.0
    S.append(vshell(BR, 4, 96, (0, 0, BZ), 14, 168, 14, "PETG 后壳"))
    S.append(vshell(BR, 4, 96, (0, -150, BZ), -166, -12, 14, "PETG 前壳"))
    S.append(cone(30, BR, 22, (0, 0, BZ - 22), 18, "PETG 腹壳"))

    # ---- ② 主控 RK3566 + IMU / ③ 3S 锂电 / ④ 无线充电线圈（沿 -Y 依次拉出）
    S.append(box((58, 34, 20), (-29, -76, 128), "3S 锂电 2000mAh"))
    S.append(box((26, 8, 10), (-13, -84, 138), "电池接头"))
    S.append(box((56, 38, 6), (-28, -76, 172), "RK3566 主控板"))
    S.append(box((14, 12, 4), (-7, -70, 178), "IMU"))
    for i in range(4):
        S.append(box((5, 8, 5), (-24 + i * 14, -78, 178), "排针"))
    S.append(capped_cyl(24, 5, "y", (0, -230, 150), 20, "无线充电接收线圈"))
    S.append(disc(24, (0, -230, 150), "y", 20, "无线充电接收线圈"))
    for k in range(3):
        S.append(cyl(24 - k * 6, 3, "y", (0, -226 + k, 150), 20, "线圈"))

    # 翅膀（两片小曲壳，让它一眼看出来是鸭）
    S.append(vshell(54, 5, 52, (0, 0, 140), -74, 6, 10, "PETG 翅膀"))
    S.append(vshell(54, 5, 52, (0, 0, 140), 174, 254, 10, "PETG 翅膀"))

    # ---- 头（细节在 0803-2），整体抬高
    S += duck_head((0, -4, 296), 1.15)

    items = [("①", "总线舵机 ×15：腿 2×5、颈 3、头 2", (150, -8, 28)),
             ("②", "RK3566 主控 + IMU，50Hz 控制环", (0, -76, 178)),
             ("③", "3S 锂电 2000mAh，续航约 90 分钟", (0, -76, 138)),
             ("④", "胸腔无线充电接收线圈", (0, -232, 150)),
             ("⑤", "PETG 外壳 + 脚底 TPU 防滑垫", (-34, -24, 3))]
    audit(items, S, -62, 12)
    print("saved", draw("0803-1", "双足鸭身总成", items, S,
                        note="25cm 高、约 800g 的双足小鸭：重物尽量压低，重心低了才站得稳；外壳用 0305 的 Voron 打印 PETG",
                        sig="设想 · 0803", az=-62, el=12, fov=27))


# ---------------------------------------------------------------- 0803-2
def fig2():
    """头部放大到 3 倍画，沿 +Z 拆开；胸口圆屏单独摆在一边。"""
    S = []
    s = 3.0

    # ⑤ 颈部 2 个头部舵机（俯仰 + 转头）
    S.append(servo((-13 * s / 1.6, -8, 0), "头部舵机 pitch"))
    S.append(servo((-13 * s / 1.6, -8, 40), "头部舵机 yaw"))
    S.append(box((30, 26, 22), (-15, -13, 80), "颈部连接件"))

    # ④ ESP32-S3 语音协处理器（小智固件）
    S.append(box((92, 66, 8), (140, -30, 110), "ESP32-S3 语音协处理器"))
    S.append(box((30, 18, 10), (150, -22, 118), "屏蔽罩"))
    for i in range(6):
        S.append(box((6, 10, 5), (150 + i * 13, -36, 114), "串口排针"))
    S.append(path_tube([(146, -10, 114), (60, -10, 114), (10, -10, 104)], 5, 6, "串口线"))

    # 头壳（下段）+ ② 广角摄像头 + ③ 眼睛 RGB LED + 鸭喙
    HZ = 140.0
    S.append(cone(20 * s / 1.5, 30 * s / 1.5, 20, (0, 0, HZ), 18, "PETG 头壳"))
    S.append(cyl(30 * s / 1.5, 46, "z", (0, 0, HZ + 20), 18, "PETG 头壳"))
    S.append(prism([(0, 0), (-92, 13), (-92, -13)], 76, "x", (-38, -6, HZ + 38), "鸭喙"))
    S.append(capped_cyl(9, 16, "y", (0, -62, HZ + 68), 14, "广角摄像头 120°"))
    S.append(disc(9, (0, -62, HZ + 68), "y", 14, "广角摄像头 120°"))
    for dx in (-30.0, 30.0):
        S.append(capped_cyl(10, 14, "y", (dx, -54, HZ + 52), 14, "眼睛 RGB LED"))
        S.append(disc(10, (dx, -54, HZ + 52), "y", 14, "眼睛 RGB LED"))

    # ① 4 麦环形阵列 + 泡棉隔震（沿 +Z 拆开）
    FZ = HZ + 150
    S.append(cyl(54, 14, "z", (0, 0, FZ), 20, "泡棉隔震环"))
    S.append(disc(54, (0, 0, FZ + 14), "z", 20, "泡棉隔震环"))
    MZ = FZ + 90
    S.append(cyl(56, 6, "z", (0, 0, MZ), 20, "4 麦环形阵列板"))
    S.append(disc(56, (0, 0, MZ + 6), "z", 20, "4 麦环形阵列板"))
    for i in range(4):
        a = i * math.pi / 2 + math.pi / 4
        S.append(capped_cyl(8, 10, "z", (math.cos(a) * 36, math.sin(a) * 36, MZ + 6), 12, "驻极体麦克风"))
    # 顶盖
    S.append(cone(56, 22, 34, (0, 0, MZ + 110), 18, "PETG 顶盖"))
    S.append(disc(22, (0, 0, MZ + 144), "z", 18, "PETG 顶盖"))

    # ⑤ 胸口 1.28 寸圆屏（表情 / 数据窗），摆在头部旁边
    DX, DY, DZ = -250.0, -40.0, 120.0
    S.append(capped_cyl(48, 18, "y", (DX, DY, DZ), 22, "1.28 寸圆屏"))
    S.append(disc(48, (DX, DY, DZ), "y", 22, "1.28 寸圆屏"))
    S.append(cyl(40, 4, "y", (DX, DY - 4, DZ), 22, "显示区"))
    S.append(disc(40, (DX, DY - 4, DZ), "y", 22, "显示区"))
    for dx, dz in ((-16, 12), (16, 12)):
        S.append(box((10, 4, 16), (DX + dx - 5, DY - 8, DZ + dz), "表情"))
    S.append(box((34, 4, 8), (DX - 17, DY - 8, DZ - 22), "表情"))

    items = [("①", "4 麦环形阵列 + 泡棉隔震，本地唤醒", (0, 0, MZ + 6)),
             ("②", "广角摄像头 120°，认窝也认人", (0, -62, HZ + 68)),
             ("③", "眼睛 RGB LED ×2，情绪跟 HA 联动", (-30, -54, HZ + 52)),
             ("④", "ESP32-S3 跑 xiaozhi，串口接主控", (186, -30, 114)),
             ("⑤", "胸口 1.28 寸圆屏显示表情 / 数据", (DX, DY - 8, DZ))]
    audit(items, S, -64, 14)
    print("saved", draw("0803-2", "头部感知与表情模组", items, S,
                        note="头是鸭子和人打交道的地方：麦阵离舵机远并垫泡棉隔震，语音单独交给 ESP32-S3，主控只管走路和表情",
                        sig="设想 · 0803", az=-64, el=14, fov=27))


if __name__ == "__main__":
    fig1(); fig2()
