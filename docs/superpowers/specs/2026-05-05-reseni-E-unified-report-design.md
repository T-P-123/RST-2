# Spec: Sjednocená závěrečná zpráva — Úlohy E

**Datum:** 2026-05-05
**Téma:** Sloučení 5 samostatných LaTeX dokumentů (`priklad{1..5}.zip`) do jednoho uceleného PDF s jednotnou titulní stranou.
**Repo:** `/Users/tomas/Projects/RST`

---

## 1. Cíl

Vytvořit jedno PDF (`reseni_E.pdf`) obsahující všech 5 vyřešených příkladů (1E–5E) s jednotnou titulní stranou a obsahem (TOC). Obsahová stránka jednotlivých příkladů (text, rovnice, výsledky, obrázky) zůstává **beze změny** — sjednocují se pouze formátovací prvky (preambule, nadpisy, číslování stran).

## 2. Vstupy

5 samostatných ZIP balíčků v `/Users/tomas/Projects/RST/priklady/`. **Pozor:** pojmenování zipů NEodpovídá akademickému pořadí. Skutečné mapování zip → E-číslo:

| Soubor | Obsah | Akademické číslo |
|--------|-------|------------------|
| `priklad1.zip` | `main.tex`, `qq_plot.png`, `qq_grafy.png` (pravděpodobnost bezporuchového provozu, klínové řemeny) | **3E** |
| `priklad2.zip` | `main.tex`, `histo.{png,svg,pdf}`, `priklad_2E_profil.png`, `priklad_2E_histogramy.png`, `size.png`, `hustoty.png` | **2E** |
| `priklad3.zip` | `main.tex`, `01..05_*.png`, `zadani.png`, `04_histogram_max_abs_M.png` (stoch. vyhodnocení vnitřních účinků nosníku) | **1E** |
| `priklad4.zip` | `main.tex`, `priklad_4E_vysledky.png`, `Mises.png`, `U.png` | **4E** |
| `priklad5.zip` | `priklad_5E/main.tex` (vnořeno!), `priklad_5E_zadani.png`, `priklad_5E_vysledky.png`, `priklad_5E_haigh.png`, `peterson.png`, `peterson1.png` | **5E** |

Finální zpráva použije **akademické pořadí 1E → 2E → 3E → 4E → 5E**.

**Stávající styly** (zdroj nejednotnosti):
- p1, p3 používají `\section*{...}` (nečíslováno, nejde do TOC)
- p2, p4, p5 používají `\section{...}` (číslováno) + vlastní `\title{}\maketitle`
- Každý má jinou preambuli (geometry, balíčky)

## 3. Výstup

```
/Users/tomas/Projects/RST/priklady/reseni_E/
├── main.tex             ← master (preambule + titulka + TOC + 5× \input)
├── priklad1.tex         ← tělo 1E (zdroj: priklad3.zip) — bez preambule
├── priklad2.tex         ← tělo 2E (zdroj: priklad2.zip)
├── priklad3.tex         ← tělo 3E (zdroj: priklad1.zip)
├── priklad4.tex         ← tělo 4E (zdroj: priklad4.zip)
├── priklad5.tex         ← tělo 5E (zdroj: priklad5.zip)
├── img/                 ← všechny obrázky s prefixem pN_ (N = akademické číslo!)
│   └── ...
└── reseni_E.pdf         ← finální PDF (po `pdflatex × 2`)
```

**Pozor na prefix obrázků:** prefix `pN_` odpovídá **akademickému** číslu (1E–5E), ne názvu zipu. Tj. obrázky z `priklad3.zip` (=1E) dostanou prefix `p1_`, obrázky z `priklad1.zip` (=3E) dostanou prefix `p3_`.

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

**priklad1.tex** = příklad **1E** (zdroj: `priklad3.zip/main.tex`)
- Smazat: úvodní `\begin{center}{\Large\textbf{Stochastické vyhodnocení vnitřních účinků nosníku}}\\{\small Příklad č. 1}\end{center}` blok
- 4× `\section*` → `\subsection*` (Zadání a výpočtový postup, Stochastické vyhodnocení, Výsledky, Závěr)
- Přidat: `\section{Příklad 1E -- Stochastické vyhodnocení vnitřních účinků nosníku}`
- Obrázky → prefix `p1_`: `01_deterministicke_prubehy.png`, `02_stochasticky_prubeh_T.png`, `03_stochasticky_prubeh_M.png`, `04_histogramy.png`, `04_histogram_max_abs_M.png`, `05_rozdil_normalni_lognormalni.png`, `zadani.png`

**priklad2.tex** = příklad **2E** (zdroj: `priklad2.zip/main.tex`)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 2E -- Osový kvadratický moment nesymetrického průřezu}` zachovat
- Obrázky → prefix `p2_`: `histo.png` (preferovat .png před .pdf/.svg), `priklad_2E_profil.png`, `priklad_2E_histogramy.png`, `size.png`, `hustoty.png`

**priklad3.tex** = příklad **3E** (zdroj: `priklad1.zip/main.tex`)
- Smazat úvodní `\begin{center}{\Large\textbf{Výpočet pravděpodobnosti bezporuchového provozu}}\\{\small Příklad č. 3}\end{center}` blok
- 5× `\section*` → `\subsection*` (Předpoklad výpočtu, Kontrola normality, Výpočet indexu spolehlivosti, Výpočet pravděpodobnosti, Závěr)
- Přidat: `\section{Příklad 3E -- Výpočet pravděpodobnosti bezporuchového provozu (klínové řemeny)}`
- Obrázky → prefix `p3_`: `qq_plot.png`, `qq_grafy.png`

**priklad4.tex** = příklad **4E** (zdroj: `priklad4.zip/main.tex`)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 4E -- MS pružnosti a deformace stupňovitého prutu}` zachovat
- Obrázky → prefix `p4_`: `priklad_4E_vysledky.png`, `Mises.png`, `U.png`

**priklad5.tex** = příklad **5E** (zdroj: `priklad5.zip/priklad_5E/main.tex` — pozor, vnořeno v podsložce!)
- Smazat: `\title…\maketitle\thispagestyle\tableofcontents\newpage`
- `\section{Příklad 5E -- Časový průběh napětí ve vrubech}` zachovat
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
2. Rozbalit 5 zipů do tempu (např. `/tmp/rst_merge/p{1..5}/`)
3. Zkopírovat obrázky s prefixy odpovídajícími **akademickému** číslu (p3_zadani.png ze zipu1, atd.) do `img/`
4. Pro každý akademický příklad: `cp <zdrojový-zip>/main.tex prikladN.tex`, aplikovat řezy podle 5.1
5. Napsat master `main.tex` s preambulí, titulkou, TOC a 5× `\input{prikladN}` v pořadí 1→5
6. Build × 2 (`pdflatex -interaction=nonstopmode main.tex`), parsovat log na chyby
7. Vizuální kontrola PDF
8. Cleanup mezisouborů (.aux .log .toc .out)
9. Commit do gitu

(Detailní plán implementace vyrobí writing-plans skill.)

(Detailní plán implementace vyrobí writing-plans skill.)
