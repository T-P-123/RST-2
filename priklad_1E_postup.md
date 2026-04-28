# Příklad 1E — Detailní postup řešení

**Téma:** Průběh vnitřních sil a momentů na nosníku + stochastická analýza zatížení
**Zdroj:** `solutions/reseni_E.pdf` (sekce 1) a `solutions/priklad_1E.py`

---

## 1. Zadání úlohy

Vykreslete průběh vnitřních sil a momentů po délce prutu. Vnější zatížení uvažujte jako **stochastické** s normálním rozdělením, střední hodnotou dle obrázku a variačním koeficientem $\mathrm{CoV} = 0{,}1$.

### 1.1 Schéma nosníku

| Prvek | Pozice / hodnota | Poznámka |
|-------|------------------|----------|
| Podpora **A** | $x = 0$ | Kloubová (pin) — reakce $F_{Ax}$, $F_{Ay}$ |
| Podpora **B** | $x = 5\ \mathrm{m}$ | Válcová (roller) — reakce $F_{By}$ |
| Moment $M_0$ | $x = 2\ \mathrm{m}$ | $20\ \mathrm{kN \cdot m}$, **CW** (po směru hodinových ručiček) |
| Síla $F$ | $x = 3\ \mathrm{m}$ | $8\ \mathrm{kN}$, směr dolů |
| Spojité zatížení $q$ | $x \in [5;\ 8]\ \mathrm{m}$ | $15\ \mathrm{kN/m}$, směr dolů |
| Délka | $L = 8\ \mathrm{m}$ | $2 + 1 + 2 + 3$, převis 3 m za B |

> **Důležité:** Kolečko v $x = 2\ \mathrm{m}$ je pouze značka místa aplikace momentu — **NE vnitřní kloub**! Bez tohoto rozlišení by úloha byla mechanizmem.

### 1.2 Znaménková konvence

- **$F_y$ kladné nahoru.**
- **$M(x)$:** sagging-positive (prohnutí dolů → $M > 0$). Vzorec:
  $M(x) = \sum F_{y,i}\cdot(x - x_i) - \sum M_{\text{CCW},j}$
- **$V(x)$:** kladná nahoru na **levé** straně řezu.
- **CCW (proti směru hodinových ručiček) — kladný směr** pro momentovou rovnováhu.
- $M_0$ je CW, takže ve $\sum M_A$ vstupuje se **záporným znaménkem**.

---

## 2. Statická určitost

3 neznámé reakce ($F_{Ax}$, $F_{Ay}$, $F_{By}$) ↔ 3 rovnice rovnováhy ($\sum F_x = 0$, $\sum F_y = 0$, $\sum M = 0$).

**Závěr:** Prostě podepřený nosník s převislým koncem, **staticky určitý**.

---

## 3. Deterministické řešení

### 3.1 Náhrada spojitého zatížení výslednicí

Pro výpočet **reakcí** lze $q$ nahradit jednou výslednicí ve svislici jejího těžiště (platí jen pro reakce, ne pro vnitřní průběhy):

$$
F_q = q \cdot L_q = 15 \cdot 3 = 45\ \mathrm{kN}
$$

$$
x_{F_q} = x_{q,\mathrm{start}} + \tfrac{L_q}{2} = 5 + \tfrac{3}{2} = 6{,}5\ \mathrm{m}
$$

kde $L_q = x_{q,\mathrm{end}} - x_{q,\mathrm{start}} = 8 - 5 = 3\ \mathrm{m}$.

### 3.2 Horizontální rovnováha

$$
\sum F_x = 0\ \Rightarrow\ F_{Ax} = 0
$$

(žádné horizontální vnější zatížení)

### 3.3 Momentová rovnováha k bodu A

Sčítáme momenty všech sil **k bodu A** ($x = 0$), CCW kladné:

$$
\sum M_A = 0:\quad -M_0\ -\ F \cdot x_F\ +\ F_{By}\cdot x_B\ -\ F_q \cdot x_{F_q}\ =\ 0
$$

**Rozbor jednotlivých členů:**

| Člen | Hodnota | Znaménko a důvod |
|------|---------|------------------|
| $-M_0$ | $-20\ \mathrm{kN \cdot m}$ | CW moment je v CCW konvenci záporný |
| $-F\cdot x_F$ | $-8 \cdot 3 = -24$ | $F$ směřuje dolů → vůči A způsobuje CW rotaci → záporné |
| $+F_{By}\cdot x_B$ | $+F_{By}\cdot 5$ | $F_{By}$ směřuje nahoru → vůči A CCW → kladné |
| $-F_q \cdot x_{F_q}$ | $-45\cdot 6{,}5 = -292{,}5$ | Výslednice $F_q$ míří dolů → CW → záporné |

