#!/usr/bin/env python3
"""微信公众号 HTML 合规校验器。

把 SKILL.md 里"必须遵守的平台限制"从模型自觉变成确定性兜底。
排版生成后必跑：检查禁用标签/属性/样式，并核查文字节点是否用
<span leaf=""> 包裹（公众号编辑器粘贴后保持样式的关键）。

用法:
    validate_gzh_html.py <file.html>
    validate_gzh_html.py --stdin < file.html
    validate_gzh_html.py <file.html>  # 固定运行墨青白名单行内强调门禁

退出码: 1 = 有 ERROR（会被公众号过滤或粘贴后样式丢失）; 0 = 通过。
"""

import argparse
import re
import sys
from html.parser import HTMLParser

# (正则, 级别, 说明) —— ERROR 会被公众号编辑器过滤掉或导致样式失效
FORBIDDEN = [
    (re.compile(r"<style[\s>]", re.I), "ERROR", "<style> 标签会被过滤，样式必须内联"),
    (re.compile(r"<script[\s>]", re.I), "ERROR", "<script> 标签会被过滤"),
    (re.compile(r"</?div[\s>]", re.I), "ERROR", "<div> 会被改写，请用 <section>"),
    (re.compile(r"<link[\s>]", re.I), "ERROR", "外部 <link>（CSS/字体）会被过滤"),
    (re.compile(r"\sclass\s*=", re.I), "ERROR", "class 属性会被剥离，请用内联 style"),
    (re.compile(r"\sid\s*=", re.I), "ERROR", "id 属性会被剥离"),
    (re.compile(r"position\s*:\s*(fixed|absolute|sticky)", re.I), "ERROR",
     "position fixed/absolute/sticky 不被支持"),
    (re.compile(r"float\s*:", re.I), "ERROR", "float 不被支持"),
    (re.compile(r"@media", re.I), "ERROR", "@media 媒体查询不被支持"),
    (re.compile(r"@keyframes", re.I), "ERROR", "@keyframes 动画不被支持"),
    (re.compile(r"@import", re.I), "ERROR", "@import 不被支持"),
    (re.compile(r"display\s*:\s*grid", re.I), "ERROR", "display:grid 不被支持，请用 flex"),
    (re.compile(r"var\s*\(\s*--", re.I), "ERROR", "CSS 变量 var(--x) 不被支持，请写死值"),
    (re.compile(r"url\s*\(\s*['\"]?https?://[^)]*\.(woff2?|ttf|otf|eot)", re.I),
     "ERROR", "外部字体不被支持"),
]

CJK = re.compile(r"[一-鿿㐀-䶿]")
SKIP_TAGS = {"head", "title", "style", "script"}  # 不参与公众号正文粘贴的区域
# 中文字后紧跟半角逗号/分号/叹号/问号（应改全角）；只查"中文在前"避免中英混排误伤
HALF_PUNCT = re.compile(r"[一-鿿㐀-䶿][,;!?]")
ASCII_QUOTE = re.compile(r"[\"']")
# 代码区特征：等宽字体或 white-space:pre —— 其内半角符号是正常的
CODE_STYLE = re.compile(r"monospace|white-space\s*:\s*pre|courier|consolas|sf mono", re.I)
# 直角引号（规则 9b：正文禁止用直角引号「」『」，应改弯引号；代码区豁免）
CJK_BRACKET = re.compile(r"[「」『』]")
# font-family 声明（规则 9a：主题字体只在全局容器声明一次，组件不重复）
FONT_FAMILY_DECL = re.compile(r"font-family\s*:", re.I)
# 只检查内联背景声明，跳过 CSS 注释、字符串和图片 URL 中的示例文字。
CSS_NON_FUNCTION = re.compile(
    r"/\*.*?\*/|url\(\s*(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|(?:\\.|[^)])*)\s*\)"
    r"|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'", re.I | re.S)
GRADIENT_BACKGROUND = re.compile(
    r"(?:^|;)\s*background(?:-image)?\s*:[^;]*\b"
    r"(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(", re.I)


