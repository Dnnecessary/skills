# 墨青测评风：原作组件样本库（逐字节提取）

本文件是 `gzh-design-custom` 的**组件骨架单一来源**。所有骨架均于 2026-11-19 从以下六份来源逐字节提取，`<span leaf="">` 内的 `{{…}}` 为可替换参数，其余样式与结构固定。排版时从这里取骨架，不得凭"语义相似"发明装饰或改写样式。

## 提取来源

| 编号 | 文件 |
|---|---|
| M | `/private/tmp/wechat-article_ink-teal-before-full-cover.html` |
| A1 | `01_WorkBuddy 上线了 LibTV，新一代AI 视频工作台来了！.html` |
| A2 | `02_WorkBuddy上线自动化浏览器，能自己上网干活啦！.html` |
| A3 | `03_千问办公2.0实测：能和团队协作的Team Agent来了.html` |
| A4 | `04_RunningHub 把 Blender 搬进云电脑，治好了我的抽卡焦虑.html` |
| A5 | `05_Seedream 5.5 的多轮编辑，稳得有点吓人.html` |
| A6 | `08_用 WorkBuddy + Hy4 flash 做 3D 互动课件（附提示词）.html`（2026-11-19 用户提供的新文章） |

提取脚本临时件：`/tmp/ink-components/extract.py`（section 标签配对器 + block_at），原始取证输出 `/tmp/ink-components/capsules_raw.txt`。

## 组件总表（含真实频率）

| 组件 | 频率（M/A1/A2/A3/A4/A5） | 状态 | 骨架来源 |
|---|---|---|---|
| 全局容器 + 正文段落 + 行内强调 | 全篇 | 白名单 | 2.1 / 4.3 |
| 窗口式配图卡 | 5/16/22/45/11/4 | 白名单 | 2.4，本库 C1 |
| 纯图片块 | 全篇 | 白名单 | 2.5 |
| 图片说明文字 | 全篇（最高频） | 白名单 | 2.5b |
| 深色胶囊 `CASE n` | 0/2/4/7/2/2 | 白名单（带 SVG 图标） | 本库 C2 |
| 深色胶囊 `BONUS` | 1/0/0/0/0/0 | 正式白名单 · 条件启用 | 本库 C2（同构） |
| 深色胶囊 裸 `01/02/03` | M 有 | 白名单（同级章节） | 本库 C2（同构） |
| 纯文字胶囊 `POINT n` | 0/0/0/3/0/0 | 白名单（**无 SVG**，独立骨架） | 本库 C3 |
| `PART nn` 分段条 | 0/0/0/3/0/0 | 白名单 · 条件自动路由（多部分文章） | 本库 C4 |
| `STEP n/m` 进度头 | 0/0/0/0/4/0 | 白名单（线性流程，非深色胶囊） | 2.2A / 本库 C5 |
| `HEADS UP` 提示块 | 1/0/0/0/0/0 | 白名单 · 条件启用（原文有风险/限制/避坑信息时） | 2.6 / 母版参考页骨架 |
| 三方块分隔符 | 2/2/0/2/1/0 | 白名单（话题转折，全文 ≤2） | 2.9 / 本库 C6 |
| 结尾符 `/// END` | 1/1/0/1/1/1 | 白名单 | 2.7 / 本库 C7 |
| 圈注词 | M/A3 | 白名单（全文 ≤3） | 2.8 |
| GALLERY 横向图集（C8） | A6 9 处 | 白名单（2.10；原「横向镜头轨/图集」的固定化） | 本库 C8 |
| 内容标题横向轨（C9） | A6 2 处 | 白名单（2.11；C8 变体，标题为内容槽位） | 本库 C9 |
| PROMPT 上下滑动块（C10） | A6 1 处 | 白名单（2.12；Prompt 回落的唯一例外） | 本库 C10 |
| STILL/GIF 成对媒体标签（C11） | A6 1 组 | 白名单（2.13；补齐真实骨架） | 本库 C11 |
| REC 录屏/过程录制状态标签 | M 1 处示例 | 正式白名单 · 条件启用；按实际录屏素材标注 | 2.13a / 本库 C14 |
| tab 式窗口卡头（C12） | A6 多处 | 白名单（2.14；C1 变体） | 本库 C12 |
| 真题呈现块（C13） | 用户 2026-11-20 指定创建 | 白名单（2.15；C10 变体） | 本库 C13 |
| 封面场景 SMIL / 词内动画 / 固定 IP | 全篇 | 白名单（本主题核心；仅场景内容可按语义现场绘制，其他部分原样调用组件） | 第三章 + assets |

> 频率揭示的取证修正：`三方块` 跨 4 篇出现（非仅母版）；`HEADS UP`/`BONUS` 在母版 M 各 1 处（此前证据册误记为"无实证"）；`MORE` 仅 A5 1 处；`POINT` 仅 A3、`STEP` 仅 A4。用户确认完整母版中的正式排版组件均纳入技能；低频只影响触发条件，不构成排除理由。

