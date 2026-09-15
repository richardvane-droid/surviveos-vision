# -*- coding: utf-8 -*-
"""重绘 0305（自建 Voron 2.4 + 铝型材工作站）与 0307（三轴龙门雕刻机）的插图与拆解图。
画风沿用 sk.py / redraw_08.py / redraw_09.py 的既有手法，只换里面的图形与标注。
用法：cd /home/claude/vision && python3 redraw_0305_0307.py
"""
from sk import *
from redraw_08 import SH, along, finish, flow, poster
from redraw_09 import ex, profile

COMIC = "'Comic Sans MS','Segoe Print','Bradley Hand',cursive"


# =============================== illos ===============================
def m0305():
    """阁楼：铝型材工作站上层嵌一台自建 Voron 2.4，侧板翻开、接屑盘抽出，排风管走天窗。"""
    pfx = "m0305"
    H = f"url(#{pfx}-hatch)"; H2 = f"url(#{pfx}-hatch2)"; HL = f"url(#{pfx}-hatchl)"
    B = []
    # --- 地面 ---
    B.append('<path d="M14 270 H386" stroke-width="1.6"/>')
    B.append('<path d="M30 276 q26 -3 52 0 M206 276 q22 -3 44 0" stroke-width="0.6"/>')
    # --- 天花一段 + 排气口 ---
    B.append('<path d="M296 22 H386" stroke-width="1.4"/>')
    B.append(f'<path d="M296 16 H386 V22 H296 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M314 22 V36 H346 V22" stroke-width="1.3"/>')
    B.append('<path d="M318 26 H342 M318 30 H342 M330 23 V36" stroke-width="0.7"/>')
    B.append('<path d="M330 14 V4 M326 9 l4 -5 l4 5" stroke-width="0.8"/>')
    # --- 排风管：从腔体顶后部升起 → 沿天花走 → 进排气口 ---
    B.append('<path d="M158 88 V54 Q158 46 166 46 H334 V36" stroke-width="1.6"/>')
    B.append('<path d="M172 88 V62 Q172 56 180 56 H320 Q328 56 328 48 V36" stroke-width="1.6"/>')
    B.append('<path d="M158 70 H172 M158 80 H172" stroke-width="0.7"/>')
    for x in (198, 228, 258, 288, 314):
        B.append(f'<path d="M{x} 46 V56" stroke-width="0.7"/>')
    B.append(f'<path d="M182 47 H318 V55 H182 Z" fill="{H}" stroke="none"/>')
    # --- 工作站型材骨架（前脸 96~160，进深 +18,-10）---
    B.append('<path d="M96 270 V74 H103 V270" stroke-width="1.6"/>')     # 左立柱 3030
    B.append('<path d="M153 270 V74 H160 V270" stroke-width="1.6"/>')     # 右立柱 3030
    B.append('<path d="M96 74 H160 V82 H96 Z" stroke-width="1.5"/>')      # 顶横梁
    B.append('<path d="M96 156 H160 V163 H96 Z" stroke-width="1.5"/>')    # 台面横梁
    B.append('<path d="M96 250 H160 V257 H96 Z" stroke-width="1.4"/>')    # 底横梁
    B.append('<path d="M96 74 l18 -10 H178 l-18 10 M160 74 l18 -10 v8 l-18 10" stroke-width="1"/>')
    B.append('<path d="M178 64 V258 M160 270 l18 -12" stroke-width="0.8"/>')
    B.append(f'<path d="M161 75 l16 -9 v7 l-16 9 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M99 90 V250 M157 90 V250" stroke-width="0.4"/>')    # 型材槽线
    # 脚：可调脚垫
    B.append('<path d="M100 257 V266 M156 257 V266" stroke-width="1.3"/>')
    B.append('<path d="M94 266 H110 V270 H94 Z M150 266 H166 V270 H150 Z" stroke-width="1.1"/>')
    # --- 木台面板（覆在型材上）---
    B.append('<path d="M90 150 H166 V156 H90 Z" stroke-width="1.4"/>')
    B.append('<path d="M90 150 l18 -10 H184 l-18 10" stroke-width="1"/>')
    B.append('<path d="M96 153 h62 M110 146 q22 -2 44 0" stroke-width="0.4"/>')
    # --- Voron 2.4 机身（全封闭方腔）---
    B.append('<path d="M102 150 V98 H154 V150 Z" stroke-width="2"/>')
    B.append('<path d="M105 148 V101 H151" stroke-width="0.9"/>')
    B.append('<path d="M102 98 l18 -10 H172 l-18 10 M154 98 l18 -10 V140 l-18 10" stroke-width="1.3"/>')
    B.append(f'<path d="M155 99 l16 -9 v49 l-16 9 Z" fill="{H}" stroke="none"/>')
    # 玻璃门（腔口）
    B.append('<path d="M108 106 H148 V146 H108 Z" stroke-width="1.4"/>')
    B.append('<path d="M110 108 H146 V144" stroke-width="0.8"/>')
    B.append('<path d="M112 110 l9 9 M144 110 l-9 9 M112 142 l9 -9" stroke-width="0.6"/>')
    # 腔内：CoreXY 龙门 + 打印头 + 热床 + 四丝杠
    B.append('<path d="M112 116 H144" stroke-width="1.2"/>')
    B.append('<path d="M112 110 H144" stroke-width="0.6"/>')
    B.append('<path d="M124 112 h12 v10 h-12 Z M128 122 v4 l2 3 M132 122 v4 l-2 3" stroke-width="1.1"/>')
    B.append('<path d="M114 138 H142 V142 H114 Z" stroke-width="1.2"/>')
    B.append('<path d="M124 138 v-8 h8 v8 M126 134 h4" stroke-width="1"/>')
    B.append('<path d="M113 112 V143 M143 112 V143" stroke-width="0.6"/>')
    for y in (120, 126, 132, 138):
        B.append(f'<path d="M111 {y} h4 M141 {y} h4" stroke-width="0.4"/>')
    # --- 翻开的侧板（铰链 + 磁扣）---
    B.append('<path d="M102 98 L80 107 V155 L102 150 Z" fill="#fff" stroke="none"/>')
    B.append(f'<path d="M100 100 L84 106 V152 L100 147 Z" fill="{HL}" stroke="none"/>')
    B.append('<path d="M102 98 L80 107 V155 L102 150" stroke-width="1.6"/>')
    B.append('<circle cx="102" cy="107" r="2.2" stroke-width="0.9"/><circle cx="102" cy="142" r="2.2" stroke-width="0.9"/>')
    B.append('<path d="M82 126 h5 v5 h-5 Z" stroke-width="0.9"/>')
    B.append('<path d="M92 96 a16 16 0 0 0 -12 8 M80 104 l1 -5 M80 104 l5 1" stroke-width="0.8"/>')
    # --- 接屑盘（整块抽出）---
    B.append('<path d="M70 166 H160 V178 H70 Z" fill="#fff" stroke="none"/>')
    B.append('<path d="M70 166 H160 V178 H70 Z" stroke-width="1.5"/>')
    B.append('<path d="M73 169 H157 V176" stroke-width="0.7"/>')
    B.append(f'<path d="M73 174 H157 V177 H73 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M66 168 V176" stroke-width="1.6"/>')
    B.append('<path d="M92 173 l3 -3 M106 174 l3 -3 M122 172 l3 -3 M138 174 l3 -3" stroke-width="0.6"/>')
    # --- 耗材干燥箱 ---
    B.append('<path d="M98 184 H158 V216 H98 Z" stroke-width="1.4"/>')
    B.append('<path d="M100 186 H156 V214" stroke-width="0.7"/>')
    B.append('<circle cx="118" cy="200" r="11" stroke-width="1.2"/><circle cx="118" cy="200" r="4" stroke-width="0.8"/>')
    B.append(f'<path d="M118 200 m-11 0 a11 11 0 0 0 22 0 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M138 190 H152 V199 H138 Z" stroke-width="1"/>')
    B.append('<path d="M141 194 h8 M141 197 h5" stroke-width="0.6"/>')
    B.append('<path d="M138 206 h14 M138 210 h9" stroke-width="0.5"/>')
    # --- 工具抽屉 ---
    B.append('<path d="M98 222 H158 V248 H98 Z" stroke-width="1.4"/>')
    B.append('<path d="M100 224 H156 V246" stroke-width="0.7"/>')
    B.append('<path d="M118 236 H138" stroke-width="1.6"/>')
    B.append(f'<path d="M100 242 H156 V246 H100 Z" fill="{H}" stroke="none"/>')
    # --- 站着的人（平视腔口）---
    B.append('<circle cx="320" cy="76" r="11" stroke-width="1.5"/>')
    B.append('<path d="M309 78 l-4 1 l4 2" stroke-width="0.8"/>')
    B.append('<path d="M320 87 V160 M306 100 H334 M309 160 H331" stroke-width="1.5"/>')
    B.append('<path d="M307 101 L302 130 L310 150 M333 101 L338 132 L330 152" stroke-width="1.4"/>')
    B.append('<path d="M311 160 L307 270 M329 160 L333 270 M307 270 H295 M333 270 H345" stroke-width="1.5"/>')
    # 视线
    B.append('<path d="M307 74 L158 126" stroke-width="0.8" stroke-dasharray="4 3"/>')
    B.append('<path d="M164 122 l-6 4 l6 3" stroke-width="0.8"/>')
    # --- 碎屑桶 ---
    B.append('<path d="M354 248 L358 270 H378 L382 248 Z" stroke-width="1.3"/>')
    B.append('<path d="M352 248 H384" stroke-width="1.2"/>')
    B.append(f'<path d="M360 262 H377 L376 269 H361 Z" fill="{H}" stroke="none"/>')
    # --- 尺寸线：腔口中心 1100~1200 ---
    B.append('<path d="M174 126 H252" stroke-width="0.6" stroke-dasharray="4 3"/>')
    B.append('<path d="M246 126 V270" stroke-width="0.9"/>')
    B.append('<path d="M246 126 l-3 7 M246 126 l3 7 M246 270 l-3 -7 M246 270 l3 -7" stroke-width="0.9"/>')

    body = "\n".join(B)
    labels = "\n".join([
        label(76, 86, "Voron 2.4 自建机", 7, "end"),
        label(76, 96, "CoreXY 全封闭腔", 7, "end"),
        label(76, 120, "侧板可翻开 · 清碎屑", 7, "end"),
        label(62, 192, "接屑盘整块抽出", 7, "end"),
        label(66, 222, "铝型材工作站", 7.5, "end"),
        label(66, 233, "占地 0.5×0.5m", 7.5, "end"),
        label(166, 200, "耗材干燥箱", 7, "start"),
        label(166, 238, "工具抽屉", 7, "start"),
        label(240, 170, "腔口中心 1100～1200", 7.5, "end"),
        label(232, 88, "站姿平视", 7, "middle"),
        label(384, 50, "→ 天窗排气口", 7, "end"),
        label(200, 290, "0305：从拧第一颗螺丝开始的 Voron 2.4，站着平视就能看进腔里", 9.5, "middle", "#1c1c1c"),
    ])
    svg = illo(pfx, body, "0305", seed=7).replace("</svg>", labels + "\n</svg>")
    # 签名字体沿用原文件
    return svg.replace(f'font-family="{HAND}" font-size="10"', f'font-family="{COMIC}" font-size="10"')


