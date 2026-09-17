"""把 parts3d/ 的合成 PNG 转成「墨色 + 透明」的轻量 PNG，放进 parts/。
纸纹交给页面背景，图里只留笔触，体积从 ~1.1MB 降到 ~70KB。
"""
import numpy as np, glob, os, sys
from PIL import Image
PAPER, INK, Q = 247.0, 58.0, 16
src = sys.argv[1] if len(sys.argv) > 1 else "parts3d"
dst = sys.argv[2] if len(sys.argv) > 2 else "parts"
tot = 0
for p in sorted(glob.glob(os.path.join(src, "*.png"))):
    g = np.asarray(Image.open(p).convert("L"), float)
    a = np.clip((PAPER - g) / (PAPER - INK), 0, 1)
    a[a < 0.07] = 0
    aa = ((a * 255).astype(np.uint8) // Q * Q).astype(np.uint8)
    la = np.zeros((*a.shape, 2), np.uint8); la[..., 0] = 61; la[..., 1] = aa
    o = os.path.join(dst, os.path.basename(p))
    Image.fromarray(la, "LA").save(o, optimize=True)
    tot += os.path.getsize(o)
print(f"{len(glob.glob(os.path.join(src,'*.png')))} 张 -> {dst}/  合计 {tot/1e6:.1f} MB")
