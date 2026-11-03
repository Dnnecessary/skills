# 公众号排版组件库 —— 摸鱼绿纸感

> **使用说明**：本组件库为「摸鱼绿纸感」主题（以「摸鱼绿」组件库为母本整体复制，组件结构、组件名、文案占位、字号铁律全部一致，**只替换为「摸鱼票据风」的纸感配色**），所有组件使用**内联样式**，可直接复制粘贴到微信公众号编辑器。
>
> **设计风格**：米黄纸感 + 极简编辑骨架。emerald 主色 + 黄色高亮点睛、标签化章节、11a 石墨灰直角标签；开头用白卡直角引言卡（暖灰细边框 + 大字金句 + 绿色点睛）与三列看点卡（极浅纸灰直角线框卡），变化在底色与灰阶——页面底由纯白换成`#FFFEF8` 米黄纸，正文由冷灰 `#374151` 转暖为 `#555555`，标题转墨黑 `#1a1a1a`，边框/分割线/浅灰底全部暖化。白卡片浮在纸面上，读感更接近印刷内页而非 App 界面。
>
> **与母本「摸鱼绿」的关系**：组件编号、HTML 结构、11 种行内样式、14px 正文 / 1.9 行高铁律全部继承，**改动有三处**——① 颜色值（映射表见下）；② 全局容器字体栈改为 CJK 优先（遵守 SKILL 9d，保证中文引号渲染为全角占格）；③ **卡片外形直角化**（2026-11-03 用户指定，对齐「摸鱼票据风」）——所有卡片/容器组件不带圆角，票据风那套黑描边、硬阴影、撕票线仍**没有**引入。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id、`position:fixed/absolute`、`float`、`@media`/`@keyframes`、`display:grid`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`linear-gradient`（可渲染但有暗色模式检测风险，文字背景默认用纯色）、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>` 等基础标签
>
> **WeChat 兼容铁律**（本主题组件全部已按此写好，改动时必须遵守）：
> - 所有"装饰性空元素"（圆点、渐变分割线、装饰短横、时间线竖线）**必须在内部放 `<span leaf=""><br></span>` 占位**，否则微信会剥掉样式
> - **不要把 `font-size`/`border-bottom` 打在 `<strong>` 上**，也不要在同一个 `<p>` 里混多个不同 `font-size`——微信编辑器会自动"纠正"导致样式被重写。正确做法：拆成多个 `<p>`，每个 `<p>` 只有一个字号；高亮样式统一挂在外层 `<span>` 上
> - 不用 `position:absolute` 做划线/高亮，删除线用 `text-decoration:line-through`
> - 结构化区域（如引言卡右下署名、看点卡某列）没有内容时**整块删掉**，不留空 section

---

## 设计变量速查表

```
页面纸感底：   #FFFEF8（本主题与母本最大的差别）
主色调：       #059669（emerald-600）
辅色：         #10B981（emerald-500）
浅绿装饰：     #34D399 / #6EE7B7 / #A7F3D0
浅绿边框：     #BBF7D0
浅绿背景：     #ECFDF5 / #F0FDF4
黄色高亮：     #FBEEB1
黄色背景（警告）：#FFFBEB
黄色文字（警告）：#92400E
红色下划线：   #FECACA（对比/否定专用）
警告橙色：     rgb(255,76,0)
警告灰色：     rgb(136,136,136)
标题色：       #1a1a1a
正文色：       #555555
次要文字：     #777777
注释/标签：    #999999
辅助文字：     #A9A49A
分隔线：       #DDD8CB
浅边框：       #EAE7DE
浅灰背景：     #EFEBE0
极浅灰：       #FBFAF4
卡片/内容底：  #ffffff（白卡片浮在纸感底上）
石墨灰标签底： #F4F4F5（11a 直角标签专用，取自石墨极简）
石墨灰标签字： #52525B（11a 标签文字与圆点，取自石墨极简）
代码背景：     #F3F4F6（沿用票据风，保持冷灰以区分代码）
代码字色：     #1F2937
正文字号：     14px（不可改）
正文行高：     1.9
全局行高：     1.75
字间距：       0.5px
最大宽度：     677px
内容区边距：   0 20px（模块左右各 20px）
```

### 与母本「摸鱼绿」的配色映射

| 母本 | 本主题 | 角色 |
|---|---|---|
| `#ffffff`（页面底） | `#FFFEF8` | 页面纸感底（卡片仍用白） |
| `#111827` | `#1a1a1a` | 标题墨黑 |
| `#374151` | `#555555` | 正文 |
| `#4B5563` | `#777777` | 次要文字 |
| `#6B7280` | `#999999` | 注释 / 标签 |
| `#9CA3AF` | `#A9A49A` | 辅助文字（温灰） |
| `#E5E7EB` | `#EAE7DE` | 浅边框 |
| `#D1D5DB` | `#DDD8CB` | 分割线 / 虚线 |
| `#F3F4F6` | `#EFEBE0` | 浅灰背景、发丝线（代码背景除外） |
| `#F9FAFB` | `#FBFAF4` | 极浅纸灰（表格斑马行、浅块底） |
| 绿色系 / 红色下划线 | **字节级不变** | 主色与强调语义完全继承 |
| 黄色系 `#FDE68A` | `#FBEEB1`（2026-11-03 用户指定） | 本主题专色黄，全篇黄色统一这一种 |

