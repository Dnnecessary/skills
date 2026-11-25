#!/usr/bin/env python3
"""Generate a research-style methodology dashboard from author analysis data."""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

from artifact_names import artifact_path


def esc(value: object) -> str:
    return html.escape(str(value))


def pct(value: float) -> str:
    return f"{value:.0%}"


def bar(label: str, value: int | float, maximum: int | float, note: str = "") -> str:
    width = 0 if not maximum else min(100, float(value) / float(maximum) * 100)
    return (
        '<div class="bar-row"><div class="bar-copy">'
        f"<span>{esc(label)}</span><b>{esc(value)}</b></div>"
        f'<div class="bar-track"><i style="width:{width:.1f}%"></i></div>'
        f"<small>{esc(note)}</small></div>"
    )


def metric(label: str, value: object, note: str = "") -> str:
    return (
        '<div class="metric"><span>'
        f"{esc(label)}</span><strong>{esc(value)}</strong><small>{esc(note)}</small></div>"
    )


def annotation_text(
    grouped: dict[str, list[dict[str, Any]]], dimension: str, fallback: str
) -> str:
    items = grouped.get(dimension, [])
    return items[0]["label"] if items else fallback


def line_chart(articles: list[dict[str, Any]]) -> str:
    dated = sorted(
        (article for article in articles if article.get("publish_date")),
        key=lambda item: item["publish_date"],
    )
    if not dated:
        return '<div class="unavailable">发布时间数据不可得</div>'
    values = [article["char_count"] for article in dated]
    max_value = max(values) or 1
    width, height, pad = 920, 280, 42
    x_step = (width - pad * 2) / max(1, len(dated) - 1)
    points = [
        (
            pad + index * x_step,
            height - pad - value / max_value * (height - pad * 2),
        )
        for index, value in enumerate(values)
    ]
    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    area = f"{pad},{height-pad} {polyline} {width-pad},{height-pad}"
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5"><title>'
        f"{esc(article['publish_date'])} · {article['char_count']} 字符 · {esc(article['title'])}"
        "</title></circle>"
        for (x, y), article in zip(points, dated)
    )
    max_labels = 7
    if len(dated) <= max_labels:
        label_indexes = list(range(len(dated)))
    else:
        label_indexes = sorted(
            {
                round(index * (len(dated) - 1) / (max_labels - 1))
                for index in range(max_labels)
            }
        )
    labels = "".join(
        f'<text x="{points[index][0]:.1f}" y="{height-12}" '
        f'text-anchor="{"start" if index == 0 else "end" if index == len(dated)-1 else "middle"}">'
        f"{esc(dated[index]['publish_date'][5:])}</text>"
        for index in label_indexes
    )
    return f"""<svg class="line-chart" viewBox="0 0 {width} {height}" role="img"
    aria-label="按发布时间排列的文章正文字符趋势">
      <defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#285f57" stop-opacity=".28"/>
        <stop offset="1" stop-color="#285f57" stop-opacity=".02"/>
      </linearGradient></defs>
      <line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" class="axis"/>
      <polygon points="{area}" fill="url(#area)"/>
      <polyline points="{polyline}" class="trend-line"/>
      {dots}{labels}
    </svg>"""


def title_learning_html(articles: list[dict[str, Any]]) -> str:
    examples = [
        (
            next((a for a in articles if "不如" in a["title"]), articles[0]),
            "对象 A + 核心能力 + 不如对象 B",
            "直接制造比较冲突，读者会立刻想知道判断依据。",
            "把两个同类对象放进同一个具体任务中比较，不要只写空泛的“谁更强”。",
        ),
        (
            next((a for a in articles if "多久" in a["title"]), articles[0]),
            "你的对象 + 一个可回答的问题",
            "把读者拉进场景，问题具体，容易产生自测冲动。",
            "用“你的___能做到什么程度？”改写成与读者经验直接相关的问题。",
        ),
        (
            next((a for a in articles if "不用" in a["title"]), articles[0]),
            "有了新工具 + 原本困难的结果",
            "用生活化结果表达技术价值，比只介绍功能更容易理解。",
            "先找工具真正改变的生活或工作场景，再写结果，不要堆功能名。",
        ),
        (
            next((a for a in articles if "浮躁" in a["title"]), articles[0]),
            "否定热门结论 + 指出真正问题",
            "反转主流叙事，同时表达作者立场和价值判断。",
            "只有在拥有实测或案例证据时使用反转标题，否则容易变成刻意唱反调。",
        ),
    ]
    seen: set[str] = set()
    cards = []
    for article, formula, reason, practice in examples:
        if article["id"] in seen:
            continue
        seen.add(article["id"])
        cards.append(
            '<article class="learning-example">'
            f'<span>原标题</span><h4>{esc(article["title"])}</h4>'
            f'<p><b>标题公式：</b>{esc(formula)}</p>'
            f'<p><b>为什么有效：</b>{esc(reason)}</p>'
            f'<p><b>你怎么学：</b>{esc(practice)}</p></article>'
        )
    return "".join(cards)


