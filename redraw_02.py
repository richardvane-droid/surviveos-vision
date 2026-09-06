from sk import *
H = "url(#marea-02-hatch)"; HL = "url(#marea-02-hatchl)"
S = 32; OX, OY = 210, 78
def ob(x, y, z=0):
    return f"{OX + (x - y)*S*0.87:.1f} {OY + (x + y)*S*0.5 - z*S:.1f}"
def obox(x0, y0, x1, y1, z0, z1, sw=1.2, top_hatch=False, side_hatch=True):
    """平面 x0..x1（西→东） y0..y1（北→南），高 z0..z1 的盒子（斜轴测）"""
    a = ob(x0,y0,z1); b = ob(x1,y0,z1); c = ob(x1,y1,z1); d = ob(x0,y1,z1)
    a0 = ob(x0,y0,z0); b0 = ob(x1,y0,z0); c0 = ob(x1,y1,z0); d0 = ob(x0,y1,z0)
    s = f'<path d="M{a} L{b} L{c} L{d} Z" stroke-width="{sw}"/>'
    s += f'<path d="M{d} L{d0} L{c0} L{c} M{c} L{c0} L{b0} L{b}" stroke-width="{sw}"/>'
    if side_hatch: s += f'<path d="M{c} L{c0} L{b0} L{b} Z" fill="{H}" stroke="none"/>'
    if top_hatch: s += f'<path d="M{a} L{b} L{c} L{d} Z" fill="{HL}" stroke="none"/>'
    return s

