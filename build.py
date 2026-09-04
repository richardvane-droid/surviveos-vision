#!/usr/bin/env python3
"""SurviveOs 设想版站点生成器：data/*.json + illos/*.svg -> dist/"""
import json, glob, shutil, os, re
from pathlib import Path
from jinja2 import Environment, DictLoader, select_autoescape

ROOT = Path(__file__).parent
DIST = ROOT / "docs"
SITE_URL = "https://richardvane-droid.github.io/surviveos-vision/"

AREAS = {
    "01": {"name": "暖村木屋", "en": "Cabin", "line": "PSK 生存盒的展示间 + 制作间 + 冬天最暖的那间屋",
           "intro": "一栋木屋，白天是 PSK 生存盒的展示间和工作台，晚上柴火炉一烧就是待客的小酒馆。这里的每个模块都围着“展示、制作、取暖、待客”四件事转，是整个系统里最有烟火气的一块。"},
    "02": {"name": "地堡", "en": "Bunker", "line": "没有窗的地下 3 米，反而装下了太阳、电影院和秘密基地",
           "intro": "地下室天生潮、天生暗，但也天生安静、天生恒温。地堡区 12 个模块的思路很一致：先把“没有窗”这件事用光、用风、用水解决掉，再往里塞最私人的那些东西——影音室、听音角、鱼缸、帐篷密室、90 天的食物，以及一块能看到整座房子在呼吸的大屏。"},
    "03": {"name": "阁楼间", "en": "Loft", "line": "斜顶之下：工具台、帐篷、光伏，和一根会预报天气的杆子",
           "intro": "斜顶阁楼是最容易被浪费的空间，也是最适合“一个人待着”的空间。这里放小制作、户外装备、一顶常驻帐篷，屋顶上是光伏板和微型气象站——整栋房子的能源与天气，从这层开始。"},
    "04": {"name": "阁楼仓库", "en": "Storage", "line": "一条过道、一间材料仓、一间喷漆房、一间木工房",
           "intro": "仓库区不追求好看，追求“找得到、拿得顺、做得了”。过道两侧是工具墙，尽头分出喷漆间和木工间，中间是材料仓——所有模块的施工，最后都要回到这里动手。"},
    "05": {"name": "庭院", "en": "Yard", "line": "柴火墙、爬山虎、20 个有名字的陶盆，和一根木头充电桩",
           "intro": "庭院是从“屋里”走到“野外”的过渡带。柴火墙既是储备也是背景墙，爬山虎负责让墙自己变绿，种植架和盆栽让浇水这件事被系统接管，角落里一根木头充电桩接住每天回家的电摩。"},
    "06": {"name": "草地", "en": "Savanna", "line": "50㎡ 的杭州稀树草原：地下滴灌、雨水罐、和一个鸟类摄像头",
           "intro": "草地区是目前真实进度最靠前的一块：疏林草原的植物配置、三传感器自动浇灌、1500L 雨水存储已经是落地方案。设想版在这个基础上继续放飞——比如让摄像头认得出 17 种鸟。"},
    "07": {"name": "钓台", "en": "Pier", "line": "伸进池塘的木平台：顶棚、钓具墙、光伏夜灯、小火塘",
           "intro": "真实项目里钓台还没做范围拆解，设想版干脆先替它想好四个模块：平台本体和顶棚、钓具储物墙、离网照明与电源、水边茶席和小火塘。做完之后，这里应该是整套系统里最“什么都不干”的地方。"},
}

STATUS = {
    "✅": {"0201", "0202", "0601", "0602", "0603"},
    "🚧": {"0103", "0209"},
}
def real_status(mid):
    if mid.startswith("07"): return ("设想", "真实项目尚未拆解此区域")
    for k, s in STATUS.items():
        if mid in s: return (k, {"✅": "真实三阶段已完成", "🚧": "真实设计进行中"}[k])
    return ("⬜", "真实项目待设计")

# ---------- load ----------
modules, by_id = [], {}
for f in sorted(glob.glob(str(ROOT / "data" / "0?.json"))):
    for m in json.load(open(f, encoding="utf-8")):
        m["area"] = m["id"][:2]
        m["status"], m["status_note"] = real_status(m["id"])
        m["svg"] = (ROOT / "illos" / f"{m['id']}.svg").read_text(encoding="utf-8")
        modules.append(m); by_id[m["id"]] = m
modules.sort(key=lambda m: m["id"])
for a in AREAS.values(): a["modules"] = []
for m in modules: AREAS[m["area"]]["modules"].append(m)
for aid, a in AREAS.items():
    a["id"] = aid
    a["svg"] = (ROOT / "illos" / f"area-{aid}.svg").read_text(encoding="utf-8")
