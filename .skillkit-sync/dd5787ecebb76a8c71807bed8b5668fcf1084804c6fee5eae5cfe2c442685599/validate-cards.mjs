#!/usr/bin/env node
/**
 * validate-cards.mjs
 *
 * 出图前的自动校验脚本：用 Playwright(chromium) 加载 HTML，
 * 遍历每个 `.poster`（即每张 1080x1440 的导出卡片），逐条检查规则：
 *
 *  R1 溢出       —— .poster 内容实际高度超过画布高度(1440px)（留 2px 容差）→ FAIL
 *  R2 底栏碰撞   —— .foot 与其上方紧邻兄弟元素重叠 → FAIL
 *  R3 最小字号   —— 可见文本 < 22px → FAIL；28px <= 字号 < 22px 之间为正文建议值，
 *                    22px <= 字号 < 28px → WARN（达到注脚下限但未达正文建议下限）
 *  R4 四横带密度 —— 纵向四等分，某带几乎无可见内容 → WARN（建议性，不影响 FAIL）
 *  R5 底座漂移   —— figure 元素存在非 0 的默认 margin（说明 base.css 复位未生效）→ WARN
 *
 * 用法：
 *   作为模块：  import { validate } from './validate-cards.mjs'
 *               const result = await validate('path/to/index.html')
 *   作为 CLI：  node validate-cards.mjs <path>
 *               <path> 可以是单个 .html 文件，或一个目录
 *               （目录优先找 index.html，没有则扫描其中所有 *.html）
 *               任一文件出现 FAIL，进程以 exit(1) 退出；否则 exit(0)。
 *               WARN 只打印，不影响退出码。
 */

