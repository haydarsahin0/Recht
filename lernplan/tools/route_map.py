"""Erzeugt die Seite „Deine Route" (Quest-Map) für einen Lerntag.

Aufruf: python3 tools/route_map.py > tag-1/pages/01b-route.html
"""
GOLD, GOLDL, DEEP, INK, MUTED, CARD, NIGHT = "#a47c3b", "#bf9858", "#85662b", "#1c1a17", "#6b665d", "#f7f6f2", "#16140f"
W, ROWS, R = 694, [78, 222, 366, 510, 654], 72
XL, XR = 84, 610

levels = [
    ("Level 1 · Die Klausur", "55 Min · 15 XP"),
    ("Level 2 · Recht & Methode", "105 Min · 30 XP"),
    ("Level 3 · Die Willenserklärung", "85 Min · 25 XP"),
    ("Level 4 · Der Vertrag", "90 Min · 55 XP"),
    ("Finale · Training & Boss", "115 Min · 220 XP"),
]
# (zeile, x, art, kurz, titel, zeit, xp)
nodes = [
    (0, 150, "n", "§1", "Klausur verstehen", "15'", ""),
    (0, 300, "n", "§2", "Was der Prüfer will", "15'", "5 XP"),
    (0, 450, "n", "§3", "Dein Gesetzbuch", "25'", "5 XP"),
    (1, 560, "n", "§4", "Was ist Recht?", "15'", "5 XP"),
    (1, 455, "n", "§5", "Privatrecht & BGB", "15'", "5 XP"),
    (1, 350, "n", "§6", "Gutachtenstil", "30'", "5 XP"),
    (1, 245, "n", "§7", "Normen & Auslegung", "20'", "5 XP"),
    (1, 140, "n", "§8", "Der Anspruch", "25'", "5 XP"),
    (2, 150, "n", "§9", "Willenserklärung", "25'", "5 XP"),
    (2, 280, "n", "§10", "Meinungsstreit", "20'", "5 XP"),
    (2, 410, "n", "§11", "Zugang", "25'", "5 XP"),
    (2, 540, "n", "§12", "Sonderfälle", "15'", "5 XP"),
    (3, 550, "n", "§13", "Angebot + Annahme", "30'", "5 XP"),
    (3, 420, "n", "§14", "Auktion & Co.", "15'", "5 XP"),
    (3, 290, "n", "§15", "Muster-Gutachten", "20'", "10 XP"),
    (3, 160, "n", "§16", "Mini-Fälle", "25'", "30 XP"),
    (4, 120, "m", "M1", "Mission 1", "25'", "30 XP"),
    (4, 215, "m", "M2", "Mission 2", "30'", "50 XP"),
    (4, 310, "m", "M3", "Mission 3", "15'", "36 XP"),
    (4, 405, "k", "", "Karten", "15'", "24 XP"),
    (4, 500, "a", "", "App-Drill", "15'", "20 XP"),
    (4, 615, "b", "", "Boss-Test", "15'", "60 XP"),
]
pauses = [(XR + R, (ROWS[0] + ROWS[1]) / 2, "r"), (XL - R, (ROWS[1] + ROWS[2]) / 2, "l"),
          (XR + R, (ROWS[2] + ROWS[3]) / 2, "r"), (XL - R, (ROWS[3] + ROWS[4]) / 2, "l")]

H = ROWS[-1] + 70
p = [f'M 36 {ROWS[0]} H {XR}']
for i in range(4):
    y0, y1 = ROWS[i], ROWS[i + 1]
    if i % 2 == 0:
        p.append(f'A {R} {R} 0 0 1 {XR} {y1} H {XL}')
    else:
        p.append(f'A {R} {R} 0 0 0 {XL} {y1} H {XR}')
p[-1] = p[-1].replace(f'H {XR}', 'H 612')
path = ' '.join(p)

