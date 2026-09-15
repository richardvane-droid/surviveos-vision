# 延伸项目（ext）扩充：把索引扩到 200 个

目的：在每个模块原有 3 个“专门方案”之外，再补 2～5 个 **GitHub 上的经典热门项目**，允许和本模块关联不那么紧（“借这个模块顺便把这个好项目学一遍”），但 intro 的最后一段必须给出一个**说得通的用法**（哪怕是“如果哪天……可以用它……”）。全站去重后目标 ≥200 个。

## 规则（在 GH_BRIEF.md 之上）
- 条目格式与 GH_BRIEF.md 完全一样（name/url/stars/zh/desc/why/intro/diagram），**多加一个字段 `"ext": true`**，追加在该模块 github 数组的末尾（原有 3 条不动）。
- 候选见下表。每个都要 WebFetch `https://github.com/owner/repo` 核实：存在、星数（页面显示值）、是否还在维护、中文情况。**如果仓库不存在或已归档很久，换一个同类的知名项目**（≥1k 星优先），不要硬凑。
- **不能和全站已有的 105 个项目重复**（`python3 gh_ext_check.py` 会列出重复和缺失）。同一个新项目只能出现在一个模块里。
- intro 480～650 字、3～4 段（\n 分段）：①是什么/谁做的/解决什么；②怎么工作（架构、输入→处理→输出）；③生态、社区、中文资料；④在本模块里的用法（明确说这是“延伸”时也没关系）。中文里不要英文引号。
- diagram：画“这个项目怎么工作 + 和本模块怎么接”，节点 4～9 个，带 usage。
- 每写完一个模块就保存 refs-0X.json；最后 `python3 gh_check.py 0X` 与 `python3 gh_render.py 0X` 修到 ALL OK、图不出框。
- 不改 build.py / ghdiag.py / 其他区域文件；不动原有条目。