> **强调色锁定（硬规则）**：组件 6 的 9 种行内样式中，6a 绿加粗 `#059669`、6e 绿下划线 `#A7F3D0`、6f 红下划线 `#FECACA` 与母本「摸鱼绿」**逐字节一致**，改配色时**不得**动这些值；**唯一例外是黄色系**——本主题黄色全部用专色 `#FBEEB1`（6c 黄高亮、6d 黄底高亮、6h 黄标签，以及 9c 黄竖条、10c 黄警告边框等所有黄色位），2026-11-03 由用户指定，同样**不得擅改**。全篇黄色只允许这一种，出现任何其他黄色值即为错误。
>
> 核对方法：6a/6e/6f 与母本比对 `## 组件 6` 到 `## 组件 7` 应完全相同；黄色位全文件检索不得出现 `#FDE68A`。

字体栈：`'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif`（CJK 优先，保证 `""''` 渲染为中文全角字形）

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;background:#fffef8;font-family:'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif;color:#555555;line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">

  <!-- 所有组件放在这里 -->

</section>
```

---

## 组件 2 开头引言卡（白卡直角 + 大字金句）

> **来源**：结构取自「石墨极简」组件 2（左右边距 20px 栅格，与正文对齐），外形与配色已**回归本主题语言并直角化**——四周 1px 暖灰细边框 `#EAE7DE`，**不带圆角**（与全主题卡片一致的票据式直角），纯白卡底 `#FFFFFF` 浮在米黄纸面上；QUOTE 标签用主绿 `#059669` 点睛，金句内关键词用主题绿色下划线 `#A7F3D0`（同 6e）。无阴影、无色块，靠细边框与留白出质感。`margin-top:32px` 与页面顶部拉开距离，不贴头。
>
> **文案策略（先读，比代码重要）**：
> - 引言卡金句与公众号外标题是**两层**，视角错开——外标题卖"为什么点开"，引言卡卖"核心观点是什么"
> - 金句**只能来自原文或用户给定**（文章第一段、核心论点、范文首句等），**禁止由排版方自创判断句**
> - 右下署名按文章实际作者填；未知则**整行删掉**，不留空行

```html
<section style="margin:32px 20px 36px;padding:30px 24px 24px;border:1px solid #EAE7DE;background:#FFFFFF;">
  <p style="font-size:11px;color:#059669;letter-spacing:2px;margin:0 0 18px;font-weight:600;">
    <span leaf="">QUOTE</span>
  </p>
  <p style="font-size:18px;font-weight:700;color:#1a1a1a;margin:0 0 8px;line-height:1.7;letter-spacing:0.5px;">
    <span leaf="">{{金句前段}}</span>
    <span style="border-bottom:2px solid #A7F3D0;"><span leaf="">{{下划线关键词}}</span></span>
    <span leaf="">{{金句收尾}}</span>
  </p>
  <p style="text-align:right;font-size:12px;color:#A9A49A;margin:16px 0 0;letter-spacing:1px;">
    <span leaf="">—— {{作者名}}</span>
  </p>
</section>
```

> **关键词下划线**：默认主题绿 `#A7F3D0`（同 6e，与整主题呼应）；想更克制可换石墨灰 `border-bottom:2px solid #52525B`（与 11a 灰标签同支灰）。金句内最多标 1~2 处。
> **字数控制**：金句 ≤60 字为佳（18px 下约 3 行），过长会削弱"大字"的冲击力。
> **无合适金句时**：整块删掉，直接从组件 3 本文看点开始，不要硬凑一句。

---

## 组件 3 本文看点（三列极简线框目录卡）

> **来源**：结构取自「石墨极简」组件 3，外形已回归本主题语言并直角化——四周 1px 暖灰细边框 `#EAE7DE`，**不带圆角**（与引言卡同支直角白/纸灰卡），卡底 `#FBFAF4` 极浅纸灰、编号 `#A9A49A`、标题 `#1a1a1a`。
>
> 3 个及以上章节时生成。**只展示精选 3 个核心看点，不是全量章节列表**——全量目录会让读者放弃阅读。章节数 ≥4 时也仍然只选 3 个。

```html
<section style="padding:0 20px 36px;">
  <p style="font-size:11px;color:#A9A49A;margin:0 0 16px;letter-spacing:2px;">
    <span leaf="">本文看点</span>
  </p>
  <section style="display:flex;justify-content:space-between;">
    <section style="flex:1;background:#FBFAF4;border:1px solid #EAE7DE;padding:18px 12px 16px;margin-right:8px;">
      <p style="font-size:11px;color:#A9A49A;font-weight:500;margin:0 0 8px;letter-spacing:1px;"><span leaf="">01</span></p>
      <p style="font-size:13px;font-weight:700;color:#1a1a1a;margin:0;line-height:1.5;"><span leaf="">{{看点一}}</span></p>
    </section>
    <section style="flex:1;background:#FBFAF4;border:1px solid #EAE7DE;padding:18px 12px 16px;margin-right:8px;">
      <p style="font-size:11px;color:#A9A49A;font-weight:500;margin:0 0 8px;letter-spacing:1px;"><span leaf="">02</span></p>
      <p style="font-size:13px;font-weight:700;color:#1a1a1a;margin:0;line-height:1.5;"><span leaf="">{{看点二}}</span></p>
    </section>
    <section style="flex:1;background:#FBFAF4;border:1px solid #EAE7DE;padding:18px 12px 16px;">
      <p style="font-size:11px;color:#A9A49A;font-weight:500;margin:0 0 8px;letter-spacing:1px;"><span leaf="">03</span></p>
      <p style="font-size:13px;font-weight:700;color:#1a1a1a;margin:0;line-height:1.5;"><span leaf="">{{看点三}}</span></p>
    </section>
  </section>
</section>
```

