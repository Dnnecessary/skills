# 公众号排版组件库 —— GitHub 极客蓝

> **使用说明**：本组件库为「GitHub 极客蓝（GitHub）」主题，复刻自 md2wechat 的 `github-readme` 真实主题输出。所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：GitHub 蓝（`#0969da`）+ 纯白 + 浅蓝底（`#e1edfb`）+ 浅灰底（`#f6f8fa`）+ 细边框 + 轻阴影。卡片化、药丸标签、圆角 12~16px、编号系统完整的现代文档感排版。正文关键词用 GitHub 蓝下划线（`border-bottom:2px solid #0969da;font-weight:600;`）标记。适合技术教程、产品评测、开发工具盘点、AI 工具介绍、数据复盘、案例拆解类文章。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id/`<div>`、`position:fixed/absolute/sticky`、`float`、`@media`/`@keyframes`、`display:grid`、CSS 变量 `var(--x)`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>/<h3>` 等基础标签
> - font-size ≤ 24px；正文强调用小标签/左竖条/蓝下划线，**不用四周虚线框**（dashed）
>
> **复刻时的刻意改动**（与原 HTML 的差异，均为平台合规要求）：
> - 原主题多处使用 `linear-gradient` 背景，已全部替换为纯色近似值（`#f0f6fc` 淡蓝过渡底、`#fbfcfd` 微灰底），避免触发公众号暗色模式 `darkmode-no-gradient` 检测弹窗
> - 原 `display:grid` 布局已改为 `flex + gap`（旧内核下 gap 可能失效，间距退化为紧凑排列，结构不塌）
> - 原 25/26px 大数字统一压到 24px 以内；`<button>`/`<svg>`/`<pre>` 高亮代码块分别改为 section 按钮卡、纯文字、通用库代码块
> - 非 900 的字重（750/760/850）归一为 700/800，兼容老内核

---

## 设计变量速查表

```
主色（GitHub 蓝）： #0969da（标题强调 / 编号 / 药丸文字 / 下划线 / 按钮）
引用竖条蓝：       #218bff（仅引用块左边条）
浅蓝底：           #e1edfb（药丸标签底 / 高亮 / 强调卡）
中蓝底：           #cee1f8（图标圆底 / 编号圆底 / 步骤连线）
淡蓝边框：         #b0cff3（强调卡的边框，比灰边框更醒目）
淡蓝过渡底：       #f0f6fc（原渐变的纯色替代，强调卡 / hero 头部）
微灰底：           #fbfcfd（原"白→灰"渐变的纯色替代，内容卡）
浅灰底：           #f6f8fa（次要标签底 / 引用块 / FAQ 问题行 / 表头）
正文色：           #1f2328
次强调文字：       #53565a / #57606a（说明段 / 引用文字）
辅助文字色：       #75767a（小标签 / 说明 / 英文小字）
细边框色：         rgba(208,215,222,0.18)（卡片边框，近乎隐形，靠阴影撑层次）
实线边框：         #d8dee4（引用块 / h3 下边线）/#d1d9e0（表格线）
阴影：             0 2px 6px rgba(31,35,40,0.06)（全主题统一轻阴影）
蓝底白字按钮：     #0969da（原渐变按钮的纯色替代）
正文字号：         16px
行高：             1.6~1.75
圆角：             卡片 12px / 大卡与按钮 16px / 药丸 999px
```

字体栈：`-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif`

---

## 组件 1 全局容器

```html
<section style="background-color:#ffffff;border-radius:12px;padding:16px;max-width:680px;margin:0 auto;width:100%;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;color:#1f2328;">

  <!-- 所有组件放在这里 -->

</section>
```

---

## 组件 2 Hero 封面卡

> 文章开头的"折页"卡：分类药丸 + 日期 + 大标题 + 装饰短线 + 一句话简介 + 编号要点行，可选配封面图（组件 30）与底部产品标签行。**标题 24px 是全篇唯一最大字**。编号要点行取自文章核心脉络（2~4 条）。

```html
<section style="margin:0 0 34px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:16px;overflow:hidden;box-shadow:0 2px 6px rgba(31,35,40,0.06);width:100%;">
  <section style="padding:24px 22px 18px;background:#f0f6fc;">
    <section style="display:flex;align-items:center;gap:8px;margin-bottom:14px;flex-wrap:wrap;">
      <span style="width:10px;height:10px;background:#cee1f8;border:1px solid #b0cff3;border-radius:3px;flex-shrink:0;"><span leaf=""><br></span></span>
      <span style="display:inline-block;padding:4px 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;color:#0969da;background:#e1edfb;border-radius:999px;"><span leaf="">{{分类标签，如：产品观察}}</span></span>
      <span style="font-size:13px;color:#75767a;font-weight:700;letter-spacing:0.8px;padding:2px 8px;border:1px solid rgba(208,215,222,0.18);border-radius:999px;background:#ffffff;"><span leaf="">{{日期，如：2026.10}}</span></span>
    </section>
    <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 10px;line-height:1.16;letter-spacing:-0.05em;"><span leaf="">{{文章主标题}}</span></p>
    <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
      <span style="width:26px;height:2px;background:#0969da;border-radius:999px;"><span leaf=""><br></span></span>
      <span style="width:14px;height:2px;background:#b0cff3;border-radius:999px;"><span leaf=""><br></span></span>
      <span style="width:36px;height:1px;background:rgba(208,215,222,0.18);border-radius:999px;"><span leaf=""><br></span></span>
    </section>
    <p style="font-size:13px;color:#53565a;margin:0;line-height:1.75;letter-spacing:0.2px;"><span leaf="">{{一句话简介，交代这篇文章解决什么问题}}</span></p>
    <section style="display:flex;flex-direction:column;gap:8px;margin-top:14px;">
      <section style="display:flex;align-items:flex-start;gap:8px;padding:9px 10px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);">
        <span style="font-size:13px;font-weight:900;color:#0969da;flex-shrink:0;"><span leaf="">01</span></span>
        <span style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.52;"><span leaf="">{{要点一}}</span></span>
      </section>
      <section style="display:flex;align-items:flex-start;gap:8px;padding:9px 10px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);">
        <span style="font-size:13px;font-weight:900;color:#0969da;flex-shrink:0;"><span leaf="">02</span></span>
        <span style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.52;"><span leaf="">{{要点二}}</span></span>
      </section>
      <section style="display:flex;align-items:flex-start;gap:8px;padding:9px 10px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);">
        <span style="font-size:13px;font-weight:900;color:#0969da;flex-shrink:0;"><span leaf="">03</span></span>
        <span style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.52;"><span leaf="">{{要点三}}</span></span>
      </section>
    </section>
  </section>
  <section style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:12px 22px 14px;background:#f0f6fc;border-top:1px solid rgba(208,215,222,0.18);">
    <p style="display:inline-flex;align-items:center;font-size:13px;color:#1f2328;margin:0;font-weight:700;letter-spacing:0.8px;padding:3px 10px;border-radius:999px;border:1px solid #b0cff3;background:#e1edfb;"><span leaf="">{{产品名/栏目名}}</span></p>
    <section style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-start;">
      <span style="background:#ffffff;padding:3px 9px;border-radius:999px;font-size:13px;color:#75767a;font-weight:700;letter-spacing:0.2px;border:1px solid rgba(208,215,222,0.18);"><span leaf="">{{关键词标签一}}</span></span>
      <span style="background:#ffffff;padding:3px 9px;border-radius:999px;font-size:13px;color:#75767a;font-weight:700;letter-spacing:0.2px;border:1px solid rgba(208,215,222,0.18);"><span leaf="">{{关键词标签二}}</span></span>
    </section>
  </section>
</section>
```

> **注意**：封面图（组件 30）插在头部区与底部标签行之间；没有配图就整块省略，不要留空 section。

---

## 组件 3 阅读导航（目录卡）

> 3 个及以上章节时生成，展示**精选 3 个核心看点**，不是全量章节列表。编号蓝色加粗，每行右下配一句灰色说明。

