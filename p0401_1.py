"""0401-1 北墙三区工具墙 · 爆炸图（hand3d）"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import *
W, H = 1200, 900
WALLW, WALLH = 3500, 2060

def main():
    sol = []
    # 墙体
    wall = box((WALLW, 80, WALLH), (0, 0, 0), "北墙"); wall.shade = False
    sol.append(wall)
    CB_H, CB_D = 900, 420
    OUT = 520                                   # 爆炸方向：各层沿 -Y 拉出
    # 下区功能柜（拉出 OUT*0.5）
    cy0 = -CB_D - OUT*0.5
    sol.append(box((2600, CB_D, CB_H), (350, cy0, 0), "功能柜"))
    for i in range(4):
        sol.append(box((150, 150, 200), (470 + i*190, cy0 + 40, 520), "电池位"))
    for i in range(2):
        sol.append(box((700, CB_D - 60, 250), (1400 + i*760, cy0 + 20, 140), "分箱抽屉"))
    sol.append(box((980, CB_D + 220, 80), (470, cy0 - 220, 20), "接屑盘"))
    # 中区洞洞板（拉出 OUT*1.15）
    PB_W, PB_H, PB_Z = 3000, 760, CB_H + 190
    py = -22 - OUT*1.15
    sol.append(box((PB_W, 22, PB_H), (250, py, PB_Z), "胡桃色洞洞板"))
    # 板上工具（往外再拉一点，挂在板前）
    ty = py - 150
    tools = (hammer((620, ty, PB_Z + 300), 300) + wrench((900, ty, PB_Z + 300))
             + plier((1150, ty, PB_Z + 330)) + driver((1400, ty, PB_Z + 320))
             + tape((1700, ty, PB_Z + 430)) + hammer((2000, ty, PB_Z + 290), 270)
             + wrench((2300, ty, PB_Z + 300)) + driver((2600, ty, PB_Z + 320)))
    sol += tools
    # 上区导轨与长杆（拉出 OUT*1.7）
    RZ = PB_Z + PB_H + 240
    ry = -30 - OUT*1.7
    sol.append(extrusion(3100, "x", (200, ry, RZ), 30, "铝导轨"))
    sol.append(cyl(17, 2500, "x", (420, ry - 90, RZ - 90), 12, "长杆 A"))
    sol.append(cyl(15, 2100, "x", (520, ry - 170, RZ - 180), 12, "长杆 B"))
    sol.append(box((300, 60, 130), (420, ry - 120, RZ - 320), "高枝剪头"))

    cam = fit_cam(sol, W, H, rect=(0.05, 0.20, 0.97, 0.91), az=-74, el=19, fov=26)
    pen, Z = render_parts(cam, sol, W, H, seed=21, lw_edge=1.9, lw_sil=3.3, hatch_step=8)
    img = compose(pen.img, W, H, 5)
    items = [(1, (1700, ry, RZ + 15), (700, 196)),
             (2, (900, py, PB_Z + PB_H - 40), (196, 330)),
             (3, (2300, ty, PB_Z + 330), (1090, 372)),
             (4, (520, cy0 + 40, 620), (170, 560)),
             (5, (1750, cy0 + 20, 265), (860, 800))]
    img = leaders_and_nums(img, cam, items, r=14)
    img = sheet(img, "北墙三区工具墙 · 爆炸图",
                [("①", "上区：铝导轨挂长杆工具与高枝剪"),
                 ("②", "中区：胡桃色洞洞板 3.0m，悬空 20mm"),
                 ("③", "工具按四类挂位，背后是黄铜影子轮廓"),
                 ("④", "下区功能柜：WORX 20V 电池充电位 ×4"),
                 ("⑤", "型材配件分箱（槽 6mm / 槽 8mm）+ 可抽接屑盘")],
                "北墙 3.5m 宽、2060 净高；墙不是一次装满的，空位留给后面的模块", "设想 · 0401", W, H)
    img.save("parts3d/0401-1.png"); print("saved 0401-1")
main()
