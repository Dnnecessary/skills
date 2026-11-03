# 公众号排版组件库 —— 摸鱼绿纸感

> **使用说明**：本组件库为「摸鱼绿纸感」主题。**组件主体全部直接调用「摸鱼票据风」**——组件 3~15 的 HTML 与票据风**逐字节一致**（不自行改造、不自创变体），只有两处例外：① 「组件 2 票据封面」被替换成本主题唯一自有组件：**封面引言卡 quote-cover**（白卡 + 暖灰细边框 + 绿 QUOTE + 18px 大字金句 + 绿色下划线 + 右下署名）；② 组件 6b 高亮底色改为本主题专用高亮黄 `#FBEEB1`（票据风为绿底 `#A7F3D0`）。另**新增一件**票据风没有的组件：组件 11 变体 B「浅边金句卡」（边框与封面引言卡同款暖灰细边，正文引语专用）。所有组件使用**内联样式**，可直接粘贴到微信公众号编辑器。
>
> **设计风格**：纸感白卡 + 票据骨架。页面底是纸感的米黄 `#FFFEF8`，票据风里的米黄卡片底 `#fffef8` 反转为纯白 `#FFFFFF`——白卡浮在纸面上；票据特征（撕票虚线 ✂、绿色实心编号块、2px 黑横线、编号角标、组件 11 的 2px 黑描边 + 硬阴影）沿用原样。**封面 2 与浅边金句卡 11-B 统一 `1px dashed #DCD6C6` 暖灰虚线边 + 圆角 8px、无阴影**，像两张撕下来的便签纸；**结尾互动区 13 直接调用「摸鱼绿」13a 的圆角浅灰卡**（`border-radius:8px` + `#F9FAFB` 底 + 柔和投影）；**话题标签 12 为小圆角（6px）** `border-radius:6px`。整篇圆角件就此四类：封面卡、金句卡、标签、结尾卡，其余（章节标题、结论卡、编号列表、图片框）仍是直角。
>
> **与「摸鱼票据风」的关系（2026-11-03 用户指定）**：**只保留封面引言卡，其余组件全部调用票据风**。本主题 = 票据风组件集（3 章节标题 / 4 小节标题 / 5 正文 / 6 强调 / 7 Case / 8 图片 / 9 结论卡 / 10 编号列表 / 11 核心观点卡 / 12 标签组 / 13 footer-cta / 14 结束符 / 15 隐藏标记）+ 组件 2 封面引言卡 + 组件 11 变体 B 浅边金句卡。**偏离仅六处**：① 组件 2 换成引言卡；② 页面底 `#FFFEF8` / 卡片底 `#FFFFFF`（票据风相反：页面白、卡片米黄）；③ 字体栈 CJK 优先（SKILL 9d）；④ 组件 6b 高亮底色改 `#FBEEB1` 黄（票据风为绿 `#A7F3D0`）；⑤ 新增组件 11 变体 B 浅边金句卡（边框与封面引言卡一致 `1px dashed #DCD6C6` + 圆角 8px、无硬阴影，票据风无此件）；⑥ 组件 13 结尾互动区直接换用「摸鱼绿」13a 圆角浅灰卡（`#F9FAFB` + `1px #E5E7EB` + 圆角 8px + 柔和投影），不再用票据风的方角黑描边 + 撕票虚线。
>
> **已停用的纸感旧组件（不要再生成）**：三列看点卡、9a 灰色虚线引用框、9b 一句话亮点卡、9c 黄色竖条小节标题、9d 居中金句分隔、10a~10d 各类提示框、11a 石墨灰标签、11b~11g 流程/对比/时间线/工具卡/表格/编号列表、12a/12b 媒体卡、13b 品牌尾卡、7a~7c 内容标签、8a/8b 代码块。票据风没有对等组件的，一律改用票据风组件替代：小节标题→组件 4；引用段→组件 11 变体 B 浅边金句卡；金句/关键数据→组件 11 核心观点卡（引语用 11 变体 B）；清单/步骤→组件 10；话题标签→组件 12；多行代码→通用库 1a/1b。
>
> **公众号平台限制须知**：
> - ❌ 不支持 `<style>`/`<script>`、CSS class/id、`position:fixed/absolute`、`float`、`@media`/`@keyframes`、`display:grid`
> - ✅ 支持内联 `style`、`display:flex`（有限）、`box-shadow`（含硬阴影偏移）、`border-radius`、`text-shadow`、`<svg>`（结尾互动区图标，微信支持）、`<section>/<p>/<span>/<strong>/<img>` 等基础标签
>
> **WeChat 兼容铁律**（本主题组件全部已按此写好，改动时必须遵守）：
> - 所有"装饰性空元素"（撕票虚线、头像占位框）**没有真实内容时整块删掉**，不留空 section
> - 正文字号固定 `14px`、行高 `1.9`——本主题排版铁律，不与其它主题共用字号
> - 不要把 `font-size`/`border-bottom` 打在 `<strong>` 上，高亮样式统一挂在外层 `<span>` 上
> - `writing-mode:vertical-rl`（票据侧边竖排字）在个别老旧客户端可能渲染异常，如遇异常可退化为横排小字，不影响其余结构

