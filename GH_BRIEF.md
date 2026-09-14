# GitHub 方案调教规范（给各区域"方案调教员"）

目标：把每个模块页的"GitHub 上的成熟方案"重做一遍——**优先知名度（星数），其次有没有中文版**，每个方案写一段 **约 500 字** 的介绍，并给一张铅笔风"项目介绍图 / 流程图"的数据描述（由 `ghdiag.py` 自动画）。

## 1. 先读什么
- `data/0X.json` 里该模块的 plan / scene / place（方案要服务这个设想）
- `data/refs-0X.json` 里现有的 github 条目（很多是几十星的小项目，要按下面的规则重选）
- `data/parts-0X*.json` 里该模块拆解的 `impl`（引用了哪些项目，重选后如果换掉了要同步改 impl 和 parts 的 github 字段）
- `ghdiag.py` 顶部的字段说明 + `parts/_sample-ghdiag.svg`（用 `python3 render.py /tmp/x.png parts/_sample-ghdiag.svg` 看效果）

## 2. 选方案：每模块 3 个（最多 4 个）
1. **用 WebSearch 找候选**（关键词：模块功能 + github / open source / 自托管 / ESPHome / HomeAssistant / 3D printed 等，中英文各搜一轮）。
2. **用 WebFetch 打开 `https://github.com/owner/repo` 核实**：仓库存在、当前星数（写页面显示值，如 `88k` / `2.3k` / `489`）、一句话简介、最近是否还在维护（有 2025 之后的提交/发布）。
3. **判断中文版**：README 里有中文段落，或仓库有 `README_zh*.md` / `README.zh-CN.md` / docs 里有 zh 目录，或项目本身是中文社区的（如 78/xiaozhi-esp32、HomeAssistant 中文文档站）。填 `zh` 字段："官方中文 README" / "有中文文档站" / "中文社区项目" / "无中文"。
4. **排序规则**：先按知名度（星数）排，同一档次里有中文版的优先。**每模块至少一个 ≥1k 星的项目**；小众项目（<100 星）只在没有更好选择、且它恰好就是这个需求的"唯一现成答案"时保留，并在 why 里说明。
5. 通用平台（home-assistant/core、esphome/esphome）可以被多个模块引用，但一个模块里不要三个都是通用平台——至少两个是**这个模块的专门方案**（硬件设计 / 固件 / 管理软件 / 打印件 / 算法）。

## 3. 每个方案写什么（写进 refs-0X.json 的 github 条目）
```json
{"name": "owner/repo", "url": "https://github.com/owner/repo", "stars": "2.3k", "zh": "官方中文 README",
 "desc": "一句话简介（30~60 字，沿用原字段）",
 "why": "为什么选它 / 在本模块里用它的哪一部分（40~80 字，沿用原字段）",
 "intro": "约 500 字（含标点 480~600）的科普式介绍：①它是什么、谁做的、解决什么问题；②核心工作原理 / 架构（输入→处理→输出）；③关键功能与生态（支持哪些硬件、和 HA/ESPHome 怎么接、社区规模、更新情况、中文资料情况）；④在本模块里怎么用——落到设想方案里的具体位置、要改什么、注意什么坑。分 3~4 个自然段，不要小标题、不要 Markdown、不要英文双引号（用“”）。",
 "diagram": {
   "title": "项目名 · 一句话（≤22 字）",
   "nodes": [{"id":"a","label":"两行以内\n每行 ≤9 字","kind":"sensor|device|step|core|db|screen|cloud|person|file","col":0,"row":0}, ...],
   "edges": [["a","b","可选连线文字 ≤8 字"], ["b","c","", "dash"]],
   "usage": "一行（≤40 字）：在本模块里的数据/控制走向"
 }}
```
- 图的节点 4~8 个：col 0 放输入（传感器/设备/人），col 1 放这个项目本身（`core`）及其内部件，col 2 放输出（屏/数据库/设备），col 3 放最终的人或外部系统；row 0..2。**每个项目一张图，画的是这个项目怎么工作 + 和本模块怎么接**，不是模块本身的流程。
- `stars` 保留页面显示格式；`desc`、`why`、`xhs` 字段保留原有语义，可以改写。

## 4. 输出与自检
- 直接改 `data/refs-0X.json`（用 Python json 读写，`ensure_ascii=False, indent=1`），只动 github 数组，xhs 不动。**每写完一个模块就保存一次**，不要攒到最后。
- 如果替换了原来的项目，把 `data/parts-0X*.json` 里该模块 parts 的 `github` 和 `impl` 里的旧项目名同步换成新项目（其他字段不动）。
- 自检：
  - `python3 -c "import json;json.load(open('data/refs-0X.json'))"`
  - `python3 gh_render.py 0X` 生成 `ghdiag/` 下的图并渲染 `/tmp/gh0X.png`，Read 看：节点文字不出框、箭头方向对、没有重叠；不合格改 diagram。
  - 每条 intro 字数（含标点）在 480~600 之间（`python3 gh_check.py 0X` 会列出不合格的）。
- 汇报：每模块列出最终 3 个项目（星数 / 中文情况），哪些是替换掉的、为什么；不要贴 intro 全文。

## 硬规则
- 不改 build.py / ghdiag.py / 其他区域的文件。
- 所有仓库必须 WebFetch 核实过；星数写核实当天页面显示值；不要编造仓库。
- 中文字符串里不要出现英文双引号；单引号也不要，用“”。
示例：data/refs-08.json 里 0803 的第一条（pollen-robotics/microduck）已按此规范写好，照它的格式与深度来。
