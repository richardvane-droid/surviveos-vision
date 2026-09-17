"""props — hand3d 的常用构件库：家具 / 电器 / 户外 / 结构。
所有尺寸单位 mm，pos 一律是构件包围盒的最小角（左-前-下）。
"""
import math
from hand3d import box, cyl, extrusion, Solid, _np
import numpy as np

# ---- 结构 ----
def wall(w, h, t=80, pos=(0, 0, 0), axis="x", name="墙"):
    """axis='x' 墙面沿 X 展开（法线 ±Y）；'y' 墙面沿 Y 展开（法线 ±X）"""
    x, y, z = pos
    s = box((w, t, h), (x, y, z), name) if axis == "x" else box((t, w, h), (x, y, z), name)
    s.shade = False
    return s

def floor(w, d, pos=(0, 0, 0), t=40, name="地面"):
    s = box((w, d, t), (pos[0], pos[1], pos[2]-t), name); s.shade = False; return s

def slab(w, d, t, pos, name="板"):
    return box((w, d, t), pos, name)

# ---- 家具 ----
def table(pos, w=1500, d=600, h=740, top=30, leg=50, name="桌"):
    x, y, z = pos
    o = [box((w, d, top), (x, y, z+h-top), name+"面")]
    for (dx, dy) in ((30, 30), (w-leg-30, 30), (30, d-leg-30), (w-leg-30, d-leg-30)):
        o.append(box((leg, leg, h-top), (x+dx, y+dy, z), name+"腿"))
    return o

def cabinet(pos, w, d, h, shelves=0, open_front=True, name="柜"):
    """开口朝 -Y 的柜体：两侧板 + 顶底板 + 背板（+ 层板）"""
    x, y, z = pos; t = 22
    o = [box((t, d, h), (x, y, z), name), box((t, d, h), (x+w-t, y, z), name),
         box((w, d, t), (x, y, z), name), box((w, d, t), (x, y, z+h-t), name),
         box((w, t, h), (x, y+d-t, z), name+"背板")]
    if not open_front: o.append(box((w, t, h), (x, y, z), name+"门"))
    for i in range(shelves):
        zz = z + (h-t) * (i+1)/(shelves+1)
        o.append(box((w-2*t, d-t, t), (x+t, y, zz), name+"层板"))
    return o

def drawer(pos, w, d, h, out=0, name="抽屉"):
    x, y, z = pos
    o = [box((w, d, h), (x, y-out, z), name),
         box((w+16, 26, h+16), (x-8, y-out-26, z-8), name+"面板")]
    o.append(cyl(9, 90, "x", (x+w/2-45, y-out-40, z+h/2), 10, "拉手"))
    return o

def shelf_run(pos, length, h, d=180, n=5, axis="x", name="书格"):
    """沿 axis 方向的连续格架"""
    x, y, z = pos; t = 24
    o = []
    for i in range(n+1):
        zz = z + (h-t)*i/n
        o.append(box((length, d, t), (x, y, zz), name) if axis == "x" else box((d, length, t), (x, y, zz), name))
    for i in (0, 1):
        if axis == "x":
            o.append(box((t, d, h), (x + i*(length-t), y, z), name+"立板"))
        else:
            o.append(box((d, t, h), (x, y + i*(length-t), z), name+"立板"))
    return o

def pegboard(pos, w, h, t=22, axis="x", name="洞洞板"):
    x, y, z = pos
    return [box((w, t, h), (x, y, z), name) if axis == "x" else box((t, w, h), (x, y, z), name)]

def stool(pos, r=160, h=680, name="凳"):
    x, y, z = pos
    o = [cyl(r, 40, "z", (x, y, z+h-40), 18, name+"面")]
    for i in range(3):
        a = i*2*math.pi/3
        o.append(cyl(16, h-40, "z", (x + math.cos(a)*r*0.62, y + math.sin(a)*r*0.62, z), 8, name+"腿"))
    return o

def bed_frame(pos, w=1200, d=2000, h=1750, name="架空床"):
    x, y, z = pos
    o = [box((w, d, 60), (x, y, z+h), name+"板")]
    for (dx, dy) in ((0, 0), (w-80, 0), (0, d-80), (w-80, d-80)):
        o.append(box((80, 80, h), (x+dx, y+dy, z), name+"柱"))
    return o

# ---- 电器 / 设备 ----
def screen(pos, w, h, t=45, tilt=0, name="屏"):
    x, y, z = pos
    return [box((w, t, h), (x, y, z), name), box((w*0.86, t*0.6, h*0.86), (x+w*0.07, y-2, z+h*0.07), name+"面")]

def monitor(pos, w=620, h=360, name="显示器"):
    x, y, z = pos
    return screen((x, y, z+180), w, h, 40, name=name) + [
        cyl(34, 180, "z", (x+w/2, y+20, z), 12, "立杆"), box((240, 180, 22), (x+w/2-120, y-70, z), "底座")]

def epaper(pos, w=170, h=120, name="墨水屏"):
    return screen(pos, w, h, 16, name=name)

def camera(pos, r=42, L=120, axis="y", name="摄像头"):
    x, y, z = pos
    return [cyl(r, L, axis, (x, y, z), 16, name), cyl(r*0.55, 16, axis, (x, y-16 if axis == "y" else y, z), 14, "镜")]

