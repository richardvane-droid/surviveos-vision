from sk import *
FONT_ = FONT

def duck(x, y, s=1.0, sw=1.3, face="right"):
    """简笔双足小鸭：脚底中心 (x,y)，高约 58*s。"""
    d = 1 if face == "right" else -1
    b = []
    b.append(f'<ellipse cx="{x:.1f}" cy="{y-24*s:.1f}" rx="{16*s:.1f}" ry="{12*s:.1f}" stroke-width="{sw}"/>')
    b.append(f'<path d="M{x+9*s*d:.1f} {y-32*s:.1f} Q{x+12*s*d:.1f} {y-40*s:.1f} {x+13*s*d:.1f} {y-44*s:.1f}" stroke-width="{sw}"/>')
    b.append(f'<circle cx="{x+14*s*d:.1f}" cy="{y-50*s:.1f}" r="{7*s:.1f}" stroke-width="{sw}"/>')
    b.append(f'<path d="M{x+21*s*d:.1f} {y-50*s:.1f} l{8*s*d:.1f} 1.5 l{-8*s*d:.1f} 2.5" stroke-width="{sw}"/>')
    b.append(f'<circle cx="{x+16*s*d:.1f}" cy="{y-52*s:.1f}" r="{1.4*s:.1f}" stroke-width="{sw*0.8}"/>')
    b.append(f'<circle cx="{x+8*s*d:.1f}" cy="{y-22*s:.1f}" r="{3.5*s:.1f}" stroke-width="{sw*0.8}"/>')
    b.append(f'<path d="M{x-4*s:.1f} {y-13*s:.1f} L{x-5*s:.1f} {y} M{x+5*s:.1f} {y-13*s:.1f} L{x+6*s:.1f} {y} M{x-11*s:.1f} {y} h{9*s:.1f} M{x+1*s:.1f} {y} h{9*s:.1f}" stroke-width="{sw}"/>')
    b.append(f'<path d="M{x-10*s:.1f} {y-26*s:.1f} q{5*s:.1f} 5 {11*s:.1f} 1" stroke-width="{sw*0.7}"/>')
    return "\n".join(b)

