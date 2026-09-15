#!/usr/bin/env python3
"""SurviveOs 设想版站点生成器：data/*.json + illos/*.svg -> dist/"""
import json, glob, shutil, os, re
from pathlib import Path
from jinja2 import Environment, DictLoader, select_autoescape

ROOT = Path(__file__).parent
DIST = ROOT / "docs"
SITE_URL = "https://richardvane-droid.github.io/surviveos-vision/"

AREAS = {
    "01": {"name": "暖村木屋", "en": "Cabin", "line": "2×5 米的木屋：北墙一整面展示墙，西南角一只柴火炉，东墙一张梯子床",
           "intro": "一间 2.00×5.00 米、东西向的长条木屋，夹在地堡和庭院之间。南墙开门窗，东墙是梯子床（床下写字台和通往地堡的暗门），西墙挂空调，唯一完整的展示面就是北墙——吧台矮柜在西段，上方从西到东排开电子画框墙、照片墙、作品展示墙，主产品展示在作品墙正下方。白天是 PSK 生存盒的展示间和工作台，晚上柴火炉一烧，就是一个人的小酒馆。",
           "space": "2.00 × 5.00m · 10㎡ · 净高 2660（梁下 2400）", "plans": ["northwall", "bunker-cabin"],
           "plan_note": "两张图：木屋北墙立面（自室内向北看）；地堡与木屋家具平面里，木屋是梁以南的那 2 米。"},
    "02": {"name": "地堡", "en": "Bunker", "line": "没有窗的 4.85×5 米，反而装下了太阳、电影院和床底的秘密基地",
           "intro": "地堡完全无窗，净高 2660，天生潮、天生暗，但也天生安静、天生恒温。西北角一张架空床，床下 1.2×1.5 米就是藏宝阁；北墙书架、沙发、地毯正对南侧梁墙上的 98 寸电视；东北角是卫生间灯箱，东侧储藏室放防灾食品，东南角开门。12 个模块的思路很一致：先把“没有窗”这件事用光、用风、用水解决掉，再往里塞最私人的那些东西。",
           "space": "4.85 × 5.00m · 24.3㎡（含卫生间、储藏室）· 净高 2660 · 完全无窗", "plans": ["bunker-cabin", "floor1"],
           "plan_note": "两张图：地堡与木屋家具平面（上北下南）；一层平面里，东南角这一户才是自己的。"},
    "03": {"name": "阁楼间", "en": "Loft", "line": "45° 坡顶之下：帐篷、工具台、一扇天窗，和一根会预报天气的杆子",
           "intro": "阁楼层整层归自己，屋面是 45° 四坡、中间最高 2060——离外墙多少米，天花板就多高。阁楼间在西侧偏中，34.5㎡ 里能站直的只有 24.1㎡，帐篷（约 2.35×2.16m）和工具台（约 1.88×0.84m）都落在可站立核心区里，头顶一扇约 800×900 的可开启天窗。这里放小制作、户外装备、一顶常驻帐篷，屋顶上是光伏板和微型气象站。",
           "space": "≈7.5 × 5.35m（带缺口）· 34.5㎡ / 可站立 24.1㎡ · 最高 2060、均 1830", "plans": ["attic"],
           "plan_note": "阁楼层分区。虚线框内为净高 2060 的可站立核心区，斜线带是檐口低矮圈，越靠外越矮。"},
    "04": {"name": "阁楼仓库", "en": "Storage", "line": "北条材料仓、东侧木工间、一只喷涂柜，和一条全能站直的过道",
           "intro": "仓库区不追求好看，追求“找得到、拿得顺、做得了”。材料仓库占北条（24.8㎡，能站直的只有 6.7㎡，低矮带正好放长直货架）；木工间占整个东侧（54.1㎡ / 可站立 26.0㎡，南北向 8.54 米的直线站立核心）；喷漆不做独立房间，改成木工间东缘南段一只 1.5×1.0 米的下抽式喷涂柜，排风一根直管向东出墙；中间 11.2㎡ 的过道全能站直，是整层的工具墙。楼板承重没核算之前，台锯这类重家伙先停在选型阶段。",
           "space": "过道 11.2㎡ · 材料仓库 24.8㎡ · 木工间 54.1㎡ · 成品暂存 16.6㎡（可站立合计约 46㎡）", "plans": ["attic"],
           "plan_note": "阁楼层分区。0402 在北条，0404 在东侧，0403 喷涂柜在木工间东缘南段，排风出东墙。"},
    "05": {"name": "庭院", "en": "Yard", "line": "木屋以南 22㎡：柴火墙、爬山虎、有名字的陶盆，和一根木头充电桩",
           "intro": "庭院约 5.1×4.35 米，从木屋南墙一直到南端的石墩，东边挨着草地，再往南是 2 米过道和 6 米缓坡。它是从“屋里”走到“野外”的过渡带：柴火墙既是储备也是背景墙，爬山虎负责让墙自己变绿，种植架和盆栽让浇水这件事被系统接管，靠过道一侧的角落里一根木头充电桩接住每天回家的电摩。22㎡ 不大，五个模块都得各占一边。",
           "space": "≈5.1 × 4.35m · 22.2㎡ · 露天", "plans": ["site"],
           "plan_note": "场地总图。庭院在木屋以南，往南依次是 2m 过道、6m 缓坡、10m 宽的河。"},
    "06": {"name": "草地", "en": "Savanna", "line": "建筑东侧 5.3×18.9 米的长条草原：地下滴灌、雨水罐、和一个鸟类摄像头",
           "intro": "草地在建筑东侧，是一条 5.3×18.9 米、约 100㎡ 的南北向长条——比最早按 50㎡ 做的方案大了一倍，形状也从近方形变成了长条，所以稀树草原的植物配置、管网、水泵、雨水罐都退回 🚧 重做一轮。设想版就按长条来想：乔木沿长边间隔、视线通廊贯穿南北、分区阀门分段，雨水罐和水泵靠建筑东墙落位，摄像头从东墙高处俯视整条草地。",
           "space": "5.3 × 18.9m · 100㎡ · 露天 · 南北向长条", "plans": ["site"],
           "plan_note": "场地总图。草地是建筑东侧那条 100㎡ 的长条，与地堡、木屋、庭院的东墙相邻。"},
    "07": {"name": "钓台", "en": "Pier", "line": "缓坡尽头临河的 5.5㎡：一把椅子、一根竿、一盏光伏灯、一只小火塘",
           "intro": "从庭院出来，穿过 2 米过道、走下 6 米缓坡，就是钓台——约 2.5×2.2 米、5.5㎡，在岸上临河的那一端，面前是 10 米宽的河。它不是伸进水里的栈桥平台，尺寸只够一个人、一把椅、一张小桌。真实项目里钓台还没做范围拆解，设想版先替它想好四个模块：平台本体和顶棚、钓具储物、离网照明与电源、水边茶席和小火塘。做完之后，这里应该是整套系统里最“什么都不干”的地方。",
           "space": "≈2.5 × 2.2m · ≈5.5㎡ · 露天 · 缓坡临河端（按庭院四分之一预估）", "plans": ["site"],
           "plan_note": "场地总图。钓台在庭院以南、缓坡临河的那一端，钓台尺寸按庭院四分之一面积预估。"},
    "08": {"name": "虚拟空间", "en": "Virtual", "line": "不属于任何一间屋：数字孪生、中枢大屏、一只到处走的 AI 小鸭、一个地下机房，和一份全屋材质总纲",
           "intro": "2026-09-09 真实项目新设的区域，收纳“不专属于任何单一物理区域”的东西：一层跨区域的基础信息层（0801 物品数字孪生、0802 全屋中枢，原地堡的 0206 / 0211 迁到这里重编号），一台在空间里移动的实体设备（0803 miniduck）、一个替掉全屋树莓派的三机小机房（0804 全屋存储 + 全屋智能），以及一份所有手工模块都要继承的材质总纲（0805：木料 / 铝型材 / 皮草，铝型材已定标欧标 2020 喷砂黑）。它们的硬件仍然落在某个房间，但服务的是整座园子——七个物理区域的传感器和箱子都往这里汇，再从这里长出一张脸、一块屏、一个搜索框。",
           "space": "跨区域 · 数据层跑在地堡储藏室的三机机架上 · 实体设备在木屋 / 地堡 / 阁楼之间移动 · 材质规则覆盖全屋", "plans": ["site"],
           "plan_note": "场地总图。虚拟空间没有自己的一块地：数字孪生和中枢覆盖图上所有区域，miniduck 靠木屋暗门下、地堡门下的通道和阁楼坡道在三个空间之间走动。"},
}