import { chromium } from 'playwright';
import { existsSync, statSync, readdirSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

// 画布基准尺寸（与 base.css 的 .poster 一致）
const CANVAS_HEIGHT = 1440;
const OVERFLOW_TOLERANCE = 2; // px，留出容差避免亚像素误判

// 字号下限（与 references/style-presets.md 一致）
const MIN_CAPTION_FONT = 22; // 注脚 / 辅助文字下限，低于此值直接 FAIL
const MIN_BODY_FONT = 28;    // 正文建议下限，[22,28) 之间记 WARN

/**
 * 校验单个 HTML 文件，返回结构化结果。
 * @param {string} htmlPath HTML 文件路径
 * @returns {Promise<{ok: boolean, failures: Array, warnings: Array}>}
 */
export async function validate(htmlPath) {
  const failures = [];
  const warnings = [];

  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();

    // 通过 file:// URL 加载本地 HTML，保证相对路径(CSS/图片)解析正确
    const fileUrl = pathToFileURL(path.resolve(htmlPath)).href;
    await page.goto(fileUrl);

    // 固定 viewport 宽度，避免响应式布局影响测量（.poster 本身定宽 1080px）
    await page.setViewportSize({ width: 1200, height: 1600 });

    const posterCount = await page.locator('.poster').count();

    for (let i = 0; i < posterCount; i++) {
      const poster = page.locator('.poster').nth(i);

      // 在浏览器上下文中对当前 .poster 执行所有度量，一次性拿回结果，
      // 避免多次 evaluate 之间的句柄失效问题。
      const metrics = await poster.evaluate((posterEl, ctx) => {
        const { canvasHeight, overflowTolerance, minCaptionFont, minBodyFont } = ctx;
        const result = {
          scrollHeight: posterEl.scrollHeight,
          clientHeight: posterEl.clientHeight,
          footCollision: null, // null=无 .foot；否则 {footTop, prevBottom}
          smallFonts: [],      // [{fontSize, text}]
          bandCoverage: [false, false, false, false], // 四等分每带是否有可见内容
          figureMargins: [],   // [{margin, tag}]
        };

        // ---- R1 溢出：由外层用 scrollHeight/clientHeight 判断 ----
        // （这里只采集数值，判断逻辑放在外层，方便统一容差处理）

        // ---- R2 底栏碰撞 ----
        const foot = posterEl.querySelector('.foot');
        if (foot) {
          const footRect = foot.getBoundingClientRect();
          // 找 .foot 在 DOM 中的前一个元素兄弟节点
          let prev = foot.previousElementSibling;
          if (prev) {
            const prevRect = prev.getBoundingClientRect();
            result.footCollision = {
              footTop: footRect.top,
              prevBottom: prevRect.bottom,
              collided: footRect.top < prevRect.bottom,
            };
          }
        }

        // ---- 工具函数：判断元素是否可见 ----
        function isVisible(el) {
          const style = window.getComputedStyle(el);
          if (style.display === 'none' || style.visibility === 'hidden') return false;
          if (parseFloat(style.opacity) === 0) return false;
          const rect = el.getBoundingClientRect();
          return rect.width > 0 && rect.height > 0;
        }

        // ---- R3 最小字号：遍历包含可见文本节点的元素 ----
        const posterRect = posterEl.getBoundingClientRect();
        const walker = document.createTreeWalker(posterEl, NodeFilter.SHOW_TEXT, null);
        const checkedEls = new Set();
        let node;
        while ((node = walker.nextNode())) {
          const text = node.textContent.replace(/\s+/g, '');
          if (!text) continue; // 跳过纯空白文本节点
          const el = node.parentElement;
          if (!el || checkedEls.has(el)) continue;
          if (!isVisible(el)) continue;
          checkedEls.add(el);

          const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
          if (fontSize < minCaptionFont) {
            result.smallFonts.push({ fontSize, text: text.slice(0, 20), level: 'fail' });
          } else if (fontSize < minBodyFont) {
            result.smallFonts.push({ fontSize, text: text.slice(0, 20), level: 'warn' });
          }

          // ---- R4 四横带密度：记录该元素覆盖的纵向区间 ----
          markBandCoverage(el);
        }

        // ---- R4 补充：图片/SVG 等非文本元素也算作"有内容"，
        // 否则大图+说明 / 图文展示式这类以 <img> 为主的内容页，
        // 图片所在的横带会被误判为空白。----
        posterEl.querySelectorAll('img, svg, picture, video, canvas').forEach((el) => {
          if (isVisible(el)) markBandCoverage(el);
        });

        function markBandCoverage(el) {
          const rect = el.getBoundingClientRect();
          const relTop = rect.top - posterRect.top;
          const relBottom = rect.bottom - posterRect.top;
          const bandHeight = canvasHeight / 4;
          for (let b = 0; b < 4; b++) {
            const bandStart = b * bandHeight;
            const bandEnd = (b + 1) * bandHeight;
            // 元素与该带有交集即认为该带有内容
            if (relBottom > bandStart && relTop < bandEnd) {
              result.bandCoverage[b] = true;
            }
          }
        }

        // ---- R5 底座漂移：检查 figure 元素是否有非 0 默认 margin ----
        // 注意：.foot 通过 flex 的 margin-top:auto 把底栏推到底部，
        // 这是 base.css 的预期设计，计算后的 margin-top 会是一个较大的
        // 像素值，不能算作"漂移"。浏览器默认的 figure margin 是
        // `1em 40px`（四边都非 0，尤其 left/right），因此只检查
        // left/right/bottom 三边即可识别"复位未生效"，避免误报
        // margin-top:auto 这种合法用法。
        const figures = posterEl.querySelectorAll('figure');
        figures.forEach((fig) => {
          const style = window.getComputedStyle(fig);
          const margins = {
            top: parseFloat(style.marginTop),
            right: parseFloat(style.marginRight),
            bottom: parseFloat(style.marginBottom),
            left: parseFloat(style.marginLeft),
          };
          const hasMargin = margins.right !== 0 || margins.bottom !== 0 || margins.left !== 0;
          if (hasMargin) {
            result.figureMargins.push(margins);
          }
        });

        return result;
      }, {
        canvasHeight: CANVAS_HEIGHT,
        overflowTolerance: OVERFLOW_TOLERANCE,
        minCaptionFont: MIN_CAPTION_FONT,
        minBodyFont: MIN_BODY_FONT,
      });

      // ===== R1 溢出 =====
      if (metrics.scrollHeight > metrics.clientHeight + OVERFLOW_TOLERANCE) {
        failures.push({
          rule: 'R1',
          msg: `内容高度 ${metrics.scrollHeight}px 超出画布高度 ${metrics.clientHeight}px（容差 ${OVERFLOW_TOLERANCE}px）`,
          posterIndex: i,
        });
      }

      // ===== R2 底栏碰撞 =====
      if (metrics.footCollision && metrics.footCollision.collided) {
        failures.push({
          rule: 'R2',
          msg: `.foot 顶边(${metrics.footCollision.footTop.toFixed(1)}px) 与上方内容底边(${metrics.footCollision.prevBottom.toFixed(1)}px) 重叠`,
          posterIndex: i,
        });
      }

      // ===== R3 最小字号 =====
      for (const sf of metrics.smallFonts) {
        if (sf.level === 'fail') {
          failures.push({
            rule: 'R3',
            msg: `字号 ${sf.fontSize}px 小于注脚下限 ${MIN_CAPTION_FONT}px（文本："${sf.text}"）`,
            posterIndex: i,
          });
        } else {
          warnings.push({
            rule: 'R3',
            msg: `字号 ${sf.fontSize}px 低于正文建议下限 ${MIN_BODY_FONT}px（文本："${sf.text}"）`,
            posterIndex: i,
          });
        }
      }

      // ===== R4 四横带密度 =====
      metrics.bandCoverage.forEach((covered, bandIdx) => {
        if (!covered) {
          warnings.push({
            rule: 'R4',
            msg: `第 ${bandIdx + 1}/4 横带（纵向 ${Math.round(bandIdx * CANVAS_HEIGHT / 4)}~${Math.round((bandIdx + 1) * CANVAS_HEIGHT / 4)}px）几乎没有可见内容，密度偏低`,
            posterIndex: i,
          });
        }
      });

      // ===== R5 底座漂移 =====
      metrics.figureMargins.forEach((m) => {
        warnings.push({
          rule: 'R5',
          msg: `figure 元素存在非 0 默认 margin（top:${m.top} right:${m.right} bottom:${m.bottom} left:${m.left}），检查 base.css 复位是否生效`,
          posterIndex: i,
        });
      });
    }
  } finally {
    await browser.close();
  }

  return {
    ok: failures.length === 0,
    failures,
    warnings,
  };
}