def m0307():
    """阁楼：三轴龙门雕刻机（无任何旋转轴），阳光板防护罩，排屑管走 0404，旁边两张待定路线清单。"""
    pfx = "m0307"
    H = f"url(#{pfx}-hatch)"; HL = f"url(#{pfx}-hatchl)"
    B = []
    # --- 地面 + 坡顶 + 矮墙 ---
    B.append('<path d="M14 252 H386" stroke-width="1.6"/>')
    B.append('<path d="M90 40 H230 L372 199" stroke-width="1.5"/>')
    B.append('<path d="M372 199 V252" stroke-width="1.3"/>')
    B.append(f'<path d="M90 34 H230 V40 H90 Z" fill="{H}" stroke="none"/>')
    for i in range(1, 11):
        t = i / 11.0
        B.append(f'<path d="M{230+142*t:.1f} {40+159*t:.1f} l-7 2" stroke-width="0.5"/>')
    # --- 阳光板防护罩 ---
    B.append('<path d="M76 252 V100 H252 V252" stroke-width="1" stroke-dasharray="5 3"/>')
    B.append(f'<path d="M78 102 h172 v148 h-172 Z" fill="{HL}" stroke="none" fill-opacity="0.32"/>')
    # --- 机架：底座框 + 台面 ---
    B.append('<path d="M88 252 V236 H238 V252" stroke-width="1.6"/>')
    B.append(f'<path d="M90 238 h146 v12 h-146 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M82 236 H244 V228 H82 Z" stroke-width="1.4"/>')
    B.append('<path d="M84 232 H242" stroke-width="0.5"/>')
    # --- 龙门：两立柱 + 横梁（X 轴）---
    B.append('<path d="M100 228 V132 H110 V228" stroke-width="1.6"/>')
    B.append('<path d="M216 228 V132 H226 V228" stroke-width="1.6"/>')
    B.append('<path d="M105 224 V138 M221 224 V138" stroke-width="0.4"/>')
    B.append('<path d="M100 132 H226 V118 H100 Z" stroke-width="1.6"/>')
    B.append('<path d="M102 125 H224" stroke-width="0.5"/>')
    # --- 滑车 + Z 轴 + 主轴 ---
    B.append('<path d="M146 112 H178 V138 H146 Z" stroke-width="1.4"/>')
    B.append('<path d="M148 114 H176 V136" stroke-width="0.6"/>')
    B.append('<path d="M154 138 H170 V176 H154 Z" stroke-width="1.3"/>')
    B.append('<path d="M157 142 V172 M167 142 V172" stroke-width="0.5"/>')
    B.append('<path d="M152 176 H172 V204 H152 Z" stroke-width="1.4"/>')
    B.append('<path d="M154 182 H170 M154 188 H170 M154 194 H170" stroke-width="0.6"/>')
    B.append(f'<path d="M165 177 h6 v26 h-6 Z" fill="{H}" stroke="none"/>')
    B.append('<path d="M157 204 H167 L165 212 H159 Z" stroke-width="1.2"/>')
    B.append('<path d="M162 212 V220" stroke-width="1.3"/>')
    # 吸尘罩（透空画法）
    B.append('<path d="M146 198 H178 V206 L174 220 H150 L146 206 Z" stroke-width="0.9" stroke-dasharray="3 2"/>')
    # 吸尘软管：沿 Z 爬到滑车
    B.append('<path d="M146 202 C128 186 142 170 132 154 C126 142 138 132 146 118" stroke-width="1.1"/>')
    for (rx, ry) in ((138, 190), (138, 172), (130, 150), (138, 130)):
        B.append(f'<path d="M{rx} {ry} l7 2" stroke-width="0.5"/>')
    # --- 工件：胡桃木板 + 压板 ---
    B.append('<path d="M114 228 V218 H208 V228" stroke-width="1.5"/>')
    B.append('<path d="M118 222 H204 M118 225 H194" stroke-width="0.4"/>')
    B.append('<path d="M156 218 l3 5 h6 l3 -5" stroke-width="0.9"/>')
    B.append('<path d="M120 218 V210 H130 V218 M188 218 V210 H198 V218" stroke-width="1.1"/>')
    # --- 三根轴的箭头 ---
    B.append('<path d="M182 146 H212 M182 146 l7 -4 M182 146 l7 4 M212 146 l-7 -4 M212 146 l-7 4" stroke-width="1"/>')
    B.append('<path d="M186 154 V188 M186 154 l-4 7 M186 154 l4 7 M186 188 l-4 -7 M186 188 l4 -7" stroke-width="1"/>')
    B.append('<path d="M88 230 L66 243 M88 230 l-1 8 M88 230 l7 0 M66 243 l1 -8 M66 243 l-7 0" stroke-width="1"/>')
    # --- 排屑管 → 0404 ---
    B.append('<path d="M180 104 H248 L360 196" stroke-width="1.5"/>')
    B.append('<path d="M180 114 H242 L354 206" stroke-width="1.5"/>')
    B.append('<path d="M180 104 V114" stroke-width="1.2"/>')
    for x in (198, 216, 234):
        B.append(f'<path d="M{x} 104 V114" stroke-width="0.5"/>')
    for t in (0.22, 0.42, 0.62, 0.82):
        B.append(f'<path d="M{248+112*t:.1f} {104+92*t:.1f} l-6 10" stroke-width="0.5"/>')
    B.append('<path d="M360 196 l10 2 l-4 6" stroke-width="0.9"/>')
    # --- 两张待定路线清单（钉在左墙上）---
    B.append('<path d="M14 142 V66 H72 V142 Z" stroke-width="1.4"/>')
    B.append('<path d="M17 139 V69 H69" stroke-width="0.5"/>')
    B.append('<path d="M20 86 H66" stroke-width="0.7"/>')
    B.append('<circle cx="24" cy="131" r="4.5" stroke-width="1.1"/>')
    B.append('<path d="M14 228 V152 H72 V228 Z" stroke-width="1.4"/>')
    B.append('<path d="M17 225 V155 H69" stroke-width="0.5"/>')
    B.append('<path d="M20 172 H66" stroke-width="0.7"/>')
    B.append('<circle cx="24" cy="217" r="4.5" stroke-width="1.1"/>')
    # --- 人（站着看）---
    B.append(figure(276, 252, 1.6, 1.4))
    B.append('<path d="M186 199 L174 194" stroke-width="0.7" stroke-dasharray="3 2"/>')

    body = "\n".join(B)
    labels = "\n".join([
        label(43, 58, "主材待定 · 两条路线", 7, "middle"),
        label(43, 81, "木 / 亚克力", 7.5, "middle"),
        label(43, 100, "2020+3030 机架", 6.5, "middle"),
        label(43, 112, "500W 风冷主轴", 6.5, "middle"),
        label(43, 124, "行程 300×300×100", 6.5, "middle"),
        label(38, 134, "未选", 6.5, "start"),
        label(43, 167, "铝（加强刚性）", 7.5, "middle"),
        label(43, 186, "全 4040 + 钢板", 6.5, "middle"),
        label(43, 198, "1.5kW 水冷主轴", 6.5, "middle"),
        label(43, 210, "行程 200×200×80", 6.5, "middle"),
        label(38, 220, "未选", 6.5, "start"),
        label(178, 149, "X", 7.5, "end"),
        label(192, 174, "Z", 7.5, "start"),
        label(62, 250, "Y", 7.5, "end"),
        label(104, 94, "阳光板防护罩", 7, "middle"),
        label(188, 202, "主轴待定", 6.5, "start"),
        label(110, 212, "胡桃木板", 7, "end"),
        label(294, 238, "排屑管 → 0404 木工间集尘", 6, "start"),
        label(163, 266, "龙门机架 · 铝型材", 7.5, "middle"),
        label(200, 286, "0307：一台三轴龙门雕刻机，X / Y / Z 三根轴，木屑顺管走向木工间", 9.5, "middle", "#1c1c1c"),
    ])
    return illo(pfx, body, "0307", seed=81).replace("</svg>", labels + "\n</svg>")