def structure_learning_html(article_count: int, ending_cta_count: int) -> str:
    return (
        '<div class="structure-path">'
        '<article><span>01 开头</span><h4>先抛场景或冲突</h4>'
        '<p>用一个真实问题、反常体验或明确判断，让读者迅速知道这篇文章与自己有什么关系。</p>'
        '<b>练习：前 100 字只回答“发生了什么，为什么值得继续看”。</b></article>'
        '<article><span>02 中段</span><h4>用证据推动判断</h4>'
        '<p>加入实测、截图、对比、成本或失败过程，并解释现象背后的机制，而不是只罗列结果。</p>'
        '<b>练习：每个核心观点后追问“我拿什么证明”。</b></article>'
        '<article><span>03 结尾</span><h4>收束结论并给出下一步</h4>'
        f'<p>样本中 {ending_cta_count}/{article_count} 篇结尾有明确问题或行动。好的结尾让读者知道如何使用结论。</p>'
        '<b>练习：在提问、行动建议、复测预告中至少选择一种。</b></article>'
        "</div>"
    )


def competitor_html(samples: list[dict[str, str]]) -> str:
    if not samples:
        return '<div class="unavailable">未提供公开竞品标题样本</div>'
    return "".join(
        f'<a class="competitor-item" href="{esc(item.get("url", "#"))}" target="_blank" rel="noreferrer">'
        f'<span>{esc(item.get("type", "其他"))}</span><b>{esc(item.get("title", ""))}</b>'
        f'<small>{esc(item.get("source", "公开搜索"))}</small></a>'
        for item in samples
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    summary = data["summary"]
    articles = data["articles"]
    annotations = data.get("annotations", [])
    competitor_path = artifact_path(args.data.parent, "competitor_samples")
    competitor_samples = data.get("competitor_samples", [])
    if competitor_path.exists():
        competitor_samples = json.loads(competitor_path.read_text(encoding="utf-8"))
    article_count = len(articles)
    total_chars = sum(article["char_count"] for article in articles)
    total_images = sum(article["image_count"] for article in articles)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in annotations:
        grouped[item["dimension"]].append(item)

    author = next(
        (article.get("author") for article in articles if article.get("author")), "作者"
    )
    date_range = summary.get("publish_date_range") or ["未知", "未知"]
    theme_items = grouped.get("theme", [])
    theme_names = [item["label"] for item in theme_items]
    theme_max = max((len(set(item["article_ids"])) for item in theme_items), default=1)
    theme_bars = "".join(
        bar(
            item["label"],
            len(set(item["article_ids"])),
            theme_max,
            f"{len(set(item['article_ids']))}/{article_count} 篇，允许多标签",
        )
        for item in theme_items
    ) or '<div class="unavailable">主题标注数据不可得</div>'
    coverage_candidates = {
        "模型与工具实测": any("实测" in name or "工具" in name for name in theme_names),
        "AI 编程工作流": any("工作流" in name or "工程" in name for name in theme_names),
        "产品与创业判断": any("产品" in name or "创业" in name for name in theme_names),
        "新手入门教程": any("入门" in article["title"] or "教程" in article["title"] for article in articles),
        "成本与选型清单": any("成本" in article["title"] or "选型" in article["title"] or "清单" in article["title"] for article in articles),
        "失败案例复盘": any("失败" in article["title"] or "复盘" in article["title"] for article in articles),
    }
    coverage_html = "".join(
        f'<div class="coverage-item {"covered" if present else "gap"}">'
        f'<span>{"作者常写" if present else "你的拓展参考"}</span><b>{esc(name)}</b></div>'
        for name, present in coverage_candidates.items()
    )

    title_labels = summary.get("title_labels", {})
    opening_labels = summary.get("opening_labels", {})
    evidence_counts = summary.get("evidence_counts", {})
    stance_counts = summary.get("stance_counts", {})
    label_names = {
        "number": "数字/版本号",
        "question": "提问",
        "other": "直接判断",
        "contrast": "对比",
        "how_to": "方法教程",
        "warning": "风险警示",
        "experience": "经验叙事",
        "scene": "场景",
        "data": "数据",
        "conclusion": "结论前置",
        "story": "故事",
        "pain": "痛点",
        "quote": "引用",
        "test": "实测",
        "authority": "权威/官方",
        "case": "案例",
        "comparison": "对比",
        "strong": "强判断",
        "cautious": "谨慎判断",
        "conditional": "条件判断",
        "risk": "风险表达",
    }

    def bars(values: dict[str, int], note: str) -> str:
        maximum = max(values.values(), default=1)
        return "".join(
            bar(label_names.get(key, key), value, maximum, note)
            for key, value in values.items()
            if value
        ) or '<div class="unavailable">当前维度没有可识别信号</div>'

    evidence_articles = sum(
        1 for article in articles if sum(article.get("evidence_counts", {}).values()) > 0
    )
    length_groups = {
        "短文 <1k": sum(article["char_count"] < 1000 for article in articles),
        "中篇 1k–2k": sum(1000 <= article["char_count"] < 2000 for article in articles),
        "长文 ≥2k": sum(article["char_count"] >= 2000 for article in articles),
    }
    image_groups = {
        "无图": sum(article["image_count"] == 0 for article in articles),
        "1–5 张": sum(1 <= article["image_count"] <= 5 for article in articles),
        "6–15 张": sum(6 <= article["image_count"] <= 15 for article in articles),
        "16 张以上": sum(article["image_count"] >= 16 for article in articles),
    }
    weekdays = Counter()
    for article in articles:
        if article.get("publish_date"):
            weekdays[datetime.fromisoformat(article["publish_date"]).strftime("%a")] += 1
    weekday_names = {
        "Mon": "周一",
        "Tue": "周二",
        "Wed": "周三",
        "Thu": "周四",
        "Fri": "周五",
        "Sat": "周六",
        "Sun": "周日",
    }
    weekday_bars = bars(
        {weekday_names.get(key, key): value for key, value in weekdays.items()},
        "样本内文章数",
    )
    dated_articles = sorted(
        (article for article in articles if article.get("publish_date")),
        key=lambda item: item["publish_date"],
    )
    release_days = Counter(article["publish_date"] for article in dated_articles)
    burst_days = sum(count > 1 for count in release_days.values())
    release_summary = (
        f"样本覆盖 {len(release_days)} 个发布日，{burst_days} 天出现同日多篇；"
        f"发布间隔中位数 {summary.get('publish_interval_days', {}).get('median', '未知')} 天。"
    )
    ending_cta_count = sum(
        bool(article.get("ending_cta", {}).get("present")) for article in articles
    )

    strongest_evidence = max(evidence_counts, key=evidence_counts.get) if evidence_counts else ""
    persona = annotation_text(grouped, "persona", "实践型内容生产者")
    structure = annotation_text(grouped, "structure", "场景—证据—判断")
    stance = annotation_text(grouped, "stance", "结论与边界并重")
    style = annotation_text(grouped, "style", "高密度表达")
    reader = annotation_text(grouped, "reader", "目标读者待进一步标注")
    benefit = annotation_text(grouped, "reader_benefit", "读者收益待进一步标注")
    persona_annotations = grouped.get("persona") or []
    persona_evidence = (
        persona_annotations[0].get("evidence", "")
        if persona_annotations
        else "来自真实任务、实测过程和明确判断。"
    )

    positive_factors = [
        (persona, "信任来源"),
        (structure, "稳定结构"),
        (f"{label_names.get(strongest_evidence, strongest_evidence)}信号 {evidence_counts.get(strongest_evidence, 0)} 次", "证据优势"),
        (f"中篇 {length_groups['中篇 1k–2k']}/{article_count}", "内容承载"),
        (f"{len(theme_items)} 个主题方向", "内容覆盖"),
    ]
    drag_factors = [
        ("样本仅代表当前观察窗口", "样本风险"),
        ("时间窗口仅覆盖短周期", "长期趋势缺口"),
        ("主题与品牌相对集中", "外推限制"),
    ]
    positive_html = "".join(
        f'<span class="factor positive"><b>{esc(value)}</b><small>{esc(kind)}</small></span>'
        for value, kind in positive_factors
    )
    drag_html = "".join(
        f'<span class="factor negative"><b>{esc(value)}</b><small>{esc(kind)}</small></span>'
        for value, kind in drag_factors
    )

    opportunities = [
        ("学习选题判断", "连续记录 10 个候选选题，分别标注变化、反差、任务和可验证证据，只写同时满足至少三项的题目。"),
        ("学习实测方法", "选择一个真实任务，固定版本、成本、耗时和验收标准，完整记录成功、失败与适用边界。"),
        ("学习文章结构", "用“体验冲突—证据—机制—判断—互动”重写一篇自己的旧文，再比较信息密度和说服力。"),
        ("学习鲜明表达", "先用一句话写出明确结论，再补充适用对象、条件和风险，练习强判断而不绝对化。"),
        ("学习栏目经营", "把自己的内容分成入口、信任、工具和定位四类，为每类设计一个可连续更新的固定栏目。"),
        ("建立个人版本", "每次模仿后记录保留了什么、删除了什么、为什么不同，逐步把外部方法转成自己的创作原则。"),
    ]
    opportunity_html = "".join(
        f'<article class="action-card"><span>0{index}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for index, (title, text) in enumerate(opportunities, start=1)
    )

    conclusions = [
        (
            "先学选题来源",
            f"{article_count} 篇覆盖 {date_range[0]} 至 {date_range[-1]}，发布间隔中位数 "
            f"{summary.get('publish_interval_days', {}).get('median', '未知')} 天。重点观察他如何持续从变化、任务和反馈中获得题目。",
        ),
        (
            "再学论证方法",
            f"常用结构是“{structure}”；最常见的证据方式是“{label_names.get(strongest_evidence, strongest_evidence)}”。",
        ),
        (
            "最后形成自己的栏目",
            f"从 {len(theme_items)} 个主题方向中选择与你经验匹配的部分，通过连续练习、复测和系列化形成自己的内容资产。",
        ),
    ]
    conclusion_cards = "".join(
        f'<article class="conclusion-card"><span>0{index}</span><h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for index, (title, text) in enumerate(conclusions, start=1)
    )

    nav_items = [
        ("overview", "00 一页看懂"),
        ("positioning", "01 定位与价值"),
        ("content-map", "02 内容地图"),
        ("topics", "03 选题方法"),
        ("writing", "04 文章写法"),
        ("evidence", "05 观点证据"),
        ("style", "06 语言风格"),
        ("value", "07 值得学习"),
        ("growth", "08 运营增长"),
        ("reuse", "09 学习与迁移"),
    ]
    nav = "".join(f'<a href="#{panel}">{esc(label)}</a>' for panel, label in nav_items)
    embedded_data = dict(data)
    embedded_data.pop("dataset_sha256", None)
    embedded = json.dumps(embedded_data, ensure_ascii=False).replace("</", "<\\/")

    document = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(author)}｜博主方法学习看板</title>
