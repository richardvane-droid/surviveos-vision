# -*- coding: utf-8 -*-
"""重绘 0401 过道工具间的插图与拆解图（对齐 ALIGN_0009 的新文案）。

新口径：北墙竖向三区（上区铝导轨长杆 / 中区胡桃色洞洞板 + 黄铜影子轮廓 / 下区功能柜）、
WORX 20V 大脚板统一电池平台、首批割草四件套、0805 型材配件分箱。
画风沿用 sk.py / redraw_08.py / redraw_09.py 的既有手法，只换里面的图形与标注。
用法：cd /home/claude/vision && python3 redraw_0401.py
"""
from sk import *
from redraw_08 import SH, along, finish, flow, poster
from redraw_09 import ex


# ============================ 工具剪影（返回 path 的 d） ============================
def d_hammer(x, y):
    return f"M{x-9} {y} h18 v8 h-6 v21 h-6 v-21 h-6 Z"

def d_driver(x, y):
    return f"M{x-3.5} {y} h7 v13 h2 v4 h-2 v12 h-7 v-12 h-2 v-4 h2 Z"

def d_spanner(x, y):
    return (f"M{x-5} {y} q5 -3 10 0 q0 6 -3.5 7 v11 q3.5 1 3.5 7 q-5 3 -10 0 "
            f"q0 -6 3.5 -7 v-11 q-3.5 -1 -3.5 -7 Z")

def d_plier(x, y):
    return (f"M{x-6} {y} l3 11 l-1 15 h-4 l-1 -15 Z "
            f"M{x+6} {y} l-3 11 l1 15 h4 l1 -15 Z")

def d_knife(x, y):
    return f"M{x} {y} h20 l6 4 l-6 4 h-20 Z"

def d_saw(x, y):
    return (f"M{x} {y} l36 5 l-3 10 l-33 -5 Z "
            f"M{x} {y-2} l-7 -1 q-6 2 -5 8 l4 6 l8 1 Z")

def d_tape(x, y):
    return f"M{x-9} {y} q0 -4 4 -4 h11 q4 0 4 4 v12 q0 4 -4 4 h-11 q-4 0 -4 -4 Z"

def d_square(x, y):
    return f"M{x} {y} h5 v16 h15 v5 h-20 Z"

def d_pruner(x, y):
    return (f"M{x-5} {y} q8 4 10 11 l-3 3 q-6 -6 -10 -12 Z "
            f"M{x+7} {y} q-8 4 -10 11 l3 3 q6 -6 10 -12 Z")

def d_trimmer(x, y, h=32):
    """打草机：上端电池 / 电机块，中间杆，下端打草盘。y 为电机块顶。"""
    return (f"M{x-9} {y} h18 v13 h-18 Z "
            f"M{x-3} {y+13} h6 v{h} h-6 Z "
            f"M{x-10} {y+13+h} h20 v7 h-20 Z")

def d_blower(x, y):
    """吹叶机：机身 + 手柄 + 出风筒。y 为机身顶。"""
    return (f"M{x} {y} h14 q6 0 6 6 v9 q0 6 -6 6 h-14 q-6 0 -6 -6 v-9 q0 -6 6 -6 Z "
            f"M{x+20} {y+7} h16 v7 h-16 Z "
            f"M{x+2} {y+21} h7 l2 9 h-8 Z")

def d_batt(x, y):
    """WORX 20V 大脚板电池：窄身 + 宽脚板。y 为顶。"""
    return f"M{x-7} {y} h14 v14 h4 v8 h-22 v-8 h4 Z"


def shadow(d, cx, cy, H, k=1.18, sw=0.55):
    """黄铜影子轮廓：放大一圈的浅色描边 + 排线填充的轮廓本体。"""
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) scale({k}) '
            f'translate({-cx:.1f} {-cy:.1f})"><path d="{d}" stroke-width="{sw}"/></g>'
            f'<path d="{d}" fill="{H}" stroke-width="0.7"/>')


def pair(dfun, x, y, H, *args):
    """影子（右下偏移 3.5）+ 工具本体（白底遮挡）。"""
    ds = dfun(x + 3.5, y + 3.5, *args)
    dt = dfun(x, y, *args)
    return shadow(ds, x + 3.5, y + 3.5, H) + f'<path d="{dt}" fill="#fff" stroke-width="1.3"/>'


def only_shadow(dfun, x, y, H, *args):
    d = dfun(x, y, *args)
    return shadow(d, x, y, H)