# =============================== parts · 0305 ===============================
def p0305_1():
    """Voron 2.4 机架与运动系统 · 爆炸图"""
    pfx = "p0305-1"
    S = SH(pfx)
    items = [
        # 1 2020 型材骨架（方框）
        lambda x, y: (profile(x - 56, y - 6, 112, 12, 12, pfx)
                      + profile(x - 56, y - 40, 12, 34, 12, pfx)
                      + profile(x + 44, y - 40, 12, 34, 12, pfx)),
        # 2 四丝杠同步升降热床
        lambda x, y: (f'<path d="M{x-44} {y} h88 v8 h-88 Z M{x-44} {y} l12 -8 h88 l-12 8" stroke-width="1.4"/>'
                      f'<path d="M{x-42} {y+2} h84 v4 h-84 Z" fill="{S}" stroke="none"/>'
                      + "".join(f'<path d="M{x+dx} {y+8} v26 M{x+dx-3} {y+16} h6 M{x+dx-3} {y+22} h6 M{x+dx-3} {y+28} h6" stroke-width="0.9"/>'
                                for dx in (-38, -14, 14, 38))
                      + f'<path d="M{x-20} {y-12} h40 v6 h-40 Z" stroke-width="0.8"/>'),
        # 3 CoreXY 皮带 + 固定电机
        lambda x, y: (f'<path d="M{x-46} {y-16} h92 v32 h-92 Z" stroke-width="1.3"/>'
                      f'<path d="M{x-40} {y-10} h80 v20 h-80 Z" stroke-width="0.6" stroke-dasharray="3 2"/>'
                      f'<path d="M{x-46} {y-16} l-10 -8 h92 l10 8 M{x+46} {y-16} l10 -8 v32" stroke-width="0.8"/>'
                      + "".join(f'<path d="M{x+dx-7} {y+dy-7} h14 v14 h-14 Z" stroke-width="1.1"/><circle cx="{x+dx}" cy="{y+dy}" r="3" stroke-width="0.7"/>'
                                for dx, dy in ((-46, -16), (46, -16)))
                      + f'<path d="M{x-46} {y-16} L{x+46} {y+16} M{x-46} {y+16} L{x+46} {y-16}" stroke-width="0.9"/>'),
        # 4 打印头（挤出机 + 热端 + 探针）
        lambda x, y: (f'<path d="M{x-16} {y-16} h32 v26 h-32 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-12} {y-12} h14 v14 h-14 Z" fill="{S}" stroke="none"/>'
                      f'<circle cx="{x+8}" cy="{y-4}" r="6" stroke-width="0.9"/>'
                      f'<path d="M{x-6} {y+10} h12 v8 l-3 6 h-6 l-3 -6 Z" stroke-width="1.2"/>'
                      f'<path d="M{x-24} {y+4} v12 M{x-27} {y+16} h6" stroke-width="1"/>'
                      f'<path d="M{x-2} {y-16} v-10 M{x-6} {y-26} h8" stroke-width="0.9"/>'),
        # 5 板材封闭腔体 + 玻璃门
        lambda x, y: (f'<path d="M{x-44} {y-24} h88 v48 h-88 Z" stroke-width="1.5"/>'
                      f'<path d="M{x-44} {y-24} l12 -8 h88 l-12 8 M{x+44} {y-24} l12 -8 v48 l-12 8" stroke-width="1"/>'
                      f'<path d="M{x+45} {y-23} l10 -7 v46 l-10 7 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x-34} {y-16} h46 v32 h-46 Z" stroke-width="1"/>'
                      f'<path d="M{x-30} {y-12} l8 8 M{x+8} {y-12} l-8 8 M{x-30} {y+12} l8 -8" stroke-width="0.5"/>'
                      f'<path d="M{x+20} {y-14} h16 v10 h-16 Z M{x+22} {y+2} h12 M{x+22} {y+8} h12" stroke-width="0.7"/>'),
    ]
    legend = [(1, "2020 型材骨架 · 250 方案，行程 250×250×250"),
              (2, "四丝杠同步升降热床，开机自动扫描补偿倾斜"),
              (3, "CoreXY 交叉皮带 + 机身固定电机（惯量小能开高速）"),
              (4, "打印头：挤出机 + 热端 + 调平探针"),
              (5, "板材封闭腔体 + 玻璃门，腔温 50℃ 以上")]
    return ex(pfx, "Voron 2.4 机架与运动系统", "0305-1", 121, legend,
              "按官方 BOM 自己配件自己拧 · 结构件 ABS 打印 100+ 件，第一批需代打",
              items, [(-60, -10), (-48, -14), (-50, -18), (-20, -18), (-48, -26)])


