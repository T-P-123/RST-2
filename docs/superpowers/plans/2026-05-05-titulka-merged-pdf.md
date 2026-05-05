# Titulka pro merged.pdf — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepend single-page A4 titulka před existující `merged.pdf` (souborné řešení Úloh E, 1E–5E) bez rebuildu zdrojového LaTeX projektu.

**Architecture:** Standalone `titlepage.tex` (article 12pt, A4, `\thispagestyle{empty}`) → `pdflatex` → `titlepage.pdf` (1 strana). Merge přes `pdfunite titlepage.pdf merged_orig.pdf merged.pdf`. Idempotent backup originálu na `merged_orig.pdf` při prvním spuštění.

**Tech Stack:** TeX Live (`pdflatex`), Poppler (`pdfunite`, `pdfinfo`), bash. Vše už nainstalováno (`/Library/TeX/texbin/pdflatex`, `/opt/homebrew/bin/pdfunite`).

**Spec:** `docs/superpowers/specs/2026-05-05-titulka-merged-pdf-design.md`

**Pracovní adresář všech souborů:** `/Users/tomas/projects/rst/pdf/`

---

### Task 1: Záloha originálního merged.pdf

**Files:**
- Read: `/Users/tomas/projects/rst/pdf/merged.pdf` (existuje, 18 stran)
- Create: `/Users/tomas/projects/rst/pdf/merged_orig.pdf` (kopie originálu)

- [ ] **Step 1: Ověř že originál existuje a má 18 stran**

Run:
```bash
pdfinfo /Users/tomas/projects/rst/pdf/merged.pdf | awk '/^Pages/ {print $2}'
```
Expected: `18`

- [ ] **Step 2: Vytvoř backup (idempotentně)**

Run:
```bash
cd /Users/tomas/projects/rst/pdf
[ -f merged_orig.pdf ] || cp merged.pdf merged_orig.pdf
```
Expected: žádný výstup, exit 0.

- [ ] **Step 3: Ověř backup**

Run:
```bash
pdfinfo /Users/tomas/projects/rst/pdf/merged_orig.pdf | awk '/^Pages/ {print $2}'
```
Expected: `18`

---

### Task 2: Napsat titlepage.tex

**Files:**
- Create: `/Users/tomas/projects/rst/pdf/titlepage.tex`

- [ ] **Step 1: Vytvoř soubor s tímto obsahem**

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[czech]{babel}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{graphicx}

\pagestyle{empty}

\begin{document}
\thispagestyle{empty}

\noindent\rule{\textwidth}{0.4pt}\\[0.3em]
{\bfseries\Large VUT FSI}\\[0.3em]
\noindent\rule{\textwidth}{0.4pt}

\begin{center}
  \vspace*{0.5cm}
  Vysoké učení technické v Brně\\[0.2em]
  Fakulta strojního inženýrství\\[0.2em]
  Ústav mechaniky těles, mechatroniky a biomechaniky

  \vfill

  {\Huge\bfseries ÚLOHY E}\\[0.6em]
  {\Large Souborné řešení příkladů 1E\,--\,5E}\\[1.2em]
  {\large\itshape Spolehlivost konstrukcí}

  \vfill

  {\bfseries Členové týmu:}\\[0.4em]
  Tomáš Pavlíček\\
  Tomáš Sláčik\\
  Vašek Horčic\\
  Eduard Paclík

  \vspace{1.5cm}

  {\small Akademický rok 2025/2026}
  \vspace*{0.5cm}
\end{center}

\end{document}
```

- [ ] **Step 2: Build a ověř výstup**

Run:
```bash
cd /Users/tomas/projects/rst/pdf
pdflatex -interaction=nonstopmode titlepage.tex
pdfinfo titlepage.pdf | awk '/^Pages|^Page size/'
```
Expected:
```
Pages:           1
Page size:       595.276 x 841.89 pts (A4)
```

Pokud `pdflatex` skončí chybou, oprav `titlepage.tex` (typicky chybějící balíček nebo špatný UTF-8). LaTeX log v `titlepage.log`.

---

### Task 3: Napsat build.sh

**Files:**
- Create: `/Users/tomas/projects/rst/pdf/build.sh`

- [ ] **Step 1: Vytvoř skript**

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Backup originálu při prvním spuštění
[ -f merged_orig.pdf ] || cp merged.pdf merged_orig.pdf

# Build titulky
pdflatex -interaction=nonstopmode titlepage.tex >/dev/null

# Merge titulka + originál → přepsat merged.pdf
pdfunite titlepage.pdf merged_orig.pdf merged.pdf

PAGES=$(pdfinfo merged.pdf | awk '/^Pages/ {print $2}')
echo "Done. merged.pdf = titlepage + merged_orig.pdf (${PAGES} stran)"
```

