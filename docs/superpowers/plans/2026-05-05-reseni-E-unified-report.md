# Sjednocená závěrečná zpráva (Úlohy E) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sloučit 5 samostatných LaTeX dokumentů (`/Users/tomas/Projects/RST/priklady/priklad{1..5}.zip`) do jediného PDF (`reseni_E.pdf`) s jednotnou titulní stranou, obsahem (TOC) a konzistentním číslováním sekcí. Obsahová stránka jednotlivých příkladů (text, rovnice, výsledky) zůstává **beze změny** — sjednocují se pouze formátovací prvky.

**Architecture:** Master `main.tex` v `/Users/tomas/Projects/RST/priklady/reseni_E/` obsahuje sjednocenou preambuli, titulní stranu, TOC a 5× `\input{prikladN}`. Každý fragment `prikladN.tex` obsahuje pouze tělo (bez `\documentclass`, `\begin{document}`). Akademické pořadí 1E→2E→3E→4E→5E (zip-názvy NEodpovídají!).

**Tech Stack:** LaTeX (pdflatex z TeX Live / MacTeX), `article` třída, balíčky: `babel-czech, lmodern, amsmath, amssymb, amsfonts, graphicx, geometry, float, booktabs, array, multirow, caption, subcaption, enumitem, fancyhdr, xcolor, hyperref`.

**Source-zip mapping (kritické!):**

| Akademické číslo | Zdrojový zip | Téma |
|------------------|--------------|------|
| 1E | `priklad3.zip` | Stochastické vyhodnocení vnitřních účinků nosníku |
| 2E | `priklad2.zip` | Osový kvadratický moment nesymetrického průřezu |
| 3E | `priklad1.zip` | Pravděpodobnost bezporuchového provozu klínových řemenů |
| 4E | `priklad4.zip` | MS pružnosti a deformace stupňovitého prutu |
| 5E | `priklad5.zip` | Časový průběh napětí ve vrubech |

**Kontextové soubory:**
- Spec: `/Users/tomas/Projects/RST/docs/superpowers/specs/2026-05-05-reseni-E-unified-report-design.md`
- Zdrojové zipy: `/Users/tomas/Projects/RST/priklady/priklad{1..5}.zip`
- Pracovní adresář: `/Users/tomas/Projects/RST/priklady/reseni_E/` (vznikne během Task 1)

---

## Task 1: Příprava adresářové struktury a rozbalení zipů

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/`
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/img/`
- Read-only: `/Users/tomas/Projects/RST/priklady/priklad{1..5}.zip`
- Temp: `/tmp/rst_merge/p{1..5}/` (pro rozbalení)

- [ ] **Step 1: Vytvořit cílový adresář a `img/` podsložku**

```bash
mkdir -p /Users/tomas/Projects/RST/priklady/reseni_E/img
```

Expected: žádný výstup, oba adresáře existují.

- [ ] **Step 2: Vytvořit temp adresáře a rozbalit všech 5 zipů**

```bash
rm -rf /tmp/rst_merge && mkdir -p /tmp/rst_merge
for n in 1 2 3 4 5; do
  mkdir -p /tmp/rst_merge/p$n
  unzip -q /Users/tomas/Projects/RST/priklady/priklad$n.zip -d /tmp/rst_merge/p$n
done
```

Expected: bez chyb. Každý `/tmp/rst_merge/pN/` obsahuje `main.tex` + obrázky. Pozor — `p5/` má vnořený `priklad_5E/` podadresář (zip5 není flat).

- [ ] **Step 3: Verifikace rozbalení**

```bash
ls /tmp/rst_merge/p1/ /tmp/rst_merge/p2/ /tmp/rst_merge/p3/ /tmp/rst_merge/p4/ /tmp/rst_merge/p5/priklad_5E/
test -f /tmp/rst_merge/p1/main.tex && \
test -f /tmp/rst_merge/p2/main.tex && \
test -f /tmp/rst_merge/p3/main.tex && \
test -f /tmp/rst_merge/p4/main.tex && \
test -f /tmp/rst_merge/p5/priklad_5E/main.tex && echo "ALL OK"
```

Expected: `ALL OK` na konci. Soubory `main.tex` přítomny ve všech 5 lokacích.

---

## Task 2: Kopírování obrázků s akademickým prefixem do `img/`

**Files:**
- Create (kopie): `/Users/tomas/Projects/RST/priklady/reseni_E/img/p{1..5}_*.png`