def p0305_2():
    """铝型材工作站与人体工学高度 · 爆炸图（附腔口高度尺寸线）"""
    pfx = "p0305-2"
    S = SH(pfx)
    items = [
        # 1 可调脚垫 + 2020 底框
        lambda x, y: (profile(x - 52, y - 6, 104, 10, 10, pfx)
                      + "".join(f'<ellipse cx="{x+dx}" cy="{y+14}" rx="7" ry="2.6" stroke-width="1.1"/>'
                                f'<path d="M{x+dx} {y+11} v-7" stroke-width="0.9"/>'
                                f'<path d="M{x+dx-7} {y+14} v3 a7 2.6 0 0 0 14 0 v-3" stroke-width="0.9"/>'
                                for dx in (-42, -14, 14, 42))),
        # 2 下层三格
        lambda x, y: (f'<path d="M{x-46} {y-26} h92 v52 h-92 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-46} {y-8} h92 M{x-46} {y+8} h92" stroke-width="1"/>'
                      f'<circle cx="{x-24}" cy="{y-17}" r="6" stroke-width="0.9"/>'
                      f'<path d="M{x+14} {y-22} h24 v8 h-24 Z" stroke-width="0.7"/>'
                      f'<path d="M{x-12} {y-2} h24" stroke-width="1.2"/>'
                      f'<path d="M{x-46} {y+12} h104 v10 h-104 Z" stroke-width="1.3"/>'
                      f'<path d="M{x-44} {y+18} h100 v3 h-100 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x+58} {y+14} v6" stroke-width="1.4"/>'
                      f'<path d="M{x+64} {y+17} h14 l-4 -3 M{x+78} {y+17} l-4 3" stroke-width="0.8"/>'),
        # 3 3030 立柱 + 横梁
        lambda x, y: (profile(x - 46, y - 34, 10, 68, 10, pfx)
                      + profile(x + 36, y - 34, 10, 68, 10, pfx)
                      + profile(x - 46, y - 44, 92, 10, 10, pfx)),
        # 4 木台面板
        lambda x, y: (f'<path d="M{x-46} {y-4} h92 v9 h-92 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-46} {y-4} l12 -8 h92 l-12 8 M{x+46} {y-4} l12 -8 v9 l-12 8" stroke-width="1"/>'
                      f'<path d="M{x-38} {y-9} q24 -3 48 0 M{x-26} {y-6} q20 -2 40 0 M{x-34} {y+2} h76" stroke-width="0.4"/>'
                      f'<path d="M{x+47} {y-3} l10 -7 v7 l-10 7 Z" fill="{S}" stroke="none"/>'),
        # 5 可翻侧板（铰链 + 磁扣）
        lambda x, y: (f'<path d="M{x-34} {y-26} h58 v52 h-58 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-30} {y-22} h50 v44 h-50 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x-34} {y-18} h-8 v6 h8 M{x-34} {y+12} h-8 v6 h8" stroke-width="1.1"/>'
                      f'<circle cx="{x-38}" cy="{y-15}" r="1.6" stroke-width="0.6"/><circle cx="{x-38}" cy="{y+15}" r="1.6" stroke-width="0.6"/>'
                      f'<path d="M{x+24} {y-4} h8 v8 h-8 Z" stroke-width="1"/>'
                      f'<path d="M{x-46} {y-30} a26 26 0 0 1 10 -10 M{x-46} {y-30} l1 -6 M{x-46} {y-30} l6 1" stroke-width="0.8"/>'),
    ]
    legend = [(1, "可调脚垫 ×4 + 2020 底框，占地约 0.5×0.5m"),
              (2, "下层三格：耗材干燥箱 / 工具抽屉 / 可整块抽出的接屑盘"),
              (3, "3030 喷砂黑立柱 ×4 + 横梁（0805 欧标规格）"),
              (4, "木台面板：台面与滑轨摩擦面覆木，挡住型材划伤露白"),
              (5, "可翻侧板：铰链 + 磁扣，清碎屑时整块翻开")]
    svg = ex(pfx, "铝型材工作站与人体工学高度", "0305-2", 123, legend,
             "改掉参考方案两个坑：侧板不好清屑 · 高度不合人体工学",
             items, [(-56, -8), (-50, -30), (-52, -40), (-50, -10), (-38, -30)])
    # 右下角：站姿平视高度示意（腔口中心 1100~1200 尺寸线）
    ins = ['<g stroke="#3d3d3d" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.92">',
           '<path d="M296 320 H460" stroke-width="1.2"/>',
           '<path d="M312 320 V205 M348 320 V205 M312 205 H348" stroke-width="1.3"/>',
           '<path d="M316 254 H344 V210 H316 Z" stroke-width="1.1"/>',
           '<path d="M316 262 H344 M316 286 H344 M316 310 H344" stroke-width="0.7"/>',
           '<circle cx="412" cy="212" r="8" stroke-width="1.3"/>',
           '<path d="M412 220 V270 M400 232 H424 M402 270 H422" stroke-width="1.3"/>',
           '<path d="M401 233 L396 256 L403 268 M423 233 L428 258 L420 268" stroke-width="1.1"/>',
           '<path d="M404 270 L400 320 M420 270 L424 320 M400 320 H392 M424 320 H432" stroke-width="1.3"/>',
           '<path d="M402 210 L354 228" stroke-width="0.7" stroke-dasharray="4 3"/>',
           '<path d="M352 232 H372" stroke-width="0.6" stroke-dasharray="3 3"/>',
           '<path d="M368 232 V320 M368 232 l-3 7 M368 232 l3 7 M368 320 l-3 -7 M368 320 l3 -7" stroke-width="0.9"/>',
           '</g>',
           f'<text x="368" y="186" text-anchor="middle" font-size="9" fill="#2a2a2a" font-family="{FONT}">腔口中心 1100～1200</text>',
           f'<path d="M368 190 L366 228" stroke="#3d3d3d" stroke-width="0.7" stroke-dasharray="3 3" fill="none"/>',
           f'<text x="412" y="336" text-anchor="middle" font-size="8.5" fill="#666" font-family="{FONT}">站姿平视，不用蹲下去</text>',
           f'<text x="330" y="336" text-anchor="middle" font-size="8.5" fill="#666" font-family="{FONT}">0.5×0.5m</text>']
    return svg.replace("</svg>", "\n".join(ins) + "\n</svg>")


