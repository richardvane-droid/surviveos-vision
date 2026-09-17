"""0208 大柏林音响 — 硬件爆炸图
0208-1 落地音箱单元总成 / 0208-2 黑胶唱盘总成
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import box, cyl, Solid
from partdraw import draw
from p01util import merge, rot, prism, audit, screw

BW, BD, BH = 340, 400, 1200        # 箱体：高约 1.2m


def driver(cx, cz, y, r, depth, nm):
    """喇叭单元：盆架环 + 锥盆 + 磁钢"""
    o = [cyl(r, 26, "y", (cx, y, cz), 24, nm),
         cyl(r * .80, -depth * .45, "y", (cx, y, cz), 20, nm + "锥盆"),
         cyl(r * .30, 16, "y", (cx, y - depth * .45, cz), 16, "防尘帽"),
         cyl(r * .52, depth * .55, "y", (cx, y + 26, cz), 18, "磁钢")]
    for i in range(6):
        a = i * math.pi / 3
        o.append(box((22, 14, 22), (cx + math.cos(a) * r * .9 - 11, y - 8, cz + math.sin(a) * r * .9 - 11), "螺钉耳"))
    return merge(o, nm)


# ---------------------------------------------------------------- 0208-1
def fig1():
    S = []
    fl = box((BW + 420, BD + 420, 40), (-230, -210, -740), "地面"); fl.shade = False; S.append(fl)

    # ① 箱体：多层板五面（前面敞开）+ 加强筋 + 吸音棉
    cab = [box((22, BD, BH), (0, 0, 0), "多层板箱体"), box((22, BD, BH), (BW - 22, 0, 0), "多层板箱体"),
           box((BW, 22, BH), (0, BD - 22, 0), "多层板箱体"), box((BW, BD, 22), (0, 0, 0), "多层板箱体"),
           box((BW, BD, 22), (0, 0, BH - 22), "多层板箱体")]
    S.append(merge(cab, "多层板箱体"))
    for zz in (420, 880):
        S.append(box((BW - 44, BD - 44, 26), (22, 0, zz), "加强筋"))
        S.append(cyl(70, 26, "z", (BW / 2, BD * .5, zz), 18, "筋上开孔"))
    for dx in (24, BW - 44):
        S.append(box((20, BD - 60, BH - 120), (dx, 20, 60), "吸音棉"))
    S.append(box((BW - 60, 20, BH - 140), (30, BD - 46, 70), "吸音棉"))

    # ④ 三个单元（往 -Y 爆炸）
    YD = -680
    S.append(driver(BW / 2, 330, YD, 150, 180, "12 寸低音"))
    S.append(driver(BW / 2, 830, YD, 66, 90, "中音单元"))
    hn = [cyl(52, 70, "y", (BW / 2, YD + 60, 1030), 18, "压缩驱动器"),
          cyl(40, 40, "y", (BW / 2, YD + 20, 1030), 18, "号角高音")]
    for k, rr in enumerate((46, 58, 74, 94, 118)):
        hn.append(cyl(rr, -24, "y", (BW / 2, YD + 20 - k * 24, 1030), 20, "号角"))
    S.append(merge(hn, "号角高音"))

    # ⑤ 磁吸前网罩
    YG = -1280
    gr = [box((BW, 26, 60), (0, YG, 0), "前网罩"), box((BW, 26, 60), (0, YG, BH - 60), "前网罩"),
          box((40, 26, BH), (0, YG, 0), "前网罩"), box((40, 26, BH), (BW - 40, YG, 0), "前网罩")]
    for i in range(38):
        gr.append(box((BW - 80, 6, 2), (40, YG + 11, 78 + i * 28), "网布"))
    S.append(merge(gr, "磁吸前网罩"))
    for dz in (80, BH - 110):
        for dx in (14, BW - 40):
            S.append(cyl(13, 26, "y", (dx + 13, YG + 26, dz), 12, "磁吸点"))

    # ③ 分频器（从箱底往 -Y 抽出、平放）
    YX, ZX = -820, -150
    S.append(box((260, 320, 16), (40, YX, ZX), "分频器"))
    for (dx, dy, r) in ((70, 80, 46), (180, 90, 34)):
        S.append(cyl(r, 62, "z", (40 + dx, YX + dy, ZX + 16), 14, "电感"))
    for i in range(4):
        S.append(cyl(22, 78, "z", (78 + i * 54, YX + 240, ZX + 16), 12, "电容"))
    S.append(box((200, 10, 4), (70, YX + 160, ZX + 16), "接线铜箔"))

    # ② 花岗岩底板 + 钉脚 ×4（往下爆炸）
    S.append(box((BW + 90, BD + 80, 44), (-45, -40, -420), "花岗岩底板"))
    for dx, dy in ((20, 20), (BW + 30, 20), (20, BD + 10), (BW + 30, BD + 10)):
        S.append(cyl(32, 46, "z", (dx - 45 + 25, dy - 40 + 25, -640), 12, "钉脚"))
        S.append(cyl(24, -58, "z", (dx - 45 + 25, dy - 40 + 25, -640), 4, "钉尖"))

    items = [("①", "多层板箱体 + 加强筋 + 吸音棉", (BW, BD * .5, BH * .60)),
             ("②", "花岗岩底板 + 钉脚，隔开地面", (BW + 45, BD * .5, -400)),
             ("③", "分频器约 500Hz / 3kHz 分两处", (110, YX + 80, ZX + 78)),
             ("④", "12 寸低音 + 中音 + 号角高音", (BW / 2 + 150, YD, 330)),
             ("⑤", "磁吸前网罩，防灰也防手", (BW, YG + 9, 600))]
    audit(items, S, -46, 16)
    p = draw("0208-1", "落地音箱单元总成", items, S,
             note="两只大箱贴南墙分列 98 寸电视两侧、间距 ≈2.6m；单只 60kg 以上，灵敏度 90dB 以上，低频偏厚要靠房间校正压回去",
             sig="设想 · 0208", az=-46, el=16, fov=27)
    print("saved", p)


# ---------------------------------------------------------------- 0208-2
def fig2():
    S = []
    PW, PD = 440, 370
    sh = box((900, 700, 30), (-230, -170, -560), "矮机柜层板"); sh.shade = False; S.append(sh)

    # ④ 避震板 + 锥形脚三点支撑
    for (dx, dy) in ((60, 60), (PW - 60, 60), (PW / 2, PD - 50)):
        S.append(cyl(34, 44, "z", (dx, dy, -450), 12, "锥形脚"))
        S.append(cyl(18, 40, "z", (dx, dy, -406), 12, "锥尖"))
    S.append(box((PW + 40, PD + 40, 30), (-20, -20, -300), "避震板"))

    # ① 实木底座 + 同步电机 + 皮带 + 副盘
    S.append(box((PW, PD, 110), (0, 0, -140), "实木底座"))
    S.append(box((PW - 40, PD - 40, 10), (20, 20, -30), "底座面板"))
    S.append(cyl(44, 90, "z", (78, PD - 90, -128), 16, "同步电机"))
    S.append(cyl(22, 30, "z", (78, PD - 90, -38), 12, "电机皮带轮"))
    S.append(box((60, 26, 34), (48, PD - 60, -100), "33⅓ / 45 转拨杆"))
    SPX, SPY = PW * .52, PD * .48
    S.append(cyl(62, 44, "z", (SPX, SPY, 100), 20, "副盘"))
    S.append(cyl(9, 150, "z", (SPX, SPY, 100), 10, "主轴"))
    # 皮带：两段直线 + 包住副盘的薄环
    S.append(cyl(64, 16, "z", (SPX, SPY, 112), 22, "皮带"))
    for sgn in (-1, 1):
        S.append(box((abs(SPX - 78), 6, 16), (min(78, SPX), SPY + sgn * 62, 112), "皮带"))

    # ② 铝合金转盘 + 橡胶唱片垫 + 唱片
    S.append(cyl(150, 40, "z", (SPX, SPY, 300), 30, "铝合金转盘"))
    for i in range(10):
        a = i * math.pi / 5
        S.append(box((30, 12, 40), (SPX + math.cos(a) * 130 - 15, SPY + math.sin(a) * 130 - 6, 300), "配重槽"))
    S.append(cyl(147, 10, "z", (SPX, SPY, 440), 30, "橡胶唱片垫"))
    S.append(cyl(150, 3, "z", (SPX, SPY, 540), 30, "唱片"))
    S.append(cyl(46, 4, "z", (SPX, SPY, 543), 20, "标签"))

    # ③ 9 寸直臂 + MM 唱头 + 配重（往 +X 爆炸）
    AX, AY, AZ = PW + 250, PD - 90, 150
    S.append(cyl(30, 110, "z", (AX, AY, AZ), 16, "唱臂座"))
    S.append(cyl(20, 60, "z", (AX, AY, AZ + 110), 14, "升降座"))
    arm = cyl(9, -230, "x", (AX, AY, AZ + 150), 12, "9 寸直臂")
    S.append(arm)
    S.append(box((46, 26, 34), (AX - 246, AY - 13, AZ + 116), "MM 唱头"))
    S.append(box((10, 6, 18), (AX - 250, AY - 3, AZ + 100), "唱针"))
    S.append(cyl(26, 70, "x", (AX + 30, AY, AZ + 150), 14, "配重"))
    S.append(cyl(9, 40, "x", (AX, AY, AZ + 150), 10, "臂管"))

    # ⑤ 亚克力防尘罩
    ZC = 760
    ct = [box((PW + 60, 12, 210), (-30, -20, ZC), "防尘罩"), box((PW + 60, 12, 210), (-30, PD + 8, ZC), "防尘罩"),
          box((12, PD + 28, 210), (-30, -20, ZC), "防尘罩"), box((12, PD + 28, 210), (PW + 18, -20, ZC), "防尘罩"),
          box((PW + 60, PD + 28, 12), (-30, -20, ZC + 210), "罩顶")]
    S.append(merge(ct, "亚克力防尘罩"))
    for dx in (60, PW - 40):
        S.append(cyl(14, 50, "x", (dx, PD + 14, ZC + 200), 12, "合页"))

    items = [("①", "皮带传动，电机藏在底座内", (SPX + 64, SPY, 118)),
             ("②", "铝合金转盘 2kg 以上，惯量稳速", (SPX + 150, SPY, 320)),
             ("③", "9 寸直臂 + MM 唱头，针压 1.8g", (AX - 246, AY - 13, AZ + 140)),
             ("④", "避震板 + 锥形脚三点支撑", (PW + 20, PD * .5, -285)),
             ("⑤", "亚克力防尘罩，合页开启", (PW / 2, -20, ZC + 120))]
    audit(items, S, -52, 24)
    p = draw("0208-2", "黑胶唱盘总成", items, S,
             note="放在电视下方 ≈220×40 的矮机柜里；皮带像一根软弹簧把电机的抖动滤掉，转盘的重量本身就是稳转速的飞轮",
             sig="设想 · 0208", az=-52, el=24, fov=27)
    print("saved", p)


fig1(); fig2()
