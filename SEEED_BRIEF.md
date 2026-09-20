# 0805 器件总纲落地：全站 Seeed 生态 review（给各区域调教员）

2026-09-20 真实项目 0805《全套方案材质与器件总设计》由"材质总设计"扩名，新增**电子器件**一支，决议：

> **全屋 DIY 电子器件优先选用 Seeed Studio（深圳矽递科技）生态 —— XIAO 主控 + Grove 模块，文档基准 <https://wiki.seeedstudio.com/cn/>。**
> 允许的例外：没有 Seeed 对应品 / 上量后成本不可接受 / 强电侧 / ESPHome 不支持该芯片。
> 例外**不在设想版页面上标注**（用户 2026-09-20 决定），静默保留原选型即可。

这是跨模块默认约束，本次要把它落到 0901 设想版全站：**GitHub 方案选型 + 模块文案里写死的型号**两处都改。

## 一、可用的 Seeed 官方开源仓库（均已 2026-09-20 WebFetch 核实）

| 仓库 | 星数 | 中文 | 是什么 | 适合挂在 |
|---|---|---|---|---|
| `Seeed-Studio/OSHW-reCamera-Series` | 474 | 有中文文档 | 开源 AI 相机整机：RISC-V 1TOPS SoC + 可换传感器板/底板，自带 Node-RED 与 SenseCraft | 摄像头类（0604 / 0105 / 0803） |
| `Seeed-Studio/ModelAssistant` | 444 | 官方 README_zh-CN | SenseCraft Model Assistant：给 MCU / 单板机用的嵌入式 AI 训练与部署工具链，导出 TFLite/ONNX | 边缘识别（0604 / 0801） |
| `Seeed-Studio/wiki-documents` | 375 | 有 cn 语言版 | Seeed Wiki 本体（Docusaurus 源码），就是 0805 指定的文档基准 | 0805 器件总纲 |
| `Seeed-Studio/OPL_Kicad_Library` | 363 | 无中文 | Open Parts Library：和 Seeed 打样供应链共享的 KiCad 元件库 | 画板子（0301） |
| `Seeed-Studio/PN532` | 502 | 无中文 | PN532 NFC 读写库 | RFID / NFC（0209 / 0801） |
| `Seeed-Studio/grove.py` | 166 | 无中文 | Grove 模块的 Python 库（嵌入式 Linux / I2C） | 传感器原型（0504 / 0403 / 0402） |
| `Seeed-Studio/OSHW-XIAO-Series` | 81 | 无中文 | XIAO 全系列开源硬件资料：ESP32C3/C5/C6/S3、nRF52840、RP2040/2350、MG24 等，含引脚图与参考设计 | 任何自制板子（0306 / 0501 / 0602 / 0505） |
| `Seeed-Studio/xiao-esphome-projects` | 37 | 无中文 | XIAO + ESPHome 的官方成品工程：电能计量、土壤湿度、IoT 按钮、24GHz mmWave、MR60BHA2 生命体征 / 跌倒检测、W5500 以太网、2/6 路继电器 | ESPHome 模块（0106 / 0202 / 0203 / 0403 / 0501 / 0602 / 0703 / 0504） |

星数低的两个（OSHW-XIAO-Series 81、xiao-esphome-projects 37）**按 GH_BRIEF 第 2.4 条的例外收录**：它们是 0805 定标器件的官方一手资料，属于"恰好是这个需求的唯一现成答案"，要在 `why` 里写明这一点。

## 二、每个区域要改的模块

改**这些**模块（其余模块不动）：