def p0305_3():
    """腔体排风与耗材干燥 · 爆炸图"""
    pfx = "p0305-3"
    S = SH(pfx)
    items = [
        # 1 加热耗材干燥箱
        lambda x, y: (f'<path d="M{x-42} {y-18} h84 v34 h-84 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-42} {y-18} l10 -7 h84 l-10 7 M{x+42} {y-18} l10 -7 v34 l-10 7" stroke-width="0.9"/>'
                      f'<circle cx="{x-18}" cy="{y-1}" r="11" stroke-width="1.1"/><circle cx="{x-18}" cy="{y-1}" r="4" stroke-width="0.7"/>'
                      f'<path d="M{x-18} {y-1} m-11 0 a11 11 0 0 0 22 0 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x+8} {y-12} h22 v10 h-22 Z M{x+11} {y-6} h12 M{x+11} {y+4} h18 M{x+11} {y+9} h12" stroke-width="0.7"/>'
                      f'<path d="M{x+2} {y-18} q6 -12 18 -16" stroke-width="0.9"/>'),
        # 2 腔体顶部 100mm 排风法兰
        lambda x, y: (f'<path d="M{x-40} {y+4} h80 v8 h-80 Z" stroke-width="1.3"/>'
                      f'<path d="M{x-40} {y+4} l10 -7 h80 l-10 7" stroke-width="0.9"/>'
                      f'<ellipse cx="{x}" cy="{y-4}" rx="20" ry="7" stroke-width="1.3"/>'
                      f'<path d="M{x-20} {y-4} v8 a20 7 0 0 0 40 0 v-8" stroke-width="1"/>'
                      f'<ellipse cx="{x}" cy="{y-4}" rx="13" ry="4.5" stroke-width="0.7"/>'
                      f'<path d="M{x-26} {y+2} h4 M{x+22} {y+2} h4" stroke-width="0.8"/>'),
        # 3 活性炭滤棉
        lambda x, y: (f'<ellipse cx="{x}" cy="{y}" rx="20" ry="7" stroke-width="1.3"/>'
                      f'<path d="M{x-20} {y} v6 a20 7 0 0 0 40 0 v-6" stroke-width="1"/>'
                      f'<path d="M{x-18} {y+4} a18 6 0 0 0 36 0 v2 a18 6 0 0 1 -36 0 Z" fill="{S}" stroke="none"/>'
                      + "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="1.6" stroke-width="0.5"/>'
                                for dx, dy in ((-11, -1), (-4, 2), (3, -2), (10, 1), (-8, 3), (7, 3)))),
        # 4 12V 静音管道风扇
        lambda x, y: (f'<ellipse cx="{x}" cy="{y-6}" rx="20" ry="7" stroke-width="1.3"/>'
                      f'<path d="M{x-20} {y-6} v14 a20 7 0 0 0 40 0 v-14" stroke-width="1.2"/>'
                      f'<circle cx="{x}" cy="{y-6}" r="4" stroke-width="0.8"/>'
                      + "".join(f'<path d="M{x} {y-6} q{a} {b} {a*1.6:.0f} {b*0.7:.0f}" stroke-width="0.7"/>'
                                for a, b in ((10, -3), (2, 5), (-10, -3), (-4, -5), (8, 4), (-8, 4)))
                      + f'<path d="M{x+20} {y+2} h12 M{x+26} {y-2} v8" stroke-width="0.8"/>'),
        # 5 铝箔软管 1.5m
        lambda x, y: (f'<path d="M{x-52} {y+6} q14 -14 30 -6 q16 8 30 -6 q14 -14 28 -4" stroke-width="1.4"/>'
                      f'<path d="M{x-52} {y-8} q14 -14 30 -6 q16 8 30 -6 q14 -14 28 -4" stroke-width="1.4"/>'
                      + "".join(f'<path d="M{x-52+i*11} {y+6-i*1.0:.1f} v-14" stroke-width="0.5"/>' for i in range(1, 9))
                      + f'<path d="M{x-52} {y+6} v-14 M{x+36} {y+2} v-14" stroke-width="1"/>'),
        # 6 天窗边排气口百叶
        lambda x, y: (f'<path d="M{x-34} {y-16} h68 v34 h-68 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-34} {y-16} l10 -7 h68 l-10 7 M{x+34} {y-16} l10 -7 v34 l-10 7" stroke-width="0.9"/>'
                      + "".join(f'<path d="M{x-28} {y-10+i*8} h56 l-4 4 h-56 Z" stroke-width="0.8"/>' for i in range(4))
                      + f'<path d="M{x-40} {y+2} l-12 0 l4 -4 M{x-52} {y+2} l4 4" stroke-width="0.9"/>'),
    ]
    legend = [(1, "下层加热耗材干燥箱：边烘边打，目标 &lt;15% RH"),
              (2, "腔体顶部 100mm 排风法兰"),
              (3, "活性炭滤棉（3 个月一换）"),
              (4, "12V 静音管道风扇：开打即开，结束延时 10 分钟"),
              (5, "铝箔软管 ≈1.5m，横过天花到天窗边"),
              (6, "天窗边排气口百叶 + 防虫网")]
    return ex(pfx, "腔体排风与耗材干燥", "0305-3", 125, legend,
              "排风没装好之前一律不打 ABS，只打 PLA",
              items, [(-46, -12), (-46, -10), (-24, -8), (-24, -14), (-56, -14), (-40, -22)])


def p0305_4():
    nodes = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44), ("step", 30, 130, 110, 40),
             ("dia", 172, 128, 116, 48), ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40), ("pill", 155, 312, 170, 30)]
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
             ("M85 170 V228", False), ("M140 250 H173", False), ("M230 270 V310", False),
             ("M330 250 H287", False), ("M30 250 Q10 250 10 150 Q10 130 28 130", True)]
    texts = [(85, 69, "Mainsail 发任务", False), (85, 83, "或切片软件直发", False),
             (230, 74, "配置文件", False), (230, 87, "printer.cfg", True),
             (85, 147, "Moonraker 收任务", False), (85, 161, "排进打印队列", False),
             (230, 149, "klippy 在线？", False), (230, 162, "跑在 M1 Mac", True),
             (390, 147, "是 → klippy 规划", False), (390, 161, "主板按时间戳出脉冲", False),
             (85, 247, "否 → 重启 klippy", False), (85, 261, "查 USB / CAN 串口", False),
             (230, 247, "先跑共振测量", False), (230, 261, "输入整形 + 压力提前", False),
             (390, 247, "温度曲线 / 层数", False), (390, 261, "摄像头盯首层", False),
             (240, 331, "开始 / 结束 / 失败 → HA 推送", False),
             (305, 146, "是", True), (216, 200, "打印中", True), (70, 200, "否", True)]
    return flow("p0305-4", "Klipper 上位机与打印监看", nodes, edges, texts, "0305-4", 127)


def p0305_5():
    nodes = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44), ("step", 30, 130, 110, 40),
             ("dia", 172, 128, 116, 48), ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40), ("pill", 155, 312, 170, 30)]
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
             ("M85 170 V228", False), ("M140 250 H173", False), ("M230 270 V310", False),
             ("M330 250 H287", False), ("M30 250 Q10 250 10 150 Q10 130 28 130", True)]
    texts = [(85, 69, "新卷登记 Spoolman", False), (85, 83, "厂商 / 材质 / 克数", False),
             (230, 74, "耗材库存", False), (230, 87, "每卷剩余克数", True),
             (85, 147, "打印结束", False), (85, 161, "Moonraker 回写用量", False),
             (230, 149, "剩余 &lt;150g？", False), (230, 162, "或库存 >8 卷", True),
             (390, 147, "是 → 提醒补货", False), (390, 161, "库存超 8 卷提示停买", False),
             (85, 247, "否 → 继续自动扣减", False), (85, 261, "标签剩余克数更新", False),
             (230, 247, "换料 / 拆件之后", False), (230, 261, "抽出接屑盘端走倒掉", False),
             (390, 247, "每月称重校准一次", False), (390, 261, "误差大就重设初值", False),
             (240, 331, "Spoolman 看板 + 二维码标签", False),
             (305, 146, "是", True), (216, 200, "够用", True), (70, 200, "否", True)]
    return flow("p0305-5", "耗材账本与接屑清理", nodes, edges, texts, "0305-5", 129)


def p0305_4p():
    pfx = "p0305-4p"
    main = "\n".join([
        # M1 Mac mini
        '<path d="M44 152 h56 v24 h-56 Z" stroke-width="1.5"/><path d="M47 155 h50 v18 h-50 Z" stroke-width="0.6"/>',
        '<circle cx="90" cy="170" r="2" stroke-width="0.8"/><path d="M52 164 h18" stroke-width="0.7"/>',
        '<path d="M108 164 H142" stroke-width="1" stroke-dasharray="3 3"/><path d="M138 160 l4 4 l-4 4" stroke-width="1"/>',
        # Mainsail 网页
        '<path d="M150 130 h74 v68 h-74 Z" stroke-width="1.5"/><path d="M150 142 h74" stroke-width="0.9"/>',
        '<circle cx="156" cy="136" r="2" stroke-width="0.6"/><circle cx="163" cy="136" r="2" stroke-width="0.6"/>',
        '<path d="M156 178 l12 -14 l10 9 l14 -20 l12 16" stroke-width="1"/>',
        '<path d="M156 150 h26 v10 h-26 Z" fill="url(#p0305-4p-shade)" stroke="none"/>',
        '<path d="M188 150 h30 M188 156 h22 M156 188 h62" stroke-width="0.6"/>',
        '<path d="M232 164 H266" stroke-width="1" stroke-dasharray="3 3"/><path d="M262 160 l4 4 l-4 4" stroke-width="1"/>',
        # 封闭腔打印机 + 摄像头
        '<path d="M272 128 h50 v70 h-50 Z" stroke-width="1.6"/><path d="M280 140 h34 v44 h-34 Z" stroke-width="1"/>',
        '<path d="M288 176 h18 M292 172 l6 -10 l6 10" stroke-width="0.9"/>',
        '<path d="M286 146 h22 M295 146 v8 h6 v-8" stroke-width="0.7"/>',
        '<circle cx="297" cy="120" r="4" stroke-width="1"/><path d="M297 124 v4" stroke-width="0.9"/>',
        '<path d="M322 132 l10 -6 v10 Z" stroke-width="0.9"/>',
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>',
    ])
    return poster(pfx, "0305 · L4", "上位机大脑", "主板只管出脉冲，动脑的活交给那台 Mac", main,
                  "网页发任务 → Moonraker → klippy 规划 → 主板出脉冲 → 推送",
                  ["参数全在 printer.cfg，改完重启就生效，不用重编固件",
                   "装完先跑共振测量出输入整形，再调压力提前",
                   "开始 / 结束 / 失败经 Moonraker 推 HomeAssistant"],
                  "跑在：0804 常驻 M1 Mac · 数据出口：HA 推送 + 摄像头",
                  "Klipper3d/klipper · mainsail-crew/mainsail", 131)


