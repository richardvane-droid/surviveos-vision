# 参考链接调研规范（给各区域调研员）

目标：给 SurviveOs 设想版网站的每个模块专题页补两块内容：
1. **GitHub 上的成熟方案**：每个模块找 **3 个左右（2~4 个）** 真实存在、相对成熟的开源项目——硬件设备设计（PCB/3D 打印件/固件）、程序（HomeAssistant 集成、ESPHome 配置、控制软件、算法）、或"整套 DIY 方案"仓库。优先：star 数多、近两年有更新、和模块用途直接相关；其次才是泛用平台（esphome/esphome、home-assistant/core 这种只在确实是核心依赖时才列，且全站别重复太多次）。
2. **小红书视觉参考**：每个模块给 **2~3 组搜索关键词**（小红书站内搜索用的中文短语，3~8 个字，例如"地下室 假窗 自然光"），每组配一句"点开看什么"（10~25 字，说明这个关键词下的热门帖能看到哪种视觉效果/做法）。不需要具体帖子链接（小红书帖子链接无法验证），网站会把关键词生成站内搜索链接。

## 必须做的验证

- 每个 GitHub 仓库 **必须用 WebFetch 打开 `https://github.com/<owner>/<repo>` 核实**：页面确实存在、不是 404、内容与你要写的说明一致；记录页面上真实的 star 数（如 "11.3k"）和一句话描述。凭记忆写的仓库名经常是错的，不核实不算完成。
- 找仓库用 WebSearch（如 `github esp32 dehumidifier home assistant`、`github aquarium controller esp32`、`github bird camera identification raspberry pi`），中英文都试；从搜索结果和 GitHub 页面里的 "Similar repositories"/README 链接顺藤摸瓜。
- 找不到 3 个直接相关的就写 2 个，宁缺毋滥；实在没有开源方案的模块（比如纯木工/纯软装）可以列 1~2 个间接相关的（例如木工计算器、切割优化、布局工具），并在 why 里说明是间接参考。

## 输出格式：写到 data/refs-0X.json（X 是区域号），JSON 数组，每模块一个对象

```json
[
  {
    "id": "0203",
    "github": [
      {"name": "owner/repo", "url": "https://github.com/owner/repo", "stars": "1.2k",
       "desc": "一句话中文说明它是什么（15~40 字）",
       "why": "对这个模块的用处（20~45 字，口语化，比如：直接拿它的 ESPHome 配置接除湿机的湿度阈值）"}
    ],
    "xhs": [
      {"keyword": "地下室 防潮 除湿机", "note": "看大家怎么把除湿机藏进柜子里、管道怎么走"}
    ]
  }
]
```

字段全部必填；纯文本，不要 Markdown；中文引号用“”，不要在字符串里出现英文双引号。写完用 `python3 -c "import json;json.load(open('data/refs-0X.json'))"` 验证 JSON 合法。
