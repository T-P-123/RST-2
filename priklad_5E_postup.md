# Příklad 5E — Detailní postup řešení

**Téma:** Časový průběh napětí ve vrubech rotační hřídele s jednostranným kontaktem, axiálně zatížené střídavou silou.
**Zdroj:** `solutions/reseni_E.pdf` (sekce 5) a `solutions/priklad_5E.py`
**Obrázky:** `img/zadani/priklad_5E_zadani.png`, `solutions/priklad_5E_vysledky.png`, `solutions/priklad_5E_haigh.png`

---

## 0. Co se v této úloze počítá (rychlý přehled pro úplného začátečníka)

Máme **rotační hřídel** (válec) zatížený **střídavou osovou silou** (tah ↔ tlak) — síla mění znaménko jako obdélníková vlna v čase. Hřídel má **dva zápichy** (úzké zúžení průměru), v nichž vzniká **koncentrace napětí**.

Speciální detail: **pravý konec není přivařený k pevné stěně, jen se o ni opírá**. Posuv do stěny tedy možný není (stěna brání), ale posuv od stěny ano (hřídel se může odlepit). Tomu se říká **jednostranný kontakt**.

Důsledek: úloha se musí spočítat **dvakrát** — jednou pro fázi „síla tlačí do stěny" (kontakt aktivní), podruhé pro fázi „síla táhne od stěny" (kontakt rozevřen). V každé fázi vyjdou **jiné vnitřní síly** v hřídeli, a tedy i jiné napětí ve vrubech.

Cíl:

1. **Deterministicky** spočítat napětí v obou vrubech v obou stavech zatížení a popsat jejich časový průběh.
2. **Stochasticky** (Monte Carlo) zjistit, jak rozptyl rozměrů (tolerance ±0,5 mm) ovlivní napětí.
3. **Vykreslit Haighův diagram** (σ_a vs σ_m) a posoudit únavu vůči Goodmanově přímce.

---

## 1. Zadání úlohy

### 1.1 Geometrie hřídele

Hřídel celkové délky **L_tot = 820 mm**, složená ze 5 úseků (zleva doprava):

| Úsek | Délka [mm] | Průměr | Popis |
|------|-----------|--------|-------|
| 1 | 200 | D = 50 | první válec |
| 2 | 10  | d = 35 | **levý zápich** (vrub) |
| 3 | 400 | D = 50 | střední válec |
| 4 | 10  | d = 35 | **pravý zápich** (vrub) |
| 5 | 200 | D = 50 | poslední válec |

- Poloměr zaoblení dna zápichu: **r = 5 mm** (oba vruby).
- Síla F působí v poloze **x_F = 500 mm** od levého vetknutí (tj. uprostřed středního úseku, mezi vruby).
- Levý vrub: x ∈ [200; 210] mm — **před** silou.
- Pravý vrub: x ∈ [610; 620] mm — **za** silou.

### 1.2 Uložení

| Konec | Vazba | Co přenáší |
|-------|-------|-----------|
| Vlevo (x=0) | **pevné vetknutí** | tah i tlak |
| Vpravo (x=820) | **jednostranný kontakt** se stěnou (δ=0) | **pouze tlak** (od stěny se může odlepit) |

> **Klíčové:** pravá stěna neumí táhnout. Pokud by reakce vyšla kladná (tažná), vyhodíme ji a hřídel se chová, jako by vpravo nebyl podepřený.

### 1.3 Zatížení

Obdélníková střídavá osová síla:

$$F(t) = \pm 1{,}4\cdot 10^5\ \mathrm{N} = \pm 140\ \mathrm{kN}$$

Tolerance: **+1000 / −0 N** (tj. F ∈ ⟨140 000; 141 000⟩ N v absolutní hodnotě).
Konvence: F > 0 ⇒ síla míří doprava (do stěny). F < 0 ⇒ síla míří doleva (od stěny).

Tolerance všech rozměrů: **±0,5 mm**.

### 1.4 Co se má spočítat

- Časový průběh σ(t) v levém i pravém vrubu.
- σ_max, σ_min, amplituda σ_a, střední napětí σ_m a R = σ_min/σ_max v každém vrubu.
- Statistiky napětí (Monte Carlo, 100 000 simulací).
- Haighův diagram s Goodmanovou přímkou (mez kluzu R_e = 500 MPa, mez únavy σ_c = 300 MPa).

---

## 2. Klíčové pojmy a vzorce (vysvětlení od základu)

### 2.1 Osové napětí v prostém prutu

Pro plný kruhový průřez o průměru d:

$$A = \frac{\pi d^2}{4},\qquad \sigma_{\mathrm{nom}} = \frac{N}{A}$$

