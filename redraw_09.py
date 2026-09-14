from sk import *
from redraw_08 import SH, along, finish, flow, poster
FONT_ = FONT

# ---------------- illos ----------------
def m0307():
    pfx="m0307"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 阁楼坡顶（右侧向下）+ 地面
    B.append('<path d="M14 246 H386" stroke-width="1.6"/><path d="M386 246 L200 40 L120 40" stroke-width="1.5"/>')
    for i in range(1,13): B.append(f'<path d="M{386-i*15} {246-i*16.5} l-7 0" stroke-width="0.5"/>')
    B.append('<path d="M262 246 V110" stroke-width="0.5" stroke-dasharray="4 3"/>')  # 2060 线
    # 机架：底座 4040 框 + 两立柱 + 横梁（正视，龙门）
    B.append('<path d="M60 246 v-12 h150 v12 M60 234 v-6 h150 v6" stroke-width="1.6"/><path d="M62 236 h146 v8 h-146 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M72 228 V120 h8 V228 M190 228 V120 h8 V228 M72 120 H198 M72 128 H198" stroke-width="1.5"/><path d="M74 130 h122 v-8" stroke-width="0.5"/>')
    B.append('<path d="M60 228 h150" stroke-width="1"/>')  # 台面
    # 型材槽线
    for x in (75,193): B.append(f'<path d="M{x} 132 V226" stroke-width="0.4"/>')
    # 主轴滑块 + Z 轴 + 主轴
    B.append('<path d="M118 112 h30 v24 h-30 Z M126 136 v22 h14 v-22 M129 158 v12 h8 v-12 M133 170 v10" stroke-width="1.2"/><path d="M120 114 h26 v20 h-26 Z" fill="' + HL + '" stroke="none"/>')
    # A/C 分度头 + 工件（翻转 45°）
    B.append('<path d="M112 228 v-10 h28 v10 M116 218 v-8 h20 v8" stroke-width="1.2"/><circle cx="126" cy="204" r="8" stroke-width="1.2"/><path d="M126 204 l-14 -14 M126 204 l14 -14" stroke-width="0.6" stroke-dasharray="2 2"/>')
    B.append('<path d="M118 196 l8 -12 l12 8 l-8 12 Z" stroke-width="1.1"/><path d="M120 195 l6 -9 l9 6 l-6 9 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M104 200 a10 10 0 0 1 4 -14 M104 200 l-3 -4 M104 200 l4 -2" stroke-width="0.8"/>')  # 转向箭头
    # 防护罩（阳光板）轮廓
    B.append('<path d="M48 234 V104 H222 V234" stroke-width="0.9" stroke-dasharray="5 3"/><path d="M50 106 h170 v126 h-170 Z" fill="' + HL + '" stroke="none" fill-opacity="0.35"/>')
    # 排屑管：从主轴罩顶部沿坡顶向右下
    B.append('<path d="M150 108 h20 q10 0 14 8 L296 230 M150 104 h20 q12 0 17 8 L300 226" stroke-width="1"/><path d="M296 230 l10 2 l-4 6" stroke-width="0.8"/>')
    for i in range(6): B.append(f'<path d="M{190+i*16} {124+i*17.5} l-3 3" stroke-width="0.5"/>')
    # 下层型材柜：VFD + 电源
    B.append('<path d="M84 246 v-14 h50 v14 M90 238 h10 M104 238 h6 M116 236 a2 2 0 1 0 0.1 0" stroke-width="0.9"/>')
    # 0301 工具台（左侧小）
    B.append('<path d="M14 246 v-30 h36 v30 M18 220 h28" stroke-width="1"/>')
    # 人（站着看，2060 内）
    B.append(figure(244, 246, 1.0))
    B.append('<path d="M238 216 l-8 -6" stroke-width="0.9"/>')
    # 天窗
    B.append('<path d="M330 184 l-26 -28 l14 -6 l24 26 Z" stroke-width="1"/><path d="M328 182 l-22 -24 M318 170 l14 -6" stroke-width="0.5"/>')
    body="\n".join(B)
    labels="\n".join([label(135,96,"铝型材龙门 · 3+2 五轴",8.5,"middle"), label(126,258,"A/C 分度头",7,"middle"),
                      label(262,104,"2060",7,"middle"), label(300,120,"排屑管 → 0404 集尘",7,"middle"),
                      label(32,258,"0301",7,"middle"), label(346,196,"天窗",7,"middle"),
                      label(200,282,"0307：阁楼核心区里一台会翻面的桌面五轴，木屑顺坡顶出去",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0307", seed=81).replace("</svg>", labels+"\n</svg>")

def m0804():
    pfx="m0804"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 储藏室一角：左侧隔墙（背面），型材机架四层
    B.append('<path d="M14 250 H386" stroke-width="1.6"/><path d="M60 250 V40" stroke-width="1.4"/>')
    for y in range(52,250,12): B.append(f'<path d="M62 {y} h-46" stroke-width="0.35"/>')
    # 机架 2020：两立柱 + 四层
    B.append('<path d="M110 250 V62 M240 250 V62 M110 62 H240" stroke-width="1.6"/><path d="M114 250 V62 M236 250 V62" stroke-width="0.5"/>')
    for y in (232,190,148,106): B.append(f'<path d="M110 {y} H240 M110 {y+4} H240" stroke-width="1.1"/><path d="M112 {y+1} h126 v2 h-126 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M110 250 v-10 M240 250 v-10 M100 250 h20 M230 250 h20" stroke-width="1"/>')  # 脚
    # 层 1 NAS
    B.append('<path d="M122 230 v-30 h78 v30 Z" stroke-width="1.2"/>')
    for i in range(4): B.append(f'<path d="M{126+i*19} 204 v22 h15 v-22 Z" stroke-width="0.7"/><circle cx="{133+i*19}" cy="222" r="1.2" stroke-width="0.6"/>')
    # 层 2 合盖笔记本
    B.append('<path d="M120 188 v-8 h100 v8 Z" stroke-width="1.2"/><path d="M122 182 h96" stroke-width="0.5"/><circle cx="214" cy="184" r="1.2" stroke-width="0.6"/>')
    # 层 3 Mac mini + 交换机
    B.append('<rect x="122" y="126" width="40" height="18" rx="4" stroke-width="1.2"/><path d="M128 131 h6" stroke-width="0.5"/><path d="M174 146 v-12 h56 v12 Z" stroke-width="1.1"/>')
    for i in range(6): B.append(f'<path d="M{178+i*9} 137 v5 h6 v-5 Z" stroke-width="0.5"/>')
    # 层 4 光猫 + 理线
    B.append('<path d="M122 104 v-16 h46 v16 Z M126 92 h6 M136 92 h6 M146 92 h6" stroke-width="1"/><path d="M182 88 v16 M190 88 v16 M198 88 v16 M206 88 v16 M214 88 v16" stroke-width="0.6"/>')
    # 网线束：沿右立柱下到底、一根穿隔墙
    B.append('<path d="M232 96 q6 0 6 6 V236 M234 100 q4 0 4 4 V236" stroke-width="0.6"/><path d="M110 140 H60 M110 144 H60" stroke-width="0.8"/><path d="M52 142 l-8 0 l3 -3 M44 142 l3 3" stroke-width="0.7"/>')
    # PDU/UPS 在地上
    B.append('<path d="M258 250 v-16 h36 v16 M262 240 h4 M270 240 h4 M278 240 h4 M286 240 h4" stroke-width="1"/>')
    # 墙上小屏：三条状态线
    B.append('<rect x="300" y="90" width="66" height="44" rx="2" stroke-width="1.2"/><path d="M306 100 h54 M306 112 h40 M306 124 h48" stroke-width="1"/><circle cx="306" cy="100" r="1.5" stroke-width="0.6"/><circle cx="306" cy="112" r="1.5" stroke-width="0.6"/><circle cx="306" cy="124" r="1.5" stroke-width="0.6"/>')
    B.append('<path d="M340 112 l6 -3 l4 3 l3 -6 l5 3" stroke-width="0.6"/>')
    # 指示灯光晕
    B.append('<path d="M204 222 l6 0 M204 226 l4 0" stroke-width="0.5" stroke-dasharray="1 2"/>')
    # 人（手机推送）
    B.append(figure(330, 250, 0.95)); B.append('<path d="M322 222 l-4 -6 h8 l-3 6" stroke-width="0.8"/>')
    body="\n".join(B)
    labels="\n".join([label(175,56,"2020 型材机架 · 60×40×120",8,"middle"), label(161,236,"NAS 4 盘",7,"middle"), label(170,178,"Windows 笔记本",7,"middle"),
                      label(142,122,"M1 Mac mini",7,"middle"), label(202,130,"2.5GbE",6.5,"middle"), label(145,84,"光猫",6.5,"middle"),
                      label(84,136,"→ 0802 屏墙",6.5,"middle"), label(276,262,"PDU + UPS",7,"middle"), label(333,84,"三条心跳",7,"middle"),
                      label(200,282,"0804：储藏室隔墙背后的“地下机房”，三台机器替掉全屋树莓派",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0804", seed=83).replace("</svg>", labels+"\n</svg>")

def m0805():
    pfx="m0805"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 吧台台面（透视板）+ 三块样板
    B.append('<path d="M20 232 L380 232 L340 150 L60 150 Z" stroke-width="1.6"/><path d="M20 232 v10 h360 v-10" stroke-width="1"/><path d="M22 234 h356 v6 h-356 Z" fill="' + H + '" stroke="none"/>')
    for i in range(1,6): B.append(f'<path d="M{60+i*46} 150 L{20+i*60} 232" stroke-width="0.35"/>')
    # 样板 1：型材段（左，斜放，端面可见十字槽）
    B.append('<path d="M70 210 l60 -30 v-22 l-60 30 Z M70 210 l-16 -8 v-22 l16 8 M54 180 l60 -30 l16 8" stroke-width="1.4"/>')
    B.append('<path d="M72 208 l56 -28 v-18 l-56 28 Z" fill="' + H + '" stroke="none"/>')
    B.append('<path d="M56 182 l14 7 v20 M62 176 v14 M56 190 h8 M62 184 l6 3 M58 178 l4 -2" stroke-width="0.9"/>')  # 端面槽示意
    B.append('<path d="M60 196 h8 v6 h-8 Z M64 190 v-4" stroke-width="0.7"/>')
    # 样板 2：木板（中）
    B.append('<path d="M150 214 l70 -34 l30 12 l-70 34 Z M150 214 v6 l30 12 v-6 M180 226 l70 -34 v6 l-70 34" stroke-width="1.4"/>')
    B.append('<path d="M158 208 q30 -12 60 -28 M164 214 q30 -12 60 -28 M172 220 q30 -12 56 -26 M156 200 q20 -8 40 -18" stroke-width="0.5"/>')
    # 样板 3：皮块（右，软，边角翻起）
    B.append('<path d="M270 216 q30 -20 60 -30 q16 4 30 12 q-30 14 -62 30 q-14 -6 -28 -12 Z" stroke-width="1.4"/><path d="M328 190 q6 -8 14 -4 q-4 8 -10 8" stroke-width="0.9"/>')
    B.append('<path d="M274 214 q28 -18 56 -28 q14 4 26 10 q-28 14 -58 28 q-12 -5 -24 -10 Z" fill="' + HL + '" stroke="none"/>')
    B.append('<path d="M280 208 q4 2 8 0 M300 200 q4 2 8 0 M320 194 q4 2 8 0" stroke-width="0.5"/>')  # 皮纹
    # 规格卡（立在后面）
    B.append('<path d="M228 150 v-56 h96 v56" stroke-width="1.1"/><path d="M236 104 h60 M236 114 h80 M236 124 h50 M236 134 h70 M236 144 h40" stroke-width="0.6"/><path d="M230 96 h92 v10 h-92 Z" fill="' + H + '" stroke="none"/>')
    # 人（伸手摸型材）
    B.append('<circle cx="120" cy="92" r="7" stroke-width="1.2"/><path d="M120 99 V136 M120 108 l-22 22 l-14 12 M120 108 l16 14 M120 136 l-10 20 M120 136 l10 20" stroke-width="1.2"/>')
    body="\n".join(B)
    labels="\n".join([label(92,254,"欧标 2020 · 喷砂黑",7.5,"middle"), label(200,254,"白蜡木 · 油蜡",7.5,"middle"), label(316,254,"植鞣皮",7.5,"middle"),
                      label(276,88,"D3 · 欧标 · 2020 · 槽 6 · 黑 · 壁厚 1.8",7,"middle"), label(300,160,"木料 / 皮草：待定标",7,"middle"),
                      label(200,278,"0805：三块样板就是全屋手工件的语法——铝做骨、木做面、皮做触感",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0805", seed=85).replace("</svg>", labels+"\n</svg>")

# ---------------- parts ----------------
def ex(pfx, title, sig, seed, legend, note, items, leaders):
    """items: list of svg fragments per part (放在 along(i,n) 位置)；leaders: list of (dx,dy)"""
    n=len(items); B=[]; L=[]; C=[]
    for i,frag in enumerate(items):
        x,y=along(i,n); B.append(frag(x,y))
    for i,(dx,dy) in enumerate(leaders):
        x,y=along(i,n); l,c=leader(x+dx,y+dy,x+dx-32,y+dy-6,i+1); L.append(l); C.append(c)
    svg=exploded(pfx,title,"",("\n".join(B)),sig,axis="M100 318 L392 40",seed=seed,leaders="\n".join(L))
    return finish(svg, legend, C, note)

def profile(x,y,w,h,d,pfx,sw=1.3):
    """一段型材（斜投影），端面画十字槽"""
    s=f'<path d="M{x} {y} h{w} v{h} h{-w} Z M{x} {y} l{d} {-d*0.6} h{w} l{-d} {d*0.6} M{x+w} {y} l{d} {-d*0.6} v{h} l{-d} {d*0.6}" stroke-width="{sw}"/>'
    s+=f'<path d="M{x+w+1} {y+1} l{d-2} {-d*0.6+1} v{h-2} l{-d+2} {d*0.6-1} Z" fill="{SH(pfx)}" stroke="none"/>'
    s+=f'<path d="M{x+w/2-2} {y+2} v{h-4} M{x+2} {y+h/2} h{w-4} M{x+w/2-4} {y+2} h4 M{x+w/2-4} {y+h-2} h4" stroke-width="0.6"/>'
    return s

def p0307_1():
    pfx="p0307-1"
    items=[lambda x,y: profile(x-60,y-10,120,16,14,pfx)+profile(x-60,y-40,16,30,14,pfx)+profile(x+44,y-40,16,30,14,pfx),  # 1 底座框
           lambda x,y: profile(x-40,y-30,10,60,10,pfx)+profile(x+30,y-30,10,60,10,pfx)+profile(x-40,y-40,80,10,10,pfx),  # 2 立柱+横梁 3030
           lambda x,y: f'<path d="M{x-46} {y} h92 v6 h-92 Z M{x-46} {y-24} h92 v6 h-92 Z" stroke-width="1.2"/><path d="M{x-30} {y-18} h20 v18 h-20 Z M{x+10} {y-18} h20 v18 h-20 Z" stroke-width="1"/><path d="M{x-44} {y+2} h88 v2 h-88 Z" fill="{SH(pfx)}" stroke="none"/>',  # 3 导轨+滑块
           lambda x,y: f'<circle cx="{x-30}" cy="{y}" r="8" stroke-width="1.2"/><path d="M{x-22} {y} h50 M{x-22} {y-2} h50 M{x-22} {y+2} h50" stroke-width="0.8"/><path d="M{x-10} {y-8} h14 v16 h-14 Z" stroke-width="1"/><path d="M{x+30} {y-10} h16 v20 h-16 Z M{x+38} {y-10} v-6 M{x+34} {y-16} h8" stroke-width="1.1"/>',  # 4 丝杠+闭环步进
           lambda x,y: f'<path d="M{x-40} {y-6} h80 v12 h-80 Z" stroke-width="1.3"/><path d="M{x-36} {y-2} h72 M{x-36} {y+2} h72" stroke-width="0.5"/><path d="M{x-30} {y-6} v12 M{x-10} {y-6} v12 M{x+10} {y-6} v12 M{x+30} {y-6} v12" stroke-width="0.5"/><path d="M{x-40} {y-6} l10 -8 h80 l-10 8" stroke-width="1"/>']  # 5 T 槽板
    legend=[(1,"底座框 4040 喷砂黑欧标（0805 规格）"),(2,"立柱 + 横梁 3030，内置角槽件 + 角码双锁"),(3,"HGR15 直线导轨 ×2 + 滑块，压在型材面上"),(4,"1605 滚珠丝杠 + 42 闭环步进（丢步报警）"),(5,"300×300 铝 T 槽板台面")]
    return ex(pfx,"铝型材龙门机架","0307-1",87,legend,"行程 300×300×120 · 整机 ≤60kg（阁楼承重待核）",items,[(-64,-16),(-44,-34),(-50,-8),(-42,-10),(-44,-14)])

def p0307_2():
    pfx="p0307-2"
    items=[lambda x,y: f'<path d="M{x-40} {y} h80 v12 h-80 Z M{x-40} {y} l10 -8 h80 l-10 8" stroke-width="1.3"/><path d="M{x-36} {y+3} h72 v6 h-72 Z" fill="{SH(pfx)}" stroke="none"/><circle cx="{x-30}" cy="{y-4}" r="2" stroke-width="0.6"/><circle cx="{x+30}" cy="{y-4}" r="2" stroke-width="0.6"/>',  # 1 底板
           lambda x,y: f'<path d="M{x-30} {y-10} h24 v22 h-24 Z" stroke-width="1.2"/><circle cx="{x-18}" cy="{y+1}" r="6" stroke-width="0.8"/><path d="M{x-6} {y+1} h20 M{x+14} {y-6} h14 v14 h-14 Z" stroke-width="1"/><path d="M{x+16} {y-4} h10 v10 h-10 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+21} {y-6} v-6 M{x+18} {y-12} h6" stroke-width="0.8"/>',  # 2 A 轴蜗轮箱+步进
           lambda x,y: f'<path d="M{x-24} {y-8} a24 8 0 1 0 48 0 a24 8 0 1 0 -48 0" stroke-width="1.3"/><path d="M{x-24} {y-8} v14 a24 8 0 0 0 48 0 v-14" stroke-width="1"/><path d="M{x-22} {y+6} a22 7 0 0 0 44 0 v-3 a22 7 0 0 1 -44 0 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+26} {y-2} h12 v10 h-12 Z M{x+32} {y-2} v-6" stroke-width="0.9"/><path d="M{x-30} {y-14} a30 12 0 0 1 12 -10 l-3 -3 M{x-18} {y-24} l-4 2" stroke-width="0.7"/>',  # 3 C 轴转台
           lambda x,y: f'<path d="M{x-20} {y-6} h40 v12 h-40 Z M{x-20} {y-6} l6 -6 h40 l-6 6 M{x+20} {y-6} l6 -6 v12 l-6 6" stroke-width="1.2"/><path d="M{x-14} {y-2} v4 M{x-4} {y-2} v4 M{x+6} {y-2} v4 M{x+16} {y-2} v4" stroke-width="0.5"/><path d="M{x+30} {y-8} a8 8 0 1 0 0.1 0" stroke-width="1"/><path d="M{x+30} {y-14} v-3 M{x+35} {y-5} l3 2 M{x+25} {y-5} l-3 2" stroke-width="0.9"/>',  # 4 小 T 槽板 / 三爪卡盘
           lambda x,y: f'<path d="M{x-16} {y-4} h10 v8 h-10 Z M{x-6} {y} h8 M{x+2} {y-6} h6 v12 h-6 Z" stroke-width="1"/><path d="M{x+14} {y-10} h20 v20 h-20 Z" stroke-width="1"/><path d="M{x+18} {y-4} h12 M{x+18} {y} h12 M{x+18} {y+4} h8" stroke-width="0.5"/><path d="M{x+34} {y-2} h10 M{x+34} {y+2} h10" stroke-width="0.6"/>']  # 5 光电回零 + 编码器
    legend=[(1,"分度头底板（T 槽压板固定在台面）"),(2,"A 轴蜗轮蜗杆箱 1:50 + 42 步进（±110°）"),(3,"C 轴转台 360° 蜗轮自锁 + 步进"),(4,"顶部 100mm 小 T 槽板 / 三爪卡盘可换"),(5,"光电回零开关 ×2 + 编码器接 grblHAL A/C 口")]
    return ex(pfx,"A/C 双旋转分度头","0307-2",89,legend,"只定位不联动：回得准比转得快重要",items,[(-44,-6),(-34,-14),(-30,-16),(-24,-12),(-20,-12)])

def p0307_3():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False),("M30 250 Q10 250 10 150 Q10 130 28 130",True)]
    texts=[(85,73,"CAM 导出带姿态段程序",False),(230,74,"姿态表",False),(230,87,"每面 A / C 角度",True),(85,147,"主轴抬安全高",False),(85,161,"A/C 转到该面角度",False),(230,149,"已锁定？",False),(230,162,"蜗轮自锁 + 编码器",True),(390,147,"是 → 探针重测 Z 零",False),(390,161,"误差 >0.05 报警",False),(85,247,"否 → 重试回零",False),(85,261,"3 次失败停机",False),(230,247,"跑本面三轴刀路",False),(230,261,"grblHAL 执行",False),(390,247,"门开 / 丢步 / 过流",False),(390,261,"→ 进给暂停",False),(240,331,"下一面 · 直到全部姿态完成",False),(305,146,"是",True),(216,200,"完成",True),(70,200,"否",True)]
    return flow("p0307-3","3+2 定位加工流",nodes,edges,texts,"0307-3",91)

def p0307_4():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False)]
    texts=[(85,73,"主轴请求启动",False),(230,74,"0304 储能",False),(230,87,"SOC / 当前负载",True),(85,147,"读 SOC 与负载",False),(85,161,"电摩在充电？",False),(230,149,"能给 2kW？",False),(230,162,"允许 / 限功率 / 拒绝",True),(390,147,"是 → 开 0404 集尘",False),(390,161,"开阁楼分路阀",False),(85,247,"否 → 限功率模式",False),(85,261,"或推送“等光伏”",False),(230,247,"3 秒后通主轴",False),(230,261,"记 cnc_runtime",False),(390,247,"主轴停 → 延时 30s",False),(390,261,"关阀关集尘",False),(240,331,"粉尘 / VOC 超标 → 推送",False),(305,146,"是",True),(216,200,"运行中",True),(70,200,"否",True)]
    return flow("p0307-4","功率与除尘联动",nodes,edges,texts,"0307-4",93)

def p0307_3p():
    pfx="p0307-3p"
    main="\n".join(['<path d="M60 150 h60 v40 h-60 Z M66 158 h48 M66 168 h48 M66 178 h30" stroke-width="1.2"/>',  # 程序
        '<path d="M130 170 H160" stroke-width="1" stroke-dasharray="3 3"/><path d="M156 166 l4 4 l-4 4" stroke-width="1"/>',
        '<circle cx="200" cy="170" r="26" stroke-width="1.4"/><path d="M200 144 v52 M174 170 h52" stroke-width="0.6"/><path d="M186 160 l14 -8 l14 8 l-14 8 Z" stroke-width="1.1"/><path d="M226 150 a30 30 0 0 1 4 26 l-4 -4 M230 176 l4 -2" stroke-width="0.8"/>',  # 分度头翻面
        '<path d="M236 170 H266" stroke-width="1" stroke-dasharray="3 3"/><path d="M262 166 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M276 146 h40 v50 h-40 Z M290 146 v-14 h12 v14 M296 132 v-8" stroke-width="1.2"/><path d="M280 190 h32 M284 184 h24" stroke-width="0.6"/>',  # 主轴切
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>'])
    return poster(pfx,"0307 · L3","翻面加工器","不追真五轴：转一下，再当三轴切",main,"CAM 姿态段 → A/C 转位锁定 → 探针重测 → 三轴刀路",
        ["每一段都是能单独看懂的三轴程序","换面后探针重测 Z，误差 >0.05mm 就停","门开 / 丢步 / 过流任一触发即暂停"],
        "跑在：grblHAL（Teensy 4.1）· 数据出口：HA cnc_runtime 实体","grblHAL/core · LinuxCNC/linuxcnc",95)

def p0307_4p():
    pfx="p0307-4p"
    main="\n".join(['<path d="M50 140 h50 v40 h-50 Z M58 150 h34 M58 160 h34 M58 170 h20" stroke-width="1.2"/><path d="M62 132 h26 v8 h-26 Z" stroke-width="0.9"/>',  # 储能电池
        '<path d="M110 160 H150" stroke-width="1" stroke-dasharray="3 3"/><path d="M146 156 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M156 130 l24 -14 l24 14 l-24 14 Z M156 130 v34 l24 14 v-34 M204 130 v34 l-24 14" stroke-width="1.3"/><path d="M170 150 l8 -14 l6 4 l-8 14 Z" fill="url(#p0307-4p-shade)" stroke="none"/>',  # CNC 方块
        '<path d="M214 150 H250" stroke-width="1" stroke-dasharray="3 3"/><path d="M246 146 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M262 132 h44 v44 h-44 Z" stroke-width="1.2"/><circle cx="284" cy="154" r="12" stroke-width="1"/><path d="M284 142 v24 M272 154 h24" stroke-width="0.7"/><path d="M306 150 h20 l-4 -4 M326 150 l-4 4" stroke-width="0.9"/>',  # 集尘机
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>'])
    return poster(pfx,"0307 · L4","开机前先问电","电够不够、灰往哪去，机器自己不管",main,"主轴请求 → 查 0304 SOC → 先开 0404 集尘 → 3 秒后通主轴",
        ["电池低或电摩在充电就只给低功率模式","集尘和阁楼分路阀先开，主轴停后延时 30 秒","粉尘 / VOC 超标推手机"],
        "跑在：ESPHome + HomeAssistant · 数据出口：cnc_power_mode 实体","home-assistant/core",97)

def p0804_1():
    pfx="p0804-1"
    items=[lambda x,y: profile(x-30,y-40,8,60,8,pfx)+profile(x+22,y-40,8,60,8,pfx)+profile(x-30,y-46,60,6,8,pfx)+profile(x-30,y+14,60,6,8,pfx),  # 1 机架
           lambda x,y: f'<path d="M{x-40} {y-8} h80 v18 h-80 Z" stroke-width="1.3"/>'+"".join(f'<path d="M{x-36+i*19} {y-5} h15 v12 h-15 Z" stroke-width="0.7"/>' for i in range(4))+f'<path d="M{x-40} {y-8} l8 -6 h80 l-8 6" stroke-width="1"/>',  # 2 NAS
           lambda x,y: f'<path d="M{x-44} {y} h88 v6 h-88 Z M{x-44} {y} l10 -8 h88 l-10 8" stroke-width="1.2"/><path d="M{x-42} {y+1} h84 v4 h-84 Z" fill="{SH(pfx)}" stroke="none"/><circle cx="{x+40}" cy="{y+3}" r="1.2" stroke-width="0.6"/>',  # 3 笔记本
           lambda x,y: f'<rect x="{x-46}" y="{y-8}" width="34" height="14" rx="4" stroke-width="1.2"/><path d="M{x-40} {y-4} h6" stroke-width="0.5"/><path d="M{x-4} {y-6} h50 v10 h-50 Z" stroke-width="1.1"/>'+"".join(f'<path d="M{x+i*8} {y-3} v4 h5 v-4 Z" stroke-width="0.5"/>' for i in range(6)),  # 4 Mac mini + 交换机
           lambda x,y: f'<path d="M{x-40} {y-4} h40 v10 h-40 Z M{x-36} {y} h4 M{x-30} {y} h4 M{x-24} {y} h4" stroke-width="1"/><path d="M{x+8} {y-10} h32 v18 h-32 Z M{x+12} {y-2} h6 M{x+20} {y-2} h6 M{x+28} {y-2} h6" stroke-width="1"/><path d="M{x+12} {y+4} h24" stroke-width="0.5"/>']  # 5 光猫+PDU/UPS
    legend=[(1,"2020 喷砂黑型材机架 60×40×120，离地 10cm"),(2,"四盘位 NAS：2×8TB 镜像 + 2×4TB"),(3,"Windows 笔记本（合盖常年在线，自带电池）"),(4,"M1 Mac mini（无头）+ 2.5GbE 交换机"),(5,"光猫 + 浪涌 PDU + 小 UPS")]
    return ex(pfx,"三机型材机架","0804-1",99,legend,"储藏室隔墙背后 · 三面打孔铝板围 · 正面风道",items,[(-36,-48),(-44,-12),(-48,-10),(-50,-12),(-44,-8)])

def p0804_2():
    pfx="p0804-2"
    disk=lambda x,y,w: f'<path d="M{x} {y} h{w} v10 h{-w} Z M{x} {y} l6 -5 h{w} l-6 5 M{x+w} {y} l6 -5 v10 l-6 5" stroke-width="1.1"/><circle cx="{x+w-6}" cy="{y+5}" r="1.5" stroke-width="0.5"/>'
    items=[lambda x,y: disk(x-40,y-4,30)+disk(x-2,y-4,30)+f'<path d="M{x-25} {y-10} q20 -14 44 0" stroke-width="0.6" stroke-dasharray="2 2"/><path d="M{x-14} {y-16} l4 -2 l-1 4" stroke-width="0.6"/>',  # 1 镜像池
           lambda x,y: disk(x-40,y-4,30)+disk(x-2,y-4,30)+f'<path d="M{x-30} {y+14} h10 M{x-25} {y+10} v8" stroke-width="0.6"/>',  # 2 单盘池
           lambda x,y: f'<path d="M{x-24} {y-8} h40 v16 h-40 Z M{x+16} {y-8} l6 -4 v16 l-6 4" stroke-width="1.2"/><path d="M{x-20} {y} h30" stroke-width="0.5"/><path d="M{x+30} {y} h14 M{x+40} {y-4} h6 v8 h-6 Z" stroke-width="0.9"/><path d="M{x-40} {y+14} l-8 -12 h96 l-8 12 Z" stroke-width="0.9" stroke-dasharray="3 2"/>',  # 3 冷备盘 + 保险箱
           lambda x,y: f'<path d="M{x-30} {y-14} h60 v28 h-60 Z" stroke-width="1.1"/>'+"".join(f'<path d="M{x-26+i*8} {y+10} v-{6+(i*5)%16}" stroke-width="0.8"/>' for i in range(7))+f'<path d="M{x-26} {y+10} h52" stroke-width="0.6"/>',  # 4 快照日历
           lambda x,y: f'<path d="M{x-30} {y-6} h24 v12 h-24 Z M{x-6} {y} h16 M{x+10} {y-8} h24 v16 h-24 Z" stroke-width="1"/><path d="M{x+14} {y-2} h16 M{x+14} {y+2} h10" stroke-width="0.5"/><path d="M{x-2} {y-14} l6 6 l6 -6" stroke-width="0.7"/>']  # 5 2.5GbE
    legend=[(1,"镜像池 2×8TB：照片 / 数据库快照 / 文档"),(2,"单盘池 2×4TB：影音库（可再生）"),(3,"USB 冷备 4TB，每周一次 → 阁楼保险箱"),(4,"快照策略：日保留 30、月保留 12"),(5,"2.5GbE 直连 0802 小主机与 Mac mini")]
    return ex(pfx,"存储与冷备盘组","0804-2",101,legend,"镜像防坏盘 · 快照防误删 · 冷盘防火水",items,[(-44,-10),(-44,-10),(-36,-14),(-34,-18),(-34,-10)])

def p0804_3():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False),("M30 250 Q10 250 10 150 Q10 130 28 130",True)]
    texts=[(85,73,"每 60 秒扫一遍",False),(230,74,"实体表",False),(230,87,"各自上报周期",True),(85,147,"设备层：last_seen",False),(85,161,"> 3× 周期 → 黄",False),(230,149,"服务层也失联？",False),(230,162,"Uptime Kuma 探端口",True),(390,147,"是 → 红 + 推手机",False),(390,161,"写失联记录",False),(85,247,"否 → 只在大屏亮黄",False),(85,261,"不吵人",True),(230,247,"恢复 → 自动清除",False),(230,261,"记恢复时长",False),(390,247,"每周汇总",False),(390,261,"失联最多的 5 个",False),(240,331,"0802 大屏 + 手机同步",False),(305,146,"是",True),(216,200,"恢复",True),(70,200,"否",True)]
    return flow("p0804-3","全屋模块健康监测",nodes,edges,texts,"0804-3",103)

def p0804_4():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False)]
    texts=[(85,73,"任务写入 /queue/pending",False),(230,74,"NAS 队列",False),(230,87,"pending / running / done",True),(85,147,"Mac mini 每 5 分钟扫",False),(85,161,"按优先级取一条",False),(230,149,"是转码任务？",False),(230,162,"有人在看 > 识别 > 校验",True),(390,147,"是 → 立即硬件转码",False),(390,161,"推给 Jellyfin",False),(85,247,"否 → 等夜间窗口",False),(85,261,"23:00～6:00 批量识别",False),(230,247,"跑识别 / 校验",False),(230,261,"结果写 done",False),(390,247,"失败重试 3 次",False),(390,261,"仍失败 → failed + 汇总",False),(240,331,"NAS 只存不算 · 笔记本只稳不重",False),(305,146,"是",True),(216,200,"完成",True),(70,200,"否",True)]
    return flow("p0804-4","影音与识别任务分工",nodes,edges,texts,"0804-4",105)

def p0804_3p():
    pfx="p0804-3p"
    main="\n".join(['<path d="M50 130 h60 v70 h-60 Z" stroke-width="1.2"/><path d="M56 142 h48 M56 156 h48 M56 170 h48 M56 184 h30" stroke-width="0.9"/><circle cx="56" cy="142" r="2" stroke-width="0.6"/><circle cx="56" cy="156" r="2" stroke-width="0.6"/><circle cx="56" cy="170" r="2" stroke-width="0.6"/><circle cx="56" cy="184" r="2" stroke-width="0.6"/>',  # 设备列表
        '<path d="M120 165 H156" stroke-width="1" stroke-dasharray="3 3"/><path d="M152 161 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M166 140 h60 v50 h-60 Z" stroke-width="1.3"/><path d="M172 176 l10 -14 l8 8 l10 -20 l8 12 l12 -16" stroke-width="1"/><path d="M172 148 h48" stroke-width="0.5"/>',  # 心跳曲线
        '<path d="M236 165 H272" stroke-width="1" stroke-dasharray="3 3"/><path d="M268 161 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M284 132 h30 v56 h-30 Z M290 138 h18 v40 h-18 Z" stroke-width="1.2"/><path d="M294 150 h10 M294 158 h10 M294 166 h6" stroke-width="0.6"/><path d="M300 126 l-4 -6 h8 Z" stroke-width="0.8"/>',  # 手机推送
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>'])
    return poster(pfx,"0804 · L3","谁悄悄死了","几十个传感器，哪一个 40 分钟没说话",main,"设备层 last_seen + 服务层端口探测 → 双失联才推手机",
        ["每个设备用自己的上报周期算超时，不一刀切","单层失联只在大屏亮黄，双层失联才吵人","每周一封汇总：失联最多的 5 个"],
        "跑在：HomeAssistant + Uptime Kuma + Beszel · 数据出口：HA webhook / 0802 大屏","louislam/uptime-kuma · henrygd/beszel",107)

def p0804_4p():
    pfx="p0804-4p"
    main="\n".join(['<path d="M46 150 h50 v30 h-50 Z M52 158 h38 M52 166 h38 M52 174 h20" stroke-width="1.2"/>',  # NAS 队列
        '<path d="M106 165 H140" stroke-width="1" stroke-dasharray="3 3"/><path d="M136 161 l4 4 l-4 4" stroke-width="1"/>',
        '<rect x="150" y="146" width="60" height="36" rx="8" stroke-width="1.4"/><path d="M160 156 h40 M160 164 h30 M160 172 h36" stroke-width="0.6"/>',  # Mac mini
        '<path d="M220 156 Q250 130 280 140" stroke-width="1" stroke-dasharray="3 3"/><path d="M276 136 l4 4 l-5 2" stroke-width="1"/>',
        '<path d="M220 174 Q250 200 280 190" stroke-width="1" stroke-dasharray="3 3"/><path d="M276 194 l4 -4 l-5 -2" stroke-width="1"/>',
        '<path d="M284 124 h40 v28 h-40 Z M290 132 l10 6 l-10 6 Z" stroke-width="1.1"/>',  # 电视转码
        '<path d="M284 178 h40 v28 h-40 Z" stroke-width="1.1"/><path d="M290 198 q6 -14 12 -4 q4 -12 10 0 q4 -6 8 4" stroke-width="0.8"/>',  # 识别（鸟）
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>'])
    return poster(pfx,"0804 · L4","三台机器分工表","NAS 只存，笔记本只稳，Mac 干重活",main,"NAS 队列目录 → Mac mini 每 5 分钟取 → 转码优先 · 识别夜跑",
        ["有人在看的转码永远排第一","23:00～6:00 批量跑鸟类 / 物品识别","失败重试 3 次，仍失败进周汇总"],
        "跑在：M1 Mac mini launchd + Jellyfin · 数据出口：/queue/done 与 HA 任务实体","jellyfin/jellyfin",109)

def p0805_1():
    pfx="p0805-1"
    items=[lambda x,y: profile(x-60,y-8,120,16,14,pfx),  # 1 型材段
           lambda x,y: f'<path d="M{x-40} {y-6} h14 v10 h-14 Z M{x-33} {y-6} v-4 M{x-36} {y-10} h6" stroke-width="1.2"/><path d="M{x-14} {y-8} h22 v12 h-22 Z M{x-10} {y-4} h14 M{x-10} {y} h14" stroke-width="1.1"/><path d="M{x+16} {y-2} h20 M{x+16} {y-2} l-4 -4 M{x+16} {y-2} l-4 4 M{x+30} {y-6} h8 v8 h-8 Z" stroke-width="1"/>',  # 2 T 螺母 / 滑块螺母 / 螺栓
           lambda x,y: f'<path d="M{x-40} {y+6} v-24 h6 v18 h18 v6 Z" stroke-width="1.3"/><path d="M{x-38} {y+4} v-20 h2 v18 h16 v2 Z" fill="{SH(pfx)}" stroke="none"/><circle cx="{x-37}" cy="{y-14}" r="1.5" stroke-width="0.6"/><circle cx="{x-24}" cy="{y+3}" r="1.5" stroke-width="0.6"/><path d="M{x+4} {y-2} h26 v8 h-26 Z M{x+8} {y+2} h4 M{x+22} {y+2} h4" stroke-width="1.1"/><path d="M{x+30} {y-2} l6 -6 M{x+30} {y+6} l6 -6" stroke-width="0.6"/>',  # 3 角码 + 内置角槽件
           lambda x,y: f'<path d="M{x-30} {y-6} h16 v16 h-16 Z M{x-28} {y-4} h12 v12 h-12 Z" stroke-width="1"/><path d="M{x+2} {y-2} h30 v6 h-30 Z M{x+2} {y-2} l6 -5 h30 l-6 5" stroke-width="1"/><path d="M{x+8} {y+4} v6 M{x+26} {y+4} v6" stroke-width="0.6"/>',  # 4 端盖 + 层板托
           lambda x,y: f'<path d="M{x-40} {y-10} h34 v20 h-34 Z M{x-36} {y-6} h10 M{x-36} {y} h10 M{x-36} {y+6} h10 M{x-20} {y-6} h10" stroke-width="1"/><path d="M{x+2} {y-10} h34 v20 h-34 Z M{x+6} {y-6} h10 M{x+6} {y} h10 M{x+6} {y+6} h10 M{x+22} {y-6} h10" stroke-width="1"/><path d="M{x+4} {y-8} h30 v16 h-30 Z" fill="{SH(pfx)}" stroke="none"/>']  # 5 分箱
    legend=[(1,"欧标 2020 喷砂黑，槽宽 6mm，壁厚 1.8mm"),(2,"M5 T 型螺母 / 滑块螺母 + M5 内六角"),(3,"L 角码（外露）与内置角槽件（藏在槽里）"),(4,"端盖 + 层板托（MakerWorld 欧标 STL 可打印）"),(5,"配件分箱：20 系列（6mm）与 30/40 系列（8mm）不混")]
    return ex(pfx,"欧标 2020 型材配件套","0805-1",111,legend,"D3 定标 · 与国标完全不通用，不得混采",items,[(-64,-12),(-44,-10),(-44,-26),(-34,-10),(-44,-14)])

def p0805_2():
    pfx="p0805-2"
    items=[lambda x,y: profile(x-50,y-6,100,10,12,pfx)+profile(x-50,y-40,10,34,12,pfx)+profile(x+40,y-40,10,34,12,pfx)+profile(x-50,y-46,100,8,12,pfx),  # 1 型材框
           lambda x,y: f'<path d="M{x-40} {y+6} v-24 h6 v18 h18 v6 Z M{x+10} {y-2} h26 v8 h-26 Z" stroke-width="1.1"/><path d="M{x-38} {y+4} v-20 h2 v18 h16 v2 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+16} {y+2} h4 M{x+28} {y+2} h4" stroke-width="0.7"/>',  # 2 内置角槽件
           lambda x,y: f'<path d="M{x-56} {y+8} h100 l24 -16 h-100 Z" stroke-width="1.4"/><path d="M{x-56} {y+8} v6 h100 v-6 M{x+44} {y+14} l24 -16 v-6" stroke-width="1"/><path d="M{x-50} {y+4} q20 -6 40 -4 M{x-46} {y+6} q30 -8 60 -6 M{x-30} {y+2} q20 -6 40 -5" stroke-width="0.5"/>',  # 3 白蜡木面板
           lambda x,y: f'<path d="M{x-16} {y+4} q10 -14 26 -12 q10 2 16 8 q-12 6 -26 10 q-10 -2 -16 -6 Z" stroke-width="1.3"/><path d="M{x-12} {y+3} q10 -12 22 -10 q8 2 12 6 q-10 5 -22 8 q-8 -2 -12 -4 Z" fill="{SH(pfx)}" stroke="none"/><path d="M{x+18} {y-10} q6 -6 12 -2" stroke-width="0.8"/>',  # 4 植鞣皮
           lambda x,y: f'<path d="M{x-30} {y-10} h26 v18 h-26 Z M{x-26} {y-4} h18 M{x-26} {y+2} h12" stroke-width="1"/><path d="M{x+6} {y-8} a5 5 0 1 0 0.1 0 M{x+20} {y-8} a5 5 0 1 0 0.1 0 M{x+34} {y-8} a5 5 0 1 0 0.1 0" stroke-width="0.9"/><path d="M{x+6} {y-3} h28" stroke-width="0.5"/>']  # 5 色号卡
    legend=[(1,"底：2020 型材框 30×30cm（铝做骨）"),(2,"内置角槽件从背面固定，正面不露螺丝"),(3,"中：18mm 白蜡木面板，油蜡饰面，边留 2mm"),(4,"面：植鞣牛皮包角 8×8cm（只在手接触处）"),(5,"色号卡：喷砂黑 / 油蜡亮度 / 皮色两档")]
    return ex(pfx,"三材分层样板","0805-2",113,legend,"常年放在 0102 作品墙下，采购前先摸一下",items,[(-54,-14),(-44,-26),(-60,-6),(-20,-16),(-34,-14)])

def p0805_3():
    nodes=[("pill",30,52,110,34),("db",196,50,68,44),("step",30,130,110,40),("dia",172,128,116,48),("step",330,130,120,40),("step",30,230,110,40),("step",175,230,110,40),("step",330,230,120,40),("pill",175,312,130,30)]
    edges=[("M85 86 V128",False),("M196 72 Q160 72 140 72",True),("M140 150 H170",False),("M288 152 H328",False),("M230 176 V228",False),("M390 170 V228",False),("M85 170 V228",False),("M140 250 H173",False),("M230 270 V310",False),("M330 250 H287",False),("M30 250 Q10 250 10 150 Q10 130 28 130",True)]
    texts=[(85,73,"模块进入选型阶段",False),(230,74,"0805 规则表",False),(230,87,"三类主材 / D3 / 约束",True),(85,147,"列出方案里的",False),(85,161,"每种材料与规格",False),(230,149,"都在三类里？",False),(230,162,"木 / 铝型材 / 皮草",True),(390,147,"是 → 查型材规格",False),(390,161,"欧标 2020/3030 黑",False),(85,247,"否 → 改方案",False),(85,261,"或登记例外 + 理由",False),(230,247,"查接地 / 磨损面",False),(230,261,"强电独立接地 · 木覆盖",False),(390,247,"通过 → 进入选型",False),(390,261,"结论写回模块文档",False),(240,331,"木料 / 皮草定标后再回溯一遍",False),(305,146,"是",True),(216,200,"通过",True),(70,200,"否",True)]
    return flow("p0805-3","材质继承检查",nodes,edges,texts,"0805-3",115)

def p0805_3p():
    pfx="p0805-3p"
    main="\n".join(['<path d="M46 140 h56 v50 h-56 Z M52 150 h44 M52 160 h44 M52 170 h30 M52 180 h20" stroke-width="1.2"/>',  # 方案清单
        '<path d="M110 165 H146" stroke-width="1" stroke-dasharray="3 3"/><path d="M142 161 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M156 136 h56 v58 h-56 Z" stroke-width="1.4"/><path d="M164 150 h12 v10 h-12 Z M164 166 h12 v10 h-12 Z M164 182 h12 v6 h-12 Z M182 155 h24 M182 171 h24 M182 186 h16" stroke-width="0.8"/><path d="M166 154 l3 3 l6 -6 M166 170 l3 3 l6 -6" stroke-width="1"/>',  # 规则表勾选
        '<path d="M220 165 H256" stroke-width="1" stroke-dasharray="3 3"/><path d="M252 161 l4 4 l-4 4" stroke-width="1"/>',
        '<path d="M266 150 h50 v30 h-50 Z" stroke-width="1.2"/><path d="M274 165 l6 6 l14 -14" stroke-width="1.4"/><path d="M300 158 h10 M300 166 h10 M300 174 h6" stroke-width="0.6"/>',  # 通过章
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>'])
    return poster(pfx,"0805 · L3","材质守门员","选型之前，先过一遍三种材料的语法",main,"方案清单 → 三类主材？→ 型材规格 → 接地 / 磨损面 → 通过或登记例外",
        ["不是木 / 铝型材 / 皮草的，改方案或写明例外","型材只认欧标 2020/3030 喷砂黑，壁厚 1.8","强电模块独立接地，磨损面一律木料覆盖"],
        "跑在：设计对话（人肉 + FreeCAD 参数库）· 数据出口：各模块文档的材质结论","FreeCAD/FreeCAD · adgaudio/OpenSCAD_connectors",117)

if __name__=="__main__":
    out={"illos/0307.svg":m0307(),"illos/0804.svg":m0804(),"illos/0805.svg":m0805(),
         "parts/0307-1.svg":p0307_1(),"parts/0307-2.svg":p0307_2(),"parts/0307-3.svg":p0307_3(),"parts/0307-4.svg":p0307_4(),"parts/0307-3-poster.svg":p0307_3p(),"parts/0307-4-poster.svg":p0307_4p(),
         "parts/0804-1.svg":p0804_1(),"parts/0804-2.svg":p0804_2(),"parts/0804-3.svg":p0804_3(),"parts/0804-4.svg":p0804_4(),"parts/0804-3-poster.svg":p0804_3p(),"parts/0804-4-poster.svg":p0804_4p(),
         "parts/0805-1.svg":p0805_1(),"parts/0805-2.svg":p0805_2(),"parts/0805-3.svg":p0805_3(),"parts/0805-3-poster.svg":p0805_3p()}
    for k,v in out.items(): open(k,"w",encoding="utf-8").write(v)
    print("ok",len(out))