def area02():
    B = []
    W, D = 4.85, 5.0
    # 地面
    B.append(f'<path d="M{ob(0,0)} L{ob(W,0)} L{ob(W,D)} L{ob(0,D)} Z" stroke-width="1.8"/>')
    WC = 1.0  # 剖切高度
    # 四面墙都剖到 1.0 高；北/西墙在后，先画；东/南墙最后画
    B.append(f'<path d="M{ob(0,D,WC)} L{ob(0,0,WC)} L{ob(W,0,WC)} M{ob(0,0,WC)} L{ob(0,0,0)}" stroke-width="1.6"/>')
    B.append(f'<path d="M{ob(0,0.05,WC)} L{ob(0,D,WC)} L{ob(0,D,0)} M{ob(W,0,WC)} L{ob(W,0,0)}" stroke-width="1.4"/>')
    # 北墙面淡排线（无窗）
    B.append(f'<path d="M{ob(0.05,0,WC-0.03)} L{ob(W-0.05,0,WC-0.03)} L{ob(W-0.05,0,0.03)} L{ob(0.05,0,0.03)} Z" fill="{HL}" stroke="none"/>')
    # 梁（南墙上方 2.4）——用一段悬空虚线框示意

    # 卫生间（东北）与储藏室（东）：隔墙 0.5 高
    B.append(f'<path d="M{ob(3.25,0,0.5)} L{ob(3.25,3.82,0.5)} L{ob(3.25,3.82,0)} M{ob(3.25,0,0.5)} L{ob(3.25,0,0)} M{ob(3.25,1.29,0.5)} L{ob(W,1.29,0.5)} M{ob(3.25,1.29,0.5)} L{ob(3.25,1.29,0)} M{ob(3.25,3.82,0.5)} L{ob(W,3.82,0.5)}" stroke-width="1.2"/>')
    B.append(f'<path d="M{ob(3.25,0,0.5)} L{ob(3.25,3.82,0.5)} L{ob(3.37,3.82,0.5)} L{ob(3.37,0,0.5)} Z" fill="{H}" stroke="none"/>')
    # 卫生间内：马桶/淋浴示意 + 灯箱（天花）
    B.append(f'<ellipse cx="{float(ob(4.0,0.6).split()[0])}" cy="{float(ob(4.0,0.6).split()[1])}" rx="7" ry="4" stroke-width="0.9"/><path d="M{ob(3.5,0.2)} L{ob(3.5,1.1)} M{ob(3.5,0.2)} L{ob(3.9,0.2)}" stroke-width="0.7" stroke-dasharray="2 2"/>')
    # 储藏室：罐头架
    for i in range(3):
        y0 = 1.5 + i*0.7
        B.append(obox(3.4, y0, 4.7, y0+0.35, 0, 0.45, 0.8, side_hatch=False))
    # 架空床（西北）0..1.2 × 0..2.0，床板 1.75；床下帐篷 1.2×1.5
    B.append(obox(0.05, 0.05, 1.2, 2.0, 1.6, 1.75, 1.3))
    B.append(f'<path d="M{ob(0.1,0.1,1.75)} q20 -6 40 0 M{ob(0.4,1.0,1.75)} q14 -4 28 0" stroke-width="0.7"/>')
    for (x,y) in ((0.1,0.1),(1.15,0.1),(1.15,1.95),(0.1,1.95)):
        B.append(f'<path d="M{ob(x,y,1.6)} L{ob(x,y,0)}" stroke-width="1.1"/>')
    # 帐篷（床下）
    B.append(f'<path d="M{ob(0.15,0.3,0)} L{ob(0.6,0.3,1.35)} L{ob(1.1,0.3,0)} Z M{ob(0.15,1.8,0)} L{ob(0.6,1.8,1.35)} L{ob(1.1,1.8,0)} Z M{ob(0.6,0.3,1.35)} L{ob(0.6,1.8,1.35)}" stroke-width="1.1"/>')
    B.append(f'<path d="M{ob(0.15,1.8,0)} L{ob(0.6,1.8,1.35)} L{ob(0.6,1.05,1.35)} L{ob(0.15,1.05,0)} Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M{ob(0.6,1.8,0.05)} L{ob(0.6,1.8,0.9)}" stroke-width="0.8"/><circle cx="{ob(0.62,1.5,0.7).split()[0]}" cy="{ob(0.62,1.5,0.7).split()[1]}" r="2.5" stroke-width="0.8"/>')
    # 书架（北墙）1.21..3.15 × 0..0.26 高 2.0
    B.append(obox(1.25, 0.02, 3.15, 0.26, 0, 2.0, 1.1, side_hatch=False))
    for z in (0.5, 1.0, 1.5):
        B.append(f'<path d="M{ob(1.25,0.26,z)} L{ob(3.15,0.26,z)}" stroke-width="0.7"/>')
    # 沙发 1.23..2.59 × 1.24..2.17 高 0.8
    B.append(obox(1.25, 1.25, 2.6, 2.15, 0, 0.45, 1.1))
    B.append(obox(1.25, 1.25, 2.6, 1.5, 0.45, 0.85, 1.0))
    # 地毯 1.36..3.15 × 2.29..4.14
    B.append(f'<path d="M{ob(1.36,2.3)} L{ob(3.15,2.3)} L{ob(3.15,4.14)} L{ob(1.36,4.14)} Z" stroke-width="0.9"/><path d="M{ob(1.5,2.45)} L{ob(3.0,2.45)} L{ob(3.0,4.0)} L{ob(1.5,4.0)} Z" stroke-width="0.5" stroke-dasharray="2 3"/>')
    # 双层衣架 0..1.16 × 2.06..2.68 高 1.7
    B.append(f'<path d="M{ob(0.1,2.35,0)} L{ob(0.1,2.35,1.7)} L{ob(1.1,2.35,1.7)} L{ob(1.1,2.35,0)} M{ob(0.1,2.35,1.0)} L{ob(1.1,2.35,1.0)}" stroke-width="1"/>')
    for i in range(5):
        x = 0.25 + i*0.18
        B.append(f'<path d="M{ob(x,2.35,1.7)} L{ob(x,2.35,1.25)} M{ob(x,2.35,1.0)} L{ob(x,2.35,0.6)}" stroke-width="0.6"/>')
    # 写字台 0204 0..0.78 × 2.99..4.64 高 0.75 + 三屏
    B.append(obox(0.05, 3.0, 0.8, 4.6, 0.7, 0.75, 1.1, side_hatch=False))
    B.append(f'<path d="M{ob(0.1,3.0,0.75)} L{ob(0.1,3.0,0)} M{ob(0.75,4.6,0.75)} L{ob(0.75,4.6,0)} M{ob(0.1,4.6,0.75)} L{ob(0.1,4.6,0)}" stroke-width="0.9"/>')
    for y in (3.2, 3.7, 4.2):
        B.append(f'<path d="M{ob(0.08,y,0.8)} L{ob(0.08,y+0.4,0.8)} L{ob(0.08,y+0.4,1.15)} L{ob(0.08,y,1.15)} Z" stroke-width="0.9"/>')
    B.append(f'<path d="M{ob(0.3,3.5,0.75)} L{ob(0.3,3.5,0.72)}" stroke-width="0.6"/>')
    # 98 寸电视（南墙，梁下）0.97..3.1，z 0.5..1.75
    B.append(f'<path d="M{ob(0.97,D-0.05,0.5)} L{ob(3.1,D-0.05,0.5)} L{ob(3.1,D-0.05,1.75)} L{ob(0.97,D-0.05,1.75)} Z" stroke-width="1.5"/>')
    B.append(f'<path d="M{ob(1.05,D-0.05,0.58)} L{ob(3.02,D-0.05,0.58)} L{ob(3.02,D-0.05,1.67)} L{ob(1.05,D-0.05,1.67)} Z" fill="{HL}" stroke="none"/>')
    B.append(f'<path d="M{ob(1.4,D-0.05,0.9)} l14 -12 l10 8 l12 -14 l14 10" stroke-width="0.8"/>')
    # 门（东南角）0.9 宽，画在南墙剖切处：门扇开启弧
    B.append(f'<path d="M{ob(3.93,D,0)} L{ob(4.74,D,0)}" stroke-width="2.2"/><path d="M{ob(3.93,D,0)} L{ob(3.93,D-0.85,0)}" stroke-width="1"/><path d="M{ob(3.93,D-0.85,0)} Q{ob(4.5,D-0.7,0)} {ob(4.74,D,0)}" stroke-width="0.7" stroke-dasharray="3 3"/>')
    # 东墙、南墙（剖到 1.0 高，最后画）
    B.append(f'<path d="M{ob(W,0,WC)} L{ob(W,D,WC)} L{ob(W,D,0)} M{ob(W,D,WC)} L{ob(0,D,WC)}" stroke-width="1.5"/>')
    B.append(f'<path d="M{ob(W,0,WC)} L{ob(W,D,WC)} L{ob(W-0.1,D,WC)} L{ob(W-0.1,0,WC)} Z M{ob(W,D,WC)} L{ob(0,D,WC)} L{ob(0,D-0.1,WC)} L{ob(W,D-0.1,WC)} Z" fill="{H}" stroke="none"/>')
    # 0201 滑轨（贴梁，南墙上方）示意：一根轨道 + 灯头
    B.append(f'<path d="M{ob(0.6,D-0.3,2.35)} L{ob(4.2,D-0.3,2.35)}" stroke-width="1.3"/><path d="M{ob(2.2,D-0.3,2.35)} l0 8 l-6 6 l12 0 Z" stroke-width="1"/><path d="M{ob(2.2,D-0.3,2.0)} l-14 22 M{ob(2.2,D-0.3,2.0)} l14 22" stroke-width="0.5" stroke-dasharray="2 2"/><path d="M{ob(0.6,D-0.3,2.35)} L{ob(0.6,D-0.3,2.4)} L{ob(4.2,D-0.3,2.4)} L{ob(4.2,D-0.3,2.35)}" stroke-width="0.6" stroke-dasharray="3 2"/>')
    # 人（一个人坐沙发）—— 简化：站在地毯旁
    fx, fy = ob(2.9, 3.4, 0).split()
    B.append(figure(float(fx), float(fy), 0.85))
    body = "\n".join(B)
    def L(x,y,z,t,size=8):
        X,Y = ob(x,y,z).split(); return label(float(X), float(Y), t, size, "middle")
    labels = "\n".join([
        label(96, 40, "架空床 200×120 · 床板 1750", 8, "middle"), label(96, 52, "床下 1.2×1.5 帐篷 = 0209", 8, "middle"),
        L(2.3, -0.3, 2.1, "书架", 7.5), L(1.9, 1.7, 1.15, "沙发", 7.5), L(2.3, 3.2, 0.05, "地毯", 7.5),
        L(0.4, 5.15, 0.9, "0204", 7.5), L(0.6, 2.5, 2.0, "衣架", 7.5),
        L(4.05, 0.65, 0.55, "卫生间 0202", 7.5), L(4.05, 2.55, 0.9, "储藏室 0210", 7.5),
        label(70, 248, "南墙梁下 98 寸电视 0207", 8, "middle"), L(4.4, 5.45, 0.1, "门", 7.5),
        label(60, 118, "0201 日轨 · 贴梁 2400", 7.5, "middle"),
        label(200, 292, "地堡 · 4.85 × 5.00 m · 无窗 · 墙剖到 1 米看进去，北在上方", 10, "middle", "#1c1c1c"),
    ])
    return illo("marea-02", body, "area-02", seed=9).replace("</svg>", labels + "\n</svg>")

if __name__ == "__main__":
    open("illos/area-02.svg", "w", encoding="utf-8").write(area02()); print("ok")