> **只有两项时**：删掉第三列，两个卡片各 `flex:1`，最后一列不加 `margin-right`。
> **看点标题 ≤8 字**：13px 字号下三列宽度有限，超过两行会把卡片撑高。

---

## 组件 4 章节标题 chapter-title（绿色编号方块 + 粗黑横线）

> **形态（2026-11-03 按票据风实物校准）**：这是「摸鱼票据风」的章节标题结构，**直接照搬，不要自创**——左侧一块**实心绿色直角方块**只装编号（白字 12px/800/字距 2px），紧跟中文标题（18px/800 墨黑），再跟灰色英文小标 `/ MATERIAL`（12px `#888`），整排底部压一条 **2px 实心黑线 `#1a1a1a`** 并向下留 12px 间距。没有 `PART` 小字、没有上下双细线、没有竖线分隔。

第一个章节用 `margin-top:16px`，后续章节用 `margin-top:48px`。最后一章编号用 `///`，英文小标改为 `/ LAST`。

```html
<section style="margin-top:48px;margin-bottom:32px;padding:0 20px;">
  <section style="display:flex;align-items:center;gap:12px;margin-bottom:24px;padding-bottom:12px;border-bottom:2px solid #1a1a1a;">
    <section style="background:#059669;color:#FFFFFF;font-size:12px;font-weight:800;padding:6px 12px;letter-spacing:2px;"><span leaf="">{{01}}</span></section>
    <section style="font-size:18px;font-weight:800;color:#1a1a1a;letter-spacing:1px;"><span leaf="">{{中文标题}}</span></section>
    <section style="font-size:12px;color:#888888;"><span leaf="">/ {{ENGLISH}}</span></section>
  </section>

  <!-- 本章节正文内容放在这里 -->

</section>
```

> **英文小标写法**：斜杠前留一个半角空格（`/ MATERIAL`、`/ MODEL ESSAY`、`/ COMMENT`），全大写；没有合适英文时写 `/ NOTE`，不要留空 section。
> **末章**：编号位写 `///`，`letter-spacing:1px`（避免三位符号过宽），英文小标用 `/ LAST`。
> **铁律**：编号方块**只放编号**，不要塞 `PART`、不要放中文；绿块与标题同一行垂直居中，横线是 2px 纯黑实线，不是暖灰细线。

---

## 组件 5 正文段落 paragraph

```html
<p style="margin-bottom:16px;font-size:14px;line-height:1.9;text-align:justify;">
  <span leaf="">{{正文内容}}</span>
</p>
```

段间距较大时用 `margin-bottom:24px`。

---

## 组件 6 行内样式（9 种 + 使用原则）

### 6a. 绿色加粗（核心概念、关键结论、品牌名/产品名）

```html
<strong style="color:#059669;"><span leaf="">文字</span></strong>
```

### 6b. 绿色背景标签

```html
<strong style="color:#059669;background:rgba(5,150,105,0.1);padding:0 4px;border-radius:2px;"><span leaf="">文字</span></strong>
```

### 6c. 黄色纯色高亮（一段话中最想让读者注意的短语，每段不超过 1-2 处）

```html
<span style="background:#FBEEB1;padding:0 4px;border-radius:2px;font-weight:600;color:#111827;"><span leaf="">文字</span></span>
```

### 6d. 黄色底部高亮（下划线效果）

```html
<span style="color:#111827;font-weight:bold;border-bottom:3px solid #FBEEB1;"><span leaf="">文字</span></span>
```

### 6e. 绿色下划线（次要强调，**正文关键词的默认标记**）

```html
<span style="border-bottom:2px solid #A7F3D0;font-weight:600;"><span leaf="">文字</span></span>
```

### 6f. 红色下划线（对比、否定、需要注意的内容）

```html
<span style="border-bottom:2px solid #FECACA;"><span leaf="">文字</span></span>
```

### 6g. 代码标签（行内代码）

```html
<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:13px;font-weight:600;"><span leaf="">code</span></span>
```

### 6h. 获取方式标签（黄色背景）

```html
<span style="background:#FBEEB1;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:13px;font-weight:700;"><span leaf="">「关键词」</span></span>
```

### 6i. 删除线灰色（旧的/被淘汰的概念）

```html
<span style="background:#F3F4F6;color:#6B7280;padding:2px 6px;border-radius:4px;font-size:13px;text-decoration:line-through;font-weight:600;"><span leaf="">旧词</span></span>
```

**使用原则**：
1. 绿色加粗用于核心概念、关键结论、品牌名/产品名
2. 黄色高亮每段不超过 1-2 处
3. 绿色下划线用于次要强调（正文关键词逐段标记用它）
4. 红色下划线用于对比、否定
5. 删除线灰色用于被淘汰的概念
6. 一段文字中不要同时使用超过 2 种高亮效果

---

## 组件 7 内容标签组（STEP / CASE / SKILL / TOOL）

### 7a. step-label（STEP 步骤标签）

```html
<section style="margin-bottom:24px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:#1a1a1a;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;"><span leaf="">STEP 01</span></span>
    <h4 style="font-size:15px;font-weight:800;color:#1a1a1a;margin:0;">
      <span leaf="">{{步骤标题}}</span>
    </h4>
  </section>
  <p style="font-size:14px;margin:0 0 16px;color:#777777;line-height:1.9;text-align:justify;">
    {{步骤内容}}
  </p>
</section>
```

### 7b. case-label（CASE 案例标签）