class LeafChecker(HTMLParser):
    """检查每个非空文本节点是否处于 <span leaf> 内。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []           # [(tag, is_leaf, is_code)]
        self.leaf_depth = 0       # 处于 span[leaf] 内的嵌套计数
        self.code_depth = 0       # 处于代码区（等宽/pre）内的嵌套计数
        self.span_leaf_count = 0  # 全文 span leaf 总数
        self.unwrapped = []       # (文本片段, 父标签) —— 未被 leaf 包裹的中文文本
        self.half_punct = []      # 正文里疑似半角标点的片段
        self.gradient_backgrounds = []  # (行, 列, 标签) —— 内联渐变背景
        self.cjk_bracket = []     # 正文里的直角引号「」『』（规则 9b 禁止，代码区豁免）
        self.font_family_decls = []  # 非代码区声明 font-family 的元素（规则 9a 应只在全局容器）

    def handle_starttag(self, tag, attrs):
        ad = dict(attrs)
        style = ad.get("style", "") or ""
        if tag not in SKIP_TAGS and not any(t in SKIP_TAGS for t, _, _ in self.stack):
            if GRADIENT_BACKGROUND.search(CSS_NON_FUNCTION.sub("", style)):
                line, col = self.getpos()
                self.gradient_backgrounds.append((line, col + 1, tag))
            # 墨青主题例外：全局容器、短标签与 /// END 可按母版声明字体。
            # 其余正文/组件区域不得为了局部造字形再覆盖字体。
            normalized_style = style.lower().replace(" ", "")
            is_master_font_exception = (
                "font-size:10px" in normalized_style and "font-weight:700" in normalized_style
            ) or (
                "font-style:italic" in normalized_style and "font-size:11px" in normalized_style
            )
            if (FONT_FAMILY_DECL.search(style)
                    and not CODE_STYLE.search(style)
                    and not is_master_font_exception):
                self.font_family_decls.append(tag)
        is_leaf = tag == "span" and "leaf" in ad
        is_code = bool(CODE_STYLE.search(style))
        if is_leaf:
            self.span_leaf_count += 1
            self.leaf_depth += 1
        if is_code:
            self.code_depth += 1
        self.stack.append((tag, is_leaf, is_code))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, was_leaf, was_code in self.stack[i:]:
                    if was_leaf:
                        self.leaf_depth -= 1
                    if was_code:
                        self.code_depth -= 1
                del self.stack[i:]
                break

    def handle_data(self, data):
        text = data.strip()
        if not text or not CJK.search(text):
            return
        if any(t in SKIP_TAGS for t, _, _ in self.stack):
            return  # <head>/<title>/<style>/<script> 内文字不进公众号正文
        if self.leaf_depth == 0:
            parent = self.stack[-1][0] if self.stack else "(root)"
            snippet = text[:24] + ("…" if len(text) > 24 else "")
            self.unwrapped.append((snippet, parent))
        if self.code_depth == 0 and (HALF_PUNCT.search(text)
                                     or ASCII_QUOTE.search(text)):
            snippet = text[:24] + ("…" if len(text) > 24 else "")
            self.half_punct.append(snippet)
        if self.code_depth == 0 and CJK_BRACKET.search(text):
            snippet = text[:24] + ("…" if len(text) > 24 else "")
            self.cjk_bracket.append(snippet)


def validate(html, name="<input>"):
    errors, warnings = [], []

    for rx, level, msg in FORBIDDEN:
        hits = len(rx.findall(html))
        if hits:
            (errors if level == "ERROR" else warnings).append(
                f"{msg}（命中 {hits} 处）")

    checker = LeafChecker()
    try:
        checker.feed(html)
    except Exception as e:  # 容错：解析失败不致命，只提示
        warnings.append(f"HTML 解析中断: {e}")

    if checker.gradient_backgrounds:
        sample = "；".join(f"第 {line} 行 {col} 列 <{tag}>"
                           for line, col, tag in checker.gradient_backgrounds[:5])
        warnings.append(
            f"[darkmode-no-gradient] {len(checker.gradient_backgrounds)} 处渐变背景，"
            f"可能触发公众号内容结构检测；文字/卡片背景建议改为主题内纯色或 rgba 纯色，"
            f"装饰渐变也需人工确认。位置：{sample}")

    has_cjk = bool(CJK.search(html))
    if has_cjk and checker.span_leaf_count == 0:
        errors.append("全文没有任何 <span leaf=\"\"> 包裹——"
                      "粘贴到公众号后样式会大面积丢失")
    elif checker.unwrapped:
        sample = "；".join(f"「{s}」(在 <{p}> 内)"
                           for s, p in checker.unwrapped[:5])
        warnings.append(
            f"{len(checker.unwrapped)} 处中文文本未被 <span leaf> 包裹，"
            f"样式可能丢失。例：{sample}")

    if checker.half_punct:
        sample = "；".join(f"「{s}」" for s in checker.half_punct[:5])
        warnings.append(
            f"{len(checker.half_punct)} 处正文疑似半角标点/英文引号，应改中文全角"
            f"（代码块内不计）。例：{sample}")

    if checker.cjk_bracket:
        sample = "；".join(f"「{s}」" for s in checker.cjk_bracket[:5])
        warnings.append(
            f"{len(checker.cjk_bracket)} 处正文出现直角引号「」『』，按规则 9b "
            f"应使用弯引号“”‘’（代码块内不计；原文本身用直角引号除外）。例：{sample}")

    if len(checker.font_family_decls) > 1:
        tags = sorted(set(checker.font_family_decls))
        warnings.append(
            f"{len(checker.font_family_decls)} 处非母版例外的元素声明了 font-family "
            f"（墨青只允许全局容器、短标签与 /// END 的既有字体例外；代码组件可用 monospace）。"
            f"涉及标签：{tags[:6]}")

    return errors, warnings, checker.span_leaf_count


# 唯一主题的行内强调门禁。规则来源：references/theme-ink-teal-tech.md 4.3，
# 逐字节取证自母版及同作者五篇成品；本技能不接受其他主题。
THEME_ID = "ink-teal-tech"
THEME_WHITELIST = {"E4": 5, "E3": 3, "E6": 3, "E5": 5, "E7": 3}

EMPH_DECL = re.compile(
    r"font-weight\s*:\s*(?:500|600|700|800|900|bold)|border-bottom|text-decoration"
    r"|(?:repeating-)?(?:linear|radial)-gradient|background(?:-color)?\s*:\s*(?:#|rgb\s*\()",
    re.I,
)


def classify_emph(style):
    """把一个行内强调 span 的 style 归到 4.3 的 E1–E7；不在白名单返回 None。"""
    s = style.lower().replace(" ", "")
    if "repeating-linear-gradient" in s:
        return "E6"
    if "radial-gradient" in s:
        return "E4"
    if "linear-gradient" in s and "58%" in s:
        return "E5"
    if "border-bottom" in s:
        if "#4fa883" in s or "rgb(79,168,131)" in s:
            return "E3"
        if "font-weight:600" in s and ("#111827" in s or "rgb(17,24,39)" in s):
            return "E2"
    if "background" in s and ("#d3f1e2" in s or "rgb(211,241,226)" in s):
        return "E7"
    if (
        "font-weight:700" in s
        and ("#111827" in s or "rgb(17,24,39)" in s)
        and not any(k in s for k in ("border-bottom", "gradient", "text-decoration", "background:"))
    ):
        return "E1"
    return None


def _exempt_paragraph(style, text):
    """代码 / Prompt、图注、纯英文段落不参与长段落强调门禁。"""
    s = style.lower().replace(" ", "")
    if "monospace" in s or "white-space:pre" in s or "font-size:12px" in s:
        return True
    if text.lstrip().startswith("@") or text.lstrip().startswith("提示词"):
        return True
    ascii_ratio = sum(1 for ch in text if ord(ch) < 128) / max(1, len(text))
    return ascii_ratio > 0.7


class EmphasisChecker(HTMLParser):
    """收集每个 <p> 的文本、样式与其中的行内强调 span。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pdepth = 0
        self.current = None
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        style = dict(attrs).get("style", "") or ""
        if tag == "p":
            if self.pdepth == 0:
                self.current = {"style": style, "text": "", "emph": []}
            self.pdepth += 1
        elif tag == "span" and self.pdepth > 0 and self.current is not None:
            if EMPH_DECL.search(style):
                self.current["emph"].append((classify_emph(style), style))

    def handle_data(self, data):
        if self.pdepth > 0 and self.current is not None:
            self.current["text"] += data

    def handle_endtag(self, tag):
        if tag == "p" and self.pdepth > 0:
            self.pdepth -= 1
            if self.pdepth == 0 and self.current is not None:
                self.paragraphs.append(self.current)
                self.current = None