Vyjádření $F_{By}$:

$$
F_{By} = \frac{M_0 + F\cdot x_F + F_q \cdot x_{F_q}}{x_B}
       = \frac{20 + 8\cdot 3 + 45\cdot 6{,}5}{5}
       = \frac{20 + 24 + 292{,}5}{5}
       = \frac{336{,}5}{5}
$$

$$
\boxed{F_{By} = 67{,}30\ \mathrm{kN}}
$$

### 3.4 Svislá rovnováha

$$
\sum F_y = 0:\quad F_{Ay} + F_{By} - F - F_q = 0
$$

$$
F_{Ay} = F + F_q - F_{By} = 8 + 45 - 67{,}30
$$

$$
\boxed{F_{Ay} = -14{,}30\ \mathrm{kN}}
$$

**Fyzikální interpretace:** Záporné znaménko znamená, že podpora A skutečně **táhne nosník dolů** (reakce směřuje dolů, opačně než předpoklad). Důvod: převislý konec s velkým spojitým zatížením ($F_q = 45\ \mathrm{kN}$ působící za podporou B) působí jako páka, která zdvíhá levý konec — A musí kompenzovat tahem.

### 3.5 Kontroly

- $\sum F_y$: $-14{,}30 + 67{,}30 - 8 - 45 = 0\ \checkmark$
- $\sum M_B$ (alternativní moment k B):
  $(0 - 5)\cdot F_{Ay} - M_0 + (3 - 5)\cdot(-F) + (6{,}5 - 5)\cdot(-F_q)$
  $= -5\cdot(-14{,}30) - 20 + (-2)\cdot(-8) + 1{,}5\cdot(-45)$
  $= 71{,}5 - 20 + 16 - 67{,}5 = 0\ \checkmark$
- $M(L) = 0$ a $V(L) = 0$ (volný konec) → numerická kontrola v Pythonu vychází.

---

## 4. Vnitřní síly a momenty $V(x)$, $M(x)$

### 4.1 Princip výpočtu

Pro libovolný řez v $x$ uvažujeme **levou část** nosníku a sčítáme:

- $V(x) = \sum F_{y,i}$ — všech svislých sil **nalevo** od řezu
- $M(x) = \sum F_{y,i}\cdot(x - x_i) - \sum M_{\text{CCW},j}$ — momentů těchto sil k řezu plus skoky od koncentrovaných momentů

> **Pozn. ke znaménku $M_0$ ve vnitřních silách:** $M_0$ je CW. V sagging-positive konvenci způsobuje CW koncentrovaný moment **kladný skok** ohybového momentu o $+M_0 = +20\ \mathrm{kN \cdot m}$ v místě aplikace. Proto v kódu (`priklad_1E.py`, řádek 92): `if x >= x_M0: m += M0`.

### 4.2 Po úsecích

#### Úsek 1: $x \in [0;\ 2)$ — pouze $F_{Ay}$

$$
V(x) = F_{Ay} = -14{,}30\ \mathrm{kN}
$$

$$
M(x) = F_{Ay}\cdot x = -14{,}30\cdot x
$$

| $x$ [m] | $V$ [kN] | $M$ [kN·m] |
|---------|----------|------------|
| 0 | $-14{,}30$ | $0$ (pin → $M = 0$) |
| 2⁻ | $-14{,}30$ | $-28{,}60$ |

#### Úsek 2: $x \in [2;\ 3)$ — přibyl $M_0$

$V$ se nemění (moment nezpůsobuje skok ve $V$):

$$
V(x) = -14{,}30\ \mathrm{kN}
$$

$M$ má **skok** $+M_0$ v $x = 2$:

$$
M(x) = F_{Ay}\cdot x + M_0 = -14{,}30\cdot x + 20
$$

| $x$ [m] | $V$ [kN] | $M$ [kN·m] |
|---------|----------|------------|
| 2⁺ | $-14{,}30$ | $-8{,}60$ (skok $+20$) |
| 3⁻ | $-14{,}30$ | $-22{,}90$ |

#### Úsek 3: $x \in [3;\ 5)$ — přibyla síla $F$

$$
V(x) = F_{Ay} - F = -14{,}30 - 8 = -22{,}30\ \mathrm{kN}
$$

$$
M(x) = F_{Ay}\cdot x + M_0 - F\cdot(x - 3)
$$

