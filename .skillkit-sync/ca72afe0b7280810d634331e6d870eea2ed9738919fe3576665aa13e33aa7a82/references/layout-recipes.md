# 版式配方：封面与内容页的可复用骨架

这份文件是排版阶段的"菜单"。规划阶段（`content-planning.md`）已经定下每一页的角色和大致版式方向，这里给出具体的 HTML 骨架，复制到 `.poster` 里改文字即可。

所有骨架基于 `.poster` 的 flex 列结构（`base.css`）：内容区从上往下排，`.foot` 用 `margin-top: auto` 推到底部。骨架里的颜色、字号全部用 `style-presets.md` 里的 token 变量（`var(--accent)` 等），不写死颜色——这样同一份骨架换一个 `data-style` 就能切换风格。

下面三块：封面配方、内容页配方、配方与风格的匹配建议。

---

## 封面配方

### 1. 大字报顶压式

主标题占满上半部分，字号拉到 `--fs-cover-title`，关键词用 `.hl`（强调色块）或描边框标出。适合信息密度高、需要"一眼砸脸"的选题。

```html
<section class="poster">
  <span class="tag">系列标签 ✦</span>

  <h1 class="cover-title" style="font-family: var(--font-display); font-weight: 900; font-size: var(--fs-cover-title); line-height: 1.5; margin-top: 48px;">
    <span style="display:block;">第一行标题</span>
    <span style="display:block;">
      <span style="color:var(--bg); background:var(--accent); padding:6px 18px; border-radius:var(--radius);">关键词</span>
    </span>
  </h1>

  <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top: 52px; max-width: 84%;">
    一句话副述，补一个利益点或人群限定
  </p>

  <div class="foot" style="display:flex; align-items:center; gap:16px;">
    <span style="font-weight:800; font-size: var(--fs-caption);">@账号名</span>
    <span style="margin-left:auto; font-size: var(--fs-caption); color: var(--ink-soft);">往下滑 →</span>
  </div>
</section>
```

适用风格：baokuan（最贴合）、minimal（去掉色块，靠纯色对比）。

### 2. 杂志栏目式

顶部一条细分隔线 + 栏目元数据（系列名/期号），标题靠**字号反差**而非加粗，留白大。适合调性克制、不靠贴纸抓眼的内容。

```html
<section class="poster">
  <div style="display:flex; justify-content:space-between; font-size: var(--fs-caption); letter-spacing:4px; color:var(--ink-soft); text-transform:uppercase; padding-bottom:24px; border-bottom: var(--hairline) solid var(--line-color);">
    <span>专题 · 栏目名</span>
    <span style="color:var(--ink); font-weight:600;">01 / 06</span>
  </div>

  <div style="margin-top:130px;">
    <p style="font-size:26px; letter-spacing:8px; color:var(--accent);">KICKER 小标签</p>
    <h1 style="font-family: var(--font-display); font-size: var(--fs-cover-title); line-height:1.4; margin-top:16px;">
      标题正文，一到两行
    </h1>
  </div>

  <div class="foot">
    <p style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名 · 往后看</p>
  </div>
</section>
```

适用风格：magazine（专属配方）。

### 3. 金句满版式

整页只放一句话，字号顶到接近 `--fs-cover-title`，居中或左对齐，几乎没有其他元素。靠"留白 + 单一信息"形成视觉冲击。

```html
<section class="poster" style="justify-content:center;">
  <p style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); line-height:1.4;">
    一句能独立成立、戳人的话<br>
    <span style="color:var(--accent);">关键的那半句</span>
  </p>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

适用风格：minimal（最贴合，整页单色块顶满）、ambient（柔和版，字号可降到 `--fs-h1` 以内）。

### 4. 图片打底式

背景用一张真实照片/截图打底，标题落在照片中"安静区"（参见 `image-handling.md` 的文字压图安全区），底部留一条纯色信息条。

```html
<section class="poster" style="position:relative; padding:0;">
  <img src="assets/cover.jpg" alt="" style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position: center 30%;">

  <div style="position:relative; padding: var(--pad); height:100%; display:flex; flex-direction:column;">
    <h1 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-cover-title); color:#fff; text-shadow: 0 2px 12px rgba(0,0,0,.35); max-width:80%;">
      标题落在画面留白区
    </h1>

    <div class="foot" style="background: rgba(0,0,0,.35); border-radius: var(--radius); padding:20px 28px; backdrop-filter: blur(2px);">
      <span style="color:#fff; font-size: var(--fs-caption);">@账号名 · 往下滑看细节</span>
    </div>
  </div>