# ================================== illo 0401 ==================================
def m0401():
    """北墙工具墙正视 + 一点点进深：上区导轨长杆、中区胡桃洞洞板黄铜影子、下区功能柜。"""
    pfx = "m0401"
    H = f"url(#{pfx}-hatch)"; H2 = f"url(#{pfx}-hatch2)"; HL = f"url(#{pfx}-hatchl)"
    DOT = f"url(#{pfx}-dots)"
    B = []

    # ---------- 房间外壳：北墙正视 + 两侧墙向观者收进来（一点点进深）----------
    B.append('<path d="M40 24 H360 V248 H40 Z" stroke-width="1.6"/>')
    B.append('<path d="M40 24 L14 14 M360 24 L386 14 M40 248 L14 272 M360 248 L386 272" stroke-width="1.2"/>')
    B.append('<path d="M14 14 V272 M386 14 V272" stroke-width="1.1"/>')
    B.append('<path d="M14 272 H386" stroke-width="1.6"/>')
    B.append(f'<path d="M40 24 L14 14 V34 L40 40 Z" fill="{HL}" stroke="none"/>')
    B.append(f'<path d="M360 24 L386 14 V34 L360 40 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M14 90 L40 94 M14 170 L40 172 M386 90 L360 94 M386 170 L360 172" stroke-width="0.3"/>')
    # 地面板缝
    for x0, x1 in ((40, 22), (140, 132), (260, 252), (360, 378)):
        B.append(f'<path d="M{x0} 248 L{x1} 272" stroke-width="0.4"/>')
    B.append('<path d="M14 260 H386" stroke-width="0.35"/>')
    B.append('<path d="M40 24 H360" stroke-width="1.2"/>')

    # ---------- 上区：横向铝导轨 + 长杆工具 ----------
    B.append('<path d="M56 28 H344 V36 H56 Z" stroke-width="1.4"/>')
    B.append('<path d="M56 32 H344" stroke-width="0.5"/>')
    B.append('<path d="M54 36 H346 L340 40 H60 Z" stroke-width="0.9"/>')
    B.append(f'<path d="M60 36 H340 V39 H60 Z" fill="{H}" stroke="none"/>')
    for x in (74, 130, 186, 224):
        B.append(f'<path d="M{x} 40 v3 q0 4 4 4" stroke-width="1"/>')
    # 长杆 1：高枝剪（杆头在左，朝楼梯口对齐）
    B.append('<path d="M62 45 h166 v4 h-166 Z" stroke-width="1.3"/>')
    B.append('<path d="M62 46 l-11 -5 M62 48 l-11 5 M51 41 l-4 -1 M51 53 l-4 1" stroke-width="1.2"/>')
    B.append('<circle cx="60" cy="47" r="1.6" stroke-width="0.9"/>')
    B.append('<path d="M228 47 h8" stroke-width="1"/>')
    # 长杆 2：伸缩杆（两节套管）
    B.append('<path d="M62 54 h94 v4 h-94 Z M156 55 h74 v2 h-74 Z" stroke-width="1.2"/>')
    B.append('<path d="M150 53 h10 v6 h-10 Z" stroke-width="0.9"/>')
    # 长杆 3：撑杆刷
    B.append('<path d="M64 62 h148" stroke-width="1"/>')
    B.append('<path d="M52 60 h12 v4 h-12 Z M52 60 l-6 -2 M52 64 l-6 2" stroke-width="0.9"/>')
    for i in range(7):
        B.append(f'<path d="M{53+i*1.6} 60 v-3" stroke-width="0.4"/>')

    # ---------- 三区之间的木压条 ----------
    B.append('<path d="M50 66 H350 V69 H50 Z" stroke-width="1.1"/>')
    B.append(f'<path d="M50 66 H350 V67.4 H50 Z" fill="{H}" stroke="none"/>')

    # ---------- 中区：胡桃色洞洞板 ----------
    B.append('<path d="M348 74 V148 H60 L56 144 H344 V74 Z" fill="#fff" stroke="none"/>')
    B.append(f'<path d="M348 74 V148 H60 L56 144 H344 V74 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M344 70 l4 4 V148 H60 l-4 -4" stroke-width="0.8"/>')
    B.append('<path d="M56 70 H344 V144 H56 Z" fill="#fff" stroke="none"/>')
    B.append(f'<path d="M56 70 H344 V144 H56 Z" fill="{DOT}" stroke="none"/>')
    B.append('<path d="M56 70 H344 V144 H56 Z" stroke-width="1.6"/>')
    for y in (77, 93, 111, 129, 140):
        B.append(f'<path d="M58 {y} q70 -2.5 144 0 q70 2.5 142 0" stroke-width="0.32"/>')
    for x in (129, 199, 263):
        B.append(f'<path d="M{x} 72 V142" stroke-width="0.6" stroke-dasharray="3 3"/>')

    # ---------- 中区工具 + 黄铜影子轮廓 ----------
    # A 敲击紧固（左半留空，给伸过来的手让路）
    B.append(pair(d_driver, 70, 82, H))
    B.append(pair(d_spanner, 96, 82, H))
    B.append(only_shadow(d_driver, 118, 82, H))
    B.append(only_shadow(d_hammer, 112, 112, H))
    # B 切割修整
    B.append(pair(d_plier, 146, 88, H))
    B.append(pair(d_knife, 162, 94, H))
    B.append(pair(d_saw, 142, 120, H))
    B.append(only_shadow(d_pruner, 188, 120, H))
    # C 测量画线（下排全空）
    B.append(pair(d_tape, 218, 90, H))
    B.append(pair(d_square, 238, 88, H))
    B.append(only_shadow(d_tape, 212, 120, H))
    # D WORX 电动
    B.append(pair(d_trimmer, 282, 82, H, 28))
    B.append('<path d="M270 130 q12 9 24 0" stroke-width="0.9"/>')
    B.append('<path d="M284 100 h7 q4 0 4 4 v3" stroke-width="1"/>')
    B.append('<path d="M275 134 l-3 5 M281 135 l-1 6 M288 134 l3 5" stroke-width="0.5"/>')
    B.append(pair(d_blower, 302, 88, H))
    B.append(only_shadow(d_batt, 308, 120, H))
    B.append(only_shadow(d_batt, 330, 120, H))
    # 荧光绿底黑字标签（黑白稿里用密排线表示荧光底色）
    for lx, ly, lw in ((272, 134, 20), (322, 106, 20)):
        B.append(f'<path d="M{lx} {ly} h{lw} v6 h-{lw} Z" stroke-width="0.9"/>')
        B.append(f'<path d="M{lx+1} {ly+1} h{lw-2} v4 h-{lw-2} Z" fill="{H2}" stroke="none"/>')

    # ---------- 下区：落地功能柜 ----------
    B.append('<path d="M48 147 H352 V248 H48 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M48 152 H352 L344 147 H56 Z" stroke-width="1.3"/>')
    B.append(f'<path d="M48 152 H352 L344 147 H56 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M48 152 H352 V248 H48 Z" stroke-width="1.6"/>')
    B.append('<path d="M160 152 V244 M256 152 V244" stroke-width="1.2"/>')
    B.append('<path d="M52 242 H348 V248 H52 Z" stroke-width="1"/>')
    B.append(f'<path d="M52 242 H348 V248 H52 Z" fill="{H}" stroke="none"/>')
    # 左格：一排电池充电位，两块 20V 大脚板电池在充电
    B.append('<path d="M54 214 H156" stroke-width="1.1"/>')
    for dx in (58, 84, 110, 136):
        B.append(f'<path d="M{dx} 214 v-6 h20 v6" stroke-width="0.9"/>')
        B.append(f'<path d="M{dx+6} 208 h8 v-3 h-8 Z" stroke-width="0.7"/>')
    for dx in (84, 110):
        B.append(f'<path d="{d_batt(dx+10, 184)}" fill="#fff" stroke="none"/>')
        B.append(f'<path d="{d_batt(dx+10, 184)}" stroke-width="1.3"/>')
        B.append(f'<path d="M{dx+5} 189 h10 M{dx+5} 193 h10" stroke-width="0.5"/>')
        B.append(f'<circle cx="{dx+10}" cy="203" r="1.6" stroke-width="0.8"/>')
        B.append(f'<path d="M{dx+14} 200 l4 -2 M{dx+14} 204 l4 1" stroke-width="0.5"/>')
    B.append('<path d="M54 224 H156 M54 234 H156" stroke-width="0.3"/>')
    # 中格：两只分开的型材配件抽屉
    B.append('<path d="M166 158 H250 V198 H166 Z M166 202 H250 V242 H166 Z" stroke-width="1.3"/>')
    B.append('<path d="M196 194 H220 M196 238 H220" stroke-width="1.6"/>')
    B.append('<path d="M176 166 H240 V186 H176 Z M176 210 H240 V230 H176 Z" stroke-width="0.9"/>')
    B.append(f'<path d="M176 166 H240 V169 H176 Z M176 210 H240 V213 H176 Z" fill="{H}" stroke="none"/>')
    # 右格：接屑盘抽出（上方留白给后面的模块）
    B.append('<path d="M262 196 H346 V214 H262 Z" stroke-width="1.1"/>')
    B.append(f'<path d="M264 198 H344 V212 H264 Z" fill="{H2}" stroke="none"/>')
    B.append('<path d="M262 158 H346" stroke-width="0.9"/>')
    B.append('<path d="M266 206 H336 L346 222 H258 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M266 206 H336 L346 222 H258 Z" stroke-width="1.4"/>')
    B.append('<path d="M258 222 H346 V234 H258 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M258 222 H346 V234 H258 Z" stroke-width="1.4"/>')
    B.append('<path d="M290 228 H314" stroke-width="1.6"/>')
    B.append(f'<path d="M258 230 H346 V234 H258 Z" fill="{H}" stroke="none"/>')
    for cx, cy in ((284, 212), (300, 216), (316, 211), (328, 215), (292, 218)):
        B.append(f'<path d="M{cx} {cy} l4 -2 M{cx+2} {cy+2} l3 1" stroke-width="0.45"/>')

    # ---------- 人：背对着站在墙前，伸手把扳手挂回轮廓里 ----------
    B.append('<path d="M6 272 V138 L11 114 Q30 104 49 114 L54 138 V272 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M6 272 V138 L11 114 Q30 104 49 114 L54 138 V272" stroke-width="1.6"/>')
    B.append('<circle cx="30" cy="84" r="13" fill="#fff" stroke-width="1.6"/>')
    B.append('<path d="M30 97 V108" stroke-width="1.1"/>')
    B.append('<path d="M21 74 q9 -7 18 0" stroke-width="0.7"/>')
    B.append('<path d="M6 196 H54" stroke-width="1.1"/>')
    B.append('<path d="M30 196 V272 M10 266 h14 M36 266 h14" stroke-width="1"/>')
    # 伸出去的手臂
    B.append('<path d="M52 126 L82 124 L84 134 L52 138 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M52 126 L82 124 L84 134 L52 138" stroke-width="1.5"/>')
    # 手里的锤子 + 一道虚线箭头：正要挂回右边那个空轮廓
    B.append(f'<path d="{d_hammer(86, 112)}" fill="#fff" stroke="none"/>')
    B.append(f'<path d="{d_hammer(86, 112)}" stroke-width="1.3"/>')
    B.append('<circle cx="87" cy="131" r="5.5" stroke-width="1.3"/>')
    B.append('<path d="M83 128 h8 M83 132 h8" stroke-width="0.6"/>')
    B.append('<path d="M97 126 H103" stroke-width="0.7" stroke-dasharray="2 2"/>')
    B.append('<path d="M101 123.5 l4 2.5 l-4 2.5" stroke-width="0.8"/>')

    # ---------- 右侧三段尺寸链（带引线）----------
    B.append('<path d="M360 24 H381 M360 69 H381 M360 152 H381 M360 248 H381" stroke-width="0.4"/>')
    B.append('<path d="M372 24 V40 M372 58 V69 M372 69 V98 M372 116 V152 M372 152 V190 M372 208 V248" stroke-width="0.6"/>')
    B.append('<path d="M369 29 l3 -5 l3 5 M369 64 l3 5 l3 -5 M369 74 l3 -5 l3 5 '
             'M369 147 l3 5 l3 -5 M369 157 l3 -5 l3 5 M369 243 l3 5 l3 -5" stroke-width="0.6"/>')

    body = "\n".join(B)
    labels = "\n".join([
        label(372, 52, "400", 6.5, "middle"),
        label(372, 110, "760", 6.5, "middle"),
        label(372, 203, "900", 6.5, "middle"),
        label(292, 46, "上区 · 横向铝导轨", 7, "middle"),
        label(292, 58, "杆头朝楼梯口对齐", 7, "middle"),
        label(93, 80, "敲击紧固", 6.5, "middle"),
        label(164, 80, "切割修整", 6.5, "middle"),
        label(231, 80, "测量画线", 6.5, "middle"),
        label(303, 78, "WORX · 荧光绿黑字标签", 6.5, "middle"),
        label(243, 120, "黄铜影子", 6.5, "middle"),
        label(243, 130, "外加浅色描边", 6.5, "middle"),
        label(105, 168, "20V 大脚板充电位", 6.5, "middle"),
        label(105, 178, "电池全屋共用", 6.5, "middle"),
        label(208, 175, "20 系列", 6.5, "middle"),
        label(208, 184, "槽 6mm", 6.5, "middle"),
        label(208, 219, "30 / 40 系列", 6.5, "middle"),
        label(208, 228, "槽 8mm", 6.5, "middle"),
        label(304, 176, "空着 · 留给后面模块", 6.5, "middle"),
        label(302, 258, "可抽出接屑盘", 7, "middle"),
        label(150, 258, "工具跟着模块分批上墙", 7, "middle"),
        label(200, 286, "北墙竖向三区：上区吊长杆 · 中区胡桃色洞洞板加黄铜影子 · 下区功能柜",
              9.5, "middle", "#1c1c1c"),
    ])
    extra = (f'<pattern id="{pfx}-dots" width="11" height="11" patternUnits="userSpaceOnUse">'
             f'<circle cx="5.5" cy="5.5" r="0.62" fill="#1c1c1c"/></pattern>')
    return illo(pfx, body, "0401", extra_defs=extra, seed=31).replace("</svg>", labels + "\n</svg>")