```html
<section style="margin:0 0 30px;padding:18px;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <p style="display:inline-block;padding:4px 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;color:#0969da;background:#e1edfb;border-radius:999px;margin:0 0 12px;"><span leaf="">阅读导航</span></p>
  <section style="display:flex;flex-direction:column;gap:12px;">
    <section style="display:flex;align-items:flex-start;gap:12px;padding-bottom:10px;border-bottom:1px solid rgba(208,215,222,0.18);">
      <p style="margin:0;min-width:34px;font-size:13px;font-weight:800;color:#0969da;letter-spacing:0.6px;"><span leaf="">01</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{看点一标题}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{看点一说明}}</span></p>
      </section>
    </section>
    <section style="display:flex;align-items:flex-start;gap:12px;padding-bottom:10px;border-bottom:1px solid rgba(208,215,222,0.18);">
      <p style="margin:0;min-width:34px;font-size:13px;font-weight:800;color:#0969da;letter-spacing:0.6px;"><span leaf="">02</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{看点二标题}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{看点二说明}}</span></p>
      </section>
    </section>
    <section style="display:flex;align-items:flex-start;gap:12px;padding-bottom:10px;">
      <p style="margin:0;min-width:34px;font-size:13px;font-weight:800;color:#0969da;letter-spacing:0.6px;"><span leaf="">03</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{看点三标题}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{看点三说明}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 4 章节编号卡（章节标题）

> 每个一级章节（`##`）的开头。圆形大编号（01/02/03…，结语用 `∞`）+ 中文标题 + 英文小字标签（实测→TEST、教程→TUTORIAL、总结→SUMMARY…）。第一章 `margin:16px 0 20px`，后续章节 `margin:36px 0 20px`。

```html
<section style="display:flex;align-items:center;gap:12px;margin:36px 0 20px;padding:14px 16px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="display:flex;align-items:center;justify-content:center;text-align:center;flex-shrink:0;width:56px;height:56px;background:#f0f6fc;border:1px solid #b0cff3;border-radius:999px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
    <p style="margin:0;font-size:24px;font-weight:900;color:#0969da;line-height:1;letter-spacing:-1.1px;"><span leaf="">{{01}}</span></p>
  </section>
  <span style="width:2px;border-radius:999px;background:#cee1f8;flex-shrink:0;"><span leaf=""><br></span></span>
  <section style="display:flex;flex-direction:column;justify-content:center;flex:1 1 0%;min-width:0;">
    <p style="margin:0 0 4px;font-size:17px;font-weight:900;color:#1f2328;line-height:1.35;letter-spacing:0.2px;"><span leaf="">{{章节标题}}</span></p>
    <p style="margin:0;font-size:13px;font-weight:600;color:#75767a;letter-spacing:1.1px;"><span leaf="">{{英文标签，如：TYPOGRAPHY · STRUCTURE}}</span></p>
  </section>
</section>
```

---

## 组件 5 小标签标题（小节标题）

> 章节内部的小标题（`###` 或需要强调的段落引导）。药丸标签写类别（引导/代码/重点…），后接 17px 加粗标题。

```html
<section style="display:flex;align-items:center;gap:8px;margin:34px 0 14px;flex-wrap:wrap;">
  <span style="display:inline-block;padding:4px 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;color:#0969da;background:#e1edfb;border-radius:999px;border:1px solid #b0cff3;"><span leaf="">{{类别标签}}</span></span>
  <p style="font-size:17px;font-weight:900;color:#1f2328;margin:0;"><span leaf="">{{小节标题}}</span></p>
</section>
```

---

## 组件 6 子标题（GitHub 下划线式）

> 原主题的 h2 样式：23px 标题 + 灰色底线叠蓝色短下划线（用 inset 阴影实现）。用于不太需要药丸标签的小节，与组件 5 二选一即可。

```html
<h3 style="display:block;font-size:23px;font-weight:700;color:#1f2328;line-height:1.35;margin:34px 0 18px;padding:0 0 10px 0;border-bottom:2px solid #d8dee4;box-shadow:inset 0 -2px 0 #0969da;"><span leaf="">{{子标题}}</span></h3>
```

---

## 组件 7 正文段落

> 普通正文段落。每段 1~3 个关键词用蓝下划线（组件 8b）标记。

```html
<p style="margin:0 0 16px;line-height:1.7;color:#1f2328;font-size:16px;"><span leaf="">{{正文内容，含<span style="border-bottom:2px solid #0969da;"><span leaf="">下划线关键词</span></span>}}</span></p>
```

> **注意**：`<span leaf>` 不可嵌套使用，实际写法是拆分为多个并列 span：`<span leaf="">正文前段</span><span style="border-bottom:2px solid #0969da;"><span leaf="">关键词</span></span><span leaf="">后段</span>`。上面示例仅为示意结构。

---

## 组件 8 正文强调样式组（6 种变体）

### 8a. 主色加粗（锚点级，全篇 ≤5 处）

```html
<strong style="color:#0969da;"><span leaf="">{{核心结论 / 产品名 / 关键数据}}</span></strong>
```

### 8b. GitHub 蓝下划线（最常用，每段 1~3 个短语）

```html
<span style="border-bottom:2px solid #0969da;"><span leaf="">{{关键短语，4~15 字}}</span></span>
```

### 8c. 浅蓝底高亮（次要关键词）

```html
<span style="background:#e1edfb;"><span leaf="">{{高亮内容}}</span></span>
```

### 8d. 行内代码（GitHub 灰底）

```html
<code style="font-family:'SF Mono',Consolas,Menlo,monospace;padding:3px 6px;background-color:rgba(175,184,193,0.2);color:#1f2328;border-radius:6px;font-size:13px;line-height:1.5;"><span leaf="">{{字段名 / 命令 / 接口}}</span></code>
```

### 8e. 荧光笔（长句强调，偶尔用）

```html
<span style="background:#cee1f8;"><span leaf="">{{强调短句}}</span></span>
```

### 8f. 删除线（已否定的旧做法 / 已完成项）

```html
<span style="text-decoration:line-through;color:#75767a;"><span leaf="">{{被否定 / 已完成的内容}}</span></span>
```

---

## 组件 9 引用高亮块（`>` 引用）

> 浅灰底圆角块 + 左侧 4px 蓝竖条，引用金句或转载内容。

```html
<section style="margin:18px 0;padding:14px 16px;background:#f6f8fa;border:1px solid #d8dee4;border-left:4px solid #0969da;color:#57606a;border-radius:10px;">
  <p style="margin:0;text-align:left;line-height:1.6;font-size:16px;color:#1f2328;"><span leaf="">{{引用内容}}</span></p>
</section>
```

---

## 组件 10 观点强调卡

> 比 9 更强的观点卡：白色卡片 + 左蓝竖条 + 顶部「观点强调」小字，底部可带一行原则小注（没有就删掉最后一段）。

```html
<section style="margin:0 0 28px;padding:16px 16px 14px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-left:3px solid #0969da;border-radius:12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="width:24px;height:2px;background:#0969da;border-radius:999px;flex-shrink:0;"><span leaf=""><br></span></span>
    <p style="font-size:13px;color:#0969da;margin:0;font-weight:700;letter-spacing:1.2px;"><span leaf="">观点强调</span></p>
  </section>
  <p style="font-size:16px;font-weight:700;color:#1f2328;margin:0;line-height:1.72;"><span leaf="">{{观点金句}}</span></p>
  <p style="font-size:13px;font-weight:700;color:#1f2328;margin:12px 0 0;line-height:1.6;padding-top:10px;border-top:1px solid rgba(208,215,222,0.18);"><span style="display:inline-block;margin-right:8px;padding:1px 7px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:800;"><span leaf="">principle</span></span><span leaf="">{{原则小注，可省略整行}}</span></p>
</section>
```

---

## 组件 11 三点总结卡

> 中段或结尾收束：药丸标题 + 一句判断 + 三条编号要点 + 可选结尾灰字。

```html
<section style="margin:0 0 28px;padding:18px 18px 16px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <p style="font-size:13px;color:#0969da;display:inline-block;margin-bottom:8px;padding:2px 8px;border-radius:999px;background:#e1edfb;font-weight:700;"><span leaf="">三点总结</span></p>
  <p style="font-size:17px;font-weight:800;color:#1f2328;line-height:1.45;margin:0 0 14px;"><span leaf="">{{总结判断句}}</span></p>
  <section style="display:flex;flex-direction:column;gap:10px;margin:0;">
    <section style="display:flex;align-items:flex-start;gap:10px;padding:0 0 10px;border-bottom:1px solid rgba(208,215,222,0.18);">
      <span style="display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:22px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:900;line-height:1;"><span leaf="">01</span></span>
      <p style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.68;margin:0;"><span leaf="">{{要点一}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:10px;padding:0 0 10px;border-bottom:1px solid rgba(208,215,222,0.18);">
      <span style="display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:22px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:900;line-height:1;"><span leaf="">02</span></span>
      <p style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.68;margin:0;"><span leaf="">{{要点二}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:10px;padding:0 0 10px;">
      <span style="display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:22px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:900;line-height:1;"><span leaf="">03</span></span>
      <p style="font-size:16px;font-weight:700;color:#1f2328;line-height:1.68;margin:0;"><span leaf="">{{要点三}}</span></p>
    </section>
  </section>
  <p style="font-size:16px;color:#75767a;line-height:1.62;margin:12px 0 0;"><span leaf="">{{收尾说明，可省略整行}}</span></p>
</section>
```

