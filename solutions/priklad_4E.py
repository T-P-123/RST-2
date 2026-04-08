"""
Příklad 4E — Pravděpodobnost dosažení MS pružnosti a MS deformace
=================================================================
Součást s vrubem zatížená ohybovým momentem M.

Zadání:
  R_e = 500 MPa (mez kluzu)
  w_max = 2 mm (maximální dovolený průhyb)
  M = 100 N·m (ohybový moment)
  Tloušťka t = 15 mm

  Rozměry z obrázku:
  - Celková délka: 45 mm (horní šířka)
  - Zúžení: 3 mm (šířka vrubu/zářezu)
  - Výška zúžení: 10 mm
  - Celková výška: 6 mm (?)

  Reinterpretace obrázku:
  - Nosník s proměnným průřezem
  - Hlavní rozměry: šířka 45mm, vrub na 3mm, výšky 10mm a 6mm

  Stochastické veličiny: log-normální rozdělení, CoV = 0.1

Řešení:
  1. MS pružnosti: σ_max ≤ R_e
  2. MS deformace: w_max ≤ w_dov
  3. Citlivostní analýza
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRY
# ============================================================

# Střední hodnoty
M_mean = 100.0       # N·m = 100 000 N·mm
R_e_mean = 500.0     # MPa
w_max_mean = 2.0     # mm (dovolený průhyb)

# Geometrie součásti (z obrázku)
# Nosník se zářezem (vrubem)
# Šířka celková h1 = 45 mm (plný průřez)
# Šířka v místě vrubu h2 = 45 - 2*10 = 25 mm?
# Nebo: výška průřezu v nejužším místě
# Z obrázku: celková výška = 45mm, hloubka vrubu = 10mm na každé straně -> čistá výška = 25mm
# Šířka vrubu (v podélném směru) = 3mm
# Na pravé straně: výška = 6mm a 10mm

# Interpretuji průřez jako obdélníkový s vrubem:
# h = 45 mm — celková výška průřezu (plný)
# h_net = 45 - 2*10 = 25 mm — výška v místě vrubu?
# Hmm, z obrázku vyplývá jiná geometrie.
#
# Po bližším pohledu na obrázek 4E:
# - Součást tloušťky t = 15 mm
# - Vlevo širší (45 mm výška), vpravo užší
# - Vrub/zářez redukuje výšku
# - 3 mm = poloměr zaoblení vrubu
# - 10 mm = hloubka vrubu na jedné straně
# - 6 mm = hloubka vrubu na druhé straně
# - Čistá výška v místě vrubu: 45 - 10 - 6 = 29 mm

# Zjednodušení:
h_gross = 45.0    # mm — celková výška průřezu
notch_top = 10.0  # mm — hloubka horního vrubu
notch_bot = 6.0   # mm — hloubka dolního vrubu
h_net = h_gross - notch_top - notch_bot  # = 29 mm — čistá výška
r_notch = 3.0     # mm — poloměr zaoblení vrubu
t = 15.0          # mm — tloušťka

# Délka nosníku (odhadem z obrázku — konzola)
L = 100.0         # mm (typický rozměr)

# Součinitel koncentrace napětí (vrub)
# Pro obdélníkový průřez s vrubem na jedné straně:
# Kt závisí na h/h_net a r/h_net
# Použijeme Petersonovu aproximaci pro ohyb

def stress_concentration_factor(h_gross, h_net, r):
    """
    Součinitel koncentrace napětí pro nosník s vrubem
    (Peterson's approximation pro stepped bar v ohybu)
    Kt = 1 + A*(t/r)^B kde t = (h_gross - h_net)/2

    Pro oboustranný vrub v ohybu (notch):
    Zjednodušená formule Kt ≈ 1 + 2*sqrt(depth/r) (Neuber)
    """
    # Hloubka vrubu (bereme horší - hlubší)
    depth = max(notch_top, notch_bot)
    # Neuberova aproximace
    Kt = 1 + 2 * np.sqrt(depth / r)
    return Kt

Kt = stress_concentration_factor(h_gross, h_net, r_notch)

# Modul průřezu v místě vrubu
W_net = t * h_net**2 / 6  # mm³ (obdélníkový průřez)

# Moment setrvačnosti v místě vrubu
I_net = t * h_net**3 / 12  # mm⁴

E = 210000.0  # MPa — modul pružnosti oceli

print("=" * 60)
print("PŘÍKLAD 4E — MS PRUŽNOSTI A DEFORMACE SOUČÁSTI S VRUBEM")
print("=" * 60)
print(f"\nGeometrie:")
print(f"  Celková výška h = {h_gross} mm")
print(f"  Hloubka vrubu nahoře = {notch_top} mm")
print(f"  Hloubka vrubu dole = {notch_bot} mm")
print(f"  Čistá výška h_net = {h_net} mm")
print(f"  Poloměr vrubu r = {r_notch} mm")
print(f"  Tloušťka t = {t} mm")
print(f"  Kt (Neuber) = {Kt:.3f}")
print(f"  W_net = {W_net:.1f} mm³")
print(f"  I_net = {I_net:.1f} mm⁴")

# ============================================================
# 1. DETERMINISTICKÝ VÝPOČET
# ============================================================

M_Nmm = M_mean * 1000  # N·m -> N·mm

# Nominální napětí v místě vrubu
sigma_nom = M_Nmm / W_net
sigma_max = Kt * sigma_nom

print(f"\nDeterministický výpočet:")
print(f"  M = {M_mean} N·m = {M_Nmm} N·mm")
print(f"  σ_nom = M/W = {sigma_nom:.2f} MPa")
print(f"  σ_max = Kt × σ_nom = {sigma_max:.2f} MPa")
print(f"  R_e = {R_e_mean} MPa")
print(f"  Součinitel bezpečnosti k MS pružnosti: k = R_e/σ_max = {R_e_mean/sigma_max:.3f}")

# Průhyb konzolového nosníku: w = M*L²/(2*E*I)
# (pro konstantní moment po délce konzoly)
w_calc = M_Nmm * L**2 / (2 * E * I_net)

print(f"\n  Průhyb (konzola, L={L}mm): w = {w_calc:.4f} mm")
print(f"  Dovolený průhyb: w_dov = {w_max_mean} mm")
print(f"  Součinitel bezpečnosti k MS deformace: k = w_dov/w = {w_max_mean/w_calc:.3f}")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo (log-normální)
# ============================================================

N_sim = 500_000
CoV = 0.1
np.random.seed(42)

def lognormal_params(mean, cov):
    """Vrátí (mu_ln, sigma_ln) pro log-normální rozdělení."""
    sigma_ln = np.sqrt(np.log(1 + cov**2))
    mu_ln = np.log(mean) - 0.5 * sigma_ln**2
    return mu_ln, sigma_ln

# Parametry log-normálního rozdělení
mu_M, sig_M = lognormal_params(M_mean * 1000, CoV)    # N·mm
mu_Re, sig_Re = lognormal_params(R_e_mean, CoV)
mu_wmax, sig_wmax = lognormal_params(w_max_mean, CoV)
mu_h, sig_h = lognormal_params(h_net, CoV)
mu_t, sig_t = lognormal_params(t, CoV)
mu_r, sig_r = lognormal_params(r_notch, CoV)
mu_L, sig_L = lognormal_params(L, CoV)

# Generování vzorků
M_mc = np.random.lognormal(mu_M, sig_M, N_sim)
Re_mc = np.random.lognormal(mu_Re, sig_Re, N_sim)
wmax_mc = np.random.lognormal(mu_wmax, sig_wmax, N_sim)
h_mc = np.random.lognormal(mu_h, sig_h, N_sim)
t_mc = np.random.lognormal(mu_t, sig_t, N_sim)
r_mc = np.random.lognormal(mu_r, sig_r, N_sim)
L_mc = np.random.lognormal(mu_L, sig_L, N_sim)

# Výpočet pro každou realizaci
W_mc = t_mc * h_mc**2 / 6
I_mc = t_mc * h_mc**3 / 12
depth_mc = np.full(N_sim, max(notch_top, notch_bot))  # hloubka vrubu konstantní pro zjednodušení
Kt_mc = 1 + 2 * np.sqrt(depth_mc / r_mc)

sigma_nom_mc = M_mc / W_mc
sigma_max_mc = Kt_mc * sigma_nom_mc
w_mc = M_mc * L_mc**2 / (2 * E * I_mc)

# MS pružnosti: porucha když σ_max > R_e
g_yield = Re_mc - sigma_max_mc
P_yield_failure = np.sum(g_yield < 0) / N_sim
P_yield_ok = 1 - P_yield_failure

# MS deformace: porucha když w > w_max
g_deform = wmax_mc - w_mc
P_deform_failure = np.sum(g_deform < 0) / N_sim
P_deform_ok = 1 - P_deform_failure

print(f"\n" + "=" * 60)
print(f"STOCHASTICKÁ ANALÝZA (Monte Carlo, N={N_sim:,}, log-normální, CoV={CoV})")
print("=" * 60)

print(f"\nMS pružnosti (σ_max ≤ R_e):")
print(f"  μ(σ_max) = {np.mean(sigma_max_mc):.2f} MPa, σ = {np.std(sigma_max_mc):.2f} MPa")
print(f"  μ(R_e) = {np.mean(Re_mc):.2f} MPa")
print(f"  P(porucha) = {P_yield_failure:.6f} = {P_yield_failure*100:.4f}%")
print(f"  P(bezpečnost) = {P_yield_ok:.6f} = {P_yield_ok*100:.4f}%")
print(f"  β (index spolehlivosti) ≈ {-stats.norm.ppf(P_yield_failure):.4f}" if P_yield_failure > 0 else "  β → ∞")

print(f"\nMS deformace (w ≤ w_max):")
print(f"  μ(w) = {np.mean(w_mc):.4f} mm, σ = {np.std(w_mc):.4f} mm")
print(f"  μ(w_max) = {np.mean(wmax_mc):.4f} mm")
print(f"  P(porucha) = {P_deform_failure:.6f} = {P_deform_failure*100:.4f}%")
print(f"  P(bezpečnost) = {P_deform_ok:.6f} = {P_deform_ok*100:.4f}%")
print(f"  β (index spolehlivosti) ≈ {-stats.norm.ppf(P_deform_failure):.4f}" if P_deform_failure > 0 else "  β → ∞")

# ============================================================
# 3. CITLIVOSTNÍ ANALÝZA
# ============================================================

print(f"\n" + "=" * 60)
print("CITLIVOSTNÍ ANALÝZA")
print("=" * 60)

# Parciální derivace g = R_e - Kt*M/W
# Vliv jednotlivých proměnných na g_yield
variables = {
    'M': M_mc,
    'R_e': Re_mc,
    'h_net': h_mc,
    't': t_mc,
    'r': r_mc,
    'L': L_mc,
    'w_max': wmax_mc,
}

print("\nKorelace s funkcí poruchy g_yield = R_e - σ_max:")
for name, var in variables.items():
    corr = np.corrcoef(var, g_yield)[0, 1]
    print(f"  ρ(g_yield, {name:>5}) = {corr:+.4f}")

print("\nKorelace s funkcí poruchy g_deform = w_max - w:")
for name, var in variables.items():
    corr = np.corrcoef(var, g_deform)[0, 1]
    print(f"  ρ(g_deform, {name:>5}) = {corr:+.4f}")

# Směrové kosinusy (importance factors) — aproximace pomocí korelačních koeficientů
print("\nFaktory důležitosti (importance factors) pro MS pružnosti:")
corrs_yield = np.array([np.corrcoef(var, g_yield)[0, 1] for var in variables.values()])
alpha_sq = corrs_yield**2
alpha_sq_norm = alpha_sq / alpha_sq.sum()
for name, a2 in zip(variables.keys(), alpha_sq_norm):
    print(f"  α²({name:>5}) = {a2:.4f} ({a2*100:.1f}%)")

# ============================================================
# 4. GRAFY
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Příklad 4E — MS pružnosti a deformace součásti s vrubem\n'
             f'(Monte Carlo, N={N_sim:,}, log-normální, CoV={CoV})',
             fontsize=13, fontweight='bold')

# Histogram σ_max vs R_e
ax = axes[0, 0]
bins = np.linspace(0, max(np.percentile(sigma_max_mc, 99.9), R_e_mean*1.3), 100)
ax.hist(sigma_max_mc, bins=bins, density=True, alpha=0.6, color='red', label='σ_max')
ax.hist(Re_mc, bins=bins, density=True, alpha=0.6, color='blue', label='R_e')
ax.axvline(R_e_mean, color='blue', linestyle='--', alpha=0.7)
ax.axvline(np.mean(sigma_max_mc), color='red', linestyle='--', alpha=0.7)
ax.set_xlabel('Napětí [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'MS pružnosti: P(σ_max > R_e) = {P_yield_failure*100:.2f}%')
ax.legend()
ax.grid(True, alpha=0.3)

# Histogram w vs w_max
ax = axes[0, 1]
bins_w = np.linspace(0, max(np.percentile(w_mc, 99.9), w_max_mean*1.5), 100)
ax.hist(w_mc, bins=bins_w, density=True, alpha=0.6, color='red', label='w (průhyb)')
ax.hist(wmax_mc, bins=bins_w, density=True, alpha=0.6, color='blue', label='w_max (dovolený)')
ax.set_xlabel('Průhyb [mm]')
ax.set_ylabel('Hustota')
ax.set_title(f'MS deformace: P(w > w_max) = {P_deform_failure*100:.2f}%')
ax.legend()
ax.grid(True, alpha=0.3)

# Funkce poruchy g_yield
ax = axes[1, 0]
ax.hist(g_yield, bins=100, density=True, alpha=0.7, color='steelblue', edgecolor='white')
ax.axvline(0, color='red', linewidth=2, linestyle='--', label='g = 0 (porucha)')
ax.fill_between([g_yield.min(), 0], 0, 0.001, alpha=0.3, color='red', transform=ax.get_xaxis_transform())
ax.set_xlabel('g = R_e - σ_max [MPa]')
ax.set_ylabel('Hustota')
ax.set_title('Funkce poruchy — MS pružnosti')
ax.legend()
ax.grid(True, alpha=0.3)

# Citlivostní analýza — bar chart
ax = axes[1, 1]
names = list(variables.keys())
colors_bar = ['red' if c < 0 else 'blue' for c in corrs_yield]
ax.barh(names, alpha_sq_norm * 100, color=colors_bar, alpha=0.7, edgecolor='white')
ax.set_xlabel('Příspěvek k rozptylu [%]')
ax.set_title('Citlivostní analýza — MS pružnosti')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_4E_vysledky.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy do solutions/priklad_4E_vysledky.png")

# ============================================================
# 5. ANSYS APDL SKRIPT
# ============================================================

ansys_script = """
! =====================================================
! Příklad 4E — ANSYS APDL skript
! Součást s vrubem zatížená ohybovým momentem
! =====================================================

FINISH
/CLEAR

/PREP7

! Materiálové vlastnosti
ET,1,PLANE183           ! 2D 8-uzlový prvek
MP,EX,1,210000          ! Modul pružnosti [MPa]
MP,PRXY,1,0.3           ! Poissonův poměr

! Geometrie - parametry
h_total = 45            ! Celková výška [mm]
notch_top = 10          ! Hloubka horního vrubu [mm]
notch_bot = 6           ! Hloubka dolního vrubu [mm]
h_net = h_total - notch_top - notch_bot  ! Čistá výška
r_notch = 3             ! Poloměr zaoblení vrubu [mm]
thickness = 15          ! Tloušťka [mm]
L_beam = 100            ! Délka [mm]

! Klíčové body a plochy
! (zjednodušená geometrie - detaily závisí na přesném tvaru)
RECTNG,0,L_beam,0,h_total

! Mesh
AESIZE,ALL,1.0          ! Velikost prvku 1 mm
! Zjemnění u vrubu
! LREFINE,...

AMESH,ALL

! Okrajové podmínky
! Vetknutí na levém okraji
DL,4,,ALL,0

! Zatížení - moment na pravém okraji
! M = 100 N·m = 100000 N·mm
! Rozložení do lineárního napětí na pravém okraji
! σ = M*y/I, síla = σ * t * dy

/SOLU
ANTYPE,STATIC
SOLVE

/POST1
PLNSOL,S,EQV            ! Von Mises napětí
PLNSOL,U,SUM            ! Celkový posuv

! Výpis maximálních hodnot
NSORT,S,EQV
*GET,sigma_max,SORT,,MAX
NSORT,U,Y
*GET,w_max_fem,SORT,,MAX

/COM, Max von Mises stress = %sigma_max% MPa
/COM, Max deflection = %w_max_fem% mm

FINISH
"""

with open('/tmp/RST-2/solutions/priklad_4E_ansys.mac', 'w') as f:
    f.write(ansys_script)

print("ANSYS APDL skript uložen do solutions/priklad_4E_ansys.mac")
