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
  viewport: { width: 1200, height: 1600 },
});

await page.goto(`file://${indexPath}`);
await page.waitForLoadState("networkidle");
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(200);

const posters = await page.locator(".poster").all();

for (let i = 0; i < posters.length; i++) {
  const index = String(i + 1).padStart(2, "0");
  const filePath = path.join(outDir, `card-${index}.png`);
  await posters[i].screenshot({ path: filePath });
  console.log(`exported ${filePath}`);
}

await browser.close();