```html
<section style="margin-bottom:28px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:#EAE7DE;color:#999999;font-size:10px;font-weight:700;padding:2px 8px;"><span leaf="">CASE 01</span></span>
    <h4 style="font-size:15px;font-weight:800;color:#1a1a1a;margin:0;">
      <span leaf="">{{案例标题}}</span>
    </h4>
  </section>
  <!-- 案例内容 -->
</section>
```

### 7c. skill-label / tool-label（编号标签）

```html
<section style="margin-bottom:28px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:#1a1a1a;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;"><span leaf="">SKILL 1</span></span>
    <h4 style="font-size:15px;font-weight:800;color:#1a1a1a;margin:0;">
      <span leaf="">{{名称}}</span>
    </h4>
  </section>
</section>
```

`SKILL 1` 可替换为 `TOOL 摄像机`、`TOOL 打光` 等。

---

## 组件 8 代码/命令/Prompt

### 8a. prompt-block（PROMPT 展示块）

```html
<p style="font-size:13px;color:#555555;margin:0 0 16px;line-height:1.8;">
  <span style="display:inline-block;background:#059669;color:#fff;font-size:11px;font-weight:700;padding:1px 7px;border-radius:3px;margin-right:6px;vertical-align:middle;letter-spacing:0.5px;"><span leaf="">PROMPT</span></span>
  <span style="font-size:12px;color:#A9A49A;font-weight:700;"><span leaf="">{{提示词内容}}</span></span>
</p>
```

### 8b. cmd-block（CMD 单行命令块）

```html
<p style="font-size:13px;color:#555555;margin:0 0 24px;line-height:1.8;">
  <span style="display:inline-block;background:#1a1a1a;color:#fff;font-size:11px;font-weight:700;padding:1px 7px;border-radius:3px;margin-right:6px;vertical-align:middle;letter-spacing:0.5px;"><span leaf="">CMD</span></span>
  <span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:13px;font-weight:600;"><span leaf="">{{命令内容}}</span></span>
</p>
```

### 8c. 多行代码块 → 用通用增量库

多行代码块**不设主题专属组件**，直接用 `common-components.md` 的 1a 深色代码块（每行一个 `<p style="margin:0">`，禁 `white-space:pre`）；浅色场景用 1b 并把左竖条换成 `#059669`。

---

## 组件 9 引用与亮点

### 9a. quote-box（灰色虚线引用框）

所有引用、补充说明的**默认组件**（虚线框是本主题的风格特征，仅此组件与 9b 保留 dashed）：

```html
<section style="background:#FBFAF4;border:1px dashed #DDD8CB;padding:12px 16px;margin-bottom:24px;text-align:justify;">
  <p style="font-size:13px;color:#555555;margin:0;line-height:1.6;">
    {{引用内容，可嵌入绿色加粗等内联样式}}
  </p>
</section>
```

### 9b. oneliner-card（一句话亮点卡片）

> 兼容性关键规则：**不要把 `font-size` 打在 `<strong>` 上**，不要在同一个 `<p>` 里混多个字号；高亮样式统一挂在外层 `<span>` 上。

单行版（只有主金句）：

```html
<section style="background:#FFF;border:1px dashed #BBF7D0;padding:14px 16px;margin-bottom:24px;text-align:center;">
  <p style="margin:0;line-height:1.6;">
    <span style="font-size:15px;color:#059669;font-weight:bold;border-bottom:3px solid #FBEEB1;padding-bottom:2px;"><span leaf="">{{亮点内容}}</span></span>
  </p>
</section>
```

带前缀引导语版（两段式）：

```html
<section style="background:#FFF;border:1px dashed #BBF7D0;padding:14px 16px;margin-bottom:24px;text-align:center;">
  <p style="font-size:12px;color:#A9A49A;margin:0 0 6px;line-height:1.5;">
    <span leaf="">{{引导语}}</span>
  </p>
  <p style="margin:0;line-height:1.6;">
    <span style="font-size:15px;color:#059669;font-weight:bold;border-bottom:3px solid #FBEEB1;padding-bottom:2px;"><span leaf="">{{亮点内容}}</span></span>
  </p>
</section>
```

带下方补充说明版：

```html
<section style="background:#FFF;border:1px dashed #BBF7D0;padding:14px 16px;margin-bottom:24px;text-align:center;">
  <p style="margin:0 0 6px;line-height:1.6;">
    <span style="font-size:15px;color:#059669;font-weight:bold;border-bottom:3px solid #FBEEB1;padding-bottom:2px;"><span leaf="">{{高亮内容}}</span></span>
  </p>
  <p style="font-size:13px;color:#A9A49A;margin:0;line-height:1.5;">
    <span leaf="">{{补充说明}}</span>
  </p>
</section>
```

### 9c. subtitle-bar（小节标题 · 黄色竖条）

黄色竖条 + 标题文字（竖条与黄色高亮同色 `#FBEEB1`，不外扩到文字背后）：

```html
<p style="font-size:15px;font-weight:900;color:#1a1a1a;margin:0 0 16px;padding:2px 0 2px 10px;border-left:4px solid #FBEEB1;line-height:1.4;">
  <span leaf="">{{小节标题}}</span>
</p>
```

要点：

- 竖条用 `border-left` 实现，不额外放空 section——微信不会剥落，也不用占位符
- 竖条颜色固定 `#FBEEB1`，与 6c/6d 黄色高亮同一支黄色，全篇黄色只剩一种
- 需要更大上间距时加 `margin-top:32px`
- 想要旧版「黄色浅底标题」时，改用 6c 黄高亮包裹标题文字即可（不作为默认）

### 9d. center-divider（居中金句分隔）

