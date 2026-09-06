from sk import *
H = "url(#marea-04-hatch)"; HL = "url(#marea-04-hatchl)"
S = 16.2; OX, OY = 206, 46
def ob(x, y, z=0):
    return f"{OX + (x - y)*S*0.87:.1f} {OY + (x + y)*S*0.5 - z*S:.1f}"
def poly(pts, z=0, sw=1.2, fill=None):
    d = "M" + " L".join(ob(x, y, z) for x, y in pts) + " Z"
    return f'<path d="{d}" stroke-width="{sw}"' + (f' fill="{fill}" stroke="none"' if fill else '') + '/>'
def obox(x0, y0, x1, y1, z0, z1, sw=1.1, shade=True):
    a = ob(x0,y0,z1); b = ob(x1,y0,z1); c = ob(x1,y1,z1); d = ob(x0,y1,z1)
    b0 = ob(x1,y0,z0); c0 = ob(x1,y1,z0); d0 = ob(x0,y1,z0)
    s = f'<path d="M{a} L{b} L{c} L{d} Z M{d} L{d0} L{c0} L{c} M{c0} L{b0} L{b}" stroke-width="{sw}"/>'
    if shade: s += f'<path d="M{c} L{c0} L{b0} L{b} Z" fill="{H}" stroke="none"/>'
    return s

