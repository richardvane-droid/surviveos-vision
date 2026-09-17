"""0209-2 写字台与连续书格 · 爆炸图（hand3d）"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import *
W, H = 1200, 900
RW, RD, RH = 1500, 2000, 1700           # 密室 1.5×2m、净高 1700

def desk(pos, w=1500, d=600, h=740):
    x, y, z = pos
    o = [box((w, d, 30), (x, y, z+h-30), "台面")]
    for (dx, dy) in ((40, 40), (w-80, 40), (40, d-80), (w-80, d-80)):
        o.append(box((40, 40, h-30), (x+dx, y+dy, z), "腿"))
    return o

def main():
    sol = []
    # 地面与两面墙（只作背景，不参与排线）
    for b in (box((RW, RD, 40), (0, 0, -40), "地面"),
              box((40, RD, RH), (-40, 0, 0), "西墙"),
              box((RW, 40, RH), (0, RD, 0), "北墙")):
        b.shade = False; sol.append(b)
    # 连续浅书格（西墙，拉出 -X 爆炸）
    sol += shelf_run((-520, 180, 300), 26+1500, 1050, 180, 5, "连续书格")
    # 写字台（北端，往 +Y 外拉）
    sol += desk((120, RD - 600 + 430, 0))
    # 人体工学椅
    sol += chair((870, RD - 1180, 0))
    # 台角瓷银茶器
    sol.append(cyl(72, 120, "z", (1420, RD - 130, 740), 18, "茶壶"))
    sol.append(cyl(36, 52, "z", (1300, RD - 90, 740), 14, "茶杯"))
    sol.append(box((260, 190, 14), (1240, RD - 230, 740), "毛毡托盘"))
    # 尽端铁皮宝箱
    sol.append(box((420, 300, 260), (-460, 250, 300), "铁皮宝箱"))

    cam = fit_cam(sol, W, H, rect=(0.06, 0.20, 0.96, 0.90), az=-58, el=22, fov=27)
    pen, Z = render_parts(cam, sol, W, H, seed=31, lw_edge=1.9, lw_sil=3.3, hatch_step=8)
    img = compose(pen.img, W, H, 7)
    items = [(1, (300, RD - 140, 745), (300, 300)),
             (2, (870, RD - 1180, 560), (960, 330)),
             (3, (-200, 700, 900), (180, 520)),
             (4, (1380, RD - 130, 800), (1060, 620)),
             (5, (-250, 400, 430), (250, 790))]
    img = leaders_and_nums(img, cam, items, r=14)
    img = sheet(img, "写字台与连续书格 · 爆炸图",
                [("①", "1.5m 标准写字台，台面 740"),
                 ("②", "人体工学椅，总高 ≤1300，抬头不顶床板"),
                 ("③", "西侧长墙连续浅书格，进深 180，五格"),
                 ("④", "台角明放瓷银茶器（毛毡托盘）"),
                 ("⑤", "书格尽端一格：铁皮宝箱")],
                "密室 1.5×2m、净高 1700；坐直了还剩一大截", "设想 · 0209", W, H)
    img.save("parts3d/0209-2.png"); print("saved 0209-2")
main()