**Pozor:** Prefix `pN_` odpovídá **akademickému** číslu (1E–5E), ne názvu zipu. Tj. obrázky z `priklad3.zip` (=1E) dostanou prefix `p1_`.

- [ ] **Step 1: Zkopírovat obrázky pro 1E (zdroj: p3)**

```bash
cd /tmp/rst_merge/p3
cp 01_deterministicke_prubehy.png       /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_01_deterministicke_prubehy.png
cp 02_stochasticky_prubeh_T.png         /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_02_stochasticky_prubeh_T.png
cp 03_stochasticky_prubeh_M.png         /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_03_stochasticky_prubeh_M.png
cp 04_histogramy.png                    /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_04_histogramy.png
cp 04_histogram_max_abs_M.png           /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_04_histogram_max_abs_M.png
cp 05_rozdil_normalni_lognormalni.png   /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_05_rozdil_normalni_lognormalni.png
cp zadani.png                            /Users/tomas/Projects/RST/priklady/reseni_E/img/p1_zadani.png
```

Expected: bez chyb, 7 souborů zkopírováno.

- [ ] **Step 2: Zkopírovat obrázky pro 2E (zdroj: p2)**

```bash
cd /tmp/rst_merge/p2
cp histo.png                       /Users/tomas/Projects/RST/priklady/reseni_E/img/p2_histo.png
cp priklad_2E_profil.png           /Users/tomas/Projects/RST/priklady/reseni_E/img/p2_priklad_2E_profil.png
cp priklad_2E_histogramy.png       /Users/tomas/Projects/RST/priklady/reseni_E/img/p2_priklad_2E_histogramy.png
cp size.png                        /Users/tomas/Projects/RST/priklady/reseni_E/img/p2_size.png
cp hustoty.png                     /Users/tomas/Projects/RST/priklady/reseni_E/img/p2_hustoty.png
```

Poznámka: `histo.svg` a `histo.pdf` se NEKOPÍRUJÍ — `main.tex` p2 odkazuje pouze na `histo.png`.

Expected: 5 souborů zkopírováno.

- [ ] **Step 3: Zkopírovat obrázky pro 3E (zdroj: p1)**

```bash
cd /tmp/rst_merge/p1
cp qq_plot.png    /Users/tomas/Projects/RST/priklady/reseni_E/img/p3_qq_plot.png
cp qq_grafy.png   /Users/tomas/Projects/RST/priklady/reseni_E/img/p3_qq_grafy.png
```

Expected: 2 soubory.

- [ ] **Step 4: Zkopírovat obrázky pro 4E (zdroj: p4)**

```bash
cd /tmp/rst_merge/p4
cp priklad_4E_vysledky.png   /Users/tomas/Projects/RST/priklady/reseni_E/img/p4_priklad_4E_vysledky.png
cp Mises.png                  /Users/tomas/Projects/RST/priklady/reseni_E/img/p4_Mises.png
cp U.png                      /Users/tomas/Projects/RST/priklady/reseni_E/img/p4_U.png
```

Expected: 3 soubory.

- [ ] **Step 5: Zkopírovat obrázky pro 5E (zdroj: p5/priklad_5E)**

```bash
cd /tmp/rst_merge/p5/priklad_5E
cp priklad_5E_zadani.png      /Users/tomas/Projects/RST/priklady/reseni_E/img/p5_priklad_5E_zadani.png
cp priklad_5E_vysledky.png    /Users/tomas/Projects/RST/priklady/reseni_E/img/p5_priklad_5E_vysledky.png
cp priklad_5E_haigh.png       /Users/tomas/Projects/RST/priklady/reseni_E/img/p5_priklad_5E_haigh.png
cp peterson.png               /Users/tomas/Projects/RST/priklady/reseni_E/img/p5_peterson.png
cp peterson1.png              /Users/tomas/Projects/RST/priklady/reseni_E/img/p5_peterson1.png
```

Expected: 5 souborů.

- [ ] **Step 6: Verifikace celkového počtu obrázků**

```bash
ls /Users/tomas/Projects/RST/priklady/reseni_E/img/ | wc -l
```

Expected: `22` (7 + 5 + 2 + 3 + 5).

---

## Task 3: Vytvoření master `main.tex` (preambule + titulka + TOC + \input)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/main.tex`

Tento soubor obsahuje pouze preambuli, titulní stranu, TOC a 5× `\input{prikladN}`. Jednotlivé fragmenty `prikladN.tex` se vytvoří v Task 4-8.

