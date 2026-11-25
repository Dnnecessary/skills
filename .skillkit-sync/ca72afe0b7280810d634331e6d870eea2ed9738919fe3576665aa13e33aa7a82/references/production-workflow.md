# 生产流程：从模板到导出 PNG

这份文件是动手阶段的操作手册——内容和版式都规划好之后，怎么落地成一个可渲染、可导出的任务目录，并把每一页 `.poster` 截图成 PNG。下面四块：环境自检、任务目录约定、从种子模板开始、渲染截图。

---

## 环境自检（首次运行 / 新机器）

渲染依赖三样，**首次在一个新环境跑之前先确认，缺了先装，别等渲染报错才发现**：

1. **Playwright 已安装**：在 Skill 安装目录下执行过 `npm i`（`node_modules/playwright` 存在）。
2. **chromium 浏览器已下载**：`npx playwright install chromium`（npm 包不含浏览器二进制，必须单独装一次）。
3. **字体就位**：`assets/fonts/SmileySans-Oblique.woff2` 存在（随 Skill 附带；缺了标题会回退系统字，丢高级感）。

**定位 Skill 自己的资产**：Skill 可能被安装在 `~/.agents/skills/` 或 `~/.claude/skills/` 等位置，**不一定在用户当前项目里**。模板、`base.css`、`fonts/` 都在 **Skill 安装目录的 `assets/` 下**——先确定 Skill 安装目录的绝对路径，从那里复制资产。

**产物落在用户的工作区**：任务目录 `cards-<slug>/` 建在**用户当前项目（cwd）**下，不要建在 Skill 安装目录里（别污染 Skill 自身）。渲染脚本里的 Playwright 依赖，可在用户项目临时 `npm i playwright` 或软链到 Skill 的 `node_modules`。

---

## 任务目录约定

每一次出图任务都建一个独立目录，命名为 `cards-<slug>/`，`<slug>` 用这次任务内容的简短拼音/英文标识（比如 `cards-rent-decor`、`cards-skincare-myth`）。目录结构固定如下：

```
cards-<slug>/
├── index.html        # 从种子模板复制并修改，含所有 .poster
├── base.css           # 从 assets/base.css 复制（或用相对路径引用）
├── fonts/             # 从 assets/fonts/ 复制（base.css 的 @font-face 依赖它，缺了得意黑会回退系统字）
├── assets/            # 源图：用户照片、截图、图库图、AI 生成图
│   ├── cover.jpg
│   ├── shot-01.jpg
│   └── ...
├── output/            # 渲染产出的 PNG，命名为 card-01.png, card-02.png ...
└── render.mjs         # 渲染脚本（见下文）
```

- `assets/` 只放**这次任务用到的图**，不要引用任务目录外的图片路径——保证整个 `cards-<slug>/` 目录可以独立打包、独立预览。
- `output/` 在渲染前如果不存在要先创建；每次重新渲染前可以清空，避免新旧文件混在一起。
- 不要把 `node_modules` 或全局依赖放进任务目录，Playwright 等依赖在项目根目录统一安装即可。

---

## 从种子模板开始

1. 根据规划阶段选定的风格（baokuan / magazine / ambient / minimal），把对应的 `assets/template-<style>.html` 复制到任务目录，重命名为 `index.html`。
2. 把 `assets/base.css` 复制到任务目录（保持文件名 `base.css`），或者直接在 `index.html` 里把 `<link rel="stylesheet" href="base.css">` 改成正确的相对路径指向项目根目录的 `assets/base.css`。**两种方式选一种，保证渲染时样式能正确加载**——推荐复制一份到任务目录，避免相对路径层级出错。
   - **同时把 `assets/fonts/` 一并复制到任务目录**（`base.css` 的 `@font-face` 用相对路径 `fonts/...` 加载得意黑等展示字体）。漏了字体不会报错，但标题会回退成系统字，丢掉一大半"高级感"。验证渲染图时，确认标题确实是得意黑（带利落倾斜），而不是端正的系统黑体。
