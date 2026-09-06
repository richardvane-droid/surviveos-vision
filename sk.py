"""小工具：生成钢笔速写(illos) / 铅笔拆解(parts) SVG 的外壳与常用构件。"""
FONT = "'Noto Sans SC','PingFang SC','Noto Sans CJK SC',sans-serif"
HAND = "'Long Cang','Kaiti SC',cursive"

def illo(pfx, body, sig, extra_defs="", seed=7, w=400, h=300):
    """钢笔速写外壳：pfx 如 m0107 / marea-01；body 放在 rough 滤镜组内；sig 右下角签名。"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <filter id="{pfx}-rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="{seed}" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <pattern id="{pfx}-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#1c1c1c" stroke-width="0.8"/>
    </pattern>
    <pattern id="{pfx}-hatch2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="#1c1c1c" stroke-width="0.8"/>
      <line x1="0" y1="3" x2="6" y2="3" stroke="#1c1c1c" stroke-width="0.6"/>
    </pattern>
    <pattern id="{pfx}-hatchl" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="9" stroke="#1c1c1c" stroke-width="0.7"/>
    </pattern>
    {extra_defs}
  </defs>
  <g filter="url(#{pfx}-rough)" stroke="#1c1c1c" fill="none" stroke-linecap="round" stroke-linejoin="round">
{body}
  </g>
  <text x="{w-14}" y="{h-8}" text-anchor="end" font-family="{HAND}" font-size="10" fill="#1c1c1c">{sig}</text>
</svg>
'''

def label(x, y, t, size=9, anchor="start", fill="#5a5a5a"):
    return f'<text x="{x}" y="{y}" font-family="{HAND}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" filter="none">{t}</text>'

def figure(x, y, s=1.0, sw=1.2):
    """简笔小人，脚底在 (x,y)，高约 44*s。"""
    h = 44*s
    return (f'<circle cx="{x}" cy="{y-h+5*s}" r="{5*s}" stroke-width="{sw}"/>'
            f'<path d="M{x} {y-h+10*s} V{y-16*s} M{x} {y-h+18*s} L{x-9*s} {y-h+30*s} M{x} {y-h+18*s} L{x+9*s} {y-h+30*s} '
            f'M{x} {y-16*s} L{x-7*s} {y} M{x} {y-16*s} L{x+7*s} {y}" stroke-width="{sw}"/>')

def exploded(pfx, title, legend, body, sig, axis="M96 318 L392 40", seed=3, w=480, h=360, leaders=""):
    """铅笔爆炸图外壳：pfx 如 p0403-1；legend 是 [(n, 文本)]；leaders 放引线+编号圈（不加滤镜）。"""
    lg = "".join(f'<text x="16" y="{46+i*13}">{n} {t}</text>' for i, (n, t) in enumerate(legend))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">
  <defs>
    <filter id="{pfx}-pencil" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <pattern id="{pfx}-shade" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
      <line x1="0" y1="0" x2="0" y2="5" stroke="#6b6b6b" stroke-width="0.7" stroke-opacity="0.8"/>
    </pattern>
    <pattern id="{pfx}-shade2" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(38)">
      <line x1="0" y1="0" x2="0" y2="4" stroke="#4a4a4a" stroke-width="0.8"/>
      <line x1="0" y1="2" x2="4" y2="2" stroke="#4a4a4a" stroke-width="0.5" stroke-opacity="0.6"/>
    </pattern>
  </defs>
  <path d="{axis}" stroke="#8a8a8a" stroke-width="0.8" stroke-dasharray="4 4" fill="none"/>
  <g filter="url(#{pfx}-pencil)" stroke="#3d3d3d" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.92">
{body}
  </g>
  <g stroke="#3d3d3d" stroke-width="0.7" fill="none" stroke-dasharray="3 3">
{leaders}
  </g>
  <text x="16" y="30" font-weight="700" font-size="12" fill="#2a2a2a">{title} · 爆炸图</text>
  <g font-size="8.5" fill="#444">{lg}</g>
  <text x="{w-16}" y="{h-10}" text-anchor="end" font-family="{HAND}" font-size="11" fill="#5a5a5a">{sig}</text>
</svg>
'''

def num(x, y, n):
    """编号圈（放 leaders 组外，需要自己拼）"""
    return f'<g stroke="#3d3d3d" stroke-width="1" fill="#f9f6ef"><circle cx="{x}" cy="{y}" r="7"/></g><text x="{x}" y="{y+3}" text-anchor="middle" font-size="9" fill="#2a2a2a" font-family="{FONT}">{n}</text>'

def leader(x1, y1, x2, y2, n):
    """虚线引线 + 编号圈，返回 (leader_line, circle) 两段。"""
    return (f'<path d="M{x1} {y1} L{x2} {y2}"/>', num(x2, y2, n))

def box3(x, y, w, h, d, sw=1.4, kx=0.5, ky=0.32, shade=None):
    """斜投影盒子：前脸左上角 (x,y)，宽 w 高 h，进深 d 向右上。返回 path 字符串。shade 为 pattern url 时给右侧面上排线。"""
    dx, dy = d*kx, d*ky
    s = (f'<path d="M{x} {y} h{w} v{h} h{-w} Z" stroke-width="{sw}"/>'
         f'<path d="M{x} {y} l{dx} {-dy} h{w} l{-dx} {dy} M{x+w} {y} l{dx} {-dy} v{h} l{-dx} {dy}" stroke-width="{sw*0.8}"/>')
    if shade:
        s += f'<path d="M{x+w} {y} l{dx} {-dy} v{h} l{-dx} {dy} Z" fill="url({shade})" stroke="none"/>'
    return s