---

## C1 窗口式配图卡（5 篇 78 处，最高频配图组件）

真实骨架（取自 M，A1/A3 仅颜色写法不同：`rgb()` vs `#hex`，首圆点主题色可能为 `#047857`）：

```html
<section style="padding: 0px 12px;"><section style="margin: 16px 0px 22px;"><section style="border: 1px solid #E5E7EB;border-radius: 8px;overflow: hidden;"><section style="display: flex;align-items: center;padding: 8px 10px;background: #F3F4F6;border-bottom: 1px solid #E5E7EB;"><section style="line-height: 0;flex-shrink: 0;"><span style="display: inline-block;width: 8px;height: 8px;border-radius: 50%;background: #111827;margin-right: 5px;line-height: 0;font-size: 0px;"><span leaf=""><br  /></span></span><span style="display: inline-block;width: 8px;height: 8px;border-radius: 50%;background: #D1D5DB;margin-right: 5px;line-height: 0;font-size: 0px;"><span leaf=""><br  /></span></span><span style="display: inline-block;width: 8px;height: 8px;border-radius: 50%;background: #D1D5DB;margin-right: 5px;line-height: 0;font-size: 0px;"><span leaf=""><br  /></span></span></section><section style="flex: 1 1 0%;min-width: 0px;margin-left: 8px;background: #FFFFFF;border-radius: 4px;padding: 3px 8px;"><p style="margin: 0px;font-family: Menlo, &quot;SF Mono&quot;, Consolas, &quot;Courier New&quot;, monospace;font-size: 10px;color: #9CA3AF;line-height: 1.3;"><span leaf="">{{窗口文件名/图注}}</span></p></section></section><section style="line-height: 0;"><span leaf=""><img data-src="{{图片URL}}" style="display: block;width: 100%;height: auto;margin: 0px;padding: 0px;"  /></span></section></section></section></section>
```

**触发**：真实产品 UI / 过程截图 / 结果截图。文件名来自材料，不伪造。

---

## C2 深色图标胶囊：CASE / BONUS / 裸编号（CASE 17 处 + BONUS 1 + 编号若干）

**这是"图标居中"争议的正确骨架**。真实结构分三层：

1. 外层 `display:flex;align-items:flex-start`（胶囊相对标题**顶部对齐**）
2. 胶囊外包裹 `flex-shrink:0;margin-top:2px;line-height:0`（标题侧轻微 2px 下沉）
3. 胶囊自身 `display:flex;align-items:center;background:#111827;padding:3px 9px 3px 8px;border-radius:12px`（**图标在胶囊内部垂直居中**）

```html
<section style="padding: 0px 12px;"><section style="margin: 30px 0px 12px;"><section style="display: flex;align-items: flex-start;"><section style="flex-shrink: 0;margin-top: 2px;line-height: 0;"><section style="display: flex;align-items: center;background: #111827;padding: 3px 9px 3px 8px;border-radius: 12px;">{{14×14 SVG 图标}}<p style="margin: 0px 0px 0px 5px;font-family: -apple-system, BlinkMacSystemFont, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, sans-serif;font-size: 10px;font-weight: 700;line-height: 1;white-space: nowrap;color: #FFFFFF;letter-spacing: 0.5px;"><span leaf="">{{CASE 01 / BONUS / 01}}</span></p></section></section><p style="margin: 0px 0px 0px 9px;font-size: 15px;font-weight: 800;color: #111827;line-height: 1.6;letter-spacing: 0.5px;flex: 1 1 0%;min-width: 0px;"><span leaf="">{{标题}}</span></p></section></section></section>
```

`{{14×14 SVG 图标}}` 必须逐字节取自 A1–A5 原作（每个情境配一个语义图标，如 CASE 01 群消息=聊天气泡、CASE 02 表格、跨群选品=指南针等），不得自绘或改 SMIL 属性大小写。图标随胶囊标签语义匹配。

**图标差异化门禁（用户确认，2026-11-25）**：同一篇文章的多个深色图标胶囊不能全部复用同一个 14×14 动画。排版时先按标题/内容的语义从作者原作图标集中选择：群聊/沟通用聊天图标，表格/对账用表格图标，文档/写作用文档图标，方向/对齐用指南针或连接图标，生成/变化用星光或变形图标，确认/完成用勾选或状态图标。只有语义相同的重复单元才允许重复同一图标；找不到同构语义时宁可使用已验证的裸编号/纯文字胶囊，也不能用一个通用图标填满全文。交付前必须统计每个胶囊实际使用的图标签名，禁止“8 个标题 = 1 个图标复制 8 次”。

