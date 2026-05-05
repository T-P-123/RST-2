# Spec: Sjednocená závěrečná zpráva — Úlohy E

**Datum:** 2026-05-05
**Téma:** Sloučení 5 samostatných LaTeX dokumentů (`priklad{1..5}.zip`) do jednoho uceleného PDF s jednotnou titulní stranou.
**Repo:** `/Users/tomas/Projects/RST`

---

## 1. Cíl

Vytvořit jedno PDF (`reseni_E.pdf`) obsahující všech 5 vyřešených příkladů (1E–5E) s jednotnou titulní stranou a obsahem (TOC). Obsahová stránka jednotlivých příkladů (text, rovnice, výsledky, obrázky) zůstává **beze změny** — sjednocují se pouze formátovací prvky (preambule, nadpisy, číslování stran).

## 2. Vstupy

5 samostatných ZIP balíčků v `/Users/tomas/Projects/RST/priklady/`:

| Soubor | Obsah |
|--------|-------|
| `priklad1.zip` | `main.tex`, `qq_plot.png`, `qq_grafy.png` |
| `priklad2.zip` | `main.tex`, `histo.{png,svg,pdf}`, `priklad_2E_profil.png`, `priklad_2E_histogramy.png`, `size.png`, `hustoty.png` |
| `priklad3.zip` | `main.tex`, `01..05_*.png`, `zadani.png`, `04_histogram_max_abs_M.png` |
| `priklad4.zip` | `main.tex`, `priklad_4E_vysledky.png`, `Mises.png`, `U.png` |
| `priklad5.zip` | `priklad_5E/main.tex` (vnořeno!), `priklad_5E_zadani.png`, `priklad_5E_vysledky.png`, `priklad_5E_haigh.png`, `peterson.png`, `peterson1.png` |

**Stávající styly** (zdroj nejednotnosti):
- p1, p3 používají `\section*{...}` (nečíslováno, nejde do TOC)
- p2, p4, p5 používají `\section{...}` (číslováno) + vlastní `\title{}\maketitle`
- Každý má jinou preambuli (geometry, balíčky)

## 3. Výstup

```
/Users/tomas/Projects/RST/priklady/reseni_E/
├── main.tex             ← master (preambule + titulka + TOC + 5× \input)
├── priklad1.tex         ← tělo 1E (bez preambule)
├── priklad2.tex         ← tělo 2E
├── priklad3.tex         ← tělo 3E
├── priklad4.tex         ← tělo 4E
├── priklad5.tex         ← tělo 5E
├── img/                 ← všechny obrázky s prefixem pN_
│   └── ...
└── reseni_E.pdf         ← finální PDF (po `pdflatex × 2`)
```

Zdrojové zipy zůstanou nedotčené v `priklady/`.

## 4. Architektura

### 4.1 Master `main.tex`

Obsahuje:
1. `\documentclass[a4paper,11pt]{article}`
2. **Sjednocenou preambuli** = sjednocení balíčků z p2/p4/p5 (nejbohatší sada): `inputenc, fontenc, babel-czech, lmodern, amsmath, amssymb, amsfonts, graphicx, geometry (margin=2.2cm), float, booktabs, array, multirow, caption, subcaption, enumitem, fancyhdr, xcolor, hyperref`
3. `\graphicspath{{img/}}`
4. `\hypersetup` s metadaty PDF
5. `\pagestyle{fancy}` se záhlavím:
   - L: "Spolehlivost konstrukcí -- Úlohy E"
   - R: `\leftmark` (jméno aktuální sekce)
   - C (foot): `\thepage`
6. Vlastní příkaz `\unit{X}` (vyjmuto z fragmentů, definováno centrálně)
7. **Titulní stranu** (`titlepage` env): VUT FSI, Ústav mechaniky těles, mechatroniky a biomechaniky / Spolehlivost konstrukcí / Závěrečná zpráva — Úlohy E / Akademický rok 2025/2026 / Tým: Pavlíček, Sláčik, Horčic, Paclík / Brno, 2026
8. `\tableofcontents \clearpage`
9. 5× `\input{prikladN} \clearpage`
10. `\end{document}`

### 4.2 Fragmenty `prikladN.tex`

Každý fragment obsahuje **pouze tělo** (text, rovnice, obrázky, vnořené sekce). Začíná `\section{Příklad NE -- nazev}`. Žádný `\documentclass`, `\usepackage`, `\begin{document}`, `\title`, `\maketitle`.

## 5. Transformační recept (pro každý příklad)

| Akce | Cíl |
|------|-----|
| **Smazat preambuli** | `\documentclass`, vše `\usepackage`, `\geometry`, `\hypersetup`, `\pagestyle`, `\fancyhf`, `\renewcommand{\headrulewidth}`, `\setlength{\parindent\|parskip}`, `\captionsetup` |
| **Smazat title** | `\title{}`, `\author{}`, `\date{}`, `\maketitle`, `\thispagestyle`, `\tableofcontents`, `\newpage` (uvnitř příkladu) |
| **Smazat dokument env** | `\begin{document}`, `\end{document}` |
| **Smazat duplikátní příkazy** | `\newcommand{\unit}` (definováno v master) |
| **Přidat hlavní nadpis** | `\section{Příklad NE -- nazev}` na začátek fragmentu |
| **Sjednotit podsekce** | u p1, p3: `\section*{X}` → `\subsection*{X}` |
| **Smazat staré nadpisové bloky** | u p1, p3: úvodní `\begin{center}{\Large\textbf{...}}\end{center}` (nahrazeno `\section`) |
| **Přesměrovat obrázky** | `\includegraphics{X.png}` → `\includegraphics{pN_X.png}` (graphicspath = `img/`) |