STATUS = {
    "✅": {"0201", "0202", "0601", "0602", "0603"},
    "🚧": {"0103", "0209", "0801"},
}
def real_status(mid):
    if mid.startswith("07"): return ("设想", "真实项目尚未拆解此区域")
    if mid in ("0801", "0804", "0307"): return ("🚧", "真实项目需求收集中")
    if mid == "0805": return ("🚧", "真实方案推演中：铝型材已定标")
    for k, s in STATUS.items():
        if mid in s: return (k, {"✅": "真实三阶段已完成", "🚧": "真实设计进行中"}[k])
    return ("⬜", "真实项目待设计")

def inline_svg(svg, cls=""):
    """strip xml header, force responsive sizing"""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg)
    svg = re.sub(r'\swidth="\d+"\sheight="\d+"', "", svg, count=1)
    return svg.replace("<svg ", f'<svg class="{cls}" role="img" ', 1)

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
PLANS = [("site", "场地总图", "上北下南。东南角一户 + 整个阁楼层是自己的；庭院往南依次是 2m 过道、6m 缓坡、10m 宽的河，钓台在缓坡临河端；草地是东侧 5.3×18.9m 的长条。"),
         ("floor1", "一层平面", "六户各带独立厨卫，只有东南角这户可用。地堡完全无窗，卫生间即 0202 灯箱；南侧梁底 2400，梁北缘就是地堡与木屋的分界线。"),
         ("attic", "阁楼层", "45° 四坡屋面，中间最高 2060。虚线框内为可站立核心区（外轮廓内缩 2060，约 82㎡，占整层 47%）；帐篷与工具台都在核心区内。"),
         ("bunker-cabin", "地堡与木屋家具平面", "地堡 4.85×5.00，木屋 2.00×5.00。两张床都架空：地堡架子床下是 0209 藏宝阁，木屋梯子床下是写字台与通往地堡的暗门。"),
         ("northwall", "木屋北墙立面", "5000×2660，自室内向北看。吧台矮柜 900 高、台面电器顶 1500，上方从西到东是 0103 电子画框墙、0104 照片墙、0102 作品展示墙，0101 主产品展示在 0102 正下方。")]
plans = {k: {"id": k, "name": n, "note": t, "svg": (ROOT / "illos" / f"plan-{k}.svg").read_text(encoding="utf-8")} for k, n, t in PLANS}
for a in AREAS.values(): a["plan_figs"] = [plans[k] for k in a["plans"]]
SIZE_TABLE = [("01 暖村木屋", "2.00 × 5.00m", "10.0㎡", "2660（梁下 2400）"),
              ("02 地堡（含卫生间、储藏室）", "4.85 × 5.00m", "24.3㎡", "2660 · 无窗"),
              ("03 阁楼间", "≈7.5 × 5.35m（带缺口）", "34.5㎡ / 可站立 24.1㎡", "最高 2060 · 均 1830"),
              ("0401 过道", "≈3.5 × 3.2m", "11.2㎡ 全可站", "2060"),
              ("0402 材料仓库", "≈7.5 × 3.3m", "24.8㎡ / 可站立 6.7㎡", "0 → 2060 渐变"),
              ("0404 木工间", "≈5.1 × 10.6m", "54.1㎡ / 可站立 26.0㎡", "0 → 2060 渐变"),
              ("成品暂存", "≈5.1 × 3.25m", "16.6㎡ / 可站立 3.6㎡", "低矮为主"),
              ("05 庭院", "≈5.1 × 4.35m", "22.2㎡", "露天"),
              ("06 草地", "5.3 × 18.9m", "100㎡", "露天"),
              ("07 钓台", "≈2.5 × 2.2m", "≈5.5㎡", "露天"),
              ("天窗", "≈800 × 900", "—", "可开启")]
BLOCKS = [("0601~0603 草地面积翻倍", "已完成方案按 50㎡ 设计，实测 100㎡ 且是 5.3×18.9m 长条，管网/水泵/雨水罐/植物配置退回 🚧 重做。设想版按长条重写。"),
          ("0201 可用净高 2660 → 2400", "滑轨贴梁固定在梁内侧天花板上，梁底就是轨道净高上限；灯具吊挂高度、光斑落点、云台俯仰行程都按 2400 重算。"),
          ("阁楼楼板承重未核算", "台锯、平刨、压刨合计 250~400kg，材料仓库满载可能上吨；核算前重型设备只停在选型阶段。设想版画出来的重家伙都带这个前提。"),
          ("木屋明火与睡眠同室", "0106 炉区 40×40 在西南角，距南墙 150、距写字台 400；一氧化碳报警器必装，烟囱穿墙是必须找工人的工序。")]
for i, m in enumerate(modules):
    m["prev"] = modules[i-1] if i > 0 else None
    m["next"] = modules[i+1] if i < len(modules)-1 else None
    m["linked"] = [by_id[x] for x in m["links"] if x in by_id]
from urllib.parse import quote
refs_by_id = {}
for f in sorted(glob.glob(str(ROOT / "data" / "refs-*.json"))):
    for r in json.load(open(f, encoding="utf-8")): refs_by_id[r["id"]] = r
from ghdiag import render as _gh_render
def _paras(t):
    t = (t or "").strip()
    if "\n" in t: return [x.strip() for x in t.split("\n") if x.strip()]
    # 没有换行时按句号粗分成 3 段
    sents = [x for x in re.split(r"(?<=[。！？])", t) if x.strip()]
    if len(sents) < 4: return [t]
    k = (len(sents) + 2) // 3
    return ["".join(sents[i:i+k]) for i in range(0, len(sents), k)]
for m in modules:
    r = refs_by_id.get(m["id"], {"github": [], "xhs": []})
    m["github"] = r["github"]
    m["github_core"] = [g for g in m["github"] if not g.get("ext")]
    m["github_ext"] = [g for g in m["github"] if g.get("ext")]
    for k, g in enumerate(m["github"], 1):
        g["intro_paras"] = _paras(g.get("intro", ""))
        g["diagram_inline"] = inline_svg(_gh_render(f"g{m['id']}-{k}", g["diagram"], g["name"], seed=(int(m["id"]) + k) % 97), "pc-art gh-diag") if g.get("diagram") else None
    m["xhs"] = [{**x, "url": "https://www.xiaohongshu.com/search_result?keyword=" + quote(x["keyword"]) + "&source=web_explore_feed"} for x in r["xhs"]]
preface = json.load(open(ROOT / "data" / "preface.json", encoding="utf-8"))
preface["svg"] = (ROOT / "illos" / "preface-doors.svg").read_text(encoding="utf-8")
parts_by_id = {}
for f in sorted(glob.glob(str(ROOT / "data" / "parts-*.json"))):
    for r in json.load(open(f, encoding="utf-8")): parts_by_id[r["id"]] = r["parts"]
for m in modules:
    m["parts"] = sorted(parts_by_id.get(m["id"], []), key=lambda p: p["k"])
    for p in m["parts"]:
        p["img"] = (ROOT / "parts" / f"{m['id']}-{p['k']}.svg").read_text(encoding="utf-8")
        p["poster"] = (ROOT / "parts" / f"{m['id']}-{p['k']}-poster.svg").read_text(encoding="utf-8") if p["kind"] == "logic" else None
parts_stats = {"total": sum(len(m["parts"]) for m in modules),
               "hw": sum(1 for m in modules for p in m["parts"] if p["kind"] == "hw"),
               "logic": sum(1 for m in modules for p in m["parts"] if p["kind"] == "logic")}
repo_index = {}
for m in modules:
    for g in m["github"]:
        e = repo_index.setdefault(g["name"], {**g, "used_by": [], "entries": []})
        e["used_by"].append(m)
        e["entries"].append((m, g))