for i, m in enumerate(modules):
    m["prev"] = modules[i-1] if i > 0 else None
    m["next"] = modules[i+1] if i < len(modules)-1 else None
    m["linked"] = [by_id[x] for x in m["links"] if x in by_id]
from urllib.parse import quote
refs_by_id = {}
for f in sorted(glob.glob(str(ROOT / "data" / "refs-*.json"))):
    for r in json.load(open(f, encoding="utf-8")): refs_by_id[r["id"]] = r
for m in modules:
    r = refs_by_id.get(m["id"], {"github": [], "xhs": []})
    m["github"] = r["github"]
    m["xhs"] = [{**x, "url": "https://www.xiaohongshu.com/search_result?keyword=" + quote(x["keyword"]) + "&source=web_explore_feed"} for x in r["xhs"]]
repo_index = {}
for m in modules:
    for g in m["github"]:
        e = repo_index.setdefault(g["name"], {**g, "used_by": []})
        e["used_by"].append(m)
repo_list = sorted(repo_index.values(), key=lambda e: -float(e["stars"].lower().replace("k", "e3").replace(",", "")) if e["stars"][:1].isdigit() else 0)
refs_stats = {"repos": len(repo_index), "links": sum(len(m["github"]) for m in modules), "xhs": sum(len(m["xhs"]) for m in modules)}
all_tags = {}
for m in modules:
    for t in m["tags"]: all_tags[t] = all_tags.get(t, 0) + 1
top_tags = [t for t, c in sorted(all_tags.items(), key=lambda x: -x[1]) if c >= 3][:18]
stats = {"areas": len(AREAS), "modules": len(modules),
         "done": sum(1 for m in modules if m["status"] == "✅"),
         "wip": sum(1 for m in modules if m["status"] == "🚧")}

def inline_svg(svg, cls=""):
    """strip xml header, force responsive sizing"""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r'\swidth="\d+"\sheight="\d+"', "", svg, count=1)
    return svg.replace("<svg ", f'<svg class="{cls}" role="img" ', 1)

# ---------- templates ----------
BASE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{% endblock %} · SurviveOs 设想版</title>
<meta name="description" content="{% block desc %}SurviveOs 乡野生存系统的完整形态设想：7 个区域、{{ stats.modules }} 个模块专题，黑白钢笔速写插图。{% endblock %}">
<link rel="icon" href="{{ root }}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Long+Cang&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ root }}style.css">
</head>
<body class="{% block bodyclass %}{% endblock %}">
<header class="top">
  <a class="wordmark" href="{{ root }}index.html"><span class="mark">SurviveOs</span><span class="sub">设想版 · 0901</span></a>
  <nav class="areas-nav">
    {% for a in areas.values() %}<a href="{{ root }}areas/{{ a.id }}.html" {% if area and area.id == a.id %}class="on"{% endif %}><i>{{ a.id }}</i>{{ a.name }}</a>{% endfor %}
    <a href="{{ root }}refs.html" class="about {% if page == 'refs' %}on{% endif %}">参考索引</a>
    <a href="{{ root }}about.html" class="about {% if page == 'about' %}on{% endif %}">关于</a>
  </nav>
</header>
<main>
{% block body %}{% endblock %}
</main>
<footer class="foot">
  <p><b>SurviveOs · 设想版</b>（模块 0901）——只在真实项目的区域/模块框架里放飞想象，<u>不代表真实进度、不构成施工依据</u>。真实进度以本地仓库 0002 清单为准。</p>
  <p class="tiny">{{ stats.areas }} 区域 · {{ stats.modules }} 个模块专题 · 插图为原创黑白钢笔速写（inline SVG）· 由 Claude 生成于 2026-09 · <a href="https://github.com/richardvane-droid/surviveos-vision">源码</a></p>
</footer>
{% block script %}{% endblock %}
</body>
</html>"""

INDEX = r"""{% extends "base" %}{% block title %}一座乡野生存系统，做完之后的样子{% endblock %}
{% block bodyclass %}home{% endblock %}
{% block body %}
<section class="hero">
  <div class="hero-text">
    <p class="kicker">SurviveOs · 完整形态设想</p>
    <h1>一座乡野生存系统，<br>做完之后的样子。</h1>
    <p class="lede">杭州乡下的一栋木屋、一个地堡、一层阁楼、一片草地和一座钓台。真实项目还在一个模块一个模块地做；这个站先把 <b>{{ stats.modules }} 个模块全部想完</b>——每个模块一页专题，小红书式的放飞文案，配一张黑白钢笔速写。</p>
    <div class="stats">
      <div><b>{{ stats.areas }}</b><span>个区域</span></div>
      <div><b>{{ stats.modules }}</b><span>个模块专题</span></div>
      <div><b>{{ stats.done }}</b><span>个真实已完成</span></div>
      <div><b>{{ stats.modules - stats.done - stats.wip }}</b><span>个纯幻想</span></div>
    </div>
    <p class="stamp-row"><span class="stamp">设想版 · 非真实进度</span><span class="hand">看看就好，别当施工图 ↗</span></p>
  </div>
  <figure class="hero-art">{{ areas['01'].svg_inline|safe }}<figcaption>01 暖村木屋 · 区域速写</figcaption></figure>