# ============================= parts/0401-1 三区工具墙 =============================
def p0401_1():
    pfx = "p0401-1"; S = SH(pfx)

    def panel(x, y, w, h, sw=1.5):
        return f'<path d="M{x} {y} l{w} {-0.305*w:.1f} v{h} l{-w} {0.305*w:.1f} Z" stroke-width="{sw}"/>'

    def dots(x, y, w, h, cols, rows):
        p = []
        for r in range(rows):
            for c in range(cols):
                px = x + 8 + c * (w - 16) / (cols - 1)
                py = y - 0.305 * (px - x) + 7 + r * (h - 14) / (rows - 1)
                p.append(f"M{px:.1f} {py:.1f} v0.5")
        return '<path d="' + " ".join(p) + '" stroke-width="1.05"/>'

    def i0(x, y):   # 1 背板龙骨框
        s = panel(x - 54, y + 4, 74, 30)
        s += f'<path d="M{x-45} {y+3} l56 -17 v18 l-56 17 Z" stroke-width="0.8"/>'
        s += f'<path d="M{x-30} {y-1.5} v24 M{x-10} {y-7.6} v24 M{x+10} {y-13.7} v24" stroke-width="0.8"/>'
        s += f'<path d="M{x+20} {y-16.6} l5 2 v30 l-5 -2 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x+20} {y-16.6} l5 2 v30 l-5 -2" stroke-width="0.9"/>'
        return s

    def i1(x, y):   # 2 下区功能柜
        s = f'<path d="M{x-52} {y+6} l72 -22 v30 l-72 22 Z" stroke-width="1.5"/>'
        s += f'<path d="M{x+20} {y-16} l6 3 v30 l-6 -3" stroke-width="1"/>'
        s += f'<path d="M{x+20} {y-16} l6 3 v30 l-6 -3 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x-28} {y-1.4} v30 M{x-4} {y-8.7} v30" stroke-width="0.9"/>'
        # 充电位（左格）
        s += f'<path d="M{x-46} {y+8} l14 -4 M{x-46} {y+13} l14 -4" stroke-width="0.6"/>'
        s += f'<path d="M{x-44} {y+4} l5 -1.5 v-7 l-5 1.5 Z M{x-36} {y+1.6} l5 -1.5 v-7 l-5 1.5 Z" stroke-width="0.9"/>'
        # 抽屉（中格）
        s += f'<path d="M{x-24} {y-2.6} l16 -5 v8 l-16 5 Z M{x-24} {y+7.4} l16 -5 v8 l-16 5 Z" stroke-width="0.9"/>'
        # 接屑盘（右格，抽出）
        s += f'<path d="M{x+2} {y+2} l16 -5 l6 3 l-16 5 Z" stroke-width="1.1"/>'
        s += f'<path d="M{x+2} {y+2} v5 l6 3 v-5 M{x+24} {y} v5 l-16 5 v-5" stroke-width="0.8"/>'
        return s

    def i2(x, y):   # 3 中区胡桃色洞洞板
        s = panel(x - 54, y + 4, 76, 34)
        s += dots(x - 54, y + 4, 76, 34, 7, 5)
        s += f'<path d="M{x+22} {y-19.2} l4 2 v34 l-4 -2 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x+22} {y-19.2} l4 2 v34 l-4 -2" stroke-width="0.9"/>'
        # 木纹
        s += (f'<path d="M{x-48} {y+9} q20 -8 38 -12 q20 -4 30 -7 '
              f'M{x-48} {y+20} q20 -8 38 -12 q20 -4 30 -7" stroke-width="0.35"/>')
        return s

    def i3(x, y):   # 4 黄铜影子贴片 + 浅色描边
        s = f'<path d="M{x-46} {y+2} l64 -20 v12 l-64 20 Z" stroke-width="1"/>'
        H = S
        s += shadow(d_hammer(x - 30, y - 16), x - 30, y - 16, H, 1.2)
        s += shadow(d_spanner(x - 2, y - 24), x - 2, y - 24, H, 1.2)
        s += f'<path d="M{x+12} {y-30} l16 -5" stroke-width="0.6" stroke-dasharray="2 2"/>'
        return s

    def i4(x, y):   # 5 挂钩与工具
        s = f'<path d="M{x-48} {y+8} h9 v12 h-9 Z M{x-39} {y+11} h10 q6 0 6 6 v4" stroke-width="1.2"/>'
        s += f'<path d="M{x-48} {y+8} h9 v12 h-9 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="{d_hammer(x-24, y+2)}" stroke-width="1.4"/>'
        s += f'<path d="{d_spanner(x-2, y-6)}" stroke-width="1.4"/>'
        s += f'<path d="{d_tape(x+18, y-12)}" stroke-width="1.4"/>'
        return s

    def i5(x, y):   # 6 上区铝导轨 + 长杆
        s = f'<path d="M{x-40} {y-6} h96 v7 h-96 Z" stroke-width="1.4"/>'
        s += f'<path d="M{x-40} {y+1} h96 v3 h-96 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x-34} {y+4} v4 q0 4 4 4 M{x+6} {y+4} v4 q0 4 4 4" stroke-width="1"/>'
        s += f'<path d="M{x-30} {y+12} h80 v3 h-80 Z" stroke-width="1.2"/>'
        s += f'<path d="M{x-30} {y+13} l-11 -5 M{x-30} {y+15} l-11 5 M{x-41} {y+8} l-4 -1" stroke-width="1.2"/>'
        s += f'<path d="M{x-24} {y+21} h66" stroke-width="1"/>'
        return s

    legend = [(1, "背板龙骨框（垫 20mm，留挂钩空腔）"),
              (2, "下区功能柜：充电位 · 配件分箱 · 接屑盘"),
              (3, "中区胡桃色洞洞板（孔距 25mm）"),
              (4, "黄铜影子贴片 + 一圈浅色描边"),
              (5, "挂钩与工具，按四类分区上墙"),
              (6, "上区横向铝导轨 + 长杆工具 / 高枝剪")]
    leaders = [(-30, 14), (-30, 6), (-30, 6), (-30, -4), (-26, -14), (-20, 2)]
    return ex(pfx, "北墙三区工具墙", "0401-1", 3, legend,
              "重的常用的落在肩腰之间，长的少用的抬上头顶，带电的脏的收进柜子",
              [i0, i1, i2, i3, i4, i5], leaders)


