#!/usr/bin/env python3
"""Create a transparent high-resolution IP source from a white-background reference.

The output remains an asset-generation intermediate. The final WeChat cover
still uses only inline SVG paths produced by generate_cover_ip.py.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def is_near_white(pixel: tuple[int, int, int, int]) -> bool:
    r, g, b, a = pixel
    return a >= 16 and min(r, g, b) >= 225 and max(r, g, b) - min(r, g, b) <= 22


def remove_edge_connected_near_white(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    width, height = rgba.size
    background: set[tuple[int, int]] = set()
    pending: list[tuple[int, int]] = []

    for x in range(width):
        pending.extend(((x, 0), (x, height - 1)))
    for y in range(height):
        pending.extend(((0, y), (width - 1, y)))

    while pending:
        x, y = pending.pop()
        if (x, y) in background or not is_near_white(pixels[x, y]):
            continue
        background.add((x, y))
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < width and 0 <= ny < height:
                pending.append((nx, ny))

    for x, y in background:
        r, g, b, _ = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
    return rgba


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    image = remove_edge_connected_near_white(Image.open(args.source))
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("reference has no visible IP after edge background removal")
    image.crop(bbox).save(args.output)


if __name__ == "__main__":
    main()