---

## 组件 12 最终判断卡

> 淡蓝底强调卡，放全文最重要的一个结论。全文最多 1 次。

```html
<section style="margin:0 0 30px;padding:18px 18px 16px;background:#f0f6fc;border:1px solid #b0cff3;border-radius:16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="display:flex;align-items:center;gap:8px;margin:0 0 10px;">
    <span style="display:inline-block;width:11px;height:11px;border-radius:4px;background:#0969da;box-shadow:0 0 0 4px #e1edfb;flex-shrink:0;"><span leaf=""><br></span></span>
    <p style="margin:0;font-size:13px;font-weight:900;color:#0969da;letter-spacing:1px;line-height:1.45;"><span leaf="">最终判断</span></p>
  </section>
  <p style="margin:0;font-size:17px;font-weight:900;color:#1f2328;line-height:1.45;letter-spacing:-0.02em;"><span leaf="">{{核心判断句}}</span></p>
  <p style="margin:9px 0 0;font-size:16px;color:#53565a;line-height:1.75;"><span leaf="">{{展开说明}}</span></p>
  <p style="margin:13px 0 0;padding-top:11px;border-top:1px solid rgba(208,215,222,0.18);font-size:13px;font-weight:800;color:#75767a;line-height:1.55;letter-spacing:0.35px;"><span leaf="">{{适用场景注，如：适合观点文、复盘、方案结论}}</span></p>
</section>
```

---

## 组件 13 数据指标卡组

> 2~3 张数字卡并排。大数字（24px 内）+ 药丸指标名 + 一句说明。

```html
<section style="margin:0 0 28px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：核心数据}}</span></p>
  <section style="display:flex;flex-wrap:wrap;gap:12px;">
    <section style="min-width:0;flex:1 1 160px;background:#f0f6fc;border:1px solid #b0cff3;border-radius:12px;padding:16px 14px 14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="display:inline-block;font-size:13px;font-weight:700;color:#75767a;margin:0 0 12px;letter-spacing:0.8px;padding:2px 8px;border-radius:999px;background:#ffffff;border:1px solid #b0cff3;"><span leaf="">{{指标名一}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#0969da;margin:0 0 6px;line-height:1;letter-spacing:-0.04em;"><span leaf="">{{数字一}}</span></p>
      <p style="font-size:16px;color:#75767a;margin:0;line-height:1.6;"><span leaf="">{{说明一}}</span></p>
    </section>
    <section style="min-width:0;flex:1 1 160px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:16px 12px 12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="display:inline-block;font-size:13px;font-weight:700;color:#75767a;margin:0 0 12px;letter-spacing:0.8px;padding:2px 8px;border-radius:999px;background:#f6f8fa;"><span leaf="">{{指标名二}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 6px;line-height:1;letter-spacing:-0.04em;"><span leaf="">{{数字二}}</span></p>
      <p style="font-size:16px;color:#75767a;margin:0;line-height:1.6;"><span leaf="">{{说明二}}</span></p>
    </section>
    <section style="min-width:0;flex:1 1 160px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:16px 12px 12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="display:inline-block;font-size:13px;font-weight:700;color:#75767a;margin:0 0 12px;letter-spacing:0.8px;padding:2px 8px;border-radius:999px;background:#f6f8fa;"><span leaf="">{{指标名三}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 6px;line-height:1;letter-spacing:-0.04em;"><span leaf="">{{数字三}}</span></p>
      <p style="font-size:16px;color:#75767a;margin:0;line-height:1.6;"><span leaf="">{{说明三}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 14 模块速览卡组

> 并列条目的"三卡速览"：药丸区块名 + 多张小卡（图标字 + PART 编号 + 卡题 + 说明）。用于盘点开篇、结构总览。

```html
<section style="margin:0 0 32px;">
  <section style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;gap:12px;">
    <p style="display:inline-block;padding:4px 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;color:#0969da;background:#e1edfb;border-radius:999px;margin:0;"><span leaf="">{{区块名，如：模块速览}}</span></p>
  </section>
  <section style="display:flex;flex-wrap:wrap;gap:12px;">
    <section style="min-width:0;flex:1 1 160px;background:#f0f6fc;border:1px solid #b0cff3;border-radius:12px;padding:16px 14px 13px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <section style="margin:0 0 10px;display:flex;align-items:center;gap:8px;">
        <section style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;background:#cee1f8;color:#0969da;font-size:22px;font-weight:900;flex-shrink:0;line-height:1;"><span leaf="">{{P}}</span></section>
        <p style="display:inline-block;font-size:13px;font-weight:700;color:#0969da;letter-spacing:0.8px;margin:0;padding:2px 8px;border-radius:999px;background:#cee1f8;"><span leaf="">{{PART 01}}</span></p>
      </section>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;line-height:1.45;"><span leaf="">{{卡片标题一}}</span></p>
      <p style="font-size:16px;color:#1f2328;margin:0;line-height:1.65;"><span leaf="">{{卡片说明一}}</span></p>
    </section>
    <section style="min-width:0;flex:1 1 160px;padding:16px 12px 12px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <section style="margin:0 0 10px;display:flex;align-items:center;gap:8px;">
        <section style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:10px;background:rgba(0,0,0,0.06);color:#0969da;font-size:22px;font-weight:900;flex-shrink:0;line-height:1;"><span leaf="">{{P}}</span></section>
        <p style="display:inline-block;font-size:13px;font-weight:700;color:#75767a;letter-spacing:0.8px;margin:0;padding:2px 8px;border-radius:999px;background:#f6f8fa;"><span leaf="">{{PART 02}}</span></p>
      </section>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;line-height:1.45;"><span leaf="">{{卡片标题二}}</span></p>
      <p style="font-size:16px;color:#75767a;margin:0;line-height:1.65;"><span leaf="">{{卡片说明二}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 15 适合谁（受众判断卡）

> 双栏"适合 / 不适合"卡。帮读者决定要不要往下读。

```html
<section style="margin:0 0 30px;padding:18px;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="margin:0 0 14px;">
    <p style="margin:0;font-size:17px;font-weight:900;color:#1f2328;line-height:1.42;letter-spacing:-0.02em;"><span leaf="">这篇适合谁</span></p>
    <p style="margin:7px 0 0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{一句话说明}}</span></p>
  </section>
  <section style="display:flex;flex-wrap:wrap;gap:12px;">
    <section style="flex:1 1 260px;min-width:0;padding:13px;border-radius:12px;background:#e1edfb;border:1px solid #b0cff3;box-sizing:border-box;">
      <p style="display:inline-block;margin:0 0 9px;padding:3px 9px;border-radius:999px;background:#ffffff;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:900;line-height:1.4;"><span leaf="">适合</span></p>
      <section style="display:flex;align-items:flex-start;gap:8px;margin:0 0 7px;font-size:16px;font-weight:700;color:#1f2328;line-height:1.65;">
        <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#0969da;flex-shrink:0;"><span leaf=""><br></span></span>
        <p style="margin:0;"><span leaf="">{{适合人群一}}</span></p>
      </section>
      <section style="display:flex;align-items:flex-start;gap:8px;margin:0 0 7px;font-size:16px;font-weight:700;color:#1f2328;line-height:1.65;">
        <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#0969da;flex-shrink:0;"><span leaf=""><br></span></span>
        <p style="margin:0;"><span leaf="">{{适合人群二}}</span></p>
      </section>
    </section>
    <section style="flex:1 1 260px;min-width:0;padding:13px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-sizing:border-box;">
      <p style="display:inline-block;margin:0 0 9px;padding:3px 9px;border-radius:999px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);color:#75767a;font-size:13px;font-weight:900;line-height:1.4;"><span leaf="">不适合</span></p>
      <section style="display:flex;align-items:flex-start;gap:8px;margin:0 0 7px;font-size:16px;font-weight:700;color:#53565a;line-height:1.65;">
        <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#75767a;flex-shrink:0;"><span leaf=""><br></span></span>
        <p style="margin:0;"><span leaf="">{{不适合人群一}}</span></p>
      </section>
      <section style="display:flex;align-items:flex-start;gap:8px;margin:0 0 7px;font-size:16px;font-weight:700;color:#53565a;line-height:1.65;">
        <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#75767a;flex-shrink:0;"><span leaf=""><br></span></span>
        <p style="margin:0;"><span leaf="">{{不适合人群二}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 16 检查清单

> 三态清单：✓ 已完成（标题划线灰字）、• 待办、! 注意。按需增删行。

```html
<section style="margin:0 0 30px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:2px;font-weight:700;"><span leaf="">{{区块名，如：发布前检查}}</span></p>
  <section style="display:flex;flex-direction:column;gap:12px;">
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;align-items:flex-start;gap:8px;">
      <p style="margin:0;width:22px;height:22px;border-radius:999px;background:#cee1f8;color:#0969da;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;flex-shrink:0;"><span leaf="">✓</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#53565a;line-height:1.55;"><span style="text-decoration:line-through;"><span leaf="">{{已完成项}}</span></span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{该项说明}}</span></p>
      </section>
    </section>
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;align-items:flex-start;gap:8px;">
      <p style="margin:0;width:22px;height:22px;border-radius:999px;background:#f6f8fa;color:#75767a;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;border:1px solid rgba(208,215,222,0.18);flex-shrink:0;"><span leaf="">•</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{待办项}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{该项说明}}</span></p>
      </section>
    </section>
    <section style="padding:12px 16px;display:flex;align-items:flex-start;gap:8px;">
      <p style="margin:0;width:22px;height:22px;border-radius:999px;background:#cee1f8;color:#0969da;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;border:1px solid #b0cff3;flex-shrink:0;"><span leaf="">!</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{注意事项}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{该项说明}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 17 资源工具卡（清单条目卡）