# ======================= parts/0401-2 WORX 平台与割草四件套 =======================
def p0401_2():
    pfx = "p0401-2"; S = SH(pfx)

    def i0(x, y):   # 1 柜内充电位排
        s = f'<path d="M{x-52} {y+4} l70 -21 v18 l-70 21 Z" stroke-width="1.5"/>'
        s += f'<path d="M{x+18} {y-17} l6 3 v18 l-6 -3" stroke-width="1"/>'
        s += f'<path d="M{x+18} {y-17} l6 3 v18 l-6 -3 Z" fill="{S}" stroke="none"/>'
        for i in range(4):
            bx = x - 46 + i * 15
            s += f'<path d="M{bx} {y+2-i*4.6} l11 -3.4 v-7 l-11 3.4 Z" stroke-width="0.9"/>'
            s += f'<path d="M{bx+3} {y-3.4-i*4.6} l5 -1.6" stroke-width="0.6"/>'
        s += f'<path d="M{x-52} {y+16} l70 -21" stroke-width="0.5"/>'
        return s

    def i1(x, y):   # 2 20V 大脚板电池 ×2
        out = ""
        for dx, dy in ((-38, 12), (-2, -8)):
            bx, by = x + dx, y + dy - 30
            out += f'<path d="M{bx-10} {by} h20 v20 h6 v12 h-32 v-12 h6 Z" stroke-width="1.5"/>'
            out += f'<path d="M{bx-7} {by+6} h14 M{bx-7} {by+12} h14" stroke-width="0.6"/>'
            out += f'<path d="M{bx-16} {by+20} h32 v4 h-32 Z" fill="{S}" stroke="none"/>'
            out += f'<circle cx="{bx}" cy="{by+26}" r="2.2" stroke-width="0.9"/>'
            out += f'<path d="M{bx+5} {by+24} l6 -2 M{bx+5} {by+29} l6 2" stroke-width="0.6"/>'
        return out

    def i2(x, y):   # 3 电动打草机
        s = f'<path d="{d_trimmer(x-18, y-34, 34)}" stroke-width="1.4"/>'
        s += f'<path d="M{x-27} {y-34} h18 v4 h-18 Z" fill="{S}" stroke="none"/>'
        s += f'<circle cx="{x-18}" cy="{y+14}" r="11" stroke-width="1.2"/>'
        s += f'<path d="M{x-29} {y+14} a11 11 0 0 0 22 0" stroke-width="0.8"/>'
        s += f'<path d="M{x-18} {y+3} v8 M{x-26} {y+18} l-5 4 M{x-10} {y+18} l5 4" stroke-width="0.7"/>'
        s += f'<path d="M{x-14} {y-14} h12 q5 0 5 5 v4" stroke-width="1.2"/>'  # 握把
        return s

    def i3(x, y):   # 4 手动修枝剪
        s = f'<path d="M{x-30} {y-26} q20 6 28 18 l-5 6 q-10 -14 -26 -18 Z" stroke-width="1.5"/>'
        s += f'<path d="M{x-30} {y-12} q18 -4 26 -10 l3 6 q-11 8 -28 10 Z" stroke-width="1.4"/>'
        s += f'<circle cx="{x-2}" cy="{y-4}" r="2.8" stroke-width="1.1"/>'
        s += f'<path d="M{x} {y} q11 10 5 24 M{x-4} {y+1} q5 14 -5 22" stroke-width="1.5"/>'
        s += f'<path d="M{x+5} {y+24} q-6 5 -14 -1" stroke-width="1"/>'
        s += f'<path d="M{x-26} {y-24} q16 6 22 15" stroke-width="0.5"/>'
        return s

    def i4(x, y):   # 5 吹叶机 WU231.9
        s = f'<path d="{d_blower(x-30, y-18)}" stroke-width="1.5"/>'
        s += f'<path d="M{x-26} {y-13} h10 v9 h-10 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x-4} {y-11} h34 v7 h-34 Z" stroke-width="1.3"/>'
        s += f'<path d="M{x+30} {y-13} l8 3 v9 l-8 3 Z" stroke-width="1.2"/>'
        s += f'<path d="M{x+40} {y-9} l8 -3 M{x+40} {y-4} l9 0 M{x+40} {y+1} l8 3" stroke-width="0.8"/>'
        s += f'<path d="M{x-24} {y+3} h7 l2 10 h-8 Z" stroke-width="1.1"/>'
        return s

    def i5(x, y):   # 6 荧光绿标签 + 型材配件分箱
        s = f'<path d="M{x-46} {y+2} l26 -8 v9 l-26 8 Z" stroke-width="1.3"/>'
        s += f'<path d="M{x-44} {y+1} l22 -7 v2 l-22 7 Z" fill="{S}" stroke="none"/>'
        s += f'<path d="M{x-42} {y-1} l14 -4 M{x-42} {y+2} l10 -3" stroke-width="0.7"/>'
        for dx, dy in ((-10, -6), (18, -15)):
            s += f'<path d="M{x+dx} {y+dy} l22 -7 l8 4 l-22 7 Z" stroke-width="1.2"/>'
            s += f'<path d="M{x+dx} {y+dy} v9 l8 4 v-9 M{x+dx+30} {y+dy-3} v9 l-22 7 v-9" stroke-width="0.9"/>'
            s += f'<path d="M{x+dx+11} {y+dy-3.5} l8 4" stroke-width="0.7"/>'
        return s

    legend = [(1, "下区柜充电位排（取下即充，轮着充）"),
              (2, "WORX 20V 大脚板电池 ×2（裸机通用）"),
              (3, "电动打草机（裸机，共用电池）"),
              (4, "手动修枝剪（四件套里唯一不带电的）"),
              (5, "吹叶机 WU231.9（8.6～11.6 m³/min）"),
              (6, "荧光绿黑字标签 + 型材配件两只分箱")]
    leaders = [(-30, 14), (-30, 6), (-30, 10), (-24, 0), (-26, -10), (-20, -4)]
    return ex(pfx, "WORX 20V 电池平台与割草四件套", "0401-2", 4, legend,
              "首批只做割草工作流：手拔 → 打草机 → 修枝剪 → 吹叶机，合计 ¥1,500～1,800",
              [i0, i1, i2, i3, i4, i5], leaders)


