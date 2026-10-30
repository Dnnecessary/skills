# 端到端样例：第一次养猫踩的坑

这是按 `SKILL.md` 8 步工作流走的一次完整样例，用来验证整套 Skill（references + assets + validate-cards.mjs）能跑通真实任务。

## 素材

`examples/sample-input.md`——一段约 600 字的"第一次养猫踩坑"经验帖，涉及猫砂选择、换粮过渡、磨爪、疫苗驱虫、砂盆摆放、陪伴时间共 6 个坑，是真实感较强的痛点解决型素材。

## 选题判断（operation-engine）

属于**痛点解决型**选题：人群具体（第一次养猫的人）、有明确利益点（避免重复花钱/跑医院）、切口小（6 个具体的坑而非"养猫攻略"）、有可信度支撑（作者亲身经历）、能引发互动（评论区可以接"你踩过哪个坑"）。选题判断为值得做。

## 页面规划（content-planning）

核心主张：第一次养猫，这 6 个坑很容易踩，提前知道能省钱省事。
读者收益：照着避开这 6 个坑，少花冤枉钱、少跑急诊。

| 页 | 角色 | 内容 |
|---|---|---|
| P1 封面 | 钩子封面 | 数字型钩子"这 6 个坑我全踩了" + 悬念（第 2 个坑差点送医院） |
| P2 | 误区 vs 真相 | 猫砂选错 vs 换豆腐砂 |
| P3 | 编号要点卡 | 换粮过渡 / 提前买猫抓板 / 第一周排疫苗表（坑 2-4） |
| P4 | 清单勾选 | 砂盆摆放原则（坑 5，5 条勾选项） |
| P5 | 金句 + 场景 | 陪伴误区（坑 6），引用句 + 场景描述 |
| P6 | 总结卡 + CTA | 6 个关键词标签回顾 + 评论区互动引导 |

共 6 页（1 封面 + 5 内容页），符合 600-1000 字素材的 5-7 张建议区间。

## 风格选择（style-system / style-presets）

选择 **baokuan（爆款原生风）**。理由：素材是第一人称、强烈避坑/吐槽语气的干货分享，需要"一眼砸脸"的视觉冲击和高密度信息卡片，baokuan 的便利贴角标、手绘箭头、编号要点卡、对比双栏配方都最贴合这种调性。同一套图文全程未混用其他风格。

## 产出

任务目录：`examples/cards-cat-mistakes/`

- `index.html`：复制自 `assets/template-baokuan.html`，1 封面 + 5 内容页，共 6 个 `.poster`
- `base.css`：复制自 `assets/base.css`
- `render.mjs`：按 `production-workflow.md` 的标准脚本，逐 `.poster` 截图
- `output/card-01.png` ~ `card-06.png`：渲染产出，均为 **1080 × 1440（3:4）**

## validate-cards.mjs 结果

```
node validate-cards.mjs examples/cards-cat-mistakes/index.html
```

结果：**退出码 0，无 FAIL**。剩余全部为 WARN：

- `[WARN][R3]`：每页 `.foot` 里的 `@账号名` 和翻页提示文案字号为 24px（即 baokuan 预设的 `--fs-caption`），低于"正文建议下限 28px"但高于"注脚下限 22px"——这是模板预设值，属于设计内行为，不是 FAIL。
- 经过两轮调整（comparison 双栏增加正文长度、checklist 改为 `flex:1 + space-evenly` 撑满、金句页补充场景描述、总结页加一段"边养边改"收尾段），原先的 `[WARN][R4]` 密度不足全部消除，6 页内容覆盖均 ≥ 75% 画布高度。
- 修复过程中还发现并修复了 1 处 `[FAIL][R3]`：清单勾选符号 "✓" 缺少显式字号继承到 16px，补上 `font-size:28px` 后通过。

## QA 核对（qa-checklist.md）

**版面检查**
- 无溢出：6 页均在 1080×1440 内，无内容被裁切
- 无底栏碰撞：`.foot` 均靠 `margin-top:auto` 推到底部，不压正文
- 最小字号达标：正文 ≥32px（`--fs-body`），注脚 24px（在 22-28px 区间，达标）
- 四横带密度：6 页均覆盖 ≥75% 画布高度，无大片死区
- 缩略图可读：封面在 360px 缩放下，"第一次养猫 / 这 6 个坑 / 我全踩了 / 一遍" 主标题层级清晰，关键词色块和描边框在小图下依然能辨认

**流量视角检查**
- 封面有钩子：数字型（6 个坑）+ 悬念型（第 2 个坑差点送医院）双钩子叠加
- 每页一个点：P2 猫砂、P3 三个开局坑、P4 砂盆摆放、P5 陪伴误区、P6 总结，逐页单一焦点
- 完读诱导：P1"往下滑一条条看"、P2"下一页更扎心"、P3"还有 2 个坑"、P4"最后一个坑最容易忽略"、P5"最后一页 总结来了"，形成连续翻页钩子
- 互动 CTA：P6 收尾"你养猫踩过哪个坑？评论区告诉我，攒够了出二期"，单一动作（评论），不堆叠多个指令
- 文案去 AI 味：全篇第一人称、短句、口语化（"猫一上厕所家里就跟起雾一样""我家沙发角已经废了"），无排比堆砌、无空洞升华、无"首先其次"式连接词
- 限流红线：未出现"最/第一/根治/100%/绝对"等极限词，表达均带主观限定（"我图便宜买的""我以为""后来"）

## 运营建议

- **发布时间窗口**：建议工作日晚 8-10 点或周末上午 10-12 点，宠物类内容在该时段互动率较高
- **话题标签**：#养猫日记 #新手养猫 #猫咪用品 #养猫踩坑 #第一次养猫
- **正文/评论区延伸方向**：正文可补充具体产品类型的选购思路（不点名品牌，给"怎么挑"的标准），评论区主动置顶"你养猫踩过哪个坑？"引导用户接话，攒够素材后按 P6 承诺出第二期，形成账号连续性

## 图片路径

- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/index.html`
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-01.png`（封面）
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-02.png`
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-03.png`
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-04.png`
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-05.png`
- `/Volumes/MarsSSD/文稿/codes/socialskill/xdxlab-viral-cards/examples/cards-cat-mistakes/output/card-06.png`

## 全局原创性终检

```
grep -riE "归藏|guizang" . --include="*.md" --include="*.html" --include="*.css" --include="*.mjs" | grep -v node_modules
```

结果：**无输出**，全局未出现第三方品牌名。