- [ ] **Step 1: Napsat master main.tex**

```latex
\documentclass[a4paper,11pt]{article}

% --- Kódování a jazyk ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{lmodern}

% --- Matematika ---
\usepackage{amsmath,amssymb,amsfonts}

% --- Grafika a layout ---
\usepackage{graphicx}
\usepackage[margin=2.2cm]{geometry}
\usepackage{float}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{hyperref}

\graphicspath{{img/}}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!60!black,
    citecolor=blue!60!black,
    urlcolor=blue!60!black,
    pdftitle={Spolehlivost konstrukcí - Úlohy E},
    pdfauthor={Pavlíček, Sláčik, Horčic, Paclík}
}

% --- Záhlaví / zápatí ---
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Spolehlivost konstrukcí -- Úlohy E}
\fancyhead[R]{\small \leftmark}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% --- Vlastní příkazy (sjednoceně z původních fragmentů) ---
\newcommand{\unit}[1]{\,\mathrm{#1}}
\newcommand{\E}[1]{\times 10^{#1}}

\begin{document}

% =========================================================
%                    TITULNÍ STRANA
% =========================================================
\begin{titlepage}
    \centering
    \vspace*{1.5cm}
    {\large Vysoké učení technické v Brně\par}
    {\large Fakulta strojního inženýrství\par}
    {\large Ústav mechaniky těles, mechatroniky a biomechaniky\par}
    \vspace{3cm}

    {\Huge\bfseries Spolehlivost konstrukcí\par}
    \vspace{0.8cm}
    {\LARGE Závěrečná zpráva -- Úlohy E\par}
    \vspace{0.5cm}
    {\large Akademický rok 2025/2026\par}

    \vspace{3cm}
    {\large\bfseries Tým:\par}
    \vspace{0.4cm}
    {\large
        Tomáš Pavlíček\\[2pt]
        Tomáš Sláčik\\[2pt]
        Vašek Horčic\\[2pt]
        Eduard Paclík\par
    }

    \vfill
    {\large Brno, 2026\par}
\end{titlepage}

\tableofcontents
\clearpage

\input{priklad1}
\clearpage
\input{priklad2}
\clearpage
\input{priklad3}
\clearpage
\input{priklad4}
\clearpage
\input{priklad5}

\end{document}
```

Použij `Write` tool na `/Users/tomas/Projects/RST/priklady/reseni_E/main.tex` s přesným obsahem výše.

- [ ] **Step 2: Sanity check master souboru — zatím nebude kompilovat (chybí prikladN.tex)**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Error|Cannot" | head -5
```

Expected: chyby typu `LaTeX Error: File 'priklad1' not found.` (5×). To je v pořádku — fragmenty zatím neexistují. Důležité: žádná chyba v preambuli ani titulce. Pokud je chyba JINÉHO typu (např. `! Undefined control sequence`), oprav preambuli.

- [ ] **Step 3: Commit master souboru**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/main.tex priklady/priklad4.zip
git commit -m "feat(reseni_E): add master main.tex with title page and TOC"
```

Expected: commit vytvořen. (`priklad4.zip` byl přidán dříve mimo plán, vezmeme ho s sebou.)

---

## Task 4: Fragment `priklad1.tex` (1E — Stochastické vyhodnocení vnitřních účinků nosníku)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/priklad1.tex`
- Source: `/tmp/rst_merge/p3/main.tex` (zip3 = akademicky 1E)

**Transformace:** smazat preambuli (řádky 1-24), úvodní `\begin{center}` titul (ř. 26-31), `\end{document}` (ř. 153). Přidat `\section{...}`. Přepsat 4× `\section*` → `\subsection*`. Přepsat cesty obrázků.

- [ ] **Step 1: Zkopírovat zdroj a zobrazit obsah pro orientaci**

```bash
cp /tmp/rst_merge/p3/main.tex /Users/tomas/Projects/RST/priklady/reseni_E/priklad1.tex
wc -l /Users/tomas/Projects/RST/priklady/reseni_E/priklad1.tex
```

Expected: 153 řádků.

- [ ] **Step 2: Smazat preambuli a vstupní hlavičku (řádky 1-32) přes Edit**

Smaž blok od `\documentclass[11pt,a4paper]{article}` (ř. 1) až po `\vspace{-2mm}` (ř. 31) **včetně**, a nahraď ho nadpisem sekce.

