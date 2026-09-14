"""python3 gh_check.py 0X  → 检查 refs-0X.json：intro 字数、字段齐全、双引号、diagram 节点"""
import sys, json, re
area = sys.argv[1]
ok = True
for r in json.load(open(f"data/refs-{area}.json", encoding="utf-8")):
    for k, g in enumerate(r["github"], 1):
        miss = [f for f in ("name", "url", "stars", "zh", "desc", "why", "intro", "diagram") if f not in g]
        n = len(g.get("intro", ""))
        d = g.get("diagram", {})
        probs = []
        if miss: probs.append(f"缺字段 {miss}")
        if not 450 <= n <= 650: probs.append(f"intro {n} 字")
        if '"' in g.get("intro", "") or "'" in g.get("intro", ""): probs.append("intro 含英文引号")
        if d and not (4 <= len(d.get("nodes", [])) <= 9): probs.append(f"diagram 节点 {len(d.get('nodes', []))}")
        if d and not d.get("usage"): probs.append("diagram 缺 usage")
        if probs: ok = False; print(r["id"], k, g.get("name"), "→", "; ".join(probs))
print("ALL OK" if ok else "有问题")
