from sk import *
H = "url(#marea-01-hatch)"; HL = "url(#marea-01-hatchl)"

VPX, VPY, K = 210, 150, 1.52
def P(x, y, t):
    f = 1 + t*(K-1)
    return f"{VPX + f*(x-VPX):.1f} {VPY + f*(y-VPY):.1f}"

def area01():
    # 一点透视：北墙为背墙 x90..330（5m=240px，48px/m），地面 y=200，顶 y=72；梁底 2400 → y=85
    bx0, bx1, fy, ty = 90, 330, 200, 72
    beam = 85
    B = []
    # 房间框架：背墙 + 四条透视线到前框
    B.append(f'<path d="M{bx0} {ty} H{bx1} V{fy} H{bx0} Z" stroke-width="1.9"/>')
    B.append(f'<path d="M{bx0} {ty} L{P(bx0,ty,1)} M{bx1} {ty} L{P(bx1,ty,1)} M{bx0} {fy} L{P(bx0,fy,1)} M{bx1} {fy} L{P(bx1,fy,1)}" stroke-width="1.5"/>')
    B.append(f'<path d="M{P(bx0,ty,1)} L{P(bx0,fy,1)} M{P(bx1,ty,1)} L{P(bx1,fy,1)}" stroke-width="1.2"/>')
    # 梁（背墙顶部一条带）+ 天花板线
    B.append(f'<path d="M{bx0} {beam} H{bx1}" stroke-width="1.4"/><path d="M{bx0+2} {ty+2} h{bx1-bx0-4} v{beam-ty-4} h{-(bx1-bx0-4)} Z" fill="{HL}" stroke="none"/>')
    B.append(f'<path d="M{bx0} {beam} L{P(bx0,beam,1)} M{bx1} {beam} L{P(bx1,beam,1)}" stroke-width="0.9"/>')
    # 地板木纹
    for i in range(1, 6):
        t = i / 6
        B.append(f'<path d="M{P(bx0,fy,t)} L{P(bx1,fy,t)}" stroke-width="0.6"/>')
    # 北墙木板缝
    for y in range(96, 200, 14):
        B.append(f'<path d="M{bx0+2} {y} H{bx1-2}" stroke-width="0.5"/>')
    # 0107 吧台矮柜 x90..210, 900 高 → y157
    B.append(f'<rect x="{bx0}" y="157" width="120" height="43" stroke-width="1.6"/><path d="M{bx0} 157 l-16 9 v43 l16 -9 M{bx0-16} 166 h0" stroke-width="1.1"/>')
    B.append(f'<path d="M{bx0-15} 168 v40 l14 -8 v-40 Z" fill="{H}" stroke="none"/>')
    B.append(f'<path d="M120 160 v37 M150 160 v37 M180 160 v37 M125 178 h4 M155 178 h4 M185 178 h4" stroke-width="0.8"/>')
    # 台面电器：管线机、制冰机、咖啡机、0205 鱼缸(x167..205, y128..157)
    B.append('<rect x="96" y="138" width="14" height="19" rx="2" stroke-width="1"/><rect x="114" y="141" width="18" height="16" rx="2" stroke-width="1"/><path d="M136 143 h18 v14 h-18 Z M140 143 v-5 h10 v5" stroke-width="1"/>')
    B.append('<rect x="163" y="130" width="42" height="27" stroke-width="1.4"/><path d="M165 136 q10 -3 20 0 t18 0 M170 150 q5 -8 10 0 M186 147 l6 -3 l-6 -3 Z" stroke-width="0.8"/><path d="M165 132 h38 v3 h-38 Z" fill="' + H + '" stroke="none"/>')
    # 0103 电子画框墙 3×3 x96..154 y85..128
    B.append('<rect x="96" y="86" width="58" height="42" stroke-width="1.5"/>')
    for i in range(3):
        for j in range(3):
            B.append(f'<rect x="{99+i*18.5}" y="{89+j*13.3}" width="16" height="11" stroke-width="0.7"/>')
    B.append('<path d="M101 96 l4 -4 l4 4 M120 108 q3 -4 6 0 M137 94 a2 2 0 1 0 0.1 0" stroke-width="0.6"/>')
    # 0104 照片墙 x158..206 y85..128：三行麻绳夹片
    for r, y in enumerate((92, 106, 120)):
        B.append(f'<path d="M159 {y} q24 3 48 0" stroke-width="0.7"/>')
        for k in range(4):
            B.append(f'<rect x="{163+k*11}" y="{y}" width="8" height="7" stroke-width="0.6"/>')
    # 0102 作品展示墙 3×3 x216..302 y87..152
    B.append('<rect x="216" y="87" width="64" height="65" stroke-width="1.5"/>')
    for i in range(3):
        for j in range(3):
            x = 219 + i * 20.5; y = 90 + j * 20.5
            B.append(f'<rect x="{x}" y="{y}" width="18" height="18" stroke-width="0.7"/><rect x="{x+4}" y="{y+7}" width="10" height="6" rx="1" stroke-width="0.7"/>')
    # 0101 主产品展示 x216..302 y157..190（挂墙矮展台，盒子掀盖）
    B.append('<rect x="216" y="160" width="64" height="30" stroke-width="1.4"/><path d="M216 160 l-8 5 v30 l8 -5" stroke-width="1"/><path d="M209 166 v28 l6 -4 v-28 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M234 178 h26 v9 h-26 Z M234 178 l4 -11 h26 l-4 11" stroke-width="1.1"/><path d="M238 182 h4 M244 182 h5 M251 182 h6 M238 168 h18" stroke-width="0.6"/>')
    B.append('<path d="M248 152 v6 M242 158 h12" stroke-width="0.8"/><path d="M248 158 l-10 12 M248 158 l10 12" stroke-width="0.5" stroke-dasharray="2 2"/>')
    # 梯子床（东墙）x284..330，床板 1850 → y=111，向前延伸到 x ~380
    tb = 0.9  # 床进深 1.85/2.0
    B.append(f'<path d="M284 111 H330 L{P(330,111,tb)} L{P(284,111,tb)} Z" stroke-width="1.6"/><path d="M286 113 h42 L{P(328,113,tb)}" stroke-width="0.8"/>')
    B.append(f'<path d="M290 111 v-8 h36 v8 M330 111 v-8 M{P(330,111,tb)} v-8" stroke-width="1"/>')
    B.append('<path d="M286 104 h38 v6 h-38 Z" fill="' + H + '" stroke="none"/>')
    # 床腿 + 梯子（在床的南端）
    B.append(f'<path d="M330 111 V200 M{P(330,111,tb)} L{P(330,200,tb)} M284 111 V200 M{P(284,111,tb)} L{P(284,200,tb)}" stroke-width="1.3"/>')
    lx0, ly0 = P(300,111,tb).split(); lx1, ly1 = P(300,200,tb).split()
    B.append(f'<path d="M{float(lx0)-5} {ly0} L{float(lx1)-5} {ly1} M{float(lx0)+5} {ly0} L{float(lx1)+5} {ly1}" stroke-width="1"/>')
    for k in range(1,6):
        yy = float(ly0) + (float(ly1)-float(ly0))*k/6; xx = float(lx0) + (float(lx1)-float(lx0))*k/6
        B.append(f'<path d="M{xx-5:.1f} {yy:.1f} h10" stroke-width="0.9"/>')
    # 床下 0105 写字台（沿东墙）260×70，台面 0.75m → y=164
    B.append(f'<path d="M296 164 H330 L{P(330,164,0.85)} L{P(296,164,0.85)} Z" stroke-width="1.3"/><path d="M296 164 V200 M{P(296,164,0.85)} L{P(296,200,0.85)}" stroke-width="0.9"/>')
    B.append('<rect x="304" y="150" width="14" height="10" stroke-width="0.8"/><path d="M311 160 v4 M305 164 h12" stroke-width="0.7"/>')
    # 床下暗门（北墙，虚线）x292..322 y111..200
    B.append('<path d="M294 200 V115 H322 V200" stroke-width="1" stroke-dasharray="4 3"/><circle cx="318" cy="160" r="1.5" stroke-width="0.8"/>')
    # 西墙空调（左墙高处）
    B.append(f'<path d="M{P(90,84,0.75)} L{P(90,84,0.35)} L{P(90,100,0.35)} L{P(90,100,0.75)} Z" stroke-width="1.2"/><path d="M{P(90,92,0.72)} L{P(90,92,0.38)} M{P(90,97,0.72)} L{P(90,97,0.38)}" stroke-width="0.6"/>')
    # 西南角 0106 柴火炉（前左）+ 烟囱
    B.append('<rect x="46" y="176" width="30" height="40" stroke-width="1.6"/><rect x="51" y="184" width="20" height="16" rx="2" stroke-width="1"/><path d="M56 197 q5 -11 10 0 M59 195 q2 -5 4 0" stroke-width="0.8"/>')
    B.append('<path d="M48 203 h26 v11 h-26 Z" fill="' + H + '" stroke="none"/><path d="M42 216 h38 M46 216 v5 M76 216 v5" stroke-width="1.2"/>')
    B.append('<path d="M57 176 v-8 h8 v8 M59 168 V40 h4 V168" stroke-width="1.3"/><path d="M60 36 q4 -8 0 -14 M65 32 q4 -8 0 -12" stroke-width="0.8"/>')
    B.append('<path d="M82 204 l12 -6 M82 212 l12 -6" stroke-width="0.7"/><circle cx="87" cy="207" r="3" stroke-width="0.8"/><circle cx="87" cy="214" r="3" stroke-width="0.8"/>')
    # 人（一个人，站在吧台前）
    B.append(figure(118, 224, 0.95))
    
    # 南墙门窗暗示：前框左右两侧竖条

    body = "\n".join(B)
    labels = "\n".join([
        label(150, 188, "0107 吧台 · 900 高", 8, "middle"),
        label(125, 66, "0103 画框墙", 8.5, "middle"), label(182, 66, "0104 照片墙", 8.5, "middle"),
        label(248, 66, "0102 作品墙", 8.5, "middle"), label(248, 202, "0101 主产品", 7.5, "middle"),
        label(186, 127, "0205", 7.5, "middle"),
        label(356, 40, "梁底 2400", 8, "middle"), label(356, 92, "梯子床 1850", 8, "middle"),
        label(308, 194, "暗门", 7.5, "middle"), label(345, 176, "0105", 8, "middle"),
        label(62, 234, "0106 炉区", 8, "middle"), label(48, 118, "空调", 8, "middle"),
        label(210, 262, "暖村木屋 · 2.00 × 5.00 m · 自南向北看", 10, "middle", "#1c1c1c"),
    ])
    svg = illo("marea-01", body, "area-01", seed=5)
    return svg.replace("</svg>", labels + "\n</svg>")

if __name__ == "__main__":
    open("illos/area-01.svg", "w", encoding="utf-8").write(area01())
    print("ok")