// ---------------------------------------------------------------------
// CLI 入口
// ---------------------------------------------------------------------

/**
 * 解析输入路径为待校验的 HTML 文件列表。
 * - 若是单个 .html 文件，直接返回该文件
 * - 若是目录，优先找 index.html；没有则扫描该目录下所有 *.html
 */
function resolveHtmlFiles(inputPath) {
  if (!existsSync(inputPath)) {
    throw new Error(`路径不存在：${inputPath}`);
  }

  const stat = statSync(inputPath);
  if (stat.isFile()) {
    return [inputPath];
  }

  // 目录：优先 index.html
  const indexPath = path.join(inputPath, 'index.html');
  if (existsSync(indexPath)) {
    return [indexPath];
  }

  // 否则扫描目录下所有 .html 文件
  return readdirSync(inputPath)
    .filter((f) => f.endsWith('.html'))
    .map((f) => path.join(inputPath, f))
    .sort();
}

async function runCli() {
  const inputPath = process.argv[2];
  if (!inputPath) {
    console.error('用法：node validate-cards.mjs <html文件或目录>');
    process.exit(1);
  }

  let files;
  try {
    files = resolveHtmlFiles(inputPath);
  } catch (err) {
    console.error(err.message);
    process.exit(1);
  }

  if (files.length === 0) {
    console.error(`目录中未找到任何 .html 文件：${inputPath}`);
    process.exit(1);
  }

  let anyFailure = false;

  for (const file of files) {
    console.log(`\n=== ${file} ===`);
    const result = await validate(file);

    if (result.failures.length === 0 && result.warnings.length === 0) {
      console.log('  全部通过，无问题。');
    }

    for (const f of result.failures) {
      console.log(`  [FAIL][${f.rule}] poster#${f.posterIndex}: ${f.msg}`);
    }
    for (const w of result.warnings) {
      console.log(`  [WARN][${w.rule}] poster#${w.posterIndex}: ${w.msg}`);
    }

    if (!result.ok) {
      anyFailure = true;
    }
  }

  process.exit(anyFailure ? 1 : 0);
}

// 仅在被直接执行时运行 CLI（被 import 时不运行）
if (import.meta.url === pathToFileURL(process.argv[1] ?? '').href) {
  runCli();
}
