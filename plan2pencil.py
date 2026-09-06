#!/usr/bin/env python3
"""把 0008 户型图的 5 张彩色 SVG 转成畅想版铅笔画风格（几何完全照抄 0008）。
用法：python3 plan2pencil.py  → illos/plan-*.svg
"""
import re, pathlib

SRC = pathlib.Path('ref0008')
DST = pathlib.Path('illos')
FONT = "'Noto Sans SC','PingFang SC','Noto Sans CJK SC',sans-serif"
HAND = "'Long Cang','Kaiti SC',cursive"

PLANS = [
    ('site',         '场地总图 · 上北下南',                 '0008-1'),
    ('floor1',       '一层平面 · 东南角一户',               '0008-2'),
    ('attic',        '阁楼层 · 分区与可站立核心区',         '0008-3'),
    ('bunker-cabin', '地堡与木屋 · 家具平面',               '0008-4'),
    ('northwall',    '木屋北墙立面 · 自室内向北看',         '0008-5'),
]

# 区域 → 排线密度（铅笔画只用灰度，用疏密区分区域）
ZONE_HATCH = {
    'f01': ('h01', 7, 38),   # 木屋 疏斜线
    'f02': ('h02', 5, 38),   # 地堡 中斜线
    'f03': ('h03', 6, 128),  # 阁楼间 反向
    'f04': ('h04', 8, 128),  # 阁楼仓库 反向疏
    'f05': ('h05', 9, 38),   # 庭院 很疏
    'f06': ('h06', 10, 38),  # 草地 极疏
    'f07': ('h07', 4, 128),  # 钓台 密反向
    'fw':  ('hw', 3, 38),    # 警示 密
    'fn':  ('hn', 4, 0),     # 他人产权 交叉
}

def defs(pfx):
    out = [f'''<filter id="{pfx}-pencil" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>''']
    for cls, (pid, step, ang) in ZONE_HATCH.items():
        if cls == 'fn':
            out.append(f'''<pattern id="{pfx}-{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="{step}" y2="{step}" stroke="#8a8a8a" stroke-width="0.5" stroke-opacity="0.7"/>
      <line x1="{step}" y1="0" x2="0" y2="{step}" stroke="#8a8a8a" stroke-width="0.5" stroke-opacity="0.7"/>
    </pattern>''')
        else:
            w = 0.9 if cls == 'fw' else 0.65
            out.append(f'''<pattern id="{pfx}-{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse" patternTransform="rotate({ang})">
      <line x1="0" y1="0" x2="0" y2="{step}" stroke="#6b6b6b" stroke-width="{w}" stroke-opacity="0.75"/>
    </pattern>''')
    out.append(f'''<marker id="{pfx}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M1 1 L9 5 L1 9" fill="none" stroke="#3d3d3d" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
    </marker>''')
    return '\n    '.join(out)

SHAPE_STYLE = {
    'wl': 'fill="none" stroke="#3d3d3d" stroke-width="1.7" stroke-opacity="0.95"',
    'wm': 'fill="none" stroke="#3d3d3d" stroke-width="1.15" stroke-opacity="0.92"',
    'wt': 'fill="none" stroke="#3d3d3d" stroke-width="0.6" stroke-opacity="0.85"',
    'eave': 'fill="none" stroke="#7a7a7a" stroke-width="0.6" stroke-dasharray="4 3"',
    'dsh': 'fill="none" stroke="#3d3d3d" stroke-width="1.3" stroke-dasharray="6 3" stroke-opacity="0.9"',
    'fx': 'fill="#f9f6ef" stroke="#3d3d3d" stroke-width="0.85" stroke-opacity="0.9"',
    'lead': 'fill="none" stroke="#3d3d3d" stroke-width="0.6" stroke-dasharray="2 2"',
}
TEXT_STYLE = {
    'b': 'font-size="12.5" font-weight="700" fill="#2a2a2a"',
    's': 'font-size="10" fill="#555"',
    'g': 'font-size="10.5" font-style="italic" fill="#8a8a8a"',
    'tn': 'font-size="11" fill="#555"',
    'tw': 'font-size="11" fill="#2a2a2a" font-weight="700"',
}
for k in ('t01','t02','t03','t04','t05','t06','t07'):
    TEXT_STYLE[k] = 'font-size="11" fill="#2a2a2a"'