def p0305_5p():
    pfx = "p0305-5p"
    main = "\n".join([
        # 料卷 + 秤
        '<circle cx="76" cy="152" r="24" stroke-width="1.5"/><circle cx="76" cy="152" r="8" stroke-width="1"/>',
        '<path d="M76 152 m-24 0 a24 24 0 0 0 48 0 Z" fill="url(#p0305-5p-shade)" stroke="none"/>',
        '<path d="M46 180 h60 v12 h-60 Z" stroke-width="1.3"/><path d="M58 186 h20" stroke-width="0.7"/>',
        '<path d="M88 184 h14 v6 h-14 Z" stroke-width="0.7"/>',
        '<path d="M112 168 H148" stroke-width="1" stroke-dasharray="3 3"/><path d="M144 164 l4 4 l-4 4" stroke-width="1"/>',
        # 账本 / 网页看板
        '<path d="M156 128 h64 v72 h-64 Z" stroke-width="1.5"/><path d="M156 140 h64" stroke-width="0.8"/>',
        '<path d="M164 152 h20 v8 h-20 Z" fill="url(#p0305-5p-shade)" stroke="none"/>',
        '<path d="M190 154 h22 M164 168 h48 M164 178 h34 M164 188 h42" stroke-width="0.6"/>',
        '<path d="M164 152 h20 v8 h-20 Z" stroke-width="0.7"/>',
        '<path d="M228 168 H262" stroke-width="1" stroke-dasharray="3 3"/><path d="M258 164 l4 4 l-4 4" stroke-width="1"/>',
        # 接屑盘抽出 + 桶
        '<path d="M268 150 h56 v10 h-56 Z" stroke-width="1.5"/><path d="M271 152 h50 v6 h-50 Z" fill="url(#p0305-5p-shade)" stroke="none"/>',
        '<path d="M264 151 v8" stroke-width="1.5"/>',
        '<path d="M282 164 l3 6 M296 166 l3 6 M310 163 l3 6" stroke-width="0.7"/>',
        '<path d="M282 182 L286 214 h22 l4 -32 Z" stroke-width="1.3"/><path d="M279 182 H315" stroke-width="1.2"/>',
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>',
    ])
    return poster(pfx, "0305 · L5", "耗材账本", "剩多少克不靠手写，盘子一抽碎屑就没了", main,
                  "登记初始重量 → 打完回写克数 → 低于 150g 提醒补货",
                  ["每卷一个二维码，扫一下就知道还剩多少克",
                   "剩余 &lt;150g 提醒补货，库存 >8 卷提示先用完",
                   "换料或拆件之后抽出接屑盘，端走倒掉"],
                  "跑在：0804 M1 Mac 上的 Spoolman · 数据出口：网页看板 + 标签",
                  "Donkie/Spoolman · Klipper3d/klipper", 133)


# =============================== parts · 0307 ===============================
def p0307_1():
    """龙门机架与两条刚性路线 · 爆炸图"""
    pfx = "p0307-1"
    S = SH(pfx)
    items = [
        # 1 底座框（两条路线并排：细截面 / 粗截面）
        lambda x, y: (profile(x - 66, y - 8, 46, 10, 10, pfx)
                      + profile(x - 66, y - 30, 10, 22, 10, pfx)
                      + profile(x - 30, y - 30, 10, 22, 10, pfx)
                      + profile(x + 8, y - 12, 56, 16, 14, pfx)
                      + profile(x + 8, y - 40, 16, 28, 14, pfx)
                      + profile(x + 48, y - 40, 16, 28, 14, pfx)
                      + f'<path d="M{x-10} {y-18} v-6 M{x-10} {y-30} a3 3 0 1 1 3 3 l-3 3" stroke-width="1"/>'),
        # 2 立柱 + 横梁（龙门）
        lambda x, y: (profile(x - 42, y - 30, 10, 60, 10, pfx)
                      + profile(x + 32, y - 30, 10, 60, 10, pfx)
                      + profile(x - 42, y - 42, 84, 12, 10, pfx)
                      + f'<path d="M{x-34} {y-30} h8 v-8 M{x+32} {y-30} h-8 v-8" stroke-width="0.8"/>'),
        # 3 HGR15 导轨 + 滑块
        lambda x, y: (f'<path d="M{x-48} {y} h96 v7 h-96 Z M{x-48} {y-24} h96 v7 h-96 Z" stroke-width="1.2"/>'
                      f'<path d="M{x-46} {y+3} h92 v3 h-92 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x-28} {y-20} h22 v20 h-22 Z M{x+8} {y-20} h22 v20 h-22 Z" stroke-width="1.1"/>'
                      f'<path d="M{x-24} {y-16} h14 M{x+12} {y-16} h14" stroke-width="0.5"/>'),
        # 4 1605 滚珠丝杠 + 闭环步进
        lambda x, y: (f'<circle cx="{x-34}" cy="{y}" r="8" stroke-width="1.2"/>'
                      f'<path d="M{x-26} {y-3} h56 M{x-26} {y+3} h56" stroke-width="1"/>'
                      + "".join(f'<path d="M{x-24+i*7} {y-3} l4 6" stroke-width="0.5"/>' for i in range(8))
                      + f'<path d="M{x-14} {y-9} h16 v18 h-16 Z" stroke-width="1.1"/>'
                      f'<path d="M{x+30} {y-11} h18 v22 h-18 Z" stroke-width="1.2"/>'
                      f'<path d="M{x+31} {y-10} h16 v20 h-16 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x+39} {y-11} v-7 M{x+34} {y-18} h10 v-5 h-10 Z" stroke-width="1"/>'),
        # 5 铝 T 槽板台面
        lambda x, y: (f'<path d="M{x-46} {y-7} h92 v14 h-92 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-46} {y-7} l12 -8 h92 l-12 8 M{x+46} {y-7} l12 -8 v14 l-12 8" stroke-width="1"/>'
                      f'<path d="M{x+47} {y-6} l10 -7 v12 l-10 7 Z" fill="{S}" stroke="none"/>'
                      + "".join(f'<path d="M{x-34+i*23} {y-7} v14 M{x-37+i*23} {y-7} h6" stroke-width="0.6"/>' for i in range(4))),
    ]
    legend = [(1, "底座框：2020+3030（木 / 亚克力）或 4040 + 钢板（铝）"),
              (2, "龙门立柱 + 横梁，角码 + 内置角槽件双重锁定"),
              (3, "HGR15 直线导轨 ×2 + 滑块，压在型材面上"),
              (4, "1605 滚珠丝杠 + 42 闭环步进 ×3（丢步报警）"),
              (5, "铝 T 槽板台面 300×300（铝路线 200×200）")]
    svg = ex(pfx, "龙门机架与两条刚性路线", "0307-1", 135, legend,
             "行程 300×300×100（木 / 亚克力）或 200×200×80（铝）",
             items, [(-72, -34), (-48, -46), (-52, -28), (-40, -14), (-52, -12)])
    extra = [f'<text x="66" y="332" text-anchor="middle" font-size="8" fill="#444" font-family="{FONT}">木 / 亚克力路线</text>',
             f'<text x="150" y="332" text-anchor="middle" font-size="8" fill="#444" font-family="{FONT}">铝路线（加强）</text>',
             f'<text x="150" y="348" text-anchor="middle" font-size="7.5" fill="#888" font-style="italic" font-family="{FONT}">主材没拍板之前，截面和导轨都不定标 · 整机 ≤60kg（楼板承重待核）</text>']
    return svg.replace("</svg>", "\n".join(extra) + "\n</svg>")