**四类互斥调用**：
- `CASE 01/02/03`：复刻作者的“同一产品/工具测试序列”结构。前文已交代测试对象或目标；每个 CASE 是一项能独立说明的实测任务，后接过程、真实媒体或结果。A1–A6 都如此使用。它不是线性步骤、能力总览或补充亮点。
- `BONUS`：母版中"正文主体讲完 → 补充彩蛋"的追加块（母版原文 "BONUS 顺手又做了两个计算机课的实验台"）。仅当原文确有补充彩蛋结构时用。
- 裸 `01/02/03`：同级章节编号，不加英文语义。
- `STEP n/m` 不在此组件，见 C5。

---

## C3 纯文字胶囊 POINT n（A3 3 处，无 SVG 图标）

**关键取证**：POINT 与 CASE 是两种不同组件。POINT 是纯文字 Menlo 胶囊，**没有 SVG 图标**，且外层用 `align-items:center`（不是 flex-start），整体是"胶囊 + 标题 + 正文"的紧凑块。

真实骨架（取自 A3）：

```html
<section style="padding: 0px 12px;"><section style="margin-bottom: 24px;"><section style="display: flex;align-items: center;gap: 8px;margin-bottom: 10px;"><span style="display: inline-block;background: rgb(17, 24, 39);color: rgb(255, 255, 255);font-family: Menlo, Consolas, &quot;Courier New&quot;, monospace;font-size: 10px;font-weight: 700;padding: 2px 8px;border-radius: 12px;letter-spacing: 1px;flex-shrink: 0;"><span leaf="">POINT 0{{n}}</span></span><p style="margin: 0px;font-size: 15px;font-weight: 800;color: rgb(17, 24, 39);line-height: 1.6;"><span leaf="">{{要点标题}}</span></p></section><p style="margin: 0px;font-size: 14px;color: rgb(75, 85, 99);line-height: 1.9;text-align: justify;"><span leaf="">{{要点正文}}</span></p></section></section>
```

**原作调用**：A3 在产品总览后先写“印象最深的有 3 点”，再用三个“能力标题 + 短解释”概括能力，之后才进入具体项目实测。

**触发**：与该“产品能力总览”同构的并列观点/能力/材料切口；**不表示先后顺序**，也不替代 CASE、PART 或 STEP。不得给 POINT 补 SVG 图标——那是我此前的错误，原作 POINT 无图标。

---

## C4 PART nn 分段条（A3 3 处）

多部分文章分段条：描边胶囊，黑底白字 `PART` + 白底黑字编号，后接章节标题。真实骨架（取自 A3）：

```html
<section style="padding: 0px 12px;"><section style="margin: 30px 0px 12px;"><section style="line-height: 0;margin-bottom: 6px;"><section style="display: inline-flex;"><section style="display: flex;border: 1px solid rgb(17, 24, 39);border-radius: 4px;overflow: hidden;"><p style="margin: 0px;font-family: -apple-system, BlinkMacSystemFont, &quot;PingFang SC&quot;, &quot;Hiragino Sans GB&quot;, &quot;Microsoft YaHei&quot;, sans-serif;font-size: 10px;font-weight: 700;line-height: 1;white-space: nowrap;background: rgb(17, 24, 39);color: rgb(255, 255, 255);padding: 4px 6px;letter-spacing: 0px;"><span leaf="">PART</span></p><p style="margin: 0px;font-family: Menlo, &quot;SF Mono&quot;, Consolas, &quot;Courier New&quot;, monospace;font-size: 10px;font-weight: 700;line-height: 1;white-space: nowrap;color: rgb(17, 24, 39);padding: 4px 7px;letter-spacing: 0px;"><span leaf="">0{{n}}</span></p></section></section></section><p style="margin: 0px;font-size: 15px;font-weight: 800;color: rgb(17, 24, 39);line-height: 1.6;letter-spacing: 0.5px;"><span leaf="">{{章节标题}}</span></p></section></section>
```

**状态**：白名单 · 条件自动路由（2026-11-25 用户确认）。**原作调用**：A3 先设定同一个“闭门会筹备”项目，之后用 `PART 01`、`PART 02`、`PART 03` 将项目叙事从多人筹备推进到工作台与工具，再进入全篇回收；每段均承接连续 CASE、正文或媒体，而不是一个短小标题。**路由最低条件**：当前文章也能确认存在围绕同一主项目的多个叙事大段，每段有独立主题和连续内容时才使用。编号按出现顺序从 `01` 开始。这里的“多个”是识别防线，不是作者明文数量规范。**排除**：普通二级标题、单段转折、单一对象介绍、仅为了拉开视觉间距的短标题，均回落为已有标题/正文结构。

---

## C5 STEP n/m 进度头（A4 4 处，非深色胶囊）

**关键取证**：STEP 与深色胶囊完全不同——它是 `align-items:baseline` + 灰色 STEP + 深色大号数字 + 灰色 `/总数` + 1px 竖线 + 标题。真实骨架（取自 A4）：