for e in repo_index.values():
    # 索引页的 500 字介绍：通用段落取第一条（最长的那条），“在本模块里怎么用”一段按模块各列一条
    base = max(e["entries"], key=lambda t: len(t[1].get("intro", "")))[1]
    paras = _paras(base.get("intro", ""))
    if len(e["entries"]) == 1 or len(paras) < 2:
        e["intro_generic"], e["intro_by_module"] = paras, []
    else:
        e["intro_generic"] = paras[:-1]
        e["intro_by_module"] = [(m, _paras(g.get("intro", ""))[-1]) for m, g in e["entries"] if g.get("intro")]
repo_list = sorted(repo_index.values(), key=lambda e: -float(e["stars"].lower().replace("k", "e3").replace(",", "")) if e["stars"][:1].isdigit() else 0)
refs_stats = {"repos": len(repo_index), "links": sum(len(m["github"]) for m in modules), "xhs": sum(len(m["xhs"]) for m in modules),
              "zh": sum(1 for e in repo_list if "无" not in (e.get("zh") or "无")),
              "multi": sum(1 for e in repo_list if len(e["used_by"]) > 1),
              "ext": sum(1 for e in repo_list if all(g.get("ext") for _, g in e["entries"]))}
for e in repo_list: e["ext_only"] = all(g.get("ext") for _, g in e["entries"])
def _starsn(e):
    s = e["stars"].lower().replace(",", "")
    return float(s.replace("k", "e3")) if s[:1].isdigit() else 0
for e in repo_list: e["area_ids"] = sorted({m["id"][:2] for m in e["used_by"]})
repo_core = [e for e in repo_list if not e["ext_only"]]
repo_ext = [e for e in repo_list if e["ext_only"]]
TIER_NOTES = [
    ("t1", "万星以上", 10000, 10 ** 9, "成熟平台级项目，社区大、文档全，出问题一搜就有答案"),
    ("t2", "1k ～ 10k 星", 1000, 10000, "细分领域里的主流方案，大多有活跃维护者和现成的接入示例"),
    ("t3", "1k 星以下", 0, 1000, "小而专的项目：恰好是这个需求的现成答案，用之前先看最近一次提交"),
]
def _tiers(lst):
    return [{"key": k, "name": n, "note": note, "repos": [e for e in lst if lo <= _starsn(e) < hi]}
            for k, n, lo, hi, note in TIER_NOTES]
def _pstats(lst):
    return {"repos": len(lst),
            "zh": sum(1 for e in lst if "无" not in (e.get("zh") or "无")),
            "multi": sum(1 for e in lst if len(e["used_by"]) > 1),
            "links": sum(len(e["entries"]) for e in lst),
            "mods": len({m["id"] for e in lst for m in e["used_by"]})}
repo_tiers = _tiers(repo_list)
REFS_PAGES = [
    {"key": "core", "file": "refs.html", "title": "参考索引 · 专门方案", "tab": "专门方案",
     "kicker": "全站引用 · 一", "h1": "{n} 个模块专门方案",
     "lede": "每个模块页“GitHub 上的成熟方案”那一栏引用的项目，去重后按星数分三档：都是直接为这个模块选的方案——硬件设计、固件、HomeAssistant 集成、管理软件。挑选时先看知名度（星数），同档次里有中文的优先；每个仓库都在 2026-09 打开核实过存在，星数取当时页面显示值，绿色标签表示有中文（官方中文 README / 中文文档站 / 界面有中文）。每个项目下面是约 500 字的介绍，被多个模块共用的会按模块各列一段“在这里怎么用”；铅笔示意图在各模块页——点右侧模块编号过去看。和模块关系没那么直接、纯为了学一遍的经典项目在另一页。",
     "repos": repo_core},
    {"key": "ext", "file": "refs-ext.html", "title": "参考索引 · 延伸阅读", "tab": "延伸阅读",
     "kicker": "全站引用 · 二", "h1": "{n} 个延伸阅读项目",
     "lede": "借这座房子的每个模块当由头，顺手把 GitHub 上的好项目好思路过一遍。这一页的项目和所在模块的关系没有上一页那么直接——有的是同一件事的另一条技术路线，有的是另一个领域里做得最好的那个——但每条介绍的最后一段都写了在那个模块里能怎么用。选择标准和上一页一样：先看知名度，同档次里有中文的优先，每个仓库都在 2026-09 打开核实过存在。它们在模块页里排在“延伸阅读”小节，用虚线卡片和正式方案分开。",
     "repos": repo_ext},
]
for p in REFS_PAGES:
    p["stats"] = _pstats(p["repos"])
    p["tiers"] = _tiers(p["repos"])
    p["h1"] = p["h1"].format(n=p["stats"]["repos"])
for i, p in enumerate(REFS_PAGES): p["other"] = REFS_PAGES[1 - i]
all_tags = {}
for m in modules:
    for t in m["tags"]: all_tags[t] = all_tags.get(t, 0) + 1
top_tags = [t for t, c in sorted(all_tags.items(), key=lambda x: -x[1]) if c >= 3][:18]
stats = {"areas": len(AREAS), "modules": len(modules),
         "done": sum(1 for m in modules if m["status"] == "✅"),
         "wip": sum(1 for m in modules if m["status"] == "🚧")}

# ---------- templates ----------
BASE = r"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% block title %}{% endblock %} · SurviveOs 设想版</title>
<meta name="description" content="{% block desc %}SurviveOs 乡野生存系统的完整形态设想：{{ stats.areas }} 个区域、{{ stats.modules }} 个模块专题，黑白钢笔速写插图。{% endblock %}">
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
    <a href="{{ root }}preface.html" class="pref {% if page == 'preface' %}on{% endif %}">序</a>
    {% for a in areas.values() %}<a href="{{ root }}areas/{{ a.id }}.html" {% if area and area.id == a.id %}class="on"{% endif %}><i>{{ a.id }}</i>{{ a.name }}</a>{% endfor %}
    <a href="{{ root }}space.html" class="about {% if page == 'space' %}on{% endif %}">户型图</a>
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
    <p class="lede">杭州乡下的一栋木屋、一个地堡、一层阁楼、一片草地、一座钓台，再加一层看不见的虚拟空间。真实项目还在一个模块一个模块地做；这个站先把 <b>{{ stats.modules }} 个模块全部想完</b>——每个模块一页专题，小红书式的放飞文案，配一张黑白钢笔速写；再往下拆成 {{ parts_stats.total }} 个核心产品模块与联动逻辑，每个都有铅笔画的爆炸图或流程图。</p>
    <div class="stats">
      <div><b>{{ stats.areas }}</b><span>个区域</span></div>
      <div><b>{{ stats.modules }}</b><span>个模块专题</span></div>
      <div><b>{{ stats.done }}</b><span>个真实已完成</span></div>
      <div><b>{{ parts_stats.total }}</b><span>个核心拆解</span></div>
    </div>
    <p class="stamp-row"><span class="stamp">设想版 · 非真实进度</span><span class="hand">看看就好，别当施工图 ↗</span></p>
    <a class="pref-entry" href="preface.html"><span class="pref-mark">序</span><span><b>{{ preface.title }}</b><small>这座园子为什么存在——三千字的代序</small></span><span class="arrow">→</span></a>
    <a class="pref-entry space-entry" href="space.html"><span class="pref-mark">📐</span><span><b>户型图与空间标注</b><small>五张铅笔底图：谁的地、多大、多高——所有模块的位置都从这里来</small></span><span class="arrow">→</span></a>
  </div>
  <figure class="hero-art">{{ areas['01'].svg_inline|safe }}<figcaption>01 暖村木屋 · 区域速写</figcaption></figure>
</section>

<section class="sec">
  <h2 class="sec-title"><span>{{ stats.areas }} 个区域</span><small>从屋里到水边，再到看不见的那一层，按编号走一圈</small></h2>
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
    <p class="space-line"><em>📐</em> {{ area.space }} <a href="{{ root }}space.html">· 看户型图 →</a></p>
  </div>
