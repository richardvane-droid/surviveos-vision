from sk import *
K=66  # px/m

def m0105():
    pfx="m0105"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 东墙立面（自西向东看）：宽 2.0m → 132px 居中 x 134..266；地 y=250；顶 2.66 → y=74；梁在北侧不画
    x0,x1,fy=134,266,250
    B.append(f'<path d="M{x0} 74 H{x1} V{fy} H{x0} Z" stroke-width="1.8"/>')
    B.append(f'<path d="M{x0} 74 L60 30 M{x1} 74 L340 30 M{x0} {fy} L60 290 M{x1} {fy} L340 290 M60 30 V290 M340 30 V290" stroke-width="1.2"/>')
    # 东墙木板缝
    for y in range(90,250,14): B.append(f'<path d="M{x0+2} {y} H{x1-2}" stroke-width="0.4"/>')
    # 梯子床：宽 0.9（沿北墙 x 方向）——在这个视角里床是贴东墙、进深 1.85 朝观者伸来；床板 1850 → y=250-122=128
    # 画床板为一块从东墙伸向观者的平面（透视）
    B.append(f'<path d="M{x0+6} 128 H{x1-6} L{x1+52} 96 H{x0-52} Z" stroke-width="1.6"/><path d="M{x0-52} 96 v-8 h{x1-x0+104} v8" stroke-width="1.1"/>')
    B.append(f'<path d="M{x0-50} 90 h{x1-x0+100} v5 h-{x1-x0+100} Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M{x0+6} 128 V250 M{x1-6} 128 V250 M{x0-52} 96 V282 M{x1+52} 96 V282" stroke-width="1.3"/>')
    # 梯子（南端，右前方）
    B.append(f'<path d="M{x1+30} 100 V280 M{x1+42} 100 V280" stroke-width="1"/>')
    for y in range(120,280,24): B.append(f'<path d="M{x1+30} {y} h12" stroke-width="0.9"/>')
    # 床底灯带（床板下沿）
    B.append(f'<path d="M{x0+20} 132 H{x1-20}" stroke-width="0.8" stroke-dasharray="3 2"/><path d="M{x0+40} 134 l-8 20 M{x0+80} 134 l0 20 M{x1-40} 134 l8 20" stroke-width="0.4" stroke-dasharray="2 2"/>')
    # 写字台 260×70：台面 0.75 → y=200；沿东墙，进深 0.7 朝观者
    B.append(f'<path d="M{x0+4} 200 H{x1-4} L{x1+26} 184 H{x0-26} Z" stroke-width="1.5"/><path d="M{x0-26} 184 v6 h{x1-x0+52} v-6" stroke-width="1"/>')
    B.append(f'<path d="M{x0-24} 186 h{x1-x0+48} v3 h-{x1-x0+48} Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M{x0-22} 190 V250 M{x1+22} 190 V250 M{x0+4} 200 V250 M{x1-4} 200 V250" stroke-width="1.1"/>')
    # 27 格零件柜（台面上靠墙）
    B.append(f'<rect x="{x0+16}" y="150" width="60" height="48" stroke-width="1.2"/>')
    for i in range(3):
        for j in range(3): B.append(f'<rect x="{x0+19+i*19}" y="{153+j*15}" width="16" height="12" stroke-width="0.5"/>')
    # 台灯/机位 + 工具
    B.append(f'<path d="M{x1-30} 198 v-30 l-20 -14 M{x1-52} 154 l-8 6 l8 4" stroke-width="1"/><path d="M{x1-58} 160 l-6 22 M{x1-56} 160 l6 22" stroke-width="0.4" stroke-dasharray="2 2"/>')
    B.append(f'<path d="M{x0+90} 196 h22 v-6 h-22 Z M{x0+100} 190 v-8" stroke-width="0.9"/>')
    # 床下暗门（北墙 = 左侧墙面，虚线门框）
    B.append('<path d="M98 250 V150 L134 140 V250" stroke-width="1" stroke-dasharray="4 3"/><circle cx="126" cy="200" r="1.5" stroke-width="0.8"/>')
    # 凳子 + 人（坐着）
    B.append(f'<path d="M{x0+96} 250 v-30 h24 v30 M{x0+96} 236 h24" stroke-width="1"/>')
    B.append(f'<circle cx="{x0+108}" cy="188" r="6" stroke-width="1.2"/><path d="M{x0+108} 194 V222 M{x0+108} 200 l-16 -4 l-6 -6 M{x0+108} 200 l14 6 M{x0+108} 222 l-10 28 M{x0+108} 222 l12 28" stroke-width="1.2"/>')
    # 地板
    for i in range(1,5):
        t=i/5; B.append(f'<path d="M{x0+(60-x0)*t:.0f} {fy+40*t:.0f} H{x1+(340-x1)*t:.0f}" stroke-width="0.5"/>')
    body="\n".join(B)
    labels="\n".join([label(200,84,"梯子床 · 床板 1850",8.5,"middle"), label(200,146,"床下 0105 写字台 260×70",8,"middle"),
                      label(116,140,"暗门→地堡",7.5,"middle"), label(200,292,"木屋东端：床上睡觉，床下做生存盒",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0105", seed=21).replace("</svg>", labels+"\n</svg>")

def m0205():
    pfx="m0205"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]; fy=250; k=64  # 木屋北墙西段立面：0..3.0m → x 40..232 ... 放大：k=64px/m, x0=36
    x0=36
    X=lambda m: x0+m*k; Y=lambda mm: fy-mm*k
    # 墙面 + 梁（2400 以上）
    B.append(f'<path d="M{X(0)} {Y(2.66)} H{X(5.0)} V{fy} H{X(0)} Z" stroke-width="1.8"/>')
    B.append(f'<path d="M{X(0)} {Y(2.4)} H{X(5.0)}" stroke-width="1.3"/><path d="M{X(0)+2} {Y(2.66)+2} h{5*k-4} v{0.26*k-4} h-{5*k-4} Z" fill="{HL}" stroke="none"/>')
    for y in range(int(Y(2.3)),fy,14): B.append(f'<path d="M{X(0)+2} {y} H{X(5.0)-2}" stroke-width="0.4"/>')
    # 吧台矮柜 0..2.5m，900 高
    B.append(f'<path d="M{X(0)} {Y(0.9)} H{X(2.5)} V{fy}" stroke-width="1.6"/><path d="M{X(0)} {Y(0.9)-4} H{X(2.5)+3} v4" stroke-width="1.2"/>')
    for m in (0.6,1.2,1.8): B.append(f'<path d="M{X(m)} {Y(0.86)} V{fy-4} M{X(m-0.3)} {Y(0.5)} h8" stroke-width="0.8"/>')
    B.append(f'<path d="M{X(2.2)} {Y(0.5)} h8" stroke-width="0.8"/>')
    # 台面电器：管线机 / 制冰机 / 咖啡机 / 鱼缸 1.6..2.4m, 高 0.6
    B.append(f'<rect x="{X(0.1)}" y="{Y(0.9)-4-0.5*k}" width="{0.3*k}" height="{0.5*k}" rx="3" stroke-width="1"/><rect x="{X(0.5)}" y="{Y(0.9)-4-0.42*k}" width="{0.4*k}" height="{0.42*k}" rx="3" stroke-width="1"/><path d="M{X(1.0)} {Y(0.9)-4} v-{0.38*k} h{0.4*k} v{0.38*k} M{X(1.08)} {Y(0.9)-4-0.38*k} v-8 h{0.24*k} v8" stroke-width="1"/>')
    tx,ty,tw,th = X(1.6), Y(0.9)-4-0.6*k, 0.8*k, 0.6*k
    B.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" stroke-width="1.6"/><path d="M{tx+3} {ty+6} h{tw-6} v3 h-{tw-6} Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M{tx+6} {ty+th-4} q6 -18 3 -28 M{tx+14} {ty+th-4} q4 -14 8 -22 M{tx+tw-10} {ty+th-4} q-4 -12 -2 -20 M{tx+tw-16} {ty+th-4} q2 -10 -4 -16" stroke-width="0.8"/>')
    B.append(f'<path d="M{tx+22} {ty+18} l7 -3 l-7 -3 Z M{tx+34} {ty+26} l-7 3 l7 3 Z M{tx+8} {ty+th-8} h{tw-16}" stroke-width="0.8"/><path d="M{tx+tw-6} {ty+8} v{th-14} M{tx+tw-9} {ty+12} h3" stroke-width="0.7"/>')
    B.append(f'<path d="M{tx+tw+2} {ty+th-10} h8 v-30 M{tx+tw+10} {ty+th-40} h-6" stroke-width="0.7"/>')  # 过滤管
    # 上方：0103 画框墙 0.2..1.4m，0104 1.55..2.55m（1500..2400）
    B.append(f'<rect x="{X(0.2)}" y="{Y(2.4)+4}" width="{1.2*k}" height="{0.86*k}" stroke-width="1.3"/>')
    for i in range(3):
        for j in range(3): B.append(f'<rect x="{X(0.24)+i*0.39*k}" y="{Y(2.4)+7+j*0.28*k}" width="{0.35*k}" height="{0.25*k}" stroke-width="0.5"/>')
    for r in range(3):
        y=Y(2.4)+10+r*0.28*k; B.append(f'<path d="M{X(1.55)} {y} q30 4 60 0" stroke-width="0.6"/>')
        for q in range(4): B.append(f'<rect x="{X(1.6)+q*0.24*k}" y="{y}" width="{0.16*k}" height="{0.18*k}" stroke-width="0.5"/>')
    # 0102 作品墙从 2.6m 起（只画一列）
    B.append(f'<rect x="{X(2.6)}" y="{Y(2.35)}" width="{0.45*k}" height="{1.35*k}" stroke-width="1"/>')
    for j in range(3): B.append(f'<rect x="{X(2.63)}" y="{Y(2.32)+j*0.45*k}" width="{0.39*k}" height="{0.4*k}" stroke-width="0.5"/>')
    B.append(f'<rect x="{X(3.1)}" y="{Y(2.35)}" width="{0.45*k}" height="{1.35*k}" stroke-width="0.6" stroke-dasharray="3 3"/>')
    # 高脚凳 + 人（坐吧台前看鱼缸）
    B.append(f'<path d="M{X(3.0)-10} {fy} v-46 h20 v46 M{X(3.0)-10} {fy-20} h20" stroke-width="1"/>')
    B.append(f'<circle cx="{X(3.0)}" cy="{fy-96}" r="6" stroke-width="1.2"/><path d="M{X(3.0)} {fy-90} V{fy-60} M{X(3.0)} {fy-84} l-14 8 l-10 -4 M{X(3.0)} {fy-84} l10 10 M{X(3.0)} {fy-60} l-8 16 M{X(3.0)} {fy-60} l8 16" stroke-width="1.2"/>')
    body="\n".join(B)
    labels="\n".join([label(X(2.0)+2,ty-6,"0205 生态鱼缸 · 台面上",8,"middle"), label(X(1.2),Y(0.9)+22,"0107 吧台矮柜 · 900 高",8,"middle"),
                      label(X(0.8),Y(2.4)-6,"0103",7.5,"middle"), label(X(2.05),Y(2.4)-6,"0104",7.5,"middle"), label(X(2.83),Y(2.4)-6,"0102",7.5,"middle"),
                      label(X(4.0),Y(2.5),"梁底 2400",7.5,"middle"), label(200,292,"木屋北墙西段：缸在吧台上，人坐着看",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0205", seed=23).replace("</svg>", labels+"\n</svg>")

if __name__=="__main__":
    open("illos/0105.svg","w",encoding="utf-8").write(m0105())
    open("illos/0205.svg","w",encoding="utf-8").write(m0205())
    print("ok")