- **01**：0103 电子画框墙、0105 PSK 工作台、0106 柴火炉系统
- **02**：0202 卫生间灯箱系统、0203 控温控湿、0205 生态鱼缸、0209 藏宝阁
- **03**：0301 小制作工具台、0302 户外装备区、0306 微型气象站、0307 CNC 雕刻机
- **04**：0402 材料仓库、0403 喷涂柜、0404 木工间
- **05**：0501 柴火堆墙、0504 自动种植架、0505 电摩充电桩
- **06**：0601 稀树草原环境系统、0602 自动浇灌、0603 雨水存储过滤、0604 摄像头监测微环境
- **07**：0703 钓台照明与电源
- **08**：0801 物品数字孪生、0802 全屋中枢、0803 miniduck、0805 器件总纲

## 三、GitHub 选型怎么改（`data/refs-0X.json`）

1. 给上面每个模块的 `github` 数组**开头插入一条 Seeed 条目**（从第一节的表里选最贴的那个，可跨模块复用同一个仓库）。
2. 原有条目保留。**插入后核心条目（没有 `"ext": true` 的）不得超过 4 条**——已经有 4 条的，删掉其中最弱的一条（星数最低且与本模块关系最远的那条）。
3. 新条目字段格式完全照 `GH_BRIEF.md` 第 3 节：`name / url / stars / zh / desc / why / intro / diagram`，**不带 `ext` 字段**。
   - `why` 里必须点明这是 0805 定下的全屋器件基准，以及在本模块里具体用它的哪一块。
   - `intro` 480~600 字，3~4 段，最后一段落到本模块的具体用法（接哪个传感器、跑什么固件、数据往哪走）。中文里不要英文引号。
   - `diagram` 节点 4~8 个，画"这个项目怎么工作 + 和本模块怎么接"，带 `usage`。
4. 全站去重：同一个 Seeed 仓库可以被多个模块引用（build.py 会合并成一条并列出"用在"），但**同一个模块里不要重复**。

## 四、模块文案里的型号怎么改（`data/0X.json`、`data/parts-*.json`）

把写死的通用型号换成 Seeed 的具体型号，只改器件名，**不要改句子的语气和长度风格**：

| 原文里的 | 换成 |
|---|---|
| ESP32 / ESP8266 / 单片机（做 Wi-Fi 传感节点） | XIAO ESP32C6（低功耗 + Thread/Zigbee）或 XIAO ESP32S3（要跑视觉时） |
| 带摄像头的自制节点 | XIAO ESP32S3 Sense，或整机用 reCamera |
| 温湿度 / 土壤 / 光照 / 气压等模块化传感器 | Grove 系列（写成"Grove 温湿度模块"这样） |
| 人体存在 / 跌倒检测 | 24GHz mmWave（MR60BHA2 / MR60FDA2） |
| 自制继电器板 | Grove 2 路 / 6 路继电器模块 |
| 墨水屏 | 照旧（Seeed 无强对应），不必改 |

**不要动**的地方：0804 的 NAS + 笔记本 + M1 Mac 机架方案（那是 0804 已定标的，不属于器件总纲）；强电侧（光伏逆变器、提升泵、空调、台锯等）；成品家电（98 寸电视、功放、打印机）。这些就是第一节说的"例外"，**静默保留，页面上不加任何说明**。

改完 `data/0X.json` 后，如果 `data/parts-0X*.json` 里同一个部件也写了旧型号，一并同步。

## 五、自检（每个区域做完都要跑）

```bash
python3 -c "import json;json.load(open('data/refs-0X.json'))"
python3 gh_check.py 0X          # intro 字数 / 字段 / 引号，要 ALL OK
python3 gh_render.py 0X         # 出图，Read 看有没有出框、重叠、箭头反了
python3 gh_ext_check.py         # 全站去重，不要新增重复
```

## 六、硬规则

- 不改 `build.py` / `ghdiag.py` / `mkcost.py` / `data/cost.json` / 其他区域的文件。
- 所有仓库必须核实过；星数用第一节表里的值（2026-09-20 核实）。
- 例外情况一律**不在页面上解释**，只是默默保持原样。
- 汇报时每模块一行：加了哪个 Seeed 仓库、删了哪条（如果有）、文案里改了哪几个型号。不要贴 intro 全文。