</section>
<section class="sec plan-sec">
  <h2 class="sec-title"><span>这块地长什么样</span><small>按 0008 户型图与空间标注重绘（铅笔版），位置和尺寸以它为准</small></h2>
  <div class="plan-grid plan-{{ area.plan_figs|length }}">
  {% for f in area.plan_figs %}<figure class="plan-fig"><div class="pc-frame">{{ f.svg_inline|safe }}</div><figcaption><b>{{ f.name }}</b> {{ f.note }}</figcaption></figure>{% endfor %}
  </div>
  <p class="tiny">{{ area.plan_note }}</p>
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

  {% if m.place %}<section class="blk place"><h2><em>📐</em> 它在哪、有多大</h2><p>{{ m.place }}</p><p class="tiny">位置与尺寸依据 0008 户型图与空间标注 v1；≈ 为按图面比例预估、未实测。<a href="{{ root }}space.html">看户型图 →</a></p></section>{% endif %}

  <section class="blk"><h2><em>🎬</em> 沉浸式想象</h2><p class="scene">{{ m.scene }}</p></section>

  <section class="blk"><h2><em>✅</em> 设想方案清单</h2>
    <ol class="plan">{% for p in m.plan %}<li><span class="box"></span><span>{{ p }}</span></li>{% endfor %}</ol></section>

  {% if m.parts %}<section class="blk"><h2><em>🧩</em> 核心拆解</h2>
    <p class="tiny">{{ m.parts|length }} 个核心产品模块 / 联动逻辑，每个都有铅笔画风格的爆炸拆解图或逻辑流程图 + 海报。</p>
    <div class="td-list">{% for p in m.parts %}
      <a class="td-item" href="{{ root }}teardown/{{ m.id }}.html#p{{ p.k }}">
        <span class="kind kind-{{ p.kind }}">{{ '产品模块' if p.kind == 'hw' else '联动逻辑' }}</span>
        <b>{{ p.k }}. {{ p.name }}</b>
        <span class="td-brief">{{ p.intro[:52] }}…</span>
      </a>{% endfor %}
    </div>
    <p class="td-cta"><a class="btn" href="{{ root }}teardown/{{ m.id }}.html">看完整拆解：爆炸图 / 流程图 / 海报 →</a></p>
  </section>{% endif %}

  <div class="two">
    <section class="blk"><h2><em>🔥</em> 小红书灵感点</h2><ul class="inspo">{% for p in m.inspo %}<li>{{ p }}</li>{% endfor %}</ul></section>
    <section class="blk"><h2><em>⚠️</em> 避坑提醒</h2><ul class="pit">{% for p in m.pitfalls %}<li>{{ p }}</li>{% endfor %}</ul></section>
  </div>

  <section class="blk budget"><h2><em>💰</em> 预算幻想</h2><p>{{ m.budget }}</p><p class="tiny">纯拍脑袋的量级感，真实选型以各模块的设备电商选型阶段为准。</p></section>

  {% if m.github %}<section class="blk"><h2><em>🔧</em> GitHub 上的成熟方案</h2>
    <p class="tiny">按知名度（星数）优先、有中文版优先挑的开源项目，每个都在 2026-09 打开核实过存在。每个方案配一段科普介绍和一张铅笔风的“它怎么工作 + 怎么接进本模块”示意图。</p>
    <div class="gh-cards">{% for g in m.github_core %}
      <article class="gh-card{% if g.ext %} gh-ext{% endif %}" id="gh{{ loop.index }}">
        <header class="gh-head">
          <a class="gh-name" href="{{ g.url }}" target="_blank" rel="noopener">{{ g.name }}</a>
          <span class="stars">★ {{ g.stars }}</span>
          {% if g.zh %}<span class="zh {% if '无' in g.zh %}zh-no{% endif %}">{{ g.zh }}</span>{% endif %}
          {% if g.ext %}<span class="ext-tag">延伸</span>{% endif %}
        </header>
        <p class="gh-desc">{{ g.desc }}</p>
        <p class="gh-why">→ {{ g.why }}</p>
        {% if g.diagram_inline %}<figure class="gh-art"><div class="pc-frame">{{ g.diagram_inline|safe }}</div></figure>{% endif %}
        {% if g.intro %}<div class="gh-intro">{% for para in g.intro_paras %}<p>{{ para }}</p>{% endfor %}</div>{% endif %}
      </article>{% endfor %}
    </div>
    {% if m.github_ext %}<h3 class="gh-ext-h"><span>延伸阅读</span> 借这个模块顺手学一遍的热门项目</h3>
    <p class="tiny">和本模块的关系没上面那么直接，但都是 GitHub 上值得整个看一遍的经典项目；每条最后一段写了在这里能怎么用。</p>
    <div class="gh-cards">{% for g in m.github_ext %}
      <article class="gh-card{% if g.ext %} gh-ext{% endif %}" id="ghx{{ loop.index }}">
        <header class="gh-head">
          <a class="gh-name" href="{{ g.url }}" target="_blank" rel="noopener">{{ g.name }}</a>
          <span class="stars">★ {{ g.stars }}</span>
          {% if g.zh %}<span class="zh {% if '无' in g.zh %}zh-no{% endif %}">{{ g.zh }}</span>{% endif %}
          {% if g.ext %}<span class="ext-tag">延伸</span>{% endif %}
        </header>
        <p class="gh-desc">{{ g.desc }}</p>
        <p class="gh-why">→ {{ g.why }}</p>
        {% if g.diagram_inline %}<figure class="gh-art"><div class="pc-frame">{{ g.diagram_inline|safe }}</div></figure>{% endif %}
        {% if g.intro %}<div class="gh-intro">{% for para in g.intro_paras %}<p>{{ para }}</p>{% endfor %}</div>{% endif %}
      </article>{% endfor %}
    </div>{% endif %}</section>{% endif %}

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

SPACE = r"""{% extends "base" %}{% block title %}户型图与空间标注{% endblock %}
{% block desc %}SurviveOs 设想版的空间底图：场地总图、一层平面、阁楼层、地堡与木屋家具平面、木屋北墙立面，铅笔重绘自 0008。{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <span>户型图</span></nav>
<article class="mod space">
  <header class="mod-head">
    <p class="kicker">空间底图 · 重绘自 00-总览 / 0008 户型图与空间标注 v1（2026-09-05）</p>
    <h1>先把地量清楚，再往上做梦</h1>
    <p class="lede">设想可以天马行空，但每个模块落在哪、有多大、朝哪边，都以这五张图为准：东南角一户 + 整个阁楼层是自己的，一层其余五户是邻居；庭院往南是过道、缓坡和一条 10 米宽的河；草地在东侧，是一条 100㎡ 的长条。<span class="est">灰色斜体的数字是按图面比例预估的，还没实测。</span></p>
  </header>
  {% for f in plans.values() %}
  <section class="blk plan-blk" id="{{ f.id }}">
    <h2><em>📐</em> {{ loop.index }} · {{ f.name }}</h2>
    <figure class="plan-fig big"><div class="pc-frame">{{ f.svg_inline|safe }}</div><figcaption>{{ f.note }}</figcaption></figure>
  </section>
  {% endfor %}
  <section class="blk"><h2><em>📏</em> 关键尺寸与净高</h2>
    <div class="tbl-wrap"><table class="size-tbl"><thead><tr><th>区域 / 空间</th><th>尺寸</th><th>面积</th><th>净高</th></tr></thead>
    <tbody>{% for r in size_table %}<tr><td>{{ r[0] }}</td><td>{{ r[1] }}</td><td>{{ r[2] }}</td><td>{{ r[3] }}</td></tr>{% endfor %}</tbody></table></div>
    <p class="tiny">带 ≈ 的按图面比例预估。阁楼规则：离外墙多少米，天花板就多高；可站立区 = 外轮廓向内缩 2060mm。</p>
  </section>
  <section class="blk"><h2><em>⛔</em> 设想版也绕不过的四个硬约束</h2>
    <ul class="pit">{% for b in blocks %}<li><b>{{ b[0] }}</b>——{{ b[1] }}</li>{% endfor %}</ul>
  </section>
  <section class="blk"><h2><em>🧭</em> 按区域看</h2>
    <div class="link-grid">{% for a in areas.values() %}<a class="link-card" href="{{ root }}areas/{{ a.id }}.html"><div class="thumb">{{ a.svg_inline|safe }}</div><div><i>{{ a.id }}</i><b>{{ a.name }}</b><p>{{ a.space }}</p></div></a>{% endfor %}</div>
  </section>
</article>
{% endblock %}"""