def area08():
    pfx="marea-08"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 三个房间的剖面小格子（左：阁楼坡顶，中：地堡，右下：木屋），之间用通道/坡道连起来，上方一层“信息云”
    # 阁楼（左上）
    B.append('<path d="M20 150 L70 100 L120 150 Z M28 150 H112" stroke-width="1.6"/><path d="M40 150 v-14 h30 v14 M46 136 h18" stroke-width="1"/>')
    # 楼梯口坡道 → 地堡
    B.append('<path d="M120 150 L150 170" stroke-width="1.3"/><path d="M122 154 L148 172" stroke-width="0.6"/>')
    # 地堡（中）
    B.append('<path d="M150 118 H270 V208 H150 Z" stroke-width="1.8"/><path d="M152 120 h116 v6 h-116 Z" fill="' + HL + '" stroke="none"/>')
    B.append('<path d="M160 208 v-10 h30 v10 M200 190 h40 v18 h-40 Z M158 130 v40 h6 v-40 Z" stroke-width="1"/><path d="M270 196 v12 h-12" stroke-width="1"/>')
    # 地堡门下通道 → 木屋
    B.append('<path d="M270 200 h20 M290 200 V226" stroke-width="1"/>')
    # 木屋（右下）
    B.append('<path d="M290 168 H380 V226 H290 Z" stroke-width="1.6"/><path d="M296 226 v-18 h40 v18 M300 214 h32" stroke-width="1"/><path d="M366 226 v-30 h10 v30" stroke-width="0.9"/>')
    # 三只鸭子位置：木屋吧台脚边（主）、地堡地毯（虚线幽灵）、阁楼（虚线）
    B.append(duck(362, 226, 0.5, 1.2, "left"))
    B.append('<g stroke-dasharray="2 2">' + duck(178, 206, 0.45, 0.9) + '</g>')
    B.append('<g stroke-dasharray="2 2">' + duck(95, 148, 0.4, 0.9) + '</g>')
    B.append('<path d="M110 150 Q140 175 175 206 Q220 214 300 222" stroke-width="0.7" stroke-dasharray="4 3"/>')
    # 信息云：上方一朵大云 + 从各房间上升的虚线 + 云里的小图标（箱子/屏/搜索）
    B.append('<path d="M100 62 q-30 0 -28 -22 q2 -22 30 -18 q10 -22 40 -14 q22 -12 44 6 q30 -8 40 14 q26 4 22 24 q-4 16 -26 12 Z" stroke-width="1.6"/>')
    B.append('<path d="M104 60 q-24 0 -22 -18" stroke-width="0.7"/>')
    B.append('<path d="M92 58 h18 v14 h-18 Z M95 62 h12 M95 66 h8" stroke-width="0.9"/>')   # 箱子
    B.append('<path d="M120 40 h30 v20 h-30 Z M124 50 l6 -6 l5 5 l8 -8 l5 5" stroke-width="0.9"/>')  # 曲线屏
    B.append('<circle cx="176" cy="46" r="6" stroke-width="1"/><path d="M180 50 l6 6" stroke-width="1.2"/>')  # 搜索
    B.append('<path d="M200 44 h12 M200 50 h20 M200 56 h16" stroke-width="0.8"/>')
    B.append('<path d="M212 40 v-4 h8 v4 M216 36 v-6" stroke-width="0.8"/>')
    # 上升虚线：房间 → 云
    for (x0,y0,x1,y1) in ((70,100,110,74),(210,118,175,72),(335,168,236,70)):
        B.append(f'<path d="M{x0} {y0} Q{(x0+x1)/2} {(y0+y1)/2-10} {x1} {y1}" stroke-width="0.7" stroke-dasharray="3 3"/>')
        B.append(f'<path d="M{x1-4} {y1+4} l4 -4 l4 4" stroke-width="0.8"/>')
    # 云下方的手机（分身）
    B.append('<path d="M300 92 h22 v40 h-22 Z M304 96 h14 v30 h-14 Z" stroke-width="1"/><path d="M306 104 l4 -4 l3 3 l5 -6" stroke-width="0.6"/>')
    B.append('<path d="M262 76 Q285 84 300 100" stroke-width="0.6" stroke-dasharray="3 3"/>')
    # 人（木屋里，一个人）
    B.append(figure(318, 226, 0.85))
    # 地面
    B.append('<path d="M14 232 Q200 226 386 230" stroke-width="1.2"/>')
    body="\n".join(B)
    labels="\n".join([label(70, 164, "03/04 阁楼", 8, "middle"), label(210, 222, "02 地堡", 8, "middle"), label(335, 240, "01 木屋", 8, "middle"),
                      label(150, 14, "0801 数字孪生 · 0802 中枢", 8.5, "middle"), label(311, 146, "手机分身", 7.5, "middle"),
                      label(352, 160, "0803 miniduck", 8, "middle"),
                      label(200, 262, "虚拟空间 · 一层看不见的信息，一只到处走的鸭", 10, "middle", "#1c1c1c"),
                      label(200, 278, "硬件落在房间里，服务的是整座园子", 8.5, "middle")])
    return illo(pfx, body, "area-08", seed=61).replace("</svg>", labels+"\n</svg>")