```html
<section style="padding: 0px 12px;"><section style="margin-bottom: 24px;"><section style="display: flex;align-items: center;gap: 8px;margin-bottom: 10px;"><section style="display: flex;align-items: baseline;flex-shrink: 0;"><p style="margin: 0px 4px 0px 0px;font-size: 11px;font-weight: 700;color: rgb(156, 163, 175);line-height: 1;letter-spacing: 1px;white-space: nowrap;"><span leaf="">STEP</span></p><p style="margin: 0px;font-family: &quot;Avenir Next&quot;, &quot;Helvetica Neue&quot;, Roboto, Arial, sans-serif;line-height: 1;font-size: 17px;font-weight: 800;color: rgb(17, 24, 39);"><span leaf="">{{n}}</span></p><p style="margin: 0px 0px 0px 1px;font-family: &quot;Avenir Next&quot;, &quot;Helvetica Neue&quot;, Roboto, Arial, sans-serif;line-height: 1;font-size: 10px;font-weight: 600;color: rgb(209, 213, 219);"><span leaf="">/{{m}}</span></p><section style="width: 1px;height: 12px;background: rgb(209, 213, 219);margin-left: 9px;line-height: 0;font-size: 0px;align-self: center;"><span leaf=""><br></span></section></section><p style="margin: 0px;font-size: 15px;font-weight: 800;color: rgb(17, 24, 39);line-height: 1.6;"><span leaf="">{{步骤标题}}</span></p></section><p style="margin: 0px;font-size: 14px;color: rgb(75, 85, 99);line-height: 1.9;text-align: justify;"><span leaf="">{{步骤正文}}</span></p></section></section>
```

**原作调用**：A4 围绕一条解决镜头连续性的单一方法，按“出剧本 → AI 优化提示词 → 打开云片场 → 正式生成”递进；每一步推进同一工作流，总数直接写在原文。

**触发**：当前材料也明确列出不可调换的连续教程流程且总数可从原文读取时使用。`n/m` 来自原文，不为体验叙述、案例列表或局部操作补造总数。

---

## C6 三方块分隔符（跨 4 篇 7 处）

真实骨架见 2.9 与 `component-three-squares-divider.html`。母版两处的原文语境：
1. "…做这种互动课件几乎不花钱" →【三方块】→ "上面这些做完，我们算算总账，先说结论"
2. 词内动画结尾 →【三方块】→ "这一天做下来，最大的感受是模型各有所长…"

**触发**：案例/实验/分论点讲完 → 进入总结、算总账、谈感受的话题转折。全文 ≤2 处。

---

## C7 结尾符 /// END（5 篇 5 处）

三种已取证变体：
- **标准简单版**（A1/A3/A4/A5）：斜体 `/// END` + 灰线 + 黄条(8×3) + 绿点(4×4)。仅在明确要求“标准简单版”时使用。
- **母版 SVG 笔尖版**（M）：灰线右侧接一个 240×21 的 SVG（墨黑笔尖 + 三层黄条）。仅在母版出现，不作为默认。
- **默认变体 · 动画像素三角**（A10，2026-11-25 用户确认固化）：第 10 篇同作者原文的完整真实骨架。灰线右侧接 `22×16` SVG，8 个 `4×4` 像素块排成“顶部 1 黄 / 中层绿黄绿 / 底层黄绿黄绿”；黄 `#F2CF5B`、绿 `#047857` 各 4 块。每块独立沿 Y 轴浮动（`1.6–2.4s`），整个 SVG `translateY(-8px)` 与横线对齐。

默认骨架文件：`assets/theme-assets/ink-teal-tech/component-end-pixel-triangle.html`。必须逐字节读取，不得手拼、缩放为静态 `8×8` 方块，或改为 flex 拼块版本。来源原文：`10_以为工作是为了好好生活，结果活成了_只有工作_.html`。

---


---

## A6 新文章发现的组件（2026-11-19 用户确认纳入，已进白名单 2.10–2.14）

来源 A6 是同作者同主题新文章。以下 5 件在 M/A1–A5 的 17 件白名单中**没有**，逐字节提取入库。2026-11-19 用户看过展品页后明确「纳入吧」，**五件已正式进入 `theme-ink-teal-tech.md` 2.10–2.14 正文规则与默认白名单**，按各自触发条件取用。

### C8 GALLERY 横向滑动图集（A6 9 处）

黑底矩形标签 `GALLERY` + 右侧灰字 `← 左右滑动 →` + `overflow-x:scroll` 横向滚动容器，每帧 `width:80%`，帧内为图片 + 底部页码 `n/m`。此前证据册将 A4 横向镜头轨、A5 横向图集记为「文章专用、不纳入默认组件」；A6 用固定 `GALLERY` 标签复用 9 次，已具备固定组件形态。

