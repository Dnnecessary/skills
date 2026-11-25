# Ink Teal Tech WeChat Layout Skill

This is a single-style WeChat layout skill. It supports only `ink-teal-tech` and converts Markdown, Word, PDF, plain text, or existing article content into inline HTML that can be pasted into the WeChat editor.

## Fixed contract

- One theme: `ink-teal-tech`.
- One source of visual truth: the supplied master article and five articles by the same author.
- One routing rule: an approved master component plus the same trigger in source content; otherwise use body text with E1-E7 inline emphasis.
- One cover system: the fixed graduate-girl IP, fixed intro copy, and scene-based SVG SMIL.
- One validator: `validate_gzh_html.py` always enforces the Ink Teal whitelist and rejects other theme IDs.

Other themes, theme selection, theme generation, generic component fallbacks, cross-theme components, and semantic component invention are intentionally unsupported.

See `SKILL.md` for the operating workflow and `references/ink-teal-source-evidence.md` for source evidence.
