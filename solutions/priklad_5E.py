"""
Příklad 5E — Časový průběh napětí ve vrubech
============================================
Součást se dvěma zápichy, na jedné straně přivařena k základnímu rámu,
na druhé straně se ho dotýká.

Zadání:
  - Zatížena souměrně střídavou silou F = +1000 / -0 N
    (míněno pulzující: F kmitá mezi 0 a 1000 N)
  - Všechny rozměry ± 0.5 mm
  - Rozměry z obrázku:
    - Celková délka: 500 mm
    - Průměry: φ50 (velký), φ35? (malý), zápichy r5 a d=0 (?)
    - Síla aplikována na konci: F = 1.4×10⁵ N? Ne...

Reinterpretace obrázku 5E:
  Hřídel/tyč se dvěma zápichy (stress raisers):
  - Celková délka L = 500 mm
  - Průměr D = 50 mm (hlavní průměr)
  - Průměr d = 35 mm (v místě zápichu)
  - Poloměr zápichu r = 5 mm
  - Síla F střídavá: 0 až 1000 N (tahová)
  - Předpětí/lisovací síla: 1.4 × 10⁵ N (? — z obrázku "1.4·10⁵N")

Hmm, po dalším přezkoumání obrázku:
  - Součást je hřídel s:
    - D = 50 mm (velký průměr)
    - d = 35 mm (průměr v zápichu/zúžení)
    - Zápichy s poloměrem r = 5 mm
    - Délka 500 mm
    - Vetknutí na levé straně (svár), na pravé se dotýká rámu
    - Zatížení: osová střídavá síla F oscilující 0 → +1000 N
    - Předpětí z lisování: 1.4·10⁵ N

Přístup:
  1. Výpočet nominálního napětí
  2. Součinitel koncentrace napětí Kt v zápichu
  3. Časový průběh napětí σ(t) = Kt × F(t)/A
  4. Stochastická analýza (rozměry ± 0.5 mm → normální, CoV)
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRY
# ============================================================

# Geometrie (střední hodnoty)
D = 50.0          # mm — velký průměr
d = 35.0          # mm — průměr v zápichu
r = 5.0           # mm — poloměr zápichu
L = 500.0         # mm — délka

# Zatížení
F_max = 1000.0    # N — maximální síla (pulzující 0 → F_max)
F_min = 0.0       # N — minimální síla
F_pretension = 1.4e5  # N — předpětí (z obrázku)

# Tolerance rozměrů
tol = 0.5         # mm — ±0.5 mm

# ============================================================
# SOUČINITEL KONCENTRACE NAPĚTÍ
# ============================================================

def Kt_stepped_shaft_tension(D, d, r):
    """
    Součinitel koncentrace napětí pro odstupňovaný hřídel v tahu
    (Peterson's approximation)
    Kt = C1 + C2*(2r/D_small) + C3*(2r/D_small)² + C4*(2r/D_small)³
    Pro D/d ≈ 1.0-6.0 a r/d = 0.01-0.3
    Zjednodušená Neuberova formule pro zápichy
    """
    t_depth = (D - d) / 2  # hloubka zápichu
    # Zjednodušená formule
    Kt = 1 + 2 * np.sqrt(t_depth / r)
    # Přesnější formule pro kruhový zápich v tahu:
    ratio_rd = r / d
    ratio_Dd = D / d
    # Peterson (pro 1.01 ≤ D/d ≤ 6.0):
    if ratio_Dd <= 2.0:
        C1 = 0.926 + 1.157*np.sqrt(ratio_rd) - 0.099*ratio_rd
        C2 = 0.012 - 3.036*np.sqrt(ratio_rd) + 0.961*ratio_rd
        C3 = -0.302 + 3.977*np.sqrt(ratio_rd) - 1.744*ratio_rd
        C4 = 0.365 - 2.098*np.sqrt(ratio_rd) + 0.878*ratio_rd
    else:
        # Fallback to Neuber
        return 1 + 2 * np.sqrt(t_depth / r)

    t_over_r = (D - d) / (2 * r)
    if t_over_r > 0:
        Kt_pet = C1 + C2/np.sqrt(t_over_r) + C3/t_over_r + C4/(t_over_r**1.5)
    else:
        Kt_pet = 1.0
    return max(Kt_pet, 1.0)


# Výpočet Kt
t_depth = (D - d) / 2
Kt_neuber = 1 + 2 * np.sqrt(t_depth / r)

# Plocha průřezu v zápichu
A_d = np.pi * d**2 / 4

print("=" * 60)
print("PŘÍKLAD 5E — ČASOVÝ PRŮBĚH NAPĚTÍ VE VRUBECH")
print("=" * 60)
print(f"\nGeometrie:")
print(f"  D = {D} mm, d = {d} mm, r = {r} mm")
print(f"  Hloubka zápichu t = {t_depth} mm")
print(f"  Plocha v zápichu A_d = {A_d:.2f} mm²")
print(f"  Kt (Neuber) = {Kt_neuber:.3f}")

# ============================================================
# 1. DETERMINISTICKÝ VÝPOČET
# ============================================================

print(f"\n{'='*60}")
print("DETERMINISTICKÝ VÝPOČET")
print("=" * 60)

# Nominální napětí (tah/tlak)
sigma_nom_max = F_max / A_d
sigma_nom_min = F_min / A_d
sigma_pretension = F_pretension / A_d

# Napětí s koncentrací
sigma_max = Kt_neuber * sigma_nom_max
sigma_min = Kt_neuber * sigma_nom_min

# Střední napětí a amplituda
sigma_m = (sigma_max + sigma_min) / 2
sigma_a = (sigma_max - sigma_min) / 2

print(f"\nBez předpětí:")
print(f"  σ_nom_max = F_max/A = {sigma_nom_max:.3f} MPa")
print(f"  σ_max = Kt × σ_nom_max = {sigma_max:.3f} MPa")
print(f"  σ_min = {sigma_min:.3f} MPa")
print(f"  σ_m (střední) = {sigma_m:.3f} MPa")
print(f"  σ_a (amplituda) = {sigma_a:.3f} MPa")
print(f"  R (poměr napětí) = σ_min/σ_max = {sigma_min/(sigma_max+1e-10):.3f}")

print(f"\nS předpětím (F_0 = {F_pretension:.0f} N):")
sigma_pretension_max = Kt_neuber * (F_pretension + F_max) / A_d
sigma_pretension_min = Kt_neuber * (F_pretension + F_min) / A_d
sigma_m_pre = (sigma_pretension_max + sigma_pretension_min) / 2
sigma_a_pre = (sigma_pretension_max - sigma_pretension_min) / 2
print(f"  σ_max = {sigma_pretension_max:.2f} MPa")
print(f"  σ_min = {sigma_pretension_min:.2f} MPa")
print(f"  σ_m = {sigma_m_pre:.2f} MPa")
print(f"  σ_a = {sigma_a_pre:.2f} MPa")

# ============================================================
# 2. ČASOVÝ PRŮBĚH NAPĚTÍ
# ============================================================

# Simulace 5 cyklů
freq = 1.0  # Hz (libovolná frekvence pro zobrazení)
t_total = 5.0 / freq  # 5 cyklů
dt = 0.001
t_arr = np.arange(0, t_total, dt)

# Pulzující zatížení: F(t) = F_max * (1 - cos(2πft))/2
# F osciluje od 0 do F_max
F_t = F_max * (1 - np.cos(2 * np.pi * freq * t_arr)) / 2

# Napětí v zápichu 1 (Kt_neuber)
sigma_1_t = Kt_neuber * F_t / A_d

# Zápichy na obou místech mohou mít různé Kt
# Zápich 2: jiný poloměr nebo hloubka?
# Z obrázku: r5 a d=0 — zápich 2 má r=5mm
# Předpokládáme oba zápichy stejné (r=5mm)
sigma_2_t = sigma_1_t  # Stejné Kt → stejný průběh

print(f"\n{'='*60}")
print("ČASOVÝ PRŮBĚH NAPĚTÍ")
print("=" * 60)
print(f"  Frekvence: {freq} Hz")
print(f"  Počet cyklů: 5")
print(f"  σ kolísá od {sigma_min:.3f} do {sigma_max:.3f} MPa (bez předpětí)")

# ============================================================
# 3. STOCHASTICKÁ ANALÝZA
# ============================================================

N_sim = 100_000
np.random.seed(42)

# Rozměry s tolerancí ±0.5mm → σ ≈ 0.5/3 ≈ 0.167 mm (3σ pravidlo)
sigma_dim = tol / 3

D_mc = np.random.normal(D, sigma_dim, N_sim)
d_mc = np.random.normal(d, sigma_dim, N_sim)
r_mc = np.random.normal(r, sigma_dim, N_sim)
r_mc = np.maximum(r_mc, 0.5)  # min poloměr

# Síla: F = +1000 -0 N → normální? Předpokládám F_max s jistou variabilitou
# "F +1000 -0 N" — asymetrické → F ∈ [0, 1000] se střední hodnotou 1000
F_mc = np.random.normal(F_max, F_max * 0.05, N_sim)  # malá variabilita síly

# Výpočty
t_depth_mc = (D_mc - d_mc) / 2
t_depth_mc = np.maximum(t_depth_mc, 0.1)
Kt_mc = 1 + 2 * np.sqrt(t_depth_mc / r_mc)
A_mc = np.pi * d_mc**2 / 4

sigma_max_mc = Kt_mc * F_mc / A_mc
sigma_a_mc = sigma_max_mc / 2  # pro pulzující (R=0)
sigma_m_mc = sigma_max_mc / 2

print(f"\n{'='*60}")
print(f"STOCHASTICKÁ ANALÝZA (N={N_sim:,})")
print("=" * 60)
print(f"  σ_max: μ = {np.mean(sigma_max_mc):.3f} MPa, σ = {np.std(sigma_max_mc):.3f} MPa, "
      f"CoV = {np.std(sigma_max_mc)/np.mean(sigma_max_mc):.4f}")
print(f"  σ_a:   μ = {np.mean(sigma_a_mc):.3f} MPa, σ = {np.std(sigma_a_mc):.3f} MPa")
print(f"  Kt:    μ = {np.mean(Kt_mc):.3f}, σ = {np.std(Kt_mc):.3f}")

# Kvantily
for q_val in [0.025, 0.5, 0.975]:
    print(f"  σ_max ({q_val*100:.1f}%) = {np.quantile(sigma_max_mc, q_val):.3f} MPa")

# ============================================================
# 4. GRAFY
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Příklad 5E — Časový průběh napětí ve vrubech\n'
             'Pulzující zatížení F = 0→1000 N, zápichy D=50/d=35 mm, r=5 mm',
             fontsize=13, fontweight='bold')

# Časový průběh síly
ax = axes[0, 0]
ax.plot(t_arr, F_t, 'b-', linewidth=1.5)
ax.set_xlabel('Čas [s]')
ax.set_ylabel('F [N]')
ax.set_title('Zatěžující síla F(t)')
ax.grid(True, alpha=0.3)
ax.set_ylim(-100, F_max * 1.2)

# Časový průběh napětí v zápichu
ax = axes[0, 1]
ax.plot(t_arr, sigma_1_t, 'r-', linewidth=1.5, label='σ(t) v zápichu')
ax.axhline(sigma_max, color='red', linestyle='--', alpha=0.5, label=f'σ_max = {sigma_max:.2f} MPa')
ax.axhline(sigma_m, color='green', linestyle='--', alpha=0.5, label=f'σ_m = {sigma_m:.2f} MPa')
ax.fill_between(t_arr, sigma_m - sigma_a, sigma_m + sigma_a, alpha=0.1, color='red')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title('Napětí v zápichu σ(t)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Histogram σ_max (stochastický)
ax = axes[1, 0]
ax.hist(sigma_max_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
ax.axvline(sigma_max, color='red', linewidth=2, linestyle='--',
           label=f'Determin. = {sigma_max:.3f} MPa')
ax.set_xlabel('σ_max [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'Rozložení maximálního napětí (N={N_sim:,})')
ax.legend()
ax.grid(True, alpha=0.3)

# Stochastický obal časového průběhu
ax = axes[1, 1]
# Několik realizací
n_curves = 50
for i in range(n_curves):
    F_t_i = F_mc[i] * (1 - np.cos(2 * np.pi * freq * t_arr)) / 2
    sigma_t_i = Kt_mc[i] * F_t_i / A_mc[i]
    ax.plot(t_arr, sigma_t_i, 'b-', alpha=0.1, linewidth=0.5)

ax.plot(t_arr, sigma_1_t, 'r-', linewidth=2, label='Deterministický')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title(f'Stochastický obal σ(t) ({n_curves} realizací)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_5E_vysledky.png', dpi=150, bbox_inches='tight')
plt.close()

# Haighův diagram
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))
ax2.set_title('Příklad 5E — Haighův diagram (σ_a vs σ_m)', fontsize=13, fontweight='bold')

# Scatter stochastických realizací
ax2.scatter(sigma_m_mc[:5000], sigma_a_mc[:5000], alpha=0.1, s=5, color='blue',
            label='Stochastické realizace')
ax2.plot(sigma_m, sigma_a, 'ro', markersize=10, zorder=5, label='Deterministický bod')

# Goodmanova přímka (R_e = 500 MPa odhadem, σ_c = 300 MPa odhadem)
Re = 500  # MPa
sigma_c = 300  # MPa — mez únavy (odhad)
sm_line = np.linspace(0, Re, 100)
sa_goodman = sigma_c * (1 - sm_line / Re)
ax2.plot(sm_line, sa_goodman, 'g--', linewidth=2, label=f'Goodman (R_e={Re}, σ_c={sigma_c})')

ax2.set_xlabel('σ_m [MPa]')
ax2.set_ylabel('σ_a [MPa]')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, max(Re, np.max(sigma_m_mc[:5000])) * 1.1)
ax2.set_ylim(0, max(sigma_c, np.max(sigma_a_mc[:5000])) * 1.1)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_5E_haigh.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy do solutions/priklad_5E_vysledky.png a priklad_5E_haigh.png")