```html
<section style="margin:16px 0 22px;"><section style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px;"><span style="display:inline-block;background:#111827;color:#FFFFFF;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:3px 7px;line-height:1.3;"><span leaf="">GALLERY</span></span><p style="margin:0;font-size:11px;color:#9CA3AF;line-height:1;letter-spacing:0.5px;white-space:nowrap;"><span leaf="">← 左右滑动 →</span></p></section><section style="display:flex;overflow-x:scroll;-webkit-overflow-scrolling:touch;"><section style="flex-shrink:0;width:80%;margin-right:10px;"><section style="border:1px solid #E5E7EB;line-height:0;" nodeleaf=""><img src="https://mmbiz.qpic.cn/mmbiz_png/iaZPxh36UvuyfE96kH9ibxtDJLoib0kIf4iadiboyUAEicbwYjl30yUv0bZpSNKsMFZHYfSnltZLibHiaicoMmHibzibGNyf8wAoLgqNE1qicx9VqDMDIeI/640?wx_fmt=png&amp;from=appmsg" data-ratio="0.562962962962963" data-type="png" data-w="1080" style="display:block;width:100%;height:auto;margin:0;padding:0;" data-width="1280" data-height="720" data-imgfileid="100008460" data-aistatus="1"></section><section style="display:flex;align-items:baseline;gap:8px;margin-top:6px;"><p style="margin:0;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:11px;font-weight:700;color:#111827;line-height:1.4;"><span leaf="">1/2</span></p></section></section><section style="flex-shrink:0;width:80%;margin-right:10px;"><section style="border:1px solid #E5E7EB;line-height:0;" nodeleaf=""><img src="https://mmbiz.qpic.cn/sz_mmbiz_png/iaZPxh36Uvuxiah4h1l2eME0FsmF33l7lyAsT3CQ3oiaAE9YmPgXCd38nnSp2XutJaKpSdz91AH1xqeI1PgGvuZsicwnTQvPLamxrNNTv5uZdeU/640?wx_fmt=png&amp;from=appmsg" data-ratio="0.562962962962963" data-type="png" data-w="1080" style="display:block;width:100%;height:auto;margin:0;padding:0;" data-width="1920" data-height="1080" data-imgfileid="100008462" data-aistatus="1"></section><section style="display:flex;align-items:baseline;gap:8px;margin-top:6px;"><p style="margin:0;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:11px;font-weight:700;color:#111827;line-height:1.4;"><span leaf="">2/2</span></p></section></section></section></section>
```

**原作调用**：A5 将一套 PPT 的连续页紧接在“多页 PPT 生成”CASE 后；A6 则把同一课件、同一模型的连续页面或状态紧接在成品介绍后。页码表明媒体属于同一证据组。

**触发**：与此同构的同一对象连续多页画面、同一对象的多状态或前后对比，且横滑本身有阅读价值时用。禁止把无关图片做成画廊。

### C9 内容标题横向轨（GALLERY 变体，A6 2 处）

**关键：本组件的文字是内容驱动的槽位，不是固定标签文案。** 与 `GALLERY` / `PROMPT` / `CASE 01` 那种永远不变的英文标识不同，C9 的文字必须按这一组图片/视频的**真实内容**填写：

- **黑底组名 = `<该组图片的共同主题> · <段数> 段`**：原文写"天文课 · 2 段""NASA 模型 · 2 段"，是因为那两组图片确实分别是天文课和 NASA 模型。**若图片内容是语文课，就必须写"语文课 · 2 段"**，绝不能照抄"天文课"。段数 = 该组图片帧数。
- **每帧小标题 = 该帧图片内容的概括**（原文"太阳系不能按图比例""一块月岩的 40 亿年"），同样是内容槽位，**且可选**：A6 的 NASA 模型组只有序号 01/02、没有任何帧小标题。不能因为别组有小标题就硬加。
- 真正固定不变的只有骨架：`overflow-x:scroll` 横滚容器、每帧 `width:78%`、`← 左右滑动 →` 提示、`Georgia` 斜体 26px 浅灰序号 `01/02`、`border:1px solid #E5E7EB` 图片框、尾部 1px 留白帧。

下面 HTML 里的"天文课 · 2 段""太阳系不能按图比例""一块月岩的 40 亿年"都是 A6 原文的**实例值**，不是模板文案；排版新文章时全部替换为实际图片内容。