out = []
out.append(f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" style="display:block;overflow:visible" font-family="Lora, serif">')
out.append(f'<path d="{path}" fill="none" stroke="#e4dccd" stroke-width="10" stroke-linecap="round"/>')
out.append(f'<path d="{path}" fill="none" stroke="{GOLDL}" stroke-width="1.2" stroke-dasharray="3 5" stroke-linecap="round"/>')
for i, (name, meta) in enumerate(levels):
    y = ROWS[i] - 40
    out.append(f'<text x="20" y="{y}" font-size="8.6" letter-spacing="2.2" fill="{GOLD}">{name.upper()}</text>')
    out.append(f'<text x="{W - 20}" y="{y}" font-size="8.6" letter-spacing="1.2" fill="{MUTED}" text-anchor="end">{meta.upper()}</text>')
# Start
out.append(f'<g transform="translate(36 {ROWS[0]})"><rect x="-7" y="-7" width="14" height="14" transform="rotate(45)" fill="{GOLD}"/></g>')
out.append(f'<text x="36" y="{ROWS[0] + 28}" font-size="8.4" letter-spacing="1.8" fill="{GOLD}" text-anchor="middle">START</text>')
for x, y, side in pauses:
    out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#fbefd8" stroke="{GOLDL}"/>')
    out.append(f'<use href="#i-coffee" x="{x - 9}" y="{y - 9}" width="18" height="18" style="color:{DEEP}"/>')
    tx, anchor = (x - 22, "end") if side == "r" else (x + 22, "start")
    out.append(f'<text x="{tx}" y="{y - 1}" font-size="8.6" fill="{INK}" text-anchor="{anchor}" font-weight="600">Pause 10\'</text>')
    out.append(f'<text x="{tx}" y="{y + 10}" font-size="8" fill="{MUTED}" text-anchor="{anchor}">+5 XP Level-Bonus</text>')
for row, x, kind, short, title, t, xp in nodes:
    y = ROWS[row]
    if kind == "n":
        out.append(f'<circle cx="{x}" cy="{y}" r="19" fill="{CARD}" stroke="{GOLDL}" stroke-width="1.2"/>')
        fs = 15 if len(short) < 3 else 13.5
        out.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="{fs}" font-weight="600" fill="{DEEP}">{short}</text>')
    elif kind == "m":
        out.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{NIGHT}" stroke="{GOLDL}" stroke-width="1.2"/>')
        out.append(f'<use href="#i-pen" x="{x - 9}" y="{y - 12}" width="18" height="18" style="color:{GOLDL}"/>')
        out.append(f'<text x="{x}" y="{y + 15}" text-anchor="middle" font-size="6.4" letter-spacing="1" fill="{GOLDL}">{short}</text>')
    elif kind == "a":
        out.append(f'<circle cx="{x}" cy="{y}" r="19" fill="#faf3e4" stroke="{GOLD}" stroke-width="1.4"/>')
        out.append(f'<use href="#i-target" x="{x - 9}" y="{y - 9}" width="18" height="18" style="color:{DEEP}"/>')
    elif kind == "k":
        out.append(f'<circle cx="{x}" cy="{y}" r="19" fill="{CARD}" stroke="{GOLDL}" stroke-width="1.2"/>')
        out.append(f'<use href="#i-cards" x="{x - 9}" y="{y - 9}" width="18" height="18" style="color:{DEEP}"/>')
    else:
        out.append(f'<circle cx="{x}" cy="{y}" r="33" fill="none" stroke="{GOLDL}" stroke-width=".8" stroke-dasharray="2 3"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="27" fill="{GOLD}"/>')
        out.append(f'<use href="#i-sword" x="{x - 12}" y="{y - 12}" width="24" height="24" style="color:#fff"/>')
    ty = y + (46 if kind == "b" else 36)
    out.append(f'<text x="{x}" y="{ty}" text-anchor="middle" font-size="9.6" font-weight="600" fill="{INK}">{title}</text>')
    meta = t + (f" · {xp}" if xp else "")
    out.append(f'<text x="{x}" y="{ty + 12}" text-anchor="middle" font-size="8.4" fill="{MUTED}">{meta}</text>')
out.append('</svg>')
svg = '\n'.join(out)

print(f'''<!-- ═════════════ ROUTE (generiert von tools/route_map.py) ═════════════ -->
<section class="page" data-id="route">
  {{{{RUN}}}}
  <div class="body">
    <div class="kicker"><span class="sec">✦</span><span class="rule"></span><span>Quest-Map</span></div>
    <h1>Deine <em>Route</em> für heute.</h1>
    <div class="routebar">
      <div><b>≈ 7:30</b><span>Std. Lernzeit</span></div>
      <div><b>4</b><span>Pausen à 10 Min</span></div>
      <div><b>350</b><span>XP möglich</span></div>
      <div class="hl"><b>230</b><span>XP Tagesziel</span></div>
    </div>
    <div class="maplegend">
      <span><i class="ml n"></i>Lernstation</span>
      <span><i class="ml m"></i>Claude-Mission · selbst schreiben</span>
      <span><i class="ml a"></i>App-Drill</span><span><i class="ml b"></i>Boss-Test</span>
      <span><i class="ml p"></i>Pause + Level-Bonus</span>
    </div>
    <div style="margin-top:14px">
{svg}
    </div>
    <div class="tr mt8"><span class="tag">TR</span><p>Bu senin bugünkü haritan. Her durağı bitirince dairenin içini kalemle doldur. Koyu daireler = Claude görevleri: Kendin yaz, fotoğrafını çek, Claude'a gönder.</p></div>
  </div>
  {{{{FOOT:Los geht's: Level 1 →}}}}
</section>''')