# ========================= parts/0401-3 影子板生成流水线 =========================
def p0401_3():
    nodes = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44),
             ("step", 30, 130, 110, 40), ("dia", 172, 128, 116, 48),
             ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40),
             ("pill", 105, 312, 270, 30)]
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True),
             ("M140 150 H170", False), ("M288 152 H328", False),
             ("M230 176 V200 H85 V228", False), ("M390 170 V228", False),
             ("M330 250 H287", False), ("M230 270 V310", False),
             ("M30 250 Q8 250 8 110 Q8 69 28 69", True)]
    texts = [(85, 72.5, "工具平放 A4 拍照", False),
             (230, 70, "手机照片", False), (230, 83, "JPG + 纸张尺寸", True),
             (85, 147.5, "透视校正", False), (85, 161, "阈值分割抠轮廓", False),
             (230, 148, "轮廓占纸面", False), (230, 161, "5% ~ 80%？", True),
             (390, 147.5, "是 → 换算成毫米", False), (390, 161, "导出 DXF 轮廓", False),
             (85, 247.5, "否 → 提示重拍", False), (85, 261, "换背景 / 补光", False),
             (230, 247.5, "打印黄铜色贴片", False), (230, 261, "外圈 2mm 浅描边", False),
             (390, 247.5, "OpenSCAD 出 STL", False), (390, 261, "凹槽外扩 1mm", False),
             (240, 330.5, "贴上胡桃色洞洞板 · 缺件一眼看得出", False),
             (305, 146, "是", True), (238, 196, "否", True),
             (300, 246, "排料", True), (22, 206, "重拍", True)]
    return flow("p0401-3", "影子板生成流水线", nodes, edges, texts, "0401-3", 5)


