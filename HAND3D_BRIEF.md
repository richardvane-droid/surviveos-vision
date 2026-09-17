# 拆解图重做规范（hand3d 管线）

旧的 103 张硬件爆炸图是手码 SVG 路径，透视和比例都靠猜，效果不好。现在改成**按真实尺寸建三维模型 → 透视投影 → z-buffer 消隐 → 铅笔笔触描边 + 38° 排线 → 纸纹合成**，输出 PNG。

## 工具

- `hand3d.py`：底层。`box(size,pos)` / `cyl(r,length,axis,pos)` / `extrusion(length,axis,pos,sec)` / `Solid.moved(d)` / `fit_cam` / `render_parts` / `compose` / `sheet` / `leaders_and_nums`
- `props.py`：常用构件。`wall/floor/table/cabinet/drawer/shelf_run/pegboard/stool/bed_frame/screen/monitor/epaper/camera/sensor_box/motor/pump/tank/pipe/led_strip/solar_panel/battery_box/stove/chimney/tent/tree/pot/rack/pegs`
- `partdraw.py`：**一次调用出图**
  ```python
  from partdraw import draw
  draw("0305-1", "Voron 2.4 机架与运动系统", items, solids,
       note="一行注脚", az=-55, el=24, fov=27)
  ```
  `items` 是 `[(编号, 图例文字, 三维锚点), ...]`，编号圈的屏幕位置自动排到左右页边，引线自动连到锚点。编号用 ①②③④⑤。
  输出到 `parts3d/<模块>-<序号>.png`，1200×900。

## 建模规矩（决定图好不好看）

1. **用文案里的真实尺寸**。先读 `data/parts-*.json` 里这一件的 `name` / `intro` / `points`，尺寸、数量、材料都要对得上；`data/0X.json` 的 `place` 里有空间尺寸。单位 mm。
2. **爆炸要看得见**：各层沿一个方向拉开，间距取物体尺度的 0.4～0.8 倍，保证每个编号指的东西都露出来、不被别的零件挡住。装好的状态没人看得懂，一定要拆开。
3. **墙和地只给够用的一块**：不要建整面 3.5m 的墙，只建比装配体大一圈的一块，`wall()/floor()` 已经把 `shade=False` 设好（不排线、只做背景）。墙太大会把主体压没。
4. **相机**：`az` 是方位角、`el` 是仰角。**装配体朝哪个方向敞开，相机就放哪一侧**（例如柜门朝 -Y 开，就用 `az` 在 -90～-40 之间）。`el` 一般 18～30。`fit_cam` 会自动把整个装配体套进画面，不用手调距离。
5. **零件要能认出来**：锤子=柄+头，扳手=杆+两个口，屏幕=框+面，罐子=圆柱，管子用 `pipe()`。宁可多花两行把形状做具体，也别用一个光板方块代表复杂物件。
6. **4～5 个编号**，对应 `points` 里的要点；图例一行不超过 22 个字。
7. 注脚一行，写空间落位或关键约束（取自 `place` / `intro`）。

## 自检（必须做）

每张出图后 **Read 一下 PNG**，检查：
- 主体是否居中、有没有被裁掉或缩得太小（画面主体高度应占 45%～75%）
- 编号引线是否指到了正确的零件上（指向空白或指错件要调锚点）
- 有没有零件互相穿模、或者被墙完全挡住
- 标题/图例区（左上 0～210px）有没有被图形压住

不合格就改模型或相机再出一次。一个模块的几张图可以写在同一个脚本里（`pXXXX.py`），放仓库根目录，方便以后重跑。

## 不要做的事

- 不要改 `hand3d.py` / `props.py` / `partdraw.py` / `build.py`（缺构件就在自己的脚本里用 box/cyl 拼）
- 不要动 `data/*.json`、`parts/*.svg`（旧 SVG 暂时留着，最后统一切换）
- 不要去网上抓图：这套管线是自己建模渲染的，站点是公开仓库