---

## 设计变量速查表

```
页面纸感底：     #FFFEF8（本主题与票据风的唯一底色差异）
卡片底：         #FFFFFF（白卡浮在纸面上；票据风原为 #fffef8）
主色调（绿）：   #059669
浅绿背景：       #F0FDF4
绿色虚线/撕票线：#A7F3D0
重点高亮黄底：   #FBEEB1（本主题专用，组件 6b；票据风原为绿底 #A7F3D0）
黑色描边/硬阴影：#1a1a1a
正文色：         #555
标题色：         #1a1a1a
次要文字：       #888 / #999
细边框：         #eee
代码背景：       #F3F4F6
案例标签底：     #E5E7EB + 字 #6B7280（组件 7 = 摸鱼绿 7b case-label 原样）
代码字色：       #1F2937
引言卡边框：     #EAE7DE（组件 2 / 11 变体 B 共用的暖灰**虚线**边，均 `dashed` + `border-radius:8px`）
结尾卡（13a）：  #F9FAFB 底 + #E5E7EB 边 + 圆角 8px + 柔和投影（摸鱼绿原版）
引言卡署名：     #A9A49A（组件 2 专用）
正文字号：       14px（本主题铁律，不可改）
正文行高：       1.9
全局行高：       1.75
字间距：         0.5px
最大宽度：       677px
内容区边距：     0 20px（正文区块左右各 20px）
章节间距：       margin-bottom: 32px
```

字体栈：`'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif`（CJK 优先，保证中文引号渲染为全角占格，SKILL 9d）

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;background:#FFFEF8;font-family:'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif;color:#555;line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">

  <!-- 所有组件放在这里 -->

</section>
```

---

## 组件 2 封面引言卡 quote-cover（本主题唯一的纸感组件）

> **定位**：这是本主题**唯一保留的纸感自有组件**，放在全文最开头充当封面（替代票据风的票据封面 ticket-cover）。其余组件全部来自票据风。
>
> **形态（2026-11-03 用户指定）**：四周 **1px 暖灰虚线**边框 `1px dashed #DCD6C6` + **圆角 8px**，纯白卡底 `#FFFFFF` 浮在米黄纸面上，像一张撕下来的便签纸；QUOTE 标签用主绿 `#059669` 点睛，金句关键词用绿色下划线 `#A7F3D0`；无阴影、无色块，靠虚线边框与留白出质感。`margin-top:32px` 与页面顶部拉开距离，不贴头。
>
> **⚠️ 虚线是设计本体**：`component_lint.py` 会对「四周虚线框」报一条 WARN，这对本主题是**预期告警**，不要为了消警告把封面/金句卡改回实线。
>
> **文案策略（先读，比代码重要）**：
> - 引言卡金句与公众号外标题是**两层**，视角错开——外标题卖"为什么点开"，引言卡卖"核心观点是什么"
> - 金句**只能来自原文或用户给定**（文章第一段、核心论点、范文首句等），**禁止由排版方自创判断句**
> - 右下署名按文章实际作者填；未知则**整行删掉**，不留空行