def p0307_2():
    """主轴与变频选型（待定）· 爆炸图"""
    pfx = "p0307-2"
    S = SH(pfx)
    items = [
        # 1 主轴夹座 + Z 滑块安装板
        lambda x, y: (f'<path d="M{x-44} {y-8} h88 v16 h-88 Z" stroke-width="1.4"/>'
                      f'<path d="M{x-44} {y-8} l10 -7 h88 l-10 7 M{x+44} {y-8} l10 -7 v16 l-10 7" stroke-width="1"/>'
                      f'<path d="M{x-14} {y-8} a14 14 0 0 0 28 0" stroke-width="1.1"/>'
                      f'<path d="M{x-24} {y-8} a24 10 0 0 1 48 0" stroke-width="0.6" stroke-dasharray="3 2"/>'
                      f'<path d="M{x-36} {y-2} h6 M{x+30} {y-2} h6" stroke-width="0.8"/>'
                      f'<path d="M{x-42} {y+3} h84 v4 h-84 Z" fill="{S}" stroke="none"/>'),
        # 2 500W 风冷主轴 + ER11
        lambda x, y: (f'<path d="M{x-14} {y-30} h28 v52 h-28 Z" stroke-width="1.4"/>'
                      + "".join(f'<path d="M{x-14} {y-24+i*7} h28" stroke-width="0.5"/>' for i in range(6))
                      + f'<path d="M{x-8} {y-38} h16 v8 h-16 Z" stroke-width="1.1"/>'
                      f'<path d="M{x-6} {y-36} q6 -6 12 0" stroke-width="0.6"/>'
                      f'<path d="M{x-7} {y+22} h14 l-3 9 h-8 Z" stroke-width="1.2"/>'
                      f'<path d="M{x-1.5} {y+31} v9" stroke-width="1.2"/>'
                      f'<path d="M{x-20} {y-26} h-10 M{x-20} {y-16} h-10" stroke-width="0.6"/>'),
        # 3 1.5kW 水冷主轴 + 水管
        lambda x, y: (f'<path d="M{x-16} {y-34} h32 v60 h-32 Z" stroke-width="1.5"/>'
                      f'<path d="M{x+10} {y-32} h5 v56 h-5 Z" fill="{S}" stroke="none"/>'
                      + "".join(f'<path d="M{x-16} {y-26+i*10} h32" stroke-width="0.4"/>' for i in range(6))
                      + f'<path d="M{x-16} {y-28} q-14 -4 -22 -14 M{x-16} {y-18} q-16 -2 -26 -10" stroke-width="1"/>'
                      f'<path d="M{x-6} {y+26} h12 l-2 10 h-8 Z" stroke-width="1.2"/>'
                      f'<path d="M{x} {y+36} v10" stroke-width="1.2"/>'),
        # 4 水箱 + 水泵（仅水冷）
        lambda x, y: (f'<path d="M{x-34} {y-12} h60 v28 h-60 Z" stroke-width="1.3"/>'
                      f'<path d="M{x-32} {y+2} q14 -5 28 0 q14 5 28 0 v12 h-56 Z" fill="{S}" stroke="none"/>'
                      f'<path d="M{x-32} {y+2} q14 -5 28 0 q14 5 28 0" stroke-width="0.8"/>'
                      f'<path d="M{x+30} {y-4} h14 v14 h-14 Z" stroke-width="1.1"/><circle cx="{x+37}" cy="{y+3}" r="4" stroke-width="0.7"/>'
                      f'<path d="M{x+26} {y-12} q10 -10 18 -4" stroke-width="0.9"/>'),
        # 5 VFD 变频器
        lambda x, y: (f'<path d="M{x-30} {y-22} h60 v44 h-60 Z" stroke-width="1.5"/>'
                      f'<path d="M{x-24} {y-16} h32 v12 h-32 Z" stroke-width="0.9"/>'
                      f'<path d="M{x-20} {y-9} h10 M{x-6} {y-9} h12" stroke-width="0.6"/>'
                      f'<circle cx="{x+18}" cy="{y-10}" r="6" stroke-width="0.9"/><path d="M{x+18} {y-10} l4 -4" stroke-width="0.8"/>'
                      + "".join(f'<path d="M{x-24+i*11} {y+6} h7 v10 h-7 Z" stroke-width="0.6"/>' for i in range(5))
                      + f'<path d="M{x-30} {y+10} h-12 M{x-30} {y+16} h-12" stroke-width="0.8"/>'),
    ]
    legend = [(1, "主轴夹座 + Z 滑块安装板（Ø52 / Ø80 两种孔径）"),
              (2, "木 / 亚克力路线：500W 风冷主轴 · ER11 · 12000～24000rpm"),
              (3, "铝路线：1.5kW 水冷主轴 · 8000～18000rpm + 进回水管"),
              (4, "水箱 + 水泵（只有水冷路线才需要）"),
              (5, "VFD 变频器：RS485 / Modbus 由固件调速")]
    svg = ex(pfx, "主轴与变频选型（待定）", "0307-2", 137, legend,
             "主材未定之前只租借试切，不采购主轴与变频器",
             items, [(-50, -6), (-24, -36), (-26, -40), (-40, -16), (-36, -26)])
    extra = [f'<text x="108" y="344" text-anchor="middle" font-size="8" fill="#888" font-style="italic" font-family="{FONT}">2 和 3 二选一 · 选谁取决于主要切木头还是切铝</text>']
    return svg.replace("</svg>", "\n".join(extra) + "\n</svg>")