ABOUT = r"""{% extends "base" %}{% block title %}关于这个设想版{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <span>关于</span></nav>
<article class="mod about">
  <header class="mod-head">
    <p class="kicker">模块 0901 · 设想版说明</p>
    <h1>这个站是"先把结局想完"的一次练习</h1>
    <p class="lede">真实的 SurviveOs 项目是一个模块一个模块严谨地做——方案原理推演、设备电商选型、施工。0901 反过来：不严谨、不算账、不等进度，先把 {{ stats.modules }} 个模块"做完之后的样子"一口气想完，给真实设计当参照物，也给自己一个随时能逛一圈的地方。</p>
  </header>
  <section class="blk"><h2><em>①</em> 框架是真的，内容是想的</h2>
    <p class="scene">{{ stats.areas }} 个区域和模块编号完全沿用真实项目的《0002 区域与子模块清单》（2026-09-09 新设 08 虚拟空间：0206 → 0801、0211 → 0802，新增 0803 miniduck；2026-09-14 再补 0307 CNC 雕刻机、0804 全屋存储 + 全屋智能、0805 全套方案材质总设计）。5 个真实已完成的模块（0201 模拟阳光、0202 卫生间灯箱、0601～0603 草地三件套）和 6 个进行中的模块（0103 电子画框墙、0209 藏宝阁、0801 物品数字孪生、0307 / 0804 需求收集中、0805 铝型材已定标），设想内容在真实方案基础上放飞；其余模块是纯幻想。2026-09-15 又按真实项目最近的几处变化做了一轮对齐：0305 放弃成品机改为自建 Voron 2.4、0307 从五轴退回三轴、0401 定了 WORX 20V 电池平台与三区工具墙、0101 主打改成卡片式 PSK、0209 从帐篷改成写字台密室、全屋共享主机从树莓派换成 0804 那三台机器。钓台区真实项目还没拆解，这里先替它想了 0701～0704 四个模块。每页右上角的状态章（⬜ / 🚧 / ✅ / 设想）标的是<b>真实进度</b>，不是设想进度。</p></section>
  <section class="blk"><h2><em>②</em> 文案参考了小红书的热门写法</h2>
    <p class="scene">标题带钩子、短句、口语、适量 emoji；正文固定五段：沉浸式想象 → 设想方案清单 → 小红书灵感点 → 避坑提醒 → 预算幻想。灵感点里反复出现的"适我主义""精神角落 / 精神领地 / 逃避间""痛屋""家的丰容计划""去家务化 / 动线""动手主义""和植物一起住""观鸟"等，来自小红书 2026 年度居住趋势和热门话题。</p></section>
  <section class="blk"><h2><em>③</em> 插图是统一风格的黑白钢笔速写</h2>
    <p class="scene">全站 {{ stats.modules }} 张模块速写 + {{ stats.areas }} 张区域全景都是原创的 inline SVG：只有一种墨色，阴影全部用 45° 排线，轮廓"描两遍"，线条经过轻微的扰动滤镜制造手绘感，右下角是编号签名。没有任何外部图片，页面在离线状态也能完整显示。</p></section>
  <section class="blk"><h2><em>④</em> 每页附了真实的参考链接</h2>
    <p class="scene">每个模块页下方有两块引用：“GitHub 上的成熟方案”列 3～4 个真实存在的开源项目（硬件设计、固件、HomeAssistant 集成、管理软件），选择时先看知名度（星数），同档次里有中文 README / 中文文档站 / 中文界面的优先，每个都在 2026-09 打开核实过、星数取自当时页面；下面再跟 2～5 个“延伸阅读”——和本模块关系没那么直接、但值得借这个由头整个学一遍的经典热门项目（全站去重后 200 多个，等于把 GitHub 上好项目好思路顺着这座房子过一遍）；每个项目配一段约 500 字的科普介绍（是什么、怎么工作、生态如何、在本模块里怎么接）和一张铅笔风的项目介绍图（由 ghdiag.py 从结构化描述自动画出，画的是这个项目的数据与控制走向以及和本模块的接法）；“小红书视觉参考”给 2～3 组站内搜索关键词，点开直接看热门帖的实拍效果。全站去重后的项目清单见参考索引，分成两页：<a href="{{ root }}refs.html">专门方案</a>与<a href="{{ root }}refs-ext.html">延伸阅读</a>。</p></section>
  <section class="blk"><h2><em>⑤</em> 每个模块再往下拆一层</h2>
    <p class="scene">每个模块页的“核心拆解”把它拆成 3～5 个最核心的东西，一共 {{ parts_stats.total }} 个：{{ parts_stats.hw }} 个<b>产品模块</b>（物理的总成——灯头、除湿柜、雨水罐组、洞洞板系统……）给科普式介绍和一张铅笔画<b>爆炸拆解图</b>；{{ parts_stats.logic }} 个<b>联动逻辑</b>（自动化 / 算法 / 数据流）当成“逻辑产品”做一张<b>海报</b>，再配一张与爆炸图对应的铅笔画<b>流程图</b>，并写明主要实现路径参考的是哪个 GitHub 项目，让逻辑可以顺着推演下去。</p></section>
  <section class="blk"><h2><em>⑥</em> 位置和尺寸以 0008 户型图为准</h2>
    <p class="scene">2026-09-05 真实项目做出了《0008 户型图与空间标注》：东南角一户 + 整个阁楼层是自己的，地堡 4.85×5 无窗、木屋 2×5、庭院 22㎡、草地是东侧 5.3×18.9 的长条、钓台在缓坡临河端只有 5.5㎡，阁楼是 45° 四坡顶。全站据此过了一遍：每个模块页多了一段“它在哪、有多大”，区域页嵌了铅笔重绘的户型底图（见<a href="{{ root }}space.html">户型图</a>），文案里和它打架的说法（50㎡ 方草地、池塘上的钢桩钓台、独立喷漆间、地堡开窗、木屋正中的展台、招待客人……）都改掉了，涉及空间布局的速写和拆解图按 0008 的几何重画。设想仍然放飞，但落点不再悬空。</p></section>
  <section class="blk"><h2><em>⑦</em> 怎么用它</h2>
    <ol class="plan">
      <li><span class="box"></span><span>开某个模块的真实设计对话前，先看一眼它的设想页，把"想要的感觉"带进去。</span></li>
      <li><span class="box"></span><span>自己逛一圈就能标出"这个我想要 / 这个算了"，比翻方案文档快得多。</span></li>
      <li><span class="box"></span><span>真实模块跨阶段时不需要改这个站——它就是一次性的完整形态快照，和真实进度是两条线。</span></li>
    </ol></section>
  <nav class="pager"><span></span><a class="up" href="{{ root }}index.html">回首页</a><span></span></nav>
</article>
{% endblock %}"""

PREFACE = r"""{% extends "base" %}{% block title %}序 · {{ preface.title }}{% endblock %}
{% block desc %}{{ preface.epigraph }}{% endblock %}
{% block bodyclass %}preface-page{% endblock %}
{% block body %}
<article class="preface">
  <header class="pref-head">
    <div class="pref-glyph">序</div>
    <p class="kicker">SurviveOs · 设想版 · 代序</p>
    <h1>{{ preface.title }}</h1>
    <p class="epigraph">{{ preface.epigraph }}</p>
  </header>
  <div class="pref-body">
    {% for sec in preface.sections %}
    <h2 class="pref-h"><span>{{ sec.h }}</span></h2>
    {% for p in sec.ps %}<p{% if loop.first and loop.index0 == 0 and sec == preface.sections[0] %} class="first"{% endif %}>{{ p }}</p>{% endfor %}
    {% endfor %}
  </div>
  <p class="signoff"><span class="hand">{{ preface.signoff }}</span><span class="seal">序</span></p>
  <figure class="pref-art">{{ preface.svg_inline|safe }}<figcaption>那段对话的最后一个问题：三道门进去，人藏在最里面。</figcaption></figure>
  <p class="tiny pref-src">{{ preface.source }}。</p>
  <nav class="pager"><span></span><a class="up" href="{{ root }}index.html">进入这座园子 →</a><span></span></nav>
</article>
{% endblock %}"""

