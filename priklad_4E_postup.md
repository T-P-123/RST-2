# Příklad 4E — Detailní postup řešení

**Téma:** Mezní stav pružnosti a mezní stav deformace stupňovitého plochého prutu zatíženého ohybovým momentem + citlivostní analýza
**Zdroj:** `solutions/reseni_E.pdf` (sekce 4) a `solutions/priklad_4E.py`

---

## 0. Co se v této úloze počítá (rychlý přehled pro úplného začátečníka)

Máme **stupňovitý plochý prut** (representa součást typu „klíč" se třemi výškami). Působí na něj **ohybový moment** $M$ (krouticí silová dvojice ohýbající prut). Úkol je odpovědět na **dvě nezávislé otázky** o spolehlivosti:

1. **Mezní stav pružnosti (MS pružnosti):** Nepřekročí maximální napětí mez kluzu materiálu? — tj. nezačne prut **plasticky téct**?
   Podmínka bezpečnosti: $\sigma_{\max} < R_e$.

2. **Mezní stav deformace (MS deformace):** Nepřekročí průhyb na konci prutu povolenou hodnotu?
   Podmínka bezpečnosti: $w < w_{\max}$.

Obě otázky se řeší **dvakrát**:
- **Deterministicky** — jednou hodnotou (s nominálními rozměry a zatížením).
- **Stochasticky** — Monte Carlo simulací s lognormálními rozděleními všech vstupů (CoV = 0,1), výsledkem je **pravděpodobnost poruchy** $P_f$ a **index spolehlivosti** $\beta$.

Nakonec se dělá **citlivostní analýza** — která z nejistot vstupů přispívá nejvíc k rozptylu výstupu.

---

## 1. Zadání úlohy

### 1.1 Cíl
Určit:
- $P_f$ (pravděpodobnost dosažení MS pružnosti),
- $P_f$ (pravděpodobnost dosažení MS deformace),
- citlivost obou mezních stavů na jednotlivé vstupní veličiny.

### 1.2 Materiálové a zátěžné parametry

| Veličina | Symbol | Hodnota |
|----------|--------|---------|
| Mez kluzu | $R_e$ | $500\ \mathrm{MPa}$ |
| Maximální dovolený průhyb | $w_{\max}$ | $2\ \mathrm{mm}$ |
| Ohybový moment | $M$ | $100\ \mathrm{N \cdot m} = 100\,000\ \mathrm{N \cdot mm}$ |
| Modul pružnosti (ocel) | $E$ | $210\,000\ \mathrm{MPa}$ |

### 1.3 Geometrie stupňovitého prutu

Plochý prut konstantní tloušťky $t$, se třemi úseky o různých výškách (kolmo k rovině ohybu). Tvar připomíná „schody":

```
   úsek 1         úsek 2       úsek 3
 ─────────────  ───────────  ───────────
                                    
  h1 = 45      |  h2 = 30   |  h3 = 10
                                    
 ─────────────  ───────────  ───────────
   r1 ↑ vrub      r2 ↑ vrub
   (3 mm)        (6 mm)
```

| Parametr | Symbol | Hodnota |
|----------|--------|---------|
| Tloušťka prutu (do hloubky) | $t$ | $15\ \mathrm{mm}$ |
| Výška úseku 1 (nejširší) | $h_1$ | $45\ \mathrm{mm}$ |
| Výška úseku 2 | $h_2$ | $30\ \mathrm{mm}$ |
| Výška úseku 3 (nejužší) | $h_3$ | $10\ \mathrm{mm}$ |
| Poloměr přechodu 1 (45→30) | $r_1$ | $3\ \mathrm{mm}$ |
| Poloměr přechodu 2 (30→10) | $r_2$ | $6\ \mathrm{mm}$ |
| Délka úseku 1 | $L_1$ | $60\ \mathrm{mm}$ |
| Délka úseku 2 | $L_2$ | $60\ \mathrm{mm}$ |
| Délka úseku 3 | $L_3$ | $60\ \mathrm{mm}$ |
| Celková délka | $L$ | $L_1+L_2+L_3 = 180\ \mathrm{mm}$ |

**Levý konec** (u $h_1$) — vetknutí. **Pravý konec** (u $h_3$) — volný, zde se zavádí ohybový moment $M$.

### 1.4 Stochastické zadání

Všechny vstupní veličiny mají **lognormální rozdělení** s **variačním koeficientem** $\mathrm{CoV} = 0{,}1$ (tj. relativní rozptyl $\pm 10\%$).

> **Proč lognormální?** Lognormální rozdělení nemůže produkovat záporné hodnoty — to dává fyzikální smysl pro rozměry, materiálové konstanty a zatížení. Pro malé CoV ($\leq 0{,}3$) je tvar prakticky shodný s normálním, ale chrání proti nesmyslným záporným vzorkům.

---

## 2. Klíčové pojmy a vzorce (vysvětlení od základu)

### 2.1 Průřezový modul a kvadratický moment

U **obdélníkového** průřezu o šířce (do hloubky) $t$ a výšce $h$ platí:

$$
W = \frac{t\cdot h^2}{6}\quad [\mathrm{mm^3}]
\qquad\text{a}\qquad
I = \frac{t\cdot h^3}{12}\quad [\mathrm{mm^4}]
$$

- $W$ — **průřezový modul v ohybu**, používá se pro výpočet **napětí** ($\sigma = M/W$).
- $I$ — **kvadratický moment průřezu**, používá se pro výpočet **deformace** ($w \propto M/(E\cdot I)$).

> **Intuice:** Vyšší $h$ znamená výrazně tužší a pevnější profil v ohybu — proto „I-nosníky" mají velkou výšku. Závislost na $h^2$ (pro pevnost) a $h^3$ (pro tuhost) znamená, že **úsek s nejmenší výškou je kritický**.

### 2.2 Nominální napětí v ohybu

Pro daný řez s ohybovým momentem $M$:

$$
\sigma_{\mathrm{nom}} = \frac{M}{W} = \frac{6\,M}{t\,h^2}
$$

To je **napětí v krajních vláknech** uvnitř pravidelné části úseku, **bez vlivu vrubů**.

### 2.3 Součinitel koncentrace napětí $K_t$

V místě, kde se průřez **náhle zužuje** (přechod $h_1 \to h_2$ nebo $h_2 \to h_3$), se napětí lokálně zvyšuje — vznikne **vrubový účinek**. Skutečné maximum napětí v kořeni vrubu je:

$$
\sigma_{\max} = K_t \cdot \sigma_{\mathrm{nom}}
$$

kde $\sigma_{\mathrm{nom}}$ je nominální napětí v **užším** úseku (užší $h$, vyšší $\sigma_{\mathrm{nom}}$). $K_t \geq 1$ je **bezrozměrný součinitel tvaru**, který se odečítá z **Petersonových diagramů** (publikované grafy z teorie pružnosti / FEM).

Pro stupňovitý plochý prut v ohybu se $K_t$ určuje z poměrů:

$$
\frac{D}{d} = \frac{\text{vyšší úsek}}{\text{nižší úsek}},\qquad
\frac{r}{d} = \frac{\text{poloměr zaoblení}}{\text{nižší úsek}}
$$

### 2.4 Mezní stav (limit state)

**Funkce poruchy** $g$ je rozdíl mezi **únosností** a **požadavkem**:

- **MS pružnosti:** $g_1 = R_e - \sigma_{\max}$. Porucha = $g_1 < 0$.
- **MS deformace:** $g_2 = w_{\max} - w$. Porucha = $g_2 < 0$.

**Pravděpodobnost poruchy:** $P_f = P(g < 0)$.

**Index spolehlivosti:** $\beta = -\Phi^{-1}(P_f)$, kde $\Phi^{-1}$ je inverzní distribuční funkce normovaného normálního rozdělení. Větší $\beta$ = bezpečnější součást.

| $\beta$ | $P_f$ | Interpretace |
|---------|-------|--------------|
| $0$ | $0{,}5$ | Náhodný hod mincí |
| $1$ | $0{,}159$ | Velmi nebezpečné |
| $2{,}5$ | $0{,}006$ | Standardní pro stavby |
| $3{,}8$ | $\sim 10^{-4}$ | Vysoká spolehlivost |

---

## 3. Deterministické řešení

### 3.1 Průřezové charakteristiky

Pro každý úsek dosadíme do vzorců $W = t\,h^2/6$, $I = t\,h^3/12$ s $t = 15\ \mathrm{mm}$:

| Úsek | $h_i$ [mm] | $W_i$ [mm³] | $I_i$ [mm⁴] |
|------|-----------|-------------|-------------|
| 1 | 45 | $15\cdot 45^2/6 = 5\,062{,}5$ | $15\cdot 45^3/12 = 113\,906$ |
| 2 | 30 | $15\cdot 30^2/6 = 2\,250{,}0$ | $15\cdot 30^3/12 = 33\,750$ |
| 3 | 10 | $15\cdot 10^2/6 = 250{,}0$ | $15\cdot 10^3/12 = 1\,250$ |

> **Pozorování:** $W_3$ je **20× menší** než $W_1$ a $I_3$ je **91× menší** než $I_1$ — úsek 3 je „slabé místo" jak pro pevnost, tak pro tuhost.

### 3.2 Nominální napětí v každém úseku

S $M = 100\,000\ \mathrm{N \cdot mm}$:

| Úsek | $\sigma_{\mathrm{nom},i} = M/W_i$ [MPa] |
|------|----------------------------------------|
| 1 | $100\,000 / 5\,062{,}5 = 19{,}75$ |
| 2 | $100\,000 / 2\,250 = 44{,}44$ |
| 3 | $100\,000 / 250 = \mathbf{400{,}0}$ ← **kritický úsek** |

### 3.3 Součinitelé tvaru $K_t$ (amesweb kalkulátor)

Hodnoty $K_t$ pro **shoulder fillet in flat bar** v ohybu odečteny z online kalkulátoru
(<https://amesweb.info/stress-concentration-factor-calculator/shoulder-fillets-in-flat-bar.aspx>):

**Vrub $r_1$ (přechod 45 → 30):**
$$
\frac{D}{d} = \frac{45}{30} = 1{,}5,\qquad \frac{r_1}{d} = \frac{3}{30} = 0{,}1
\;\Longrightarrow\; K_{t1} \approx 1{,}86
$$

**Vrub $r_2$ (přechod 30 → 10):**
$$
\frac{D}{d} = \frac{30}{10} = 3{,}0,\qquad \frac{r_2}{d} = \frac{6}{10} = 0{,}6
\;\Longrightarrow\; K_{t2} = 1{,}00
$$

> **Proč je $K_{t2} = 1$?** Vrub $r_2$ má relativně **velký** poloměr vůči užšímu rozměru ($r/d = 0{,}6$) — zaoblení je tak „měkké", že podle kalkulátoru nezpůsobuje žádnou koncentraci napětí. Vrub $r_1$ má naopak **ostré** zaoblení ($r/d = 0{,}1$) → výraznější koncentrace.

### 3.4 Skutečné maximální napětí ve vrubech

Vrubový součinitel se aplikuje na nominální napětí v **užším** úseku za vrubem:

$$
\sigma_{\max,1} = K_{t1}\cdot\sigma_{\mathrm{nom},2} = 1{,}86 \cdot 44{,}44 = 82{,}7\ \mathrm{MPa}
$$

$$
\sigma_{\max,2} = K_{t2}\cdot\sigma_{\mathrm{nom},3} = 1{,}00 \cdot 400 = \boxed{400\ \mathrm{MPa}}
$$

**Rozhoduje úsek 3** ($\sigma_{\max,2} = 400$ MPa). Vrub $r_2$ nepřispívá koncentrací, ale samotné nominální napětí v nejužším průřezu zůstává nejvyšší.

### 3.5 Součinitel bezpečnosti k MS pružnosti

$$
k_{\mathrm{yield}} = \frac{R_e}{\sigma_{\max,2}} = \frac{500}{400} = \boxed{1{,}250}
$$

Rezerva 25 % do meze kluzu — výrazně větší než s původními $K_t$.

### 3.6 Průhyb volného konce — Mohrova analogie pro stupňovitý prut

#### Princip

Pro **konzolu zatíženou konstantním momentem $M$** (vetknutí vlevo, volný konec vpravo, žádné silové zatížení) je úhel natočení a průhyb dán integrací křivosti $\kappa(x) = M/(E\,I(x))$. Průhyb na volném konci:

$$
w = \int_0^{L} \frac{M}{E\,I(x)}\cdot (L - x)\,\mathrm{d}x
$$

Pro stupňovitý prut s konstantním $I_i$ na úseku $[a_i, b_i]$ se integrál v daném úseku spočítá analyticky:

$$
\int_{a_i}^{b_i}(L - x)\,\mathrm{d}x = \frac{(L-a_i)^2 - (L-b_i)^2}{2} \equiv J_i
$$

Celkový průhyb je suma příspěvků jednotlivých úseků:

$$
w = \frac{M}{E}\sum_{i=1}^{3}\frac{J_i}{I_i}
$$

#### Dosazení

S $L = 180\ \mathrm{mm}$, hranice úseků $[0; 60]$, $[60; 120]$, $[120; 180]$:

$$
J_1 = \frac{(180-0)^2 - (180-60)^2}{2} = \frac{32\,400 - 14\,400}{2} = 9\,000
$$

$$
J_2 = \frac{(180-60)^2 - (180-120)^2}{2} = \frac{14\,400 - 3\,600}{2} = 5\,400
$$

$$
J_3 = \frac{(180-120)^2 - (180-180)^2}{2} = \frac{3\,600 - 0}{2} = 1\,800
$$

Příspěvky úseků (s $M/E = 100\,000/210\,000 = 0{,}4762$):

| Úsek | $J_i/I_i$ | Příspěvek $w_i = (M/E)\cdot J_i/I_i$ [mm] | Podíl |
|------|-----------|-------------------------------------------|-------|
| 1 | $9\,000/113\,906 = 0{,}0790$ | $0{,}038$ | 4,7 % |
| 2 | $5\,400/33\,750 = 0{,}1600$ | $0{,}076$ | 9,5 % |
| 3 | $1\,800/1\,250 = 1{,}4400$ | $\mathbf{0{,}686}$ | **85,8 %** |

$$
\boxed{w = 0{,}038 + 0{,}076 + 0{,}686 = 0{,}800\ \mathrm{mm}}
$$

> **Důležité pozorování:** **Úsek 3 přispívá ~86 %** k celkovému průhybu, přestože je stejně dlouhý jako ostatní. Důvod: závislost na $1/I \propto 1/h^3$ — třetí mocnina znamená, že tenký úsek je ohybově extrémně poddajný.

#### Součinitel bezpečnosti k MS deformace

$$
k_{\mathrm{deform}} = \frac{w_{\max}}{w} = \frac{2}{0{,}800} = 2{,}501
$$

Více než 2,5× rezerva — deformace deterministicky vyhovuje s velkým komfortem.

### 3.7 Shrnutí deterministických výsledků

| Veličina | Hodnota | Vyhodnocení |
|----------|---------|-------------|
| $\sigma_{\max}$ | $400\ \mathrm{MPa}$ | < $R_e = 500\ \mathrm{MPa}$ ✓ ($k=1{,}250$) |
| $w$ | $0{,}800\ \mathrm{mm}$ | < $w_{\max} = 2\ \mathrm{mm}$ ✓ ($k=2{,}501$) |

Deterministicky **oba mezní stavy vyhovují**; rezerva u MS pružnosti je 25 %.

---

## 4. Stochastická analýza — Monte Carlo

### 4.1 Princip metody

**Monte Carlo (MC)** je numerická simulační technika — místo jednoho deterministického výpočtu se úloha řeší $N$-krát s **náhodně tažnými vstupy** podle zadaných pravděpodobnostních rozdělení. Empirické rozdělení výstupu pak aproximuje skutečné statistické chování.

**V této úloze:** $N = 500\,000$ realizací, lognormální vstupy, $\mathrm{CoV} = 0{,}1$.

### 4.2 Lognormální rozdělení — parametry

Lognormální rozdělení $X \sim \mathrm{LN}(\mu_{\ln}, \sigma_{\ln})$ má **střední hodnotu** $\mu$ a **směrodatnou odchylku** $\sigma$ v lineární škále, jež se přepočítají na parametry v logaritmické škále:

$$
\sigma_{\ln} = \sqrt{\ln\!\left(1 + \mathrm{CoV}^2\right)}
$$

$$
\mu_{\ln} = \ln(\mu) - \tfrac{1}{2}\sigma_{\ln}^2
$$

Pro $\mathrm{CoV} = 0{,}1$:

$$
\sigma_{\ln} = \sqrt{\ln(1{,}01)} = \sqrt{0{,}00995} \approx 0{,}0998
$$

V Pythonu (`priklad_4E.py`, řádky 120–127):

```python
def lognormal_params(mean, cov):
    sigma_ln = np.sqrt(np.log(1 + cov**2))
    mu_ln = np.log(mean) - 0.5 * sigma_ln**2
    return mu_ln, sigma_ln

def lognormal_sample(mean, cov, n):
    mu_ln, sig_ln = lognormal_params(mean, cov)
    return np.random.lognormal(mu_ln, sig_ln, n)
```

### 4.3 Náhodně tažné vstupy

| Veličina | $\mu$ | Rozdělení | Použití |
|----------|-------|-----------|---------|
| $M$ | $100\,000\ \mathrm{N \cdot mm}$ | LN, CoV=0,1 | Zatížení |
| $R_e$ | $500\ \mathrm{MPa}$ | LN, CoV=0,1 | Mez kluzu |
| $w_{\max}$ | $2\ \mathrm{mm}$ | LN, CoV=0,1 | Limit deformace |
| $h_3$ | $10\ \mathrm{mm}$ | LN, CoV=0,1 | Kritický rozměr |
| $t$ | $15\ \mathrm{mm}$ | LN, CoV=0,1 | Tloušťka |
| $K_{t2}$ | $1{,}00$ | deterministicky (žádná koncentrace) | Vrubový součinitel |
| $L$ | $180\ \mathrm{mm}$ | LN, CoV=0,1 | Celková délka |
| $E$ | $210\,000\ \mathrm{MPa}$ | LN, CoV=0,1 | Modul pružnosti |

> **Zjednodušení:** $h_1$, $h_2$ a délky jednotlivých úseků se v MC pro průhyb modelují deterministicky (nejistota se aplikuje jen na nejcitlivější veličiny — to je obvyklý kompromis pro snížení počtu rozměrů problému).

### 4.4 Výpočet napětí v každé realizaci

$$
W_3^{(k)} = \frac{t^{(k)}\cdot (h_3^{(k)})^2}{6}
$$

$$
\sigma_{\max}^{(k)} = K_{t2}\cdot\frac{M^{(k)}}{W_3^{(k)}} = \frac{M^{(k)}}{W_3^{(k)}}\quad(K_{t2}=1)
$$

V kódu:

```python
W3_mc = t_mc * h3_mc**2 / 6.0
sigma_max_mc = Kt2 * M_mc / W3_mc   # Kt2 = 1.0 deterministicky
```

### 4.5 Výpočet průhybu v každé realizaci

Stejný vzorec jako deterministicky, ale $t$, $h_3$, $E$, $M$ jsou náhodné:

$$
I_1^{(k)} = \frac{t^{(k)}\cdot h_1^3}{12},\qquad
I_2^{(k)} = \frac{t^{(k)}\cdot h_2^3}{12},\qquad
I_3^{(k)} = \frac{t^{(k)}\cdot (h_3^{(k)})^3}{12}
$$

$$
w^{(k)} = \frac{M^{(k)}}{E^{(k)}}\!\left(\frac{J_1}{I_1^{(k)}} + \frac{J_2}{I_2^{(k)}} + \frac{J_3}{I_3^{(k)}}\right)
$$

> **Pozn.:** $J_1$, $J_2$, $J_3$ zůstávají deterministické (závisejí na délkách, které se zde předpokládají pevné).

### 4.6 Funkce poruchy a $P_f$

Pro každou realizaci se spočítá:

$$
g_1^{(k)} = R_e^{(k)} - \sigma_{\max}^{(k)}\quad(\text{MS pružnosti})
$$

$$
g_2^{(k)} = w_{\max}^{(k)} - w^{(k)}\quad(\text{MS deformace})
$$

**Pravděpodobnost poruchy** = empirický podíl realizací, kde $g < 0$:

$$
\hat{P}_f = \frac{\#\{k\,:\,g^{(k)} < 0\}}{N}
$$

V kódu (řádky 149–155):

```python
g_yield = Re_mc - sigma_max_mc
P_yield_failure = np.sum(g_yield < 0) / N_sim

g_deform = wm_mc - w_mc
P_deform_failure = np.sum(g_deform < 0) / N_sim
```

**Index spolehlivosti:** $\beta = -\Phi^{-1}(\hat{P}_f)$ pomocí `scipy.stats.norm.ppf`.

### 4.7 Výsledky

| Mezní stav | $P_f$ | $\beta$ | Střední hodnota výstupu | Vyhodnocení |
|------------|-------|---------|-------------------------|-------------|
| **MS pružnosti** | $\boxed{21{,}48\ \%}$ | $0{,}79$ | $\mu(\sigma_{\max}) \approx 416\ \mathrm{MPa}$, $\sigma \approx 103\ \mathrm{MPa}$ | **Nevyhovuje** |
| **MS deformace** | $\boxed{0{,}36\ \%}$ | $2{,}69$ | $\mu(w) \approx 0{,}86\ \mathrm{mm}$ | Vyhovuje s rezervou |

### 4.8 Klíčový závěr — proč je $P_f$ pro pružnost stále velké?

**Deterministicky** $\sigma_{\max} = 400\ \mathrm{MPa}$ leží **pod** $R_e = 500\ \mathrm{MPa}$ — mezera 100 MPa, $k = 1{,}25$.

**Stochasticky** je směrodatná odchylka výstupu $\sigma_{\sigma_{\max}} \approx 103\ \mathrm{MPa}$, tedy **srovnatelná** s touto bezpečnostní rezervou.

**Důvod velkého rozptylu:** $\sigma_{\max}$ závisí kvadraticky na $h_3$ ($\sigma \propto 1/h_3^2$). Lognormální propagace přes mocninnou závislost **zesiluje** vstupní variabilitu. Vstupní CoV = 0,1 dává výstupní CoV $\approx 0{,}25$ pro $\sigma_{\max}$.

**Závěr:** I přes deterministickou rezervu 25 % má součást **~21% pravděpodobnost překročení meze kluzu** — pravděpodobnostně **nevyhovuje** (oproti $\approx 40\,\%$ při původních $K_t$).

---

## 5. Citlivostní analýza

### 5.1 Princip

Cíl: zjistit, **která vstupní veličina nejvíc přispívá** k rozptylu funkce poruchy $g$. To umožňuje:
- zaměřit kontrolu kvality (zpřesnit nejcitlivější rozměr),
- konstrukčně optimalizovat (zesílit nejcitlivější parametr).

**Metoda:** výpočet **Pearsonovy korelace** $\rho(g, X_i)$ mezi funkcí poruchy a každým vstupem; **faktor důležitosti** je normovaný kvadrát:

$$
\alpha_i^2 = \frac{\rho_i^2}{\sum_j \rho_j^2}\cdot 100\%
$$

V kódu (řádky 185–189):

```python
corrs_y = np.array([np.corrcoef(v, g_yield)[0, 1] for v in variables_yield.values()])
alpha_sq_y = corrs_y**2 / (corrs_y**2).sum()
```

### 5.2 Výsledky pro MS pružnosti

| Veličina | $\rho(g_1, X_i)$ | $\alpha_i^2$ | Interpretace |
|----------|------------------|--------------|--------------|
| $h_3$ | $+0{,}714$ | $\mathbf{53{,}1\ \%}$ | **Dominantní** — výška kritického průřezu |
| $R_e$ | $+0{,}438$ | $19{,}9\ \%$ | Mez kluzu |
| $M$ | $-0{,}361$ | $13{,}6\ \%$ | Zatížení |
| $t$ | $+0{,}359$ | $13{,}4\ \%$ | Tloušťka |

> **Znaménka korelací:**
> - **Kladné** ($h_3$, $R_e$, $t$): zvýšení této veličiny zvětší rezervu $g_1 = R_e - \sigma_{\max}$ → bezpečnější.
> - **Záporné** ($M$): zvýšení této veličiny zmenší rezervu → nebezpečnější.
> - $K_{t2} = 1$ je deterministicky pevné, do citlivostní analýzy nevstupuje.

### 5.3 Interpretace dominance $h_3$

Funkce poruchy:
$$
g_1 = R_e - K_{t2}\cdot\frac{6\,M}{t\,h_3^2} = R_e - \frac{6\,M}{t\,h_3^2}
$$

$h_3$ vstupuje **kvadraticky ve jmenovateli**, zatímco $M$ a $t$ jen **lineárně**. Citlivost na relativní změnu (logaritmická citlivost) je úměrná mocnině:

$$
\frac{\partial \ln \sigma_{\max}}{\partial \ln h_3} = -2,\qquad
\frac{\partial \ln \sigma_{\max}}{\partial \ln M} = +1,\qquad\ldots
$$

Proto $h_3$ s CoV = 0,1 zesiluje rozptyl výstupu **dvojnásobně** ve srovnání s lineárními vstupy → 4× větší příspěvek k varianci → 53 % vs ~13 %.

### 5.4 Praktický důsledek

Pro **zvýšení spolehlivosti** je nejúčinnější:

1. **Zvětšit $h_3$** (mocninný efekt) — i malé zvětšení dramaticky sníží napětí.
2. **Zpřesnit toleranci $h_3$** (snížit jeho CoV) — sníží rozptyl výstupu.
3. Ostatní opatření (tužší $R_e$, menší $M$) mají 4× menší účinek.

---

## 6. Vizualizace (vygenerované soubory)

| Soubor | Obsah |
|--------|-------|
| `priklad_4E_vysledky.png` | 2×2 panel: (a) histogramy $\sigma_{\max}$ a $R_e$ s vyznačením $P_f$, (b) histogramy $w$ a $w_{\max}$, (c) histogram funkce poruchy $g_1$ s ohraničením $g=0$, (d) sloupcový graf příspěvků $\alpha_i^2$ k MS pružnosti. |
| `priklad_4E_ansys.mac` | APDL skript pro ANSYS — 2D plane stress, PLANE183, validace deterministického napětí ve vrubu (FEM vs analytický $K_t$). |

---

## 7. Klíčové vztahy a vzorce — souhrn

**Průřezové charakteristiky obdélníku** ($t \times h$):
$$
W = \frac{t\,h^2}{6},\qquad I = \frac{t\,h^3}{12}
$$

**Nominální napětí v ohybu:**
$$
\sigma_{\mathrm{nom}} = \frac{M}{W}
$$

**Maximální napětí ve vrubu:**
$$
\sigma_{\max} = K_t\cdot\sigma_{\mathrm{nom}}\quad(K_t\text{ z Petersonových diagramů podle }D/d, r/d)
$$

**Průhyb stupňovité konzoly s konstantním $M$:**
$$
w = \frac{M}{E}\sum_{i=1}^{n}\frac{J_i}{I_i},\qquad J_i = \frac{(L-a_i)^2 - (L-b_i)^2}{2}
$$

**Lognormální rozdělení z $\mu, \mathrm{CoV}$:**
$$
\sigma_{\ln} = \sqrt{\ln(1+\mathrm{CoV}^2)},\qquad \mu_{\ln} = \ln\mu - \tfrac{1}{2}\sigma_{\ln}^2
$$

**Funkce poruchy a $P_f$:**
$$
g = \text{únosnost} - \text{požadavek},\qquad P_f = P(g < 0),\qquad \beta = -\Phi^{-1}(P_f)
$$

**Faktor důležitosti:**
$$
\alpha_i^2 = \frac{\rho^2(g, X_i)}{\sum_j \rho^2(g, X_j)}
$$

---

## 8. Závěr

| | Výsledek |
|---|----------|
| **Kritické místo** | Úsek 3 ($h_3 = 10$ mm), bez koncentrace ($K_{t2} = 1$) |
| **$\sigma_{\max}$ deterministicky** | $400\ \mathrm{MPa}$ (mezera $100\ \mathrm{MPa}$ do $R_e$, $k = 1{,}25$) |
| **$w$ deterministicky** | $0{,}800\ \mathrm{mm}$ (úsek 3 dává ~86 % příspěvku) |
| **MS pružnosti — $P_f$** | $\mathbf{21{,}48\ \%}$ → součást **NEVYHOVUJE** |
| **MS deformace — $P_f$** | $0{,}36\ \%$ → vyhovuje ($\beta = 2{,}69$) |
| **Dominantní citlivost** | $h_3$ — 53 % rozptylu (kvadratická závislost) |
| **Doporučení** | Zvětšit $h_3$ nebo zpřesnit jeho toleranci |

**Hlavní poučení:** I při deterministické bezpečnosti $k = 1{,}25$ (rezerva 25 %) je **při běžných výrobních tolerancích ($\mathrm{CoV} = 10\,\%$) ~21 % pravděpodobnost dosažení meze kluzu**. Pravděpodobnostní přístup odhaluje slabé místo, které deterministický výpočet skrývá. Oproti původním Petersonovým hodnotám ($K_{t1}=1{,}68$, $K_{t2}=1{,}15$, $P_f \approx 40\,\%$) dává amesweb kalkulátor odlišný profil — vrub $r_2$ nezpůsobuje koncentraci, ale samotný úsek 3 je stále dominantní rizikový bod.