```html
<p style="font-size:14px;margin-bottom:20px;text-align:center;color:#059669;font-weight:700;letter-spacing:1px;border-top:1px solid #EFEBE0;border-bottom:1px solid #EFEBE0;padding:12px 0;">
  <span leaf="">{{居中金句}}</span>
</p>
```

---

## 组件 10 提示与信息

### 10a. warn-tip（踩坑提示）

```html
<section style="padding:6px 0 4px;margin-bottom:16px;">
  <p style="margin-bottom:6px;font-size:12px;font-weight:700;color:#A9A49A;letter-spacing:1px;">
    <span style="color:rgb(255,76,0);"><span leaf="">！踩坑提示 🕳</span></span>
  </p>
  <p style="font-size:13px;color:#555555;margin:0;line-height:1.7;">
    <span style="color:rgb(136,136,136);font-weight:bold;"><span leaf="">{{提示内容}}</span></span>
  </p>
</section>
```

标题可改为 `！真正的战场 🕳`、`！目前最大的槽点 🕳` 等。

### 10b. green-tip（绿色提示）

```html
<section style="padding:6px 0 4px;margin-bottom:16px;">
  <p style="margin-bottom:6px;font-size:12px;font-weight:700;color:#A9A49A;letter-spacing:1px;">
    <span style="color:#059669;"><span leaf="">✦ {{提示标题}}</span></span>
  </p>
  <p style="font-size:13px;color:#555555;margin:0;line-height:1.7;">
    {{提示内容}}
  </p>
</section>
```

### 10c. yellow-warning（黄色警告框）

```html
<section style="background:#FFFBEB;border:1px solid #FBEEB1;padding:12px 16px;margin-bottom:20px;">
  <p style="font-size:13px;color:#92400E;margin:0;font-weight:700;">
    <span leaf="">{{警告内容}}</span>
  </p>
</section>
```

### 10d. green-info（绿色信息框）

```html
<section style="background:#F0FDF4;padding:12px 16px;border:1px solid #BBF7D0;margin-bottom:20px;">
  <p style="font-size:13px;color:#555555;margin:0;line-height:1.7;text-align:justify;">
    {{信息内容}}
  </p>
</section>
```

---

## 组件 11 布局组件

### 11a. pill-row（石墨灰横向直角标签组）

用于「适用话题」「关键词」「标签」等**并列短词**：横向排列、宽度不够时自动折行，不占竖直版面。配色取「石墨极简」的灰阶（标签底 `#F4F4F5`、文字与圆点 `#52525B`），在米黄纸感底上呈中性灰，不与绿色主色争抢。**标签外形为直角矩形**（2026-11-03 直角化，去掉了原来的胶囊圆头），内部圆点仍为圆形。

```html
<section style="margin-bottom:14px;">
  <p style="margin:0;font-size:13px;line-height:2.4;">
    <span style="display:inline-block;font-size:13px;font-weight:700;color:#52525B;background:#F4F4F5;padding:3px 10px;margin:0 6px 6px 0;"><span style="display:inline-block;width:6px;height:6px;background:#52525B;border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf="">{{标签1}}</span></span><span style="display:inline-block;font-size:13px;font-weight:700;color:#52525B;background:#F4F4F5;padding:3px 10px;margin:0 6px 6px 0;"><span style="display:inline-block;width:6px;height:6px;background:#52525B;border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf="">{{标签2}}</span></span><span style="display:inline-block;font-size:13px;font-weight:700;color:#52525B;background:#F4F4F5;padding:3px 10px;margin:0 6px 6px 0;"><span style="display:inline-block;width:6px;height:6px;background:#52525B;border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf="">{{标签3}}</span></span>
  </p>
</section>
```

**横向要点**：所有标签 `span` 必须放在**同一个 `<p>` 内**，各自 `display:inline-block` + `margin:0 6px 6px 0` 撑开横向间距；满一行自动折行。**不要**每个标签套一个 `<section>`/`<p>`，那是竖排列表（旧写法 11a-pill-list 已废弃）。外层 `<p>` 字号固定 `13px`，与标签内字号一致，避免微信重写样式。

带说明文字版（标签较多且每项带一句解释时用，**此项保持竖排**，颜色同样用石墨灰）：

```html
<section style="margin-bottom:14px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;font-size:13px;font-weight:700;color:#52525B;background:#F4F4F5;padding:3px 10px;"><span style="display:inline-block;width:6px;height:6px;background:#52525B;border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf="">{{标题}}</span></span>
  </p>
  <p style="font-size:13px;color:#777777;margin:0;line-height:1.7;text-align:justify;">
    <span leaf="">{{描述内容}}</span>
  </p>
</section>
```

### 11b. flow-cards（三步横排流程卡片）