TEARDOWN = r"""{% extends "base" %}{% block title %}{{ m.id }} {{ m.name }} · 核心拆解{% endblock %}
{% block desc %}{{ m.name }} 的 {{ m.parts|length }} 个核心产品模块与联动逻辑：科普介绍 + 铅笔画爆炸图 / 流程图 / 海报。{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <a href="{{ root }}areas/{{ area.id }}.html">{{ area.id }} {{ area.name }}</a> › <a href="{{ root }}modules/{{ m.id }}.html">{{ m.id }} {{ m.name }}</a> › <span>核心拆解</span></nav>
<article class="mod td">
  <header class="mod-head">
    <p class="kicker">{{ area.name }} · 模块 {{ m.id }} · 核心拆解</p>
    <h1>{{ m.name }}：{{ m.parts|length }} 个核心模块与逻辑</h1>
    <p class="lede">{{ m.tagline }}</p>
    <p class="meta"><span class="st st-{{ m.status }}">{{ m.status }} {{ m.status_note }}</span>
      <span class="tag">产品模块 {{ m.parts|selectattr('kind','equalto','hw')|list|length }}</span>
      <span class="tag">联动逻辑 {{ m.parts|selectattr('kind','equalto','logic')|list|length }}</span></p>
    <div class="td-nav">{% for p in m.parts %}<a href="#p{{ p.k }}"><i>{{ p.k }}</i>{{ p.name }}</a>{% endfor %}</div>
  </header>

  {% for p in m.parts %}
  <section class="blk part" id="p{{ p.k }}">
    <h2><span class="kind kind-{{ p.kind }}">{{ '产品模块' if p.kind == 'hw' else '联动逻辑' }}</span> {{ p.k }}. {{ p.name }}</h2>
    <p class="scene">{{ p.intro }}</p>
    {% if p.kind == 'hw' %}
    <figure class="part-art"><div class="pc-frame">{{ p.img_inline|safe }}</div><figcaption><span class="hand">爆炸拆解图 · 铅笔稿</span></figcaption></figure>
    {% else %}
    <div class="logic-art">
      <figure class="part-art poster"><div class="pc-frame">{{ p.poster_inline|safe }}</div><figcaption><span class="hand">逻辑产品海报</span></figcaption></figure>
      <figure class="part-art flow"><div class="pc-frame">{{ p.img_inline|safe }}</div><figcaption><span class="hand">逻辑流程图 · 铅笔稿（类比爆炸图）</span></figcaption></figure>
    </div>
    {% endif %}
    <div class="two">
      <div><h3>{{ '关键参数 / 组成' if p.kind == 'hw' else '触发 · 阈值 · 兜底 · 出口' }}</h3>
        <ul class="inspo">{% for x in p.points %}<li>{{ x }}</li>{% endfor %}</ul></div>
      <div>{% if p.impl %}<h3>主要实现路径</h3><p class="impl">{{ p.impl }}</p>{% endif %}
        {% if p.github %}<h3>参考项目</h3><p class="gh-chips">{% for g in p.github %}<a href="{{ g.url }}" target="_blank" rel="noopener">{{ g.name }}</a>{% endfor %}</p>{% endif %}</div>
    </div>
  </section>
  {% endfor %}

  <nav class="pager">
    {% if m.prev %}<a href="{{ root }}teardown/{{ m.prev.id }}.html">← {{ m.prev.id }} {{ m.prev.name }} 拆解</a>{% else %}<span></span>{% endif %}
    <a class="up" href="{{ root }}modules/{{ m.id }}.html">回到 {{ m.name }} 专题页</a>
    {% if m.next %}<a href="{{ root }}teardown/{{ m.next.id }}.html">{{ m.next.id }} {{ m.next.name }} 拆解 →</a>{% endif %}
  </nav>
</article>
{% endblock %}"""

