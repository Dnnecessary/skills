#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""墨青测评风 · 静态手绘圈注词生成器（作者母版逐字节复刻）。

来源：作者原文
  /Users/Petrichr/WorkBuddy/2026-11-17-06-44-58/微信文章/
  03_千问办公2.0实测：能和团队协作的Team Agent来了.html
正文「…排成了一个[网页工作台]」处的行内 SVG。原文资产已逐字节保存为
  assets/theme-assets/ink-teal-tech/component-circled-word-author.svg

关键事实（与旧版主题描述不同，务必以此为准）：
- 圈注是【静态】的，SVG 内没有任何 <animate> / <animateTransform>。
- 描边色是 #047857（深青绿），不是 #0DA77D；stroke-width=1.3，圆头圆角。
- 圈是一条【开口】的手绘椭圆 path，末端带一小段收笔尾迹（L1.3 3.5），
  不是四段贝塞尔闭合的规整椭圆，也不是 CSS border-radius:50%。
- 字形是字体转出的 path，填充 #111827（比正文深一档），与圈放在同一个
  viewBox 内；整块 SVG 作为 inline-block 插在文字流里。
- 参考词「网页工作台」：width=74 height=22，margin:0 7px（比普通词 0 1px
  大，为圈外扩留白），vertical-align:-5.7px，overflow:visible。

本脚本把这个母版结构参数化：任意词 -> 字形 path + 按词宽缩放的手绘椭圆，
圈的 x 方向随词宽缩放、y 方向保持 22px，圈心始终对准字形中心。

用法（需带 fontTools 的 venv）：
  /Users/Petrichr/venv/bin/python scripts/generate_circled_word.py 网页工作台
  /Users/Petrichr/venv/bin/python scripts/generate_circled_word.py 就是这里 注意这个 \
      --out /tmp/circled-words.html
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from glyph_to_path import load_font, glyph_layer  # noqa: E402

SKILL_ROOT = Path(__file__).resolve().parent.parent
CIRCLE_ASSET = (
    SKILL_ROOT
    / "assets/theme-assets/ink-teal-tech/component-circled-word-author.svg"
)

REF_W = 74.0            # 母版参考词「网页工作台」的 SVG 宽度
REF_ELLIPSE_CX = 39.25  # 母版椭圆包围盒 x∈[-5.5, 84] 的中心
SIZE = 15.0             # 与正文同字号
HEIGHT = 22
GLYPH_COLOR = "#111827"
CIRCLE_COLOR = "#047857"
STROKE_WIDTH = "1.3"
MARGIN = "0 9px"        # 母版 0 7px；生成器字形略宽，给圈外扩多留 2px 防压邻字
OVERSHOOT = 12.0        # 圈比词宽多出的总像素（左右各 6px），母版约 5.5~10px


def load_author_circle():
    """从逐字节保存的母版资产里取出手绘椭圆 path 的 d 与完整标签。"""
    s = CIRCLE_ASSET.read_text()
    m = re.search(r'<path d="([^"]+)" fill="none" stroke="#047857"[^>]*/?>', s)
    if not m:
        raise RuntimeError(f"母版圈注 path 未找到：{CIRCLE_ASSET}")
    return m.group(1), m.group(0)


def scale_circle_x(d, kx, tx):
    """只缩放/平移 path 的 x 坐标，保持手写笔触与 stroke-width 不失真。

    母版 path 仅用 M/Q/L 绝对命令，所有数字都是成对的 x y 坐标。
    不用 <g transform="scale()">，因为那会把 1.3px 描边在横向一起压扁。
    """
    counter = [-1]

    def repl(m):
        counter[0] += 1
        v = float(m.group(0))
        if counter[0] % 2 == 0:  # x 坐标
            v = v * kx + tx
        out = f"{v:.2f}".rstrip("0").rstrip(".")
        return out if out not in ("", "-") else "0"

    return re.sub(r"-?\d+(?:\.\d+)?", repl, d)


def build(word, size=SIZE, glyph_color=GLYPH_COLOR,
          circle_color=CIRCLE_COLOR, stroke_width=STROKE_WIDTH,
          margin=MARGIN, font_path=None):
    font, cmap, glyph_set, upm = load_font(font_path) if font_path else load_font()
    glyphs, width = glyph_layer(
        word, size, glyph_color, cmap, glyph_set, upm, opacity=False
    )
    d, _ = load_author_circle()

    # 圈左右各外扩约 6px；母版字宽 74 对应圈宽约 89.5
    kx = (width + OVERSHOOT) / 89.5
    tx = width / 2.0 - REF_ELLIPSE_CX * kx
    circle_d = scale_circle_x(d, kx, tx)

    # y 方向不缩放：字形与圈共用 22px 高；字少时圈也不会矮成一条线
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" '
        f'height="{HEIGHT}" viewBox="0 0 {width:g} {HEIGHT}" '
        f'role="img" aria-label="圈注：{word}" '
        f'style="display:inline-block;vertical-align:-5.7px;overflow:visible;'
        f'transform:scale(1);margin:{margin};">'
        f'{glyphs}'
        f'<path d="{circle_d}" fill="none" stroke="{circle_color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round"/>'
        f'</svg>'
    )
    return svg, width


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="+", help="要圈注的词，可多个")
    ap.add_argument("--size", type=float, default=SIZE, help="字号 px（默认 15）")
    ap.add_argument("--glyph-color", default=GLYPH_COLOR)
    ap.add_argument("--circle-color", default=CIRCLE_COLOR)
    ap.add_argument("--stroke-width", default=STROKE_WIDTH)
    ap.add_argument("--margin", default=MARGIN)
    ap.add_argument("--font", default=None)
    ap.add_argument("--out", help="把所有结果写入文件（默认打印到 stdout）")
    args = ap.parse_args()

    out = []
    for w in args.words:
        svg, width = build(
            w, args.size, args.glyph_color, args.circle_color,
            args.stroke_width, args.margin, args.font,
        )
        out.append(svg)
        print(f"===== {w}  (width={width:g}, height={HEIGHT}) =====", file=sys.stderr)
    payload = "\n".join(out) + "\n"
    if args.out:
        Path(args.out).write_text(payload)
        print(f"生成 {len(out)} 个圈注词 -> {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    main()