def m0803():
    pfx="m0803"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 木屋内一角：北墙（左侧梯子床下的暗门）+ 吧台脚边，鸭子从暗门底下钻出来
    # 地面
    B.append('<path d="M14 244 H386" stroke-width="1.6"/>')
    for i in range(1,5): B.append(f'<path d="M{20+i*20} 244 l-6 20" stroke-width="0.4"/>')
    # 北墙木板缝
    for y in range(60, 240, 14): B.append(f'<path d="M40 {y} H360" stroke-width="0.4"/>')
    # 梯子床（左上）床板 + 腿 + 梯子
    B.append('<path d="M40 96 H124 M40 90 H124 M44 96 V244 M120 96 V244" stroke-width="1.4"/><path d="M42 90 h80 v5 h-80 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M104 96 V244 M114 96 V244 M104 120 h10 M104 150 h10 M104 180 h10 M104 210 h10" stroke-width="0.9"/>')
    # 暗门（虚线）+ 底下 12cm 通道
    B.append('<path d="M50 244 V124 H98 V244" stroke-width="1" stroke-dasharray="4 3"/><circle cx="93" cy="186" r="1.5" stroke-width="0.8"/>')
    B.append('<path d="M54 244 v-14 h42 v14" stroke-width="1.2"/><path d="M56 242 h38 v-10 h-38 Z" fill="' + HL + '" stroke="none"/>')
    # 写字台（床下）
    B.append('<path d="M46 186 H100 M46 186 V244 M50 190 h46 v10 h-46 Z" stroke-width="1"/>')
    # 吧台矮柜（右侧）900 高 → 从地面 244 到 190
    B.append('<path d="M230 244 V190 H386 M230 190 l-6 3 v51" stroke-width="1.6"/><path d="M226 194 v48 l4 -2 v-48 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M270 194 V240 M310 194 V240 M350 194 V240 M280 218 h6 M320 218 h6 M360 218 h6" stroke-width="0.8"/>')
    # 台面电器 + 咖啡杯
    B.append('<path d="M240 190 v-22 h18 v22 M262 190 v-16 h22 v16 M290 190 v-26 h40 v26 M296 170 q10 -4 20 0 M300 182 l6 -3 l-6 -3 Z" stroke-width="1"/>')
    B.append('<path d="M340 190 v-8 h10 v8 M350 185 q5 0 5 4" stroke-width="0.9"/>')
    # 高脚凳 + 人（坐着低头看鸭子）
    B.append('<path d="M198 244 v-46 h20 v46 M198 224 h20" stroke-width="1"/>')
    B.append('<circle cx="208" cy="152" r="6" stroke-width="1.2"/><path d="M208 158 V190 M208 166 l-14 14 M208 166 l14 8 M208 190 l-8 18 M208 190 l10 18" stroke-width="1.2"/>')
    B.append('<path d="M194 180 l-6 6" stroke-width="0.9"/>')
    # 鸭子从通道钻出来，仰头看人（大）
    B.append(duck(150, 244, 1.05, 1.5, "right"))
    B.append('<path d="M176 178 l3 -5 M182 182 l4 -4" stroke-width="0.7"/>')
    # 胸口屏数字 + 对话气泡
    B.append('<path d="M132 130 q0 -10 10 -10 h52 q10 0 10 10 v18 q0 10 -10 10 h-24 l-8 10 v-10 h-20 q-10 0 -10 -10 Z" stroke-width="1"/>')
    # 充电小窝（角落）
    B.append('<path d="M330 244 a16 8 0 0 1 32 0 Z" stroke-width="1"/><path d="M334 244 a12 5 0 0 1 24 0" stroke-width="0.6"/><path d="M346 232 l-3 6 h6 l-3 6" stroke-width="0.8"/>')
    body="\n".join(B)
    labels="\n".join([label(168, 142, "+310L", 9, "middle"), label(168, 154, "够草地喝一星期", 7, "middle"),
                      label(74, 116, "暗门 · 12cm 通道", 7.5, "middle"), label(82, 82, "梯子床", 8, "middle"),
                      label(308, 254, "0107 吧台", 7.5, "middle"), label(346, 224, "充电窝", 7, "middle"),
                      label(200, 278, "0803 miniduck：从暗门底下钻过来，仰头汇报一句", 9.5, "middle", "#1c1c1c")])
    return illo(pfx, body, "0803", seed=63).replace("</svg>", labels+"\n</svg>")

# ---------- parts ----------
def SH(pfx): return f"url(#{pfx}-shade)"
def along(i, n, x0=110, y0=300, x1=380, y1=60):
    t = i/(n-1); return x0+(x1-x0)*t, y0+(y1-y0)*t
def finish(svg, legend, C, note):
    svg = svg.replace('<g font-size="8.5" fill="#444"></g>', '<g font-size="8.5" fill="#444">'+"".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i,(n,t) in enumerate(legend))+'</g>')
    return svg.replace('</svg>', "\n".join(C)+f'\n<text x="16" y="{46+len(legend)*13+6}" font-size="8" fill="#888" font-style="italic">{note}</text>\n</svg>')