| $x$ [m] | $V$ [kN] | $M$ [kN·m] |
|---------|----------|------------|
| 3⁺ | $-22{,}30$ | $-22{,}90$ |
| 5⁻ | $-22{,}30$ | $F_{Ay}\cdot 5 + M_0 - F\cdot 2 = -71{,}5 + 20 - 16 = -67{,}50$ |

Zde je **$M_{\min} = -67{,}50\ \mathrm{kN \cdot m}$** (těsně před B).

#### Úsek 4: $x \in [5;\ 8]$ — přibyly $F_{By}$ a $q$

$$
V(x) = F_{Ay} - F + F_{By} - q\cdot(x - 5)
$$

$$
M(x) = F_{Ay}\cdot x + M_0 - F\cdot(x - 3) + F_{By}\cdot(x - 5) - q\cdot\frac{(x - 5)^2}{2}
$$

V $x = 5^+$: $V$ skočí o $+F_{By} = +67{,}30$ kN:

$$
V(5^+) = -22{,}30 + 67{,}30 = +45{,}00\ \mathrm{kN}
$$

Po započtení nuly z $q$ na okamžik $x = 5^+$ je $V_{\max} \approx 45\ \mathrm{kN}$ (numericky `+44{,}96` kvůli diskretizaci $q$ ve skriptu). Ke konci $x = 8$ pak $V$ klesá o $q\cdot 3 = 45$ kN, takže $V(8) = 0\ \checkmark$.

V $x = 8$ rovněž $M(8) = 0$ (volný konec) — numerická kontrola v Pythonu ji potvrzuje.

### 4.3 Souhrnná tabulka klíčových hodnot

| Veličina | Hodnota | Pozice |
|----------|---------|--------|
| $V_{\max}$ | $+44{,}96\ \mathrm{kN}$ | těsně za podporou B |
| $V_{\min}$ | $-22{,}30\ \mathrm{kN}$ | mezi $F$ a $B$ (úsek 3) |
| $M_{\min}$ | $-67{,}50\ \mathrm{kN \cdot m}$ | u podpory B ($x = 5$) |
| $M(2^-)$ | $-28{,}60\ \mathrm{kN \cdot m}$ | těsně před momentem |
| $M(2^+)$ | $-8{,}60\ \mathrm{kN \cdot m}$ | těsně za momentem (skok $+20$) |

> **Pozorování:** Celý nosník je v oblasti **záporných** ohybových momentů → horní vlákna jsou tažená, spodní tlačená. To je typické pro nosník s převislým koncem zatíženým spojitým zatížením, kde převis dominuje.

---

## 5. Stochastická analýza — Monte Carlo

### 5.1 Model nejistoty

Pouze **zatížení** je náhodné (geometrie deterministická). Variační koeficient $\mathrm{CoV} = 0{,}1$, normální rozdělení:

$$
\sigma_X = \mu_X \cdot \mathrm{CoV}
$$

| Veličina | Rozdělení | $\mu$ | $\sigma$ |
|----------|-----------|-------|----------|
| $M_0$ | $N(\mu, \sigma)$ | $20\ \mathrm{kN \cdot m}$ | $2$ |
| $F$ | $N(\mu, \sigma)$ | $8\ \mathrm{kN}$ | $0{,}8$ |
| $q$ | $N(\mu, \sigma)$ | $15\ \mathrm{kN/m}$ | $1{,}5$ |

### 5.2 Postup simulace

**Počet realizací:** $N = 100\,000$.

V každé realizaci $k$:

1. **Tažení vzorků** — nezávisle z normálního rozdělení:
   $M_0^{(k)},\ F^{(k)},\ q^{(k)}$ — viz `np.random.normal(...)` v Pythonu, řádky 179–181.
2. **Dosazení do rovnic rovnováhy** — stejné jako deterministicky:
   $F_{By}^{(k)} = \dfrac{M_0^{(k)} + F^{(k)}\cdot x_F + F_q^{(k)} \cdot x_{F_q}}{x_B}$
   $F_{Ay}^{(k)} = F^{(k)} + F_q^{(k)} - F_{By}^{(k)}$
3. **Obálky průběhů** — z prvních $1\,000$ realizací se pro každý bod $x$ uloží min/max $V$ a $M$ → červený pás na grafu.

### 5.3 Výpočet statistik

Z vektorů $\{F_R^{(k)}\}_{k=1}^{N}$:

$$
\hat{\mu}_{F_R} = \frac{1}{N}\sum_{k=1}^{N} F_R^{(k)}
$$

