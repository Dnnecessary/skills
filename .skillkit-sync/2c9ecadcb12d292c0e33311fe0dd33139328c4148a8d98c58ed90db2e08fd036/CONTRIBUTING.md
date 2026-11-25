# 墨青测评风维护指南

本技能不是多主题组件仓库。维护目标是让输出持续忠实于墨青测评风母版，而不是扩大组件数量。

## 允许的改动

- 修复与母版不一致的 HTML、CSS、SVG、间距、字体、动效或校验逻辑。
- 在指定母版或五篇同作者原作中发现新的重复结构后，补充证据并经用户确认纳入白名单。
- 改进确定性校验、预览与回归测试。

## 禁止的改动

- 新增其他主题、主题选择、主题生成器或通用组件库。
- 从其他公众号主题借用引用块、金句卡、提示卡、数据卡、参数卡、目录、签名区或 CTA。
- 用语义推断取代“母版白名单 + 原文触发条件”的双判定。
- 伪造图片、图注、案例、数据或场景动画。

## 新规则准入

每条候选规则必须先写入 `references/ink-teal-source-evidence.md`，并具备：

1. 来源文件；
2. 可定位的 HTML/CSS/SVG 签名；
3. 出现频率；
4. 原始触发条件；
5. 是否允许泛化及其边界。

证据不完整时默认不进入 `theme-ink-teal-tech.md`。

## 验证

```bash
python3 scripts/component_lint.py .
python3 scripts/validate_gzh_html.py --theme ink-teal-tech output.html
python3 scripts/test_validate_gzh_html.py
```

组件源头与产物校验必须 0 ERROR。涉及封面或词内动画时，还需按主题库规定逐帧检查 SVG 与固定 390px 容器预览。
