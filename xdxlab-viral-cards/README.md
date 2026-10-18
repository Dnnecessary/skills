# xdxlab-viral-cards

把文章、脚本、截图、产品笔记、字幕或素材，做成**会涨粉的小红书 3:4 图文**(封面 + 内容页)。

这不是一个单纯的排版工具——运营优先、版面在后：先判断选题值不值得做、设计封面钩子和完读路径，再选风格、排版、渲染导出。内置 4 套原创视觉风格（爆款原生 / 高级杂志 / 柔和氛围 / 极简冲击），以及去 AI 味文案、风控自查、数据复盘等运营内核。

流程：HTML（4 套风格模板 + 共享 `base.css`） → Playwright (chromium) 截图 → 1080×1440 PNG。

---

## 这是一个 Agent Skill

本仓库是一份遵循 **Agent Skills** 约定的技能包：根目录的 [`SKILL.md`](SKILL.md) 是入口文件（YAML frontmatter 声明 `name` / `description`，正文是给 AI Agent 看的工作流说明），`references/` 下是按需加载的详细方法论文档，`assets/` 是渲染用的模板和共享样式。

这套约定不是 Claude 专属——只要你的 AI Agent（Claude Code、Codex CLI、Gemini CLI、Copilot CLI 等）支持"读取一个技能目录里的 `SKILL.md` 作为额外指令"这种模式，就可以使用本 Skill。内容全部是自然语言描述（"读哪个文件、跑什么命令"），不依赖任何 Claude 专属的工具调用语法。

---

## 安装方式

### 1. 克隆仓库

```bash
git clone https://github.com/xdx888999/xdxlab-viral-cards.git
```

### 2. 放进你的 Agent 的 skills 目录

不同 Agent 的技能目录约定不完全一致，把克隆下来的目录**复制或软链**到对应位置即可：

| Agent | 常见 skills 目录 |
|---|---|
| Claude Code（全局） | `~/.claude/skills/xdxlab-viral-cards/` |
| Claude Code（项目内） | `<项目>/.claude/skills/xdxlab-viral-cards/` |
| 通用 Agent Skills 约定 | `~/.agents/skills/xdxlab-viral-cards/` |
| Codex CLI / Gemini CLI / Copilot CLI 等 | 参考各自文档里的 skills/plugins 目录，按同样方式放置即可 |

软链示例（推荐，方便后续 `git pull` 更新）：

```bash
ln -s /path/to/xdxlab-viral-cards ~/.claude/skills/xdxlab-viral-cards
```

### 3. 安装渲染依赖

出图环节依赖 Playwright + chromium，在 Skill 目录下执行一次：

```bash
npm install
npx playwright install chromium
```

---

## 如何更新

**如果按上面推荐的"克隆 + 软链"方式安装**：直接在克隆目录里拉取最新代码即可，软链指向的还是同一个目录，所有 Agent 下次调用时自动生效。

```bash
cd /path/to/xdxlab-viral-cards
git pull
```

**如果是把目录复制到了 skills 目录里**（没用软链）：拉取最新代码后，重新整体覆盖复制一次。

```bash
cd /path/to/xdxlab-viral-cards
git pull
rm -rf ~/.claude/skills/xdxlab-viral-cards   # 换成你实际的 skills 路径
cp -r . ~/.claude/skills/xdxlab-viral-cards
```

更新后若 `package.json` 有变化，记得重新执行一次 `npm install`。

> 字体已内置（`assets/fonts/SmileySans-Oblique.woff2`，得意黑 Smiley Sans，免费商用），无需额外下载。

---

## 怎么用

跟你的 AI Agent 描述需求即可，比如：

> 帮我把这篇文章做成小红书图文
> 这个产品我想发小红书推广一下，帮我出一套图
> 这是我发过的笔记和后台数据截图，帮我看看为什么没爆

Agent 会自动识别并加载这个 Skill（基于 `SKILL.md` 里的 `description`），按"选题判断 → 页面规划 → 选风格 → 封面设计 → 渲染 → 去AI味 → QA → 交付"八步走完整流程。也支持只要一张封面、或者拿已发布笔记做复盘诊断。

---

## 目录结构

```
xdxlab-viral-cards/
├── SKILL.md              # 入口：定位、工作流、非协商项
├── references/           # 按需加载的方法论文档（选题/钩子/排版/文案/风控...）
├── assets/                # base.css + 4 套风格模板 + 字体
├── examples/              # 示例素材与产出
├── validate-cards.mjs     # 出图前自动校验脚本（溢出/字号/密度等）
└── test/                  # 校验脚本的单测
```

---

## 字体授权

内置 **得意黑 Smiley Sans**（`assets/fonts/SmileySans-Oblique.woff2`），免费商用字体，详见其官方发布页的授权条款。如需替换/新增其他展示字体，请只使用明确标注"个人+商用免费"的字体（见 `references/typography-and-texture.md`）。

## License

[MIT](LICENSE)