## 候选分配（每模块 2～5 个）
| 模块 | 候选（owner/repo）| 学习点 / 挂钩 |
|---|---|---|
| 0101 | photoprism/photoprism；mrdoob/three.js | 产品照片库；网页里转着看 PSK 的 3D 模型 |
| 0102 | AppFlowy-IO/AppFlowy；TriliumNext/Notes | 每只盒子一页“出生故事”的知识库 |
| 0103 | AUTOMATIC1111/stable-diffusion-webui；ImageMagick/ImageMagick | 本地生成画作；批量裁切/调色成画框尺寸 |
| 0104 | LibrePhotos/librephotos；ente-io/ente | 自托管相册的两条路线（AI 整理 / 端到端加密） |
| 0105 | frappe/erpnext；Part-DB/Part-DB-server | BOM 与工单；电子元件库存 |
| 0106 | br3ttb/Arduino-PID-Library；eclipse-mosquitto/mosquitto | PID 控风门；MQTT 总线本身 |
| 0107 | mealie-recipes/mealie；TandoorRecipes/recipes | 菜谱/酒谱管理 |
| 0201 | MarlinFirmware/Marlin；diyHue/diyHue | 滑轨步进运动控制；Hue 桥模拟让灯进 Hue 生态 |
| 0202 | homebridge/homebridge；music-assistant/server | 进 Apple 家庭 App；卫生间放歌 |
| 0203 | Koenkk/zigbee2mqtt；zwave-js/zwave-js-ui | 传感器无线接入的两大协议 |
| 0204 | excalidraw/excalidraw；jgraph/drawio | 画全屋系统图 |
| 0205 | opencv/opencv；micropython/micropython | 鱼的视觉识别；单片机快速原型 |
| 0207 | Radarr/Radarr；Sonarr/Sonarr；HandBrake/HandBrake | 片库自动化与转码 |
| 0208 | badaix/snapcast；navidrome/navidrome；mikebrady/shairport-sync | 多房间同步、音乐库、AirPlay |
| 0209 | usememos/memos；ankitects/anki；koreader/koreader | 名言与卡片记忆、电子书 |
| 0210 | kiwix/kiwix-tools（或 kiwix/kiwix-desktop）；meshtastic/firmware；openfoodfacts/openfoodfacts-server | 离线维基百科；无网通讯；食品数据库 |
| 0212 | google-ai-edge/mediapipe；SamR1/FitTrackee | 摄像头数动作；训练日志 |
| 0301 | platformio/platformio-core；KiCad/kicad-source-mirror | 固件工程化；画板子 |
| 0302 | organicmaps/organicmaps；OpenTracksApp/OpenTracks | 离线地图与轨迹 |
| 0303 | advplyr/audiobookshelf；kovidgoyal/calibre | 帐篷里听书看书 |
| 0304 | pvlib/pvlib-python；Louisvdw/dbus-serialbattery | 发电量预测；BMS 接 Victron 生态 |
| 0305 | Klipper3d/klipper；OctoPrint/OctoPrint；prusa3d/PrusaSlicer | 打印机固件、远程控制、切片器 |
| 0306 | weewx/weewx；merbanan/rtl_433 | 气象站软件标杆；解码 433MHz 传感器 |
| 0307 | cncjs/cncjs；vlachoudis/bCNC；bdring/FluidNC | G 代码发送器与 ESP32 CNC 固件 |
| 0401 | paperless-ngx/paperless-ngx；zxing/zxing | 工具说明书归档；条码扫描 |
| 0402 | odoo/odoo；nocodb/nocodb | ERP 库存；表格式数据库 |
| 0403 | comfyanonymous/ComfyUI；google/filament | 生成/渲染涂装效果预览（PBR 材质） |
| 0404 | Jack000/SVGnest；Jack000/Deepnest | 板材排料 |
| 0501 | 1technophile/OpenMQTTGateway；espressif/esp32-camera | BLE/433 网关；柴火墙延时摄影 |
| 0502 | danforthcenter/plantcv；imagej/ImageJ | 叶面覆盖率图像分析 |
| 0503 | inaturalist/inaturalist；hbldh/bleak | 物种识别社区；BLE 读花草传感器的库 |
| 0504 | farmOS/farmOS；FarmBot/Farmbot-Web-App | 农事记录；自动农场 |
| 0505 | steve-community/steve；teslamate-org/teslamate | OCPP 充电服务器；车辆数据 |
| 0601 | qgis/QGIS；OpenDroneMap/ODM | 草地地图与航拍建模 |
| 0602 | node-red/node-red；open-meteo/open-meteo | 可视化编排；免费天气 API |
| 0603 | influxdata/influxdb；grafana/grafana | 时序库与曲线 |
| 0604 | ultralytics/ultralytics；AlexxIT/go2rtc | YOLO 检测；视频流中转 |
| 0701 | IfcOpenShell/IfcOpenShell；OpenCPN/OpenCPN | BIM 数据；河道海图 |
| 0702 | manyfold3d/manyfold；tesseract-ocr/tesseract | 3D 模型库；小黑板 OCR |
| 0703 | OpenEMS/openems；davidusb-geek/emhass | 能源管理系统；HA 能源优化 |
| 0704 | rhasspy/piper；openai/whisper | 本地 TTS 读诗；语音笔记转文字 |
| 0801 | teableio/teable；zxing-js/library；pmndrs/react-three-fiber | 物品表格数据库；网页扫码；网页里看箱子的 3D 清单 |
| 0802 | gethomepage/homepage；Lissy93/dashy；ollama/ollama | 起始页仪表盘；本地大模型当管家 |
| 0803 | huggingface/lerobot；Hypfer/Valetudo；ggml-org/llama.cpp | 机器人学习；扫地机自主导航思路；本地推理 |
| 0804 | awesome-selfhosted/awesome-selfhosted；portainer/portainer；syncthing/syncthing；restic/restic；n8n-io/n8n | 自托管地图；容器管理；同步；备份；自动化 |
| 0805 | blender/blender；CadQuery/cadquery | 材质渲染；代码化 CAD |

（表里“若已用则换”的地方，以 `gh_ext_check.py` 输出的全站重复为准。）