def p0307_3():
    nodes = [("pill", 30, 52, 110, 34), ("db", 186, 50, 88, 44), ("step", 30, 130, 110, 40),
             ("dia", 172, 128, 116, 48), ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40), ("pill", 155, 312, 170, 30)]
    edges = [("M85 86 V128", False), ("M186 72 Q158 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
             ("M85 170 V228", False), ("M140 250 H173", False), ("M230 270 V310", False),
             ("M330 250 H287", False), ("M30 250 Q10 250 10 150 Q10 130 28 130", True)]
    texts = [(85, 69, "cncjs 下发 G 代码", False), (85, 83, "机旁小主机 / 平板", False),
             (230, 74, "三轴固件", False), (230, 87, "grblHAL / FluidNC", True),
             (85, 147, "固件解析 G 代码", False), (85, 161, "前瞻加减速 → 脉冲", False),
             (230, 149, "安全信号正常？", False), (230, 162, "限位 门磁 探针", True),
             (390, 147, "是 → 按刀路走三轴", False), (390, 161, "M3 / M5 控主轴启停", False),
             (85, 247, "否 → 进给暂停", False), (85, 261, "抬刀并停主轴", False),
             (230, 247, "VFD 经 RS485 调速", False), (230, 261, "不用手动旋钮", False),
             (390, 247, "门开 / 丢步 / 过流", False), (390, 261, "任一触发即暂停", False),
             (240, 331, "安全逻辑走固件输入，不走网页", False),
             (305, 146, "是", True), (216, 200, "加工中", True), (70, 200, "否", True)]
    return flow("p0307-3", "三轴控制与限位安全", nodes, edges, texts, "0307-3", 139)


def p0307_4():
    nodes = [("pill", 30, 52, 110, 34), ("db", 196, 50, 68, 44), ("step", 30, 130, 110, 40),
             ("dia", 172, 128, 116, 48), ("step", 330, 130, 120, 40), ("step", 30, 230, 110, 40),
             ("step", 175, 230, 110, 40), ("step", 330, 230, 120, 40), ("pill", 155, 312, 170, 30)]
    edges = [("M85 86 V128", False), ("M196 72 Q160 72 140 72", True), ("M140 150 H170", False),
             ("M288 152 H328", False), ("M230 176 V228", False), ("M390 170 V228", False),
             ("M85 170 V228", False), ("M140 250 H173", False), ("M230 270 V310", False),
             ("M330 250 H287", False)]
    texts = [(85, 69, "主轴请求启动", False), (85, 83, "ESPHome 读继电器", False),
             (230, 74, "0304 储能", False), (230, 87, "SOC / 当前负载", True),
             (85, 147, "HA 查 SOC 与负载", False), (85, 161, "电摩是否在充电", False),
             (230, 149, "能给 2kW？", False), (230, 162, "按 SOC 决定", True),
             (390, 147, "是 → 先开 0404 集尘", False), (390, 161, "按材质开对应分路阀", False),
             (85, 247, "否 → 限功率模式", False), (85, 261, "或推送“等光伏”", False),
             (230, 247, "3 秒后才通主轴", False), (230, 261, "记 cnc_runtime", False),
             (390, 247, "主轴停 → 延时 30s", False), (390, 261, "关阀关集尘", False),
             (240, 331, "木屑与铝屑分路阀分桶，绝不混用", False),
             (305, 146, "是", True), (216, 200, "运行中", True), (70, 200, "否", True)]
    return flow("p0307-4", "功率与排屑联动", nodes, edges, texts, "0307-4", 141)


def p0307_3p():
    pfx = "p0307-3p"
    main = "\n".join([
        # 平板 / 小主机 发送端
        '<path d="M40 138 h46 v62 h-46 Z" stroke-width="1.5"/><path d="M44 142 h38 v50 h-38 Z" stroke-width="0.7"/>',
        '<path d="M50 152 h26 M50 160 h20 M50 168 h26 M50 176 h16" stroke-width="0.6"/>',
        '<circle cx="63" cy="196" r="1.8" stroke-width="0.7"/>',
        '<path d="M94 168 H128" stroke-width="1" stroke-dasharray="3 3"/><path d="M124 164 l4 4 l-4 4" stroke-width="1"/>',
        # 控制板 + 三路安全信号
        '<path d="M136 136 h66 v64 h-66 Z" stroke-width="1.5"/>',
        '<path d="M144 146 h26 v18 h-26 Z" fill="url(#p0307-3p-shade)" stroke="none"/>',
        '<path d="M144 146 h26 v18 h-26 Z" stroke-width="0.9"/>',
        '<path d="M178 148 h16 M178 154 h16 M178 160 h10" stroke-width="0.5"/>',
        '<path d="M144 174 h8 v8 h-8 Z M158 174 h8 v8 h-8 Z M172 174 h8 v8 h-8 Z" stroke-width="0.8"/>',
        '<path d="M148 190 v10 M162 190 v10 M176 190 v10" stroke-width="0.9"/>',
        '<path d="M136 156 h-10 M136 166 h-10" stroke-width="0.8"/>',
        '<path d="M210 168 H244" stroke-width="1" stroke-dasharray="3 3"/><path d="M240 164 l4 4 l-4 4" stroke-width="1"/>',
        # 三轴龙门机
        '<path d="M252 194 h72 v10 h-72 Z" stroke-width="1.4"/>',
        '<path d="M260 194 V146 h8 v48 M308 194 V146 h8 v48 M260 146 h56 v-10 h-56 Z" stroke-width="1.3"/>',
        '<path d="M280 136 h16 v20 h-16 Z M284 156 h8 v16 h-8 Z M288 172 v8" stroke-width="1.1"/>',
        '<path d="M266 194 h44 v-8 h-44 Z" stroke-width="0.9"/>',
        '<path d="M262 128 h52 M262 128 l5 -3 M262 128 l5 3 M314 128 l-5 -3 M314 128 l-5 3" stroke-width="0.8"/>',
        '<path d="M304 152 v28 M304 152 l-3 5 M304 152 l3 5 M304 180 l-3 -5 M304 180 l3 -5" stroke-width="0.8"/>',
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>',
    ])
    return poster(pfx, "0307 · L3", "三轴安全闸", "门一开就停：安全不交给网页", main,
                  "cncjs 下发 → 固件解析 → 限位 / 门磁 / 探针三路直连 → 异常即停",
                  ["限位定行程，门磁做安全门输入，探针测刀长与 Z 零",
                   "VFD 主轴走 RS485 / Modbus，由固件调速与启停",
                   "门开 / 丢步 / 过流任一触发即进给暂停并抬刀"],
                  "跑在：grblHAL（Teensy 4.1）或 FluidNC（ESP32）· 数据出口：cncjs 日志",
                  "grblHAL/core · bdring/FluidNC", 143)


def p0307_4p():
    pfx = "p0307-4p"
    main = "\n".join([
        # 储能电池
        '<path d="M44 140 h52 v44 h-52 Z" stroke-width="1.4"/><path d="M56 132 h28 v8 h-28 Z" stroke-width="1"/>',
        '<path d="M52 150 h36 M52 160 h36 M52 170 h22" stroke-width="0.8"/>',
        '<path d="M104 162 H138" stroke-width="1" stroke-dasharray="3 3"/><path d="M134 158 l4 4 l-4 4" stroke-width="1"/>',
        # 三轴龙门机（小）
        '<path d="M146 186 h66 v10 h-66 Z" stroke-width="1.4"/>',
        '<path d="M154 186 V146 h8 v40 M196 186 V146 h8 v40 M154 146 h50 v-10 h-50 Z" stroke-width="1.3"/>',
        '<path d="M170 136 h14 v18 h-14 Z M174 154 h6 v14 h-6 Z M177 168 v6" stroke-width="1.1"/>',
        '<path d="M160 186 h40 v-8 h-40 Z" stroke-width="0.9"/>',
        '<path d="M186 176 l6 6 M194 172 l6 6" stroke-width="0.6"/>',
        '<path d="M220 162 H254" stroke-width="1" stroke-dasharray="3 3"/><path d="M250 158 l4 4 l-4 4" stroke-width="1"/>',
        # 分路阀 + 两只集尘桶
        '<circle cx="272" cy="150" r="10" stroke-width="1.3"/><path d="M272 140 v20 M262 150 h20" stroke-width="0.7"/>',
        '<path d="M264 158 L258 176 M280 158 L296 176" stroke-width="1.1"/>',
        '<path d="M248 178 L252 208 h18 l4 -30 Z" stroke-width="1.3"/><path d="M245 178 H278" stroke-width="1.1"/>',
        '<path d="M288 178 L292 208 h18 l4 -30 Z" stroke-width="1.3"/><path d="M285 178 H318" stroke-width="1.1"/>',
        '<path d="M254 192 h14 M256 198 h10" stroke-width="0.5"/>',
        '<path d="M294 192 l4 4 M302 190 l4 4 M298 200 l4 4" stroke-width="0.5"/>',
        '<path d="M40 270 Q180 262 320 270" stroke-width="1.2"/>',
    ])
    return poster(pfx, "0307 · L4", "开机前先问电", "电够不够、屑往哪去，机器自己不管", main,
                  "主轴请求 → 查 0304 的 SOC → 先开集尘分路阀 → 3 秒后通主轴",
                  ["电池低或电摩在充电，就只给低功率模式",
                   "集尘和阁楼分路阀先开，主轴停后延时 30 秒再关",
                   "木屑与铝屑分路阀和集尘桶分开，绝不混用"],
                  "跑在：ESPHome + HomeAssistant · 数据出口：cnc_power_mode 实体",
                  "home-assistant/core", 145)


OUT = {
    "illos/0305.svg": m0305,
    "illos/0307.svg": m0307,
    "parts/0305-1.svg": p0305_1,
    "parts/0305-2.svg": p0305_2,
    "parts/0305-3.svg": p0305_3,
    "parts/0305-4.svg": p0305_4,
    "parts/0305-5.svg": p0305_5,
    "parts/0305-4-poster.svg": p0305_4p,
    "parts/0305-5-poster.svg": p0305_5p,
    "parts/0307-1.svg": p0307_1,
    "parts/0307-2.svg": p0307_2,
    "parts/0307-3.svg": p0307_3,
    "parts/0307-4.svg": p0307_4,
    "parts/0307-3-poster.svg": p0307_3p,
    "parts/0307-4-poster.svg": p0307_4p,
}

if __name__ == "__main__":
    for path, fn in OUT.items():
        open(path, "w", encoding="utf-8").write(fn())
    print("ok", len(OUT))
