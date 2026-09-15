"""python3 gh_ext_check.py → 全站 github 条目去重统计：总数、ext 数、跨模块重复的 ext、字段/字数问题"""
import json, glob, collections
seen = collections.defaultdict(list); total = 0; ext = 0; probs = []
for f in sorted(glob.glob("data/refs-0?.json")):
    for r in json.load(open(f, encoding="utf-8")):
        for k, g in enumerate(r["github"], 1):
            total += 1; seen[g["name"].lower()].append(r["id"])
            if g.get("ext"):
                ext += 1
                n = len(g.get("intro", ""))
                if not 450 <= n <= 650: probs.append(f'{r["id"]}-{k} {g["name"]} intro {n} 字')
                if not g.get("diagram"): probs.append(f'{r["id"]}-{k} {g["name"]} 缺 diagram')
                if '"' in g.get("intro", "") or "'" in g.get("intro", ""): probs.append(f'{r["id"]}-{k} {g["name"]} 含英文引号')
uniq = len(seen)
print(f"引用 {total} 处，去重 {uniq} 个项目，其中 ext 条目 {ext} 条")
dup_ext = {n: ids for n, ids in seen.items() if len(ids) > 1}
for f in sorted(glob.glob("data/refs-0?.json")):
    for r in json.load(open(f, encoding="utf-8")):
        for g in r["github"]:
            if g.get("ext") and len(seen[g["name"].lower()]) > 1: probs.append(f'{r["id"]} ext {g["name"]} 与 {seen[g["name"].lower()]} 重复')
for p in sorted(set(probs)): print("!", p)
print("目标 200，还差", max(0, 200 - uniq))