def sensor_box(pos, w=140, d=90, h=180, name="传感器盒"):
    x, y, z = pos
    return [box((w, d, h), (x, y, z), name), cyl(8, 40, "z", (x+w/2, y+d/2, z+h), 8, "天线")]

def motor(pos, s=42, L=48, axis="z", name="步进电机"):
    x, y, z = pos
    size = {"x": (L, s, s), "y": (s, L, s), "z": (s, s, L)}[axis]
    o = [box(size, (x, y, z), name)]
    o.append(cyl(5, 24, axis, (x+s/2, y+s/2, z+L) if axis == "z" else (x+L, y+s/2, z+s/2) if axis == "x" else (x+s/2, y+L, z+s/2), 10, "轴"))
    return o

def pump(pos, r=60, h=140, name="泵"):
    x, y, z = pos
    return [cyl(r, h, "z", (x, y, z), 16, name), cyl(18, 90, "y", (x, y, z+h*0.4), 12, "接口")]

def tank(pos, r, L, axis="y", name="水罐"):
    return [cyl(r, L, axis, pos, 24, name)]

def pipe(p0, p1, r=18, name="管"):
    p0, p1 = _np(p0), _np(p1); d = p1-p0; L = float(np.linalg.norm(d))
    if L < 1e-6: return []
    ax = int(np.argmax(np.abs(d))); axis = "xyz"[ax]
    return [cyl(r, L*np.sign(d[ax]), axis, tuple(p0), 14, name)]

def led_strip(p0, p1, w=14, name="灯带"):
    p0, p1 = _np(p0), _np(p1); d = p1-p0; L = float(np.linalg.norm(d))
    ax = int(np.argmax(np.abs(d)))
    size = [w, w, w]; size[ax] = abs(L)
    pos = list(np.minimum(p0, p1))
    return [box(tuple(size), tuple(pos), name)]

def solar_panel(pos, w=1650, d=1000, t=35, name="光伏板"):
    x, y, z = pos
    o = [box((w, d, t), (x, y, z), name)]
    for i in range(1, 4):
        o.append(box((w, 6, t+2), (x, y + d*i/4, z-1), "栅线"))
    return o

def battery_box(pos, w=520, d=320, h=280, name="电池箱"):
    x, y, z = pos
    return [box((w, d, h), (x, y, z), name), box((w*0.55, 12, h*0.3), (x+w*0.2, y-12, z+h*0.5), "面板")]

def stove(pos, w=560, d=440, h=680, name="铸铁炉"):
    x, y, z = pos
    o = [box((w, d, h), (x, y, z), name),
         box((w*0.62, 16, h*0.5), (x+w*0.19, y-16, z+h*0.26), "玻璃门"),
         box((w+120, d+100, 30), (x-60, y-50, z-30), "炉台")]
    for dx in (60, w-60):
        o.append(cyl(22, 140, "z", (x+dx, y+d/2, z-140), 10, "炉腿"))
    return o

def chimney(p0, h, r=80, name="烟囱"):
    x, y, z = p0
    return [cyl(r, h, "z", (x, y, z), 18, name), cyl(r*1.25, 60, "z", (x, y, z+h*0.35), 18, "保温段")]

def tent(pos, w=1200, d=1500, h=1200, name="帐篷"):
    x, y, z = pos
    apex = (x+w/2, y+d/2, z+h)
    corners = [(x, y, z), (x+w, y, z), (x+w, y+d, z), (x, y+d, z)]
    faces = [[corners[i], corners[(i+1) % 4], apex] for i in range(4)]
    edges = [(corners[i], corners[(i+1) % 4]) for i in range(4)] + [(c, apex) for c in corners]
    return [Solid([[f[0], f[1], f[2], f[2]] for f in faces], edges, name)]

def tree(pos, h=2600, r=110, crown=900, name="树"):
    x, y, z = pos
    o = [cyl(r, h*0.6, "z", (x, y, z), 12, name+"干")]
    for i in range(3):
        rr = crown*(0.75 + 0.12*i)/2
        o.append(cyl(rr, 140, "z", (x, y, z + h*0.55 + i*180), 18, name+"冠"))
    return o

def pot(pos, r=180, h=220, name="陶盆"):
    x, y, z = pos
    return [cyl(r, h, "z", (x, y, z), 20, name), cyl(r*1.08, 26, "z", (x, y, z+h-26), 20, "口沿")]

def rack(pos, w, d, h, levels=4, name="货架", post=30):
    x, y, z = pos
    o = []
    for (dx, dy) in ((0, 0), (w-post, 0), (0, d-post), (w-post, d-post)):
        o.append(extrusion(h, "z", (x+dx, y+dy, z), post, name+"立柱"))
    for i in range(levels):
        zz = z + (h-24) * i/(levels-1)
        o.append(box((w, d, 24), (x, y, zz), name+"层板"))
    return o

def pegs(board_pos, w, h, nx=8, nz=4, axis="x", r=6):
    """洞洞板挂钩阵列（画成小圆柱）"""
    x, y, z = board_pos
    o = []
    for i in range(nx):
        for j in range(nz):
            px = x + w*(i+0.5)/nx
            pz = z + h*(j+0.5)/nz
            o.append(cyl(r, 40, "y", (px, y-40, pz), 8, "挂钩"))
    return o