def p0401_3p():
    pfx = "p0401-3p"; S = SH(pfx)
    main = "\n".join([
        # 左：手机拍照
        '<rect x="44" y="124" width="32" height="54" rx="5" stroke-width="1.4"/>',
        '<rect x="47" y="130" width="26" height="40" rx="2" stroke-width="0.6"/>',
        '<path d="M51 138 h18 M51 146 h18 M51 154 h12" stroke-width="0.8"/>',
        '<circle cx="60" cy="174" r="1.6" stroke-width="0.8"/>',
        '<path d="M53 118 q7 -8 14 0" stroke-width="0.9"/>',
        '<path d="M63 114 v-6 M55 110 l-3 -4 M71 110 l3 -4" stroke-width="0.9"/>',
        # 中：A4 纸上的扳手 + 抠出的轮廓
        '<path d="M132 128 l64 -20 v52 l-64 20 Z" stroke-width="1.5"/>',
        '<path d="M150 126 q9 -6 18 0 q0 10 -6 12 v18 q6 2 6 12 q-9 6 -18 0 q0 -10 6 -12 v-18 q-6 -2 -6 -12 Z" stroke-width="1.5"/>',
        '<path d="M138 156 l58 -18" stroke-width="0.6" stroke-dasharray="2 2"/>',
        # 右：黄铜贴片落到胡桃色洞洞板上
        '<path d="M236 142 l68 -20 v50 l-68 20 Z" stroke-width="1.5"/>',
        '<path d="M242 148 q22 -10 38 -13 M242 162 q22 -10 38 -13 M242 176 q22 -10 38 -13" stroke-width="0.35"/>',
        '<path d="M248 154 v0.5 M262 150 v0.5 M276 146 v0.5 M290 142 v0.5 M248 170 v0.5 M262 166 v0.5 M276 162 v0.5 M290 158 v0.5 M248 186 v0.5 M262 182 v0.5 M276 178 v0.5 M290 174 v0.5" stroke-width="1.1"/>',
        '<g transform="translate(272 154) scale(1.24) translate(-272 -154)"><path d="M264 139 q8 -5 16 0 q0 8 -5 9 v13 q5 1 5 9 q-8 5 -16 0 q0 -8 5 -9 v-13 q-5 -1 -5 -9 Z" stroke-width="0.6"/></g>',
        '<path d="M264 139 q8 -5 16 0 q0 8 -5 9 v13 q5 1 5 9 q-8 5 -16 0 q0 -8 5 -9 v-13 q-5 -1 -5 -9 Z" fill="' + S + '" stroke="none"/>',
        '<path d="M264 139 q8 -5 16 0 q0 8 -5 9 v13 q5 1 5 9 q-8 5 -16 0 q0 -8 5 -9 v-13 q-5 -1 -5 -9 Z" stroke-width="0.9"/>',
        # 箭头
        '<path d="M82 150 Q106 146 126 142" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M122.9 146.1 L128 141 L121.3 138.3" stroke-width="1"/>',
        '<path d="M200 150 Q216 154 230 160" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M226.1 161.4 L233 161 L229.4 155.2" stroke-width="1"/>',
        '<path d="M40 262 Q180 254 320 262" stroke-width="1.2"/>',
        '<path d="M44 266 q40 -3 80 0 M236 266 q40 -3 80 0" stroke-width="0.6"/>',
    ])
    svg = poster(pfx, "0401 · L3", "影子板生成流水线", "拍一张照片，工具就有了自己的影子", main,
                 "手机照片 → 抠轮廓换算毫米 → DXF → 打黄铜贴片贴上胡桃板",
                 ["拍照即出轮廓，不用趴在墙上手描",
                  "黄铜贴片外圈留 2mm 浅色描边，木色底才压得住",
                  "凹槽外扩 1mm，取放不卡手；打印失败可出纸样"],
                 "跑在：电脑 Python + OpenSCAD · 数据出口：DXF / STL 文件",
                 "tkubic/GridfinityShadowMaker", 9)
    add = ('<text x="60" y="196" font-size="8" fill="#666" text-anchor="middle">拍照</text>'
           '<text x="164" y="212" font-size="8" fill="#666" text-anchor="middle">抠轮廓 · 换算毫米</text>'
           '<text x="270" y="210" font-size="8" fill="#666" text-anchor="middle">黄铜贴片上胡桃板</text>')
    return svg.replace("</svg>", add + "\n</svg>")