Použij `Edit` tool na `/Users/tomas/Projects/RST/priklady/reseni_E/priklad1.tex`:

`old_string`:
```
\documentclass[11pt,a4paper]{article}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{caption}

\geometry{
	left=18mm,
	right=18mm,
	top=16mm,
	bottom=18mm
}

\setlength{\parindent}{0pt}
\setlength{\parskip}{3pt}
\captionsetup{font=small}

\begin{document}

\begin{center}
	{\Large \textbf{Stochastické vyhodnocení vnitřních účinků nosníku}}\\[-1mm]
	{\small Příklad č. 1}
\end{center}

\vspace{-2mm}

\section*{Zadání a výpočtový postup}
```

`new_string`:
```
\section{Příklad 1E -- Stochastické vyhodnocení vnitřních účinků nosníku}

\subsection*{Zadání a výpočtový postup}
```

- [ ] **Step 3: Přepsat zbylé 3× `\section*` → `\subsection*`**

Použij `Edit` 3×:

(a) `\section*{Stochastické vyhodnocení}` → `\subsection*{Stochastické vyhodnocení}`
(b) `\section*{Výsledky}` → `\subsection*{Výsledky}`
(c) `\section*{Závěr}` → `\subsection*{Závěr}`

- [ ] **Step 4: Smazat `\end{document}` na konci**

`old_string`: `\end{document}`
`new_string`: (prázdný)

- [ ] **Step 5: Přepsat cesty obrázků (prefix `p1_`)**

Použij `Edit` 7× (nebo `replace_all` s individuálním názvem):

| Hledat | Nahradit |
|--------|----------|
| `{zadani.png}` | `{p1_zadani.png}` |
| `{01_deterministicke_prubehy.png}` | `{p1_01_deterministicke_prubehy.png}` |
| `{02_stochasticky_prubeh_T.png}` | `{p1_02_stochasticky_prubeh_T.png}` |
| `{03_stochasticky_prubeh_M.png}` | `{p1_03_stochasticky_prubeh_M.png}` |
| `{04_histogram_max_abs_M.png}` | `{p1_04_histogram_max_abs_M.png}` |

Poznámka: `04_histogramy.png` a `05_rozdil_normalni_lognormalni.png` nejsou v p3/main.tex referencovány, ale jsou ve zipu — stačí je mít jen v `img/` (nezáleží).

- [ ] **Step 6: Verifikace — zkompilovat se zatím chybějícími prikladN dál**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Error|Cannot" | head -10
```

Expected: chyby `File 'priklad2' not found.`, `File 'priklad3' not found.` atd. — ale **NE** v `priklad1`. Žádný `! LaTeX Error` ani `! Undefined control sequence` při zpracování `priklad1.tex`.

- [ ] **Step 7: Commit**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/priklad1.tex
git commit -m "feat(reseni_E): add priklad1.tex (1E - vnitřní účinky nosníku)"
```

---

## Task 5: Fragment `priklad2.tex` (2E — Osový kvadratický moment)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/priklad2.tex`
- Source: `/tmp/rst_merge/p2/main.tex` (zip2 = akademicky 2E)

**Transformace:** smazat preambuli (ř. 1-44), `\title…\maketitle\thispagestyle` (ř. 46-58), zachovat `\section{Příklad 2E -- ...}` (ř. 62), smazat `\end{document}` (ř. 198). Přepsat cesty obrázků.

- [ ] **Step 1: Zkopírovat zdroj**

```bash
cp /tmp/rst_merge/p2/main.tex /Users/tomas/Projects/RST/priklady/reseni_E/priklad2.tex
```

- [ ] **Step 2: Smazat preambuli (řádky 1 až 58 = `\documentclass` až `\thispagestyle{fancy}` včetně)**

Použij `Edit` na `/Users/tomas/Projects/RST/priklady/reseni_E/priklad2.tex`:

`old_string`:
```
\documentclass[a4paper,11pt]{article}

% Kódování a jazyk
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{lmodern}

% Matematika
\usepackage{amsmath,amssymb,amsfonts}

% Grafika a layout
\usepackage{graphicx}
\usepackage[margin=2.2cm]{geometry}
\usepackage{float}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!60!black,
    citecolor=blue!60!black,
    urlcolor=blue!60!black
}

% Záhlaví
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small RST -- Řešení příkladu 2E}
\fancyhead[R]{\small Akademický rok 2025/2026}
\fancyfoot[C]{\thepage}

\renewcommand{\headrulewidth}{0.4pt}

% Vlastní příkazy
\newcommand{\unit}[1]{\,\mathrm{#1}}
\newcommand{\E}[1]{\times 10^{#1}}

\title{%
    \vspace{-1cm}
    \textbf{Rizika a spolehlivost technických systémů}\\[0.3cm]
    \Large Řešení příkladu 2E -- Osový kvadratický moment\\[0.2cm]
    \large Akademický rok 2025/2026
}
\author{}
\date{}

\begin{document}
\maketitle
\thispagestyle{fancy}

%% ============================================================
%% PŘÍKLAD 2E
%% ============================================================
\section{Příklad 2E -- Osový kvadratický moment nesymetrického průřezu}
```

`new_string`:
```
\section{Příklad 2E -- Osový kvadratický moment nesymetrického průřezu}
```

- [ ] **Step 3: Smazat `\end{document}` na konci souboru**

`old_string`: `\end{document}`
`new_string`: (prázdný)

- [ ] **Step 4: Přepsat cesty obrázků (prefix `p2_`)**

Použij `Edit` 3×:

| Hledat | Nahradit |
|--------|----------|
| `{size.png}` | `{p2_size.png}` |
| `{histo.png}` | `{p2_histo.png}` |
| `{hustoty.png}` | `{p2_hustoty.png}` |

Poznámka: obrázky `priklad_2E_profil.png` a `priklad_2E_histogramy.png` nejsou v aktuální verzi p2/main.tex referencovány, ale máme je v `img/` (nevadí).

- [ ] **Step 5: Verifikace kompilace**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Error|! " | head -10
```

Expected: chyby `File 'priklad3' not found.`, `File 'priklad4' not found.`, `File 'priklad5' not found.` — ale **NE** v `priklad1` ani `priklad2`. Žádný jiný typ chyby.

- [ ] **Step 6: Commit**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/priklad2.tex
git commit -m "feat(reseni_E): add priklad2.tex (2E - osový kvadratický moment)"
```

---

## Task 6: Fragment `priklad3.tex` (3E — Pravděpodobnost bezporuchového provozu)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/priklad3.tex`
- Source: `/tmp/rst_merge/p1/main.tex` (zip1 = akademicky 3E)

**Transformace:** smazat preambuli (ř. 1-13), úvodní centered titul (ř. 15-22), 5× `\section*` → `\subsection*`, smazat `\end{document}` (ř. 164). Přepsat cesty obrázků (prefix `p3_`).

- [ ] **Step 1: Zkopírovat zdroj**

```bash
cp /tmp/rst_merge/p1/main.tex /Users/tomas/Projects/RST/priklady/reseni_E/priklad3.tex
```

- [ ] **Step 2: Smazat preambuli + úvodní centered blok, nahradit `\section{...}`**

Použij `Edit` na `/Users/tomas/Projects/RST/priklady/reseni_E/priklad3.tex`:

`old_string`:
```
\documentclass[12pt,a4paper]{article}

\usepackage[czech]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{float}
\usepackage{geometry}

\geometry{margin=2.5cm}

\begin{document}


\begin{center}
	{\Large \textbf{Výpočet pravděpodobnosti bezporuchového provozu}}\\[-1mm]
	{\small Příklad č. 3}
\end{center}
```

`new_string`:
```
\section{Příklad 3E -- Výpočet pravděpodobnosti bezporuchového provozu (klínové řemeny)}
```

- [ ] **Step 3: Přepsat 5× `\section*` → `\subsection*`**

Použij `Edit` 5×:

(a) `\section*{Předpoklad výpočtu}` → `\subsection*{Předpoklad výpočtu}`
(b) `\section*{Kontrola normality}` → `\subsection*{Kontrola normality}`
(c) `\section*{Výpočet indexu spolehlivosti}` → `\subsection*{Výpočet indexu spolehlivosti}`
(d) `\section*{Výpočet pravděpodobnosti}` → `\subsection*{Výpočet pravděpodobnosti}`
(e) `\section*{Závěr}` → `\subsection*{Závěr}`

- [ ] **Step 4: Smazat `\end{document}`**

`old_string`: `\end{document}`
`new_string`: (prázdný)

- [ ] **Step 5: Přepsat cestu obrázku (prefix `p3_`)**

Použij `Edit` 1×:

