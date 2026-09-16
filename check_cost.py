#!/usr/bin/env python3
"""核对造价数据与生成结果是否一致。改完价格必须跑到 ALL OK。

检查四件事：
1. data/cost.json 自身：区间合法、BOM 条数 3~6、BOM 合计 = 中位、区域/分期/总计自洽
2. 46 个模块页：造价卡片里的区间、中位、年度、分期、BOM 金额都能在页面上找到
3. docs/cost.html：总计、各区域中位、每个模块的中位都出现
4. 区域页：区域合计出现
"""

import json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
cost = json.loads((ROOT / "data" / "cost.json").read_text(encoding="utf-8"))
M, META = cost["modules"], cost["meta"]
bad = []


def yuan(v):
    return f"{int(v):,}"


def need(cond, msg):
    if not cond:
        bad.append(msg)


# ---- 1. 数据自洽 ----
tot = {"low": 0, "high": 0, "mid": 0, "opex": 0}
for c, d in M.items():
    need(d["low"] <= d["mid"] <= d["high"], f"{c} 区间不合法 {d['low']}/{d['mid']}/{d['high']}")
    need(3 <= len(d["bom"]) <= 6, f"{c} BOM 条数 {len(d['bom'])} 不在 3~6")
    s = sum(b["amount"] for b in d["bom"])
    need(s == d["mid"], f"{c} BOM 合计 {s} ≠ 中位 {d['mid']}")
    for k in tot:
        tot[k] += d[k]
for k, v in tot.items():
    need(META["total"][k] == v, f"总计 {k} 对不上：meta {META['total'][k]} vs 逐项 {v}")
need(len(M) == META["modules"] == 46, f"模块数 {len(M)} 不是 46")
need(sum(len(d["bom"]) for d in M.values()) == META["bom_items"], "BOM 条目数与 meta 不符")
for a, ag in META["areas"].items():
    s = sum(M[c]["mid"] for c in M if c[:2] == a)
    need(s == ag["mid"], f"区域 {a} 中位对不上：meta {ag['mid']} vs 逐项 {s}")
for p, pg in META["phases"].items():
    s = sum(M[c]["mid"] for c in M if str(M[c]["phase"]) == p)
    need(s == pg["mid"], f"分期 {p} 中位对不上：meta {pg['mid']} vs 逐项 {s}")

# ---- 2. 模块页 ----
for c, d in M.items():
    f = DOCS / "modules" / f"{c}.html"
    need(f.exists(), f"{c} 模块页不存在")
    if not f.exists():
        continue
    h = f.read_text(encoding="utf-8")
    need(f"¥{yuan(d['low'])} ～ ¥{yuan(d['high'])}" in h, f"{c} 页面缺区间")
    need(f"中位 ¥{yuan(d['mid'])}" in h, f"{c} 页面缺中位")
    need(d["phase_name"] in h, f"{c} 页面缺分期 {d['phase_name']}")
    if d["opex"] < 0:
        need(f"年度净省 ¥{yuan(-d['opex'])}" in h, f"{c} 页面缺年度净省")
    elif d["opex"] > 0:
        need(f"年度 ¥{yuan(d['opex'])}" in h, f"{c} 页面缺年度 {d['opex']}")
    for b in d["bom"]:
        need(f"¥{yuan(b['amount'])}" in h, f"{c} 页面缺支出项金额 {b['item']} ¥{b['amount']}")

# ---- 3. 汇总页 ----
f = DOCS / "cost.html"
need(f.exists(), "cost.html 不存在")
if f.exists():
    h = f.read_text(encoding="utf-8")
    need(f"¥{yuan(META['total']['low'])} ～ ¥{yuan(META['total']['high'])}" in h, "汇总页缺总区间")
    need(f"¥{yuan(META['total']['mid'])}" in h, "汇总页缺总中位")
    need(f"¥{yuan(META['total']['opex'])}" in h, "汇总页缺年度合计")
    for a, ag in META["areas"].items():
        need(f"¥{yuan(ag['mid'])}" in h, f"汇总页缺区域 {a} 中位")
    for c, d in M.items():
        need(f"¥{yuan(d['mid'])}" in h, f"汇总页缺模块 {c} 中位")
        need(f"modules/{c}.html" in h, f"汇总页缺模块 {c} 链接")

# ---- 4. 区域页 ----
for a, ag in META["areas"].items():
    f = DOCS / "areas" / f"{a}.html"
    if not f.exists():
        bad.append(f"区域页 {a} 不存在")
        continue
    h = f.read_text(encoding="utf-8")
    need(f"中位 ¥{yuan(ag['mid'])}" in h, f"区域页 {a} 缺合计中位")

if bad:
    print(f"FAIL（{len(bad)} 项）")
    for b in bad[:40]:
        print("  -", b)
    sys.exit(1)
print(f"ALL OK：{len(M)} 个模块 / {META['bom_items']} 条支出 / 中位 ¥{yuan(META['total']['mid'])} / "
      f"年度 ¥{yuan(META['total']['opex'])}；模块页、区域页、汇总页数字一致")