```html
<section style="background:#FBFAF4;padding:16px;border:1px solid #EFEBE0;margin-bottom:24px;">
  <section style="display:flex;align-items:stretch;justify-content:center;gap:6px;">
    <section style="flex:1;text-align:center;padding:10px 8px;background:#059669;">
      <p style="font-size:13px;font-weight:800;color:#fff;margin:0 0 3px;">
        <span leaf="">{{步骤1标题}}</span>
      </p>
      <p style="font-size:10px;color:rgba(255,255,255,0.8);margin:0;line-height:1.5;">
        <span leaf="">{{步骤1描述}}</span>
      </p>
    </section>
    <section style="display:flex;align-items:center;color:#DDD8CB;font-size:14px;padding:0 4px;">
      <span leaf="">→</span>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid #EAE7DE;">
      <p style="font-size:13px;font-weight:800;color:#1a1a1a;margin:0 0 3px;">
        <span leaf="">{{步骤2标题}}</span>
      </p>
      <p style="font-size:10px;color:#A9A49A;margin:0;line-height:1.5;">
        <span leaf="">{{步骤2描述}}</span>
      </p>
    </section>
    <section style="display:flex;align-items:center;color:#DDD8CB;font-size:14px;padding:0 4px;">
      <span leaf="">→</span>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid #A7F3D0;">
      <p style="font-size:13px;font-weight:800;color:#059669;margin:0 0 3px;">
        <span leaf="">{{步骤3标题}}</span>
      </p>
      <p style="font-size:10px;color:#A9A49A;margin:0;line-height:1.5;">
        <span leaf="">{{步骤3描述}}</span>
      </p>
    </section>
  </section>
  <p style="font-size:12px;color:#A9A49A;text-align:center;margin:12px 0 0;letter-spacing:0.5px;">
    <span leaf="">{{底部说明文字}}</span>
  </p>
</section>
```

箭头 `→` 可替换为 `×` 做对比型布局。

### 11c. three-col-cards（三列对比卡片）

```html
<section style="background:#FBFAF4;padding:16px;border:1px solid #EFEBE0;margin-bottom:28px;">
  <section style="display:flex;align-items:stretch;justify-content:center;gap:6px;">
    <section style="flex:1;text-align:center;padding:10px 8px;background:#059669;">
      <p style="font-size:13px;font-weight:800;color:#fff;margin:0 0 3px;">
        <span leaf="">{{卡片1标题}}</span>
      </p>
      <p style="font-size:10px;color:rgba(255,255,255,0.8);margin:0;line-height:1.5;">
        <span leaf="">{{卡片1描述}}</span>
      </p>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid #EAE7DE;">
      <p style="font-size:13px;font-weight:800;color:#1a1a1a;margin:0 0 3px;">
        <span leaf="">{{卡片2标题}}</span>
      </p>
      <p style="font-size:10px;color:#A9A49A;margin:0;line-height:1.5;">
        <span leaf="">{{卡片2描述}}</span>
      </p>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid #EAE7DE;">
      <p style="font-size:13px;font-weight:800;color:#1a1a1a;margin:0 0 3px;">
        <span leaf="">{{卡片3标题}}</span>
      </p>
      <p style="font-size:10px;color:#A9A49A;margin:0;line-height:1.5;">
        <span leaf="">{{卡片3描述}}</span>
      </p>
    </section>
  </section>
</section>
```

### 11d. timeline（时间线列表）

```html
<section style="display:flex;margin-bottom:28px;">
  <section style="display:flex;flex-direction:column;align-items:center;margin-right:16px;flex-shrink:0;">
    <section style="width:14px;height:14px;border-radius:50%;border:3px solid #059669;background:#fff;margin-top:4px;box-shadow:0 0 0 2px #fff;">
      <span leaf=""><br></span>
    </section>
    <section style="width:2px;background:#EAE7DE;flex:1;margin-top:4px;min-height:48px;">
      <span leaf=""><br></span>
    </section>
  </section>
  <section style="flex:1;padding-bottom:12px;">
    <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
      <span style="display:inline-block;background:#1a1a1a;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;"><span leaf="">{{CASE 01}}</span></span>
      <h4 style="font-size:15px;font-weight:800;color:#1a1a1a;margin:0;">
        <span leaf="">{{标题}}</span>
      </h4>
    </section>
    <p style="font-size:11px;font-weight:600;color:#A9A49A;letter-spacing:1px;margin:0 0 12px;">
      <span leaf="">{{英文副标题}}</span>
    </p>
    <p style="font-size:14px;margin:0 0 16px;color:#777777;line-height:1.7;text-align:justify;">
      {{内容}}
    </p>
  </section>
</section>
```

最后一个时间线节点去掉竖线部分。

### 11e. tool-card（工具说明卡片）

基本版：

```html
<section style="background:#fff;padding:16px 20px;box-shadow:0 4px 16px rgba(5,150,105,0.12);margin-bottom:24px;">
  <p style="font-size:13px;color:#555555;margin:0;line-height:1.8;">
    {{说明内容}}
  </p>
</section>
```

居中高亮版（同 oneliner-card 规则：拆多个 `<p>`，不要 `<strong>` 带 font-size/border-bottom）：

```html
<section style="background:#fff;padding:16px 20px;box-shadow:0 4px 16px rgba(5,150,105,0.12);margin-bottom:24px;text-align:center;">
  <p style="font-size:13px;color:#A9A49A;margin:0 0 6px;line-height:1.5;">
    <span leaf="">{{小字}}</span>
  </p>
  <p style="margin:0;line-height:1.6;">
    <span style="font-size:15px;color:#059669;font-weight:bold;border-bottom:3px solid #FBEEB1;padding-bottom:2px;"><span leaf="">{{高亮大字}}</span></span>
  </p>
</section>
```

### 11f. table（表格）

本主题保留 `<table>` 组件（摸鱼绿实测微信可用）；Markdown 表格优先用它，数据密度低时也可改用 11c 三列卡片。