kde N je vnitřní osová síla (tah +, tlak −) a σ_nom je **nominální** (průměrné) napětí v průřezu.

### 2.2 Součinitel koncentrace napětí K_t

Vrub (zápich, rádius, otvor) způsobuje **lokální zvýšení napětí** na dně vrubu nad nominální hodnotu:

$$\sigma_{\max} = K_t \cdot \sigma_{\mathrm{nom}}$$

K_t závisí jen na **geometrii** (poměry D/d a r/d), nikoliv na materiálu ani zatížení. Hodnoty se odečítají z **Petersonových grafů** — pro náš případ (kruhový hřídel s U-vrubem v axiálním tahu, Chart 2.19):

$$\frac{D}{d} = \frac{50}{35} = 1{,}429,\qquad \frac{r}{d} = \frac{5}{35} = 0{,}143 \quad\Rightarrow\quad K_t \approx 2{,}10$$

> **Intuice:** ostrý vrub (malé r) napětí silně zvedá. Náš poměr r/d = 0,143 je střední — proto K_t ≈ 2.

> **Alternativa:** Neuberova aproximace $K_t = 1 + 2\sqrt{t/r}$ (kde t = (D−d)/2 = 7,5 mm) dá K_t ≈ 3,45 — je konzervativní (větší). Petersonův graf je přesnější, používáme tedy 2,10.

### 2.3 Staticky určitá vs. neurčitá úloha

- **Staticky určitá:** počet neznámých reakcí ≤ počet rovnic rovnováhy. Stačí Newton.
- **Staticky neurčitá:** víc reakcí než rovnic → musíme přidat **podmínku kompatibility** (geometrické omezení deformací).

Naše hřídel s **oboustranným** vetknutím by byla 1× staticky neurčitá. Náš **jednostranný kontakt** to dělá ještě zajímavější:

| Smysl síly F | Pravá stěna | Úloha |
|--------------|-------------|-------|
| F > 0 (do stěny) | kontakt aktivní | **staticky neurčitá** |
| F < 0 (od stěny) | kontakt rozevřen | **staticky určitá** |

### 2.4 Osová poddajnost prutu

Délka úseku L o průřezu A pod osovou silou N se prodlouží o:

$$\Delta L = \frac{N\cdot L}{E\cdot A}$$

Pro prut složený z více úseků se prodloužení sčítají. Definujeme **poddajnost** C (násobenou modulem E, který se vykrátí):

$$C\cdot E = \sum_i \frac{L_i}{A_i}$$

Pro **levou část** (od vetknutí k místu síly, x ∈ [0; x_F]):

$$C_L\cdot E = \frac{L_{D,\mathrm{lev}}}{A_D} + \frac{L_{d,\mathrm{lev}}}{A_d}$$

Analogicky pro **pravou část** (od síly ke konci, x ∈ [x_F; L_tot]).

### 2.5 Charakteristiky cyklického zatížení

Pro napětí, které mezi σ_max a σ_min střídá hodnoty, definujeme:

| Veličina | Vzorec | Význam |
|----------|--------|--------|
| **amplituda** | $\sigma_a = \dfrac{\sigma_{\max} - \sigma_{\min}}{2}$ | poloviční rozkmit |
| **střední napětí** | $\sigma_m = \dfrac{\sigma_{\max} + \sigma_{\min}}{2}$ | střed cyklu |
| **součinitel asymetrie** | $R = \dfrac{\sigma_{\min}}{\sigma_{\max}}$ | typ cyklu |

**Typy cyklů podle R:**
- R = −1 → **symetrický střídavý** (σ_m = 0)
- R = 0 → **míjivý** tah (σ_min = 0)
- R = ±∞ → **míjivý tlak** (σ_max = 0)
- jiné R → **asymetrický střídavý**

---

## 3. Deterministické řešení — Stav A (kontakt aktivní)

### 3.1 Kdy nastává

Síla míří doprava (F = +140 kN), tlačí hřídel do pravé stěny. Stěna se brání reakcí R_R. Úloha **staticky neurčitá**.

### 3.2 Volné těleso (FBD) a vnitřní síly

Konvence: tah +, +x doprava. R_R je reakce od pravé stěny — působí proti pohybu, tedy doleva, R_R ≤ 0.

Vnitřní osová síla N(x):

$$N_{\mathrm{levá}}(x < x_F) = F + R_R$$
$$N_{\mathrm{pravá}}(x > x_F) = R_R$$

(Mezi vetknutím a silou jde celá síla F minus reakce, za silou jde už jen reakce R_R.)

### 3.3 Podmínka kompatibility