3. 打开 `index.html`，找到模板里的 `<!-- POSTERS_HERE: 复制 .poster 区块来增加页数 -->` 注释。模板自带一个封面 `.poster` 和一个内容 `.poster` 作为示例：
   - 封面 `.poster`：按规划表的 P1 内容替换文案，标题、副述、底栏文案全部对应改成本次任务的内容。
   - 在 `POSTERS_HERE` 位置，按规划表逐页复制 `.poster` 区块：每一页对应规划表里的一行（P2、P3...），从 `layout-recipes.md` 里挑选对应配方的 HTML 骨架，粘进新的 `.poster` 区块里，替换文案和图片路径。
   - 最后一页（总结/CTA）同理，用"总结卡"配方。
4. 改完后用浏览器直接打开 `index.html` 预览整套图文（`.stage` 会把所有 `.poster` 纵向排列），逐页检查文案、版式、图片是否正确显示，确认无误后再进入渲染步骤。

> 提示：如果某一页用了图片打底式、大图+说明或图文展示式配方，先把对应的图放进 `assets/`，并在 `<img src="assets/xxx.jpg">` 里写相对路径——保证 `index.html` 和 `assets/` 在同一个任务目录下时路径能直接生效。

---

## 渲染截图

用 Playwright 加载 `index.html`，对每个 `.poster` 节点逐个截图导出到 `output/`。下面是可以直接放进 `cards-<slug>/render.mjs` 使用的脚本（Node ESM，项目已 `npm install playwright`）：

```js
// render.mjs
import { chromium } from "playwright";
import { fileURLToPath } from "url";
import path from "path";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const indexPath = path.join(__dirname, "index.html");
const outDir = path.join(__dirname, "output");

if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

const browser = await chromium.launch();
const page = await browser.newPage({
  // 视口大于画布即可，截图按节点尺寸导出，不依赖视口大小
  viewport: { width: 1200, height: 1600 },
});

await page.goto(`file://${indexPath}`);

// 等待网络空闲（外部字体/图片加载完成）
await page.waitForLoadState("networkidle");

// 等待字体加载完成，避免截图时字体还是兜底字体导致布局跳动
await page.evaluate(() => document.fonts.ready);

// 给一点缓冲时间，确保布局（尤其是 flex 计算）稳定
await page.waitForTimeout(200);

const posters = await page.locator(".poster").all();

for (let i = 0; i < posters.length; i++) {
  const index = String(i + 1).padStart(2, "0");
  const filePath = path.join(outDir, `card-${index}.png`);
  await posters[i].screenshot({ path: filePath });
  console.log(`exported ${filePath}`);
}

await browser.close();
```

运行方式（在任务目录下）：

```bash
node render.mjs
```

要点说明：
- **逐个节点截图**：用 `.poster` 元素自身的 `.screenshot()`，不是整页截图再裁剪——这样导出尺寸就是元素的实际渲染尺寸（1080×1440），不需要额外裁切。
- **等待就绪**：`waitForLoadState("networkidle")` 等图片/外部资源加载完，`document.fonts.ready` 等字体加载完——两者缺一都可能导致截图时图片还是空白、文字还是兜底字体导致换行位置不对。如果页面里有大量本地图片，必要时可以把 `waitForTimeout` 适当调大（如 500ms）。
- **文件命名**：按页面顺序命名为 `card-01.png`、`card-02.png`……与 `.poster` 在 `index.html` 里出现的顺序一致，方便后续按顺序发布。

---

## 核对尺寸

渲染完成后，检查 `output/` 里每个 PNG 的实际尺寸是否为 **1080 × 1440**。可以用以下命令快速核对（基于 macOS 自带的 `sips`，或用 `file` 命令）：

```bash
for f in output/*.png; do
  echo "$f: $(sips -g pixelWidth -g pixelHeight "$f" | tail -2 | tr '\n' ' ')"
done
```

如果某张图尺寸不对（常见原因：该 `.poster` 内部内容溢出导致 `overflow: hidden` 没有生效、或该节点没有正确继承 `.poster` 的宽高样式），回到 `index.html` 检查对应 `.poster` 的内容是否撑破了 `height: 1440px`（参考 `qa-checklist.md` 的"版面检查"部分），修复后重新运行 `render.mjs`。
