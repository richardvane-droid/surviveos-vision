# SurviveOs · 设想版（模块 0901）

一座杭州乡野生存系统 SurviveOs "做完之后的样子"：7 个区域、42 个模块专题页，小红书种草体文案 + 统一风格的黑白钢笔速写插图（原创 inline SVG，无外部图片）。

在线访问：https://richardvane-droid.github.io/surviveos-vision/

> 只在真实项目的区域/模块框架里放飞想象，不代表真实进度、不构成施工依据。

## 结构

```
data/       每个区域一个 JSON：模块文案（hook / tagline / scene / plan / inspo / pitfalls / budget / links / tags / sketch_brief）
illos/      每模块一张速写 NNNN.svg + 每区域一张全景 area-0X.svg，风格规范见 STYLE.md
build.py    生成器：data + illos -> docs/
docs/       生成出来的静态站点（GitHub Pages 从 main 分支 /docs 发布）
render.py   把若干 SVG 拼成一张 PNG 预览图，方便检查插图
data/refs-0X.json  每模块的 GitHub 成熟方案 + 小红书关键词（规范见 REFS_BRIEF.md），build.py 会合并进模块页并生成 docs/refs.html
data/parts-*.json  每模块 3~5 个核心产品模块/联动逻辑的科普文案（规范见 PARTS_BRIEF.md）
parts/      核心拆解的铅笔画：NNNN-K.svg（硬件爆炸图 / 逻辑流程图）、NNNN-K-poster.svg（逻辑产品海报），生成 docs/teardown/NNNN.html
check_parts.py  检查 parts JSON 与 SVG 是否配齐
```

## 本地重新生成

```bash
pip install jinja2
python3 build.py        # 输出到 docs/
python3 -m http.server -d docs 8000
```

改文案：编辑 `data/0X.json`；改插图：编辑 `illos/NNNN.svg`（保持 STYLE.md 第 2 节的手法）；然后重新 `python3 build.py` 并提交。