```html
<section style="margin:16px 0 22px;"><section style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:10px;"><span style="display:inline-block;background:#111827;color:#FFFFFF;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:3px 7px;line-height:1.3;"><span leaf="">天文课 · 2 段</span></span><p style="margin:0;font-size:11px;color:#9CA3AF;line-height:1;letter-spacing:0.5px;white-space:nowrap;"><span leaf="">← 左右滑动 →</span></p></section><section style="display:flex;align-items:flex-start;overflow-x:scroll;-webkit-overflow-scrolling:touch;"><section style="flex-shrink:0;width:78%;margin-right:10px;"><section style="display:flex;align-items:flex-end;margin-bottom:8px;"><p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-style:italic;font-weight:700;font-size:26px;color:#D1D5DB;line-height:1;flex-shrink:0;"><span leaf="">01</span></p><section style="margin-left:8px;min-width:0;"><p style="margin:0;font-size:13px;font-weight:800;color:#111827;line-height:1.5;"><span leaf="">太阳系不能按图比例</span></p></section></section><section style="border:1px solid #E5E7EB;line-height:0;" nodeleaf=""><img src="https://mmbiz.qpic.cn/sz_mmbiz_gif/iaZPxh36UvuxDqyBrQqzaiaXuwSsGejrN8SQ0UrOiahJAKkAhK94X7WMPibJFsQuP3E2ElFNdtaicNRFMeJAoWpsWSY6icdPFSC8ezmMZr33Yq9mU/640?wx_fmt=gif&amp;from=appmsg" data-ratio="0.5625579240037072" data-type="gif" data-w="1079" style="display:block;width:100%;height:auto;margin:0;padding:0;" data-width="1920" data-height="1080" data-imgfileid="100008502" data-aistatus="1"></section></section><section style="flex-shrink:0;width:78%;margin-right:10px;"><section style="display:flex;align-items:flex-end;margin-bottom:8px;"><p style="margin:0;font-family:Georgia,'Times New Roman',serif;font-style:italic;font-weight:700;font-size:26px;color:#D1D5DB;line-height:1;flex-shrink:0;"><span leaf="">02</span></p><section style="margin-left:8px;min-width:0;"><p style="margin:0;font-size:13px;font-weight:800;color:#111827;line-height:1.5;"><span leaf="">一块月岩的 40 亿年</span></p></section></section><section style="border:1px solid #E5E7EB;line-height:0;" nodeleaf=""><img src="https://mmbiz.qpic.cn/mmbiz_gif/iaZPxh36Uvuy5NE4rxgDZXiaawJNO1vUAI4cvt62MEQIia8icw7XZFa9UK4Dic8bb35dN7MCgE6N03bsrnAYWl1hURKibadpT9Ge3ZFaekNJ0pIug/640?wx_fmt=gif&amp;from=appmsg" data-ratio="0.5625579240037072" data-type="gif" data-w="1079" style="display:block;width:100%;height:auto;margin:0;padding:0;" data-width="1920" data-height="1080" data-imgfileid="100008505" data-aistatus="1"></section></section><section style="flex-shrink:0;width:1px;"><span leaf=""><br></span></section></section></section>
```

**原作调用**：A6 用“天文课 · 2 段”“NASA 模型 · 2 段”标记同一主题下的分段演示；每帧只在需要说明具体段落时附标题，NASA 组仅保留序号。

**触发**：多段视频/演示图片属于一个真实共同主题，且读者需要以组名与序号辨识各段时才用。黑底组名与帧小标题一律取自图片真实内容，禁止照抄原文示例文案或为无共同主题的图片硬造组名。

### C10 PROMPT 上下滑动提示词块（A6 1 处）

灰底圆角卡 `background:#F3F4F6;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden`；头部条含黑底 `PROMPT` 小标签（`border-radius:3px`）+ 13px/700 标题 + 灰字 `上下滑动 ↕`；内容区 `height:300px;overflow-y:scroll`，内含提示词正文、`border-top` 分隔的小标题、白底代码框（Menlo 11px）。

```html
<section style="background:#F3F4F6;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden;"><section style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 14px;border-bottom:1px solid #E5E7EB;"><section style="display:flex;align-items:center;gap:8px;min-width:0;"><span style="display:inline-block;background:#111827;color:#FFFFFF;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:2px 6px;border-radius:3px;line-height:1.4;"><span leaf="">PROMPT</span></span><p style="margin:0;font-size:13px;font-weight:700;color:#111827;line-height:1.4;"><span leaf="">AI 互动课件设计师</span></p></section><p style="margin:0;font-size:11px;color:#9CA3AF;line-height:1;letter-spacing:0.5px;white-space:nowrap;"><span leaf="">上下滑动 ↕</span></p></section><section style="height:300px;overflow-y:scroll;-webkit-overflow-scrolling:touch;box-sizing:border-box;padding:14px 16px 6px;"><p style="margin:0 0 8px;font-size:12px;font-weight:700;color:#111827;line-height:1.9;text-align:left;font-size:13px;"><span leaf="">角色与目标</span></p><p style="margin:0 0 8px;font-size:12px;color:#374151;line-height:1.9;text-align:left;overflow-wrap:anywhere;"><span leaf="">你同时是课程设计师、游戏设计师和前端工程师。用户会给你一次课的教学源文档，你要把它做成一套互动课件：每一页是一个 HTML 文件，最后装进一个播放器，成为一份可以左右翻页的完整课件。</span></p><p style="margin:0 0 8px;font-size:12px;color:#374151;line-height:1.9;text-align:left;overflow-wrap:anywhere;"><span leaf="">课件主要有两种用法：老师在教室里用投影或触控一体机带着全班上课；学员在电脑、平板或手机上自学。所以它要在三米外看得清、用手指点得准。</span></p></section></section>
```