`old_string`: `{qq_grafy.png}`
`new_string`: `{p3_qq_grafy.png}`

Poznámka: `qq_plot.png` ve zipu existuje, ale v textu p1/main.tex není referencován (jen `qq_grafy.png` na ř. 84). Necháváme zkopírovaný v `img/` jako záloha — neškodí.

- [ ] **Step 6: Verifikace kompilace**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Error|! " | head -10
```

Expected: chyby pouze `File 'priklad4' not found.`, `File 'priklad5' not found.`. Žádný jiný typ.

- [ ] **Step 7: Commit**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/priklad3.tex
git commit -m "feat(reseni_E): add priklad3.tex (3E - pravděpodobnost bezporuchového provozu)"
```

---

## Task 7: Fragment `priklad4.tex` (4E — MS pružnosti a deformace stupňovitého prutu)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/priklad4.tex`
- Source: `/tmp/rst_merge/p4/main.tex` (zip4 = akademicky 4E)

**Transformace:** smazat preambuli (ř. 1-58), zachovat `\section{Příklad 4E -- ...}` (ř. 62), smazat `\end{document}` (ř. 285). Přepsat cesty obrázků (prefix `p4_`).

- [ ] **Step 1: Zkopírovat zdroj**

```bash
cp /tmp/rst_merge/p4/main.tex /Users/tomas/Projects/RST/priklady/reseni_E/priklad4.tex
```

- [ ] **Step 2: Smazat preambuli a hlavičku (ř. 1 až 61) — zachovat `\section{...}` na ř. 62**

Použij `Edit` na `/Users/tomas/Projects/RST/priklady/reseni_E/priklad4.tex`:

`old_string`:
```
\documentclass[a4paper,11pt]{article}

% Kódování a jazyk
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{lmodern}

% Matematika
\usepackage{amsmath,amssymb,amsfonts}

% Grafika a layout
\usepackage{graphicx}
\usepackage[margin=2.2cm]{geometry}
\usepackage{float}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!60!black,
    citecolor=blue!60!black,
    urlcolor=blue!60!black
}

% Záhlaví
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small RST -- Řešení příkladu 4E}
\fancyhead[R]{\small Akademický rok 2025/2026}
\fancyfoot[C]{\thepage}

\renewcommand{\headrulewidth}{0.4pt}

% Vlastní příkazy
\newcommand{\unit}[1]{\,\mathrm{#1}}
\newcommand{\E}[1]{\times 10^{#1}}

\title{%
    \vspace{-1cm}
    \textbf{Rizika a spolehlivost technických systémů}\\[0.3cm]
    \Large Řešení příkladu 4E -- MS pružnosti a deformace stupňovitého prutu\\[0.2cm]
    \large Akademický rok 2025/2026
}
\author{}
\date{}

\begin{document}
\maketitle
\thispagestyle{fancy}

%% ============================================================
%% PŘÍKLAD 4E
%% ============================================================
\section{Příklad 4E -- MS pružnosti a deformace stupňovitého prutu}
```

`new_string`:
```
\section{Příklad 4E -- MS pružnosti a deformace stupňovitého prutu}
```

- [ ] **Step 3: Smazat `\end{document}`**

`old_string`: `\end{document}`
`new_string`: (prázdný)

- [ ] **Step 4: Přepsat cesty obrázků (prefix `p4_`)**

Použij `Edit` 3×:

| Hledat | Nahradit |
|--------|----------|
| `{Mises.png}` | `{p4_Mises.png}` |
| `{U.png}` | `{p4_U.png}` |
| `{priklad_4E_vysledky.png}` | `{p4_priklad_4E_vysledky.png}` |

- [ ] **Step 5: Verifikace kompilace**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep -E "Error|! " | head -10
```

Expected: chyba pouze `File 'priklad5' not found.`. Žádný jiný typ.

- [ ] **Step 6: Commit**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/priklad4.tex
git commit -m "feat(reseni_E): add priklad4.tex (4E - MS pružnosti stupňovitého prutu)"
```

---

## Task 8: Fragment `priklad5.tex` (5E — Časový průběh napětí ve vrubech)

**Files:**
- Create: `/Users/tomas/Projects/RST/priklady/reseni_E/priklad5.tex`
- Source: `/tmp/rst_merge/p5/priklad_5E/main.tex` (zip5 = akademicky 5E, **vnořené v podsložce!**)