```html
<section style="margin-bottom:24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr>
        <th style="background:#059669;color:#fff;font-weight:700;padding:8px 12px;text-align:left;"><span leaf="">{{列标题1}}</span></th>
        <th style="background:#059669;color:#fff;font-weight:700;padding:8px 12px;text-align:left;"><span leaf="">{{列标题2}}</span></th>
        <th style="background:#059669;color:#fff;font-weight:700;padding:8px 12px;text-align:left;"><span leaf="">{{列标题3}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;"><span leaf="">{{内容}}</span></td>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;"><span leaf="">{{内容}}</span></td>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;"><span leaf="">{{内容}}</span></td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;background:#FBFAF4;"><span leaf="">{{内容}}</span></td>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;background:#FBFAF4;"><span leaf="">{{内容}}</span></td>
        <td style="padding:8px 12px;border-bottom:1px solid #EAE7DE;color:#555555;background:#FBFAF4;"><span leaf="">{{内容}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

偶数行自动带浅灰背景 `#FBFAF4`，列数按实际需求增减。

### 11g. ordered-list（数字编号列表）

```html
<section style="margin-bottom:24px;">
  <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#059669;color:#fff;font-size:11px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:2px;"><span leaf="">1</span></span>
    <p style="font-size:14px;color:#555555;margin:0;line-height:1.9;flex:1;">
      <span leaf="">{{列表项内容}}</span>
    </p>
  </section>
  <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#059669;color:#fff;font-size:11px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:2px;"><span leaf="">2</span></span>
    <p style="font-size:14px;color:#555555;margin:0;line-height:1.9;flex:1;">
      <span leaf="">{{列表项内容}}</span>
    </p>
  </section>
  <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#059669;color:#fff;font-size:11px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:2px;"><span leaf="">3</span></span>
    <p style="font-size:14px;color:#555555;margin:0;line-height:1.9;flex:1;">
      <span leaf="">{{列表项内容}}</span>
    </p>
  </section>
</section>
```

---

## 组件 12 媒体组件

### 12a. image（图片容器）

```html
<section style="text-align:center;margin-bottom:24px;overflow:hidden;">
  <!-- 保留原始图片代码不修改 -->
</section>
```

### 12b. video-card（视频容器卡片）

```html
<section style="background:#fff;padding:12px;margin-bottom:32px;border:2px solid #059669;box-shadow:0 4px 12px rgba(5,150,105,0.1);">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="width:8px;height:8px;background:#059669;border-radius:50%;"><span leaf=""><br></span></span>
    <span style="font-size:11px;color:#059669;font-weight:700;letter-spacing:1px;"><span leaf="">VIDEO 01</span></span>
    <span style="flex:1;height:1px;background:linear-gradient(to right,rgba(5,150,105,0.2),transparent);"><span leaf=""><br></span></span>
    <span style="font-size:11px;color:#A9A49A;"><span leaf="">{{视频描述}}</span></span>
  </section>
  <section style="overflow:hidden;">
    <!-- 保留原始视频代码不修改 -->
  </section>
</section>
```

---

## 组件 13 结尾组件

### 13a. footer-cta（互动三连区，即本主题的签名/CTA 区）

固定文案照写；SVG 图标微信支持，原样保留。

```html
<section style="background:#FBFAF4;border:1px solid #EAE7DE;padding:32px 20px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.03);margin:0 0 24px;">
  <p style="font-size:13px;font-weight:bold;color:#1a1a1a;margin-bottom:20px;line-height:1.6;">
    <span leaf="">既然看到这里了，如果觉得有用，随手点个赞、在看、转发三连吧。</span>
  </p>
  <section style="display:flex;justify-content:center;gap:24px;margin-bottom:16px;">
    <section style="text-align:center;cursor:pointer;color:#777777;">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid #EFEBE0;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">点赞</span></span>
    </section>
    <section style="text-align:center;cursor:pointer;color:#777777;">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid #EFEBE0;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">在看</span></span>
    </section>
    <section style="text-align:center;cursor:pointer;color:#059669;">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#ECFDF5;box-shadow:0 2px 4px rgba(5,150,105,0.15);border:1px solid #A7F3D0;">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18v-4a8 8 0 0 1 8-8h8"></path><polyline points="16 2 20 6 16 10"></polyline></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">转发</span></span>
    </section>
  </section>
  <p style="font-size:10px;color:#A9A49A;letter-spacing:1px;margin:0;">
    <span leaf="">THANKS FOR READING</span>
  </p>
</section>
```

**签名文案适配**：SKILL.md 的作者签名（"我是 {{作者名}}…"两段，默认占位、由用户替换）以正文段落（组件 5）形式放在 footer-cta **之前**；footer-cta 内部文案保持上面的固定句式，两者不重复出现"三连"字样时可将签名第二段并入 footer-cta 顶部文字。

### 13b. brand-card（品牌尾图）

```html
<section style="text-align:center;" nodeleaf="">
  <!-- 保留原始品牌尾图代码不修改 -->
</section>
```

有品牌尾图素材时放在 footer-cta 之后，无素材整块省略。

---

## 完整文章模板骨架

```html
<section style="max-width:677px;margin:0 auto;background:#fffef8;font-family:'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif;color:#555555;line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">

  <!-- 1. 开头引言卡（组件2 quote-open：白卡直角 + 暖灰细边框 + 18px 大字金句；无合适金句则整块删） -->

  <!-- 2. 本文看点（组件3 highlight-trio：三列极浅纸灰线框卡，只取 3 个核心看点，紧跟引言卡之下） -->

  <!-- 3. 前言正文（开场白，组件5 段落 × N，放 0 20px 边距的 section 内） -->

  <!-- 4. 第一章（组件4 chapter-title，margin-top:16px） -->
  <!--    章内：组件5 正文 + 组件6 行内样式 + 组件7 标签 + 组件8 代码 + 组件9 引用亮点 + 组件10 提示 + 组件11 布局 + 组件12 媒体 -->

  <!-- 5. 第二章…第N章（组件4，margin-top:48px） -->

  <!-- 6. 结语章（组件4 变体：编号 ///，PART 改 LAST，章名"写在最后"） -->

  <!-- 7. 互动三连（组件13a footer-cta，前面放固定签名段落） -->

  <!-- 8. 品牌尾图（组件13b，有素材才加） -->

</section>
```

