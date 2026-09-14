"""python3 gh_render.py 0X  → 把 refs-0X.json 里每个 github.diagram 渲染到 ghdiag/NNNN-K.svg，并出一张 /tmp/gh0X.png 拼图"""
import sys, json, os, subprocess
from ghdiag import render
area = sys.argv[1]
os.makedirs("ghdiag", exist_ok=True)
files = []
for r in json.load(open(f"data/refs-{area}.json", encoding="utf-8")):
    for k, g in enumerate(r["github"], 1):
        if "diagram" not in g: continue
        fn = f"ghdiag/{r['id']}-{k}.svg"
        open(fn, "w", encoding="utf-8").write(render(f"g{r['id']}-{k}", g["diagram"], g["name"], seed=(int(r["id"]) + k) % 97))
        files.append(fn)
print("rendered", len(files))
if files:
    subprocess.run(["python3", "render.py", f"/tmp/gh{area}.png"] + files)
    print(f"sheet -> /tmp/gh{area}.png")
