"""0103 电子画框墙 — 两张硬件爆炸图（hand3d 管线）
0103-1 九屏胡桃木画框总成 / 0103-2 iPad 常供电改装件
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import box, cyl
from props import wall
from partdraw import draw
from p01util import merge, audit

FW, FH = 1200, 900          # 外框 120×90cm
SX, SZ = 916, 700           # 九屏区 92×70
BX, BZ = 142, 100           # 左右边框 / 上下边框
Z0 = 1500                   # 底边 1500（吧台电器顶）
PW, PH = 300, 228           # 单台 iPad Pro 12.9 的画面块
G = 8                       # 隔屏间距 8mm


# ---------------------------------------------------------------- 0103-1
def fig1():
    YB, YW, YG, YS, YF = -3, -300, -600, -900, -1220
    E = 175                                   # 外框四条边各自往外拉开
    SP = 70                                   # 九屏在自己这层摊开，露出背后的格栅
    S = []                                    # 不建墙：墙一大就把总成压没了，用理线槽交代墙面

    # ⑤ 3mm 铝背板 + 明装理线槽（线不进墙）
    S.append(box((FW, 3, FH), (0, YB, Z0), "3mm 铝背板"))
    S.append(box((76, 46, 470), (880, -86, 990), "明装理线槽"))
    S.append(box((84, 54, 26), (876, -90, 1452), "槽口盖"))

    # ④ Lightning 线束 + 多口 USB-A 充电头（从框下沿引出）
    cab = []
    for i in range(9):
        x = 190 + i * 102
        cab.append(cyl(6, -330, "z", (x, YW, Z0 + 60), 8, "Lightning 尾线"))
    cab.append(cyl(15, 1110, "x", (-140, YW, 1160), 10, "线束"))
    S.append(merge(cab, "Lightning 线束"))
    S.append(box((210, 82, 56), (-350, YW - 41, 1090), "多口 USB-A 充电头"))
    for i in range(4):
        S.append(box((30, 12, 11), (-332 + i * 46, YW - 53, 1116), "USB-A 口"))

    # ③ 隔屏格栅：外圈与外框同尺寸 + 8mm 内格条
    gr = [box((FW, 14, BZ), (0, YG, Z0 + FH - BZ), "隔屏格栅"),
          box((FW, 14, BZ), (0, YG, Z0), "隔屏格栅"),
          box((BX, 14, SZ), (0, YG, Z0 + BZ), "隔屏格栅"),
          box((BX, 14, SZ), (FW - BX, YG, Z0 + BZ), "隔屏格栅")]
    for k in (1, 2):
        gr.append(box((G, 14, SZ), (BX + k * PW + (k - 1) * G, YG, Z0 + BZ), "8mm 格条"))
        gr.append(box((SX, 14, G), (BX, YG, Z0 + BZ + k * PH + (k - 1) * G), "8mm 格条"))
    S.append(merge(gr, "隔屏格栅"))

    # ② 九块 iPad Pro 12.9（本层摊开 70，实装是 8）
    for r in range(3):
        for c in range(3):
            x = FW / 2 + (c - 1) * (PW + SP) - PW / 2
            z = Z0 + FH / 2 + (r - 1) * (PH + SP) - PH / 2
            S.append(box((PW, 11, PH), (x, YS, z), "iPad 屏幕"))
            S.append(box((PW - 26, 4, PH - 26), (x + 13, YS - 4, z + 13), "画面"))

    # ① 胡桃木外框四条边往外拉开 + 框下凸台
    S += [box((FW, 76, BZ), (0, YF, Z0 + FH - BZ + E), "胡桃木外框"),
          box((FW, 76, BZ), (0, YF, Z0 - E), "胡桃木外框"),
          box((BX, 76, SZ), (-E, YF, Z0 + BZ), "胡桃木外框"),
          box((BX, 76, SZ), (FW - BX + E, YF, Z0 + BZ), "胡桃木外框"),
          box((FW, 116, 44), (0, YF - 40, Z0 - E - 44), "框下凸台 4cm")]

    items = [("①", "胡桃木外框 120×90cm，宽边框", (-E + 70, YF, 1950)),
             ("②", "九台 iPad Pro 12.9 拼 3×3，屏区 92×70", (600, YS - 4, 1950)),
             ("③", "隔屏格栅把屏幕间距压到 8mm", (34, YG, 1950)),
             ("④", "Lightning 线束汇到多口 USB-A 充电头", (-250, YW - 41, 1118)),
             ("⑤", "3mm 铝背板，线从框下沿进明装理线槽", (918, -86, 1090))]
    audit(items, S, -44, 18)
    p = draw("0103-1", "九屏胡桃木画框总成", items, S,
             note="北墙西段吧台上方：底边 1500 压着电器顶、顶边到梁底 2400；单台连框 713g，两点吊挂",
             sig="设想 · 0103", az=-44, el=18, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0103-2
def fig2():
    IW, ID = 306, 221                 # iPad Pro 12.9 一代
    DX, DZ = 128, 178                 # 爆炸：每层往 +X 挪一点、往上抬一层
    def L(k, x=0, y=0, z=0):
        return (x + k * DX, y, z + k * DZ)

    S = []
    # 0 铝背板（画框那层）
    x, y, z = L(0, -33, -30, 0)
    S.append(box((372, 282, 3), (x, y, z), "3mm 铝背板"))
    # 1 导热硅胶垫 2mm
    x, y, z = L(1, 76, 62, 0)
    S.append(box((152, 96, 3), (x, y, z), "导热硅胶垫"))
    # 2 iPad 后壳（电池已拆）
    x, y, z = L(2)
    sh = [box((IW, ID, 2), (x, y, z), "iPad 后壳"),
          box((IW, 6, 11), (x, y, z + 2), "后壳边"), box((IW, 6, 11), (x, y + ID - 6, z + 2), "后壳边"),
          box((6, ID, 11), (x, y, z + 2), "后壳边"), box((6, ID, 11), (x + IW - 6, y, z + 2), "后壳边"),
          box((158, 102, 2), (x + 74, y + 60, z + 2), "空出来的电池位")]
    S.append(merge(sh, "iPad 后壳"))
    # 3 电池替换板
    x, y, z = L(3, 77, 63)
    S.append(box((150, 94, 5), (x, y, z), "电池替换板"))
    for (dx, dy, w, d) in ((14, 16, 30, 22), (58, 14, 26, 18), (98, 20, 34, 26), (30, 58, 42, 20)):
        S.append(box((w, d, 8), (x + dx, y + dy, z + 5), "板上元件"))
    S.append(box((20, 11, 10), (x + 122, y + 42, z + 5), "电池插座"))
    # 4 Lightning 尾线
    x, y, z = L(4, 150, 96)
    S += [box((16, 10, 7), (x, y, z), "Lightning 头"),
          cyl(5, -170, "y", (x + 8, y, z + 3), 10, "尾线"),
          cyl(5, 230, "x", (x + 8, y - 170, z + 3), 10, "尾线"),
          box((30, 16, 11), (x + 232, y - 178, z - 2), "接多口充电头")]
    # 5 原屏幕总成
    x, y, z = L(5)
    S += [box((IW, ID, 6), (x, y, z), "原屏幕总成"),
          box((IW - 26, ID - 26, 3), (x + 13, y + 13, z + 6), "显示面")]

    items = [("①", "原屏幕总成回装，引导式访问锁屏", L(5, 150, 110, 8)),
             ("②", "Lightning 尾线，9 条汇到多口充电头", L(4, 158, 30, 3)),
             ("③", "电池替换板 3.8V，带电量模拟", L(3, 130, 100, 2)),
             ("④", "导热硅胶垫 2mm，把热传给铝背板", L(1, 152, 110, 3)),
             ("⑤", "iPad 后壳：电池拆掉，半年不鼓包", L(2, 40, 110, 2))]
    audit(items, S, -52, 28)
    p = draw("0103-2", "iPad 常供电改装件", items, S,
             note="九台平板一块电池都没有，断电重启也能开机；一代机是 Lightning 口，和别处的 Type-C 分开采购",
             sig="设想 · 0103", az=-52, el=28, fov=27)
    print("saved", p)


fig1()
fig2()
