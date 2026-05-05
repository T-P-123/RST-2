# Titulní strana — Souborné řešení Úloh E

**Datum:** 2026-05-05
**Projekt:** `priklady/reseni_souborne/`
**Kontext:** předmět *Spolehlivost konstrukcí*, VUT FSI, akademický rok 2025/2026.

## Cíl

Nahradit dosavadní jednoduchý `\maketitle` v `priklady/reseni_souborne/main.tex` plnohodnotnou titulní stranou, která splní pokyny:

> Na titulní straně uveďte název školy, předmětu, řešené úlohy, akademický rok, číslo skupiny. Uveďte jména jednotlivých členů týmu.

(Číslo skupiny — vynecháno na základě explicitní instrukce uživatele.)

## Rozhodnuté parametry

| Položka | Hodnota |
|---|---|
| Škola | Vysoké učení technické v Brně |
| Fakulta | Fakulta strojního inženýrství |
| Ústav | Ústav mechaniky těles, mechatroniky a biomechaniky |
| Předmět | Spolehlivost konstrukcí |
| Úloha | Úlohy E (souborné řešení příkladů 1E–5E) |
| Akademický rok | 2025/2026 |
| Tým | Tomáš Pavlíček, Tomáš Sláčik, Vašek Horčic, Eduard Paclík |
| Číslo skupiny | — (vynecháno) |
| Logo | Oficiální VUT logo (stáhnout do `reseni_souborne/logo/`); pokud nedostupné, použít textový fallback |

## Layout (varianta A — Klasický VUT styl)

A4, jedna celostránková `titlepage` před TOC:

```
[VUT logo, šířka ~4 cm, vlevo nahoře]
\rule (horizontal line, full width)

(centered, normal font:)
Vysoké učení technické v Brně
Fakulta strojního inženýrství
Ústav mechaniky těles, mechatroniky a biomechaniky

\vfill

(centered:)
ÚLOHY E                                    (Huge bold)
Souborné řešení příkladů 1E – 5E           (Large)

(centered, italic:)
Spolehlivost konstrukcí                    (large)

\vfill

(centered:)
Členové týmu:                              (bold)
Tomáš Pavlíček
Tomáš Sláčik
Vašek Horčic
Eduard Paclík

Akademický rok 2025/2026                   (small)
```

## Implementační poznámky

1. **Soubor:** `priklady/reseni_souborne/main.tex`
   - Nahradit blok `\title{...}\author{}\date{}` + `\maketitle` celou `titlepage` environmentem.
   - `\begin{titlepage} … \end{titlepage}` automaticky potlačí číslo stránky a vytvoří jednu izolovanou stránku.
2. **Logo:** stáhnout VUT logo (preferovaně PDF nebo vysoké rozlišení PNG) do `priklady/reseni_souborne/logo/vut.pdf` nebo `vut.png`. Vložit přes `\includegraphics[width=4cm]{logo/vut}`. Při neúspěchu stažení použít textový fallback `{\bfseries\Large VUT FSI}` ve stejné pozici.
3. **Hlavička dokumentu:** `\fancyhead[L]{\small Spolehlivost konstrukcí -- Úlohy E}` (drobná úprava, konzistence s předmětem na titulce).
4. **TOC:** zůstává v `\tableofcontents` na další stránce (titulpage automaticky `\clearpage`-ne).

## Postup ověření

1. Build: `pdflatex main.tex` (2× kvůli TOC).
2. Vizuální kontrola titulpage v `main.pdf` — PDF-prohlížeč.
3. Ověřit, že počet stránek roste o 1 (z 19 → 20).

## Out of scope

- Změny obsahu jednotlivých příkladů (1E–5E).
- Stylová změna záhlaví/zápatí mimo `\fancyhead[L]`.
- Číslo skupiny.
- Datum odevzdání nad rámec akademického roku.
