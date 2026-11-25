#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成墨青测评风封面「作者介绍语」的点阵飞散字组。

背景：作者母版的介绍语不是 <text>，也不是曲线字形，而是 16 列宽的
中文点阵字模：每个字拆成「上半 / 下半」两片，各自带独立的
translate（飞散轨迹）+ scale（1→.74→.16 碎裂）+ opacity（互斥）动画。
系统里没有中文点阵字库，因此本脚本用轮廓字体现场栅格化成点阵，
再按母版同构的动画骨架生成 <g>，输出到 stdout 供装配脚本注入。

用法（用带 fontTools + PIL 的 venv）：
    /Users/Petrichr/venv/bin/python generate_cover_intro.py \
        "不做岸上的看客，只做深海里的求索者" --out /tmp/intro-groups.xml

关键约束（与母版一致，勿随意改）：
- 16 列点阵；字与字等宽字位；方块填充率约 95%。
- 前半句蓝灰 #8291A5，逗号计入前半；后半句青绿 #0DA77D。
- 每字两片（逗号一片）：upper home_y / lower home_y，片内局部坐标以片中心为 0。
- 动画 8s 循环：opacity 0~15% 显示 →15~20% 淡出 →90~97% 恢复；
  scale 1→1→.74→.16 碎裂；translate 先轻微位移再飞向散布终点后复位。
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
COLS = 16                 # 点阵列数（母版固定）
ROWS = 16                 # 点阵最大行数
SQUARE_FILL = 0.95        # 方块填充率：step=S, 方块=S*SQUARE_FILL
THRESHOLD = 100           # 栅格化二值阈值

COLOR_A = "#8291A5"       # 前半蓝灰
COLOR_B = "#0DA77D"       # 后半青绿

# 关键时序（与母版逐字节一致）
DUR = "8s"
KT_MOTION = "0;.15;.19375;.24;.90;.91;.9525;1"
KS_MOTION = ("0.77 0 0.175 1;" * 7).rstrip(";")
KT_OPACITY = "0;.155;.20;.925;.97;1"
SP_OPACITY = "0.45 0 0.55 1"

# 排布（1246 宽画布；已验收为 IP 与介绍语、介绍语与右侧留白近似对称）
# 当前 16×16 点阵实际步长为 3.396875：首组中心 x=285.17，最后组中心 x=1124.83。
# 不得回退到旧的 START_X=170 / step=3.9，否则会再次造成 IP 右侧拥挤、画布右侧留白过大。
START_X = 258.0
HOME_TOP_Y = 112.0        # 整行字中心 y（原 90 偏上，用户要求整体下调；IP 中心≈118）
COMMA_SLOT_RATIO = 0.45   # 逗号字位宽度（原 1.0 会让前后半句之间空出一大块）
SCATTER_X0, SCATTER_DX = 382.0, 69.0   # 飞散终点 x 起点/步长；与居中布局同步
SCATTER_Y0, SCATTER_DY = 148.0, -7.0   # 飞散终点 y 起点/步长
SCATTER_CYCLE = 11        # 每 11 组回到起点（与母版两轮飞散同构）