<style>
:root{{--paper:#f2eee4;--paper2:#faf7ef;--card:#fffdf8;--ink:#202824;--muted:#74746c;--line:#d6d0c2;--red:#285f57;--red2:#4d8278;--black:#1e2925;--gray:#aaa59b;--gold:#b88a42}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.7 "PingFang SC","Noto Sans CJK SC",system-ui,sans-serif}}
.topbar{{position:sticky;top:0;z-index:20;background:#f8f4ecef;backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}}.topbar-inner{{max-width:1160px;margin:auto;display:flex;align-items:center;gap:22px;padding:10px 20px}}
.brand{{font-family:Georgia,"Songti SC",serif;font-weight:800;white-space:nowrap;color:var(--ink)}}nav{{display:flex;flex:1;min-width:0;gap:2px;overflow-x:auto;scrollbar-width:thin}}nav a{{color:#4b4640;text-decoration:none;padding:7px 9px;white-space:nowrap;font-size:12px;border-bottom:2px solid transparent}}nav a:hover,nav a.active{{color:var(--red);border-color:var(--red)}}
main{{max-width:1160px;margin:auto;padding:34px 20px 90px}}.hero{{padding:42px 0 48px;border-bottom:1px solid var(--line);position:relative}}.hero:after{{content:"REPORT";position:absolute;right:0;top:20px;font:800 74px/1 Georgia,serif;letter-spacing:.04em;color:#d8cec03b}}.eyebrow{{color:var(--red);font-size:11px;font-weight:800;letter-spacing:.16em}}h1{{font:800 clamp(38px,5vw,60px)/1.1 Georgia,"Songti SC",serif;margin:12px 0 18px;max-width:820px;letter-spacing:-.035em}}.hero p{{font-size:16px;max-width:820px;color:#5c554d}}.hero-meta{{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}}.hero-meta span{{border:1px solid var(--line);background:var(--paper2);padding:6px 10px;font-size:12px}}
.chapter{{padding:72px 0 28px;scroll-margin-top:62px}}.chapter-head{{display:flex;align-items:flex-start;gap:13px;margin-bottom:24px;position:relative}}.chapter-no{{background:var(--red);color:#fff;font-weight:900;padding:5px 9px}}h2{{font:800 31px/1.2 Georgia,"Songti SC",serif;margin:0}}.chapter-sub{{color:var(--muted);margin-top:3px}}.ghost-no{{position:absolute;right:4px;top:-44px;font:76px/1 Georgia,serif;color:#d7cec255}}
.grid-2{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.grid-3{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}.card,.conclusion-card,.metric,.action-card{{background:var(--card);border:1px solid var(--line);box-shadow:0 7px 20px #4b39220b}}
.card{{padding:22px}}.card h3,.conclusion-card h3,.action-card h3{{font-family:Georgia,"Songti SC",serif;margin:0 0 9px}}.conclusion-card{{padding:22px;position:relative;min-height:158px;border-top:3px solid var(--red)}}.conclusion-card>span,.action-card>span{{color:var(--red);font-weight:900}}
.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}}.metric{{padding:17px}}.metric span,.metric small,small,.muted{{display:block;color:var(--muted)}}.metric strong{{display:block;font:800 29px/1.2 Georgia,serif;margin:6px 0;color:var(--red)}}
.red-alert{{margin:36px calc(50% - 50vw);padding:42px max(22px,calc((100vw - 1120px)/2));background:linear-gradient(105deg,#173d37,#2e695f);color:#fff}}.red-alert .eyebrow{{color:#d9e7df}}.red-alert h3{{font:800 30px/1.35 Georgia,"Songti SC",serif;margin:8px 0;max-width:960px}}.red-alert p{{max-width:900px;color:#dce9e4}}
.bar-row{{margin:14px 0}}.bar-copy{{display:flex;justify-content:space-between;gap:12px}}.bar-track{{height:10px;background:#ece5db;margin:6px 0;overflow:hidden}}.bar-track i{{display:block;height:100%;background:linear-gradient(90deg,var(--red),var(--red2))}}
.line-chart{{width:100%;min-height:280px}}.line-chart .axis{{stroke:#bdb4a8;stroke-width:1}}.line-chart .trend-line{{fill:none;stroke:var(--red);stroke-width:4}}.line-chart circle{{fill:var(--red)}}.line-chart text{{font-size:12px;fill:var(--muted)}}
.unavailable{{padding:23px;border:1px dashed #b8aea0;background:#f7f2ea;color:var(--muted);text-align:center}}
.black-quote{{background:var(--black);color:#fff;padding:27px 31px;font:700 22px/1.55 Georgia,"Songti SC",serif;margin-top:20px}}.asset-loop{{display:grid;gap:8px}}.asset-loop div{{display:grid;grid-template-columns:86px 82px 1fr;align-items:center;gap:12px;padding:12px 14px;background:#faf7f1;border:1px solid var(--line);position:relative}}.asset-loop div:not(:last-child):after{{content:"↓";position:absolute;left:49px;bottom:-17px;z-index:2;color:var(--red);font-weight:900}}.asset-loop b{{color:var(--red)}}.asset-loop small{{color:var(--ink);font-weight:700}}.asset-loop em{{color:var(--muted);font-style:normal;font-size:12px}}
.action-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:13px}}.action-card{{padding:20px;border-top:4px solid var(--red)}}.method-note{{border:1px solid var(--line);background:#f9f5ed;padding:18px;margin-top:16px}}
.coverage-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}}.coverage-item{{padding:16px;background:#faf7f1;border:1px solid var(--line)}}.coverage-item span{{display:block;font-size:11px;color:var(--muted)}}.coverage-item.covered{{border-top:3px solid var(--black)}}.coverage-item.covered b{{color:var(--black)}}.coverage-item.gap{{border:1px dashed #a78c5d;background:#fffaf0}}.coverage-item.gap b{{color:#8b672e}}
.learning-examples{{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}}.learning-example{{padding:18px;background:#faf7f1;border:1px solid var(--line);border-top:3px solid var(--red)}}.learning-example>span{{font-size:11px;color:var(--red);font-weight:800}}.learning-example h4{{margin:5px 0 12px;font:800 18px/1.4 Georgia,"Songti SC",serif}}.learning-example p{{margin:7px 0}}.learning-example b{{color:var(--black)}}
.structure-path{{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--line)}}.structure-path article{{padding:22px;background:#faf7f1;position:relative}}.structure-path article+article{{border-left:1px solid var(--line)}}.structure-path article+article:before{{content:"→";position:absolute;left:-10px;top:28px;background:var(--paper);color:var(--red);font-weight:900}}.structure-path span{{color:var(--red);font-weight:900;font-size:12px}}.structure-path h4{{font:800 19px/1.35 Georgia,"Songti SC",serif;margin:7px 0}}.structure-path b{{display:block;margin-top:12px;font-size:12px;color:var(--red)}}
.competitor-list{{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}}.competitor-item{{display:grid;gap:4px;padding:15px;border:1px solid var(--line);text-decoration:none;color:var(--ink);background:#faf7f1}}.competitor-item:hover{{border-color:var(--red)}}.competitor-item span{{color:var(--red);font-size:11px;font-weight:800}}.competitor-item small{{color:var(--muted)}}
.analysis-summary{{margin-top:16px;padding:19px 21px;background:#e8ede7;border-left:5px solid var(--red);color:#35413c}}.analysis-summary h4{{margin:0 0 7px;font:800 17px/1.3 Georgia,"Songti SC",serif;color:var(--black)}}.analysis-summary p{{margin:5px 0}}.analysis-summary b{{color:var(--red)}}
.rhythm-grid{{align-items:start}}.rhythm-stack{{display:grid;gap:16px}}.rhythm-stack .analysis-summary{{margin-top:0}}.weekday-bars{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:22px}}.weekday-bars .bar-row{{margin:9px 0}}.rhythm-advice li{{margin:7px 0}}
.page-notes{{margin-top:64px;padding-top:20px;border-top:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr;gap:24px;color:var(--muted);font-size:12px}}.page-notes p{{margin:4px 0}}.page-notes b{{color:var(--ink)}}
@media(max-width:900px){{.grid-2,.grid-3,.metrics,.action-grid,.coverage-grid,.competitor-list,.learning-examples,.structure-path,.page-notes{{grid-template-columns:1fr}}.structure-path article+article{{border-left:0;border-top:1px solid var(--line)}}.structure-path article+article:before{{display:none}}.ghost-no,.hero:after{{display:none}}}}
@media(max-width:560px){{.asset-loop div{{grid-template-columns:82px 1fr}}.asset-loop em{{grid-column:1/-1}}.asset-loop div:not(:last-child):after{{left:45px}}}}
@media(max-width:560px){{.weekday-bars{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class="topbar"><div class="topbar-inner"><div class="brand">{esc(author)} · 方法学习看板</div><nav>{nav}</nav></div></header>
<main>
<header class="hero">
  <div class="eyebrow">LEARN THE METHOD · BUILD YOUR OWN</div>
  <h1>解构优秀创作者的方法体系，建立你的内容能力</h1>
  <p>从定位、选题、论证、表达与运营五个层面，识别这个博主可迁移的方法、适用条件与训练路径。重点不是复制表面风格，而是把经过验证的决策逻辑转化为自己的创作能力。</p>
  <div class="hero-meta"><span>样本 {article_count} 篇</span><span>{esc(date_range[0])} → {esc(date_range[-1])}</span><span>正文与公开元数据分析</span></div>
</header>

<section class="chapter" id="overview">
  <div class="chapter-head"><span class="chapter-no">00</span><div><h2>一页看懂</h2><div class="chapter-sub">先理解这个作者，再决定学什么</div></div><span class="ghost-no">00</span></div>
  <div class="grid-3">{conclusion_cards}</div>
  <div class="red-alert"><div class="eyebrow">LEARNING SUMMARY</div><h3>最值得学习的不是“写同样的内容”，而是用真实任务形成判断，再把判断组织成可理解、可验证、可互动的文章。</h3><p>{esc(author)} 的核心方法是“{esc(structure)}”。学习时应复制决策过程和验证方式，而不是复制具体观点、措辞或个人经历。</p></div>
</section>

<section class="chapter" id="positioning">
  <div class="chapter-head"><span class="chapter-no">01</span><div><h2>定位与价值</h2><div class="chapter-sub">先判断他靠什么建立可信度，再决定是否值得学</div></div><span class="ghost-no">01</span></div>
  <div class="grid-2"><div class="card"><h3>他的核心定位</h3><p>{esc(persona)}</p><h3>可信度从哪里来</h3><p>{esc(persona_evidence)}</p></div><div class="card"><h3>他服务谁</h3><p>{esc(reader)}</p><h3>他解决什么问题</h3><p>{esc(benefit)}</p></div></div>
  <div class="analysis-summary"><h4>你可以学什么</h4><p>学习的第一步不是模仿文风，而是明确自己的<b>身份、目标读者和稳定价值</b>。这个作者通过真实任务和明确取舍建立可信度，你也需要找到自己能够持续提供证据的经验领域。</p><p><b>练习：</b>用一句话填写“我是怎样的人，通过什么方法，帮助哪类读者解决什么问题”。如果其中任何一项无法具体说明，先不要急着模仿选题和标题。</p></div>
</section>

<section class="chapter" id="content-map">
  <div class="chapter-head"><span class="chapter-no">02</span><div><h2>内容地图</h2><div class="chapter-sub">经常写什么，各类内容承担什么作用</div></div><span class="ghost-no">02</span></div>
  <div class="grid-2"><div class="card"><h3>主题覆盖</h3>{theme_bars}</div><div class="card"><h3>内容资产分工</h3><div class="asset-loop"><div><b>热点判断</b><small>吸引新读者</small><em>快速解释变化，并给出明确的第一判断。</em></div><div><b>真实实测</b><small>建立信任</small><em>用任务、结果、成本和失败过程证明判断。</em></div><div><b>工作流</b><small>提供方法</small><em>把经验整理成步骤、清单和可重复使用的工具。</em></div><div><b>原则观点</b><small>建立定位</small><em>说明长期坚持的判断标准和取舍逻辑。</em></div><div><b>反馈复测</b><small>持续更新</small><em>回应新问题、补充边界，并发展下一篇内容。</em></div></div></div></div>
  <div class="analysis-summary"><h4>值得学习：让不同内容承担不同任务</h4><p>当前内容集中在 <b>{len(theme_items)} 个核心方向</b>。模型工具实测与 AI 编程工作流负责证明专业能力，产品与创业判断负责建立长期观点。</p><p><b>怎么学：</b>不要只列自己想写的主题，而要给每类内容分配任务。用热点内容带来入口，用实测内容建立信任，用工具内容提供可执行价值，用原则内容形成个人定位。</p></div>
  <div class="card" style="margin-top:18px"><h3>我还可以学习哪些内容方向</h3><p class="muted">已覆盖方向用于理解作者的内容基础；尚未覆盖方向用于启发你建立自己的差异，不代表作者必须补齐。</p><div class="coverage-grid">{coverage_html}</div></div>
</section>

<section class="chapter" id="topics">
  <div class="chapter-head"><span class="chapter-no">03</span><div><h2>选题方法</h2><div class="chapter-sub">题目从哪里来，如何找到有价值的切口</div></div><span class="ghost-no">03</span></div>
  <div class="grid-3"><div class="conclusion-card"><span>01</span><h3>追踪变化</h3><p>新模型、新功能、新争议出现时快速进入。</p></div><div class="conclusion-card"><span>02</span><h3>寻找反差</h3><p>主流评价与真实体验不一致时形成观点。</p></div><div class="conclusion-card"><span>03</span><h3>从任务出发</h3><p>围绕开发、产品、成本和验收等真实问题写作。</p></div></div>
  <div class="card" style="margin-top:18px"><h3>我要怎么学选题</h3><p>每次准备写作时，从“变化强度、读者相关性、可验证程度、能否形成明确判断”四个角度思考。优先选择既与读者有关、又能亲自验证的题目，而不是只追逐热点。</p></div>
  <div class="analysis-summary"><h4>值得学习：从反差和任务中找选题</h4><p>作者最有辨识度的选题不是单纯追热点，而是寻找<b>公开评价与真实使用之间的反差</b>。反差再通过任务、成本、截图或对比验证，就能形成独立判断。</p><p><b>怎么学：</b>建立选题表，每个题目都回答四个问题：发生了什么变化、和普遍认知有什么不同、我能否亲自验证、读者为什么在意。答不全的题目暂时不写。</p></div>
  <div class="card" style="margin-top:18px"><h3>竞品选题雷达</h3><p class="muted">公开搜索标题显示，同行常用“终极教程、完整指南、工具盘点、实测对比、新闻热点”切入。当前作者更强在鲜明判断和亲身实测，空位在系统教程、成本清单和失败复盘。</p><div class="competitor-list">{competitor_html(competitor_samples)}</div></div>
</section>

<section class="chapter" id="writing">
  <div class="chapter-head"><span class="chapter-no">04</span><div><h2>文章写法</h2><div class="chapter-sub">标题怎么起、开头怎么抓人、正文怎么展开</div></div><span class="ghost-no">04</span></div>
  <div class="grid-2"><div class="card"><h3>标题类型</h3>{bars(title_labels,"文章标签数")}</div><div class="card"><h3>开头类型</h3>{bars(opening_labels,"文章标签数，可多标签")}</div></div>
  <div class="grid-2" style="margin-top:18px"><div class="card"><h3>我应该学习什么标题方法</h3><ul><li>用具体对象和任务代替宽泛主题。</li><li>用问题、反差或结果建立阅读理由。</li><li>把热点名称与读者真正关心的收益连接起来。</li><li>观点型标题要有证据支撑，避免只靠冲突。</li></ul></div><div class="card"><h3>我要怎么练标题</h3><ol><li>先写一句文章核心判断。</li><li>分别改写成问题式、对比式、结果式三个版本。</li><li>删掉无法从正文证明的夸张词。</li><li>选择最能说明对象、问题和收益的版本。</li></ol></div></div>
  <div class="analysis-summary"><h4>我应该学习什么：先给判断，再展开证据</h4><p>这些标题经常把新产品、版本变化和明确结论放在一起，让读者快速知道文章讨论的对象和立场。正文再用场景、实测和对比解释判断依据。</p><p><b>我要怎么学：</b>写作前先完成五句话：发生了什么、我的判断是什么、证据是什么、适合谁不适合谁、读者下一步做什么。再把五句话扩展成全文。</p></div>
  <div class="card" style="margin-top:18px"><h3>代表标题怎么学</h3><p class="muted">选择最有代表性的标题，重点理解标题公式、有效原因、适用条件和可以练习的写法。</p><div class="learning-examples">{title_learning_html(articles)}</div></div>
  <div class="card" style="margin-top:18px"><h3>一篇文章可以怎么搭</h3><p class="muted">把抽象的“节奏”改成三个清楚的写作任务：开头抓住问题，中段提供证明，结尾推动下一步。</p>{structure_learning_html(article_count, ending_cta_count)}</div>
</section>

<section class="chapter" id="evidence">
  <div class="chapter-head"><span class="chapter-no">05</span><div><h2>观点与证据</h2><div class="chapter-sub">结论如何产生，读者为什么愿意相信</div></div><span class="ghost-no">05</span></div>
  <div class="grid-2"><div class="card"><h3>证据类型</h3>{bars(evidence_counts,"文本信号次数")}</div><div class="card"><h3>判断方式</h3>{bars(stance_counts,"文本信号次数")}<p>{esc(stance)}</p></div></div>
  <div class="analysis-summary"><h4>值得学习：观点必须有可检查的证据</h4><p><b>{label_names.get(strongest_evidence, strongest_evidence)}</b>是最突出的证据方式，共识别 {evidence_counts.get(strongest_evidence, 0)} 次。可信度来自亲自使用和任务验证，而不是重复公开资料。</p><p><b>怎么学：</b>每个重要结论至少配一种证据，并记录版本、任务、耗时、成本、结果和失败条件。先积累证据，再寻找漂亮表达，不要反过来。</p></div>
</section>

<section class="chapter" id="style">
  <div class="chapter-head"><span class="chapter-no">06</span><div><h2>语言风格</h2><div class="chapter-sub">表达为什么有辨识度，又如何保持易读</div></div><span class="ghost-no">06</span></div>
  <div class="grid-2"><div class="conclusion-card"><span>01</span><h3>{esc(style)}</h3><p>专业词与生活化表达并置，降低复杂主题的理解成本。</p></div><div class="conclusion-card"><span>02</span><h3>{esc(stance)}</h3><p>用明确判断形成记忆点，再补充条件和风险。</p></div></div>
  <div class="metrics">{metric("段落中位数",summary['paragraph_count']['median'],"短段落形成节奏")}{metric("句子中位数",summary['sentence_count']['median'],"按标点切分")}{metric("中篇文章",f"{length_groups['中篇 1k–2k']}/{article_count}","主要篇幅")}{metric("图片总数",total_images,"按内容类型使用")}</div>
  <div class="analysis-summary"><h4>值得学习：口语表达不等于降低信息密度</h4><p>表达方式可以概括为<b>口语化外壳 + 高密度判断</b>：专业内容被翻译成生活化语言，但核心概念、对比和结论没有被删掉。</p><p><b>怎么学：</b>写完后做两轮修改。第一轮删除空泛铺垫，每段只保留一个推进点；第二轮把抽象术语改写成具体场景或类比，但保留必要的专业边界。</p></div>
</section>

<section class="chapter" id="value">
  <div class="chapter-head"><span class="chapter-no">07</span><div><h2>值得学习</h2><div class="chapter-sub">把作者优势翻译成你可以训练的能力</div></div><span class="ghost-no">07</span></div>
  <div class="grid-2"><div class="card"><h3>最值得学的四项能力</h3><ol><li><b>选题判断：</b>从变化和反差中发现问题。</li><li><b>真实验证：</b>用任务和结果支撑结论。</li><li><b>明确立场：</b>敢于判断，同时说明边界。</li><li><b>内容资产化：</b>把单篇文章变成栏目、清单和复测。</li></ol></div><div class="card"><h3>学习顺序</h3><ol><li>先学习观察和记录，不急着模仿语言。</li><li>再学习证据组织和文章结构。</li><li>随后练习标题、开头和结尾。</li><li>最后才提炼属于自己的表达风格。</li></ol></div></div>
  <div class="analysis-summary"><h4>我要把方法学到什么程度</h4><p>目标不是写得越来越像他，而是能在自己的领域独立完成：发现问题、收集证据、形成判断、说明边界、推动读者行动。</p><p>当你换一个题材仍能使用这些方法，并能根据自己的经验做出调整，方法才真正变成了你的能力。</p></div>
</section>

<section class="chapter" id="growth">
  <div class="chapter-head"><span class="chapter-no">08</span><div><h2>运营增长</h2><div class="chapter-sub">涨粉策略、栏目规划、内容分发与竞品研究</div></div><span class="ghost-no">08</span></div>
  <div class="card"><h3>内容供给趋势</h3>{line_chart(articles)}</div>
  <div class="metrics">{metric("文章数",article_count,"有效正文")}{metric("发布间隔",f"{summary.get('publish_interval_days', {}).get('median','未知')} 天","中位数")}{metric("主题方向",len(theme_items),"内容地图")}{metric("证据覆盖",f"{evidence_articles}/{article_count}","文章级识别")}</div>
  <div class="analysis-summary"><h4>值得学习：用栏目代替随机更新</h4><p>更新节奏偏高频，但真正值得学习的是把快讯、深度实测、工作流模板和原则观点组合起来，让每类内容承担不同任务。</p><p><b>怎么学：</b>先选择两个固定栏目连续做四周，一个负责及时性，一个负责长期价值。四周后复盘选题来源、制作成本和可持续性，再决定是否扩展栏目。</p></div>
  <div class="grid-2 rhythm-grid" style="margin-top:18px"><div class="card"><h3>他如何保持连续输出</h3><p>{esc(release_summary)}</p><div class="weekday-bars">{weekday_bars}</div><div class="method-note"><b>观察结论：</b>高频更新来自产品变化、真实测试和连续反馈共同供给选题。值得学习的是建立稳定的选题来源，不是机械复制每天发布。</div></div><div class="rhythm-stack"><div class="card rhythm-advice"><h3>你应该选择什么节奏</h3><ol><li><b>刚开始：</b>每周 1 篇深度内容。先练习把选题、证据和结构做完整。</li><li><b>已经稳定：</b>每周 1 篇深度内容 + 1 篇短判断，兼顾长期价值与及时性。</li><li><b>遇到热点：</b>先发布短判断，7 天后补充实测或复盘，不要求首篇覆盖所有信息。</li><li><b>判断标准：</b>更新频率不能高于证据积累速度。没有新任务、新证据或新判断时，不为更新而更新。</li></ol></div><div class="analysis-summary"><h4>怎么把他的节奏变成你的节奏</h4><p>先连续四周记录每篇内容实际需要的选题、研究、写作和修改时间，再决定频率。能稳定完成并保留复盘时间的节奏，才是你的可持续节奏。</p><p><b>练习：</b>建立一个“1+1”内容循环：一篇解决长期问题的主内容，加一篇来自评论、测试或新变化的轻内容。连续执行四周，再根据负担调整，而不是直接模仿作者的日更频率。</p></div></div></div>
  <div class="grid-2" style="margin-top:18px"><div class="card"><h3>我应该学习什么增长方法</h3><ol><li><b>入口内容：</b>用及时且鲜明的判断让新读者认识你。</li><li><b>信任内容：</b>用真实任务、成本和失败过程证明能力。</li><li><b>工具内容：</b>把经验整理成清单、模板和可执行步骤。</li><li><b>定位内容：</b>持续表达稳定的原则和判断标准。</li></ol></div><div class="card"><h3>我要怎么建立栏目</h3><ol><li>选择一个你能长期获取素材的专业领域。</li><li>设计一个及时栏目和一个长期栏目。</li><li>为每个栏目固定选题来源、文章结构和更新周期。</li><li>连续完成四期后，再决定保留、调整或扩展。</li></ol></div></div>
  <div class="card" style="margin-top:18px"><h3>我要怎么学习内容迭代</h3><div class="grid-3"><div><b>写之前</b><p>明确这篇内容要解决谁的什么问题，并准备一个核心判断和至少一种证据。</p></div><div><b>发布之后</b><p>收集读者提出的具体问题，判断哪些疑问说明文章表达不清，哪些可以发展成新选题。</p></div><div><b>一周之后</b><p>补充新的案例、失败条件或变化，把一次性内容发展成复测、系列或工具资产。</p></div></div></div>
  <div class="grid-2" style="margin-top:18px"><div class="card"><h3>我应该从竞品学习什么</h3><ul><li>他们分别服务什么读者</li><li>用哪些栏目持续提供价值</li><li>如何把标题与具体问题连接</li><li>使用什么证据建立可信度</li><li>有哪些内容需求尚未被满足</li></ul></div><div class="card"><h3>我要怎么做竞品研究</h3><ol><li>每个账号选择 5 篇代表内容。</li><li>记录选题、标题公式、结构、证据和读者价值。</li><li>找出重复出现的方法与尚未覆盖的空位。</li><li>选择与你能力匹配的方法，转成自己的栏目实验。</li></ol></div></div>
</section>

<section class="chapter" id="reuse">
  <div class="chapter-head"><span class="chapter-no">09</span><div><h2>学习与迁移</h2><div class="chapter-sub">把看懂转化为可执行练习，再形成自己的方法</div></div><span class="ghost-no">09</span></div>
  <div class="action-grid">{opportunity_html}</div>
  <div class="black-quote">学习方法，不复制答案。复制选题判断、验证过程、文章结构和复盘机制；保留自己的经历、资源、价值观与表达习惯。</div>
  <div class="card" style="margin-top:18px"><h3>四周学习计划</h3><div class="grid-2"><div><b>第 1 周：观察</b><p>拆解 5 篇代表文章，只记录选题来源、核心判断、证据、结构和结尾动作。</p><b>第 2 周：局部练习</b><p>选择自己的题材，分别练习一次选题方法、证据方法和文章结构。</p></div><div><b>第 3 周：对照改写</b><p>用同一主题写两个版本：一个使用学到的方法，一个按原有习惯写，比较差异。</p><b>第 4 周：形成原则</b><p>保留适合自己的部分，删除依赖他人经历和资源的部分，形成一页个人创作原则。</p></div></div></div>
</section>

<footer class="page-notes">
  <p><b>来源说明：</b>基于 {article_count} 篇公开文章的正文、标题、发布时间及图片等公开信息整理，样本时间为 {esc(date_range[0])} 至 {esc(date_range[-1])}。</p>
  <p><b>免责声明：</b>本看板仅用于内容学习与方法研究，结论为基于有限样本的归纳，不代表作者本人观点，也不构成效果或增长承诺。</p>
</footer>
<script type="application/json" id="analysis-data">{embedded}</script>
<script>
const links=[...document.querySelectorAll('nav a')];
const sections=[...document.querySelectorAll('.chapter')];
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{{
 if(entry.isIntersecting){{links.forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}}
}}),{{rootMargin:'-20% 0px -70% 0px'}});
sections.forEach(section=>observer.observe(section));
</script>
</main></body></html>"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