Pravý konec se nesmí pohnout (drží jej stěna):

$$\Delta_{\mathrm{tot}} = \frac{N_{\mathrm{levá}}\cdot C_L\cdot E + N_{\mathrm{pravá}}\cdot C_R\cdot E}{E} = 0$$

Po vykrácení E:

$$N_{\mathrm{levá}}\cdot C_L + N_{\mathrm{pravá}}\cdot C_R = 0$$

Dosadíme:

$$(F + R_R)\cdot C_L + R_R\cdot C_R = 0 \quad\Rightarrow\quad \boxed{R_R = -F\cdot \frac{C_L}{C_L + C_R}}$$

### 3.4 Výpočet poddajností

Průřezy:
$$A_D = \frac{\pi\cdot 50^2}{4} = 1963{,}5\ \mathrm{mm^2},\qquad A_d = \frac{\pi\cdot 35^2}{4} = 962{,}1\ \mathrm{mm^2}$$

**Levá část (x ∈ [0; 500]):** úseky D mají dohromady 200 + 290 = 490 mm, úsek d (levý zápich) má 10 mm.

$$C_L = \frac{490}{1963{,}5} + \frac{10}{962{,}1} = 0{,}24955 + 0{,}01039 = 0{,}25995\ \mathrm{mm/mm^2}$$

**Pravá část (x ∈ [500; 820]):** úseky D mají dohromady 110 + 200 = 310 mm, úsek d (pravý zápich) má 10 mm.

$$C_R = \frac{310}{1963{,}5} + \frac{10}{962{,}1} = 0{,}15788 + 0{,}01039 = 0{,}16827\ \mathrm{mm/mm^2}$$

### 3.5 Reakce a vnitřní síly v Stavu A

$$R_R = -140\,000 \cdot \frac{0{,}25995}{0{,}25995 + 0{,}16827} = -140\,000 \cdot \frac{0{,}25995}{0{,}42822} = \boxed{-84\,985\ \mathrm{N}}$$

$$N_{\mathrm{levá}}^{A} = F + R_R = 140\,000 - 84\,985 = \boxed{+55\,015\ \mathrm{N}}\ (\text{tah})$$

$$N_{\mathrm{pravá}}^{A} = R_R = \boxed{-84\,985\ \mathrm{N}}\ (\text{tlak})$$

> **Smysl:** kus síly (≈ 60 %) jde do levé stěny tahem, zbytek (≈ 40 %) odtlačí pravou stěnu.

---

## 4. Deterministické řešení — Stav B (kontakt rozevřen)

### 4.1 Kdy nastává

Síla míří doleva (F = −140 kN), táhne hřídel od pravé stěny. Stěna nemůže táhnout zpět ⇒ **R_R = 0**, hřídel se odlepí. Úloha **staticky určitá**.

### 4.2 Vnitřní síly

Z rovnováhy (F+R_L+R_R=0, R_R=0 ⇒ R_L = −F = +140 kN):

$$N_{\mathrm{levá}}^{B} = F + 0 = \boxed{-140\,000\ \mathrm{N}}\ (\text{tlak})$$
$$N_{\mathrm{pravá}}^{B} = 0$$

> **Pravá část je „mrtvá":** v Stavu B za silou není nic, co by tahalo nebo tlačilo. Síla se rozhodla jít doleva, vetknutí ji zachytí.

---

## 5. Lokální napětí ve vrubech

Pomocí $\sigma = K_t \cdot N/A_d$ (vrub je v užším průřezu d, používáme A_d):

### 5.1 Levý vrub (x ∈ [200; 210])

$$\sigma_L^{A} = 2{,}10\cdot \frac{55\,015}{962{,}1} = \boxed{+120{,}1\ \mathrm{MPa}}\ (\text{tah})$$

$$\sigma_L^{B} = 2{,}10\cdot \frac{-140\,000}{962{,}1} = \boxed{-305{,}6\ \mathrm{MPa}}\ (\text{tlak})$$

### 5.2 Pravý vrub (x ∈ [610; 620])

$$\sigma_R^{A} = 2{,}10\cdot \frac{-84\,985}{962{,}1} = \boxed{-185{,}5\ \mathrm{MPa}}\ (\text{tlak})$$

$$\sigma_R^{B} = 0\ \mathrm{MPa}$$

### 5.3 Charakteristiky cyklu

| Vrub | σ_max [MPa] | σ_min [MPa] | σ_a [MPa] | σ_m [MPa] | R | Charakter |
|------|-------------|-------------|-----------|-----------|---|-----------|
| **Levý**  | +120,1 | −305,6 | **212,8** | **−92,8** | −2,55 | asymetrický střídavý (tah ↔ velký tlak) |
| **Pravý** | 0      | −185,5 | **92,8**  | **−92,8** | ±∞ | míjivý tlak (0 ↔ tlak) |