def area04():
    W, D = 12.6, 13.85
    B = []
    # 楼板外轮廓（整层）+ 檐口低矮圈排线（核心区外）
    B.append(poly([(0,0),(W,0),(W,D),(0,D)], 0, 1.8))
    core = [(2.06,2.06),(10.54,2.06),(10.54,11.79),(2.06,11.79)]
    B.append(f'<path d="{"M"+" L".join(ob(x,y) for x,y in [(0,0),(W,0),(W,D),(0,D)])} Z {"M"+" L".join(ob(x,y) for x,y in core)} Z" fill="{HL}" stroke="none" fill-rule="evenodd"/>')
    B.append(f'<path d="{"M"+" L".join(ob(x,y) for x,y in core)} Z" stroke-width="1.1" stroke-dasharray="6 3"/>')
    # 45° 坡屋面示意：四角各一条从檐口到核心区角的斜线 + 屋脊/最高点 2.06
    for (ex,ey),(cx,cy) in zip([(0,0),(W,0),(W,D),(0,D)], core):
        B.append(f'<path d="M{ob(ex,ey,0)} L{ob(cx,cy,2.06)}" stroke-width="0.6" stroke-dasharray="2 3"/>')
    B.append(f'<path d="{"M"+" L".join(ob(x,y,2.06) for x,y in core)} Z" stroke-width="0.6" stroke-dasharray="2 3"/>')
    # 分区线
    B.append(f'<path d="M{ob(0,3.3)} L{ob(7.5,3.3)} M{ob(7.5,0)} L{ob(7.5,13.85)} M{ob(4.0,3.3)} L{ob(4.0,6.5)} M{ob(0,6.5)} L{ob(7.5,6.5)} M{ob(7.5,10.6)} L{ob(12.6,10.6)} M{ob(0,11.5)} L{ob(4.0,11.5)} L{ob(4.0,10.6)} L{ob(7.5,10.6)}" stroke-width="0.9"/>')
    # 楼梯（西侧，突出楼板外）
    B.append(poly([(-1.0,3.3),(4.0,3.3),(4.0,6.5),(-1.0,6.5)], 0, 1.0))
    for i in range(1,8):
        x = -1.0 + i*0.55
        B.append(f'<path d="M{ob(x,3.4)} L{ob(x,6.4)}" stroke-width="0.5"/>')
    # 0402 北条：两排长直货架（低矮带）
    B.append(obox(0.3, 0.3, 7.2, 0.9, 0, 0.9, 1.0))
    B.append(obox(0.3, 1.3, 7.2, 1.9, 0, 1.4, 1.0))
    for x in range(1, 7):
        B.append(f'<path d="M{ob(x+0.3,0.3,0)} L{ob(x+0.3,0.3,0.9)} M{ob(x+0.3,1.3,0)} L{ob(x+0.3,1.3,1.4)}" stroke-width="0.5"/>')
    # 0404 木工间：台锯（北段）+ 工作台 + 集尘桶（坡下）
    B.append(obox(8.6, 3.0, 9.8, 4.6, 0, 0.85, 1.1))
    B.append(f'<path d="M{ob(9.2,3.2,0.85)} L{ob(9.2,4.4,0.85)}" stroke-width="0.8"/>')
    B.append(obox(8.4, 5.6, 9.6, 8.0, 0, 0.9, 1.1))
    B.append(f'<path d="M{ob(11.6,4.0,0)} a5 3 0 1 0 0.1 0" stroke-width="0.9"/><path d="M{ob(11.6,4.0,0)} l0 -14 M{ob(11.6,4.0,1.0)} a5 3 0 1 0 0.1 0" stroke-width="0.8"/>')
    B.append(obox(10.9, 6.2, 12.2, 8.2, 0, 0.6, 0.8))
    # 0403 喷涂柜 1.5×1.0 在核心区东缘南段 + 排风直管出东墙
    B.append(obox(9.04, 8.1, 10.54, 9.1, 0, 1.6, 1.3))
    B.append(f'<path d="M{ob(10.54,8.6,1.4)} L{ob(12.6,8.6,1.4)} M{ob(10.54,8.6,1.6)} L{ob(12.6,8.6,1.6)} M{ob(12.6,8.6,1.4)} L{ob(12.6,8.6,1.6)}" stroke-width="1"/>')
    B.append(f'<path d="M{ob(12.7,8.6,1.5)} l8 0 l-3 -3 M{ob(12.7,8.6,1.5)} l8 0 l-3 3" stroke-width="0.7"/>')
    # 0401 过道：工具墙（沿过道北侧）
    B.append(f'<path d="M{ob(4.2,3.35,0)} L{ob(4.2,3.35,1.8)} L{ob(7.3,3.35,1.8)} L{ob(7.3,3.35,0)}" stroke-width="1"/>')
    for i in range(6):
        B.append(f'<path d="M{ob(4.5+i*0.5,3.35,1.2)} l0 -6 M{ob(4.5+i*0.5,3.35,0.7)} l0 -5" stroke-width="0.6"/>')
    # 03 阁楼间：帐篷 2.35×2.16 + 工具台 1.88×0.84 + 天窗
    B.append(f'<path d="M{ob(1.93,6.5)} L{ob(4.28,6.5)} L{ob(4.28,8.66)} L{ob(1.93,8.66)} Z" stroke-width="0.9"/>')
    B.append(f'<path d="M{ob(1.93,6.5)} L{ob(3.1,7.58,1.5)} L{ob(4.28,6.5)} M{ob(4.28,8.66)} L{ob(3.1,7.58,1.5)} L{ob(1.93,8.66)}" stroke-width="1.1"/>')
    B.append(f'<path d="M{ob(1.93,8.66)} L{ob(3.1,7.58,1.5)} L{ob(4.28,8.66)} Z" fill="{H}" stroke="none"/>')
    B.append(obox(4.5, 6.77, 6.4, 7.6, 0, 0.75, 1.0))
    B.append(f'<path d="M{ob(5.3,9.4)} L{ob(6.1,9.4)} L{ob(6.1,10.35)} L{ob(5.3,10.35)} Z M{ob(5.3,9.4)} L{ob(6.1,10.35)} M{ob(6.1,9.4)} L{ob(5.3,10.35)}" stroke-width="0.9"/>')
    # 爬行储物：周转箱
    for (x,y) in ((8.2,11.4),(9.4,11.4),(10.6,11.4),(1.0,12.2),(2.2,12.2)):
        B.append(obox(x, y, x+0.9, y+0.7, 0, 0.5, 0.7, shade=False))
    # 人：站在过道
    fx, fy = ob(5.8, 5.2, 0).split(); B.append(figure(float(fx), float(fy), 0.55))
    body = "\n".join(B)
    def L(x,y,z,t,size=8):
        X,Y = ob(x,y,z).split(); return label(float(X), float(Y), t, size, "middle")
    labels = "\n".join([
        L(3.6, -1.2, 1.2, "0402 材料仓库 · 北条长货架", 8), L(10.2, 0.3, 2.6, "0404 木工间 · 整个东侧", 8),
        L(5.6, 4.6, 2.6, "0401 过道", 7.5), L(1.6, 8.9, 2.2, "0303 帐篷", 7.5), L(5.5, 7.0, 1.7, "0301", 7.5),
        L(8.6, 10.2, 2.2, "0403 喷涂柜 1.5×1.0", 7.5), L(13.9, 8.2, 1.9, "排风出东墙", 7), L(6.1, 10.6, 0.9, "天窗", 7),
        L(-1.6, 4.9, 0.8, "楼梯", 7.5), L(9.8, 12.7, 0.9, "成品暂存 · 爬行", 7), L(9.3, 1.9, 1.6, "台锯", 7),
        L(2.2, 10.6, 0.0, "虚线内可站立 2060", 7),
        label(200, 293, "阁楼层 · 45° 四坡顶下：越靠外墙越矮，虚线框内才能站直", 10, "middle", "#1c1c1c"),
    ])
    return illo("marea-04", body, "area-04", seed=11).replace("</svg>", labels + "\n</svg>")

if __name__ == "__main__":
    open("illos/area-04.svg", "w", encoding="utf-8").write(area04()); print("ok")