</section>
```

适用风格：四套均可，但 minimal 风格用此配方时注意标题色要与底图反差拉满，避免破坏"单色块"调性。

### 5. 图文展示式

封面的主角是一张**不能裁的图**（App 截图 / 产品实拍 / 界面图）——常见于产品测评、App 推广类选题。标题必须让位给图，不能像"大字报顶压式"那样占满上半屏。

```html
<section class="poster">
  <span class="tag">系列标签 ✦</span>

  <h1 style="font-family: var(--font-display); font-weight:900; font-size: 64px; line-height:1.2; margin-top:24px;">
    一到两行、够短的标题
    <span style="color:var(--bg); background:var(--accent); padding:2px 16px; border-radius:var(--radius);">关键词</span>
  </h1>

  <div style="flex:1; min-height:0; display:flex; align-items:center; justify-content:center; margin:18px 0 6px;">
    <img src="assets/hero.png" style="max-height:100%; max-width:80%; object-fit:contain; border-radius:32px; filter:drop-shadow(0 22px 44px rgba(0,0,0,.25));">
  </div>

  <p style="font-size: var(--fs-body); color: var(--ink-soft); line-height:1.5;">一句副述，给出利益点或人群限定</p>

  <div class="foot" style="display:flex; justify-content:flex-end;">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">往下滑看体验 →</span>
  </div>
</section>
```

**硬规则（和"大图+说明"共用）**：

- 图必须 `object-fit:contain`，绝不裁掉界面或主体。
- **主图至少占画布高度 55%**：标题压到 1-2 行、字号不超过约 `var(--fs-h1)`，行高收紧到 1.1-1.25，副述只留一行。
- 出图后做缩略图测试（缩到 360px 宽），确认图上的关键细节仍可辨认；如果模糊到看不清，先压标题/副述，而不是缩小图。
- 标题里如果带强调色块（`.hl`），块本身不要太大，避免和图抢视觉重心——图才是说服力来源。

适用风格：四套均可；baokuan/ambient 可用 `drop-shadow` 让图有质感，minimal/magazine 建议去掉投影，改用细线边框或纯展示。

---

## 内容页配方

### 1. 编号要点卡

3-4 条并列要点，每条一个编号圆标 + 标题 + 一行说明，卡片化呈现，密度高、信息量大。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); line-height:1.15; margin-top:24px;">
    本页主题 <span style="color:var(--accent);">关键词</span>
  </h2>

  <div style="margin-top:44px; display:flex; flex-direction:column; gap:28px;">
    <div style="display:flex; gap:28px; align-items:flex-start; border-radius: var(--radius); padding:30px 32px; border: var(--hairline) solid var(--line-color); background: var(--accent-soft);">
      <div style="flex:none; width:76px; height:76px; border-radius:50%; background:var(--accent); color:var(--bg); font-family:var(--font-display); font-weight:900; font-size:46px; display:flex; align-items:center; justify-content:center;">1</div>
      <div style="flex:1;">
        <div style="font-weight:800; font-size:40px; line-height:1.25;">要点标题</div>
        <div style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:10px;">一到两句具体说明，给出可照做的细节</div>
      </div>
    </div>
    <!-- 重复以上结构，共 3-4 条 -->
  </div>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名 · 翻页看下一组</span>
  </div>
</section>
```

最小密度：3 条要点卡 + 标题 + 底栏，整体覆盖画布约 80% 高度，满足 ≥75% 要求。

### 2. 对比双栏