</section>

<section class="sec">
  <h2 class="sec-title"><span>七个区域</span><small>从屋里到水边，按编号走一圈</small></h2>
  <div class="area-grid">
  {% for a in areas.values() %}
    <a class="area-card" href="areas/{{ a.id }}.html">
      <div class="art">{{ a.svg_inline|safe }}</div>
      <div class="meta"><i>{{ a.id }}</i><h3>{{ a.name }}</h3><p>{{ a.line }}</p><span class="count">{{ a.modules|length }} 个模块 →</span></div>
    </a>
  {% endfor %}
  </div>
</section>

<section class="sec" id="all">
  <h2 class="sec-title"><span>全部 {{ stats.modules }} 个专题</span><small>点标签筛选，点卡片进专题页</small></h2>
  <div class="chips"><button class="chip on" data-tag="">全部</button>{% for t in top_tags %}<button class="chip" data-tag="{{ t }}">#{{ t }}</button>{% endfor %}</div>
  <div class="mod-grid">
  {% for m in modules %}
    <a class="mod-card" href="modules/{{ m.id }}.html" data-tags="{{ m.tags|join(',') }}">
      <div class="thumb">{{ m.svg_inline|safe }}</div>
      <div class="body">
        <div class="row"><i>{{ m.id }}</i><b>{{ m.name }}</b><span class="st st-{{ m.status }}" title="{{ m.status_note }}">{{ m.status }}</span></div>
        <p class="hook">{{ m.hook }}</p>
        <p class="tags">{% for t in m.tags[:3] %}<span>#{{ t }}</span>{% endfor %}</p>
      </div>
    </a>
  {% endfor %}
  </div>
  <p class="empty" hidden>这个标签下暂时没有模块。</p>