REFS = r"""{% extends "base" %}{% block title %}{{ rp.title }}{% endblock %}
{% block body %}
<nav class="crumb"><a href="{{ root }}index.html">首页</a> › <a href="{{ root }}refs.html">参考索引</a> › <span>{{ rp.tab }}</span></nav>
<article class="mod about">
  <header class="mod-head">
    <p class="kicker">{{ rp.kicker }}</p>
    <h1>{{ rp.h1 }}</h1>
    <nav class="refs-tabs">{% for p in refs_pages %}<a href="{{ root }}{{ p.file }}" class="{% if p.key == rp.key %}on{% endif %}">{{ p.tab }} <i>{{ p.stats.repos }}</i></a>{% endfor %}</nav>
    <p class="lede">{{ rp.lede }}</p>
  </header>
  <section class="blk refs-sum">
    <div class="rs"><b>{{ rp.stats.repos }}</b><span>个项目</span></div>
    <div class="rs"><b>{{ rp.stats.zh }}</b><span>个有中文</span></div>
    <div class="rs"><b>{{ rp.stats.mods }}</b><span>个模块引用</span></div>
    <div class="rs"><b>{{ rp.stats.links }}</b><span>处引用</span></div>
    <nav class="rs-jump">{% for t in rp.tiers %}<a href="#{{ t.key }}">{{ t.name }} <i>{{ t.repos|length }}</i></a>{% endfor %}</nav>
  </section>
  {% for t in rp.tiers %}{% if t.repos %}
  <section class="blk repo-tier" id="{{ t.key }}">
    <h2><em>★</em> {{ t.name }} <small>{{ t.repos|length }} 个</small></h2>
    <p class="tier-note">{{ t.note }}</p>
    <div class="repo-table">{% for e in t.repos %}
      <div class="repo-row">
        <div class="rmain">
          <div class="rhead">
            <a class="rname" href="{{ e.url }}" target="_blank" rel="noopener">{{ e.name }}</a>
            <span class="stars">★ {{ e.stars }}</span>
            {% if e.zh %}<span class="zh {% if '无' in e.zh %}zh-no{% endif %}">{{ e.zh }}</span>{% endif %}
          </div>
          <p class="rdesc">{{ e.desc }}</p>
          <div class="rintro">{% for para in e.intro_generic %}<p>{{ para }}</p>{% endfor %}{% for m, para in e.intro_by_module %}<p class="rmod"><a href="{{ root }}modules/{{ m.id }}.html"><i>{{ m.id }}</i>{{ m.name }}</a>{{ para }}</p>{% endfor %}</div>
        </div>
        <div class="rused"><span class="rused-l">用在</span>{% for m in e.used_by %}<a href="{{ root }}modules/{{ m.id }}.html" title="{{ m.name }}"><i>{{ m.id }}</i>{{ m.name }}</a>{% endfor %}</div>
      </div>{% endfor %}
    </div>
  </section>{% endif %}{% endfor %}
  <nav class="pager"><span></span><a class="up" href="{{ root }}index.html">回首页</a><a href="{{ root }}{{ rp.other.file }}">{{ rp.other.tab }}（{{ rp.other.stats.repos }} 个）→</a></nav>
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
.areas-nav{display:flex;flex-wrap:wrap;gap:2px 11px;font-size:.88rem}
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
.gh-cards{display:grid;grid-template-columns:1fr;gap:18px}
.gh-card{border:1.6px solid var(--line);border-radius:200px 12px 180px 12px/12px 180px 12px 200px;padding:14px 18px 12px;background:rgba(255,255,255,.4);font-size:.9rem}
.gh-card .gh-head{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px}
.gh-name{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-weight:700;font-size:.98rem;border-bottom:1.5px solid transparent}
.gh-name:hover{border-bottom-color:var(--red)}
.zh{display:inline-block;font-size:.72rem;padding:1px 8px;border:1.3px solid #2f6b3a;color:#2f6b3a;border-radius:200px 8px 180px 8px/8px 180px 8px 200px;letter-spacing:.04em}
.zh.zh-no{border-color:var(--ink3);color:var(--ink3)}
.ext-tag{display:inline-block;font-size:.7rem;padding:1px 8px;border:1.3px dashed var(--red);color:var(--red);border-radius:200px 8px 180px 8px/8px 180px 8px 200px;letter-spacing:.08em}
.gh-ext-h{font-family:"Noto Serif SC","Songti SC",serif;font-size:1.05rem;font-weight:900;margin:26px 0 4px;display:flex;align-items:center;gap:10px}
.gh-ext-h span{font-family:"Long Cang","Kaiti SC",cursive;font-weight:400;font-size:1.3rem;color:var(--red)}
.gh-card.gh-ext{border-style:dashed;background:rgba(255,255,255,.25)}
.gh-art{margin:12px 0 6px}
.gh-art .pc-frame{padding:8px 10px 4px}
.gh-art svg{width:100%;height:auto;display:block;max-width:560px;margin:0 auto}
.gh-intro p{margin:0 0 .7em;line-height:1.75;color:var(--ink);text-indent:2em}
.gh-intro p:last-child{margin-bottom:0}
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
.refs-tabs{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 0}
.refs-tabs a{font-size:.92rem;padding:5px 18px;border:1.6px solid var(--line);border-radius:200px 12px 180px 12px/12px 180px 12px 200px;background:rgba(255,255,255,.35)}
.refs-tabs a i{margin-left:5px}
.refs-tabs a.on{background:var(--ink);color:var(--paper)}
.refs-tabs a.on i{color:var(--paper2)}
.refs-tabs a:not(.on):hover{box-shadow:3px 3px 0 var(--ink)}
.refs-sum{display:flex;flex-wrap:wrap;align-items:flex-end;gap:10px 28px;padding:14px 0 6px;border-top:1.5px solid var(--line);border-bottom:1px dotted rgba(28,28,28,.35)}
.refs-sum .rs b{font-family:"Noto Serif SC","Songti SC",serif;font-size:1.7rem;font-weight:700;margin-right:6px;line-height:1}
.refs-sum .rs span{font-size:.82rem;color:var(--ink3)}
.refs-sum .rs-jump{margin-left:auto;display:flex;gap:8px;flex-wrap:wrap}
.refs-sum .rs-jump a{font-size:.8rem;padding:3px 12px;border:1.3px solid var(--ink);border-radius:200px 10px 180px 10px/10px 180px 10px 200px}
.refs-sum .rs-jump a i{margin-left:4px}
.refs-sum .rs-jump a:hover{background:var(--ink);color:var(--paper)}
.repo-tier h2 small{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem;font-weight:400;color:var(--ink3);margin-left:8px;letter-spacing:.04em}
.repo-tier .tier-note{margin:2px 0 8px;font-size:.86rem;color:var(--ink3)}
.repo-table{display:flex;flex-direction:column}
.repo-row{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:8px 28px;align-items:start;padding:18px 0;border-bottom:1px dotted rgba(28,28,28,.35)}
.repo-row:last-child{border-bottom:none}
.repo-row .rhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px}
.repo-row .rname{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.9rem;font-weight:600;word-break:break-all;border-bottom:1.3px solid transparent}
.repo-row .rname:hover{border-bottom-color:var(--red)}
.repo-row .stars{color:var(--red);font-size:.82rem;white-space:nowrap}
.repo-row .zh{font-size:.68rem}
.repo-row .rdesc{margin:5px 0 0;color:var(--ink);font-size:.92rem;line-height:1.7;font-weight:500}
.repo-row .rintro{margin-top:6px;font-size:.86rem;line-height:1.75;color:var(--ink2)}
.repo-row .rintro p{margin:0 0 .45em;text-indent:2em}
.repo-row .rintro p:last-child{margin-bottom:0}
.repo-row .rintro p.rmod{text-indent:0;padding-left:2em;position:relative}
.repo-row .rintro p.rmod a{display:inline-block;margin-right:8px;font-size:.78rem;color:var(--ink);border:1.2px solid var(--ink3);border-radius:200px 8px 180px 8px/8px 180px 8px 200px;padding:0 8px;line-height:1.5;vertical-align:1px}
.repo-row .rintro p.rmod a i{margin-right:4px}
.repo-row .rintro p.rmod a:hover{border-color:var(--red);color:var(--red)}
.repo-row .rused{display:flex;flex-direction:column;gap:3px;padding-top:2px;position:sticky;top:12px;border-left:1px dotted rgba(28,28,28,.35);padding-left:14px}
.repo-row .rused-l{font-size:.7rem;color:var(--ink3);letter-spacing:.1em}
.repo-row .rused a{font-size:.8rem;color:var(--ink2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
.repo-row .rused a i{color:var(--ink3);margin-right:6px}
.repo-row .rused a:hover{color:var(--red)}
.repo-row .rused a:hover i{color:var(--red)}
@media (max-width:820px){.repo-row{grid-template-columns:1fr;gap:6px}.repo-row .rused{border-left:none;padding-left:0;flex-direction:row;flex-wrap:wrap;gap:4px 14px}.refs-sum .rs-jump{margin-left:0}}
.td-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px}
.td-item{display:flex;flex-direction:column;gap:4px;border:1.6px solid var(--line);border-radius:12px 200px 12px 180px/180px 12px 200px 12px;padding:10px 14px;background:rgba(255,255,255,.4);font-size:.9rem}
.td-item:hover{box-shadow:3px 3px 0 var(--ink)}
.td-item b{font-family:"Noto Serif SC",serif}
.td-brief{color:var(--ink3);font-size:.8rem;line-height:1.45}
.kind{display:inline-block;font-size:.72rem;padding:1px 8px;border:1.3px solid currentColor;border-radius:200px 8px 180px 8px/8px 180px 8px 200px;letter-spacing:.06em;align-self:flex-start;vertical-align:middle}
.kind-hw{color:#2f6b3a}.kind-logic{color:var(--red)}
.td-cta{margin:14px 0 0}
.btn{display:inline-block;padding:8px 18px;border:1.6px solid var(--ink);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;font-weight:700;background:rgba(255,255,255,.5)}
.btn:hover{background:var(--ink);color:var(--paper)}
.td-nav{display:flex;flex-wrap:wrap;gap:6px 14px;margin:14px 0 0;font-size:.85rem}
.td-nav a{border-bottom:1.5px solid transparent}.td-nav a:hover{border-bottom-color:var(--red)}
.td-nav a i{margin-right:4px}
.part h2 .kind{margin-right:6px;font-size:.7rem}
.part h3{font-size:.95rem;margin:12px 0 6px;font-weight:900}
.part-art{margin:16px 0 4px}
.pc-frame{border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;padding:10px 12px 6px;background:#f9f6ef}
.part-art figcaption{text-align:right;font-size:.85rem;color:var(--ink3);margin-top:2px}
.logic-art{display:grid;grid-template-columns:300px 1fr;gap:16px;align-items:start}
.logic-art .poster .pc-frame{padding:8px}
.impl{margin:0;color:var(--ink);line-height:1.6}
.gh-chips a{display:inline-block;margin:0 8px 6px 0;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.8rem;border:1.3px solid var(--ink3);border-radius:200px 8px 180px 8px/8px 180px 8px 200px;padding:1px 8px;color:var(--ink2)}
.gh-chips a:hover{border-color:var(--red);color:var(--red)}
.td .mod-head{padding-bottom:4px}
@media (max-width:820px){.logic-art{grid-template-columns:1fr}.logic-art .poster{max-width:360px}}
.areas-nav .pref{font-family:"Long Cang","Kaiti SC",cursive;font-size:1.25rem;color:var(--red);padding-right:6px;border-right:1.4px solid var(--ink3);margin-right:4px}
.pref-entry{display:flex;align-items:center;gap:14px;margin:22px 0 0;padding:12px 16px;border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;background:rgba(255,255,255,.45);max-width:520px;transition:transform .15s}
.pref-entry:hover{transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--ink)}
.pref-entry .pref-mark{font-family:"Long Cang","Kaiti SC",cursive;font-size:2rem;color:var(--red);line-height:1;flex:0 0 auto}
.pref-entry b{display:block;font-family:"Noto Serif SC",serif;font-weight:900}
.pref-entry small{display:block;color:var(--ink3);font-size:.82rem}
.pref-entry .arrow{margin-left:auto;color:var(--red)}
.preface{max-width:640px;margin:0 auto;padding:30px 0 20px}
.pref-head{text-align:center;padding:26px 0 10px}
.pref-glyph{font-family:"Long Cang","Kaiti SC",cursive;font-size:6rem;line-height:1;color:var(--ink);opacity:.9;margin-bottom:6px}
.pref-head h1{font-size:clamp(1.7rem,3.4vw,2.3rem);font-weight:900;letter-spacing:.04em}
.epigraph{font-family:"Long Cang","Kaiti SC",cursive;font-size:1.35rem;color:var(--red);margin:14px auto 0;max-width:560px;line-height:1.7}
.pref-body{margin-top:26px;border-top:1.6px solid var(--line);padding-top:22px}
.pref-body p{font-family:"Noto Serif SC","Songti SC",serif;font-size:1.08rem;line-height:2.05;margin:0 0 1.1em;text-indent:2em;color:var(--ink)}
.pref-body p.first::first-letter{font-size:2.6em;font-weight:900;float:left;line-height:1;margin:6px 8px 0 0;font-family:"Noto Serif SC",serif}
.pref-body p.first{text-indent:0}
.pref-h{font-family:"Long Cang","Kaiti SC",cursive;font-weight:400;font-size:1.5rem;color:var(--red);margin:30px 0 10px;display:flex;align-items:center;gap:12px}
.pref-h::before,.pref-h::after{content:"";flex:1;border-top:1px dashed rgba(28,28,28,.35)}
.pref-h span{white-space:nowrap}
.pref-h:first-child{margin-top:4px}
.signoff{display:flex;justify-content:flex-end;align-items:center;gap:14px;margin:6px 0 30px;font-size:1.2rem}
.seal{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;border:2px solid var(--red);color:var(--red);font-family:"Long Cang","Kaiti SC",cursive;font-size:1.5rem;border-radius:4px;transform:rotate(-6deg);opacity:.9}
.pref-art{margin:0;border:1.6px solid var(--line);border-radius:255px 14px 225px 14px/14px 225px 14px 255px;padding:10px 14px 4px;background:rgba(255,255,255,.4)}
.pref-art figcaption{text-align:right;font-size:.85rem;color:var(--ink3);margin-top:2px;font-family:"Long Cang","Kaiti SC",cursive;font-size:1.05rem}
.pref-src{margin-top:16px;text-align:center}
.space-line{margin-top:10px;font-size:.92rem;color:var(--ink2)}
.space-line em{font-style:normal;margin-right:4px}
.space-line a{color:var(--red);border-bottom:1.5px solid transparent}.space-line a:hover{border-bottom-color:var(--red)}
.plan-grid{display:grid;gap:18px;align-items:start}
.plan-grid.plan-2{grid-template-columns:1fr 1fr}
.plan-fig{margin:0}
.plan-fig .pc-frame{padding:10px 12px 6px}
.plan-fig svg{width:100%;height:auto;display:block;max-height:560px;margin:0 auto}
.plan-fig.big svg{max-height:720px}
.plan-fig figcaption{font-size:.85rem;color:var(--ink3);margin-top:6px;line-height:1.55}
.plan-fig figcaption b{color:var(--ink);margin-right:4px}
.space-entry .pref-mark{font-size:1.5rem}
.est{color:#8a8a8a;font-style:italic}
.blk.place p:first-of-type{font-size:1.02rem;line-height:1.75}
.tbl-wrap{overflow-x:auto}
.size-tbl{width:100%;border-collapse:collapse;font-size:.9rem;margin:6px 0 8px}
.size-tbl th,.size-tbl td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.size-tbl th{font-weight:700;border-bottom:1.6px solid var(--ink)}
.size-tbl td:nth-child(2),.size-tbl td:nth-child(3),.size-tbl td:nth-child(4){white-space:nowrap}
.plan-blk h2{margin-bottom:8px}
@media (max-width:820px){.plan-grid.plan-2{grid-template-columns:1fr}}
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

env = Environment(loader=DictLoader({"base": BASE, "index": INDEX, "area": AREA, "module": MODULE, "about": ABOUT, "refs": REFS, "teardown": TEARDOWN, "preface": PREFACE, "space": SPACE}),
                  autoescape=select_autoescape(default=True))

# ---------- build ----------
if DIST.exists(): shutil.rmtree(DIST)
(DIST / "areas").mkdir(parents=True); (DIST / "modules").mkdir(); (DIST / "teardown").mkdir()
for m in modules: m["svg_inline"] = inline_svg(m["svg"], "sk-art")
for a in AREAS.values(): a["svg_inline"] = inline_svg(a["svg"], "sk-art")
preface["svg_inline"] = inline_svg(preface["svg"], "sk-art")
for f in plans.values(): f["svg_inline"] = inline_svg(f["svg"], "pc-art plan-art")
for m in modules:
    for p in m["parts"]:
        p["img_inline"] = inline_svg(p["img"], "pc-art")
        p["poster_inline"] = inline_svg(p["poster"], "pc-poster") if p["poster"] else None
ctx = dict(areas=AREAS, modules=modules, stats=stats, top_tags=top_tags, area=None, page=None, repo_list=repo_list, repo_tiers=repo_tiers, refs_pages=REFS_PAGES, refs_stats=refs_stats, parts_stats=parts_stats, preface=preface, plans=plans, size_table=SIZE_TABLE, blocks=BLOCKS)

(DIST / "index.html").write_text(env.get_template("index").render(root="", **ctx), encoding="utf-8")
(DIST / "about.html").write_text(env.get_template("about").render(root="", **{**ctx, "page": "about"}), encoding="utf-8")
for _p in REFS_PAGES:
    (DIST / _p["file"]).write_text(env.get_template("refs").render(root="", **{**ctx, "page": "refs", "rp": _p}), encoding="utf-8")
(DIST / "preface.html").write_text(env.get_template("preface").render(root="", **{**ctx, "page": "preface"}), encoding="utf-8")
(DIST / "space.html").write_text(env.get_template("space").render(root="", **{**ctx, "page": "space"}), encoding="utf-8")
alist = list(AREAS.values())
for i, a in enumerate(alist):
    (DIST / "areas" / f"{a['id']}.html").write_text(env.get_template("area").render(
        root="../", **{**ctx, "area": a, "prev_area": alist[i-1] if i else None, "next_area": alist[i+1] if i < len(alist)-1 else None}), encoding="utf-8")
for m in modules:
    (DIST / "modules" / f"{m['id']}.html").write_text(env.get_template("module").render(
        root="../", **{**ctx, "m": m, "area": AREAS[m["area"]]}), encoding="utf-8")
    if m["parts"]:
        (DIST / "teardown" / f"{m['id']}.html").write_text(env.get_template("teardown").render(
            root="../", **{**ctx, "m": m, "area": AREAS[m["area"]]}), encoding="utf-8")
# 旧编号跳转（2026-09-09：0206→0801，0211→0802）
REDIRECTS = {"0206": "0801", "0211": "0802"}
for old, new in REDIRECTS.items():
    for sub in ("modules", "teardown"):
        (DIST / sub / f"{old}.html").write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={new}.html"><link rel="canonical" href="{SITE_URL}{sub}/{new}.html"><title>{old} 已迁至 {new}</title></head><body><p>模块 {old} 已随 08 虚拟空间设立重编号为 <a href="{new}.html">{new}</a>，正在跳转…</p></body></html>', encoding="utf-8")
(DIST / "style.css").write_text(CSS, encoding="utf-8")
(DIST / "favicon.svg").write_text(FAVICON, encoding="utf-8")
(DIST / ".nojekyll").write_text("")
# sitemap
urls = ["index.html", "preface.html", "space.html", "about.html", "refs.html", "refs-ext.html"] + [f"areas/{a}.html" for a in AREAS] + [f"modules/{m['id']}.html" for m in modules] + [f"teardown/{m['id']}.html" for m in modules if m["parts"]]
(DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{SITE_URL}{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
print(f"built {len(urls)} pages -> {DIST}")