def convert(name, title, sig):
    pfx = f'pl-{name}'
    s = (SRC / f'{name}.svg').read_text(encoding='utf-8')
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
    W, H = int(vb.group(1)), int(vb.group(2))
    TOP = 30
    body = re.sub(r'^<svg[^>]*>', '', s.strip()); body = re.sub(r'</svg>$', '', body)
    body = re.sub(r'<defs>.*?</defs>', '', body, flags=re.S)
    # 原图硬编码颜色 → 铅笔灰
    body = body.replace('#6B5646', '#3d3d3d').replace('#3E2B21', '#3d3d3d')
    body = body.replace('marker-end="url(#ar1)"', f'marker-end="url(#{pfx}-arrow)"')
    body = body.replace('marker-end="url(#ar2)"', f'marker-end="url(#{pfx}-arrow)"')
    body = body.replace('marker-end="url(#ar3)"', f'marker-end="url(#{pfx}-arrow)"')
    body = body.replace('fill="url(#lz)"', f'fill="url(#{pfx}-hn)" fill-opacity="0.6"')

    drawn, texts = [], []
    for m in re.finditer(r'<(rect|line|polygon|path|text)\b[^>]*?(?:/>|>.*?</text>)', body, re.S):
        el = m.group(0); tag = m.group(1)
        cm = re.search(r'class="([^"]+)"', el)
        cls = cm.group(1).split() if cm else []
        if tag == 'text':
            if 'b' in cls:
                style = TEXT_STYLE['b']
            else:
                hit = [c for c in cls if c in TEXT_STYLE]
                style = TEXT_STYLE[hit[0]] if hit else 'font-size="11" fill="#2a2a2a"'
            el = re.sub(r'\s*class="[^"]+"', '', el)
            el = el.replace('<text', f'<text {style}', 1)
            texts.append(el)
            continue
        el = re.sub(r'\s*class="[^"]+"', '', el)
        z = [c for c in cls if c in ZONE_HATCH]
        if z:
            pid = ZONE_HATCH[z[0]][0]
            drawn.append(el.replace(f'<{tag}', f'<{tag} fill="url(#{pfx}-{pid})" stroke="#3d3d3d" stroke-width="0.5" stroke-opacity="0.6"', 1))
        else:
            st = [c for c in cls if c in SHAPE_STYLE]
            if st:
                sty = SHAPE_STYLE[st[0]]
                for attr in re.findall(r'\b(stroke-width|fill|stroke)="', el):
                    sty = re.sub(rf'\s*{attr}="[^"]*"', '', sty)
                el = el.replace(f'<{tag}', f'<{tag} {sty}', 1)
            if 'lead' in cls or 'marker-end' in el:
                texts.append(el)   # 引线/箭头不加滤镜
            else:
                drawn.append(el)
    out = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H+TOP+14}" width="{W}" height="{H+TOP+14}" font-family="{FONT}">
  <defs>
    {defs(pfx)}
  </defs>
  <text x="14" y="20" font-weight="700" font-size="12" fill="#2a2a2a">{title}</text>
  <g transform="translate(0,{TOP})">
    <g filter="url(#{pfx}-pencil)" stroke-linecap="round" stroke-linejoin="round">
      {chr(10).join('      '+d for d in drawn)}
    </g>
    <g>
      {chr(10).join('      '+t for t in texts)}
    </g>
  </g>
  <text x="{W-12}" y="{H+TOP+8}" text-anchor="end" font-family="{HAND}" font-size="11" fill="#5a5a5a">{sig}</text>
</svg>
'''
    (DST / f'plan-{name}.svg').write_text(out, encoding='utf-8')
    print('wrote', f'illos/plan-{name}.svg', len(out))

if __name__ == '__main__':
    for n, t, s in PLANS:
        convert(n, t, s)