**Transformace:** smazat preambuli (ř. 1-58), zachovat `\section{Příklad 5E -- ...}` (ř. 62), smazat `\end{document}` (ř. 213). Přepsat cesty obrázků (prefix `p5_`).

- [ ] **Step 1: Zkopírovat zdroj (z vnořené podsložky)**

```bash
cp /tmp/rst_merge/p5/priklad_5E/main.tex /Users/tomas/Projects/RST/priklady/reseni_E/priklad5.tex
```

- [ ] **Step 2: Smazat preambuli a hlavičku (ř. 1 až 61) — zachovat `\section{...}` na ř. 62**

Použij `Edit` na `/Users/tomas/Projects/RST/priklady/reseni_E/priklad5.tex`:

`old_string`:
```
\documentclass[a4paper,11pt]{article}

% Kódování a jazyk
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[czech]{babel}
\usepackage{lmodern}

% Matematika
\usepackage{amsmath,amssymb,amsfonts}

% Grafika a layout
\usepackage{graphicx}
\usepackage[margin=2.2cm]{geometry}
\usepackage{float}
\usepackage{booktabs}
\usepackage{array}
\usepackage{multirow}
\usepackage{caption}
\usepackage{subcaption}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{hyperref}

\hypersetup{
    colorlinks=true,
    linkcolor=blue!60!black,
    citecolor=blue!60!black,
    urlcolor=blue!60!black
}

% Záhlaví
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small RST -- Řešení příkladu 5E}
\fancyhead[R]{\small Akademický rok 2025/2026}
\fancyfoot[C]{\thepage}

\renewcommand{\headrulewidth}{0.4pt}

% Vlastní příkazy
\newcommand{\unit}[1]{\,\mathrm{#1}}
\newcommand{\E}[1]{\times 10^{#1}}

\title{%
    \vspace{-1cm}
    \textbf{Rizika a spolehlivost technických systémů}\\[0.3cm]
    \Large Řešení příkladu 5E -- Časový průběh napětí ve vrubech\\[0.2cm]
    \large Akademický rok 2025/2026
}
\author{}
\date{}

\begin{document}
\maketitle
\thispagestyle{fancy}

%% ============================================================
%% PŘÍKLAD 5E
%% ============================================================
\section{Příklad 5E -- Časový průběh napětí ve vrubech}
```

`new_string`:
```
\section{Příklad 5E -- Časový průběh napětí ve vrubech}
```

- [ ] **Step 3: Smazat `\end{document}`**

`old_string`: `\end{document}`
`new_string`: (prázdný)

- [ ] **Step 4: Přepsat cesty obrázků (prefix `p5_`)**

Použij `Edit` 4×:

| Hledat | Nahradit |
|--------|----------|
| `{priklad_5E_zadani.png}` | `{p5_priklad_5E_zadani.png}` |
| `{priklad_5E_vysledky.png}` | `{p5_priklad_5E_vysledky.png}` |
| `{priklad_5E_haigh.png}` | `{p5_priklad_5E_haigh.png}` |
| `{peterson1.png}` | `{p5_peterson1.png}` |

Poznámka: `peterson.png` (bez čísla) je ve zipu, ale v aktuální verzi p5/main.tex je referencován pouze `peterson1.png` (ř. 141). Necháváme `peterson.png` v `img/` jako rezervu.

- [ ] **Step 5: Verifikace prvního průchodu kompilace (úplná)**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex 2>&1 | tail -30
```

Expected: žádná `! Error`, žádné `Cannot find` u obrázků nebo souborů. Možná varování typu `Overfull \hbox` jsou OK.

- [ ] **Step 6: Commit**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/priklad5.tex
git commit -m "feat(reseni_E): add priklad5.tex (5E - časový průběh napětí ve vrubech)"
```

---

## Task 9: Finální build, kontrola PDF a cleanup

**Files:**
- Output: `/Users/tomas/Projects/RST/priklady/reseni_E/reseni_E.pdf`
- Cleanup: `*.aux *.log *.toc *.out` v `reseni_E/`

- [ ] **Step 1: Spustit pdflatex 2× (kvůli TOC + referencím)**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Expected: oba běhy končí `Output written on main.pdf (X pages, Y bytes).` bez `! Error`.

- [ ] **Step 2: Zkontrolovat log na chyby**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
grep -E "^! |^l\." main.log | head -20
```

Expected: žádný výstup (= žádné `!` chyby v logu). Pokud něco vyleze, oprav ručně.

- [ ] **Step 3: Zkontrolovat varování o nevyřešených referencích**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
grep -E "Reference|undefined|may have changed" main.log | head -10
```

