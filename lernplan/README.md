# Lernplan · Zivilrecht-Klausur (8 Tage)

| Tag | Datei | Inhalt |
|---|---|---|
| 1 | `tag-1/Tag-1-Das-Fundament.pdf` | Klausur, Gutachtenstil, Recht & Methode, Willenserklärung, Zugang, Vertragsschluss (§§ 1–4 der Vorlesung) |

- **Quiz-App:** https://claude.ai/artifact/Aqkgt1pBGem1hGmo2Bcx4v (Quelle `app/zivilrecht-drill.html`) – Karteikarten
  mit Wiederholungssystem, Quiz, Mini-Fälle; Fortschritt im Artifact-Datenspeicher (`progress`).
- `korrektur/` – Korrektur-Schlüssel für die Claude-Missionen und wie man den App-Fortschritt liest.
- Bauen: `node build.cjs tag-1` (Playwright/Chromium). Das Skript setzt `tag-1/pages/*.html` zusammen,
  teilt Seiten an `<!--BREAK-->`, nummeriert, rendert das PDF und meldet jede Seite, die überläuft.
- `tools/route_map.py` erzeugt die Quest-Map-Seite (`tag-1/pages/01b-route.html`).