# ========================== parts/0401-4 取用归位提醒 ==========================
def p0401_4():
    nodes = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44),
             ("step", 30, 130, 110, 40), ("dia", 172, 128, 116, 48),
             ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("dia", 172, 226, 116, 48), ("step", 330, 230, 120, 40),
             ("pill", 100, 312, 280, 30)]
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True),
             ("M140 150 H170", False), ("M288 152 H328", False),
             ("M230 176 V200 H85 V228", False), ("M390 170 V228", True),
             ("M330 250 H290", False), ("M230 274 V310", False),
             ("M85 270 V327 H98", False)]
    texts = [(85, 72.5, "手机碰工具 NFC", False),
             (230, 70, "工具去向清单", False), (230, 83, "去向模块 + 时间", True),
             (85, 147.5, "收到 tag_scanned", False), (85, 161, "查该工具状态", False),
             (230, 148, "还在影子里？", False), (230, 161, "首碰 / 再碰", True),
             (390, 147.5, "是 → 标记在外", False), (390, 161, "写下去向模块", False),
             (85, 247.5, "否 → 标记归位", False), (85, 261, "清零计时", False),
             (230, 246, "超过 3 天未归位？", False), (230, 259, "7 天中枢屏亮黄", True),
             (390, 247.5, "每晚 22:00", False), (390, 261, "巡检在外清单", False),
             (240, 330.5, "推送提醒 · 割草四件套整组核对 · 小白板手写兜底", False),
             (305, 146, "是", True), (238, 196, "否", True),
             (396, 200, "当晚", True), (240, 292, "是", True),
             (152, 222, "否 → 明晚再查", True)]
    return flow("p0401-4", "取用归位提醒", nodes, edges, texts, "0401-4", 6)