```html
<section style="margin:32px 20px 36px;padding:30px 24px 24px;border:1px dashed #DCD6C6;border-radius:8px;background:#FFFFFF;">
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

> **关键词下划线**：固定主题绿 `#A7F3D0`（同组件 6c），金句内最多标 1~2 处。
> **字数控制**：金句 ≤60 字为佳（18px 下约 3 行），过长会削弱"大字"的冲击力。
> **无合适金句时**：整块删掉，直接从组件 3 章节标题开始，不要硬凑一句。

---

## 组件 3 章节标题 chapter-title

**用途**：大章节分隔，编号 01/02/03…

**可替换字段**：`{{编号}}` `{{标题}}` `{{副标题}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="display:flex;align-items:center;gap:12px;margin-bottom:24px;padding-bottom:12px;border-bottom:2px solid #1a1a1a;">
    <section style="background:#059669;color:#fff;font-size:12px;font-weight:800;padding:6px 12px;letter-spacing:2px;"><span leaf="">{{编号}}</span></section>
    <section style="font-size:18px;font-weight:800;color:#1a1a1a;letter-spacing:1px;"><span leaf="">{{标题}}</span></section>
    <section style="font-size:12px;color:#888;"><span leaf="">/ {{副标题}}</span></section>
  </section>

  <!-- 本章节正文内容放在这里 -->

</section>
```

---

## 组件 4 小节标题 subtitle

**用途**：章节内的二级标题。

**可替换字段**：`{{小节标题}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:16px;">
    <section style="width:4px;height:16px;background:#059669;"><span leaf=""><br></span></section>
    <section style="font-size:15px;font-weight:700;color:#1a1a1a;"><span leaf="">{{小节标题}}</span></section>
  </section>
</section>
```

---

## 组件 5 正文段落 paragraph

**用途**：普通正文，可内嵌组件 6 文字强调。字号行高是本主题铁律，不要跟随其它主题改动。

**首行缩进（2026-11-03 用户指定）**：每个正文段落首行缩进 **2 个汉字宽**，用 `text-indent:2em` 实现，**不加全角空格**（避免空格混进正文、被编辑器吞掉或复制时带出）。

**缩进适用范围**：仅组件 5 正文段落。**不缩进**——章节标题 3、小节标题 4、封面卡 2、金句卡 11-B、结论卡 9、编号列表 10、核心观点卡 11、标签 12、图片说明、结尾互动区 13、代码块、署名。这些要么居中、要么本身就是卡片/列表结构，缩进会破坏对齐。

**可替换字段**：`{{正文内容}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <p style="font-size:14px;color:#555;line-height:1.9;margin-bottom:16px;text-align:justify;text-indent:2em;">
    <span leaf="">{{正文内容}}</span>
  </p>
</section>
```

---

## 组件 6 文字强调（5 种子样式）

**用途**：在正文段落内使用，按需选择一种，一段文字不要叠加超过 2 种。

### 6a. 绿色加粗 —— 产品名/工具名

```html
<span style="color:#059669;font-weight:700;"><span leaf="">{{文字}}</span></span>
```

### 6b. 黄色高亮 —— 核心观点/关键数据

> **本主题唯一色偏**：底色调成本主题专用高亮黄 `#FBEEB1`（票据风原为绿底 `#A7F3D0`）；文字仍用 `#111`，绿下划线 6c 保持不变。

```html
<span style="background:#FBEEB1;padding:0 4px;font-weight:600;color:#111;"><span leaf="">{{文字}}</span></span>
```

### 6c. 绿色下划线 —— 重要短语（正文关键词的默认标记）

```html
<span style="border-bottom:2px solid #A7F3D0;font-weight:600;"><span leaf="">{{文字}}</span></span>
```

