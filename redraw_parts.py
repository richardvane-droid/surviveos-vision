from sk import *
def SH(pfx): return f"url(#{pfx}-shade)"

def along(i, n, x0=110, y0=300, x1=380, y1=60):
    """爆炸轴上第 i/n 个位置"""
    t = i/(n-1) if n > 1 else 0
    return x0 + (x1-x0)*t, y0 + (y1-y0)*t

def p0101_1():
    pfx="p0101-1"; B=[]; L=[]; C=[]
    n=5
    # 1 托架×2（最下，贴墙）
    x,y=along(0,n); B.append(f'<path d="M{x-40} {y} l-14 -30 l24 -4 l10 34 Z M{x+10} {y-8} l-14 -30 l24 -4 l10 34 Z" stroke-width="1.5"/><path d="M{x-38} {y-2} l-10 -24 l16 -3 l8 27 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-46} {y-18} a2 2 0 1 0 0.1 0 M{x+4} {y-26} a2 2 0 1 0 0.1 0" stroke-width="0.8"/>')
    # 2 薄抽屉层
    x,y=along(1,n); B.append(f'<path d="M{x-56} {y+6} h96 l24 -14 h-96 Z" stroke-width="1.5"/><path d="M{x-56} {y+6} v12 h96 v-12 M{x+40} {y+18} l24 -14 v-12" stroke-width="1.2"/><path d="M{x+41} {y+17} l22 -13 v-11 l-22 13 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-10} {y+12} h10" stroke-width="1.2"/>')
    # 3 倾斜台面（12°）
    x,y=along(2,n); B.append(f'<path d="M{x-58} {y+8} h96 l24 -14 h-96 Z" stroke-width="1.5"/><path d="M{x-58} {y+8} l0 4 h96 l24 -14 v-4 M{x+38} {y+12} l24 -14" stroke-width="1"/><path d="M{x-54} {y+3} l6 -10 M{x+30} {y+3} l6 -10" stroke-width="0.6" stroke-dasharray="2 2"/>')
    # 4 毛毡内衬（27 卡槽）
    x,y=along(3,n); B.append(f'<path d="M{x-54} {y+6} h84 l22 -12 h-84 Z" stroke-width="1.3"/><path d="M{x-52} {y+5} h80 l20 -11 h-80 Z" fill="{SH(pfx)}" stroke="none"/>')
    for i in range(3):
        for j in range(4): B.append(f'<path d="M{x-46+j*18+i*6} {y+2-i*4} h9 v3 h-9 Z" stroke-width="0.6"/>')
    # 5 生存盒 + 铭牌（最上）
    x,y=along(4,n); B.append(f'<path d="M{x-30} {y+6} h40 v20 h-40 Z M{x-30} {y+6} l6 -20 h40 l-6 20" stroke-width="1.4"/><path d="M{x-24} {y-12} h34 v16 h-34 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-26} {y+12} h8 M{x-14} {y+12} h10 M{x-26} {y+20} h30" stroke-width="0.6"/><path d="M{x+18} {y+16} h18 v8 h-18 Z" stroke-width="0.9"/>')
    for i,(dx,dy) in enumerate([(-60,-16),(-70,-2),(-72,-4),(-66,-2),(-44,-16)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-40,y+dy-4,i+1); L.append(l); C.append(c)
    legend=[(1,"手刨胡桃木托架 ×2（膨胀螺栓咬墙）"),(2,"薄抽屉层（3 只未开封同款）"),(3,"倾斜 12° 台面，前低后高，台高 900"),(4,"3mm 深灰毛毡内衬 · 27 卡槽刻编号"),(5,"PSK 生存盒 + 黄铜铭牌 40×18")]
    svg=exploded(pfx,"胡桃木挂墙展台","",("\n".join(B)),"0101-1",axis="M100 318 L392 40",seed=41,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    svg=svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">挂在北墙 0102 作品九宫格正下方，不落地</text>\n</svg>')
    return svg

def p0402_1():
    pfx="p0402-1"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n); B.append(f'<path d="M{x-70} {y} h140 l30 -16 h-140 Z" stroke-width="1.5"/><path d="M{x-70} {y} v6 h140 v-6 M{x+70} {y+6} l30 -16 v-6" stroke-width="1"/><path d="M{x+71} {y+5} l28 -15 v-5 l-28 15 Z" fill="{SH(pfx)}" stroke="none"/>')  # 1 踢脚板底座
    x,y=along(1,n)
    for i in range(6): B.append(f'<path d="M{x-70+i*28} {y+8} v-{28+i*4} M{x-70+i*28} {y-20-i*4} l8 -4" stroke-width="1.3"/>')  # 2 立柱（随斜顶渐高）
    B.append(f'<path d="M{x-72} {y-22} L{x+72} {y-46}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    x,y=along(2,n)
    for r in range(3): B.append(f'<path d="M{x-66} {y+6-r*12} h130 l10 -5" stroke-width="1.2"/><path d="M{x-66} {y+6-r*12} l6 3 M{x-40} {y+6-r*12} l6 3 M{x-14} {y+6-r*12} l6 3 M{x+12} {y+6-r*12} l6 3 M{x+38} {y+6-r*12} l6 3" stroke-width="0.8"/>')  # 3 托臂三阶
    x,y=along(3,n)
    for r in range(3): B.append(f'<path d="M{x-60} {y+4-r*10} h120 v-4 h-120 Z" stroke-width="0.9"/><path d="M{x-58} {y+3-r*10} h116 v-2 h-116 Z" fill="{SH(pfx)}" stroke="none"/>')  # 4 垫木+长料
    B.append(f'<path d="M{x-60} {y-24} h120 v-3 h-120 Z M{x-60} {y-30} h100 v-3 h-100 Z" stroke-width="0.8"/>')
    x,y=along(4,n); B.append(f'<path d="M{x-22} {y} h44 v14 h-44 Z" stroke-width="1"/><path d="M{x-18} {y+5} h20 M{x-18} {y+10} h14" stroke-width="0.6"/><path d="M{x+30} {y+2} h20 v12 h-20 Z M{x+34} {y+7} h12" stroke-width="0.8"/>')  # 5 标签
    for i,(dx,dy) in enumerate([(-74,-6),(-74,-10),(-70,-14),(-64,-14),(-26,6)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-30,y+dy-2,i+1); L.append(l); C.append(c)
    legend=[(1,"踢脚板底座（离地 100mm）"),(2,"分格立柱 40×40，随 45° 斜顶三阶渐高"),(3,"托臂 40×40 木方 · 间距 600mm · 三阶"),(4,"垫木通风 + 长料躺放（头朝通道）"),(5,"每格标签：木种 / 厚度 / 购入年月")]
    svg=exploded(pfx,"斜顶下长直木料架","",("\n".join(B)),"0402-1",axis="M100 318 L392 40",seed=43,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">北条低矮带 · 长 7m · 最高一阶 ≤1.2m</text>\n</svg>')

def p0403_1():
    pfx="p0403-1"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n); B.append(f'<path d="M{x-50} {y-30} h90 v40 h-90 Z M{x+40} {y-30} l24 -12 v40 l-24 12" stroke-width="1.5"/><path d="M{x+41} {y-29} l22 -11 v37 l-22 11 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-46} {y-26} h82 v32 h-82 Z" stroke-width="0.6"/><circle cx="{x-5}" cy="{y-10}" r="9" stroke-width="1"/><path d="M{x-11} {y-10} h12 M{x-5} {y-16} v12" stroke-width="0.7"/>')  # 1 柜体+静压箱+风机
    x,y=along(1,n); B.append(f'<path d="M{x-50} {y} h90 l24 -12 h-90 Z" stroke-width="1.3"/><path d="M{x-46} {y-2} h82 l18 -9 h-82 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-50} {y} v6 h90 v-6" stroke-width="0.9"/>')  # 2 集雾盘
    x,y=along(2,n); B.append(f'<path d="M{x-50} {y} h90 l24 -12 h-90 Z" stroke-width="1.2"/><path d="M{x-48} {y-1} h86 l20 -10 h-86 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-44} {y-4} q4 -3 8 0 t8 0 t8 0 t8 0 t8 0 t8 0 t8 0" stroke-width="0.6"/>')  # 3 过滤棉
    x,y=along(3,n); B.append(f'<path d="M{x-50} {y} h90 l24 -12 h-90 Z" stroke-width="1.4"/>')
    for i in range(1,9): B.append(f'<path d="M{x-50+i*10} {y} l24 -12" stroke-width="0.6"/>')
    for i in range(1,4): B.append(f'<path d="M{x-50+i*6} {y-i*3} h90" stroke-width="0.5"/>')  # 4 钢格栅
    x,y=along(4,n); B.append(f'<path d="M{x-50} {y+4} v-40 h90 v40 M{x+40} {y-36} l24 -12 v40" stroke-width="1.3"/><path d="M{x-46} {y-22} h82" stroke-width="0.9"/><path d="M{x-30} {y-22} v6 M{x-10} {y-22} v6 M{x+10} {y-22} v6 M{x+28} {y-22} v6" stroke-width="0.8"/><path d="M{x-50} {y-36} l-8 6 v40 l8 -6" stroke-width="0.9" stroke-dasharray="3 2"/>')  # 5 三面挡板+晾杆+前帘
    for i,(dx,dy) in enumerate([(-54,-20),(-54,-2),(-54,-4),(-54,-4),(-54,-30)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-34,y+dy-2,i+1); L.append(l); C.append(c)
    legend=[(1,"柜体 1.5×1.0m · 30 铝型材+镀锌板 · 底部静压箱+风机"),(2,"集雾盘（可抽出清洗）"),(3,"过滤棉（每月换）"),(4,"钢格栅台面 · 台高 900 · 风往下抽"),(5,"三面挡板 600 高 + 晾杆 S 钩 + 前帘")]
    svg=exploded(pfx,"下抽式喷涂柜本体","",("\n".join(B)),"0403-1",axis="M100 318 L392 40",seed=45,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">放在木工间东缘南段，不是一个房间</text>\n</svg>')

def p0403_2():
    pfx="p0403-2"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n); B.append(f'<path d="M{x-40} {y-20} h60 v30 h-60 Z M{x+20} {y-20} l16 -8 v30 l-16 8" stroke-width="1.4"/><path d="M{x+21} {y-19} l14 -7 v27 l-14 7 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+20} {y-5} l16 -8 M{x+28} {y-9} a4 4 0 1 0 0.1 0" stroke-width="0.8"/>')  # 1 静压箱
    x,y=along(1,n); B.append(f'<path d="M{x-16} {y-14} a16 14 0 1 0 32 0 a16 14 0 1 0 -32 0" stroke-width="1.4"/><path d="M{x-16} {y-14} v20 a16 6 0 0 0 32 0 v-20" stroke-width="1"/><path d="M{x-12} {y+2} a12 4 0 0 0 24 0 v-4 a12 4 0 0 1 -24 0 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-8} {y-14} h16 M{x} {y-22} v16 M{x-6} {y-20} l12 12 M{x+6} {y-20} l-12 12" stroke-width="0.7"/>')  # 2 风机
    x,y=along(2,n); B.append(f'<path d="M{x-20} {y-8} a20 8 0 1 0 40 0 a20 8 0 1 0 -40 0" stroke-width="1.3"/><path d="M{x-20} {y-8} v-2 M{x+20} {y-8} v-2 M{x-20} {y-10} L{x+60} {y-58} M{x+20} {y-10} L{x+100} {y-58} M{x+60} {y-58} a20 8 0 0 0 40 0" stroke-width="1.2"/><path d="M{x+21} {y-10} L{x+100} {y-58} v-2 L{x+21} {y-12} Z" fill="{SH(pfx)}" stroke="none"/>')
    for i in range(1,5): B.append(f'<path d="M{x-20+i*16} {y-10-i*9.6} l40 0" stroke-width="0.4"/>')  # 3 150mm 硬管 ≈2.06m（斜着躺）
    x,y=along(3,n); B.append(f'<path d="M{x-24} {y-14} h48 v6 h-48 Z M{x-20} {y-8} v14 h40 v-14" stroke-width="1.2"/><path d="M{x-16} {y-4} h32 M{x-16} {y+2} h32" stroke-width="0.7"/><circle cx="{x}" cy="{y+18}" r="4" stroke-width="0.8"/>')  # 4 检修口/快拆卡箍
    x,y=along(4,n); B.append(f'<path d="M{x-22} {y-22} h44 v30 h-44 Z" stroke-width="1.3"/>')
    for i in range(4): B.append(f'<path d="M{x-20} {y-18+i*7} l40 4" stroke-width="0.9"/>')
    B.append(f'<path d="M{x-24} {y+12} h48 M{x-18} {y+14} l3 3 M{x-8} {y+14} l3 3 M{x+2} {y+14} l3 3 M{x+12} {y+14} l3 3" stroke-width="0.6"/>')  # 5 外墙口百叶+防虫网
    for i,(dx,dy) in enumerate([(-44,-10),(-20,-24),(-24,-4),(-28,-10),(-26,-16)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-34,y+dy-4,i+1); L.append(l); C.append(c)
    legend=[(1,"柜底静压箱（接过滤棉之后）"),(2,"管道风机 300m³/h"),(3,"150mm 铝箔硬管 · 全长 ≈2.06m · 一根到底"),(4,"室内段快拆卡箍 + 检修口"),(5,"东墙外口：防雨百叶 + 防虫网")]
    svg=exploded(pfx,"直排风管组","",("\n".join(B)),"0403-2",axis="M100 318 L392 40",seed=47,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">向东直穿低矮圈出东墙，不拐弯</text>\n</svg>')

def p0604_1():
    pfx="p0604-1"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n); B.append(f'<path d="M{x-40} {y-40} h30 v60 h-30 Z" stroke-width="1.5"/><path d="M{x-38} {y-38} h26 v56 h-26 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-30} {y-26} a2 2 0 1 0 0.1 0 M{x-30} {y-6} a2 2 0 1 0 0.1 0 M{x-30} {y+12} a2 2 0 1 0 0.1 0" stroke-width="0.9"/><path d="M{x-10} {y-24} h20 v4 h-20 Z M{x-10} {y-4} h20 v4 h-20 Z" stroke-width="1"/>')  # 1 墙板+膨胀螺栓+底座
    x,y=along(1,n); B.append(f'<path d="M{x-14} {y-4} h110 l10 -4 v8 l-10 -4 Z" stroke-width="1.4"/><path d="M{x-14} {y-4} a3 8 0 1 0 0 8 Z" stroke-width="1"/><path d="M{x-12} {y-2} h100 v4 h-100 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+30} {y-4} v-8 M{x+80} {y-4} v-8" stroke-width="0.8"/>')  # 2 横臂 Φ40×60cm
    x,y=along(2,n); B.append(f'<path d="M{x-16} {y-12} h22 v16 h-22 Z M{x+6} {y-8} h8 v8 h-8 Z" stroke-width="1.3"/><circle cx="{x-5}" cy="{y-4}" r="4" stroke-width="0.8"/><path d="M{x-5} {y+4} v8 M{x-9} {y+12} h8" stroke-width="0.8"/><path d="M{x+30} {y-14} h26 v20 h-26 Z M{x+56} {y-10} h12 v12 h-12 Z" stroke-width="1.3"/><circle cx="{x+43}" cy="{y-4}" r="5" stroke-width="0.8"/>')  # 3 广角机+长焦机
    x,y=along(3,n); B.append(f'<path d="M{x-14} {y-8} h28 v12 h-28 Z" stroke-width="1.2"/><circle cx="{x-6}" cy="{y-2}" r="2" stroke-width="0.7"/><circle cx="{x+2}" cy="{y-2}" r="2" stroke-width="0.7"/><circle cx="{x+9}" cy="{y-2}" r="2" stroke-width="0.7"/><path d="M{x-8} {y+8} l-6 12 M{x+8} {y+8} l6 12" stroke-width="0.5" stroke-dasharray="2 2"/>')  # 4 红外补光
    x,y=along(4,n); B.append(f'<path d="M{x-30} {y} q20 -20 40 0 t40 0" stroke-width="1.2"/><path d="M{x-34} {y} a4 4 0 1 0 0.1 0 M{x+50} {y} h10 v8 h-10 Z M{x+52} {y+2} h6" stroke-width="0.9"/>')  # 5 PoE 网线穿墙
    for i,(dx,dy) in enumerate([(-44,-30),(-18,-8),(-20,-10),(-18,-6),(-36,-4)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-32,y+dy-6,i+1); L.append(l); C.append(c)
    legend=[(1,"东墙底座（≈4m 高）· 膨胀螺栓 ×4"),(2,"热镀锌横臂 Φ40mm × 60cm"),(3,"广角机 2.8mm 朝北 · 长焦机 12mm 对水盆"),(4,"850nm 红外补光（不惊扰夜行动物）"),(5,"PoE 供电，一根网线穿墙进屋")]
    svg=exploded(pfx,"东墙双机横臂","",("\n".join(B)),"0604-1",axis="M100 318 L392 40",seed=49,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">不立杆：挂在建筑东墙上俯视整条 18.9m 草地</text>\n</svg>')

def p0701_1():
    pfx="p0701-1"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n)
    for (dx,dy) in ((-60,0),(-10,-10),(40,-20),(-40,16),(10,6),(60,-4)):
        B.append(f'<path d="M{x+dx} {y+dy} h16 v10 h-16 Z M{x+dx} {y+dy} l6 -4 h16 l-6 4 M{x+dx+16} {y+dy} l6 -4 v10 l-6 4" stroke-width="1.1"/><path d="M{x+dx+8} {y+dy} v-6" stroke-width="0.8"/>')
    B.append(f'<path d="M{x-70} {y+34} q20 -6 40 0 t40 0 t40 0 t40 0" stroke-width="0.6" stroke-dasharray="2 2"/>')  # 1 六个预制墩+碎石垫层
    x,y=along(1,n); B.append(f'<path d="M{x-60} {y+6} h110 l30 -16 h-110 Z M{x-60} {y+6} v-6 h110 v6 M{x+50} {y} l30 -16" stroke-width="1.3"/>')
    for i in range(1,5): B.append(f'<path d="M{x-60+i*22} {y+6} l30 -16" stroke-width="0.9"/>')  # 2 柱脚件+松木框龙骨
    x,y=along(2,n); B.append(f'<path d="M{x-62} {y+8} h114 l32 -18 h-114 Z" stroke-width="1.5"/>')
    for i in range(1,12): B.append(f'<path d="M{x-62+i*9.5} {y+8} l32 -18" stroke-width="0.6"/>')
    B.append(f'<path d="M{x-62} {y+8} v4 h114 v-4 M{x+52} {y+12} l32 -18 v-4" stroke-width="1"/><path d="M{x+53} {y+11} l30 -17 v-3 l-30 17 Z" fill="{SH(pfx)}" stroke="none"/>')  # 3 面板 2.5×2.2
    x,y=along(3,n); B.append(f'<path d="M{x+40} {y+10} l32 -18 v-6 l-32 18 Z" stroke-width="1.2"/><path d="M{x+41} {y+9} l30 -17 v-4 l-30 17 Z" fill="{SH(pfx)}" stroke="none"/>')  # 4 挡水条
    x,y=along(4,n); B.append(f'<path d="M{x-30} {y} h50 v6 h-50 Z M{x-26} {y+6} v12 M{x+16} {y+6} v12" stroke-width="1.1"/><path d="M{x-28} {y+3} h46" stroke-width="0.5"/>')  # 5 靠岸长凳
    for i,(dx,dy) in enumerate([(-66,-2),(-62,-6),(-64,-6),(38,-12),(-32,-4)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-32,y+dy-6,i+1); L.append(l); C.append(c)
    legend=[(1,"预制混凝土墩 ×6 · 40cm 碎石垫层 · 不打桩不下水"),(2,"镀锌柱脚件 + 防腐松木框龙骨 90×45 @400"),(3,"防腐木面板 2.5×2.2m · 板缝 5mm 排水"),(4,"临河侧 10cm 木挡水条"),(5,"靠岸一侧固定长凳（凳下放鱼护）")]
    svg=exploded(pfx,"预制墩木框钓台平台","",("\n".join(B)),"0701-1",axis="M100 318 L392 40",seed=51,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">岸上、缓坡坡脚 · ≈5.5㎡ · 一人尺度</text>\n</svg>')

def p0701_3():
    pfx="p0701-3"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n); B.append(f'<path d="M{x-70} {y+20} L{x+60} {y-40} L{x+90} {y-30} L{x-40} {y+30} Z" stroke-width="1.3"/><path d="M{x-68} {y+19} L{x+58} {y-39} L{x+86} {y-30} L{x-40} {y+28} Z" fill="{SH(pfx)}" stroke="none"/>')  # 1 缓坡坡面
    x,y=along(1,n)
    for i in range(4): B.append(f'<path d="M{x-50+i*22} {y+10-i*10} h18 v6 h-18 Z M{x-50+i*22} {y+10-i*10} l8 -4 h18 l-8 4 M{x-32+i*22} {y+10-i*10} l8 -4 v6 l-8 4" stroke-width="1.1"/>')  # 2 防腐木框踏步
    x,y=along(2,n)
    for i in range(4): B.append(f'<path d="M{x-50+i*22} {y+8-i*10} h18 l8 -4 h-18 Z" stroke-width="0.9"/><path d="M{x-48+i*22} {y+7-i*10} q3 -2 6 0 t6 0 t6 0" stroke-width="0.5"/>')  # 3 碎石填芯
    x,y=along(3,n)
    for i in range(3): B.append(f'<path d="M{x-40+i*30} {y+10-i*12} v-34 M{x-40+i*30} {y-24-i*12} a3 3 0 1 0 0.1 0" stroke-width="1.3"/>')  # 4 防腐木柱
    x,y=along(4,n); B.append(f'<path d="M{x-60} {y+20} L{x+50} {y-30}" stroke-width="2.2"/><path d="M{x-60} {y+20} L{x+50} {y-30}" stroke-width="0.6" stroke-dasharray="1 6"/><path d="M{x-30} {y+6} l2 -4 M{x} {y-8} l2 -4 M{x+30} {y-22} l2 -4" stroke-width="0.7"/>')  # 5 毛竹扶手
    for i,(dx,dy) in enumerate([(-70,-2),(-52,-2),(-52,-2),(-42,-30),(-60,10)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-30,y+dy-6,i+1); L.append(l); C.append(c)
    legend=[(1,"6m 缓坡坡面（从 2m 过道下到钓台）"),(2,"防腐木框踏步 ×12 · 90×45 木方 · 踏面 30cm"),(3,"框内碎石夯实，与坡面齐平"),(4,"单侧防腐木柱，扶手高 75cm"),(5,"Φ60 去皮毛竹扶手，两年换一次")]
    svg=exploded(pfx,"缓坡踏步与竹扶手","",("\n".join(B)),"0701-3",axis="M100 318 L392 40",seed=53,leaders="\n".join(L))
    svg=svg.replace('<g font-size="8.5" fill="#444"></g>','<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>',"\n".join(C)+'\n<text x="16" y="120" font-size="8" fill="#888" font-style="italic">没有栈道：踏步嵌在坡里，两侧留给菖蒲芦苇</text>\n</svg>')

if __name__=="__main__":
    for fn,f in ((p0101_1,"0101-1"),(p0402_1,"0402-1"),(p0403_1,"0403-1"),(p0403_2,"0403-2"),(p0604_1,"0604-1"),(p0701_1,"0701-1"),(p0701_3,"0701-3")):
        open(f"parts/{f}.svg","w",encoding="utf-8").write(fn())
    print("ok")