Expected: žádné `Reference ... undefined`. (Hláška `Rerun to get cross-references right` je OK po prvním běhu, neměla by být po druhém.)

- [ ] **Step 4: Přejmenovat výstupní PDF**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
mv main.pdf reseni_E.pdf
ls -la reseni_E.pdf
```

Expected: soubor `reseni_E.pdf` existuje, velikost ≥ 1 MB (kvůli obrázkům).

- [ ] **Step 5: Vizuální kontrola PDF**

```bash
open /Users/tomas/Projects/RST/priklady/reseni_E/reseni_E.pdf
```

Otevře se Preview. Zkontroluj:
1. Titulní strana = VUT FSI, Spolehlivost konstrukcí, Závěrečná zpráva — Úlohy E, akademický rok 2025/2026, 4 jména týmu, Brno 2026
2. Strana 2 = obsah s 5 položkami (1. Příklad 1E, 2. Příklad 2E, …, 5. Příklad 5E)
3. Každý příklad začíná na nové straně
4. Záhlaví: vlevo "Spolehlivost konstrukcí -- Úlohy E", vpravo aktuální sekce
5. Obrázky jsou viditelné (ne broken-image placeholdery)
6. V textu žádné `??` (= špatná reference)

Pokud něco není OK, vrať se k příslušné Task a oprav.

- [ ] **Step 6: Smazat mezisoubory**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
rm -f main.aux main.log main.toc main.out main.pdf
```

Expected: pouze `main.tex priklad{1..5}.tex img/ reseni_E.pdf` zůstanou.

- [ ] **Step 7: Přidat `.gitignore` pro mezisoubory (kvůli budoucím buildům)**

Vytvoř `/Users/tomas/Projects/RST/priklady/reseni_E/.gitignore`:

```
*.aux
*.log
*.toc
*.out
*.fdb_latexmk
*.fls
*.synctex.gz
main.pdf
```

Použij `Write` tool na `/Users/tomas/Projects/RST/priklady/reseni_E/.gitignore` s obsahem výše.

- [ ] **Step 8: Commit finálního PDF + .gitignore**

```bash
cd /Users/tomas/Projects/RST
git add priklady/reseni_E/.gitignore priklady/reseni_E/reseni_E.pdf
git commit -m "feat(reseni_E): build final unified report PDF"
```

Expected: commit s 2 přidanými soubory.

---

## Task 10: Závěrečná verifikace + úklid temp

**Files:**
- Cleanup: `/tmp/rst_merge/`

- [ ] **Step 1: Smazat temp adresář**

```bash
rm -rf /tmp/rst_merge
```

Expected: bez chyb.

- [ ] **Step 2: Final tree check**

```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E
ls -la
echo "---"
ls img/ | wc -l
```

Expected:
- `main.tex priklad1.tex priklad2.tex priklad3.tex priklad4.tex priklad5.tex img/ reseni_E.pdf .gitignore`
- `img/` obsahuje **22 souborů**

- [ ] **Step 3: Git log review**

```bash
cd /Users/tomas/Projects/RST
git log --oneline -10
```

Expected: 7 nových commitů (`feat(reseni_E): ...`) + 2 starší (`docs(reseni_E): ...` ze spec fáze).

- [ ] **Step 4: Hotovo**

Závěrečná zpráva je v `/Users/tomas/Projects/RST/priklady/reseni_E/reseni_E.pdf`. Zdrojové zipy v `priklady/priklad{1..5}.zip` zůstaly nedotčené.

---

## Akceptační kritéria celého plánu

- ✅ `reseni_E.pdf` existuje, otevře se v Preview
- ✅ 1 titulní strana s VUT FSI + jména týmu
- ✅ 1 strana s obsahem (TOC) — 5 očíslovaných položek 1E–5E v akademickém pořadí
- ✅ 5 příkladů, každý na nové straně, s vlastním `\section`
- ✅ Záhlaví ukazuje aktuální sekci, dole číslo strany
- ✅ Všechny obrázky se zobrazí (vizuální check)
- ✅ Žádné `??` v textu, `main.log` čistý od `! Error`
- ✅ Hodnoty/rovnice/výsledky beze změny vůči zdrojovým zipům
- ✅ Zdrojové zipy v `priklady/` nedotčené
