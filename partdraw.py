"""partdraw — 一次调用画一张拆解图 PNG（hand3d + props）。

用法：
    from partdraw import draw
    draw("0305-1", "Voron 2.4 机架与运动系统",
         [("①","2020 骨架", 三维锚点), ...],
         solids, note="...", az=-55, el=24)
图例与编号共用一份数据：每项 (编号, 说明文字, 锚点)；编号圈的屏幕位置自动排布到左右页边。
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from hand3d import (Cam, fit_cam, render_parts, compose, sheet, leaders_and_nums, all_pts)
from PIL import Image

W, H = 1200, 900
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "parts3d")

def _auto_slots(cam, items, W, H, top=0.24, bot=0.90, mx=0.055):
    """编号圈排到左右页边：先按投影 x 均分左右（保持两边数量平衡），再按投影 y 定槽位"""
    pr = [(n, t, cam.proj(a)[0]) for n, t, a in items]
    order = sorted(range(len(pr)), key=lambda i: pr[i][2][0])
    half = (len(pr) + 1) // 2
    side = {}
    for rank, i in enumerate(order):
        side[i] = "L" if rank < half else "R"
    out = []
    for sd in ("L", "R"):
        grp = sorted([i for i in range(len(pr)) if side[i] == sd], key=lambda i: pr[i][2][1])
        m = len(grp)
        for j, i in enumerate(grp):
            y = H*top + (H*bot - H*top) * ((j+0.5)/m if m > 1 else 0.5)
            x = W*mx if sd == "L" else W*(1-mx)
            out.append((i, (x, y)))
    out.sort(key=lambda r: r[0])
    return [(pr[i][0], pr[i][1], xy) for i, xy in out]

def draw(pid, title, items, solids, note="", sig=None, az=-55, el=24, fov=27,
         rect=(0.05, 0.22, 0.96, 0.91), seed=None, hatch_step=8, lw_edge=1.95, lw_sil=3.3,
         cam=None, slots=None, suffix="爆炸图"):
    seed = seed if seed is not None else (abs(hash(pid)) % 97)
    cam = cam or fit_cam(solids, W, H, rect=rect, az=az, el=el, fov=fov)
    pen, Z = render_parts(cam, solids, W, H, seed=seed, lw_edge=lw_edge, lw_sil=lw_sil, hatch_step=hatch_step)
    img = compose(pen.img, W, H, seed)
    placed = slots or _auto_slots(cam, items, W, H)
    img = leaders_and_nums(img, cam, [(n, a, xy) for (n, _, a), (_, _, xy) in zip(items, placed)], r=14)
    legend = [(n, t) for n, t, _ in items]
    img = sheet(img, f"{title} · {suffix}", legend, note, sig or f"设想 · {pid.split('-')[0]}", W, H)
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, pid + ".png")
    img.save(p, optimize=True)
    return p