$$
\hat{\sigma}_{F_R} = \sqrt{\frac{1}{N}\sum_{k=1}^{N}\!\left(F_R^{(k)} - \hat{\mu}_{F_R}\right)^{\!2}}
$$

$$
\widehat{\mathrm{CoV}} = \frac{\hat{\sigma}_{F_R}}{|\hat{\mu}_{F_R}|}
$$

(Absolutní hodnota ve jmenovateli kvůli zápornému $F_{Ay}$.)

### 5.4 Výsledky

| Reakce | $\hat{\mu}$ [kN] | $\hat{\sigma}$ [kN] | $\widehat{\mathrm{CoV}}$ |
|--------|------------------|---------------------|--------------------------|
| $F_{Ay}$ | $-14{,}30$ | $1{,}45$ | $0{,}101$ |
| $F_{By}$ | $+67{,}29$ | $5{,}88$ | $0{,}087$ |

### 5.5 Diskuse výsledků

- **Střední hodnoty se shodují s deterministickými** — důsledek **linearity** rovnic rovnováhy v $M_0$, $F$, $q$. Pro lineární zobrazení normálního vstupu platí $E[aX + bY] = aE[X] + bE[Y]$.
- **CoV výstupu $\approx$ CoV vstupu pro $F_{Ay}$** ($0{,}101$) — přibližně lineární propagace nejistoty zachovává variabilitu.
- **CoV $F_{By}$ je nižší** ($0{,}087$): ve vztahu pro $F_{By}$ se tři **nezávislé** zdroje $M_0$, $F$, $q$ sčítají s **kladnými** znaménky → variace se "průměrují" (kvadratický součet variancí dává relativně menší celkovou variabilitu vůči součtu středních hodnot).

Analyticky pro $F_{By}$:

$$
\sigma_{F_{By}}^2 = \frac{1}{x_B^2}\!\left(\sigma_{M_0}^2 + (x_F\sigma_F)^2 + (x_{F_q}\sigma_{F_q}\cdot L_q)^2\right)
$$

Po dosazení dostaneme přibližně $\sigma_{F_{By}} \approx 5{,}9\ \mathrm{kN}$, což odpovídá MC.

---

## 6. Vizualizace (vygenerované soubory)

| Soubor | Obsah |
|--------|-------|
| `priklad_1E_diagram.png` | $N(x)$, $V(x)$, $M(x)$ — modrá deterministická křivka + červený pás obálky z 1 000 MC realizací |
| `priklad_1E_histogramy.png` | Empirické histogramy $F_{Ay}$ a $F_{By}$ z $N = 100\,000$ MC realizací; červená přerušovaná čára = deterministická hodnota (= střední hodnota histogramu) |

---

## 7. Klíčové vztahy a vzorce — souhrn

**Rovnice rovnováhy:**

$$
\sum F_x = 0,\qquad \sum F_y = 0,\qquad \sum M_A = 0
$$

**Reakce:**

$$
F_{By} = \frac{M_0 + F\cdot x_F + q\cdot L_q \cdot x_{F_q}}{x_B}
$$

$$
F_{Ay} = F + q\cdot L_q - F_{By}
$$

**Vnitřní síly (rezání zleva):**

$$
V(x) = \sum_{x_i < x} F_{y,i} - \int_0^{x} q(\xi)\,\mathrm{d}\xi
$$

$$
M(x) = \sum_{x_i < x} F_{y,i}\cdot(x - x_i) + \sum_{x_{m,j} < x} M_{0,j}^{(\text{CW})} - \int_0^{x} q(\xi)\cdot(x - \xi)\,\mathrm{d}\xi
$$

**Stochastická propagace:**

$$
\sigma_X = \mu_X \cdot \mathrm{CoV},\qquad \widehat{\mathrm{CoV}} = \frac{\hat{\sigma}}{|\hat{\mu}|}
$$

---

## 8. Závěr

| | Výsledek |
|---|----------|
| **Reakce (deterministicky)** | $F_{Ax} = 0$, $F_{Ay} = -14{,}30\ \mathrm{kN}$, $F_{By} = +67{,}30\ \mathrm{kN}$ |
| **Maximální moment** | $M_{\min} = -67{,}50\ \mathrm{kN \cdot m}$ u podpory B |
| **MC ($N = 10^5$)** | CoV reakcí $0{,}087$ ($F_{By}$) až $0{,}101$ ($F_{Ay}$) |
| **Charakter** | Lineární propagace nejistoty; horní vlákna nosníku tažená v celé délce |
