#!/usr/bin/env python3
"""Shared author-prefixed artifact names."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path


SUFFIXES = {
    "methodology_report": "方法论报告.md",
    "copywriting_framework": "文案框架.md",
    "analysis_data": "分析数据.json",
    "article_features": "文章特征.csv",
    "dashboard": "方法论看板.html",
    "lark_sync": "飞书同步.json",
    "competitor_samples": "竞品标题样本.json",
}


def author_slug(root: Path) -> str:
    value = unicodedata.normalize("NFKC", root.name)
    value = re.sub(r'[/\\:*?"<>|\x00-\x1f]', " ", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return value or "博主"


def artifact_name(root: Path, key: str) -> str:
    return f"{author_slug(root)}-{SUFFIXES[key]}"


def artifact_path(root: Path, key: str) -> Path:
    return root / artifact_name(root, key)