**原作调用**：A6 先展示互动课件成品与模型效果，再给出可直接复用的“AI 互动课件设计师”全文；A4 在 STEP 2 提到可复用的优化提示词后，紧接完整 Skill。两处都是正文刚引用、读者可复制使用的长内容。

**规则裁定（2026-11-19 用户确认纳入）**：已写入 `theme-ink-teal-tech.md` 2.12，`PROMPT` 块成为「代码 / Prompt 回落正文」的唯一例外——仅当原文确有同样的可复制长内容结构时使用，否则仍回落 2.1；不得套窗口栏或伪证据图。

### C11 STILL / GIF 成对媒体标签（A6 1 组）

`STILL` 为**描边胶囊**（`border:1px solid #111827;color:#111827`）+ 灰字「静帧」；`GIF` 为黑底胶囊 + 灰字「实机」，两者成对出现。主题规则已提及 `REC/GIF/STILL` 标签名，但此前无完整骨架。

```html
<section style="padding: 0px 12px;"><section style="display:flex;align-items:center;margin-bottom:6px;"><span style="display:inline-block;border:1px solid #111827;color:#111827;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:2px 6px;line-height:1.3;"><span leaf="">STILL</span></span><p style="margin:0;font-family:Menlo,'SF Mono',Consolas,'Courier New',monospace;font-size:10px;color:#9CA3AF;letter-spacing:1.5px;line-height:1.4;margin-left:8px;"><span leaf="">静帧</span></p></section><section style="display:flex;align-items:center;margin-bottom:6px;"><span style="display:inline-block;background:#111827;color:#FFFFFF;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:3px 7px;line-height:1.3;"><span leaf="">GIF</span></span><p style="margin:0;font-family:Menlo,'SF Mono',Consolas,'Courier New',monospace;font-size:10px;color:#9CA3AF;letter-spacing:1.5px;line-height:1.4;margin-left:8px;"><span leaf="">实机</span></p></section></section>
```

**原作调用**：A6 在同一对象的静帧与动态实机对照之前，先用 STILL 与 GIF 明示两个验证状态。

**触发**：同一素材同时给出静态截图与动态实机，用于标注媒体验证状态。

### C14 REC 录屏 / 过程录制状态标签（母版 M 1 处展示）

母版核心展板将 `REC` 与 `STILL / GIF` 并列作为媒体状态提示。它是可单独调用的录屏/过程录制标签，不是 `STILL / GIF` 成对组件的别名，也不替代媒体本身。

真实视觉骨架为深色等宽字胶囊，调用时紧邻对应的真实录屏媒体或过程演示：

```html
<section style="padding:0px 12px;"><section style="display:flex;align-items:center;margin-bottom:6px;"><span style="display:inline-block;background:#111827;color:#FFFFFF;font-family:Menlo,Consolas,monospace;font-size:10px;font-weight:700;padding:3px 7px;border-radius:12px;letter-spacing:1px;line-height:1.3;"><span leaf="">REC</span></span><p style="margin:0px 0px 0px 8px;font-family:Menlo,Consolas,monospace;font-size:10px;color:#9CA3AF;letter-spacing:1.5px;line-height:1.4;"><span leaf="">录屏 / 过程演示</span></p></section>{{真实录屏媒体}}</section>
```

**原作调用**：A4 将 REC 紧贴“同一套资产图，先做白模预演当参考”的连续过程媒体，用它说明这不是单张截图而是可观看的预演。

**状态**：正式白名单 · 条件启用。**触发**：当前素材确为屏幕录制或过程录像，需要在媒体前标明其为连续动态过程时调用；标签说明可按素材填写，如「录屏」「过程演示」。**排除**：静态截图单独使用 `STILL`；同一对象的静帧与 GIF 对照使用 C11；不能只凭文章谈到“过程”就添加 REC，也不得用占位框代替真实媒体。

### C12 tab 式窗口卡头（C1 变体，A6 多处）

白底 tab：`border:1px solid #E5E7EB;border-bottom:0;border-radius:7px 7px 0 0`，内含 6px 青绿圆点 + 11px/700 自定义标题，贴在图片上沿。与 C1「三圆点 + 文件名栏」是不同骨架。

```html
<section style="padding: 0px 12px;"><section style="display:flex;align-items:center;border:1px solid #E5E7EB;border-bottom:0;border-radius:7px 7px 0 0;padding:5px 12px 5px 9px;background:#FFFFFF;flex-shrink:0;max-width:72%;box-sizing:border-box;"><span style="display:inline-block;width:6px;height:6px;border-radius:3px;background:#0DA77D;margin-right:6px;flex-shrink:0;line-height:0;font-size:0;"><span leaf=""><br></span></span><p style="margin:0;font-size:11px;font-weight:700;color:#111827;line-height:1.5;"><span leaf="">WorkBuddy · 成品</span></p></section></section>
```