左右两栏并列，分别代表"误区/真相"或"方案A/方案B"，靠对齐和颜色区分。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    本页主题
  </h2>

  <div style="display:flex; gap:32px; margin-top:56px; flex:1;">
    <div style="flex:1; border-radius: var(--radius); padding: 40px 32px; border: var(--hairline) solid var(--line-color); display:flex; flex-direction:column;">
      <div style="font-size:28px; color:var(--ink-soft); letter-spacing:4px;">大家以为</div>
      <div style="font-size: var(--fs-h1); font-weight:800; margin-top:20px;">误区描述</div>
      <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:24px;">展开说明</p>
    </div>
    <div style="flex:1; border-radius: var(--radius); padding: 40px 32px; background: var(--accent-soft); display:flex; flex-direction:column;">
      <div style="font-size:28px; color:var(--accent); letter-spacing:4px;">真相是</div>
      <div style="font-size: var(--fs-h1); font-weight:800; margin-top:20px;">真相描述</div>
      <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:24px;">展开说明</p>
    </div>
  </div>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

最小密度：双栏 `flex:1` 撑满中间高度，配合标题和底栏天然覆盖 ≥75%。

### 3. 清单勾选

一组短句要点，前面带勾选/序号图标，适合密集罗列"可以做的事"。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    清单标题
  </h2>

  <ul style="margin-top:48px; display:flex; flex-direction:column; gap:36px; list-style:none;">
    <li style="display:flex; gap:24px; align-items:flex-start;">
      <span style="flex:none; width:48px; height:48px; border-radius:50%; border: var(--hairline) solid var(--accent); color:var(--accent); display:flex; align-items:center; justify-content:center; font-weight:800;">✓</span>
      <span style="font-size: var(--fs-body); line-height:1.5;">一条具体、可执行的清单项</span>
    </li>
    <!-- 重复 5-7 条 -->
  </ul>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名 · 建议收藏</span>
  </div>
</section>
```

最小密度：5-7 条清单项 + 较大行间距，自然覆盖到画布下部。

### 4. 大图+说明

一张大图（截图/实物图）占画布主要面积，配一行标题和一行说明，靠图本身做证据。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    这一页讲的事
  </h2>

  <figure style="margin-top:32px; flex:1; min-height:0; border-radius: var(--radius); overflow:hidden; border: var(--hairline) solid var(--line-color);">
    <img src="assets/shot.jpg" alt="" style="width:100%; height:100%; object-fit:cover; object-position: center top;">
  </figure>

  <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:24px;">一句说明这张图证明了什么</p>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

**图的两种放法（按图的类型选对，别用错）：**

- **满铺裁切**（氛围照 / 实景图 / 横图）→ `object-fit:cover` 填满 figure，用 `object-position` 控裁切（见 `image-handling.md`）。上面骨架就是这类。
- **完整展示**（手机截图 / 产品竖图 / 界面图 / 任何不能裁的图）→ 必须 `object-fit:contain` 整图显示，**绝不裁掉界面或主体**；figure 去掉描边铺底，让图带自己的边，居中 + 一点柔投影即可。

**尺寸下限（硬规则）**：图是这一页的主角，**主图至少占画布高度 55%**。标题压到 1-2 行、用紧凑行高给图让位。

**反例（实测踩过）**：大标题 + 大行高占掉半屏，把主图挤成缩略图——图主导页最忌讳这个。图一旦小到看不清细节，这页的"证据"作用就废了。出图后做缩略图测试：缩到 360px 宽，主图细节还能不能看清。

### 5. 引用金句

中段使用的金句页，比封面的"金句满版式"略小，通常带一个引号符号和来源说明。

```html
<section class="poster" style="justify-content:center;">
  <div style="font-size:120px; color: var(--accent-soft); line-height:1; font-family: var(--font-display);">"</div>
  <p style="font-family: var(--font-display); font-weight:800; font-size: var(--fs-h1); line-height:1.45; margin-top:-20px;">
    引用的那句话，最好独立成立、可被截图转发
  </p>
  <p style="font-size: var(--fs-caption); color: var(--ink-soft); margin-top:32px;">—— 一句来源/补充说明</p>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

### 6. 步骤时间线

竖向时间线，每步一个节点 + 标题 + 说明，适合教程型内容。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    操作步骤
  </h2>

  <div style="margin-top:48px; display:flex; flex-direction:column; gap:0;">
    <div style="display:flex; gap:28px;">
      <div style="flex:none; display:flex; flex-direction:column; align-items:center;">
        <span style="width:56px; height:56px; border-radius:50%; background:var(--accent); color:var(--bg); display:flex; align-items:center; justify-content:center; font-weight:800; font-size:30px;">1</span>
        <span style="flex:1; width: var(--hairline); background: var(--line-color); margin:8px 0;"></span>
      </div>
      <div style="padding-bottom:36px;">
        <div style="font-weight:800; font-size:36px;">步骤标题</div>
        <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:8px;">操作说明</p>
      </div>
    </div>
    <!-- 重复每一步，最后一步不需要连接线 -->
  </div>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