- [ ] **Step 2: Spustitelnost**

Run:
```bash
chmod +x /Users/tomas/projects/rst/pdf/build.sh
```
Expected: exit 0.

---

### Task 4: První build a verifikace

**Files:**
- Modify: `/Users/tomas/projects/rst/pdf/merged.pdf` (přepis — titulka + originál)
- Create: `/Users/tomas/projects/rst/pdf/titlepage.pdf` (build artifact)
- Create: `/Users/tomas/projects/rst/pdf/titlepage.aux` (LaTeX aux, ignorováno gitem)
- Create: `/Users/tomas/projects/rst/pdf/titlepage.log` (LaTeX log, ignorováno gitem)

- [ ] **Step 1: Spusť build**

Run:
```bash
cd /Users/tomas/projects/rst/pdf
bash build.sh
```
Expected: výstup `Done. merged.pdf = titlepage + merged_orig.pdf (19 stran)`, exit 0.

- [ ] **Step 2: Ověř počet stran výstupu**

Run:
```bash
pdfinfo /Users/tomas/projects/rst/pdf/merged.pdf | awk '/^Pages/ {print $2}'
```
Expected: `19`

- [ ] **Step 3: Ověř backup je netknutý**

Run:
```bash
pdfinfo /Users/tomas/projects/rst/pdf/merged_orig.pdf | awk '/^Pages/ {print $2}'
```
Expected: `18`

- [ ] **Step 4: Idempotence — spusť build podruhé**

Run:
```bash
cd /Users/tomas/projects/rst/pdf
bash build.sh
pdfinfo merged.pdf | awk '/^Pages/ {print $2}'
pdfinfo merged_orig.pdf | awk '/^Pages/ {print $2}'
```
Expected: výstup buildu hlásí 19 stran, `merged.pdf` má 19 stran, `merged_orig.pdf` stále 18 stran (nepřepsán).

- [ ] **Step 5: Vizuální kontrola**

Run:
```bash
open /Users/tomas/projects/rst/pdf/merged.pdf
```
Vizuálně ověř v Preview/PDF.js:
- Strana 1 = titulka (VUT FSI, ÚLOHY E, tým, akademický rok 2025/2026)
- Strana 2 = původní strana 1 z `merged_orig.pdf`
- Layout odpovídá specifikaci ([`docs/superpowers/specs/2026-05-05-titulka-merged-pdf-design.md`](../specs/2026-05-05-titulka-merged-pdf-design.md))

Pokud vizuál nesedí (např. překryvy, špatné zalomení, chybějící diakritika), oprav `titlepage.tex` a opakuj Task 4.

---

### Task 5: Commit zdrojů

**Files:**
- Add: `pdf/titlepage.tex`, `pdf/build.sh`

PDFs (`merged.pdf`, `merged_orig.pdf`, `titlepage.pdf`) **necommitovat** — binární artefakty regenerovatelné z `build.sh` a tracked spec/skriptu.

- [ ] **Step 1: Stage zdroje**

Run:
```bash
cd /Users/tomas/Projects/RST
git add pdf/titlepage.tex pdf/build.sh
git status --short pdf/
```
Expected: `A  pdf/titlepage.tex`, `A  pdf/build.sh`, případně untracked PDFs (`?? pdf/merged.pdf` atd. — ignorovat).

- [ ] **Step 2: Commit**

Run:
```bash
git commit -m "feat(titulka): standalone titlepage prepend for merged.pdf

Generates single-page A4 titulka via pdflatex and prepends to existing
merged.pdf (souborné řešení Úloh E) using pdfunite. Backup originálu
saved to merged_orig.pdf on first build.

See docs/superpowers/specs/2026-05-05-titulka-merged-pdf-design.md."
```
Expected: nový commit, exit 0.

- [ ] **Step 3: Ověř git status čistý (kromě untracked PDFs a aux)**

Run:
```bash
git status --short
```
Expected: žádné staged/modified soubory; untracked PDFs a `.aux`/`.log` v `pdf/` jsou OK (LaTeX aux v `.gitignore`, PDFs explicitně netrackované).

---

## Spec coverage

| Spec sekce | Task |
|---|---|
| Backup originálu (`merged_orig.pdf`) | Task 1 |
| Obsah + layout titulky | Task 2 |
| Build skript | Task 3 |
| Verifikace (19 stran, A4, vizuál) | Task 4 |
| Idempotence backupu | Task 4 step 4 |
| Out-of-scope (logo, header/footer, čísl. skupiny) | respektováno — žádný task |
| Závislosti (pdflatex, pdfunite) | předpokládáno; Task 4 by selhal pokud chybí |