**原作调用**：A6 把“WorkBuddy · 成品”“甲烷 · 教学演示”“甲烷 · 开源 3D 模型”等自定义对象名贴在对应成品图上沿，标题均来自当前媒体。

**触发**：给动态成品配来自真实媒体的自定义标题，并贴在该图片上沿时。

### C13 真题呈现块（C10 变体，用户 2026-11-20 指定创建）

复用 C10 灰底圆角卡骨架（高度随内容自适应、不滚动），**标签固定为「真题呈现」**（不是可替换标识，样式带 `white-space:nowrap;flex-shrink:0`，长标题不挤压换行）；标题是**内容槽位**，按本次题目来源填写（联考/模考名称，如「湖北鄂东南联盟11月联考」）。内容区两个段落均加首行缩进 `text-indent:2em`（C13 专属，不推翻母版正文顶格规则）；含作文题材料正文 + 灰色写作要求句 `color:#6B7280`（要求句与材料正文拉开层级，不用强调样式）。

```html
<section style="background:#F3F4F6;border:1px solid #E5E7EB;border-radius:8px;overflow:hidden;"><section style="display:flex;align-items:center;justify-content:space-between;gap:8px;padding:10px 14px;border-bottom:1px solid #E5E7EB;"><section style="display:flex;align-items:center;gap:8px;min-width:0;"><span style="display:inline-block;white-space:nowrap;flex-shrink:0;background:#111827;color:#FFFFFF;font-family:'Avenir Next','Helvetica Neue',Roboto,Arial,sans-serif;font-size:10px;font-weight:700;letter-spacing:1px;padding:2px 6px;border-radius:3px;line-height:1.4;"><span leaf="">真题呈现</span></span><p style="margin:0;font-size:13px;font-weight:700;color:#111827;line-height:1.4;"><span leaf="">湖北鄂东南联盟11月联考</span></p></section></section><section style="padding:14px 16px 6px;"><p style="margin:0 0 8px;font-size:12px;color:#374151;line-height:1.9;text-align:left;text-indent:2em;overflow-wrap:anywhere;"><span leaf="">那些年我们在课堂上读过的文字，总有一些会在往后的日子里不请自来。它们或许曾以语言的光泽打动过你，或许曾借故事的体温捂热过你，又或许在懵懂年纪为你叩响过生命与社会的门扉…而一篇课文真正的完成，往往不在教室里，而在漫长人生的某次“重逢”里：你忽然从中认出了自己的来路，读懂了别人的悲欢，也照见了一个家庭、一个民族在时代风尘中跋涉的身影。此刻，浮上你心头的，又是哪篇课文？</span></p><p style="margin:0 0 8px;font-size:12px;color:#6B7280;line-height:1.9;text-align:left;text-indent:2em;overflow-wrap:anywhere;"><span leaf="">以上材料引发了你怎样的联想和思考？请写一篇文章。</span></p></section></section>
```

**固定 vs 槽位**：固定的只有「真题呈现」标签（黑底白字）、卡片骨架与灰色要求句颜色；无滚动、无「上下滑动」提示，高度随内容自适应；标题（哪里的联考/模考）与材料正文每次按题目替换。**触发**：文章需要原样呈现一道真题/模考作文题并保留材料 + 要求句层级时用；不得把普通提示词、代码块改套此组件。

## 取证纪律

新增或修正任何组件，必须：① 在本库补真实骨架；② 在 `ink-teal-source-evidence.md` 补来源/签名/频率/触发；③ 得到用户确认后才进入 `theme-ink-teal-tech.md` 正文规则。缺一项默认不进入白名单。

`A6` 新组件 C8–C12 已完成 ①②③（骨架入库、证据入册、用户确认），2026-11-19 正式纳入 2.10–2.14 正文规则与默认白名单。

`C13` 真题呈现块由用户 2026-11-20 明确指定创建（复用 C10 变体），非原作逐字节提取；已按 ①②③ 补齐骨架、证据与用户确认，纳入 2.15 正文规则与默认白名单。

`PART` / `MORE` / `STORYBOARD / SHOT` 已于 2026-11-25 获用户确认：原作骨架与来源证据齐备，纳入 2.16–2.18 条件自动路由。其**原作观察**与**路由最小条件**须分开读取：PART 对应 A3 的连续大段结构；MORE 对应 A5 主案例之后、最终收束之前的“其他亮点”；STORYBOARD/SHOT 对应 A4 的连续镜头轨 + FINAL CUT 解释。为避免自动误套，路由可使用“至少两块 / 至少两镜”“需有媒体与说明”等最低识别条件，但这些不是作者明文阈值。