def p0803_1():
    pfx="p0803-1"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n)  # 1 脚 + 小腿 + TPU 脚垫
    B.append(f'<path d="M{x-46} {y} h26 l6 -6 h-26 Z M{x+14} {y-4} h26 l6 -6 h-26 Z" stroke-width="1.3"/><path d="M{x-44} {y-1} h22 l4 -4 h-22 Z M{x+16} {y-5} h22 l4 -4 h-22 Z" fill="{SH(pfx)}" stroke="none"/>')
    B.append(f'<path d="M{x-30} {y-6} v-26 M{x+30} {y-10} v-26 M{x-34} {y-32} h8 v-8 h-8 Z M{x+26} {y-36} h8 v-8 h-8 Z" stroke-width="1.2"/>')
    x,y=along(1,n)  # 2 大腿舵机组 ×2
    for dx in (-30, 24):
        B.append(f'<path d="M{x+dx} {y-10} h18 v22 h-18 Z M{x+dx+18} {y-10} l6 -4 v22 l-6 4" stroke-width="1.2"/><path d="M{x+dx+19} {y-9} l4 -3 v20 l-4 3 Z" fill="{SH(pfx)}" stroke="none"/><circle cx="{x+dx+9}" cy="{y+1}" r="4" stroke-width="0.8"/><path d="M{x+dx+9} {y-14} v4" stroke-width="0.8"/>')
    B.append(f'<path d="M{x-12} {y+1} h36" stroke-width="0.6" stroke-dasharray="2 2"/>')
    x,y=along(2,n)  # 3 胸腔：主控 + IMU + 电池 + 线圈
    B.append(f'<path d="M{x-36} {y-14} h60 v30 h-60 Z M{x+24} {y-14} l10 -6 v30 l-10 6" stroke-width="1.4"/><path d="M{x+25} {y-13} l8 -5 v28 l-8 5 Z" fill="{SH(pfx)}" stroke="none"/>')
    B.append(f'<path d="M{x-30} {y-8} h20 v10 h-20 Z M{x-26} {y-4} h4 M{x-20} {y-4} h4 M{x-4} {y-8} h22 v14 h-22 Z M{x-2} {y-2} h18 M{x-2} {y+2} h18" stroke-width="0.8"/>')
    B.append(f'<circle cx="{x-6}" cy="{y+22}" r="7" stroke-width="0.8"/><circle cx="{x-6}" cy="{y+22}" r="4" stroke-width="0.6"/>')
    x,y=along(3,n)  # 4 颈舵机 ×3 + 头舵机 ×2
    B.append(f'<path d="M{x-14} {y+6} h12 v14 h-12 Z M{x-8} {y+6} v-10 M{x-14} {y-16} h12 v6 h-12 Z M{x-8} {y-16} v-8 M{x-12} {y-30} h8 v6 h-8 Z" stroke-width="1.1"/>')
    B.append(f'<path d="M{x+10} {y-6} h14 v12 h-14 Z M{x+30} {y-2} h12 v10 h-12 Z" stroke-width="1.1"/><circle cx="{x+17}" cy="{y}" r="3" stroke-width="0.7"/><circle cx="{x+36}" cy="{y+3}" r="2.5" stroke-width="0.7"/>')
    x,y=along(4,n)  # 5 外壳（蛋形身 + 头壳）
    B.append(f'<path d="M{x-24} {y+6} a24 20 0 1 0 48 0 a24 20 0 1 0 -48 0" stroke-width="1.4"/><path d="M{x-22} {y+6} a22 18 0 0 0 44 0" stroke-width="0.5"/><path d="M{x-10} {y+22} a10 5 0 0 0 20 0 v-4 a10 5 0 0 1 -20 0 Z" fill="{SH(pfx)}" stroke="none"/>')
    B.append(f'<circle cx="{x+40}" cy="{y-10}" r="12" stroke-width="1.3"/><path d="M{x+52} {y-10} l10 3 l-10 3" stroke-width="1"/><circle cx="{x+43}" cy="{y-13}" r="1.5" stroke-width="0.7"/>')
    for i,(dx,dy) in enumerate([(-50,-8),(-34,-14),(-40,-18),(-18,-24),(-28,-4)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-32,y+dy-6,i+1); L.append(l); C.append(c)
    legend=[(1,"脚板 + 小腿 · 脚底 TPU 防滑垫"),(2,"髋/膝总线舵机组 ×2×5，一根串行线"),(3,"胸腔：RK3566 主控 + IMU + 3S 2,000mAh + 无线充电线圈"),(4,"颈舵机 ×3 + 头舵机 ×2"),(5,"拓竹打印 PETG 外壳（换季换羽）")]
    svg=exploded(pfx,"双足鸭身总成","",("\n".join(B)),"0803-1",axis="M100 318 L392 40",seed=65,leaders="\n".join(L))
    return finish(svg, legend, C, "25cm 高 · 约 800g · 重物压低才站得稳")

def p0803_2():
    pfx="p0803-2"; B=[]; L=[]; C=[]; n=5
    x,y=along(0,n)  # 1 头壳底座 + 泡棉隔震
    B.append(f'<path d="M{x-30} {y-8} a30 10 0 1 0 60 0 a30 10 0 1 0 -60 0" stroke-width="1.3"/><path d="M{x-30} {y-8} v10 a30 10 0 0 0 60 0 v-10" stroke-width="1"/><path d="M{x-26} {y+2} a26 8 0 0 0 52 0 v-3 a26 8 0 0 1 -52 0 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x-24} {y-8} q6 -4 12 0 t12 0 t12 0 t12 0" stroke-width="0.6"/>')
    x,y=along(1,n)  # 2 ESP32-S3 语音板
    B.append(f'<path d="M{x-28} {y-10} h44 v24 h-44 Z" stroke-width="1.2"/><path d="M{x-22} {y-4} h14 v10 h-14 Z M{x-2} {y-6} h12 M{x-2} {y-2} h12 M{x-2} {y+2} h12 M{x-2} {y+6} h12" stroke-width="0.7"/><path d="M{x-28} {y-2} h-6 M{x-28} {y+4} h-6 M{x+16} {y-2} h6 M{x+16} {y+4} h6" stroke-width="0.6"/>')
    x,y=along(2,n)  # 3 胸口圆屏（放这里代表表情/数据窗）+ 眼睛 LED
    B.append(f'<circle cx="{x-10}" cy="{y}" r="14" stroke-width="1.3"/><circle cx="{x-10}" cy="{y}" r="11" stroke-width="0.6"/><path d="M{x-17} {y+2} l4 -4 l4 3 l5 -6" stroke-width="0.8"/>')
    B.append(f'<circle cx="{x+22}" cy="{y-8}" r="5" stroke-width="1.1"/><circle cx="{x+38}" cy="{y-8}" r="5" stroke-width="1.1"/><circle cx="{x+22}" cy="{y-8}" r="2" stroke-width="0.6"/><circle cx="{x+38}" cy="{y-8}" r="2" stroke-width="0.6"/><path d="M{x+22} {y-3} v6 M{x+38} {y-3} v6" stroke-width="0.6"/>')
    x,y=along(3,n)  # 4 广角摄像头模组
    B.append(f'<path d="M{x-16} {y-12} h28 v22 h-28 Z" stroke-width="1.2"/><circle cx="{x-2}" cy="{y-1}" r="7" stroke-width="1"/><circle cx="{x-2}" cy="{y-1}" r="3.5" stroke-width="0.7"/><path d="M{x-2} {y-8} v-4 M{x+12} {y-1} h6" stroke-width="0.6"/><path d="M{x+6} {y-1} l30 -14 M{x+6} {y-1} l30 14" stroke-width="0.4" stroke-dasharray="2 2"/>')
    x,y=along(4,n)  # 5 4 麦环形阵列
    B.append(f'<path d="M{x-24} {y} a24 9 0 1 0 48 0 a24 9 0 1 0 -48 0" stroke-width="1.3"/>')
    for dx,dy in ((-18,-3),(18,-3),(-8,6),(8,6)): B.append(f'<circle cx="{x+dx}" cy="{y+dy}" r="2.5" stroke-width="0.8"/>')
    B.append(f'<path d="M{x} {y-9} v-8 M{x-3} {y-14} l3 -3 l3 3" stroke-width="0.7"/>')
    for i,(dx,dy) in enumerate([(-34,-12),(-32,-14),(-28,-16),(-20,-16),(-28,-6)]):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-32,y+dy-6,i+1); L.append(l); C.append(c)
    legend=[(1,"头壳底座 + 泡棉隔震圈（隔开舵机噪音）"),(2,"ESP32-S3 语音协处理器（xiaozhi 固件）"),(3,"胸口 1.28 寸圆屏 + 眼睛 RGB LED ×2"),(4,"广角摄像头 120°：认标记、认一个人"),(5,"4 麦环形阵列，本地唤醒词")]
    svg=exploded(pfx,"头部感知与表情模组","",("\n".join(B)),"0803-2",axis="M100 318 L392 40",seed=67,leaders="\n".join(L))
    return finish(svg, legend, C, "听、看、表情各一套，语音卡了不影响走路")