def theme_checks(html):
    """运行墨青测评风唯一的正文行内强调门禁。"""
    checker = EmphasisChecker()
    checker.feed(html)
    errors, warnings = [], []
    zero, unknown, over = [], [], []
    counts = {}
    for p in checker.paragraphs:
        text = re.sub(r"\s+", " ", p["text"]).strip()
        for code, style in p["emph"]:
            if code is None:
                unknown.append(style)
            else:
                counts[code] = counts.get(code, 0) + 1
        if len(p["emph"]) > 2:
            over.append(text[:24])
        if len(text) >= 40 and not _exempt_paragraph(p["style"], text) and not p["emph"]:
            zero.append(text[:24])
    if zero:
        sample = "；".join(f"「{t}」" for t in zero[:5])
        errors.append(
            f"[封闭白名单] {len(zero)} 个叙述型长段落（≥40 字）0 处行内强调；"
            f"按主题 4.3 每个长段落至少 1 处，须用 E1–E7 现成骨架。例：{sample}")
    if unknown:
        sample = "；".join(s[:70] for s in unknown[:3])
        errors.append(
            f"[封闭白名单] {len(unknown)} 处行内强调样式不属于 4.3 E1–E7 默认白名单"
            f"（部分在母版仅出现 1 次或属标题 / Prompt 层，主题已明确不纳入）；"
            f"新文章只能照抄 E1–E7 骨架。例：{sample}")
    if over:
        warnings.append(
            f"[封闭白名单] {len(over)} 个段落行内强调超过 2 处（主题 4.3 每段 1–2 处）。例：{over[:3]}")
    for code, limit in THEME_WHITELIST.items():
        if counts.get(code, 0) > limit:
            warnings.append(f"[封闭白名单] {code} 用了 {counts[code]} 处，超过上限 {limit} 处")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="HTML 文件路径")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读取")
    ap.add_argument(
        "--theme",
        default=THEME_ID,
        choices=[THEME_ID],
        help="兼容旧调用的固定主题参数；本技能仅支持 ink-teal-tech",
    )
    args = ap.parse_args()

    if args.stdin or not args.file:
        html = sys.stdin.read()
        name = "<stdin>"
    else:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            html = f.read()
        name = args.file

    errors, warnings, leaf_n = validate(html, name)
    t_err, t_warn = theme_checks(html)
    errors += t_err
    warnings += t_warn

    print(f"📋 墨青测评风公众号 HTML 合规校验: {name}")
    print(f"   主题门禁: {THEME_ID}")
    print(f"   span leaf 包裹: {leaf_n} 处")
    if errors:
        print(f"\n❌ ERROR ×{len(errors)}（必须修复，否则粘贴后失效）:")
        for e in errors:
            print(f"   • {e}")
    if warnings:
        print(f"\n⚠️  WARNING ×{len(warnings)}（建议检查）:")
        for w in warnings:
            print(f"   • {w}")
    if not errors and not warnings:
        print("\n✅ 完全合规，可直接粘贴到公众号编辑器")
    elif not errors:
        print("\n✅ 无致命问题，可粘贴（warning 请人工确认）")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