### 5.1 Specifika podle příkladu

**priklad1.tex** (zdroj `priklad1.zip/main.tex`)
- Smazat: úvodní `\begin{center}` blok s nadpisem
- 6× `\section*` → `\subsection*` (Předpoklad výpočtu, Kontrola normality, Výpočet indexu spolehlivosti, Výpočet pravděpodobnosti, Závěr, …)
- Přidat: `\section{Příklad 1E -- Výpočet pravděpodobnosti bezporuchového provozu}`
- Obrázky: `qq_plot.png`→`p1_qq_plot.png`, `qq_grafy.png`→`p1_qq_grafy.png`

**priklad2.tex** (z `priklad2.zip/main.tex`)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 2E -- Osový kvadratický moment nesymetrického průřezu}` zachovat
- Obrázky → prefix `p2_`: `histo.{png,svg,pdf}`, `priklad_2E_profil.png`, `priklad_2E_histogramy.png`, `size.png`, `hustoty.png`

**priklad3.tex** (z `priklad3.zip/main.tex`)
- 4× `\section*{…}` → `\subsection*{…}` (Zadání, Stochastické vyhodnocení, Výsledky, Závěr)
- Smazat úvodní centered nadpisový blok (pokud je); přidat `\section{Příklad 3E -- Stochastický průběh vnitřních sil}`
- Obrázky → prefix `p3_`: `01_…`, `02_…`, `03_…`, `04_…`, `05_…`, `zadani.png`

**priklad4.tex** (z `priklad4.zip/main.tex`)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 4E -- MS pružnosti a deformace stupňovitého prutu}` zachovat
- Obrázky → prefix `p4_`: `priklad_4E_vysledky.png`, `Mises.png`, `U.png`

**priklad5.tex** (z `priklad5.zip/priklad_5E/main.tex` — pozor, vnořeno!)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 5E -- ...}` zachovat
- Obrázky → prefix `p5_`: `priklad_5E_zadani.png`, `priklad_5E_vysledky.png`, `priklad_5E_haigh.png`, `peterson.png`, `peterson1.png`

## 6. Build & verifikace

**Build:**
```bash
cd /Users/tomas/Projects/RST/priklady/reseni_E/
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex   # 2× kvůli TOC + odkazům
mv main.pdf reseni_E.pdf
```

**Akceptační kritéria:**
- ✅ `main.log` neobsahuje `! LaTeX Error` ani `! Undefined control sequence`
- ✅ PDF má 1 titulní stranu + 1 stranu obsahu + 5 příkladů, každý začíná na nové straně
- ✅ Obsah obsahuje 5 očíslovaných položek (1.–5. Příklad NE)
- ✅ Záhlaví: vlevo "Spolehlivost konstrukcí -- Úlohy E", vpravo název aktuálního příkladu, dole číslo strany
- ✅ Žádné `??` v textu (=špatná reference)
- ✅ Všechny obrázky se zobrazí (vizuální kontrola)
- ✅ Hodnoty, rovnice a výsledky **se neliší** od původních PDF v zipech

**Cleanup:** smazat `.aux .log .toc .out` po úspěšném buildu.

## 7. Rizika

| Riziko | Opatření |
|--------|----------|
| Duplikátní `\newcommand` napříč fragmenty | Vyhodit z fragmentů, definovat jen v master. |
| Chyba kompilace v některém příkladu | Lokalizovat přes řádek v `.log`, opravit, znovu build. Iterace per priklad. |
| Obrázek nenalezen | Po editaci grep `\includegraphics`, ověřit existenci v `img/`. |
| Zip5 vnořený (`priklad_5E/main.tex`) | Ošetřit při kopírování. |
| Konflikty `\section{Příklad NE}` název | Použít jednotnou šablonu z analyzovaných souborů (viz 5.1). |

## 8. Mimo rozsah

- Změny obsahu (text, výpočty, hodnoty, závěry)
- Refactoring Python skriptů v `solutions/`
- Aktualizace `solutions/reseni_E.tex` (zůstane jako historický artefakt)
- Verzování / CI

## 9. Plán implementace (předběžné kroky)

1. Vytvořit `priklady/reseni_E/` + `priklady/reseni_E/img/`
2. Rozbalit 5 zipů do tempu
3. Zkopírovat obrázky s prefixy do `img/`
4. Pro každý příklad: `cp main.tex prikladN.tex`, aplikovat řezy
5. Napsat master `main.tex`
6. Build × 2, parsovat log
7. Vizuální kontrola PDF
8. Cleanup mezisouborů
9. Commit

(Detailní plán implementace vyrobí writing-plans skill.)
