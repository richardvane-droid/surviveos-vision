"""0305-1 Voron 2.4 机架与运动系统 · 爆炸图（hand3d）"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hand3d import *

W, H = 1200, 900
S = 20; B = 250                      # 型材 20mm，行程 250
L = B + 4*S                          # 外框边长 ≈330
E = 130                              # 爆炸间距

def frame(z0=0):
    o = []
    for z in (z0, z0 + L - S):
        o += [extrusion(L, "x", (0, 0, z)), extrusion(L, "x", (0, L-S, z)),
              extrusion(L-2*S, "y", (0, S, z)), extrusion(L-2*S, "y", (L-S, S, z))]
    for (x, y) in ((0,0),(L-S,0),(0,L-S),(L-S,L-S)):
        o.append(extrusion(L-2*S, "z", (x, y, z0+S)))
    return o

def bed(z):
    o = [box((B, B, 6), ((L-B)/2, (L-B)/2, z), "热床"),
         box((B-20, B-20, 4), ((L-B)/2+10, (L-B)/2+10, z-6), "床板")]
    for (x, y) in ((S+14, S+14), (L-S-14, S+14), (S+14, L-S-14), (L-S-14, L-S-14)):
        o.append(cyl(4, 150, "z", (x, y, z-150), 12, "丝杠"))
    return o

def gantry(z):
    o = [extrusion(L-2*S, "x", (S, L/2-S/2, z), name="X 梁"),
         extrusion(L-2*S, "y", (S, S, z+S), name="Y 梁 A"),
         extrusion(L-2*S, "y", (L-2*S, S, z+S), name="Y 梁 B")]
    for (x, y) in ((S, S), (L-2*S, S), (S, L-2*S), (L-2*S, L-2*S)):
        o.append(box((42, 42, 40), (x-11, y-11, z+S+S), "电机"))
    return o

def head(z):
    return [box((70, 58, 62), (L/2-35, L/2-29, z), "打印头"),
            cyl(7, 26, "z", (L/2, L/2, z-26), 14, "喷嘴", cap=True)]

def panels(dx):
    t = 3
    return [box((t, L, L), (-E-dx, 0, 0), "侧板"), box((t, L, L), (L+E+dx-t, 0, 0), "侧板")]

def main():
    ZB, ZG, ZH = 470, 640, 800          # 爆炸后各层的高度
    sol = []
    grp = {}
    grp["frame"] = frame(0)
    grp["bed"] = [s.moved((0, 0, ZB-170)) for s in bed(170)]
    grp["gantry"] = [s.moved((0, 0, ZG-(L-3*S))) for s in gantry(L-3*S)]
    grp["head"] = [s.moved((0, 0, ZH-(L-6*S))) for s in head(L-6*S)]
    grp["panel"] = panels(120)
    for k in ("panel", "frame", "bed", "gantry", "head"): sol += grp[k]

    cam = Cam(eye=(1750, -2050, 1500), target=(L/2, L/2, 400), fov=27, W=W, H=H)
    pen, Z = render_parts(cam, sol, W, H, seed=13, lw_edge=2.1, lw_sil=3.6, hatch_step=7)
    img = compose(pen.img, W, H, 3)

    anchors = {
        "frame": (L/2, 0, L*0.35), "bed": (L*0.28, L/2, ZB+3),
        "gantry": (L*0.75, L/2-S/2, ZG+S), "head": (L/2, L/2, ZH+30),
        "panel": (L+120-3, L*0.55, 140),
    }
    items = [(1, anchors["frame"], (232, 712)),
             (2, anchors["bed"],   (214, 470)),
             (3, anchors["gantry"],(980, 330)),
             (4, anchors["head"],  (690, 172)),
             (5, anchors["panel"], (1070, 610))]
    img = leaders_and_nums(img, cam, items, r=14)
    img = sheet(img, "Voron 2.4 机架与运动系统 · 爆炸图",
                [("①", "2020/3030 铝型材骨架，边长约 330"),
                 ("②", "四丝杠同步升降热床 250×250"),
                 ("③", "CoreXY 龙门：X 梁 + 双 Y 梁 + 四电机"),
                 ("④", "打印头与喷嘴，行程 250×250×250"),
                 ("⑤", "封闭腔体板材，腔温 50℃ 以上")],
                "自建 · 按官方 BOM 自己配件自己拧，结构件 ABS 打印 100+ 件", "设想 · 0305", W, H)
    os.makedirs("parts3d", exist_ok=True)
    img.save("parts3d/0305-1.png")
    print("saved parts3d/0305-1.png", img.size)

main()