def p0401_4p():
    pfx = "p0401-4p"; S = SH(pfx)
    main = "\n".join([
        # 左：墙上的影子 + NFC 标签 + 手机碰一下
        '<path d="M38 120 h46 v62 h-46 Z" stroke-width="1.4"/>',
        '<path d="M43 128 v0.5 M55 128 v0.5 M67 128 v0.5 M79 128 v0.5 M43 144 v0.5 M55 144 v0.5 M67 144 v0.5 M79 144 v0.5 M43 160 v0.5 M55 160 v0.5 M67 160 v0.5 M79 160 v0.5" stroke-width="1.1"/>',
        '<g transform="translate(58 146) scale(1.22) translate(-58 -146)"><path d="M49 132 h18 v8 h-6 v21 h-6 v-21 h-6 Z" stroke-width="0.6"/></g>',
        '<path d="M49 132 h18 v8 h-6 v21 h-6 v-21 h-6 Z" fill="' + S + '" stroke="none"/>',
        '<path d="M49 132 h18 v8 h-6 v21 h-6 v-21 h-6 Z" stroke-width="0.9"/>',
        '<rect x="90" y="132" width="24" height="22" rx="4" stroke-width="1.3"/>',
        '<circle cx="102" cy="143" r="7.5" stroke-width="1"/><circle cx="102" cy="143" r="4.5" stroke-width="0.8"/><circle cx="102" cy="143" r="1.8" stroke-width="0.7"/>',
        '<rect x="88" y="160" width="26" height="42" rx="5" stroke-width="1.4"/>',
        '<rect x="91" y="166" width="20" height="28" rx="2" stroke-width="0.6"/>',
        '<path d="M95 174 h12 M95 181 h12 M95 188 h7" stroke-width="0.7"/>',
        '<path d="M118 156 l5 -4 M118 164 l6 0" stroke-width="0.9"/>',
        # 中：HomeAssistant 房子 + 去向清单
        '<path d="M150 168 l28 -24 l28 24 v32 h-56 Z" stroke-width="1.6"/>',
        '<path d="M144 170 l34 -30 l34 30" stroke-width="1.2"/>',
        '<circle cx="178" cy="178" r="7.5" stroke-width="1.2"/>',
        '<path d="M178 170.5 v-3 M178 185.5 v3 M170.5 178 h-3 M185.5 178 h3" stroke-width="1"/>',
        '<path d="M152 196 h52 v3 h-52 Z" fill="' + S + '" stroke="none"/>',
        # 右：推送 + 四件套整组 + 小白板
        '<rect x="248" y="136" width="30" height="50" rx="5" stroke-width="1.4"/>',
        '<rect x="251" y="142" width="24" height="36" rx="2" stroke-width="0.6"/>',
        '<path d="M255 150 h16 M255 158 h16 M255 166 h10" stroke-width="0.8"/>',
        '<circle cx="263" cy="182" r="1.6" stroke-width="0.8"/>',
        '<path d="M280 144 q8 -4 6 -12 M284 148 q12 -6 10 -18" stroke-width="0.8"/>',
        '<rect x="250" y="148" width="26" height="12" rx="2" fill="' + S + '" stroke="none"/>',
        '<path d="M288 186 h42 v30 h-42 Z" stroke-width="1.4"/>',
        '<path d="M293 194 h20 M293 201 h26 M293 208 h16" stroke-width="0.8"/>',
        '<path d="M296 186 v-5 M322 186 v-5" stroke-width="1"/>',
        '<path d="M236 210 h40 v22 h-40 Z" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M242 216 v12 M250 214 l4 14 M260 216 h8 v10 h-8 Z M270 216 v12" stroke-width="1"/>',
        # 箭头
        '<path d="M120 170 Q132 170 144 172" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M139.8 175.4 L146 172 L140.4 167.4" stroke-width="1"/>',
        '<path d="M210 168 Q228 164 244 160" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M240.4 163.8 L246 159.5 L239.6 156.4" stroke-width="1"/>',
        '<path d="M210 190 Q248 198 284 200" stroke-width="1" stroke-dasharray="3 3"/>',
        '<path d="M279.6 203.4 L286 200 L280.4 195.4" stroke-width="1"/>',
        '<path d="M40 262 Q180 254 320 262" stroke-width="1.2"/>',
        '<path d="M44 266 q40 -3 80 0 M236 266 q40 -3 80 0" stroke-width="0.6"/>',
    ])
    svg = poster(pfx, "0401 · L4", "取用归位提醒", "工具去了哪个模块，这面墙比你先知道", main,
                 "NFC 碰一下 → HA 记去向模块 → 每晚巡检在外清单 → 推送 + 中枢屏",
                 ["碰一下带走，再碰一下归位，零登记",
                  "3 天未归位推送，7 天中枢屏亮黄",
                  "割草四件套整组登记，回来少一件立刻看得出"],
                 "跑在：HomeAssistant · 数据出口：在外清单实体 + 手机推送",
                 "home-assistant/core", 10)
    add = ('<text x="61" y="196" font-size="8" fill="#666" text-anchor="middle">空影子 = 在外</text>'
           '<text x="178" y="216" font-size="8" fill="#666" text-anchor="middle">记下去向模块</text>'
           '<text x="256" y="246" font-size="8" fill="#666" text-anchor="middle">推送 · 整组核对 · 白板兜底</text>')
    return svg.replace("</svg>", add + "\n</svg>")


OUT = {
    "illos/0401.svg": m0401,
    "parts/0401-1.svg": p0401_1,
    "parts/0401-2.svg": p0401_2,
    "parts/0401-3.svg": p0401_3,
    "parts/0401-3-poster.svg": p0401_3p,
    "parts/0401-4.svg": p0401_4,
    "parts/0401-4-poster.svg": p0401_4p,
}

if __name__ == "__main__":
    for path, fn in OUT.items():
        open(path, "w", encoding="utf-8").write(fn())
    print("ok", len(OUT))
