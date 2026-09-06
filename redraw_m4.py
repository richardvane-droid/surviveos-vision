from sk import *

def m0401():
    pfx="m0401"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 站在楼梯口向东看过道 3.5×3.2：平顶 2060 的核心区，尽头是木工间，再远处坡顶下落到东檐口
    # 近框：x 30..370, y 30..262；远框（3.5m 远）：x 150..250, y 96..190
    B.append('<path d="M30 30 L150 96 M370 30 L250 96 M30 262 L150 190 M370 262 L250 190" stroke-width="1.4"/>')
    B.append('<path d="M150 96 H250 V190 H150 Z" stroke-width="1.2" stroke-dasharray="4 3"/>')  # 过道尽头（进入木工间，无墙）
    # 远处木工间：地面延伸 + 坡顶从 2060 下落到东墙 0
    B.append('<path d="M150 190 L120 214 L280 214 L250 190 M150 96 L200 148 L250 96" stroke-width="1"/>')
    B.append(f'<path d="M150 96 L200 148 L250 96 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M175 152 h50 v22 h-50 Z M182 152 v-8 h36 v8 M200 152 v-14" stroke-width="1"/>')  # 台锯
    # 平顶（核心区 2060）线
    for i in range(1,4):
        t=i/4; B.append(f'<path d="M{30+120*t:.0f} {30+66*t:.0f} H{370-120*t:.0f}" stroke-width="0.5"/>')
    # 地板线
    for i in range(1,5):
        t=i/5; B.append(f'<path d="M{30+120*t:.0f} {262-72*t:.0f} H{370-120*t:.0f}" stroke-width="0.6"/>')
    # 左墙（北侧）= 工具墙：洞洞板 + 影子轮廓；墙后是 0402 低矮带（画一道半高栏板 + 坡顶）
    B.append('<path d="M40 58 L150 108 V184 L40 236 Z" stroke-width="1.3"/>')
    for k in range(6):
        t=k/6; x=42+108*t; y0=60+50*t; y1=236-52*t
        B.append(f'<path d="M{x:.0f} {y0:.0f} V{y1:.0f}" stroke-width="0.35"/>')
    for k in range(5):
        t=k/5; B.append(f'<path d="M42 {64+34*t:.0f} L148 {110+15*t:.0f}" stroke-width="0.35"/>')
    B.append('<path d="M60 110 l0 30 l14 -6 l0 -30 Z M62 112 h12 M90 120 l0 20 l8 -4 l0 -20 Z M110 130 l0 18 l8 -4 l0 -18 Z" stroke-width="1"/>')
    B.append('<path d="M60 90 l14 -6 M60 170 l14 -6 M90 100 l8 -4 M110 108 l8 -4" stroke-width="0.9"/>')
    # 右侧（南）= 通向阁楼间，无墙：帐篷尖顶露一角
    B.append('<path d="M250 190 L370 262 M250 96 L370 30" stroke-width="0.5"/>')
    B.append('<path d="M300 200 L330 150 L360 200" stroke-width="1.2"/><path d="M330 150 L330 200" stroke-width="0.6"/><path d="M302 199 L330 152 L330 199 Z" fill="' + H + '" stroke="none"/>')
    # 人（站在过道中，头顶有 2060 余量）+ 工具
    B.append(figure(200, 240, 1.15))
    B.append('<path d="M212 214 l10 -4 M222 210 l6 2" stroke-width="0.9"/>')
    # 天花高度标注
    B.append('<path d="M290 40 V250" stroke-width="0.5" stroke-dasharray="3 3"/><path d="M286 40 h8 M286 250 h8" stroke-width="0.6"/>')
    body="\n".join(B)
    labels="\n".join([label(94,52,"北侧工具墙（背后是 0402 低矮带）",7.5,"middle"), label(200,92,"→ 东：0404 木工间，坡顶落到檐口",7.5,"middle"),
                      label(330,146,"南：0303 帐篷",7.5,"middle"), label(300,146,"2060",7.5,"end"),
                      label(200,292,"0401 过道 3.5×3.2 m：整层唯一全程能站直的十字路口",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0401", seed=31).replace("</svg>", labels+"\n</svg>")

def m0402():
    pfx="m0402"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 北条剖面：向西看，北墙在右（檐口净高 0），坡顶 45° 向左上升到 2060；地面 y=240；1m=56px
    k=56; fy=240; xN=360  # 北檐口 x
    B.append(f'<path d="M20 {fy} H{xN}" stroke-width="1.8"/>')
    B.append(f'<path d="M{xN} {fy} L{xN-3.3*k} {fy-3.3*k+0}" stroke-width="1.8"/>')  # 45° 屋面（3.3m 进深，高 3.3?） 实际 2060 处在离墙 2.06m
    B.append(f'<path d="M{xN-2.06*k} {fy-2.06*k} V{fy}" stroke-width="0.7" stroke-dasharray="4 3"/>')
    B.append(f'<path d="M{xN-3.3*k} {fy} V{fy-3.3*k+8}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    # 椽条排线示意
    for i in range(1,12):
        x=xN-i*0.28*k; B.append(f'<path d="M{x:.0f} {fy-(xN-x):.0f} l-8 0" stroke-width="0.5"/>')
    # 低矮带：三层长直货架（贴屋面阶梯状，越靠外越矮）
    shelves=[(0.4,1.0,0.32),(1.0,1.5,0.88),(1.5,2.06,1.42)]
    for (a,b,h) in shelves:
        x0=xN-b*k; x1=xN-a*k; y=fy-h*k
        B.append(f'<path d="M{x0:.0f} {y:.0f} H{x1:.0f} M{x0:.0f} {y:.0f} V{fy}" stroke-width="1.2"/>')
        B.append(f'<path d="M{x0:.0f} {y+3:.0f} H{x1-2:.0f} v3 H{x0:.0f} Z" fill="{H}" stroke="none"/>')
        # 板材/方料横躺
        for j in range(2):
            B.append(f'<path d="M{x0+4+j*3:.0f} {y-4-j*5:.0f} h{(x1-x0)-10-j*6:.0f} v4 h-{(x1-x0)-10-j*6:.0f} Z" stroke-width="0.7"/>')
        for hh in (0.3, 0.6, 0.9, 1.2):
            if hh < h-0.1: B.append(f'<path d="M{x0+2:.0f} {fy-hh*k:.0f} H{x1-2:.0f}" stroke-width="0.6"/>')
    # 长料沿东西向：用透视短线示意（几根圆管端头）
    for j in range(3):
        B.append(f'<circle cx="{xN-0.12*k-j*7:.0f}" cy="{fy-0.08*k-j*3:.0f}" r="3" stroke-width="0.7"/>')
    # 站立带（内侧 1.24m）：人站着取货 + 脚轮 A 字架
    B.append(figure(xN-2.75*k, fy, 1.1))
    B.append(f'<path d="M{xN-2.6*k:.0f} {fy-1.5*k:.0f} l14 -6" stroke-width="0.9"/>')
    B.append(f'<path d="M{xN-3.5*k:.0f} {fy-6} l14 -{1.6*k} l14 {1.6*k} M{xN-3.5*k+4:.0f} {fy-6} h22" stroke-width="1.1"/><circle cx="{xN-3.5*k+2:.0f}" cy="{fy-2}" r="3" stroke-width="0.8"/><circle cx="{xN-3.5*k+26:.0f}" cy="{fy-2}" r="3" stroke-width="0.8"/>')
    for j in range(4):
        B.append(f'<path d="M{xN-3.5*k+6+j*3:.0f} {fy-10} l8 -{1.3*k-j*8}" stroke-width="0.5"/>')
    # 尺寸标注
    B.append(f'<path d="M{xN-1.24*k-2.06*k:.0f} {fy+12} H{xN-2.06*k:.0f} M{xN-2.06*k:.0f} {fy+12} H{xN}" stroke-width="0.6"/><path d="M{xN-3.3*k:.0f} {fy+8} v8 M{xN-2.06*k:.0f} {fy+8} v8 M{xN} {fy+8} v8" stroke-width="0.6"/>')
    body="\n".join(B)
    labels="\n".join([label(xN-1.03*k,fy+26,"低矮带 2.06 m：只放货架",7.5,"middle"), label(xN-2.68*k,fy+26,"站立带 1.24 m",7.5,"middle"),
                      label(xN-2.06*k-4,fy-2.1*k-6,"净高 2060",7.5,"end"), label(xN-0.2*k,fy-0.6*k,"北墙",7.5,"end"),
                      label(120,60,"离外墙多少米，天花板就多高",8.5,"middle"),
                      label(200,292,"0402 材料仓库：北条 7.5×3.3 m 的剖面，货架贴着坡顶阶梯排",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0402", seed=33).replace("</svg>", labels+"\n</svg>")

def m0403():
    pfx="m0403"; H=f"url(#{pfx}-hatch)"; HL=f"url(#{pfx}-hatchl)"
    B=[]
    # 木工间东缘剖面：向北看，东墙在右；坡顶 45°；喷涂柜在核心区东缘（离东墙 2.06m），排风直管向东出墙
    k=50; fy=236; xE=372
    B.append(f'<path d="M14 {fy} H{xE}" stroke-width="1.8"/><path d="M{xE} {fy} L{xE-4.2*k} {fy-4.2*k+0}" stroke-width="1.8"/>')
    B.append(f'<path d="M{xE-2.06*k} {fy-2.06*k} V{fy}" stroke-width="0.6" stroke-dasharray="4 3"/>')
    for i in range(1,15):
        x=xE-i*0.28*k; B.append(f'<path d="M{x:.0f} {fy-(xE-x):.0f} l-7 0" stroke-width="0.5"/>')
    # 喷涂柜 1.5(宽)×1.0(深)：剖面看到深 1.0 → 50px；台面 0.9，柜高 1.6；下抽风机在台面下
    cx0=xE-2.06*k-1.0*k; cx1=xE-2.06*k
    B.append(f'<path d="M{cx0} {fy} V{fy-1.6*k} H{cx1} V{fy}" stroke-width="1.6"/>')
    B.append(f'<path d="M{cx0} {fy-0.9*k} H{cx1}" stroke-width="1.2"/>')
    for j in range(6): B.append(f'<path d="M{cx0+6+j*7} {fy-0.9*k} v-4 M{cx0+9+j*7} {fy-0.9*k} v-4" stroke-width="0.5"/>')  # 格栅
    B.append(f'<path d="M{cx0+8} {fy-0.6*k} h{1.0*k-16} v{0.25*k} h-{1.0*k-16} Z" stroke-width="1"/><path d="M{cx0+10} {fy-0.58*k} h{1.0*k-20} v3 h-{1.0*k-20} Z" fill="{H}" stroke="none"/>')  # 过滤棉
    B.append(f'<circle cx="{(cx0+cx1)/2}" cy="{fy-0.22*k}" r="9" stroke-width="1.1"/><path d="M{(cx0+cx1)/2-6} {fy-0.22*k} h12 M{(cx0+cx1)/2} {fy-0.22*k-6} v12" stroke-width="0.7"/>')  # 风机
    B.append(f'<path d="M{cx0+4} {fy-1.6*k} l-10 -14 h{1.0*k+6} l4 14" stroke-width="0.9"/><path d="M{cx0+2} {fy-1.55*k} v-{0.6*k} M{cx1-2} {fy-1.55*k} v-{0.6*k}" stroke-width="0.5" stroke-dasharray="2 2"/>')  # 柜顶挡板
    # 排风直管：从风机向东，穿低矮圈到东墙，约 2.06m，一根到底
    py=fy-0.3*k
    B.append(f'<path d="M{cx1} {py-6} H{xE+6} M{cx1} {py+6} H{xE+6}" stroke-width="1.2"/><path d="M{xE+6} {py-9} v18 M{xE+12} {py-6} l8 0 l-3 -3 M{xE+12} {py+6} l8 0 l-3 3" stroke-width="0.8"/>')
    for x in range(int(cx1)+10, int(xE), 16): B.append(f'<path d="M{x} {py-6} v12" stroke-width="0.4"/>')
    # 台锯在北段 5m 外（画在左侧远处，虚线距离）
    B.append(f'<path d="M30 {fy} v-{0.85*k} h50 v{0.85*k} M40 {fy-0.85*k} v-8 h30 v8 M55 {fy-0.85*k} v-14" stroke-width="1"/>')
    B.append(f'<path d="M84 {fy-1.1*k} H{cx0-4}" stroke-width="0.5" stroke-dasharray="3 3"/><path d="M84 {fy-1.1*k-4} v8 M{cx0-4} {fy-1.1*k-4} v8" stroke-width="0.6"/>')
    # 人（戴口罩喷漆）
    B.append(figure(cx0-26, fy, 1.05)); B.append(f'<path d="M{cx0-20} {fy-30} l14 -4 l6 4" stroke-width="0.9"/><path d="M{cx0+4} {fy-1.2*k} l-6 -6 M{cx0+8} {fy-1.25*k} l-4 -8" stroke-width="0.4" stroke-dasharray="1 2"/>')
    # 小零件（喷涂中）
    B.append(f'<path d="M{cx0+18} {fy-0.9*k-2} v-12 h14 v12" stroke-width="0.9"/>')
    body="\n".join(B)
    labels="\n".join([label((cx0+cx1)/2,fy-1.6*k-26,"0403 下抽式喷涂柜 1.5×1.0",8,"middle"), label((cx1+xE)/2,py-14,"排风直管 ≈2.06 m 出东墙",7.5,"middle"),
                      label(xE-6,fy-0.9*k,"东墙",7.5,"end"), label(120,fy-1.1*k-8,"与台锯拉开 ≥5 m",7.5,"middle"), label(55,fy+14,"台锯（北段）",7.5,"middle"),
                      label(200,292,"不做喷漆间：木工间东缘一只柜子，一根直管把漆雾送出墙",9.5,"middle","#1c1c1c")])
    return illo(pfx, body, "0403", seed=35).replace("</svg>", labels+"\n</svg>")

if __name__=="__main__":
    open("illos/0401.svg","w",encoding="utf-8").write(m0401())
    open("illos/0402.svg","w",encoding="utf-8").write(m0402())
    open("illos/0403.svg","w",encoding="utf-8").write(m0403())
    print("ok")
