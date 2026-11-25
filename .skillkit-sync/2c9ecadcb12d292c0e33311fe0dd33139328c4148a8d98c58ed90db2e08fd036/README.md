# 墨青测评风公众号排版 Skill

这是一个只保留“墨青测评风”的微信公众号排版技能。它将 Markdown、Word、PDF、纯文本或已有正文转为可直接粘贴到公众号编辑器的内联 HTML。

## 固定规则

- 唯一主题：`ink-teal-tech`。
- 唯一组件来源：母版与五篇同作者原作的逐字节证据。
- 唯一路由：白名单组件 + 原文相同触发条件；不满足时回落为正文和 E1–E7 行内强调。
- 唯一封面：固定毕业女孩 IP、固定介绍语、场景化 SVG SMIL 动画。
- 唯一校验：`validate_gzh_html.py` 默认运行墨青白名单门禁，拒绝其他主题标识。

不支持其他主题、主题选择、主题生成器、通用组件补齐、跨主题组件或按语义自由造卡。

## 目录

```text
SKILL.md                                  # 唯一工作流
references/theme-ink-teal-tech.md         # 母版白名单与完整组件骨架
references/ink-teal-source-evidence.md    # 母版与五篇原作证据册
references/format-normalize.md            # 输入归一化
assets/theme-assets/ink-teal-tech/        # IP、封面、词内动画、圈注资产
scripts/validate_gzh_html.py              # 公众号与墨青门禁
scripts/component_lint.py                 # 母版组件源头检查
scripts/wrap_preview.py                   # 复制预览页
```

## 校验

```bash
python3 scripts/component_lint.py .
python3 scripts/validate_gzh_html.py --theme ink-teal-tech output.html
python3 scripts/wrap_preview.py output.html
```

产物必须是 `<section>...</section>` 片段。校验必须 0 ERROR；E4、E5、E6 的渐变告警仅在确认样式属于母版白名单时保留。

## 维护

任何新增组件、样式或动画规则，必须先在指定母版或同作者原作中取得来源、签名、频率和触发条件四项证据，并记录到 `references/ink-teal-source-evidence.md`，再经用户确认后更新主题规则库。
