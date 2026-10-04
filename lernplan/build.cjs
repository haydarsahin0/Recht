// Baut ein Lern-PDF und prüft, dass keine Seite überläuft.
//
//   node build.cjs tag-1            → setzt tag-1/pages/*.html zusammen, rendert tag-1/<out>.pdf
//   node build.cjs datei.html x.pdf → rendert eine einzelne HTML-Datei
//   Option: --png <ordner>          → zusätzlich jede Seite als PNG (zur Sichtprüfung)
//
// Platzhalter in den Seiten (nur im Ordner-Modus):
//   {{RUN}}        Kopfzeile mit Seitenzahl
//   {{FOOT:text}}  Fußzeile mit Fortschritt in % und Text
//   {{P:id}}       Seitenzahl der <section data-id="id">
//   {{APP}}        Link zur Quiz-App (meta.json: app)
//   <!--BREAK-->   teilt eine Seite (nur zwischen Blöcken direkt im .body)
//   data-level="n" auf <section> → Daumenregister mit Level n hervorgehoben
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

// <!--BREAK--> auf oberster Ebene im .body teilt eine Seite in Folgeseiten mit gleichem Kicker.
function splitBreaks(s) {
  if (!s.includes('<!--BREAK-->')) return [s];
  const footIdx = s.search(/^\s*\{\{FOOT:/m);
  const before = s.slice(0, footIdx), after = s.slice(footIdx);
  const bodyStart = before.indexOf('<div class="body"');
  const bodyOpenEnd = before.indexOf('>', bodyStart) + 1;
  const prefix = before.slice(0, bodyOpenEnd);
  const inner = before.slice(bodyOpenEnd, before.lastIndexOf('</div>'));
  const parts = inner.split('<!--BREAK-->');
  const n = parts.length;
  const kicker = (inner.match(/<div class="kicker">[\s\S]*?<\/div>/) || [''])[0];
  const label = k => kicker.replace(/(<span class="rule"><\/span><span>[^<]*)(<\/span>)/, `$1 · Teil ${k}/${n}$2`);
  return parts.map((part, k) => {
    const pre = k === 0 ? prefix : prefix.replace(/data-id="([^"]+)"/, (_, id) => `data-id="${id}-${k + 1}"`);
    const body = k === 0 ? part.replace(kicker, label(1)) : `\n    ${label(k + 1)}\n` + part;
    const end = k === n - 1 ? after : '  {{FOOT:Weiter auf der nächsten Seite →}}\n</section>\n';
    return `${pre}${body}  </div>\n${end}`;
  });
}

function assemble(dir) {
  const meta = JSON.parse(fs.readFileSync(path.join(dir, 'meta.json'), 'utf8'));
  const files = fs.readdirSync(path.join(dir, 'pages')).filter(f => f.endsWith('.html')).sort();
  const raw = files.map(f => fs.readFileSync(path.join(dir, 'pages', f), 'utf8')).join('\n');
  const sections = raw.split(/(?=<section\b)/).filter(s => s.trim().startsWith('<section')).flatMap(splitBreaks);
  const total = sections.length;
  const pad = n => String(n).padStart(2, '0');
  const ids = {};
  sections.forEach((s, i) => { const m = s.match(/data-id="([^"]+)"/); if (m) ids[m[1]] = i + 1; });

  const out = sections.map((s, i) => {
    const n = i + 1;
    const pct = Math.round((n / total) * 100);
    const lvl = Number((s.match(/data-level="(\d)"/) || [])[1] || 0);
    s = s.replace(/\{\{P:([\w-]+)\}\}/g, (_, id) => { if (!ids[id]) throw new Error('Unbekannte Seiten-ID: ' + id); return ids[id]; });
    s = s.split('{{APP}}').join(meta.app || '').split('{{PAGES}}').join(String(total));
    s = s.replace('{{RUN}}', `<header class="run"><span>Recht · Klausurtraining</span><span>${meta.run}</span><span class="pg">${pad(n)} / ${pad(total)}</span></header>`);
    s = s.replace(/\{\{FOOT:([^}]*)\}\}/, (_, t) => `<footer class="foot"><div class="prog"><div class="trk"><i style="width:${pct}%"></i></div><b>${pct} %</b></div><span>${t}</span></footer>`);
    if (lvl) {
      const tabs = meta.levels.map((name, k) => `<span class="${k + 1 === lvl ? 'on' : k + 1 < lvl ? 'done' : ''}">${name}</span>`).join('');
      s = s.replace(/<\/section>\s*$/, `<div class="tabs">${tabs}</div>\n</section>\n`);
    }
    return s;
  }).join('\n');

  const html = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<title>${meta.title}</title>
<link rel="stylesheet" href="../assets/theme.css">
<link rel="stylesheet" href="style.css">
</head>
<body>
${out}
</body>
</html>
`;
  const file = path.join(dir, path.basename(dir) + '.html');
  fs.writeFileSync(file, html);
  return { file, pdf: path.join(dir, meta.out) };
}

(async () => {
  const args = process.argv.slice(2);
  const pngIdx = args.indexOf('--png');
  const pngDir = pngIdx >= 0 ? args.splice(pngIdx, 2)[1] : null;
  let [src, out] = args;
  if (fs.statSync(src).isDirectory()) ({ file: src, pdf: out } = assemble(src));

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 } });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);

  const report = await page.evaluate(() => [...document.querySelectorAll('.page')].map((p, i) => {
    const body = p.querySelector('.body');
    const foot = p.querySelector('.foot');
    if (!body || !foot || p.classList.contains('nocheck')) return { page: i + 1, free: null };
    let bottom = 0;
    body.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height) bottom = Math.max(bottom, r.bottom); });
    return { page: i + 1, free: Math.round(foot.getBoundingClientRect().top - 12 - bottom) };
  }));
  for (const r of report) {
    if (r.free === null) continue;
    console.log(`Seite ${String(r.page).padStart(2)}: ${r.free < 0 ? 'ÜBERLAUF' : 'frei'} ${r.free}px`);
  }

  await page.pdf({ path: out, preferCSSPageSize: true, printBackground: true });
  if (pngDir) {
    fs.mkdirSync(pngDir, { recursive: true });
    const els = await page.$$('.page');
    for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(pngDir, `p${String(i + 1).padStart(2, '0')}.png`) });
  }
  await browser.close();
  console.log('→', out);
  if (report.some(r => r.free !== null && r.free < 0)) process.exitCode = 1;
})();
