"""GitHub 方案的铅笔风“项目介绍图 / 流程图”生成器。

输入（refs-0X.json 里每个 github 条目的 diagram 字段）：
{
  "title": "Home Assistant · 本地优先的家庭自动化中枢",
  "nodes": [ {"id":"s","label":"传感器 / ESPHome","kind":"sensor","col":0,"row":0},
             {"id":"ha","label":"Home Assistant\n自动化引擎","kind":"core","col":1,"row":0},
             {"id":"db","label":"历史数据库","kind":"db","col":1,"row":1},
             {"id":"ui","label":"仪表盘 / 手机","kind":"screen","col":2,"row":0} ],
  "edges": [ ["s","ha","MQTT / 原生"], ["ha","db"], ["ha","ui","推送"] ],
  "usage": "在本模块里：ESPHome 节点 → HA 自动化 → 0802 大屏"
}
kind: core(圆角矩形双线) / step(圆角矩形) / db(圆柱) / sensor(圆) / screen(显示器) / cloud(云) / device(方盒) / person(小人) / file(文档)
col 0..3（从左到右），row 0..2。最多 9 个节点。
"""
import re
FONT = "'Noto Sans SC','PingFang SC','Noto Sans CJK SC',sans-serif"
HAND = "'Long Cang','Kaiti SC',cursive"
W, H = 480, 300
COLS = {0: 78, 1: 200, 2: 322, 3: 430}
ROWS = {0: 96, 1: 176, 2: 250}
NW, NH = 104, 44

def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def _shape(kind, cx, cy, pfx):
    x, y = cx - NW/2, cy - NH/2
    if kind == "core":
        return (f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8" stroke-width="1.6"/>'
                f'<rect x="{x+3}" y="{y+3}" width="{NW-6}" height="{NH-6}" rx="6" stroke-width="0.6"/>'
                f'<path d="M{x+5} {y+NH+2} h{NW-6} v3 h-{NW-6} Z" fill="url(#{pfx}-shade)" stroke="none"/>')
    if kind == "step":
        return (f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" stroke-width="1.4"/>'
                f'<path d="M{x+4} {y+NH+2} h{NW-6} v3 h-{NW-6} Z" fill="url(#{pfx}-shade)" stroke="none"/>')
    if kind == "db":
        return (f'<path d="M{x+12} {y+6} a{NW/2-12} 6 0 0 1 {NW-24} 0 v{NH-12} a{NW/2-12} 6 0 0 1 -{NW-24} 0 Z" stroke-width="1.4"/>'
                f'<ellipse cx="{cx}" cy="{y+6}" rx="{NW/2-12}" ry="6" stroke-width="1.2"/>')
    if kind == "sensor":
        return (f'<circle cx="{cx}" cy="{cy}" r="{NH/2}" stroke-width="1.4"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{NH/2-5}" stroke-width="0.5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="3" stroke-width="1"/>'
                f'<path d="M{cx-6} {y-4} q6 -6 12 0 M{cx-10} {y-8} q10 -10 20 0" stroke-width="0.8"/>')
    if kind == "screen":
        return (f'<rect x="{x}" y="{y-2}" width="{NW}" height="{NH-2}" rx="3" stroke-width="1.4"/>'
                f'<path d="M{cx-14} {y+NH-4} h28 M{cx-8} {y+NH-4} v6 h16 v-6" stroke-width="1"/>'
                f'<path d="M{x+3} {y+1} h{NW-6} v4 h-{NW-6} Z" fill="url(#{pfx}-shade)" stroke="none"/>')
    if kind == "cloud":
        return (f'<path d="M{x+18} {cy+16} q-22 0 -18 -16 q2 -14 18 -12 q6 -16 26 -10 q14 -10 30 4 q20 -4 24 10 q14 4 10 16 q-4 10 -18 8 Z" stroke-width="1.4"/>')
    if kind == "device":
        return (f'<path d="M{x+4} {y+8} h{NW-8} v{NH-8} h-{NW-8} Z M{x+4} {y+8} l8 -8 h{NW-8} l-8 8 M{x+NW-4} {y+8} l8 -8 v{NH-8} l-8 8" stroke-width="1.3"/>'
                f'<path d="M{x+NW-3} {y+9} l6 -6 v{NH-10} l-6 6 Z" fill="url(#{pfx}-shade)" stroke="none"/>')
    if kind == "person":
        return (f'<circle cx="{cx}" cy="{y+2}" r="6" stroke-width="1.2"/>'
                f'<path d="M{cx} {y+8} V{y+26} M{cx} {y+12} l-9 8 M{cx} {y+12} l9 8 M{cx} {y+26} l-7 14 M{cx} {y+26} l7 14" stroke-width="1.2"/>')
    if kind == "file":
        return (f'<path d="M{x+14} {y-2} h{NW-38} l10 10 v{NH-6} h-{NW-28} Z M{x+NW-24} {y-2} v10 h10" stroke-width="1.3"/>'
                f'<path d="M{x+22} {y+14} h{NW-50} M{x+22} {y+22} h{NW-60} M{x+22} {y+30} h{NW-56}" stroke-width="0.5"/>')
    return f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" stroke-width="1.4"/>'

def _anchor(a, b):
    """从节点 a 中心到节点 b 中心的连线，在两端各缩进到节点边界附近"""
    ax, ay, bx, by = a["cx"], a["cy"], b["cx"], b["cy"]
    dx, dy = bx - ax, by - ay
    def edge(cx, cy, dx, dy, sign):
        # 矩形边界近似
        hw, hh = NW/2 + 4, NH/2 + 6
        if abs(dx) * hh > abs(dy) * hw:
            t = hw / abs(dx) if dx else 0
        else:
            t = hh / abs(dy) if dy else 0
        return cx + sign*dx*t, cy + sign*dy*t
    x1, y1 = edge(ax, ay, dx, dy, 1)
    x2, y2 = edge(bx, by, dx, dy, -1)
    return x1, y1, x2, y2

