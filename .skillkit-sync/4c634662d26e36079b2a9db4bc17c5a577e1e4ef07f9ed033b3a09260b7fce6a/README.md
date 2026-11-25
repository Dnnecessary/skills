# 作者内容方法论分析 Skill

这是一个面向 Codex 的内容分析技能，用来基于多篇作者、博主、公众号或品牌文章正文，生成可复核的作者方法论分析。它不仅输出“这个作者怎么写”，也会进一步回答“我应该学习什么、我要怎么学、哪些地方不能照搬”。

## 适用场景

- 分析公众号、博客、品牌号或个人作者的多篇文章。
- 提炼作者定位、选题系统、分析框架、判断标准、表达模板和写作 SOP。
- 从标题、结构、证据、案例、语言风格、行动引导和发布节奏中总结可迁移方法。
- 生成学习者视角的 Markdown 报告、独立文案框架、可审计数据和交互 HTML 看板。

## 默认产物

运行技能时，所有产物会写入用户提供的 `output_dir`：

```text
<output_dir>/
  <博主>-方法论报告.md
  <博主>-文案框架.md
  <博主>-分析数据.json
  <博主>-文章特征.csv
  <博主>-方法论看板.html
  <博主>-飞书同步.json
  <博主>-竞品标题样本.json
```

其中 `<博主>-分析数据.json` 和 `<博主>-文章特征.csv` 是可审计交付物；报告、HTML 看板和飞书同步内容都应基于同一份分析数据生成。

## 工作流

1. 建立样本清单，读取 Markdown、TXT、DOCX 或可提取文本的 PDF。
2. 使用 `scripts/analyze_corpus.py` 生成确定性统计、文章级特征、去重信息和样本指纹。
3. 按 `references/data-analysis-framework.md` 完成解释性分析，区分可计算事实与主观归纳。
4. 按 `references/report-template.md` 生成主报告。
5. 按 `references/copywriting-framework-template.md` 生成独立文案框架。
6. 使用 `scripts/generate_dashboard.py` 生成学习者视角的 HTML 看板。
7. 在来源允许且无敏感风险时，默认同步到飞书文档。
8. 使用 `scripts/validate_outputs.py` 校验数据、报告、HTML 和同步元数据的一致性。

## 快速使用

在 Codex 中可以这样调用：

```text
使用 $author-methodology-analysis 分析这些文章，生成方法论报告、文案框架和学习者视角 HTML 看板，重点说明我应该学习什么以及我要怎么学。
```

确定性分析脚本也可以单独运行：

```bash
python3 scripts/analyze_corpus.py \
  --input "<input_dir>" \
  --output "<output_dir>"
```

生成 HTML 看板：

```bash
python3 scripts/generate_dashboard.py \
  --data "<output_dir>/<博主>-分析数据.json" \
  --output "<output_dir>/<博主>-方法论看板.html"
```

校验输出：

```bash
python3 scripts/validate_outputs.py "<output_dir>"
```

## 目录结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── analysis-data.schema.json
│   ├── copywriting-framework-template.md
│   ├── data-analysis-framework.md
│   ├── interactive-dashboard-template.md
│   └── report-template.md
└── scripts/
    ├── analyze_corpus.py
    ├── artifact_names.py
    ├── generate_dashboard.py
    └── validate_outputs.py
```

## 设计原则

- 不只看标题，必须基于正文样本分析。
- 少于 5 篇文章时只做描述性分析；少于 3 篇时不输出稳定趋势或风格结论。
- 词频、标题标签和结构统计来自脚本，不能由模型重新估算。
- 主题、立场、读者画像和金句风格等主观标签必须带证据、规则和置信度。
- 看板默认站在学习者视角，避免写成作者评分、自检或增长后台。
- 不分析平台后台阅读、分享、点赞、收藏、关注或转化表现。
- 学习结构和方法，不复刻作者独特表达，不冒充作者。

## 关联文章

- [用 AI 拆解公众号作者的方法论](https://mp.weixin.qq.com/s/fG7mdtQeO03lxcS406apow)