### 6d. 代码标签 —— 技术名词/模型名/命令

```html
<span style="background:#F3F4F6;color:#1F2937;padding:2px 6px;border-radius:4px;font-size:13px;font-weight:600;"><span leaf="">{{文字}}</span></span>
```

### 6e. 品牌紫色 —— Claude / Obsidian / Gemini 等 AI 品牌名专用

```html
<span style="color:#7C3AED;font-weight:700;"><span leaf="">{{文字}}</span></span>
```

**使用原则**：产品/工具名用 6a；核心观点/关键数据用 6b；重要短语（次要强调，逐段标记默认用它）用 6c；技术名词/模型名用 6d；AI 品牌名专用 6e，不要把 6a 和 6e 混用在同一个词上。

---

## 组件 7 Case 标题 case-title（2026-11-03 起直接调用「摸鱼绿」7b case-label）

**用途**：案例/示例展示前的小标题，紧跟其后的内容是该案例的具体展开。

**形态**：**直接调用「摸鱼绿」主题的 7b case-label**——浅灰胶囊 `#E5E7EB` 底 + 圆角 12px + `#6B7280` 灰字（10px / 700 / 大写 `CASE 01`），右侧 <h4> 粗体案例名（15px / 800 / `#111827`），两者 `gap:8px` 基线居中。不再用此前那版「绿色标签 / 纯文字 case01:」的自造写法。

**仅有的适配（一处）**：外层 `<section>` 由 7b 的 `margin-bottom:28px` 改为本主题统一的 `margin-bottom:32px;padding:0 20px`，与全篇其它区块的边距对齐。除此之外与摸鱼绿 7b 逐字节一致。

**可替换字段**：`{{case编号}}`（两位数字，如 `01`）`{{案例名称}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:#E5E7EB;color:#6B7280;font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;"><span leaf="">CASE {{case编号}}</span></span>
    <h4 style="font-size:15px;font-weight:800;color:#111827;margin:0;">
      <span leaf="">{{案例名称}}</span>
    </h4>
  </section>
</section>
```

**排版约束**：
- 标签只装英文编号（`CASE 01`，大写、两位数字），**不要把「case01: 案例名」整串塞进标签、也不要用冒号拼成一行纯文字**——那样标签退化成普通加粗段落，层级就丢了。
- 灰底 + 灰字，**不要改绿**：绿色已属于章节标题编号块，案例标签保持中性灰，才不跟章节层级抢。
- 整行左侧对齐、**不做首行缩进**（缩进只属于正文段落 5）。

---

## 组件 8 图片容器 image-ticket

**用途**：包裹图片，票据纸感边框（米黄底 + 细灰边）。**规则**：`<img>` 标签及其 `src`/`data-src` 原封不动复制，只套外层容器。

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="background:#FFFFFF;border:1px solid #eee;padding:6px;margin-bottom:0;">
    <figure style="margin:0;">
      <span leaf=""><img src="{{图片URL}}" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
    </figure>
  </section>
