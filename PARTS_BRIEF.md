# 核心拆解规范（给各区域"拆解员"）

目标：给每个模块补一页"核心拆解"：列出它 **3~5 个最核心的产品模块或联动逻辑**，每个都给科普式介绍 + 一张（硬件）或两张（逻辑）**铅笔画风格**的图。读者是家人朋友和未来做真实设计的自己，所以"逻辑要可推演"——主要实现路径要参考真实 GitHub 项目怎么做的，不要凭空发明。

## 1. 先读什么
- `data/0X.json` 里该模块的 plan/scene（设想内容，拆解要跟它一致）
- `data/refs-0X.json` 里该模块的 github 引用（实现路径优先沿用这些项目的做法；需要新引用时用 WebSearch/WebFetch 找并核实存在）
- `parts/_sample-exploded.svg`（硬件爆炸图标准答案）、`parts/_sample-flow.svg`（逻辑流程图标准答案）、`parts/_sample-poster.svg`（逻辑海报标准答案）——**照抄它们的手法**

## 2. 每个模块拆成 3~5 个 part，两种 kind

**hw（产品模块 / 硬件）**：一个物理的东西（灯头总成、除湿机柜、雨水罐组、洞洞板系统……）。
- 文案：`intro` 科普式介绍 100~160 字（它是什么、为什么这么设计、关键原理，像百科词条的"科普"口吻，不要小红书语气）；`points` 3~4 条关键参数/组成（每条 12~30 字）。
- 图：一张**爆炸拆解图** `parts/NNNN-K.svg`，viewBox 0 0 480 360：零件沿一条斜向细虚线"爆炸轴"拉开（4~7 个零件，最下面是底座/壳体，最上面是最外层零件），每个零件带虚线引线 + 圆圈编号，左上角标题 + 图例（编号 → 中文零件名），右下角签名 `NNNN-K`。

**logic（联动逻辑 / 程序）**：一段自动化/算法/数据流（日轨调度、先进先出提醒、来客识别、灌溉判断……）。
- 文案：`intro` 100~160 字科普式说明它解决什么、输入输出是什么、核心判断；`points` 3~4 条（触发条件 / 关键阈值 / 失败兜底 / 数据出口）；`impl` 一句 30~60 字"主要实现路径"（写清用哪个 GitHub 项目/组件的哪部分，例如"用 altmenorg/HAsmartirrigation 的蒸散量算法算日需水量，ESPHome 本地执行阀门"）。
- 图：**两张**——
  - 海报 `parts/NNNN-K-poster.svg`，viewBox 0 0 360 480 竖版：双线手绘边框、顶部小字条（左 `SURVIVEOS · LOGIC PRODUCT`，右 `NNNN · LK`）、大标题（逻辑产品名，3~6 字）、红色手写体一句话卖点、中部主视觉（用 3~4 个简笔图形 + 虚线箭头画出这段逻辑的输入→处理→输出）、一行灰色小字流程摘要、3 条带勾选圈的特性、底部"跑在：… · 数据出口：…"和"参考实现：owner/repo"、右上一枚旋转的红色"设想·逻辑"印章。
  - 流程图 `parts/NNNN-K.svg`，viewBox 0 0 480 360：胶囊=起止、圆角矩形=步骤、菱形=判断、圆柱=数据源、6~9 个节点、带箭头连线（marker）、判断分支写"是/否"、左上角标题、右下角签名。节点里的字 10.5px，两行以内。

## 3. 铅笔画风格（三张 sample 已经定死，务必一致）
- 线条灰黑 `#3d3d3d`、`stroke-opacity 0.92`，主轮廓 1.4~1.6，细节 0.6~0.9；阴影用 38° 灰排线 pattern；所有"画"的线放进 `filter="url(#pNNNN-K-pencil)"`（feTurbulence 0.045 + feDisplacementMap 1.4，照抄 sample）。
- **文字、引线、编号圈、箭头连线不加滤镜**（保持清晰可读）。字体照抄 sample 的 font-family。
- 所有 id 前缀 `pNNNN-K-`（海报用 `pNNNN-Kp-`），避免同页冲突。文件 4~14 KB。不要外部资源、不要 `<image>`、不要脚本。
- 中文字符串里不要出现英文双引号；需要引号用“”。

## 4. 输出：data/parts-0X.json（一个区域一个文件，JSON 数组）

```json
[
  {"id": "0201",
   "parts": [
     {"k": 1, "kind": "hw", "name": "模拟太阳灯头总成",
      "intro": "……100~160 字科普……",
      "points": ["COB 灯珠 300W，色温 2700~6500K 可调", "菲涅尔透镜焦距 ……", "……"],
      "github": [{"name": "owner/repo", "url": "https://github.com/owner/repo"}]},
     {"k": 2, "kind": "logic", "name": "日轨调度器",
      "intro": "……", "points": ["……"],
      "impl": "用 basnijholt/adaptive-lighting 的色温曲线 + 自写太阳高度角计算，ESPHome 本地执行",
      "github": [{"name": "basnijholt/adaptive-lighting", "url": "https://github.com/basnijholt/adaptive-lighting"}]}
   ]}
]
```
`github` 每个 part 0~2 个，必须是核实过存在的仓库（优先复用 refs-0X.json 里已核实的）。`k` 从 1 开始连续编号，图文件名用它：`parts/0201-1.svg`、`parts/0201-2.svg`、`parts/0201-2-poster.svg`。

## 5. 自检
- 每画完一个模块的图，运行 `cd /home/claude/vision && python3 render.py /tmp/pXX.png parts/NNNN-1.svg parts/NNNN-2.svg parts/NNNN-2-poster.svg …` 然后用 Read 看 PNG：文字有没有互相压住/超出框、爆炸图零件是否能看出是什么、流程图箭头是否指对、海报各区块是否对齐。不合格就改。
- `python3 -c "import json;json.load(open('data/parts-0X.json'))"` 检查 JSON；`python3 -c "import xml.dom.minidom as m,glob;[m.parse(f) for f in glob.glob('parts/0X*.svg')]"` 检查 SVG 都是合法 XML。
