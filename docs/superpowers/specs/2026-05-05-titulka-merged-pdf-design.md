# Titulní strana — prepend k `merged.pdf`

**Datum:** 2026-05-05
**Pracovní adresář:** `/Users/tomas/projects/rst/pdf/`
**Kontext:** finální merged PDF souborného řešení Úloh E (1E–5E) existuje samostatně mimo hlavní repo `RST/`. Je třeba k němu prependnout titulní stranu bez přebuilďování zdrojového LaTeX projektu `reseni_souborne/`.

## Cíl

Vygenerovat samostatnou jednostránkovou A4 titulpage (`titlepage.pdf`) přes `pdflatex` a spojit ji s existujícím `merged.pdf` přes `pdfunite`. Obsahově vychází z [`2026-05-05-titulka-design.md`](2026-05-05-titulka-design.md) (varianta A — klasický VUT styl), s text-only fallbackem místo loga.

## Vstupy a výstupy

| Soubor | Role |
|---|---|
| `merged.pdf` (existující, 18 stran, 4.7 MB) | vstup — finální obsah 1E–5E |
| `merged_orig.pdf` | backup originálu (vytvořen idempotentně před prvním buildem) |
| `titlepage.tex` | LaTeX zdroj titulky |
| `titlepage.pdf` | build artifact, 1 strana A4 |
| `build.sh` | build + merge skript |
| `merged.pdf` (přepsaný) | výstup — titulka + originál (19 stran) |

Cesty všech souborů: `/Users/tomas/projects/rst/pdf/`.

## Obsah titulky

| Položka | Hodnota |
|---|---|
| Škola | Vysoké učení technické v Brně |
| Fakulta | Fakulta strojního inženýrství |
| Ústav | Ústav mechaniky těles, mechatroniky a biomechaniky |
| Předmět | Spolehlivost konstrukcí |
| Úloha | Úlohy E (souborné řešení příkladů 1E–5E) |
| Akademický rok | 2025/2026 |
| Tým | Tomáš Pavlíček, Tomáš Sláčik, Vašek Horčic, Eduard Paclík |
| Číslo skupiny | — (vynecháno per uživatel) |
| Logo | text-only fallback `VUT FSI` (žádný obrázek) |

## Layout

A4, `article` 12pt, `\thispagestyle{empty}`, `geometry a4paper`, `babel czech`, `inputenc utf8`.

```
[horizontal rule, plná šířka]
{\bfseries\Large VUT FSI}                         (text fallback, vlevo nahoře)
[horizontal rule, plná šířka]

(centered, normal:)
Vysoké učení technické v Brně
Fakulta strojního inženýrství
Ústav mechaniky těles, mechatroniky a biomechaniky

\vfill

(centered:)
ÚLOHY E                                           (\Huge \bfseries)
Souborné řešení příkladů 1E – 5E                  (\Large)

(centered, italic:)
Spolehlivost konstrukcí                           (\large)

\vfill

(centered:)
Členové týmu:                                     (\bfseries)
Tomáš Pavlíček
Tomáš Sláčik
Vašek Horčic
Eduard Paclík

Akademický rok 2025/2026                          (\small)
```

## Build skript

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
[ -f merged_orig.pdf ] || cp merged.pdf merged_orig.pdf
pdflatex -interaction=nonstopmode titlepage.tex
pdfunite titlepage.pdf merged_orig.pdf merged.pdf
echo "Done. merged.pdf = titlepage + merged_orig.pdf ($(pdfinfo merged.pdf | awk '/^Pages/ {print $2}') stran)"
```

Idempotence: `merged_orig.pdf` se vytváří jen když neexistuje — opakované spuštění nepřepíše backup vlastním výstupem.

## Postup ověření

1. `bash build.sh` — exit code 0, žádný `! LaTeX Error` ve výstupu.
2. `pdfinfo merged.pdf` — `Pages: 19`, `Page size: 595.276 x 841.89 pts (A4)`.
3. Vizuální kontrola titulky v PDF prohlížeči (PDF.js / Preview).
4. Druhá strana = původní strana 1 z `merged_orig.pdf`.

## Out of scope

- Stažení / vložení oficiálního VUT loga (PNG/PDF).
- Změny v zdrojovém LaTeX projektu `priklady/reseni_souborne/`.
- Úpravy obsahu `merged_orig.pdf` (1E–5E).
- Číslo skupiny, datum odevzdání nad rámec akademického roku.
- Header / footer / číslování stran (titulka má `\thispagestyle{empty}`, zbytek dokumentu zachovává původní styl).

## Závislosti

- `pdflatex` (TeX Live, `/Library/TeX/texbin/pdflatex`) — ověřeno.
- `pdfunite` (poppler, `/opt/homebrew/bin/pdfunite`) — ověřeno.
- `pdfinfo` (poppler) — pro verifikaci stránek.