def render(pfx, spec, sig, seed=5):
    nodes = spec.get("nodes", [])[:9]
    byid = {}
    for n in nodes:
        n = dict(n)
        n["cx"] = COLS.get(int(n.get("col", 0)), 200)
        n["cy"] = ROWS.get(int(n.get("row", 0)), 96)
        byid[n["id"]] = n
    drawn, texts, arrows = [], [], []
    for n in byid.values():
        drawn.append(_shape(n.get("kind", "step"), n["cx"], n["cy"], pfx))
        lines = str(n["label"]).split("\n")[:2]
        ty = n["cy"] - (len(lines)-1)*6 + 4
        if n.get("kind") == "person": ty = n["cy"] + 42
        if n.get("kind") == "sensor" and sum(len(l) for l in lines) > 6: ty = n["cy"] + 40
        elif n.get("kind") == "sensor": ty = n["cy"] + 4 - (len(lines)-1)*6
        for i, l in enumerate(lines):
            texts.append(f'<text x="{n["cx"]}" y="{ty+i*13}" text-anchor="middle" font-size="{9.5 if len(l) > 10 else 10.5}">{_esc(l)}</text>')
    for e in spec.get("edges", []):
        if len(e) < 2 or e[0] not in byid or e[1] not in byid: continue
        a, b = byid[e[0]], byid[e[1]]
        x1, y1, x2, y2 = _anchor(a, b)
        dash = ' stroke-dasharray="3 3"' if (len(e) > 3 and e[3] == "dash") else ""
        if abs(y1 - y2) < 2 or abs(x1 - x2) < 2:
            d = f"M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}"
        else:
            mx = (x1 + x2) / 2
            d = f"M{x1:.1f} {y1:.1f} C{mx:.1f} {y1:.1f} {mx:.1f} {y2:.1f} {x2:.1f} {y2:.1f}"
        arrows.append(f'<path d="{d}"{dash}/>')
        if len(e) > 2 and e[2]:
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2 - 5
            texts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="8" fill="#666">{_esc(e[2])}</text>')
    title = _esc(spec.get("title", ""))
    def _w(t, cjk, lat):
        return sum(cjk if ord(c) > 0x2e80 else lat for c in t)
    sig_fs = 10 if _w(sig, 10, 5.6) <= 210 else 8
    sig_w = _w(sig, sig_fs, sig_fs * 0.56)
    raw_usage = spec.get("usage", "")
    room = 448 - sig_w - 10
    while raw_usage and _w(raw_usage, 9, 5) > room:
        raw_usage = raw_usage[:-2] + "…"
    usage = _esc(raw_usage)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">
  <defs>
    <filter id="{pfx}-pencil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.4" xChannelSelector="R" yChannelSelector="G"/></filter>
    <pattern id="{pfx}-shade" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><line x1="0" y1="0" x2="0" y2="5" stroke="#6b6b6b" stroke-width="0.7" stroke-opacity="0.8"/></pattern>
    <marker id="{pfx}-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9" fill="none" stroke="#3d3d3d" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></marker>
  </defs>
  <text x="16" y="28" font-weight="700" font-size="12" fill="#2a2a2a">{title}</text>
  <path d="M16 36 H464" stroke="#8a8a8a" stroke-width="0.6" stroke-dasharray="4 4"/>
  <g filter="url(#{pfx}-pencil)" stroke="#3d3d3d" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="0.92">
    {"".join(drawn)}
  </g>
  <g stroke="#3d3d3d" stroke-width="1.2" fill="none" marker-end="url(#{pfx}-arrow)" stroke-linecap="round">{"".join(arrows)}</g>
  <g fill="#2a2a2a">{"".join(texts)}</g>
  <path d="M16 272 H464" stroke="#8a8a8a" stroke-width="0.6" stroke-dasharray="4 4"/>
  <text x="16" y="288" font-size="9" fill="#555">{usage}</text>
  <text x="464" y="288" text-anchor="end" font-family="{HAND}" font-size="{sig_fs}" fill="#5a5a5a">{_esc(sig)}</text>
</svg>
'''

def slug(name):
    return re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()

if __name__ == "__main__":
    import sys, json
    spec = {"title": "Home Assistant · 本地优先的家庭自动化中枢",
            "nodes": [{"id": "s", "label": "传感器 / ESPHome", "kind": "sensor", "col": 0, "row": 0},
                      {"id": "hw", "label": "华为智慧生活\n设备", "kind": "device", "col": 0, "row": 1},
                      {"id": "ha", "label": "Home Assistant\n自动化引擎", "kind": "core", "col": 1, "row": 0},
                      {"id": "db", "label": "历史数据库", "kind": "db", "col": 1, "row": 1},
                      {"id": "ui", "label": "仪表盘 / 手机", "kind": "screen", "col": 2, "row": 0},
                      {"id": "me", "label": "一个人", "kind": "person", "col": 3, "row": 0},
                      {"id": "cloud", "label": "可选：云端 LLM", "kind": "cloud", "col": 2, "row": 1}],
            "edges": [["s", "ha", "MQTT / 原生"], ["hw", "ha", "集成"], ["ha", "db"], ["ha", "ui", "推送"], ["ui", "me"], ["ha", "cloud", "", "dash"]],
            "usage": "在本模块里：ESPHome 节点 → HA 自动化 → 0802 大屏 / 手机"}
    open("parts/_sample-ghdiag.svg", "w", encoding="utf-8").write(render("g0000-1", spec, "home-assistant/core"))
    print("ok")