</section>
{% endblock %}
{% block script %}<script>
(function(){
  var chips=document.querySelectorAll('.chip'),cards=document.querySelectorAll('.mod-card'),empty=document.querySelector('.empty');
  chips.forEach(function(c){c.addEventListener('click',function(){
    chips.forEach(function(x){x.classList.remove('on')});c.classList.add('on');
    var t=c.dataset.tag,n=0;
    cards.forEach(function(k){var ok=!t||(','+k.dataset.tags+',').indexOf(','+t+',')>=0;k.hidden=!ok;if(ok)n++;});
    empty.hidden=n>0;
  });});
})();
</script>{% endblock %}"""

AREA = r"""{% extends "base" %}{% block title %}{{ area.id }} {{ area.name }}{% endblock %}
{% block desc %}{{ area.name }}：{{ area.line }}。{{ area.modules|length }} 个模块专题。{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <span>{{ area.id }} {{ area.name }}</span></nav>
<section class="area-hero">
  <figure class="area-art">{{ area.svg_inline|safe }}</figure>
  <div class="area-head">
    <p class="kicker">区域 {{ area.id }} · {{ area.en }}</p>
    <h1>{{ area.name }}</h1>
    <p class="lede">{{ area.line }}</p>
    <p class="intro">{{ area.intro }}</p>
  </div>
</section>
<section class="sec">
  <h2 class="sec-title"><span>{{ area.modules|length }} 个模块专题</span><small>按编号排列，编号不代表优先级</small></h2>
  <div class="mod-list">
  {% for m in area.modules %}
    <a class="mod-row" href="{{ root }}modules/{{ m.id }}.html">
      <div class="thumb">{{ m.svg_inline|safe }}</div>
      <div class="body">
        <div class="row"><i>{{ m.id }}</i><b>{{ m.name }}</b><span class="st st-{{ m.status }}" title="{{ m.status_note }}">{{ m.status }} {{ m.status_note }}</span></div>
        <h3>{{ m.hook }}</h3>
        <p>{{ m.tagline }}</p>
        <p class="tags">{% for t in m.tags %}<span>#{{ t }}</span>{% endfor %}</p>
      </div>
    </a>
  {% endfor %}
  </div>
</section>
<nav class="pager">
  {% if prev_area %}<a href="{{ root }}areas/{{ prev_area.id }}.html">← {{ prev_area.id }} {{ prev_area.name }}</a>{% else %}<span></span>{% endif %}
  {% if next_area %}<a href="{{ root }}areas/{{ next_area.id }}.html">{{ next_area.id }} {{ next_area.name }} →</a>{% endif %}
</nav>
{% endblock %}"""

MODULE = r"""{% extends "base" %}{% block title %}{{ m.id }} {{ m.name }}{% endblock %}
{% block desc %}{{ m.hook }}——{{ m.tagline }}{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <a href="{{ root }}areas/{{ area.id }}.html">{{ area.id }} {{ area.name }}</a> › <span>{{ m.id }} {{ m.name }}</span></nav>
<article class="mod">
  <header class="mod-head">
    <p class="kicker">{{ area.name }} · 模块 {{ m.id }} · {{ m.name }}</p>
    <h1>{{ m.hook }}</h1>
    <p class="lede">{{ m.tagline }}</p>
    <p class="meta">
      <span class="st st-{{ m.status }}">{{ m.status }} {{ m.status_note }}</span>
      {% for t in m.tags %}<span class="tag">#{{ t }}</span>{% endfor %}
    </p>
  </header>
  <figure class="mod-art">
    {{ m.svg_inline|safe }}
    <figcaption><span class="hand">速写 · {{ m.sketch_brief }}</span></figcaption>
  </figure>

  <section class="blk"><h2><em>🎬</em> 沉浸式想象</h2><p class="scene">{{ m.scene }}</p></section>

  <section class="blk"><h2><em>✅</em> 设想方案清单</h2>
    <ol class="plan">{% for p in m.plan %}<li><span class="box"></span><span>{{ p }}</span></li>{% endfor %}</ol></section>

  <div class="two">
    <section class="blk"><h2><em>🔥</em> 小红书灵感点</h2><ul class="inspo">{% for p in m.inspo %}<li>{{ p }}</li>{% endfor %}</ul></section>
    <section class="blk"><h2><em>⚠️</em> 避坑提醒</h2><ul class="pit">{% for p in m.pitfalls %}<li>{{ p }}</li>{% endfor %}</ul></section>
  </div>

  <section class="blk budget"><h2><em>💰</em> 预算幻想</h2><p>{{ m.budget }}</p><p class="tiny">纯拍脑袋的量级感，真实选型以各模块的设备电商选型阶段为准。</p></section>

  {% if m.github %}<section class="blk"><h2><em>🔧</em> GitHub 上的成熟方案</h2>
    <p class="tiny">真实存在、可直接拿来用或改的开源项目（星数为 2026-09 抓取时页面显示值）。</p>
    <div class="gh-list">{% for g in m.github %}
      <a class="gh" href="{{ g.url }}" target="_blank" rel="noopener">
        <div class="gh-head"><b>{{ g.name }}</b><span class="stars">★ {{ g.stars }}</span></div>
        <p class="gh-desc">{{ g.desc }}</p>
        <p class="gh-why">→ {{ g.why }}</p>
      </a>{% endfor %}
    </div></section>{% endif %}

  {% if m.xhs %}<section class="blk"><h2><em>📷</em> 小红书视觉参考</h2>
    <p class="tiny">点关键词直接跳到小红书站内搜索（需登录小红书），看热门帖里的实拍效果。</p>
    <div class="xhs-list">{% for x in m.xhs %}
      <a class="xhs" href="{{ x.url }}" target="_blank" rel="noopener"><span class="kw">🔍 {{ x.keyword }}</span><span class="xnote">{{ x.note }}</span></a>{% endfor %}
    </div></section>{% endif %}

  {% if m.linked %}<section class="blk"><h2><em>🔗</em> 联动模块</h2>
    <div class="link-grid">{% for l in m.linked %}
      <a class="link-card" href="{{ root }}modules/{{ l.id }}.html"><div class="thumb">{{ l.svg_inline|safe }}</div><div><i>{{ l.id }}</i><b>{{ l.name }}</b><p>{{ l.tagline }}</p></div></a>
    {% endfor %}</div></section>{% endif %}

  <nav class="pager">
    {% if m.prev %}<a href="{{ root }}modules/{{ m.prev.id }}.html">← {{ m.prev.id }} {{ m.prev.name }}</a>{% else %}<span></span>{% endif %}
    <a class="up" href="{{ root }}areas/{{ area.id }}.html">回到 {{ area.name }}</a>
    {% if m.next %}<a href="{{ root }}modules/{{ m.next.id }}.html">{{ m.next.id }} {{ m.next.name }} →</a>{% endif %}
  </nav>
</article>
{% endblock %}"""

ABOUT = r"""{% extends "base" %}{% block title %}关于这个设想版{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <span>关于</span></nav>
<article class="mod about">
  <header class="mod-head">
    <p class="kicker">模块 0901 · 设想版说明</p>
    <h1>这个站是"先把结局想完"的一次练习</h1>
    <p class="lede">真实的 SurviveOs 项目是一个模块一个模块严谨地做——方案原理推演、设备电商选型、施工。0901 反过来：不严谨、不算账、不等进度，先把 {{ stats.modules }} 个模块"做完之后的样子"一口气想完，给真实设计当参照物，也给家人朋友一个能逛的地方。</p>
  </header>
  <section class="blk"><h2><em>①</em> 框架是真的，内容是想的</h2>
    <p class="scene">7 个区域和模块编号完全沿用真实项目的《0002 区域与子模块清单》。5 个真实已完成的模块（0201 模拟阳光、0202 卫生间灯箱、0601～0603 草地三件套）和 2 个进行中的模块（0103 电子画框墙、0209 藏宝阁），设想内容在真实方案基础上放飞；其余模块是纯幻想。钓台区真实项目还没拆解，这里先替它想了 0701～0704 四个模块。每页右上角的状态章（⬜ / 🚧 / ✅ / 设想）标的是<b>真实进度</b>，不是设想进度。</p></section>
  <section class="blk"><h2><em>②</em> 文案参考了小红书的热门写法</h2>
    <p class="scene">标题带钩子、短句、口语、适量 emoji；正文固定五段：沉浸式想象 → 设想方案清单 → 小红书灵感点 → 避坑提醒 → 预算幻想。灵感点里反复出现的"适我主义""精神角落 / 精神领地 / 逃避间""痛屋""家的丰容计划""去家务化 / 动线""动手主义""和植物一起住""观鸟"等，来自小红书 2026 年度居住趋势和热门话题。</p></section>
  <section class="blk"><h2><em>③</em> 插图是统一风格的黑白钢笔速写</h2>
    <p class="scene">全站 {{ stats.modules }} 张模块速写 + 7 张区域全景都是原创的 inline SVG：只有一种墨色，阴影全部用 45° 排线，轮廓"描两遍"，线条经过轻微的扰动滤镜制造手绘感，右下角是编号签名。没有任何外部图片，页面在离线状态也能完整显示。</p></section>
  <section class="blk"><h2><em>④</em> 每页附了真实的参考链接</h2>
    <p class="scene">每个模块页下方有两块引用：“GitHub 上的成熟方案”列 2～4 个真实存在的开源项目（硬件设计、固件、HomeAssistant 集成、管理软件），每个都在 2026-09 打开核实过、星数取自当时页面；“小红书视觉参考”给 2～3 组站内搜索关键词，点开直接看热门帖的实拍效果。全站去重后的项目清单见<a href="{{ root }}refs.html">参考索引</a>。</p></section>
  <section class="blk"><h2><em>⑤</em> 怎么用它</h2>
    <ol class="plan">
      <li><span class="box"></span><span>开某个模块的真实设计对话前，先看一眼它的设想页，把"想要的感觉"带进去。</span></li>
      <li><span class="box"></span><span>家人朋友逛完在微信里说"这个我想要 / 这个算了"，比看方案文档快得多。</span></li>
      <li><span class="box"></span><span>真实模块跨阶段时不需要改这个站——它就是一次性的完整形态快照，和真实进度是两条线。</span></li>
    </ol></section>
  <nav class="pager"><span></span><a class="up" href="{{ root }}index.html">回首页</a><span></span></nav>
</article>
{% endblock %}"""

REFS = r"""{% extends "base" %}{% block title %}参考索引{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <span>参考索引</span></nav>
<article class="mod about">
  <header class="mod-head">
    <p class="kicker">全站引用</p>
    <h1>{{ refs_stats.repos }} 个开源项目，{{ refs_stats.xhs }} 组小红书关键词</h1>
    <p class="lede">{{ stats.modules }} 个模块专题页里引用的 GitHub 项目汇总（按星数排序，去重），每个都在 2026-09 打开核实过存在。点模块编号回到对应专题页看“为什么用它”。小红书关键词在各模块页里。</p>
  </header>
  <section class="blk">
    <div class="repo-table">{% for e in repo_list %}
      <div class="repo-row">
        <a class="rname" href="{{ e.url }}" target="_blank" rel="noopener">{{ e.name }}</a>
        <span class="stars">★ {{ e.stars }}</span>
        <span class="rdesc">{{ e.desc }}</span>
        <span class="rused">{% for m in e.used_by %}<a href="{{ root }}modules/{{ m.id }}.html" title="{{ m.name }}">{{ m.id }}</a>{% endfor %}</span>
      </div>{% endfor %}
    </div>
  </section>
  <nav class="pager"><span></span><a class="up" href="{{ root }}index.html">回首页</a><span></span></nav>
</article>
{% endblock %}"""

CSS = r"""
:root{--paper:#f5f0e6;--paper2:#ece5d7;--ink:#1c1c1c;--ink2:#4d4944;--ink3:#8a847a;--line:#1c1c1c;--red:#b5372b;--w:1120px}
*{box-sizing:border-box}
html{background:var(--paper)}
body{margin:0;color:var(--ink);font-family:"Noto Sans SC",-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.75;
 background:var(--paper);
 background-image:radial-gradient(rgba(0,0,0,.035) 1px,transparent 1px);background-size:5px 5px}
a{color:inherit;text-decoration:none}
h1,h2,h3{font-family:"Noto Serif SC","Songti SC","STSong",serif;line-height:1.3;margin:0}
.hand{font-family:"Long Cang","Kaiti SC","KaiTi",cursive;font-size:1.25em;color:var(--ink2)}
i{font-style:normal;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85em;color:var(--ink3);letter-spacing:.04em}
svg{display:block;width:100%;height:auto}
main{max-width:var(--w);margin:0 auto;padding:0 20px}

/* sketchy border helper */
.sk{border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;background:rgba(255,255,255,.35)}

/* header */
.top{max-width:var(--w);margin:0 auto;padding:18px 20px 8px;display:flex;flex-wrap:wrap;gap:10px 24px;align-items:baseline;justify-content:space-between;border-bottom:1.6px solid var(--line)}
.wordmark .mark{font-family:"Noto Serif SC",serif;font-weight:900;font-size:1.5rem;letter-spacing:.02em}
.wordmark .sub{margin-left:10px;font-family:"Long Cang",cursive;font-size:1.15rem;color:var(--red)}
.areas-nav{display:flex;flex-wrap:wrap;gap:2px 14px;font-size:.92rem}
.areas-nav a{padding:2px 2px;border-bottom:2px solid transparent}
.areas-nav a i{margin-right:3px}
.areas-nav a.on,.areas-nav a:hover{border-bottom-color:var(--red)}
.areas-nav .about{margin-left:6px;color:var(--ink3)}

/* hero */
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:36px;align-items:center;padding:44px 0 30px}
.kicker{font-family:"Long Cang",cursive;font-size:1.3rem;color:var(--red);margin:0 0 6px}
.hero h1{font-size:clamp(1.9rem,4.2vw,3rem);font-weight:900}
.lede{font-size:1.08rem;color:var(--ink2);margin:14px 0 0}
.stats{display:flex;gap:28px;margin:22px 0 12px;flex-wrap:wrap}
.stats div{display:flex;flex-direction:column}
.stats b{font-family:"Noto Serif SC",serif;font-size:2rem;font-weight:900;line-height:1}
.stats span{font-size:.82rem;color:var(--ink3)}
.stamp-row{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:8px 0 0}
.stamp{display:inline-block;padding:3px 10px;border:2px solid var(--red);color:var(--red);font-weight:700;font-size:.85rem;letter-spacing:.12em;transform:rotate(-3deg);border-radius:4px;opacity:.9;
 mask-image:radial-gradient(rgba(0,0,0,.95) 60%,rgba(0,0,0,.75));}
.hero-art{margin:0}
.hero-art figcaption,.mod-art figcaption{text-align:right;font-size:.85rem;color:var(--ink3);margin-top:4px}
.hero-art svg{border-bottom:1.6px solid var(--line)}

/* sections */
.sec{padding:26px 0 10px}
.sec-title{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;margin:0 0 18px;font-size:1.5rem;font-weight:900}
.sec-title small{font-family:"Long Cang",cursive;font-weight:400;font-size:1.1rem;color:var(--ink3)}

.area-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.area-card{border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;overflow:hidden;background:rgba(255,255,255,.4);display:flex;flex-direction:column;transition:transform .15s}
.area-card:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--ink)}
.area-card .art{padding:6px 10px 0;border-bottom:1.6px solid var(--line)}
.area-card .meta{padding:12px 16px 16px}
.area-card h3{font-size:1.25rem;display:inline;margin-left:6px}
.area-card p{margin:6px 0 8px;color:var(--ink2);font-size:.93rem}
.area-card .count{font-family:"Long Cang",cursive;color:var(--red);font-size:1.1rem}

.chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 18px}
.chip{font:inherit;font-size:.85rem;padding:3px 12px;border:1.4px solid var(--ink);background:transparent;border-radius:200px 12px 180px 12px/12px 180px 12px 200px;cursor:pointer;color:var(--ink2)}
.chip.on,.chip:hover{background:var(--ink);color:var(--paper)}

.mod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.mod-card{border:1.6px solid var(--line);border-radius:14px 200px 14px 220px/220px 14px 200px 14px;background:rgba(255,255,255,.45);overflow:hidden;display:flex;flex-direction:column;transition:transform .15s}
.mod-card:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--ink)}
.mod-card .thumb{padding:4px 8px 0;border-bottom:1.6px solid var(--line)}
.mod-card .body{padding:10px 14px 12px}
.row{display:flex;align-items:center;gap:8px}
.row b{font-family:"Noto Serif SC",serif;font-weight:900}
.st{margin-left:auto;font-size:.78rem;white-space:nowrap;color:var(--ink3)}
.st-✅{color:#2f6b3a}.st-🚧{color:#a6691a}.st-设想{color:var(--red)}
.hook{margin:6px 0 4px;font-weight:500;line-height:1.5;font-size:.95rem}
.tags{margin:0;font-size:.78rem;color:var(--ink3)}.tags span{margin-right:8px}
.empty{color:var(--ink3);text-align:center}

/* area page */
.crumb{font-size:.85rem;color:var(--ink3);padding:14px 0 0}
.crumb a:hover{color:var(--red)}
.area-hero{display:grid;grid-template-columns:1.25fr 1fr;gap:30px;align-items:center;padding:16px 0 10px}
.area-art{margin:0;border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;padding:8px 14px 2px;background:rgba(255,255,255,.4)}
.area-head h1{font-size:clamp(1.8rem,3.6vw,2.6rem);font-weight:900}
.intro{color:var(--ink2);margin-top:12px}
.mod-list{display:flex;flex-direction:column;gap:16px}
.mod-row{display:grid;grid-template-columns:260px 1fr;gap:20px;align-items:center;border:1.6px solid var(--line);border-radius:14px 220px 14px 240px/240px 14px 220px 14px;padding:12px 18px 12px 12px;background:rgba(255,255,255,.4);transition:transform .15s}
.mod-row:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--ink)}
.mod-row .thumb{border-right:1.6px solid var(--line);padding-right:12px}
.mod-row h3{font-size:1.2rem;margin:6px 0 4px}
.mod-row p{margin:0 0 6px;color:var(--ink2);font-size:.95rem}

