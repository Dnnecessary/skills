#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把中文词按字体转成 SVG path —— 墨青测评风"词内动画"的字形层生成器。

背景：原文的词内动画是"字 -> 场景动画 -> 字"原地交叉，字形层必须是 path
（用 <text> 会触发 leaf 警告，用 position:absolute 叠加微信不支持）。
本脚本把任意词转成真实字形 path，供与场景 path 放进同一个 SVG 交叉切换。

用法（用带 fontTools 的 venv）：
    /Users/Petrichr/venv/bin/python glyph_to_path.py 天气 暴涨 钻进
    /Users/Petrichr/venv/bin/python glyph_to_path.py --size 15 --color '#374151' 天气

输出：每个词一段完整可嵌入的字形层 <g>（含原文同款 opacity 时序），
      以及该词建议的 width。把它和场景层拼进同一个 svg 即可。
"""
import argparse
import sys

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
# 字态停留要够长：原文实测到 0.14~0.26 才隐去（旧值 0.1 太短）
KT_W = "0;0.16;0.24;0.84;0.9;1"
SP = "0.45 0 0.55 1"
DEFAULT_DUR = "3.8s"  # 仅为默认；原文实测 3.6/3.8/3.9/5.6s 都有，按词传入
# 基线补偿：字体转出的字形层相对正文基线偏高约 2 个 SVG 单位（2026-11-16 截图实测：
# 正文 y=190-217 vs 动画词 y=188-214，偏上约 3px@1.87x ≈ 2 单位）。统一 +2 下移对齐。
# 注意：场景层物件也必须同步 +2（见主题库/装配脚本），否则字与场景错位。
BASELINE_DY = 2.0


def load_font(path=FONT):
    from fontTools.ttLib import TTCollection, TTFont
    if path.lower().endswith(".ttc"):
        font = TTCollection(path).fonts[0]
    else:
        font = TTFont(path)
    return font, font.getBestCmap(), font.getGlyphSet(), font["head"].unitsPerEm


def word_paths(text, size, cmap, glyph_set, upm):
    """按字拆分成 [(path_d, advance_px)]，坐标未缩放（宽高单位为字体 upm）。"""
    from fontTools.pens.svgPathPen import SVGPathPen
    out = []
    for ch in text:
        gname = cmap.get(ord(ch))
        if not gname:
            out.append(("", size / 2))
            continue
        pen = SVGPathPen(glyph_set)
        glyph_set[gname].draw(pen)
        d = pen.getCommands()
        adv = glyph_set[gname].width / upm * size
        out.append((d, adv))
    return out


def glyph_layer(text, size, color, cmap, glyph_set, upm, opacity=True, dur=DEFAULT_DUR):
    """返回 (可嵌入的 <g> 字形层, 建议 width px)。dur 按词传入。"""
    ps = word_paths(text, size, cmap, glyph_set, upm)
    width = round(sum(a for _, a in ps) + 2, 1)
    scale = size / size  # 字体输出已按 upm 归一，交给 transform 缩放
    # SVGPathPen 的 d 基于 upm 坐标、y 向上；用 scale(size/upm, -size/upm) 缩放并翻正
    k = size / upm
    parts = []
    if opacity:
        sp = ";".join([SP] * 5)
        parts.append(
            f'<g><animate attributeName="opacity" values="1;1;0;0;1;1" '
            f'keyTimes="{KT_W}" calcMode="spline" keySplines="{sp}" '
            f'dur="{dur}" repeatCount="indefinite"/>'
        )
    x = 1.0
    for d, adv in ps:
        if d:
            parts.append(
                f'<g transform="translate({x:.2f} {size + BASELINE_DY}) scale({k:.6f},-{k:.6f})">'
                f'<path d="{d}" fill="{color}"/></g>'
            )
        x += adv
    if opacity:
        parts.append("</g>")
    return "".join(parts), width


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="+", help="要转成的词，可多个")
    ap.add_argument("--size", type=float, default=15, help="字号 px（默认 15）")
    ap.add_argument("--color", default="#374151", help="字形颜色（默认 #374151）")
    ap.add_argument("--font", default=FONT, help="字体文件 .ttc/.ttf")
    ap.add_argument("--no-opacity", action="store_true", help="只输出 path，不加 opacity 时序")
    ap.add_argument("--dur", default=DEFAULT_DUR, help="动画周期，如 3.8s/3.9s/5.6s（默认 3.8s）")
    args = ap.parse_args()

    try:
        font, cmap, gs, upm = load_font(args.font)
    except Exception as e:
        print(f"字体加载失败：{e}\n请确认使用带 fontTools 的 venv：/Users/Petrichr/venv/bin/python", file=sys.stderr)
        sys.exit(1)

    for w in args.words:
        g, width = glyph_layer(w, args.size, args.color, cmap, gs, upm, not args.no_opacity, args.dur)
        print(f"===== {w}  (建议 width={width}, height=22) =====")
        print(g)
        print()


if __name__ == "__main__":
    main()