def flow(pfx, title, nodes, edges, texts, sig, seed):
    """nodes: list of (kind,x,y,w,h); kinds: pill/step/dia/db/end"""
    B=[]; SHD=f"url(#{pfx}-shade)"
    for k,x,y,w,h in nodes:
        if k=="pill": B.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}"/>')
        elif k=="step": B.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/><rect x="{x+2}" y="{y+2}" width="{w-4}" height="{h-4}" rx="5" stroke-width="0.5"/><path d="M{x+4} {y+h+2} h{w-4} v3 h-{w-4} Z" fill="{SHD}" stroke="none"/>')
        elif k=="dia": B.append(f'<path d="M{x+w/2} {y} l{w/2} {h/2} l-{w/2} {h/2} l-{w/2} -{h/2} Z"/><path d="M{x+w/2+2} {y+h} l{w/2-2} -{h/2} l4 2 l-{w/2} {h/2+2} Z" fill="{SHD}" stroke="none"/>')
        elif k=="db": B.append(f'<path d="M{x} {y+6} a{w/2} 6 0 0 1 {w} 0 v{h-12} a{w/2} 6 0 0 1 -{w} 0 Z"/><ellipse cx="{x+w/2}" cy="{y+6}" rx="{w/2}" ry="6"/>')
    DA=' stroke-dasharray="3 3"'; SM=' font-size="8.5" fill="#666"'
    E="".join(f'<path d="{d}"{DA if dash else ""}/>' for d,dash in edges)
    T="".join(f'<text x="{x}" y="{y}"{SM if small else ""}>{t}</text>' for x,y,t,small in texts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 360" width="480" height="360" font-family="{FONT_}">
  <defs>
    <filter id="{pfx}-pencil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter>
    <pattern id="{pfx}-shade" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><line x1="0" y1="0" x2="0" y2="5" stroke="#6b6b6b" stroke-width="0.7" stroke-opacity="0.8"/></pattern>
    <marker id="{pfx}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#3d3d3d" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker>
  </defs>
  <text x="16" y="30" font-weight="700" font-size="12" fill="#2a2a2a">{title} · 流程图</text>
  <g filter="url(#{pfx}-pencil)" stroke="#3d3d3d" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.4" stroke-opacity="0.92">
{chr(10).join(B)}
  </g>
  <g stroke="#3d3d3d" stroke-width="1.2" fill="none" marker-end="url(#{pfx}-arrow)" stroke-linecap="round">{E}</g>
  <g font-size="10.5" fill="#2a2a2a" text-anchor="middle">{T}</g>
  <text x="464" y="350" text-anchor="end" font-family="{HAND}" font-size="11" fill="#5a5a5a">{sig}</text>
</svg>
'''

def p0803_3():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False),("M30 250 Q10 250 10 150 Q10 130 28 130",True)]
    texts=[(85,73,"整点 / 呼唤 / 低电",False),(230,74,"房间图",False),(230,87,"反光标记 + 方位",True),(85,147,"摄像头找标记",False),(85,161,"IMU 推算航向",False),(230,149,"看到标记？",False),(230,162,"是 / 否",True),(390,147,"是 → 走向下一路点",False),(390,161,"通道口低头 · 坡道前倾",False),(85,247,"否 → 原地转一圈",False),(85,261,"3 次仍无 → 蹲下推送",False),(230,247,"到窝：对准线圈",False),(230,261,"开始充电",False),(390,247,"摔倒 → stand-up 策略",False),(390,261,"起身后重找标记",False),(240,331,"停在窝里 / 停在主人脚边",False),(305,146,"是",True),(216,200,"到达",True),(70,200,"否",True)]
    return flow("p0803-3","跨房间巡游与回窝",nodes,edges,texts,"0803-3",69)

def p0803_4():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False)]
    texts=[(85,73,"唤醒词（本地）",False),(230,74,"HA 实体",False),(230,87,"MCP 白名单",True),(85,147,"录音 → 大模型",False),(85,161,"静音拨杆先查",False),(230,149,"是问数据？",False),(230,162,"数据 / 待办 / 闲聊",True),(390,147,"MCP 读实体",False),(390,161,"雨水罐 / 温度 / 电量…",False),(85,247,"待办 → 写 todo",False),(85,261,"同步到 0801 清单",False),(230,247,"生成 ≤20 字回答",False),(230,261,"圆屏显示数字",False),(390,247,"3 秒无结果",False),(390,261,"“我去问问大屏”+推送",False),(240,331,"说出来 · 眼睛按好坏变色",False),(305,146,"是",True),(216,200,"闲聊",True),(70,200,"待办",True)]
    return flow("p0803-4","问答与全屋数据播报",nodes,edges,texts,"0803-4",71)

def poster(pfx, code, title, slogan, main, summary, feats, run, ref, seed):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 480" width="360" height="480" font-family="{FONT_}">
  <defs>
    <filter id="{pfx}-pencil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter>
    <pattern id="{pfx}-shade" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><line x1="0" y1="0" x2="0" y2="5" stroke="#6b6b6b" stroke-width="0.7" stroke-opacity="0.8"/></pattern>
  </defs>
  <g filter="url(#{pfx}-pencil)" stroke="#3d3d3d" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <rect x="14" y="14" width="332" height="452" rx="4" stroke-width="1.6"/><rect x="19" y="19" width="322" height="442" rx="3" stroke-width="0.7"/>
    <path d="M30 44 H330" stroke-width="0.8"/>
{main}
    <circle cx="48" cy="332" r="7" stroke-width="1.2"/><path d="M45 332 l2 2 l4 -5" stroke-width="1.2"/>
    <circle cx="48" cy="362" r="7" stroke-width="1.2"/><path d="M45 362 l2 2 l4 -5" stroke-width="1.2"/>
    <circle cx="48" cy="392" r="7" stroke-width="1.2"/><path d="M45 392 l2 2 l4 -5" stroke-width="1.2"/>
    <path d="M30 420 H330" stroke-width="0.8"/>
  </g>
  <text x="30" y="38" font-size="9" fill="#666" letter-spacing="2">SURVIVEOS · LOGIC PRODUCT</text>
  <text x="330" y="38" font-size="9" fill="#666" text-anchor="end">{code}</text>
  <text x="180" y="72" text-anchor="middle" font-family="'Noto Serif SC','Songti SC',serif" font-weight="900" font-size="22" fill="#2a2a2a">{title}</text>
  <text x="180" y="90" text-anchor="middle" font-family="{HAND}" font-size="13" fill="#b5372b">{slogan}</text>
  <text x="180" y="300" text-anchor="middle" font-size="9.5" fill="#666">{summary}</text>
  <g font-size="11" fill="#2a2a2a"><text x="64" y="336">{feats[0]}</text><text x="64" y="366">{feats[1]}</text><text x="64" y="396">{feats[2]}</text></g>
  <text x="30" y="440" font-size="9" fill="#666">{run}</text>
  <text x="30" y="454" font-size="9" fill="#666">参考实现：{ref}</text>
  <g transform="rotate(-8 296 108)"><rect x="266" y="98" width="60" height="20" rx="3" fill="none" stroke="#b5372b" stroke-width="1.4"/><text x="296" y="112" text-anchor="middle" font-size="9.5" fill="#b5372b" font-weight="700" letter-spacing="1">设想·逻辑</text></g>
</svg>
'''

def p0803_3p():
    pfx="p0803-3p"
    main = ("\n".join([
        # 三个小房间格 + 虚线路径 + 鸭子 + 窝
        '<path d="M40 200 h70 v50 h-70 Z M150 180 h70 v70 h-70 Z M260 200 h60 v50 h-60 Z" stroke-width="1.3"/>',
        '<path d="M110 240 h40 M220 240 h40" stroke-width="1"/>',
        '<path d="M75 236 Q130 210 185 230 T290 236" stroke-width="1" stroke-dasharray="3 3"/>',
        '<circle cx="75" cy="236" r="3" stroke-width="1"/><circle cx="185" cy="230" r="3" stroke-width="1"/><circle cx="290" cy="236" r="3" stroke-width="1"/>',
        duck(185, 248, 0.55, 1.2),
        '<path d="M60 250 a10 5 0 0 1 20 0 Z M300 250 a10 5 0 0 1 20 0 Z" stroke-width="1"/>',
        '<path d="M40 120 h60 v40 h-60 Z M48 130 l8 -6 l10 8 M80 128 a4 4 0 1 0 0.1 0 M60 150 h20" stroke-width="1"/>',  # 房间图
        '<path d="M100 140 Q140 150 180 200" stroke-width="0.8" stroke-dasharray="3 3"/>',
        '<path d="M250 120 h60 v40 h-60 Z M256 150 l12 -20 l8 12 l10 -16 l14 24" stroke-width="1"/>',  # 电量/坡道
        '<path d="M240 150 Q220 180 200 200" stroke-width="0.8" stroke-dasharray="3 3"/>',
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>']))
    return poster(pfx,"0803 · L3","巡游回窝器","一张手绘房间图，三个房间自己走",main,"触发 → 找反光标记 → 走向下一路点 → 电量低回最近的窝",
                  ["路点就是充电窝、通道口、坡道顶的反光标记","通道口低头慢走，坡道前倾，摔了自己起身","连找 3 次没找到就蹲下，推送手机"],
                  "跑在：鸭身 RK3566 robotd · 数据出口：HA 位置实体（在哪个房间）","pollen-robotics/microduck",73)

def p0803_4p():
    pfx="p0803-4p"
    main = ("\n".join([
        duck(90, 250, 0.9, 1.4),
        '<path d="M120 150 q0 -12 12 -12 h80 q12 0 12 12 v30 q0 12 -12 12 h-60 l-14 10 v-10 h-6 q-12 0 -12 -12 Z" stroke-width="1.3"/>',
        '<path d="M136 160 h60 M136 172 h40" stroke-width="0.7"/>',
        '<path d="M250 130 h60 v50 h-60 Z M256 140 h48 M256 150 h48 M256 160 h30" stroke-width="1.1"/>',  # HA 实体表
        '<path d="M224 162 H248" stroke-width="1" stroke-dasharray="3 3"/><path d="M244 158 l4 4 l-4 4" stroke-width="1"/>',
        '<circle cx="106" cy="228" r="6" stroke-width="1"/><path d="M103 228 l2 2 l4 -4" stroke-width="0.8"/>',
        '<path d="M160 230 l40 -10 M160 236 l40 10" stroke-width="0.6" stroke-dasharray="2 2"/>',
        '<path d="M210 210 h30 v30 h-30 Z M214 218 l6 -4 l5 5 l7 -8 l8 8" stroke-width="1"/>',  # 圆屏数据
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>']))
    return poster(pfx,"0803 · L4","会说话的仪表盘","问它一句，它去大屏那边查了用嘴说",main,"唤醒词 → 大模型 → MCP 读 HA 实体 → ≤20 字回答 + 圆屏数字",
                  ["只认一个人的声音，物理静音拨杆一拨就聋","随口一句“记得买螺丝”写进 0801 待办","3 秒没结果就说“我去问问大屏”并推送手机"],
                  "跑在：ESP32-S3 xiaozhi + HA MCP Server · 数据出口：HA todo 实体","78/xiaozhi-esp32",75)

if __name__=="__main__":
    open("illos/area-08.svg","w",encoding="utf-8").write(area08())
    open("illos/0803.svg","w",encoding="utf-8").write(m0803())
    open("parts/0803-1.svg","w",encoding="utf-8").write(p0803_1())
    open("parts/0803-2.svg","w",encoding="utf-8").write(p0803_2())
    open("parts/0803-3.svg","w",encoding="utf-8").write(p0803_3())
    open("parts/0803-4.svg","w",encoding="utf-8").write(p0803_4())
    open("parts/0803-3-poster.svg","w",encoding="utf-8").write(p0803_3p())
    open("parts/0803-4-poster.svg","w",encoding="utf-8").write(p0803_4p())
    print("ok")