</section>
```

---

## 组件 9 结论卡片 conclusion-card

**用途**：章节小结、观点总结。

**可替换字段**：`{{前缀}}` `{{结论内容}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="background:#F0FDF4;border-left:4px solid #059669;padding:14px 16px;margin-bottom:0;">
    <p style="font-size:14px;color:#1a1a1a;font-weight:600;line-height:1.7;margin:0;">
      <span leaf="">{{前缀}}</span>
      <span style="color:#059669;"><span leaf="">{{结论内容}}</span></span>
    </p>
  </section>
</section>
```

---

## 组件 10 编号特点列表 numbered-feature-list

**用途**：特点、步骤、清单，每项独立一个卡片，可重复 N 次。

**可替换字段**：`{{序号}}` `{{小标题}}` `{{描述}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="background:#FFFFFF;border:1px solid #eee;margin-bottom:12px;">
    <section style="display:flex;align-items:stretch;">
      <section style="width:36px;background:#059669;display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:800;"><span leaf="">{{序号}}</span></section>
      <section style="flex:1;padding:12px 16px;font-size:13px;color:#555;line-height:1.7;border-left:1px dashed #A7F3D0;">
        <span style="font-weight:600;color:#1a1a1a;"><span leaf="">{{小标题}}</span></span>
        <span leaf="">：{{描述}}</span>
      </section>
    </section>
  </section>
</section>
```

（本组件的 `border-left:1px dashed` 是撕票分隔线，属本主题风格特征，可直接使用，不受"正文强调不用虚线框"规则约束。）

---

## 组件 11 核心观点卡片 key-point-card

**用途**：全文核心金句、关键数据，适合章节高潮或中段强调。硬阴影描边是本主题最强锚点（结尾互动区已换成摸鱼绿圆角卡，不再呼应它）。**引语/名句不要用它，用下面的变体 B。**

**可替换字段**：`{{金句前半}}` `{{大数字}}`（可选）`{{金句后半}}` `{{补充说明}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="background:#FFFFFF;border:2px solid #1a1a1a;box-shadow:3px 3px 0 #1a1a1a;padding:20px;margin-bottom:0;">
    <p style="font-size:15px;color:#1a1a1a;font-weight:700;line-height:1.8;margin:0 0 12px;text-align:center;">
      <span leaf="">{{金句前半}}</span>
      <span style="color:#059669;font-size:24px;"><span leaf="">{{大数字}}</span></span>
      <span leaf="">{{金句后半}}</span>
    </p>
    <p style="font-size:14px;color:#555;line-height:1.8;margin:0;text-align:justify;">
      <span leaf="">{{补充说明}}</span>
    </p>
  </section>
</section>
```

无大数字时去掉中间那个 `font-size:24px` 的 `<span>`，整句金句合并放第一行 `<p>` 即可。

---

## 组件 11 变体 B｜浅边金句卡 quote-card（金句直通 / 文中引语专用）

**用途**：正文中引用名句、诗句、他人原话（「金句直通」板块、案例里的引语）。**边框与组件 2 封面引言卡完全一致**——`1px dashed #DCD6C6` 暖灰**虚线**边 + 圆角 8px + 纯白底、**无硬阴影**（2026-11-03 用户指定改虚线 + 圆角），让引语安静地贴在纸面上，不与票据风的硬阴影卡片抢戏。

**与组件 11 的分工**：组件 11（2px 黑描边 + 硬阴影）只用于全文级"核心观点/关键数据"，全文 ≤2 处；**凡是引语、名句、诗句一律用 11b**，11b 不占硬阴影额度，可多处使用。

**可替换字段**：`{{金句}}` `{{作者}}` `{{作品}}`

**排版（2026-11-03 用户指定）**：金句**靠左**、不居中；出处（作者 + 作品名）**另起一行、靠右**，字号 12px、暖灰 `#888`，写成 `—— {{作者}}《{{作品}}》`。

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="background:#FFFFFF;border:1px dashed #DCD6C6;border-radius:8px;padding:24px 20px;margin-bottom:0;">
    <p style="font-size:15px;color:#1a1a1a;font-weight:700;line-height:1.8;margin:0 0 12px;text-align:left;">
      <span leaf="">{{金句}}</span>
    </p>
    <p style="font-size:12px;color:#888;line-height:1.8;margin:0;text-align:right;">
      <span leaf="">—— {{作者}}《{{作品}}》</span>
    </p>
  </section>
</section>
```

不加阴影、不加左侧竖条、不加引号图标——质感靠虚线边框与留白。圆角 8px 与封面卡同一档。**版式固定为「左对齐金句 + 右对齐署名」**，不要居中、不要把署名接在金句后面同一行；无作者或无作品时，能查到多少写多少（如只写 `—— 曹植`），两者都未知则整行删掉。

---

## 组件 12 标签组 tag-group

**用途**：#话题标签，可多个并排；也用于正文末尾单独展示话题标签。

**可替换字段**：`{{#标签}}`

```html
<section style="margin-bottom:32px;padding:0 20px;">
  <section style="display:flex;gap:8px;flex-wrap:wrap;">
    <section style="font-size:10px;color:#059669;border:1px solid #059669;border-radius:6px;padding:4px 12px;"><span leaf="">{{#标签1}}</span></section>
    <section style="font-size:10px;color:#059669;border:1px solid #059669;border-radius:6px;padding:4px 12px;"><span leaf="">{{#标签2}}</span></section>
    <section style="font-size:10px;color:#059669;border:1px solid #059669;border-radius:6px;padding:4px 12px;"><span leaf="">{{#标签3}}</span></section>
  </section>
</section>
```

---

## 组件 13 结尾互动区 footer-cta（2026-11-03 起直接调用「摸鱼绿」13a）

**用途**：文章结尾互动三连区（点赞·在看·转发）。**用户指定：直接使用「摸鱼绿」主题的 13a footer-cta**，不再用票据风的方角黑描边 + 撕票虚线版本，也不再是本主题此前那版浅边方角卡。

**形态**：圆角 8px 浅灰卡 `#F9FAFB` + `1px #E5E7EB` 细边 + 极淡柔和投影 `0 4px 12px rgba(0,0,0,0.03)`；三个图标块 40×40、圆角 12px；第三个「转发」用绿色强调（`#ECFDF5` 底 + `#A7F3D0` 边 + 绿图标）；底部 `THANKS FOR READING` 纯字、**无撕票虚线 ✂**。

**仅有的适配（两处）**：① 外层加 `padding:0 20px 32px`，与全篇其它区块的 20px 左右内边距对齐；② 卡片 `margin` 置 0（原 13a 的 `0 0 24px` 由外层 padding 承担）。除此之外与摸鱼绿 13a 逐字节一致。

**签名文案适配**：SKILL.md 的作者签名（"我是 {{作者名}}…"两段，默认占位、由用户替换）以正文段落（组件 5）形式放在本组件**之前**；本组件内部文案保持 13a 固定句，不要重复堆叠两句"三连"。

**可替换字段**：`{{互动文案}}`（默认固定句「既然看到这里了，如果觉得有用，随手点个赞、在看、转发三连吧。」）

```html
<section style="padding:0 20px 32px;">
  <section style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:8px;padding:32px 20px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.03);margin:0;">
    <p style="font-size:13px;font-weight:bold;color:#111827;margin:0 0 20px;line-height:1.6;">
      <span leaf="">{{互动文案}}</span>
    </p>
    <section style="display:flex;justify-content:center;gap:24px;margin-bottom:16px;">
      <section style="text-align:center;color:#4B5563;">
        <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid #F3F4F6;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
        </section>
        <span style="font-size:10px;font-weight:600;"><span leaf="">点赞</span></span>
      </section>
      <section style="text-align:center;color:#4B5563;">
        <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid #F3F4F6;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path></svg>
        </section>
        <span style="font-size:10px;font-weight:600;"><span leaf="">在看</span></span>
      </section>
      <section style="text-align:center;color:#059669;">
        <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#ECFDF5;border-radius:8px;box-shadow:0 2px 4px rgba(5,150,105,0.15);border:1px solid #A7F3D0;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18v-4a8 8 0 0 1 8-8h8"></path><polyline points="16 2 20 6 16 10"></polyline></svg>
        </section>
        <span style="font-size:10px;font-weight:600;"><span leaf="">转发</span></span>
      </section>
    </section>
    <p style="font-size:10px;color:#9CA3AF;letter-spacing:1px;margin:0;">
      <span leaf="">THANKS FOR READING</span>
    </p>
  </section>
</section>
```

---

## 组件 14 结束符 end-mark

**用途**：文章最末尾收尾，放在外层容器（组件 1）内最后，footer-cta 之后。

```html
<p style="text-align:center;color:#D1D5DB;font-size:14px;margin:24px 0 0 0;">
  <span leaf="">/</span>
</p>
```

---

## 组件 15 隐藏标记 hidden-mark

**用途**：微信编辑器兼容标记，放在外层容器（组件 1）**之外**，是整篇产物的最后一个元素。

```html
<p style="display:none;">
  <mp-style-type data-value="3"></mp-style-type>
</p>
```

---

## 多行代码块 → 用通用增量库

本主题不设专属多行代码块组件；Markdown 的三反引号围栏代码块直接用 `common-components.md` 的 1a 深色代码块（默认）或 1b 浅色代码块，左竖条/强调色换成本主题主色 `#059669`；行内代码用本主题组件 6d。

---

## 完整文章模板骨架

```html
<section style="max-width:677px;margin:0 auto;background:#FFFEF8;font-family:'Source Han Sans SC','思源黑体','PingFang SC','Hiragino Sans GB','Microsoft YaHei',-apple-system,BlinkMacSystemFont,sans-serif;color:#555;line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">

  <!-- 1. 封面引言卡（组件2 quote-cover，本主题唯一的纸感组件） -->

  <!-- 2. 第一章（组件3 chapter-title） -->
  <!--    章内：组件5 正文 + 组件6 行内强调 + 组件7 Case标题 + 组件8 图片 + 组件9 结论卡片 + 组件4 小节标题 + 组件10 编号特点列表（多项） -->

  <!-- 3. 第二章…第N章（组件3，同上结构） -->

  <!-- 4. 核心观点卡片（组件11，全文收束前的高潮句，放最后一章之后） -->

  <!-- 5. 标签组（组件12，可选，全文话题标签汇总） -->

  <!-- 6. 固定签名段落（组件5 正文段落，SKILL.md 固定文案，footer-cta 之前） -->

  <!-- 7. 结尾互动区（组件13 footer-cta） -->

  <!-- 8. 结束符（组件14 end-mark） -->

</section>

<!-- 9. 隐藏标记（组件15 hidden-mark，外层容器之外，全文最后一个元素） -->
```

**骨架铁律**：本主题**不设目录/导航组件**（旧的三列看点卡已停用）——票据风强调"一张凭证从头看到尾"的阅读仪式，不做分段跳读；组件 15 隐藏标记必须在组件 1 全局容器闭合**之后**，是整篇产物真正的最后一个元素。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 硬阴影卡片（核心观点卡片 11）、绿色加粗 6a | 全文金句、关键数据、产品名 | 全文 ≤5 处 |
| **标记层** | 绿色下划线 6c（默认）、黄色高亮 6b | 正文关键词强调 | 每段 1~3 处 |
| **容器层** | 结论卡片 9、编号特点列表 10、标签组 12（小圆角（6px））、虚线卡（封面 2 / 金句 11 变体 B，`1px dashed #DCD6C6` + 圆角 8px）、结尾互动区 13（摸鱼绿 13a 圆角卡） | 小结、清单、话题标签、引语、收尾 CTA | 按需 |

**克制原则**：
- 硬阴影卡片（`box-shadow` 无虚化偏移）现仅剩**组件 11 核心观点卡片**一处，全文 ≤1 处，不要为凑形式再加；封面引言卡、浅边金句卡是暖灰**虚线**边 + 圆角、无阴影；结尾互动区走摸鱼绿 13a（圆角 + 极淡柔和投影，不是硬阴影）
- 引语、名句、诗句、他人原话一律用**组件 11 变体 B 浅边金句卡**（暖灰虚线边 + 圆角 8px、无阴影），可多处使用；不要用组件 11 的硬阴影卡去包一句引语
- 黄色高亮 6b 每段不超过 1-2 处；一段内不超过 2 种强调叠加（黄只做"最想让你看见的那一句"，绿色下划线仍是默认标记）
- 品牌紫色 6e 只用于 AI 品牌专名，不用于普通强调

---

## 文章类型 → 组件组合配方

按 SKILL.md 第 3 步判定的文章类型选配方；核心组件构成本篇的排版主旋律，点缀组件按内容出现处使用，一篇文章点缀组件种类 ≤3。

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 教程/操作指南 | 编号特点列表 10（步骤化）+ Case 标题 7 + 结论卡片 9 | 图片容器 8、代码标签 6d |
| 盘点/工具清单 | 标签组 12 + 编号特点列表 10 + 核心观点卡片 11 | 图片容器 8、结论卡片 9 |
| 观点/深度分析 | 正文段落 5 + 结论卡片 9 + 核心观点卡片 11 | 小节标题 4、黄色高亮 6b |
| 访谈/人物特稿 | 正文段落 5 + Case 标题 7（人物/场景切分）+ 结论卡片 9 | 核心观点卡片 11（引语金句） |
| 数据复盘/报告 | 核心观点卡片 11（大数字）+ 编号特点列表 10 + 结论卡片 9 | 代码标签 6d（术语/指标名） |
| 生活/情感随笔 | 正文段落 5 + 核心观点卡片 11（无大数字版）+ 结论卡片 9（少量） | 小节标题 4 |
| 案例实战 | Case 标题 7 + 图片容器 8 + 结论卡片 9 + 编号特点列表 10 | 核心观点卡片 11 |

所有类型共用固定结构：封面引言卡 2 + 章节标题 3 + 固定签名段落 + 结尾互动区 13 + 结束符 14 + 隐藏标记 15。

---

## Markdown → 摸鱼绿纸感 映射规则

| Markdown 元素 | 对应组件 | 说明 |
|---|---|---|
| `# 标题` | 不使用 | 公众号文章标题在平台设置；封面引言卡的金句从中提炼 |
| 文章开头 `> 引言` | 组件 2 封面引言卡 | 18px 大字金句 + 绿色下划线关键词 + 右下署名；原文无金句则整块删掉 |
| `## 章节标题` | 组件 3 chapter-title | 编号 01/02/03… |
| `### 子标题` | 组件 4 subtitle | 左竖条小标题 |
| 普通段落 | 组件 5 paragraph | 每段主动标 1~3 处绿色下划线 6c |
| `**加粗文字**` | 组件 6a 绿色加粗 | 产品名/工具名 |
| `==高亮文字==` | 组件 6b 黄色高亮 `#FBEEB1` | 核心观点/关键数据，每段 ≤2 处 |
| `<u>下划线</u>` / `++文字++` | 组件 6c 绿色下划线 | 次要强调（默认标记） |
| AI 品牌名（Claude/Obsidian/Gemini 等） | 组件 6e 品牌紫色 | 不与 6a 混用 |
| 案例/示例小标题 | 组件 7 case-title（= 摸鱼绿 7b） | 浅灰胶囊 `CASE 01` + 粗体案例名 |
| 文中引语 / 名句 / 诗句 / 他人原话 | 组件 11 变体 B 浅边金句卡 | 暖灰虚线边 `1px dashed #DCD6C6` + 圆角 8px + 白底 + **左对齐金句 + 右对齐署名（作者《作品名》）**；「金句直通」板块用它 |
| `![](图片)` | 组件 8 image-ticket | `src`/`data-src` 原样保留，不改写 |
| 章节小结/观点 | 组件 9 conclusion-card | |
| 特点/步骤/清单 | 组件 10 numbered-feature-list | 每项一张卡片 |
| 核心金句/关键数据 | 组件 11 key-point-card | 硬阴影锚点层，全文慎用 |
| `> 引用段落`（非开头） | 组件 9 conclusion-card 或并入正文 | 本主题无独立引用块组件 |
| `#话题` 标签 | 组件 12 tag-group | |
| 行内 `` `code` `` / 技术名词/模型名 | 组件 6d 代码标签 | |
| ` ``` 多行代码块 ``` ` | 通用库 1a 深色（默认）/ 1b 浅色 | 左竖条换本主题主色 `#059669` |
| 文末 | 组件 13 footer-cta（+ 14 end-mark） | 固定签名段落放 footer-cta 前 |