**Pozorování:**
- **Levý vrub je kritický** — má největší tlakovou špičku −305,6 MPa (Stav B, celá síla vetknutí).
- **Pravý vrub** je vždy v tlaku nebo nulový — když síla táhne doleva, pravá strana se odlepí a napětí padne na 0.
- Obě σ_m vyšla shodně −92,8 MPa (důsledek symetrie obdélníkové vlny).

---

## 6. Časový průběh napětí

Síla F(t) je obdélníková vlna ±140 kN — okamžité přepínání mezi +F0 a −F0. Statický výpočet ⇒ napětí **přepíná mezi dvěma diskrétními hodnotami** podle stavu:

```
σ_levý(t)  : ─── +120,1 MPa (Stav A) ─── −305,6 MPa (Stav B) ─── ...
σ_pravý(t) : ─── −185,5 MPa (Stav A) ───   0 MPa   (Stav B) ─── ...
```

Viz `solutions/priklad_5E_vysledky.png`, panely 2. řádku.

> **Proč žádný přechod?** Dynamika (setrvačnost, vlnění) se zanedbává — řešíme jako kvazistatický problém. Reálná hřídel by měla rampu mikrosekund, ale pro únavu nehraje roli.

---

## 7. Stochastická analýza (Monte Carlo)

### 7.1 Vstupní rozdělení

Tolerance ±0,5 mm interpretována pravidlem 3σ ⇒ směrodatná odchylka:

$$\sigma_{\mathrm{dim}} = \frac{0{,}5}{3} \approx 0{,}167\ \mathrm{mm}$$

| Veličina | Rozdělení | Parametry |
|----------|-----------|-----------|
| D, d, r, L₁…L₅, x_F | Normální | μ = nominal, σ = 0,167 mm |
| F | Uniformní | ⟨140 000; 141 000⟩ N |

(Poloměr r ošetřen `np.maximum(..., 0.5)` — ochrana proti nesmyslné záporné hodnotě.)

### 7.2 Postup

Pro každou z **N = 100 000** realizací: vygenerovat náhodné rozměry → spočítat A_D, A_d, K_t, C_L, C_R → vyřešit Stav A i B → výsledné σ_L_max, σ_L_min, σ_R_min, σ_a, σ_m.

### 7.3 Výsledky

| Veličina | μ | σ | CoV | 95% CI |
|----------|---|---|-----|--------|
| σ_L_max [MPa] | +120,54 | 1,91 | 0,016 | [+116,9; +124,3] |
| σ_L_min [MPa] | −306,74 | 4,80 | 0,016 | [−316,3; −297,4] |
| σ_L_a   [MPa] | +213,64 | 3,35 | 0,016 | [+207,2; +220,3] |
| σ_R_min [MPa] | −186,20 | 2,91 | 0,016 | [−192,0; −180,6] |
| σ_R_a   [MPa] | +93,10  | 1,45 | 0,016 | [+90,3; +96,0] |
| K_t [-]       | 2,100   | 0,020 | 0,010 | [2,06; 2,14] |

**Variabilita napětí ≈ 1,6 %** — velmi nízká, protože tolerance ±0,5 mm na rozměrech řádu desítek mm je relativně malá.

**Kde se rozptyl bere:**
1. **A_d** — nejvíc (kvadratická závislost na d, σ ∝ 1/A_d).
2. **K_t** — citlivý na poloměr r (Neuberovo $\sqrt{(D-d)/r}$).
3. **F** — minimálně (úzká tolerance +1000/−0 N, jen 0,7 % nominálu).

---

## 8. Haighův diagram (σ_a vs σ_m) a kontrola únavy

### 8.1 Co Haigh ukazuje

Vodorovná osa: **střední napětí** σ_m. Svislá: **amplituda** σ_a. Každý zatěžovací stav je jeden bod.

**Goodmanova přímka** ohraničuje bezpečnou oblast:

$$\frac{\sigma_a}{\sigma_c} + \frac{|\sigma_m|}{R_e} = 1$$

s materiálovými konstantami:
- R_e = 500 MPa (mez kluzu)
- σ_c = 300 MPa (mez únavy v symetrickém střídavém cyklu)

Bod **pod** přímkou ⇒ vyhoví na únavu, **nad** ⇒ nevyhoví.

### 8.2 Naše body

