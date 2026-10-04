// Rendert eine Lernplan-HTML-Datei als A4-PDF und prüft, dass keine Seite überläuft.
// Aufruf: node build.cjs tag-1-probe.html Tag-1-Probe.pdf [--png <dir>]
const { chromium } = require('playwright');
const { resolve } = require('node:path');

(async () => {
const [src, out, flag, pngDir] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
await page.goto('file://' + resolve(src));
await page.evaluate(() => document.fonts.ready);

const problems = await page.evaluate(() => {
  const res = [];
  document.querySelectorAll('.page').forEach((p, i) => {
    const body = p.querySelector('.body');
    const foot = p.querySelector('.foot');
    let bottom = 0;
    body.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height) bottom = Math.max(bottom, r.bottom); });
    const free = foot.getBoundingClientRect().top - 14 - bottom;
    res.push({ page: i + 1, free: Math.round(free) });
  });
  return res;
});
for (const p of problems) console.log(`Seite ${String(p.page).padStart(2)}: ${p.free < 0 ? 'ÜBERLAUF' : 'frei'} ${p.free}px`);

await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
if (flag === '--png') {
  const n = problems.length;
  for (let i = 0; i < n; i++) {
    const el = (await page.$$('.page'))[i];
    await el.screenshot({ path: `${pngDir}/p${String(i + 1).padStart(2, '0')}.png` });
  }
}
await browser.close();
if (problems.some(p => p.free < 0)) process.exitCode = 1;
})();
