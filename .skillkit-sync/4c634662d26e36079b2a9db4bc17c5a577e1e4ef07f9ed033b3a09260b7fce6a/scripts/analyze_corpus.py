#!/usr/bin/env python3
"""Extract documents and build reproducible article-level analysis data."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from artifact_names import artifact_path


SUPPORTED = {".md", ".markdown", ".txt", ".docx", ".pdf"}
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+", re.MULTILINE)
LIST_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+", re.MULTILINE)
QUOTE_RE = re.compile(r"^\s*>\s+", re.MULTILINE)
BOLD_RE = re.compile(r"(?:\*\*|__)(.+?)(?:\*\*|__)")
SENTENCE_RE = re.compile(r"[^。！？!?；;\n]+[。！？!?；;]?")
PARAGRAPH_RE = re.compile(r"\n\s*\n+")
DATE_RE = re.compile(r"(20\d{2})[-/.年](\d{1,2})[-/.月](\d{1,2})")
META_RE = re.compile(r"^-\s*([^：:]+)[：:]\s*(.+?)\s*$", re.MULTILINE)
LATIN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_+.-]{1,}")
CJK_RE = re.compile(r"[\u4e00-\u9fff]{2,}")

STOPWORDS = {
    "一个", "一种", "一些", "这个", "那个", "这些", "那些", "可以", "可能",
    "就是", "不是", "但是", "因为", "所以", "如果", "我们", "你们", "他们",
    "自己", "已经", "没有", "还有", "以及", "进行", "通过", "对于", "关于",
    "什么", "怎么", "为什么", "非常", "很多", "比较", "其实", "然后", "这里",
    "这样", "这种", "时候", "问题", "事情", "内容", "文章",
}

CTA_PATTERNS = {
    "like": re.compile(r"点赞|点个赞"),
    "favorite": re.compile(r"收藏|存下来"),
    "comment": re.compile(r"评论区|留言|评论"),
    "share": re.compile(r"转发|分享给"),
    "follow": re.compile(r"关注(?:我|公众号|账号)?"),
    "resource": re.compile(r"领取|下载|资料|回复关键词"),
    "contact": re.compile(r"加群|咨询|联系我|私信"),
    "purchase": re.compile(r"购买|下单|报名|订阅"),
}
ENDING_CTA_PATTERNS = {
    "question": re.compile(r"你(?:怎么看|怎么想|用了吗|试了吗)|感觉怎么样|有没有|是否"),
    "comment": re.compile(r"评论区|留言|反馈|告诉我"),
    "action": re.compile(r"试试|走一遍|参与|贴出来|顺手|赶快|去试"),
    "follow": re.compile(r"关注(?:我|公众号|账号)?"),
}
EVIDENCE_PATTERNS = {
    "data": re.compile(r"\d+(?:\.\d+)?%|数据显示|统计|样本"),
    "quote": re.compile(r"据.{0,20}(?:表示|称|报道)|引用|原文"),
    "authority": re.compile(r"研究|报告|论文|官方|权威"),
    "test": re.compile(r"实测|测试|亲测|实验"),
    "experience": re.compile(r"我(?:用|做|试|发现|经历)|亲身|经验"),
    "case": re.compile(r"案例|例如|比如|以.+为例"),
    "comparison": re.compile(r"相比|对比| versus | vs\.? ", re.IGNORECASE),
}
STANCE_PATTERNS = {
    "strong": re.compile(r"一定|必然|毫无疑问|显然|本质上|真正"),
    "cautious": re.compile(r"可能|也许|或许|倾向于|在一定程度上|目前来看"),
    "conditional": re.compile(r"如果|除非|前提是|取决于|只要"),
    "risk": re.compile(r"风险|谨慎|警惕|代价|问题|缺点|局限"),
}
SENSITIVE_PATTERNS = {
    "confidential_marking": re.compile(r"机密|保密|内部资料|仅限内部|不得外传"),
    "identity_number": re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)"),
    "phone_number": re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)"),
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
}


def read_document(path: Path) -> tuple[str, list[str]]:
    warnings: list[str] = []
    suffix = path.suffix.lower()
    if suffix in {".md", ".markdown", ".txt"}:
        return path.read_text(encoding="utf-8", errors="replace"), warnings
    if suffix == ".docx":
        try:
            from docx import Document
        except ImportError:
            return "", ["python-docx unavailable"]
        document = Document(path)
        return "\n\n".join(p.text for p in document.paragraphs), warnings
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError:
            return "", ["pypdf unavailable"]
        reader = PdfReader(path)
        pages = [(page.extract_text() or "") for page in reader.pages]
        text = "\n\n".join(pages).strip()
        if not text:
            warnings.append("PDF has no extractable text; OCR required")
        return text, warnings
    return "", [f"unsupported format: {suffix}"]


def strip_markdown(text: str) -> str:
    text = IMAGE_RE.sub("", text)
    text = LINK_RE.sub(r"\1", text)
    text = HEADING_RE.sub("", text)
    text = LIST_RE.sub("", text)
    text = QUOTE_RE.sub("", text)
    text = BOLD_RE.sub(r"\1", text)
    text = re.sub(r"`{1,3}", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def normalize_title(title: str) -> str:
    return re.sub(r"[\s，。！？、,.!?：:；;《》“”\"'（）()【】\[\]-]+", "", title).lower()


def extract_title(text: str, path: Path) -> str:
    heading = re.search(r"^\s*#\s+(.+?)\s*$", text, re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return path.stem


def extract_metadata(text: str) -> dict[str, str]:
    metadata = {key.strip(): value.strip() for key, value in META_RE.findall(text[:2500])}
    date = ""
    for key in ("发布时间", "日期", "publish_time"):
        if key in metadata:
            date = metadata[key]
            break
    url = ""
    for key in ("原文链接", "链接", "url"):
        if key in metadata:
            url = metadata[key]
            break
    author = ""
    for key in ("公众号", "作者", "账号", "author"):
        if key in metadata:
            author = metadata[key]
            break
    return {"publish_time": date, "url": url, "author": author}


def extract_analysis_body(text: str) -> str:
    """Remove archive title/metadata while preserving the actual article body."""
    separator = re.search(r"(?m)^\s*---\s*$", text[:4000])
    if separator:
        return text[separator.end() :].lstrip()
    heading = re.match(r"^\s*#\s+.+?\n+", text)
    return text[heading.end() :] if heading else text


def parse_datetime(value: str) -> str | None:
    match = DATE_RE.search(value)
    if not match:
        return None
    try:
        return datetime(*map(int, match.groups())).date().isoformat()
    except ValueError:
        return None


def tokenize(text: str) -> list[str]:
    tokens = [word.lower() for word in LATIN_RE.findall(text)]
    for block in CJK_RE.findall(text):
        if block in STOPWORDS:
            continue
        if len(block) <= 4:
            tokens.append(block)
        else:
            tokens.extend(block[i : i + 2] for i in range(len(block) - 1))
    return [token for token in tokens if token not in STOPWORDS and len(token) > 1]


def classify_title(title: str) -> list[str]:
    labels: list[str] = []
    if "?" in title or "？" in title or title.startswith(("为什么", "如何", "怎么")):
        labels.append("question")
    if re.search(r"\d", title):
        labels.append("number")
    if re.search(r"不是.+而是|对比|相比|vs", title, re.IGNORECASE):
        labels.append("contrast")
    if re.search(r"清单|步骤|方法|指南|教程|攻略", title):
        labels.append("how_to")
    if re.search(r"警惕|别再|不要|风险|坑", title):
        labels.append("warning")
    if re.search(r"我|复盘|亲测|经历", title):
        labels.append("experience")
    return labels or ["other"]


def classify_opening(text: str) -> list[str]:
    opening = strip_markdown(text)[:300]
    labels: list[str] = []
    checks = {
        "conclusion": r"先说结论|结论是|我的判断",
        "question": r"[？?]|为什么|如何|怎么",
        "scene": r"最近|今天|昨天|当.+时|场景",
        "story": r"我(?:曾经|最近|第一次|记得)|有一天",
        "data": r"\d+(?:\.\d+)?%|数据显示|统计",
        "pain": r"痛点|困扰|问题是|很多人",
        "quote": r"有人说|曾说|引用|据.+表示",
    }
    for label, pattern in checks.items():
        if re.search(pattern, opening):
            labels.append(label)
    return labels or ["other"]


def image_records(text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for index, match in enumerate(IMAGE_RE.finditer(text), start=1):
        before = strip_markdown(text[max(0, match.start() - 100) : match.start()])
        after = strip_markdown(text[match.end() : match.end() + 100])
        records.append(
            {
                "index": index,
                "alt": match.group(1).strip(),
                "path": match.group(2).strip(),
                "before": before[-80:],
                "after": after[:80],
            }
        )
    return records


def count_patterns(text: str, patterns: dict[str, re.Pattern[str]]) -> dict[str, int]:
    return {name: len(pattern.findall(text)) for name, pattern in patterns.items()}


def ending_cta(text: str) -> dict[str, Any]:
    ending = text[-320:]
    signals = count_patterns(ending, ENDING_CTA_PATTERNS)
    labels = [name for name, count in signals.items() if count]
    return {
        "present": bool(labels),
        "labels": labels,
        "signal_count": sum(signals.values()),
        "excerpt": ending[-180:],
    }


def segment_energy(text: str) -> list[int]:
    """Estimate opening/middle/ending rhetorical energy from visible text signals."""
    length = len(text)
    if not length:
        return [0, 0, 0]
    cuts = [text[: length // 3], text[length // 3 : 2 * length // 3], text[2 * length // 3 :]]
    energies: list[int] = []
    for segment in cuts:
        score = (
            segment.count("?")
            + segment.count("？")
            + segment.count("!")
            + segment.count("！")
            + len(re.findall(r"但是|然而|没想到|真正|本质|所以|因此|如果", segment))
        )
        energies.append(min(5, 1 + score // 2))
    return energies


def article_features(path: Path, root: Path) -> dict[str, Any]:
    raw, warnings = read_document(path)
    title = extract_title(raw, path)
    metadata = extract_metadata(raw)
    analysis_raw = extract_analysis_body(raw)
    clean = strip_markdown(analysis_raw)
    paragraphs = [p.strip() for p in PARAGRAPH_RE.split(clean) if p.strip()]
    sentences = [s.strip() for s in SENTENCE_RE.findall(clean) if s.strip()]
    images = image_records(analysis_raw)
    tokens = tokenize(clean)
    article_id = hashlib.sha256(
        f"{normalize_title(title)}\n{metadata['url']}\n{clean[:1000]}".encode("utf-8")
    ).hexdigest()[:12]

    return {
        "id": article_id,
        "source_file": path.relative_to(root).as_posix(),
        "source_type": path.suffix.lower().lstrip("."),
        "title": title,
        "normalized_title": normalize_title(title),
        "url": metadata["url"],
        "author": metadata["author"],
        "publish_time_raw": metadata["publish_time"],
        "publish_date": parse_datetime(metadata["publish_time"]),
        "text_sha256": hashlib.sha256(clean.encode("utf-8")).hexdigest(),
        "char_count": len(re.sub(r"\s", "", clean)),
        "paragraph_count": len(paragraphs),
        "sentence_count": len(sentences),
        "avg_sentence_chars": round(
            statistics.mean(len(re.sub(r"\s", "", s)) for s in sentences), 2
        )
        if sentences
        else 0,
        "heading_count": len(HEADING_RE.findall(analysis_raw)),
        "list_item_count": len(LIST_RE.findall(analysis_raw)),
        "question_count": clean.count("?") + clean.count("？"),
        "quote_count": len(QUOTE_RE.findall(analysis_raw)),
        "bold_count": len(BOLD_RE.findall(analysis_raw)),
        "link_count": len(LINK_RE.findall(analysis_raw)),
        "image_count": len(images),
        "image_analysis_available": path.suffix.lower() in {".md", ".markdown"},
        "images": images,
        "title_labels": classify_title(title),
        "opening_labels": classify_opening(analysis_raw),
        "cta_counts": count_patterns(clean, CTA_PATTERNS),
        "ending_cta": ending_cta(clean),
        "segment_energy": segment_energy(clean),
        "evidence_counts": count_patterns(clean, EVIDENCE_PATTERNS),
        "stance_counts": count_patterns(clean, STANCE_PATTERNS),
        "sensitive_counts": count_patterns(clean, SENSITIVE_PATTERNS),
        "top_tokens": Counter(tokens).most_common(30),
        "warnings": warnings,
        "text_excerpt": clean[:500],
    }


def numeric_summary(values: list[int | float]) -> dict[str, float | int]:
    if not values:
        return {"count": 0}
    ordered = sorted(values)
    return {
        "count": len(values),
        "min": ordered[0],
        "max": ordered[-1],
        "mean": round(statistics.mean(values), 2),
        "median": round(statistics.median(values), 2),
    }


def build_summary(articles: list[dict[str, Any]], skipped: list[dict[str, str]]) -> dict[str, Any]:
    token_documents: Counter[str] = Counter()
    token_totals: Counter[str] = Counter()
    title_labels: Counter[str] = Counter()
    opening_labels: Counter[str] = Counter()
    cta_totals: Counter[str] = Counter()
    evidence_totals: Counter[str] = Counter()
    stance_totals: Counter[str] = Counter()
    sensitive_totals: Counter[str] = Counter()
    for article in articles:
        token_map = dict(article["top_tokens"])
        token_totals.update(token_map)
        token_documents.update(token_map.keys())
        title_labels.update(article["title_labels"])
        opening_labels.update(article["opening_labels"])
        cta_totals.update(article["cta_counts"])
        evidence_totals.update(article["evidence_counts"])
        stance_totals.update(article["stance_counts"])
        sensitive_totals.update(article["sensitive_counts"])

    dates = sorted(a["publish_date"] for a in articles if a["publish_date"])
    intervals: list[int] = []
    if len(dates) >= 2:
        parsed = [datetime.fromisoformat(value) for value in dates]
        intervals = [(b - a).days for a, b in zip(parsed, parsed[1:])]

    return {
        "raw_file_count": len(articles) + len(skipped),
        "effective_article_count": len(articles),
        "skipped_count": len(skipped),
        "publish_date_count": len(dates),
        "publish_date_range": [dates[0], dates[-1]] if dates else None,
        "publish_interval_days": numeric_summary(intervals),
        "char_count": numeric_summary([a["char_count"] for a in articles]),
        "paragraph_count": numeric_summary([a["paragraph_count"] for a in articles]),
        "sentence_count": numeric_summary([a["sentence_count"] for a in articles]),
        "image_count": numeric_summary([a["image_count"] for a in articles]),
        "heading_count": numeric_summary([a["heading_count"] for a in articles]),
        "title_labels": dict(title_labels),
        "opening_labels": dict(opening_labels),
        "cta_counts": dict(cta_totals),
        "evidence_counts": dict(evidence_totals),
        "stance_counts": dict(stance_totals),
        "sensitive_counts": dict(sensitive_totals),
        "top_tokens": [
            {
                "token": token,
                "total_count": count,
                "document_count": token_documents[token],
                "document_coverage": round(token_documents[token] / len(articles), 4)
                if articles
                else 0,
            }
            for token, count in token_totals.most_common(100)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    input_root = args.input.expanduser().resolve()
    output_root = args.output.expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    existing_data_path = artifact_path(output_root, "analysis_data")
    existing_payload: dict[str, Any] = {}
    if existing_data_path.exists():
        try:
            existing_payload = json.loads(existing_data_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing_payload = {}
    paths = (
        [input_root]
        if input_root.is_file() and input_root.suffix.lower() in SUPPORTED
        else sorted(
            path
            for path in input_root.rglob("*")
            if path.is_file() and path.suffix.lower() in SUPPORTED
        )
    )
    relative_root = input_root.parent if input_root.is_file() else input_root

    articles: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for path in paths:
        feature = article_features(path, relative_root)
        if not feature["char_count"]:
            skipped.append({"source_file": feature["source_file"], "reason": "; ".join(feature["warnings"]) or "empty text"})
            continue
        dedupe_key = (feature["normalized_title"], feature["text_sha256"])
        if dedupe_key in seen:
            skipped.append({"source_file": feature["source_file"], "reason": "duplicate title and text"})
            continue
        seen.add(dedupe_key)
        articles.append(feature)

    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "input_root": str(input_root),
        "dataset_sha256": hashlib.sha256(
            "\n".join(sorted(a["text_sha256"] for a in articles)).encode("utf-8")
        ).hexdigest(),
        "sample_policy": {
            "article_count": len(articles),
            "mode": "descriptive_only" if len(articles) < 5 else "comparative",
            "trend_allowed": len(articles) >= 5 and sum(bool(a["publish_date"]) for a in articles) >= 5,
        },
        "sync_policy": {
            "public_url_count": sum(
                1
                for article in articles
                if article["url"].startswith(("http://", "https://"))
            ),
            "all_sources_public": bool(articles)
            and all(
                article["url"].startswith(("http://", "https://"))
                for article in articles
            ),
            "sensitive_signal_count": sum(
                sum(article["sensitive_counts"].values()) for article in articles
            ),
            "requires_confirmation": (
                not articles
                or not all(
                    article["url"].startswith(("http://", "https://"))
                    for article in articles
                )
                or any(
                    any(article["sensitive_counts"].values()) for article in articles
                )
            ),
            "note": "Missing public URLs or pattern matches trigger review; neither proves confidentiality.",
        },
        "summary": build_summary(articles, skipped),
        "articles": articles,
        "skipped": skipped,
        "annotations": existing_payload.get("annotations", []),
        "competitor_samples": existing_payload.get("competitor_samples", []),
    }

    data_path = artifact_path(output_root, "analysis_data")
    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_path = artifact_path(output_root, "article_features")
    columns = [
        "id", "source_file", "title", "url", "author", "publish_date", "char_count",
        "paragraph_count", "sentence_count", "avg_sentence_chars", "heading_count",
        "list_item_count", "question_count", "quote_count", "bold_count", "link_count",
        "image_count", "image_analysis_available", "title_labels", "opening_labels",
        "warnings",
    ]
    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for article in articles:
            row = {key: article.get(key, "") for key in columns}
            for key in ("title_labels", "opening_labels", "warnings"):
                row[key] = "|".join(row[key])
            writer.writerow(row)

    print(data_path)
    print(csv_path)
    print(f"articles: {len(articles)}, skipped: {len(skipped)}")
    return 0 if articles else 1


if __name__ == "__main__":
    raise SystemExit(main())