> 无序列表 / 工具资源的高级形态：每条一张卡（类别药丸 + 条目名 + 一句说明）。

```html
<section style="margin:0 0 28px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：资源工具箱}}</span></p>
  <section style="display:flex;flex-direction:column;gap:12px;">
    <section style="background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <section style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px;">
        <p style="display:inline-block;margin:0;font-size:13px;font-weight:700;letter-spacing:1px;color:#0969da;background:#e1edfb;padding:2px 8px;border-radius:999px;"><span leaf="">{{类别，如：工具}}</span></p>
        <p style="margin:0;font-size:13px;color:#75767a;"><span leaf="">•</span></p>
      </section>
      <p style="margin:0 0 4px;"><span style="font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{条目名}}</span></span></p>
      <p style="margin:0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{一句说明}}</span></p>
    </section>
    <section style="background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <section style="display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:6px;">
        <p style="display:inline-block;margin:0;font-size:13px;font-weight:700;letter-spacing:1px;color:#0969da;background:#e1edfb;padding:2px 8px;border-radius:999px;"><span leaf="">{{类别，如：资料}}</span></p>
        <p style="margin:0;font-size:13px;color:#75767a;"><span leaf="">•</span></p>
      </section>
      <p style="margin:0 0 4px;"><span style="font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{条目名}}</span></span></p>
      <p style="margin:0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{一句说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 18 承接过渡卡

> 章节之间的"桥"：左蓝竖条 + 药丸「下一段为什么重要」+ 一句承接判断。全文用 1~2 次即可，不要每章都加。

```html
<section style="display:flex;align-items:stretch;gap:12px;margin:8px 0 30px;">
  <section style="width:3px;border-radius:999px;background:#0969da;flex-shrink:0;"><span leaf=""><br></span></section>
  <section style="flex:1 1 0%;min-width:0;padding:14px 15px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
    <p style="display:inline-block;margin:0 0 7px;padding:3px 8px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:900;line-height:1.4;"><span leaf="">下一段为什么重要</span></p>
    <p style="margin:0;font-size:17px;font-weight:900;color:#1f2328;line-height:1.45;letter-spacing:-0.02em;"><span leaf="">{{承接判断句}}</span></p>
    <p style="margin:8px 0 0;font-size:16px;color:#53565a;line-height:1.72;"><span leaf="">{{展开说明}}</span></p>
    <p style="margin:11px 0 0;padding-top:9px;border-top:1px solid rgba(208,215,222,0.18);font-size:13px;font-weight:900;color:#75767a;line-height:1.5;letter-spacing:0.5px;"><span leaf="">{{下一段预告，可省略整行}}</span></p>
  </section>