/* module page */
.mod{max-width:820px;margin:0 auto;padding-bottom:30px}
.mod-head{padding:18px 0 8px}
.mod-head h1{font-size:clamp(1.6rem,3.4vw,2.4rem);font-weight:900}
.meta{display:flex;flex-wrap:wrap;gap:6px 12px;margin:14px 0 0;font-size:.85rem;align-items:center}
.meta .st{margin-left:0;border:1.4px solid currentColor;padding:1px 8px;border-radius:200px 10px 180px 10px/10px 180px 10px 200px}
.meta .tag{color:var(--ink3)}
.mod-art{margin:18px 0 6px;border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;padding:10px 16px 6px;background:rgba(255,255,255,.45)}
.blk{padding:22px 0 4px;border-top:1.6px dashed rgba(28,28,28,.35)}
.blk h2{font-size:1.25rem;font-weight:900;margin:0 0 10px;display:flex;align-items:center;gap:8px}
.blk h2 em{font-style:normal;font-size:1.05rem}
.scene{font-size:1.02rem;color:var(--ink);margin:0;text-indent:0}
.plan{list-style:none;padding:0;margin:0;counter-reset:p}
.plan li{display:flex;gap:12px;align-items:flex-start;padding:7px 0;border-bottom:1px dotted rgba(28,28,28,.25)}
.plan li:last-child{border-bottom:0}
.box{flex:0 0 16px;height:16px;margin-top:6px;border:1.6px solid var(--ink);border-radius:5px 2px 6px 3px;position:relative}
.two{display:grid;grid-template-columns:1fr 1fr;gap:0 30px}
.inspo,.pit{margin:0;padding:0 0 0 2px;list-style:none}
.inspo li,.pit li{position:relative;padding:5px 0 5px 22px}
.inspo li::before{content:"✦";position:absolute;left:0;color:var(--red)}
.pit li::before{content:"✕";position:absolute;left:1px;color:var(--ink3);font-weight:700}
.budget p{margin:0}
.tiny{font-size:.8rem;color:var(--ink3)}
.link-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.link-card{display:grid;grid-template-columns:88px 1fr;gap:10px;align-items:center;border:1.6px solid var(--line);border-radius:200px 12px 180px 12px/12px 180px 12px 200px;padding:8px 10px;background:rgba(255,255,255,.4);font-size:.85rem}
.link-card:hover{box-shadow:3px 3px 0 var(--ink)}
.link-card b{display:block;font-family:"Noto Serif SC",serif}
.link-card p{margin:2px 0 0;color:var(--ink3);line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.gh-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
.gh{display:block;border:1.6px solid var(--line);border-radius:200px 12px 180px 12px/12px 180px 12px 200px;padding:10px 14px;background:rgba(255,255,255,.4);font-size:.88rem}
.gh:hover{box-shadow:3px 3px 0 var(--ink)}
.gh-head{display:flex;justify-content:space-between;gap:8px;align-items:baseline}
.gh-head b{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.85rem;word-break:break-all}
.stars{font-size:.78rem;color:var(--red);white-space:nowrap}
.gh-desc{margin:6px 0 4px;color:var(--ink2);line-height:1.5}
.gh-why{margin:0;color:var(--ink);line-height:1.5}
.xhs-list{display:flex;flex-direction:column;gap:8px}
.xhs{display:flex;gap:14px;align-items:baseline;flex-wrap:wrap;border-bottom:1px dotted rgba(28,28,28,.3);padding:6px 0}
.xhs .kw{font-weight:700;color:var(--red);white-space:nowrap}
.xhs .xnote{color:var(--ink2);font-size:.9rem}
.xhs:hover .kw{border-bottom:1.5px solid var(--red)}
.repo-table{display:flex;flex-direction:column}
.repo-row{display:grid;grid-template-columns:230px 60px 1fr 150px;gap:12px;align-items:baseline;padding:8px 0;border-bottom:1px dotted rgba(28,28,28,.3);font-size:.88rem}
.repo-row .rname{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;word-break:break-all;border-bottom:1px solid transparent}
.repo-row .rname:hover{border-bottom-color:var(--red)}
.repo-row .rdesc{color:var(--ink2)}
.repo-row .rused a{font-family:ui-monospace,monospace;font-size:.78rem;color:var(--ink3);margin-right:6px}
.repo-row .rused a:hover{color:var(--red)}
@media (max-width:820px){.repo-row{grid-template-columns:1fr 60px;}.repo-row .rdesc,.repo-row .rused{grid-column:1/-1}}
.pager{display:flex;justify-content:space-between;gap:12px;padding:26px 0 10px;font-size:.92rem;border-top:1.6px solid var(--line);margin-top:26px}
.pager a{border-bottom:1.5px solid transparent;white-space:nowrap}.pager a:hover{border-bottom-color:var(--red)}
.pager .up{font-family:"Long Cang",cursive;font-size:1.15rem;color:var(--red)}

.foot{max-width:var(--w);margin:30px auto 0;padding:18px 20px 40px;border-top:1.6px solid var(--line);font-size:.88rem;color:var(--ink2)}
.foot a{border-bottom:1px solid var(--ink3)}

@media (max-width:820px){
 .hero,.area-hero{grid-template-columns:1fr;gap:18px;padding-top:22px}
 .hero-art{order:-1}
 .two{grid-template-columns:1fr}
 .mod-row{grid-template-columns:1fr;gap:8px}
 .mod-row .thumb{border-right:0;border-bottom:1.6px solid var(--line);padding:0 0 6px}
 .top{padding-bottom:12px}
}
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#f5f0e6"/><path d="M5 26 L16 7 L27 26 Z" fill="none" stroke="#1c1c1c" stroke-width="2.4" stroke-linejoin="round"/><path d="M12 26 V19 H20 V26" fill="none" stroke="#1c1c1c" stroke-width="2"/></svg>"""

env = Environment(loader=DictLoader({"base": BASE, "index": INDEX, "area": AREA, "module": MODULE, "about": ABOUT, "refs": REFS}),
                  autoescape=select_autoescape(default=True))

# ---------- build ----------
if DIST.exists(): shutil.rmtree(DIST)
(DIST / "areas").mkdir(parents=True); (DIST / "modules").mkdir()
for m in modules: m["svg_inline"] = inline_svg(m["svg"], "sk-art")
for a in AREAS.values(): a["svg_inline"] = inline_svg(a["svg"], "sk-art")
ctx = dict(areas=AREAS, modules=modules, stats=stats, top_tags=top_tags, area=None, page=None, repo_list=repo_list, refs_stats=refs_stats)

(DIST / "index.html").write_text(env.get_template("index").render(root="", **ctx), encoding="utf-8")
(DIST / "about.html").write_text(env.get_template("about").render(root="", **{**ctx, "page": "about"}), encoding="utf-8")
(DIST / "refs.html").write_text(env.get_template("refs").render(root="", **{**ctx, "page": "refs"}), encoding="utf-8")
alist = list(AREAS.values())
for i, a in enumerate(alist):
    (DIST / "areas" / f"{a['id']}.html").write_text(env.get_template("area").render(
        root="../", **{**ctx, "area": a, "prev_area": alist[i-1] if i else None, "next_area": alist[i+1] if i < len(alist)-1 else None}), encoding="utf-8")
for m in modules:
    (DIST / "modules" / f"{m['id']}.html").write_text(env.get_template("module").render(
        root="../", **{**ctx, "m": m, "area": AREAS[m["area"]]}), encoding="utf-8")
(DIST / "style.css").write_text(CSS, encoding="utf-8")
(DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
(DIST / ".nojekyll").write_text("")
# sitemap
urls = ["index.html", "about.html", "refs.html"] + [f"areas/{a}.html" for a in AREAS] + [f"modules/{m['id']}.html" for m in modules]
(DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
print(f"built {len(urls)} pages -> {DIST}")
