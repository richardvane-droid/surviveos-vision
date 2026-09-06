from sk import *

def scene07(pfx, variant):
    H = f"url(#{pfx}-hatch)"; HL = f"url(#{pfx}-hatchl)"
    B = []
    # 河岸线 & 河（右下），对岸远处
    B.append('<path d="M40 232 Q140 226 250 236 T390 230" stroke-width="1.4"/>')
    for y, a in ((246, 0), (258, 12), (270, 4), (280, 16)):
        B.append(f'<path d="M{20+a} {y} q30 -4 60 0 t60 0 t60 0 t60 0 t60 0" stroke-width="0.7"/>')
    B.append('<path d="M14 60 q60 -10 120 0 M250 58 q40 -8 80 0" stroke-width="0.6" stroke-dasharray="3 3"/>')  # 对岸暗示
    # 缓坡：从左上（庭院/过道）斜下到钓台
    B.append('<path d="M14 120 L60 122 L130 200 L200 214" stroke-width="1.6"/><path d="M14 138 L58 140 L120 208" stroke-width="0.9"/>')
    B.append(f'<path d="M14 122 L60 124 L130 202 L124 212 L58 142 L14 140 Z" fill="{HL}" stroke="none"/>')
    # 踏步（缓坡上 4 级）+ 竹扶手
    for i in range(4):
        x = 66 + i*16; y = 130 + i*18
        B.append(f'<path d="M{x} {y} l10 2 l0 6 l-10 -2 Z" stroke-width="0.9"/>')
    B.append('<path d="M62 112 L128 186" stroke-width="1.2"/><path d="M66 128 v-14 M92 156 v-14 M118 184 v-14" stroke-width="0.9"/>')
    # 过道/庭院暗示（左上）：石墩 + 过道
    B.append('<path d="M14 104 h30 v14 h-30 Z" stroke-width="1"/><path d="M16 106 h26 v10 h-26 Z" fill="' + H + '" stroke="none"/>')
    # 钓台：2.5×2.2 木平台（斜轴测），台面 y≈206，右侧临河
    B.append('<path d="M150 214 L300 214 L340 190 L190 190 Z" stroke-width="1.8"/><path d="M150 214 v12 h150 v-12 M300 226 l40 -24 v-12" stroke-width="1.3"/>')
    B.append(f'<path d="M300 214 l40 -24 v12 l-40 24 Z" fill="{H}" stroke="none"/>')
    for i in range(1, 9):
        B.append(f'<path d="M{150+i*17} 214 l40 -24" stroke-width="0.5"/>')
    # 预制墩（台下）
    B.append('<path d="M160 226 v8 h10 v-8 M280 226 v8 h10 v-8 M322 202 v8 h8 v-8" stroke-width="0.9"/>')
    # 挡水条（临河侧）
    B.append('<path d="M300 212 l40 -24 M300 209 l40 -24" stroke-width="0.9"/>')
    if variant in ("area", "0701"):
        # 顶棚：四柱 + 单坡竹瓦，不超过台面
        B.append('<path d="M160 214 V120 M292 214 V128 M198 190 V104 M332 190 V112" stroke-width="1.4"/>')
        B.append('<path d="M150 118 L302 126 L342 108 L192 100 Z" stroke-width="1.6"/>')
        for i in range(1, 8):
            B.append(f'<path d="M{150+i*19} {118+i*1} l40 -18" stroke-width="0.6"/>')
        B.append('<path d="M150 118 l0 -6 l152 8 l0 6 M302 126 v-6 l40 -18 v6" stroke-width="0.9"/>')
        B.append('<path d="M300 130 v14 a3 3 0 1 0 0.1 0 M300 150 v10 a3 3 0 1 0 0.1 0" stroke-width="0.8"/>')  # 雨链
    # 一把椅子 + 一根竿 + 竿架
    B.append('<path d="M212 206 h16 v-14 h-16 Z M212 192 v-16 h16 v16 M214 206 v8 M226 206 v8" stroke-width="1.1"/>')
    B.append('<path d="M262 208 v-12 M262 196 L370 150" stroke-width="1"/><path d="M370 150 L376 232" stroke-width="0.5" stroke-dasharray="2 3"/>')
    B.append('<path d="M258 196 l8 0 M262 196 l-3 -4 M262 196 l3 -4" stroke-width="0.8"/>')
    # 小桌
    B.append('<path d="M240 204 h18 l6 -4 h-18 Z M240 204 v8 M258 204 v8 M264 200 v8" stroke-width="0.9"/>')
    if variant == "0703":
        # 夜：月亮、灯柱（光伏板顶）、电池箱
        B.append('<path d="M60 50 a14 14 0 1 0 12 20 a11 11 0 0 1 -12 -20" stroke-width="1.2"/>')
        B.append('<path d="M330 190 V110 M318 106 l24 -10 l14 4 l-24 10 Z" stroke-width="1.3"/><path d="M330 120 l-10 6 v8 l10 -6 Z" stroke-width="1"/>')
        B.append(f'<path d="M320 134 l-40 40 M340 130 l30 40" stroke-width="0.5" stroke-dasharray="2 2"/>')
        B.append('<path d="M170 208 h20 v-12 h-20 Z M172 200 h16" stroke-width="1"/><path d="M175 203 h3 M181 203 h3" stroke-width="0.7"/>')
        B.append('<path d="M100 40 l2 -2 M300 44 l2 2 M360 70 l2 -2 M40 90 l2 -2" stroke-width="1"/>')
    if variant == "0704":
        # 火塘（台面嵌盆）+ 矮桌 + 一只蒲团 + 水壶
        B.append('<path d="M232 202 a12 5 0 1 0 24 0 a12 5 0 1 0 -24 0" stroke-width="1.3"/><path d="M236 200 q4 -14 8 -4 q4 -12 6 0 q2 -8 4 2" stroke-width="0.9"/>')
        B.append('<path d="M238 196 q2 -30 12 -40 M248 194 q0 -20 8 -30" stroke-width="0.5" stroke-dasharray="2 3"/>')
        B.append('<path d="M270 208 h16 l6 -4 h-16 Z M270 208 v6 M286 208 v6" stroke-width="0.9"/><path d="M276 204 a3 2 0 1 0 6 0 a3 2 0 1 0 -6 0 M282 203 l3 -2" stroke-width="0.8"/>')
        B.append('<path d="M196 208 a8 3 0 1 0 16 0 a8 3 0 1 0 -16 0" stroke-width="1"/>')
    if variant == "area":
        fx, fy = 222, 210
    B.append(figure(300, 208, 0.75) if variant != "0704" else figure(204, 206, 0.6))
    # 草/芦苇
    B.append('<path d="M120 216 l2 -8 l2 8 M136 224 l2 -9 M360 226 l2 -8 l2 8 M376 224 l2 -7 M30 226 l3 -10 l3 10" stroke-width="0.9"/>')
    body = "\n".join(B)
    caps = {"area": "钓台 · 缓坡尽头临河 ≈2.5 × 2.2 m，面前是 10 米宽的河",
            "0701": "0701 · 岸上小平台 + 单坡竹瓦顶棚，不伸进水里",
            "0703": "0703 · 光伏灯柱 + 离网电池箱，一个人的夜钓灯",
            "0704": "0704 · 台面嵌一只铁盆火塘，一张矮桌，一只蒲团"}
    labels = "\n".join([
        label(14, 98, "庭院 → 2m 过道", 8), label(40, 186, "6m 缓坡", 8),
        label(300 if variant not in ("area","0701") else 245, 176 if variant not in ("area","0701") else 96, "钓台 ≈2.5×2.2", 8, "middle"),
        label(330, 262, "河 · 宽 10m", 9, "middle"), label(200, 290, caps[variant], 9.5, "middle", "#1c1c1c"),
    ])
    sig = "07 钓台" if variant == "area" else variant
    return illo(pfx, body, sig, seed=13).replace("</svg>", labels + "\n</svg>")

if __name__ == "__main__":
    for v, f in (("area", "area-07"), ("0701", "0701"), ("0703", "0703"), ("0704", "0704")):
        open(f"illos/{f}.svg", "w", encoding="utf-8").write(scene07("marea-07" if v == "area" else f"m{v}", v))
    print("ok")