**骨架顺序铁律**：引言卡 quote-open 在最上（无金句则省略），三列看点 highlight-trio **紧跟引言卡之下、前言正文之前**——读者先看全文地图再进入内容。引言卡与看点卡合计只做一次，正文中段不要重复。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 绿色加粗 6a / 黄底下划线 6d / oneliner-card 9b | 核心概念、产品名、关键结论 | 全文 ≤5 处 |
| **标记层** | 绿色下划线 6e（默认）/ 黄色纯色高亮 6c | 正文关键词强调 | 每段 1~3 处 |
| **容器层** | quote-box 9a / 提示 10x / 标签 11a / 卡片 11x | 引用、旁注、提示、结构化信息 | 按需 |

**克制原则**：
- 黄色高亮每段不超过 1-2 处；一段内不超过 2 种高亮效果
- 红色下划线只用于对比/否定，不做普通强调
- 绿色纯色背景仅出现在流程首卡、标签等结构位；开头引言卡与看点卡不加大色块，仅以绿字/绿下划线点睛

---

## 文章类型 → 组件组合配方

按 SKILL.md 第 3 步判定的文章类型选配方；核心组件构成本篇的排版主旋律，点缀组件按内容出现处使用，一篇文章点缀组件种类 ≤3，避免花哨。

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 教程/操作指南 | step-label 7a + cmd/prompt 8a/8b + 代码块（通用库1a） | warn-tip 10a、green-tip 10b、flow-cards 11b |
| 盘点/工具清单 | skill/tool-label 7c + tool-card 11e + pill-row 11a | table 11f、oneliner-card 9b |
| 观点/深度分析 | paragraph 5 + quote-box 9a + oneliner-card 9b | center-divider 9d、subtitle-bar 9c |
| 访谈/人物特稿 | paragraph 5 + quote-box 9a（引语）+ timeline 11d（经历脉络） | oneliner-card 9b、center-divider 9d |
| 数据复盘/报告 | three-col-cards 11c + table 11f + ordered-list 11g | green-info 10d、黄色纯色高亮 6c |
| 生活/情感随笔 | paragraph 5 + oneliner-card 9b + center-divider 9d | quote-box 9a（少量） |
| 案例实战 | case-label 7b / timeline 11d + step-label 7a | prompt-block 8a、yellow-warning 10c |

所有类型共用固定结构：引言卡 2（有金句才用）+ 本文看点 3 + 章节标题 4 + 签名/三连 13。

---

## Markdown → 摸鱼绿纸感 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| `# 标题` | 不使用 | 公众号文章标题在平台设置；引言卡金句从中提炼（视角错开，禁止复述外标题关键词） |
| 文章开头 `> 引言` | 组件 2 quote-open 引言卡 | 白卡直角 + 18px 大字金句 + 绿色下划线关键词；原文无金句则不生成 |
| `## 章节标题` | 组件 4 chapter-title | PART 01/02/03…，末章 /// + LAST |
| `### 子标题` | 组件 9c subtitle-bar | 黄色竖条 + 小节标题 |
| 普通段落 | 组件 5 paragraph | 每段主动标 1~3 处绿色下划线 6e |
| `**加粗文字**` | 组件 6a 绿色加粗 | 核心概念/品牌名 |
| `==高亮文字==` | 组件 6c 黄色纯色高亮 | 每段 ≤2 处 |
| `<u>下划线</u>` / `++文字++` | 组件 6e 绿色下划线 | 次要强调 |
| `~~删除线~~` | 组件 6i 删除线灰色 | 被淘汰的概念 |
| `> 引用段落`（非开头） | 组件 9a quote-box | 灰色虚线框（本主题特征） |
| 核心金句 | 组件 9b oneliner-card / 9d center-divider | 视觉焦点 |
| 操作步骤 | 组件 7a step-label（+ 8a/8b） | STEP 01/02… |
| 案例/场景 | 组件 7b case-label 或 11d timeline | CASE 01/02… |
| 技能/工具清单 | 组件 7c skill/tool-label + 11e tool-card | |
| Prompt 提示词 | 组件 8a prompt-block（短）/ 通用库 1a（长多行） | |
| 单行命令 | 组件 8b cmd-block | |
| ` ``` 多行代码块 ``` ` | 通用库 1a 深色（默认）/ 1b 浅色（左竖条换 #059669） | 每行一个 `<p style="margin:0">` |
| 行内 `` `code` `` | 组件 6g 代码标签 | |
| 并列要点 | 组件 11a pill-row | |
| 流程（3 步） | 组件 11b flow-cards | 箭头可换 × 做对比 |
| 三项对比 | 组件 11c three-col-cards | |
| 递进/时间脉络 | 组件 11d timeline | |
| Markdown 表格 | 组件 11f table | 偶数行浅灰底 |
| `1. 2. 3.` 编号列表 | 组件 11g ordered-list | |
| 注意/警告 | 组件 10a warn-tip / 10c yellow-warning | |
| 亮点提示 | 组件 10b green-tip / 10d green-info | |
| `![](图片)` | 组件 12a image | 原图代码保留 |
| 视频 | 组件 12b video-card | 原视频代码保留 |
| 文末 | 组件 13a footer-cta（+ 13b brand-card） | 签名段落放 footer-cta 前 |