最小密度：4-5 步即可自然撑满，少于 3 步建议改用"编号要点卡"。

### 7. 数据强调

把一个核心数字放大成视觉锤，配简短上下文说明，用于强化可信度/利益点。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    本页主题
  </h2>

  <div style="flex:1; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px;">
    <div style="font-family: var(--font-display); font-weight:900; font-size: 220px; color: var(--accent); line-height:1;">73%</div>
    <p style="font-size: var(--fs-body); color: var(--ink-soft); text-align:center; max-width:80%;">
      这个数字代表什么、来源是什么
    </p>
  </div>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名</span>
  </div>
</section>
```

### 8. 总结卡

回顾全篇要点，用一组小标签/关键词卡片代替逐条复述，收口并引导互动。

```html
<section class="poster">
  <h2 style="font-family: var(--font-display); font-weight:900; font-size: var(--fs-h1); margin-top:24px;">
    总结这几条
  </h2>

  <div style="margin-top:48px; display:flex; flex-wrap:wrap; gap:20px;">
    <span style="padding:16px 28px; border-radius: var(--radius); background: var(--accent-soft); font-size: var(--fs-body); font-weight:700;">关键词一</span>
    <span style="padding:16px 28px; border-radius: var(--radius); background: var(--accent-soft); font-size: var(--fs-body); font-weight:700;">关键词二</span>
    <!-- 重复 4-6 个关键词标签 -->
  </div>

  <p style="font-size: var(--fs-body); color: var(--ink-soft); margin-top:40px; line-height:1.6;">
    一句收尾的话，落到具体动作（收藏/评论），参考 operation-engine.md 的结尾写法
  </p>

  <div class="foot">
    <span style="font-size: var(--fs-caption); color: var(--ink-soft);">@账号名 · 评论区告诉我</span>
  </div>
</section>
```

---

## 配方与风格的匹配建议

| 配方 | baokuan 爆款原生 | magazine 高级杂志 | ambient 柔和氛围 | minimal 极简冲击 |
|---|---|---|---|---|
| 大字报顶压式 | ✅ 最贴合 | – | – | ✅（去色块版） |
| 杂志栏目式 | – | ✅ 专属 | – | – |
| 金句满版式 | – | – | ✅（柔和版） | ✅ 最贴合 |
| 图片打底式 | ✅ | ✅ | ✅ | ⚠️ 谨慎，注意保持单色调性 |
| 图文展示式 | ✅ | ✅ | ✅ 最贴合 | ⚠️ 去投影，改细线边框 |
| 编号要点卡 | ✅ 最贴合 | ⚠️ 去阴影/卡片感，改用细线分隔 | ✅（圆角放大、配色柔和） | – |
| 对比双栏 | ✅ | ✅ | ✅ | ⚠️ 可用但建议简化为文字对比 |
| 清单勾选 | ✅ | ✅ | ✅ | ⚠️ 勾选符号建议改为短横线 |
| 大图+说明 | ✅ | ✅ | ✅ | – |
| 引用金句 | ⚠️ 可用，建议加 `.hl` 强调 | ✅ 最贴合 | ✅ | ✅ |
| 步骤时间线 | ✅ | ⚠️ 节点改为细线序号 | ✅ | – |
| 数据强调 | ✅ | ✅ | ⚠️ 数字不宜过分夸张，保持柔和 | ✅ |
| 总结卡 | ✅ | ⚠️ 标签改为细线分隔的列表 | ✅ | ⚠️ 关键词改为纯文字罗列 |

> minimal 风格的核心是"全画面单一色块、靠字号和留白说话"，凡是带卡片背景、阴影、多色块的配方（编号要点卡、清单勾选）放进 minimal 都要先做减法——去掉背景色块和分隔线，只保留文字本身的大小对比。magazine 风格反之，凡是带强阴影/高饱和色块的配方（baokuan 的卡片样式）要替换成发丝线分隔，避免破坏纸感。