| Vrub | σ_m [MPa] | σ_a [MPa] | σ_a + σ_c·|σ_m|/R_e | Vyhoví? |
|------|-----------|-----------|---------------------|---------|
| Levý  | −92,8 | 212,8 | 212,8 + 300·92,8/500 = 268,5 | < 300 ✓ těsně |
| Pravý | −92,8 | 92,8  | 92,8 + 55,7 = 148,5 | < 300 ✓ s rezervou |

Viz `solutions/priklad_5E_haigh.png` — bublina MC bodů se Goodmanovou přímkou.

> **Levý vrub je na hraně.** Při horší realizaci tolerance nebo nižší σ_c by mohl spadnout nad přímku.

---

## 9. Souhrn pro odprezentování (cheat sheet)

### 9.1 Co říct na úvod (1 minuta)

> „Mám axiálně zatíženou hřídel se dvěma zápichy. Vlevo pevné vetknutí, vpravo se opírá o stěnu — ale od stěny se může odlepit. Síla se střídá mezi ±140 kN. Cílem je najít napětí ve vrubech v čase a posoudit únavu."

### 9.2 Co kreslit na tabuli

1. **Schéma** s rozměry 200/10/400/10/200, D=50, d=35, r=5, x_F=500.
2. Šipky vazeb: vlevo vetknutí (oboustranné), vpravo „⊕→|" (jednostranný kontakt).
3. **Dva FBD** vedle sebe: Stav A (R_R aktivní), Stav B (R_R = 0).

### 9.3 Tři klíčové vzorce

1. **Reakce v Stavu A:** $R_R = -F\cdot C_L/(C_L+C_R)$ — z kompatibility.
2. **Lokální napětí:** $\sigma = K_t \cdot N/A_d$.
3. **Charakteristiky cyklu:** $\sigma_a = (\sigma_{\max}-\sigma_{\min})/2$, $\sigma_m = (\sigma_{\max}+\sigma_{\min})/2$.

### 9.4 Čtyři čísla, která musí padnout

- Stav A: $N_L = +55\ \mathrm{kN}$, $N_R = −85\ \mathrm{kN}$.
- Stav B: $N_L = −140\ \mathrm{kN}$, $N_R = 0$.
- $K_t = 2{,}10$ (Peterson Chart 2.19 pro D/d = 1,43, r/d = 0,143).
- Levý vrub: σ ∈ ⟨−305,6; +120,1⟩ MPa, σ_a = 212,8, σ_m = −92,8.

### 9.5 Možné otázky a odpovědi

**Q: Proč jsou dva stavy a ne jeden?**
A: Pravý kontakt je jednostranný — neumí táhnout. Když síla míří od stěny, hřídel se odlepí a úloha se zjednoduší (staticky určitá). Když míří do stěny, kontakt drží a úloha je 1× staticky neurčitá.

**Q: Proč pro K_t Peterson a ne Neuber?**
A: Neuber dá K_t ≈ 3,45, je to konzervativní mez (předpokládá ostrou trhlinu). Peterson je experimentálně kalibrovaný graf pro reálnou geometrii — přesnější. Konzervativní volba by byla bezpečná, ale příliš pesimistická.

**Q: Proč tak nízké CoV výstupu (1,6 %)?**
A: Rozměry mají tolerance řádově půl procenta nominálu (0,5/35 ≈ 1,4 %), navíc se ve vzorcích vyskytují s exponentem 1–2. Výsledné napětí proto kolísá podobně málo.

**Q: Která veličina nejvíc ovlivňuje rozptyl?**
A: Průřez A_d (skrz průměr d) a součinitel K_t (skrz poloměr r). Síla F skoro vůbec — má úzkou toleranci.

**Q: Proč je obě σ_m shodně −92,8 MPa?**
A: Pro pravý vrub: (0 + (−185,5))/2 = −92,75. Pro levý: (+120,1 + (−305,6))/2 = −92,75. Numericky shodné, vyplývá z toho, že amplitudy obou cyklů jsou symetrické kolem stejné průměrné kompresní hodnoty (důsledek vyvážených sil v obou stavech).

**Q: Vyhoví hřídel na únavu?**
A: Podle Goodmana ano — levý vrub má 268,5 MPa proti limitu 300 MPa, ale **rezerva je malá** (~10 %). Při horší toleranci nebo slabším materiálu by mohl spadnout.

**Q: Co kdyby kontakt byl oboustranný (přivařený)?**
A: Pak by Stav B vypadal stejně jako Stav A (jen se zápornou silou). Tlaková špička v levém vrubu by klesla z −305,6 na −120,1 MPa — hřídel by byla 2,5× méně namáhaná. Jednostranný kontakt je z hlediska únavy nepříznivý.