def rasterize(ch, font_size=96, render_scale=6):
    """把一个字栅格化成 COLS×ROWS 的 0/1 矩阵（按墨迹居中，行从顶部）。"""
    canvas = Image.new("L", (COLS * render_scale, ROWS * render_scale), 0)
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, font_size)
    # 先量墨迹 bbox，按整格居中
    box = draw.textbbox((0, 0), ch, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    x = (canvas.width - w) // 2 - box[0]
    y = (canvas.height - h) // 2 - box[1]
    draw.text((x, y), ch, font=font, fill=255)
    small = canvas.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    grid = [[1 if small.getpixel((cx, cy)) > THRESHOLD else 0
             for cx in range(COLS)] for cy in range(ROWS)]
    # 裁到实际有墨的行，垂直居中放回 ROWS 行
    rows_with_ink = [r for r in range(ROWS) if any(grid[r])]
    if not rows_with_ink:
        return grid
    top, bottom = rows_with_ink[0], rows_with_ink[-1]
    height = bottom - top + 1
    pad = (ROWS - height) // 2
    new = [[0] * COLS for _ in range(ROWS)]
    for i, r in enumerate(range(top, bottom + 1)):
        new[pad + i] = grid[r][:]
    return new


def matrix_blocks(grid, step):
    """点阵矩阵 -> 方块 (x, y, col, row) 列表，坐标相对矩阵中心（单位=SVG 单位）。"""
    square = step * SQUARE_FILL
    blocks = []
    h = len(grid)
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v:
                x = (c - (COLS - 1) / 2.0) * step - square / 2.0
                y = (r - (h - 1) / 2.0) * step - square / 2.0
                blocks.append((x, y, square, square, c, r))
    return blocks


def path_d(blocks):
    parts = []
    for x, y, w, h, _, _ in blocks:
        parts.append(f"M{x:.3f} {y:.3f}h{w:.3f}v{h:.3f}h-{w:.3f}z")
    return "".join(parts)


def group_xml(home_x, home_y, mid_x, mid_y, end_x, end_y, color, d):
    hx, hy = f"{home_x:.2f}", f"{home_y:.2f}"
    mx, my = f"{mid_x:.2f}", f"{mid_y:.2f}"
    ex, ey = f"{end_x:.2f}", f"{end_y:.2f}"
    tvals = f"{hx} {hy};{hx} {hy};{mx} {my};{ex} {ey};{ex} {ey};{ex} {ey};{hx} {hy};{hx} {hy}"
    return (
        f'<g transform="translate({hx} {hy})">'
        f'<animateTransform attributeName="transform" type="translate" values="{tvals}" '
        f'keyTimes="{KT_MOTION}" dur="{DUR}" repeatCount="indefinite" '
        f'calcMode="spline" keySplines="{KS_MOTION}"/>'
        f'<g opacity="1">'
        f'<animate attributeName="opacity" values="1;1;0;0;1;1" '
        f'keyTimes="{KT_OPACITY}" dur="{DUR}" repeatCount="indefinite"/>'
        f'<g transform="scale(1)">'
        f'<animateTransform attributeName="transform" type="scale" '
        f'values="1;1;.74;.16;.16;.16;1;1" keyTimes="{KT_MOTION}" '
        f'dur="{DUR}" repeatCount="indefinite" calcMode="spline" keySplines="{KS_MOTION}"/>'
        f'<path d="{d}" fill="{color}"/>'
        f'</g></g>'
        f'<rect x="-3" y="-3" width="6" height="6" rx="1" fill="{color}" opacity="0">'
        f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
        f'keyTimes="0;.16;.195;.23;.265;1" dur="{DUR}" repeatCount="indefinite"/>'
        f'</rect></g>'
    )


def build(text, step):
    chars = list(text)
    # 断点：逗号计入前半
    comma = text.find("，")
    split = comma + 1 if comma >= 0 else len(chars)
    slot = step * COLS
    out = []
    gidx = 0
    cursor = START_X  # 累积排版：逗号只占 0.45 字位，后半句整体左移靠拢
    for idx, ch in enumerate(chars):
        color = COLOR_A if idx < split else COLOR_B
        width = slot * (COMMA_SLOT_RATIO if ch == "，" else 1.0)
        cx = cursor + width / 2.0
        cursor += width
        grid = rasterize(ch)
        if ch == "，":
            # 逗号：窄字位，整字坐标系下方一个 2 点小撇
            sq = step * SQUARE_FILL
            blocks = [(0 * step - sq / 2, 4 * step - sq / 2, sq, sq, 0, 0),
                      (1 * step - sq / 2, 5 * step - sq / 2, sq, sq, 0, 0)]
            out.append(group_xml(cx, HOME_TOP_Y,
                                 cx + 24, HOME_TOP_Y + 2,
                                 SCATTER_X0 + SCATTER_DX * (gidx % SCATTER_CYCLE),
                                 SCATTER_Y0 + SCATTER_DY * (gidx % SCATTER_CYCLE),
                                 color, path_d(blocks)))
            gidx += 1
            continue
        # 拆上下两片：共享「整字坐标系」才能拼回完整字（母版关键）。
        # 上下片 blocks 都按整字 ROWS×COLS 网格取坐标，home_y 相同；
        # 只靠不同的飞散终点让两片在动画中分离，首帧则严丝合缝拼成整字。
        ink_rows = [r for r in range(ROWS) if any(grid[r])]
        top_r, bot_r = ink_rows[0], ink_rows[-1]
        mid_r = (top_r + bot_r) // 2
        square = step * SQUARE_FILL
        for part, rows in (("upper", list(range(top_r, mid_r + 1))),
                           ("lower", list(range(mid_r + 1, bot_r + 1)))):
            if not rows:
                continue
            blocks = []
            for r in rows:
                for c in range(COLS):
                    if grid[r][c]:
                        # 局部坐标基于整字 16×16 中心，两片一致
                        x = (c - (COLS - 1) / 2.0) * step - square / 2.0
                        y = (r - (ROWS - 1) / 2.0) * step - square / 2.0
                        blocks.append((x, y, square, square, c, r))
            home_y = HOME_TOP_Y
            mid_x = cx + (24 if part == "upper" else 28)
            mid_y = home_y + (2 if part == "upper" else -2)
            # 上下片飞散终点镜像分叉（上片偏上、下片偏下），保留撕裂感
            slot_end = gidx // 2
            end_x = SCATTER_X0 + SCATTER_DX * (slot_end % SCATTER_CYCLE)
            end_y = (SCATTER_Y0 - 14 if part == "upper" else SCATTER_Y0 + 14) \
                + SCATTER_DY * (slot_end % SCATTER_CYCLE)
            out.append(group_xml(cx, home_y, mid_x, mid_y, end_x, end_y, color, path_d(blocks)))
            gidx += 1
    return "".join(out), gidx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("text", help="介绍语文案")
    ap.add_argument("--out", help="输出 XML 文件（默认 stdout）")
    ap.add_argument("--step", type=float, default=3.396875, help="点阵步长（默认 3.396875，匹配已验收的居中布局）")
    args = ap.parse_args()
    xml, n = build(args.text, args.step)
    if args.out:
        Path(args.out).write_text(xml)
        print(f"生成 {n} 个字组 -> {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(xml)


if __name__ == "__main__":
    main()