</section>
```

---

## 组件 19 步骤流

> 教程步骤：左侧编号方块 + 蓝色连线，右侧说明卡。步骤 2~6 步。

```html
<section style="margin:0 0 32px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：落地步骤}}</span></p>
  <section style="display:flex;gap:12px;align-items:stretch;margin-bottom:12px;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
      <span style="width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:#ffffff;color:#0969da;font-size:13px;font-weight:800;border:1px solid #b0cff3;box-shadow:0 2px 6px rgba(31,35,40,0.06);"><span leaf="">01</span></span>
      <span style="width:2px;flex:1 1 auto;background:#cee1f8;margin-top:8px;border-radius:999px;"><span leaf=""><br></span></span>
    </section>
    <section style="flex:1 1 0%;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px 16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;"><span leaf="">{{步骤一标题}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.72;"><span leaf="">{{步骤一说明}}</span></p>
    </section>
  </section>
  <section style="display:flex;gap:12px;align-items:stretch;margin-bottom:12px;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
      <span style="width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:#ffffff;color:#0969da;font-size:13px;font-weight:800;border:1px solid #b0cff3;box-shadow:0 2px 6px rgba(31,35,40,0.06);"><span leaf="">02</span></span>
      <span style="width:2px;flex:1 1 auto;background:#cee1f8;margin-top:8px;border-radius:999px;"><span leaf=""><br></span></span>
    </section>
    <section style="flex:1 1 0%;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px 16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;"><span leaf="">{{步骤二标题}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.72;"><span leaf="">{{步骤二说明}}</span></p>
    </section>
  </section>
  <section style="display:flex;gap:12px;align-items:stretch;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;">
      <span style="width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;background:#ffffff;color:#0969da;font-size:13px;font-weight:800;border:1px solid #b0cff3;box-shadow:0 2px 6px rgba(31,35,40,0.06);"><span leaf="">03</span></span>
    </section>
    <section style="flex:1 1 0%;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px 16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;"><span leaf="">{{步骤三标题（最后一步无连线）}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.72;"><span leaf="">{{步骤三说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 20 对比卡（VS）

> 新旧方式对照：每行三段（左卡 + VS 徽章 + 右卡），新方式卡用淡蓝底突出。行数按需增减。

```html
<section style="margin:0 0 32px;">
  <section style="display:flex;align-items:stretch;gap:8px;margin-bottom:12px;">
    <section style="flex:1 1 0%;min-width:0;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px 14px 12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <span style="display:inline-block;margin:0 0 8px;font-size:13px;font-weight:700;color:#75767a;letter-spacing:1px;padding:3px 10px;border-radius:999px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);"><span leaf="">{{旧方式}}</span></span>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;line-height:1.45;"><span leaf="">{{旧方式要点}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">{{旧方式说明}}</span></p>
    </section>
    <section style="display:flex;align-items:center;justify-content:center;flex-shrink:0;width:24px;"><span style="display:inline-flex;align-items:center;justify-content:center;background:#0969da;color:#ffffff;font-size:10px;font-weight:900;padding:3px 4px;border-radius:4px;letter-spacing:0.5px;"><span leaf="">VS</span></span></section>
    <section style="flex:1 1 0%;min-width:0;background:#f0f6fc;border:1px solid #b0cff3;border-radius:12px;padding:14px 14px 12px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <span style="display:inline-block;margin:0 0 8px;font-size:13px;font-weight:700;color:#0969da;letter-spacing:1px;padding:3px 10px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;"><span leaf="">{{新方式}}</span></span>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 6px;line-height:1.45;"><span leaf="">{{新方式要点}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">{{新方式说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 21 误区 / 事实卡

> 破除误解：左灰卡「误区」+ 右淡蓝卡「事实」。可放多组。

```html
<section style="margin:0 0 30px;">
  <p style="margin:0 0 12px;font-size:13px;font-weight:900;color:#75767a;line-height:1.45;letter-spacing:1.2px;"><span leaf="">{{区块名，如：常见误区}}</span></p>
  <section style="display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px;">
    <section style="flex:1 1 260px;min-width:0;padding:13px 14px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="display:inline-block;margin:0 0 7px;padding:3px 8px;border-radius:999px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);color:#75767a;font-size:13px;font-weight:900;line-height:1.4;"><span leaf="">误区</span></p>
      <p style="margin:0;font-size:16px;font-weight:700;color:#53565a;line-height:1.68;"><span leaf="">{{误区内容}}</span></p>
    </section>
    <section style="flex:1 1 260px;min-width:0;padding:13px 14px;border-radius:12px;background:#f0f6fc;border:1px solid #b0cff3;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="display:inline-block;margin:0 0 7px;padding:3px 8px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:900;line-height:1.4;"><span leaf="">事实</span></p>
      <p style="margin:0;font-size:16px;font-weight:800;color:#1f2328;line-height:1.68;"><span leaf="">{{事实内容}}</span></p>
      <p style="margin:8px 0 0;font-size:16px;color:#75767a;line-height:1.62;"><span leaf="">{{补充说明，可省略}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 22 时间线

> 场景 / 递进脉络：蓝点 + 竖线 + 药丸标签 + 标题 + 说明。末行无竖线。

```html
<section style="margin:0 0 30px;">
  <p style="font-size:13px;font-weight:900;color:#75767a;margin:0 0 16px;letter-spacing:1.2px;"><span leaf="">{{区块名，如：应用场景}}</span></p>
  <section style="display:flex;gap:12px;align-items:flex-start;padding:0 0 16px;min-height:48px;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;padding-top:3px;">
      <span style="width:10px;height:10px;border-radius:999px;background:#0969da;flex-shrink:0;box-shadow:0 0 0 3px #e1edfb;"><span leaf=""><br></span></span>
      <span style="flex:1;width:2px;background:#d8dee4;margin-top:4px;min-height:20px;"><span leaf=""><br></span></span>
    </section>
    <section style="flex:1;min-width:0;padding-bottom:4px;">
      <span style="display:inline-block;font-size:13px;font-weight:700;color:#0969da;background:#e1edfb;padding:2px 8px;border-radius:999px;margin:0 0 4px;line-height:1.5;"><span leaf="">{{节点标签}}</span></span>
      <p style="font-size:17px;font-weight:700;color:#1f2328;margin:0 0 2px;line-height:1.5;"><span leaf="">{{节点标题}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.65;"><span leaf="">{{节点说明}}</span></p>
    </section>
  </section>
  <section style="display:flex;gap:12px;align-items:flex-start;padding:0 0 16px;min-height:48px;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;padding-top:3px;">
      <span style="width:10px;height:10px;border-radius:999px;background:#0969da;flex-shrink:0;box-shadow:0 0 0 3px #e1edfb;"><span leaf=""><br></span></span>
      <span style="flex:1;width:2px;background:#d8dee4;margin-top:4px;min-height:20px;"><span leaf=""><br></span></span>
    </section>
    <section style="flex:1;min-width:0;padding-bottom:4px;">
      <span style="display:inline-block;font-size:13px;font-weight:700;color:#0969da;background:#e1edfb;padding:2px 8px;border-radius:999px;margin:0 0 4px;line-height:1.5;"><span leaf="">{{节点标签}}</span></span>
      <p style="font-size:17px;font-weight:700;color:#1f2328;margin:0 0 2px;line-height:1.5;"><span leaf="">{{节点标题}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.65;"><span leaf="">{{节点说明}}</span></p>
    </section>
  </section>
  <section style="display:flex;gap:12px;align-items:flex-start;min-height:48px;">
    <section style="display:flex;flex-direction:column;align-items:center;flex-shrink:0;padding-top:3px;">
      <span style="width:10px;height:10px;border-radius:999px;background:#0969da;flex-shrink:0;box-shadow:0 0 0 3px #e1edfb;"><span leaf=""><br></span></span>
    </section>
    <section style="flex:1;min-width:0;padding-bottom:4px;">
      <span style="display:inline-block;font-size:13px;font-weight:700;color:#0969da;background:#e1edfb;padding:2px 8px;border-radius:999px;margin:0 0 4px;line-height:1.5;"><span leaf="">{{末节点标签}}</span></span>
      <p style="font-size:17px;font-weight:700;color:#1f2328;margin:0 0 2px;line-height:1.5;"><span leaf="">{{末节点标题}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.65;"><span leaf="">{{末节点说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 23 适用说明条（适合 / 前提 / 风险 / 不适合）

> 四行「适用说明」：左侧圆角小标签 + 右侧两行说明。按需增删行。

```html
<section style="margin:0 0 28px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：适用说明}}</span></p>
  <section style="display:flex;flex-direction:column;gap:12px;">
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;gap:12px;align-items:center;">
      <section style="display:flex;align-items:center;justify-content:flex-start;width:96px;flex-shrink:0;">
        <p style="display:inline-block;margin:0;font-size:13px;font-weight:700;color:#0969da;background:#e1edfb;border:1px solid #b0cff3;border-radius:8px;padding:4px 10px;text-align:center;min-width:64px;box-sizing:border-box;"><span leaf="">适合</span></p>
      </section>
      <section style="min-width:0;">
        <p style="margin:0 0 3px;font-size:16px;color:#1f2328;line-height:1.7;"><span leaf="">{{适合的内容类型}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{一句补充}}</span></p>
      </section>
    </section>
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;gap:12px;align-items:center;">
      <section style="display:flex;align-items:center;justify-content:flex-start;width:96px;flex-shrink:0;">
        <p style="display:inline-block;margin:0;font-size:13px;font-weight:700;color:#0969da;background:#ffffff;border:1px solid #b0cff3;border-radius:8px;padding:4px 10px;text-align:center;min-width:64px;box-sizing:border-box;"><span leaf="">前提</span></p>
      </section>
      <section style="min-width:0;">
        <p style="margin:0 0 3px;font-size:16px;color:#1f2328;line-height:1.7;"><span leaf="">{{使用前提}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{一句补充}}</span></p>
      </section>
    </section>
    <section style="padding:12px 16px;display:flex;gap:12px;align-items:center;">
      <section style="display:flex;align-items:center;justify-content:flex-start;width:96px;flex-shrink:0;">
        <p style="display:inline-block;margin:0;font-size:13px;font-weight:700;color:#0969da;background:#cee1f8;border:1px solid #b0cff3;border-radius:8px;padding:4px 10px;text-align:center;min-width:64px;box-sizing:border-box;"><span leaf="">风险</span></p>
      </section>
      <section style="min-width:0;">
        <p style="margin:0 0 3px;font-size:16px;color:#1f2328;line-height:1.7;"><span leaf="">{{风险提醒}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{一句补充}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 24 FAQ 问答卡

> Q 黑圆标灰底问题行 + A 蓝圆标白底回答行，一问一答一张卡。

```html
<section style="margin:0 0 30px;">
  <p style="font-size:13px;font-weight:900;color:#75767a;margin:0 0 16px;letter-spacing:1.2px;"><span leaf="">常见问题</span></p>
  <section style="margin:0 0 12px;border-radius:12px;overflow:hidden;border:1px solid rgba(208,215,222,0.18);">
    <section style="display:flex;align-items:flex-start;gap:8px;padding:12px 16px;background:#f6f8fa;">
      <span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:999px;background:#1f2328;color:#ffffff;font-size:11px;font-weight:900;flex-shrink:0;margin-top:1px;"><span leaf="">Q</span></span>
      <p style="margin:0;font-size:16px;font-weight:700;color:#1f2328;line-height:1.55;"><span leaf="">{{问题}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:12px 16px;background:#ffffff;">
      <span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:999px;background:#0969da;color:#ffffff;font-size:11px;font-weight:900;flex-shrink:0;margin-top:1px;"><span leaf="">A</span></span>
      <p style="margin:0;font-size:16px;color:#53565a;line-height:1.7;"><span leaf="">{{回答}}</span></p>
    </section>
  </section>
  <section style="margin:0 0 12px;border-radius:12px;overflow:hidden;border:1px solid rgba(208,215,222,0.18);">
    <section style="display:flex;align-items:flex-start;gap:8px;padding:12px 16px;background:#f6f8fa;">
      <span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:999px;background:#1f2328;color:#ffffff;font-size:11px;font-weight:900;flex-shrink:0;margin-top:1px;"><span leaf="">Q</span></span>
      <p style="margin:0;font-size:16px;font-weight:700;color:#1f2328;line-height:1.55;"><span leaf="">{{问题}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:12px 16px;background:#ffffff;">
      <span style="display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:999px;background:#0969da;color:#ffffff;font-size:11px;font-weight:900;flex-shrink:0;margin-top:1px;"><span leaf="">A</span></span>
      <p style="margin:0;font-size:16px;color:#53565a;line-height:1.7;"><span leaf="">{{回答}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 25 参数信息条

> 键值对信息：左侧灰色大写小字键名 + 右侧加粗值 + 灰色说明。

```html
<section style="margin:0 0 28px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：参数信息}}</span></p>
  <section style="display:flex;flex-direction:column;gap:12px;">
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;gap:8px;align-items:baseline;">
      <p style="margin:0;font-size:13px;font-weight:700;letter-spacing:1px;color:#75767a;flex-shrink:0;"><span leaf="">{{键名一}}</span></p>
      <section style="min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{值一}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{说明一}}</span></p>
      </section>
    </section>
    <section style="padding:12px 16px;border-bottom:1px solid rgba(208,215,222,0.18);display:flex;gap:8px;align-items:baseline;">
      <p style="margin:0;font-size:13px;font-weight:700;letter-spacing:1px;color:#75767a;flex-shrink:0;"><span leaf="">{{键名二}}</span></p>
      <section style="min-width:0;">
        <p style="margin:0 0 2px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{值二}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.6;"><span leaf="">{{说明二}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 26 案例卡（数据结果卡）

> 双卡案例：顶部数据结果药丸 + 案例名 + 一句做法说明。

```html
<section style="margin:0 0 30px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：案例精选}}</span></p>
  <section style="display:flex;flex-wrap:wrap;gap:12px;">
    <section style="flex:1 1 260px;min-width:0;padding:16px 12px 12px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <p style="display:inline-block;margin:0 0 8px;padding:3px 8px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:700;"><span leaf="">{{结果数据，如：阅读完成率 +38%}}</span></p>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 4px;"><span leaf="">{{案例名}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">{{一句做法说明}}</span></p>
    </section>
    <section style="flex:1 1 260px;min-width:0;padding:16px 12px 12px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <p style="display:inline-block;margin:0 0 8px;padding:3px 8px;border-radius:999px;background:#e1edfb;color:#0969da;font-size:13px;font-weight:700;"><span leaf="">{{结果数据}}</span></p>
      <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 4px;"><span leaf="">{{案例名}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">{{一句做法说明}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 27 方案卡（价格 / 版本对比）

> 三列版本卡，中间推荐版用淡蓝底。价格行用大字（24px 内），条目用 `•` 前缀。

```html
<section style="margin:0 0 30px;">
  <p style="font-size:13px;color:#75767a;margin:0 0 12px;letter-spacing:1.8px;font-weight:700;"><span leaf="">{{区块名，如：方案组合}}</span></p>
  <section style="display:flex;flex-wrap:wrap;gap:12px;">
    <section style="flex:1 1 200px;min-width:0;padding:16px 12px 12px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <p style="font-size:13px;font-weight:700;color:#75767a;margin:0 0 6px;letter-spacing:1px;"><span leaf="">{{版本名一}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 10px;line-height:1;"><span leaf="">{{价格一}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目一}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目二}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">• {{条目三}}</span></p>
    </section>
    <section style="flex:1 1 200px;min-width:0;background:#f0f6fc;border:1px solid #b0cff3;border-radius:12px;padding:18px 16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
      <p style="font-size:13px;font-weight:700;color:#75767a;margin:0 0 6px;letter-spacing:1px;"><span leaf="">{{推荐版本名}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 10px;line-height:1;"><span leaf="">{{推荐价格}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目一}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目二}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">• {{条目三}}</span></p>
    </section>
    <section style="flex:1 1 200px;min-width:0;padding:16px 12px 12px;border-radius:12px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;display:flex;flex-direction:column;gap:8px;">
      <p style="font-size:13px;font-weight:700;color:#75767a;margin:0 0 6px;letter-spacing:1px;"><span leaf="">{{版本名三}}</span></p>
      <p style="font-size:24px;font-weight:900;color:#1f2328;margin:0 0 10px;line-height:1;"><span leaf="">{{价格三}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目一}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0 0 6px;line-height:1.7;"><span leaf="">• {{条目二}}</span></p>
      <p style="font-size:16px;color:#53565a;margin:0;line-height:1.7;"><span leaf="">• {{条目三}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 28 图文卡（图 + 说明绑在一起）

> 说明文字在上、截图在下的一体卡。适合教程截图、产品界面讲解。

```html
<section style="margin:0 0 32px;">
  <section style="background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:16px 16px 14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
    <p style="display:inline-block;padding:4px 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;color:#0969da;background:#e1edfb;border-radius:999px;margin:0 0 8px;"><span leaf="">{{图注标签，如：功能截图}}</span></p>
    <p style="margin:0 0 8px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.45;"><span leaf="">{{这张图说明什么}}</span></p>
    <p style="margin:0 0 8px;font-size:16px;color:#1f2328;line-height:1.78;"><span leaf="">{{正文解释}}</span></p>
    <p style="margin:10px 0 0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{适用提示，可省略}}</span></p>
  </section>
  <section style="margin-top:12px;border-radius:12px;overflow:hidden;background:#ffffff;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);">
    <img src="{{图片URL}}" alt="{{图片说明}}" style="width:100% !important;height:auto !important;display:block;">
  </section>
</section>
```

---

## 组件 29 图片解读卡（一图 + 编号说明）

> 截图/海报在上，下方 2~3 条编号解读行。

```html
<section style="margin:0 0 28px;">
  <section style="margin:0 0 14px;">
    <p style="display:inline-block;margin:0 0 8px;font-size:13px;color:#0969da;letter-spacing:1.2px;font-weight:700;padding:2px 8px;border-radius:999px;background:#e1edfb;"><span leaf="">{{图注标签，如：图片解读}}</span></p>
    <p style="margin:0;font-size:17px;font-weight:800;color:#1f2328;line-height:1.45;"><span leaf="">{{这张图的看点}}</span></p>
  </section>
  <section style="width:100%;overflow:hidden;background:#ffffff;border-radius:12px;border:1px solid rgba(208,215,222,0.18);box-shadow:0 2px 6px rgba(31,35,40,0.06);box-sizing:border-box;">
    <img src="{{图片URL}}" alt="{{图片说明}}" style="width:100% !important;height:auto !important;display:block;">
  </section>
  <section style="display:flex;flex-direction:column;gap:12px;margin-top:14px;">
    <section style="display:flex;align-items:flex-start;gap:12px;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <p style="margin:0;width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:#cee1f8;color:#0969da;font-size:13px;font-weight:800;flex-shrink:0;border:1px solid #b0cff3;box-sizing:border-box;"><span leaf="">01</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 3px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{区域名一}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{说明一}}</span></p>
      </section>
    </section>
    <section style="display:flex;align-items:flex-start;gap:12px;background:#fbfcfd;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:14px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
      <p style="margin:0;width:28px;height:28px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:#cee1f8;color:#0969da;font-size:13px;font-weight:800;flex-shrink:0;border:1px solid #b0cff3;box-sizing:border-box;"><span leaf="">02</span></p>
      <section style="flex:1 1 0%;min-width:0;">
        <p style="margin:0 0 3px;font-size:17px;font-weight:800;color:#1f2328;line-height:1.55;"><span leaf="">{{区域名二}}</span></p>
        <p style="margin:0;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">{{说明二}}</span></p>
      </section>
    </section>
  </section>
</section>
```

---

## 组件 30 图片容器（通用）

> 普通配图：自适应、居中、不铺满。需要全宽出血的封面图才用 `width:100%`。`![说明](url)` 有说明文字时在图下加灰色小字说明行；空 alt 不加。

```html
<section style="margin:0 0 24px;">
  <img src="{{图片URL}}" alt="{{alt}}" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:12px;border:1px solid rgba(208,215,222,0.18);">
  <p style="margin:8px 0 0;font-size:13px;color:#75767a;text-align:center;line-height:1.6;"><span leaf="">{{图片说明，仅当原文有 alt 说明才生成}}</span></p>
</section>
```

---

## 组件 31 列表组件

### 31a. 无序列表（`-` 项）

> 圆点前缀 + 关键短语可加蓝下划线。

```html
<section style="margin:0 0 20px;padding-left:8px;">
  <p style="margin:0 0 8px;line-height:1.7;color:#1f2328;font-size:16px;"><span leaf="">• {{列表项一，关键词可用<span style="border-bottom:2px solid #0969da;"><span leaf="">下划线</span></span>标记}}</span></p>
  <p style="margin:0 0 8px;line-height:1.7;color:#1f2328;font-size:16px;"><span leaf="">• {{列表项二}}</span></p>
  <p style="margin:0;line-height:1.7;color:#1f2328;font-size:16px;"><span leaf="">• {{列表项三}}</span></p>
</section>
```

> **注意**：同组件 7，实际写法把嵌套 span 拆为并列 span；此项说明在后文不再重复。

### 31b. 有序列表（`1.` 项）

> 蓝色加粗编号前缀。

```html
<section style="margin:0 0 20px;padding-left:8px;">
  <p style="margin:0 0 8px;line-height:1.7;color:#1f2328;font-size:16px;"><span style="font-weight:900;color:#0969da;"><span leaf="">1. </span></span><span leaf="">{{步骤项一}}</span></p>
  <p style="margin:0 0 8px;line-height:1.7;color:#1f2328;font-size:16px;"><span style="font-weight:900;color:#0969da;"><span leaf="">2. </span></span><span leaf="">{{步骤项二}}</span></p>
  <p style="margin:0;line-height:1.7;color:#1f2328;font-size:16px;"><span style="font-weight:900;color:#0969da;"><span leaf="">3. </span></span><span leaf="">{{步骤项三}}</span></p>
</section>
```

---

## 组件 32 数据表格（真实表格语义）

> 仅用于真正的数据对照表（参数表 / 版本对比）。GitHub 风格：灰底表头 + `#d1d9e0` 细线。

```html
<section style="overflow-x:auto;margin:16px 0;">
  <table style="width:100%;border-collapse:collapse;font-size:15px;">
    <thead>
      <tr>
        <th style="background-color:#f6f8fa;padding:8px 16px;text-align:left;font-weight:600;color:#1f2328;border:1px solid #d1d9e0;"><span leaf="">{{表头一}}</span></th>
        <th style="background-color:#f6f8fa;padding:8px 16px;text-align:left;font-weight:600;color:#1f2328;border:1px solid #d1d9e0;"><span leaf="">{{表头二}}</span></th>
        <th style="background-color:#f6f8fa;padding:8px 16px;text-align:left;font-weight:600;color:#1f2328;border:1px solid #d1d9e0;"><span leaf="">{{表头三}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行一列一}}</span></td>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行一列二}}</span></td>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行一列三}}</span></td>
      </tr>
      <tr>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行二列一}}</span></td>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行二列二}}</span></td>
        <td style="padding:8px 16px;border:1px solid #d1d9e0;color:#1f2328;"><span leaf="">{{行二列三}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

---

## 组件 33 作者卡（尾部签名区，仅末尾一处）

> 签名区 + 关注引导。`{{作者名}}` / `{{一句话简介}}` / `{{头像字}}` 由用户署名替换；没给署名就保留占位并在交付时提醒。原文末尾已有作者签名段时，并入本卡，不另生成。

```html
<section style="overflow:hidden;margin:30px 0 24px;padding:18px 18px 16px;background:#f0f6fc;border:1px solid #b0cff3;border-radius:16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="display:flex;align-items:center;gap:12px;margin:0 0 14px;">
    <span style="width:46px;height:46px;border-radius:15px;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:#0969da;color:#ffffff;font-size:17px;font-weight:900;letter-spacing:-0.04em;box-shadow:0 4px 16px rgba(9,105,218,0.12);"><span leaf="">{{头像字，取名字前两字}}</span></span>
    <section style="min-width:0;flex:1 1 0%;">
      <p style="margin:0 0 3px;font-size:17px;font-weight:900;color:#1f2328;line-height:1.28;letter-spacing:-0.02em;"><span leaf="">我是 {{作者名}}</span></p>
      <p style="margin:0;font-size:13px;font-weight:800;color:#75767a;letter-spacing:0.8px;line-height:1.45;"><span leaf="">{{一句话简介，如：热衷于分享 AI 观察与干货}}</span></p>
    </section>
  </section>
  <section style="display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0;">
    <span style="display:inline-block;padding:4px 9px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:800;line-height:1.4;"><span leaf="">{{内容标签一}}</span></span>
    <span style="display:inline-block;padding:4px 9px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:800;line-height:1.4;"><span leaf="">{{内容标签二}}</span></span>
  </section>
  <section style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:16px 0 0;padding-top:12px;border-top:1px solid rgba(208,215,222,0.18);">
    <p style="margin:0;flex:1 1 180px;font-size:16px;color:#75767a;line-height:1.65;"><span leaf="">如果你觉得今天这篇有收获，欢迎<strong style="color:#0969da;"><span leaf="">点赞、在看、转发</span></strong>三连，我们下篇见</span></p>
  </section>
</section>
```

> **注意**：上面互动引导里 `strong` 嵌套 `span leaf` 的写法，实际输出时把 strong 拆在 leaf 外层：`…欢迎<span leaf="">点赞、在看、转发</span>…` 的相邻文本分别包 leaf，强调用 `<span style="color:#0969da;font-weight:700;">` 实现。

---

## 组件 34 信念宣言卡

> 个人观点浓缩卡：「我相信 / 我拒绝」两组清单。适合专栏开头、个人品牌文。

```html
<section style="margin:0 0 30px;padding:20px 18px 16px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <p style="display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:900;line-height:1.42;letter-spacing:0.7px;"><span leaf="">{{宣言标签，如：我的长期判断}}</span></p>
  <p style="margin:0;font-size:17px;font-weight:900;color:#1f2328;line-height:1.42;letter-spacing:-0.02em;"><span leaf="">{{宣言主张}}</span></p>
  <p style="margin:9px 0 0;font-size:16px;color:#53565a;line-height:1.74;"><span leaf="">{{展开一句}}</span></p>
  <section style="margin:15px 0 0;display:flex;flex-direction:column;gap:8px;">
    <p style="margin:0;font-size:13px;font-weight:900;color:#75767a;line-height:1.45;letter-spacing:0.8px;"><span leaf="">我相信</span></p>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:10px 11px;border-radius:8px;background:#f0f6fc;border:1px solid #b0cff3;color:#1f2328;font-size:16px;font-weight:700;line-height:1.66;">
      <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#0969da;flex-shrink:0;"><span leaf=""><br></span></span>
      <p style="margin:0;"><span leaf="">{{信条一}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:10px 11px;border-radius:8px;background:#f0f6fc;border:1px solid #b0cff3;color:#1f2328;font-size:16px;font-weight:700;line-height:1.66;">
      <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#0969da;flex-shrink:0;"><span leaf=""><br></span></span>
      <p style="margin:0;"><span leaf="">{{信条二}}</span></p>
    </section>
  </section>
  <section style="margin:15px 0 0;display:flex;flex-direction:column;gap:8px;">
    <p style="margin:0;font-size:13px;font-weight:900;color:#75767a;line-height:1.45;letter-spacing:0.8px;"><span leaf="">我拒绝</span></p>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:10px 11px;border-radius:8px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);color:#53565a;font-size:16px;font-weight:700;line-height:1.66;">
      <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#75767a;flex-shrink:0;"><span leaf=""><br></span></span>
      <p style="margin:0;"><span leaf="">{{拒绝项一}}</span></p>
    </section>
    <section style="display:flex;align-items:flex-start;gap:8px;padding:10px 11px;border-radius:8px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);color:#53565a;font-size:16px;font-weight:700;line-height:1.66;">
      <span style="margin-top:0.62em;display:inline-block;width:6px;height:6px;border-radius:999px;background:#75767a;flex-shrink:0;"><span leaf=""><br></span></span>
      <p style="margin:0;"><span leaf="">{{拒绝项二}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 35 系列卡（连载导读）

> 系列文章标识：栏目药丸 + 期数 + 系列标题 + 下一篇预告条。

```html
<section style="margin:0 0 30px;padding:18px 18px 16px;background:#ffffff;border:1px solid rgba(208,215,222,0.18);border-radius:16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);">
  <section style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:0 0 12px;">
    <span style="display:inline-block;padding:4px 10px;border-radius:999px;background:#e1edfb;border:1px solid #b0cff3;color:#0969da;font-size:13px;font-weight:900;letter-spacing:0.8px;line-height:1.4;"><span leaf="">{{系列名}}</span></span>
    <span style="display:inline-block;padding:4px 10px;border-radius:999px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);color:#75767a;font-size:13px;font-weight:900;letter-spacing:0.8px;line-height:1.4;"><span leaf="">{{期数，如：第 07 期}}</span></span>
  </section>
  <p style="margin:0;font-size:17px;font-weight:900;color:#1f2328;line-height:1.38;letter-spacing:-0.025em;"><span leaf="">{{系列主张}}</span></p>
  <p style="margin:8px 0 0;font-size:16px;color:#53565a;line-height:1.72;"><span leaf="">{{系列说明}}</span></p>
  <p style="margin:15px 0 0;padding:11px 12px;border-radius:8px;background:#f0f6fc;border:1px solid #b0cff3;color:#1f2328;font-size:16px;font-weight:800;line-height:1.62;"><span leaf="">下一篇：{{预告标题}}</span></p>
</section>
```

---

## 组件 36 结尾 CTA 卡

> 收尾行动卡：一句行动号召 + 两个按钮卡（主蓝按钮 + 白底次按钮，均为静态 section，非真按钮）。放在作者卡之前或代替其互动行。

```html
<section style="background:#f0f6fc;border:1px solid #b0cff3;border-radius:16px;padding:18px 18px 16px;box-shadow:0 2px 6px rgba(31,35,40,0.06);margin:0 0 24px;">
  <p style="font-size:17px;font-weight:800;color:#1f2328;margin:0 0 14px;line-height:1.45;"><span leaf="">{{行动号召句}}</span></p>
  <section style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:14px;">
    <section style="text-align:center;color:#ffffff;min-width:0;flex:1 1 140px;background:#0969da;border:1px solid #b0cff3;border-radius:12px;padding:12px 8px;box-shadow:0 4px 16px rgba(9,105,218,0.12);box-sizing:border-box;">
      <span style="font-size:13px;font-weight:700;"><span leaf="">{{主按钮文案，如：试一版成稿}}</span></span>
    </section>
    <section style="text-align:center;color:#53565a;min-width:0;flex:1 1 140px;background:#f6f8fa;border:1px solid rgba(208,215,222,0.18);border-radius:12px;padding:12px 8px;box-sizing:border-box;">
      <span style="font-size:13px;font-weight:700;"><span leaf="">{{次按钮文案，如：转发给需要的人}}</span></span>
    </section>
  </section>
  <p style="font-size:13px;color:#75767a;letter-spacing:0.8px;margin:0;padding-top:12px;border-top:1px solid rgba(208,215,222,0.18);"><span leaf="">{{收尾小注，可省略}}</span></p>
</section>
```

---

## 组件 37 章节分割线

> 原主题渐变 hr 的纯色版：1px 浅灰线。

```html
<section style="height:1px;background:#d8dee4;margin:34px auto;width:100%;">
  <span leaf=""><br></span>
</section>
```

---

## 完整文章模板骨架

装配顺序（**只用本主题组件 + 通用增量库，不跨主题混用**）：

```
1. 全局容器（组件 1）
2. Hero 封面卡（组件 2）—— 分类药丸 + 主标题 + 编号要点行 + 底部标签行
3. [可选] 封面图（组件 30 的全宽变体，嵌在 Hero 头部区与底部标签行之间）
4. 阅读导航（组件 3）—— 精选 3 个看点；3 章以下可省
5. 章节循环：
   - 章节编号卡（组件 4，编号 01/02/03…，末章结语用 ∞）
   - 小标签标题（组件 5）或 子标题（组件 6）—— 小节层级
   - 正文段落（组件 7，每段 1~3 处蓝下划线，组件 8b）
   - 行内强调按需插入（组件 8a/8c/8d/8e）
   - 按文章类型插入区块组件（见配方表）：
     数据卡（13）/ 速览卡（14）/ 受众卡（15）/ 清单（16）/ 工具卡（17）/
     承接卡（18）/ 步骤流（19）/ 对比卡（20）/ 误区卡（21）/ 时间线（22）/
     说明条（23）/ FAQ（24）/ 参数条（25）/ 案例卡（26）/ 方案卡（27）/
     图文卡（28）/ 解读卡（29）
   - 列表（31）/ 表格（32）按原文结构插入
   - 引用块（9）/ 观点卡（10）遇引用与金句时插入
6. 收束区（按需选 1~2 个）：
   - 三点总结卡（组件 11）或 最终判断卡（组件 12）
   - 信念宣言卡（34）/ 系列卡（35）/ 结尾 CTA 卡（36）
7. 作者卡（组件 33）—— 全文仅末尾一处签名区
8. 章节分割线（组件 37）按需分隔大区块；正文中不用
```

层级频率纪律：主色加粗（8a）全文 ≤5 处；最终判断卡（12）全文 ≤1 次；承接卡（18）全文 1~2 次；其余标记层组件按段落需要使用。

---

## 文章类型 → 组件组合配方表

| 文章类型 | 核心组件组合 | 点缀组件 |
|---------|-------------|---------|
| 技术教程 / 操作指南 | 2 封面 → 3 导航 → 4+5+7 正文骨架 → 19 步骤流 → 28 图文卡 → 16 检查清单 → 24 FAQ → 33 作者卡 | 8d 行内代码、31b 有序列表、18 承接卡、36 CTA |
| 工具盘点 / 清单 | 2 封面 → 14 速览卡 → 17 工具卡 ×N → 20 对比卡 → 26 案例卡 → 11 总结卡 → 33 | 13 数据卡、32 表格、15 受众卡、36 CTA |
| 产品评测 / 案例拆解 | 2 封面 → 15 受众卡 → 4 章节骨架 → 29 解读卡 → 28 图文卡 → 20 对比卡 → 12 最终判断 → 33 | 13 数据卡、25 参数条、21 误区卡、27 方案卡 |
| 观点 / 深度分析 | 2 封面 → 3 导航 → 4+7 论证骨架 → 10 观点卡 → 21 误区卡 → 22 时间线 → 12 最终判断 → 33 | 34 宣言卡、18 承接卡、9 引用块 |
| 数据复盘 / 报告 | 2 封面 → 13 数据卡 → 32 表格 → 22 时间线 → 26 案例卡 → 11 总结卡 → 33 | 12 最终判断、20 对比卡、29 解读卡 |
| 方案 / 商业稿 | 2 封面 → 3 导航 → 5+7 骨架 → 27 方案卡 → 25 参数条 → 24 FAQ → 36 CTA → 33 | 20 对比卡、26 案例卡、16 清单 |

---

## Markdown → 组件映射规则表

| Markdown 元素 | 对应组件 |
|--------------|---------|
| `# 标题` / frontmatter `title` | Hero 封面卡主标题（组件 2），原文标题不复述进正文 |
| 文章最开头的 `> 引用` | 并入 Hero 封面卡的一句话简介；过长则用组件 9 引用块放其后 |
| `## 章节标题` | 章节编号卡（组件 4），按顺序编 01/02/03，末章结语用 `∞` |
| `### 子标题` | 小标签标题（组件 5）或 子标题（组件 6），同一篇内风格统一 |
| 正文段落 | 正文段落（组件 7）+ 蓝下划线（8b）每段 1~3 处 |
| `**加粗**` | 主色加粗（8a，全文 ≤5 处）或去粗用 8b 下划线，视语义强弱 |
| `==高亮==` | 浅蓝底高亮（8c） |
| `<u>` / `++文字++` | GitHub 蓝下划线（8b） |
| `~~删除线~~` | 删除线（8f） |
| `` `code` `` | 行内代码（8d） |
| ` ``` 代码块 ``` ` | **通用增量库** 1a 深色 / 1b 浅色代码块（技术文章默认 1b 浅色，更贴 GitHub 气质）；行内命令同理 |
| 非开头 `> 引用` | 引用高亮块（组件 9）；核心金句升级为观点强调卡（组件 10） |
| `![说明](url)` | 图片容器（组件 30），有说明才加说明行；卡片内配图用 28/29 |
| `- 无序列表` | 短列表用 31a；带说明的并列条目升级为 17 工具卡或 14 速览卡 |
| `1. 有序列表` | 操作步骤升级为 19 步骤流；普通序列用 31b |
| Markdown 表格 | 真实数据表用组件 32；版本/方案对比改用 27 或 20 |
| `---` 分割线 | 组件 37（正文中慎用，靠组件间距分隔即可） |
| 待补素材占位 `【插入…】` | **通用增量库** 2c 居中素材占位板块 |
| 文末已有"我是 XXX"署名段 | 并入作者卡（组件 33），沿用原文署名，不再另生成 |
