"""
Příklad 4E — Pravděpodobnost dosažení MS pružnosti a MS deformace
=================================================================
Stupňovitý plochý prut zatížený konstantním ohybovým momentem M.
Geometrie podle interpretace konsensu (sage MCP):
  - 3 úseky výšek h: 45 → 30 → 10 mm
  - tloušťka t = 15 mm
  - rádiusy přechodů r1 = 3 mm (45→30), r2 = 6 mm (30→10)
  - kritický průřez: h3 = 10 mm

Zadání:
  R_e = 500 MPa, w_max = 2 mm, M = 100 N·m
  Stochastické veličiny: log-normální, CoV = 0.1

Řešení:
  1. Nominální napětí v jednotlivých sekcích
  2. Součinitelé tvaru K_t (Peterson, stupňovitý prut)
  3. MS pružnosti (FOSM lognormální)
  4. MS deformace (Mohrova analogie)
  5. Citlivostní analýza
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRY
# ============================================================

M_mean = 100.0       # N·m
R_e_mean = 500.0     # MPa
w_max_mean = 2.0     # mm
E = 210000.0         # MPa

# Geometrie stupňovitého prutu
h1 = 45.0    # mm
h2 = 30.0    # mm
h3 = 10.0    # mm — kritická sekce
r1 = 3.0     # mm — přechod 45→30
r2 = 6.0     # mm — přechod 30→10
t  = 15.0    # mm — tloušťka

# Délky úseků (odhad — v zadání nekótováno)
L1 = 60.0
L2 = 80.0
L3 = 60.0

# Součinitele tvaru (Peterson, stepped flat bar v ohybu)
# Vrub r1 (45→30): D/d = 1.5, r/d = 0.1 → Kt1 ≈ 1.68
# Vrub r2 (30→10): D/d = 3.0, r/d = 0.6 → Kt2 ≈ 1.15
Kt1 = 1.68
Kt2 = 1.15

# Pomocné průřezové charakteristiky
def W(h, t=t):
    return t * h**2 / 6.0

def I(h, t=t):
    return t * h**3 / 12.0

W1, W2, W3 = W(h1), W(h2), W(h3)
I1, I2, I3 = I(h1), I(h2), I(h3)

print("=" * 60)
print("PŘÍKLAD 4E — STUPŇOVITÝ PRUT V OHYBU (konsensus)")
print("=" * 60)
print(f"\nGeometrie:")
print(f"  h1 = {h1}, h2 = {h2}, h3 = {h3} mm")
print(f"  r1 = {r1}, r2 = {r2} mm,  t = {t} mm")
print(f"  L1 = {L1}, L2 = {L2}, L3 = {L3} mm (odhad)")
print(f"  W1 = {W1:.1f}, W2 = {W2:.1f}, W3 = {W3:.1f} mm³")
print(f"  I1 = {I1:.0f}, I2 = {I2:.0f}, I3 = {I3:.0f} mm⁴")
print(f"  Kt1 = {Kt1}, Kt2 = {Kt2}")

# ============================================================
# 1. DETERMINISTICKÝ VÝPOČET
# ============================================================

M_Nmm = M_mean * 1000

sig_nom1 = M_Nmm / W1
sig_nom2 = M_Nmm / W2
sig_nom3 = M_Nmm / W3

sig_max1 = Kt1 * sig_nom2   # napětí ve vrubu r1 (počítané k užšímu průřezu h2)
sig_max2 = Kt2 * sig_nom3   # napětí ve vrubu r2 (počítané k užšímu průřezu h3)

print(f"\nDeterministický výpočet (M = {M_mean} N·m = {M_Nmm} N·mm):")
print(f"  σ_nom v sekci 1 (h={h1}): {sig_nom1:.2f} MPa")
print(f"  σ_nom v sekci 2 (h={h2}): {sig_nom2:.2f} MPa")
print(f"  σ_nom v sekci 3 (h={h3}): {sig_nom3:.2f} MPa  ← kritická")
print(f"  σ_max u vrubu r1: Kt1·σ_nom2 = {sig_max1:.2f} MPa")
print(f"  σ_max u vrubu r2: Kt2·σ_nom3 = {sig_max2:.2f} MPa  ← rozhoduje")
print(f"  k = R_e/σ_max = {R_e_mean/sig_max2:.3f}")

# Průhyb na volném konci konzoly s konstantním M (vetknutí u h1, volný u h3):
# w = ∫₀^L M/(E·I(x))·(L−x) dx;  pro úsek [a,b] integral = ((L-a)²−(L-b)²)/2
L_tot = L1 + L2 + L3
def section_integral(a, b, L):
    return ((L - a)**2 - (L - b)**2) / 2.0

J1 = section_integral(0, L1, L_tot)
J2 = section_integral(L1, L1+L2, L_tot)
J3 = section_integral(L1+L2, L_tot, L_tot)

w_calc = (M_Nmm / E) * (J1/I1 + J2/I2 + J3/I3)

print(f"\n  Průhyb (volný konec): w = {w_calc:.4f} mm")
print(f"  w_max = {w_max_mean} mm  →  k = {w_max_mean/w_calc:.3f}")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo (log-normální)
# ============================================================

N_sim = 500_000
CoV = 0.1
np.random.seed(42)

def lognormal_params(mean, cov):
    sigma_ln = np.sqrt(np.log(1 + cov**2))
    mu_ln = np.log(mean) - 0.5 * sigma_ln**2
    return mu_ln, sigma_ln

def lognormal_sample(mean, cov, n):
    mu_ln, sig_ln = lognormal_params(mean, cov)
    return np.random.lognormal(mu_ln, sig_ln, n)

M_mc   = lognormal_sample(M_Nmm, CoV, N_sim)
Re_mc  = lognormal_sample(R_e_mean, CoV, N_sim)
wm_mc  = lognormal_sample(w_max_mean, CoV, N_sim)
h3_mc  = lognormal_sample(h3, CoV, N_sim)
t_mc   = lognormal_sample(t, CoV, N_sim)
Kt2_mc = lognormal_sample(Kt2, CoV, N_sim)
L_mc   = lognormal_sample(L1+L2+L3, CoV, N_sim)
E_mc   = lognormal_sample(E, CoV, N_sim)

# σ_max v kritickém vrubu r2
W3_mc = t_mc * h3_mc**2 / 6.0
sigma_max_mc = Kt2_mc * M_mc / W3_mc

# Stochastický průhyb stejným vzorcem jako deterministický (stochastické h3, t, E, M):
I3_mc = t_mc * h3_mc**3 / 12.0
I1_det = t_mc * h1**3 / 12.0
I2_det = t_mc * h2**3 / 12.0
w_mc = (M_mc / E_mc) * (J1/I1_det + J2/I2_det + J3/I3_mc)

# MS pružnosti
g_yield = Re_mc - sigma_max_mc
P_yield_failure = np.sum(g_yield < 0) / N_sim
P_yield_ok = 1 - P_yield_failure

# MS deformace
g_deform = wm_mc - w_mc
P_deform_failure = np.sum(g_deform < 0) / N_sim
P_deform_ok = 1 - P_deform_failure

beta_yield = -stats.norm.ppf(P_yield_failure) if 0 < P_yield_failure < 1 else float('nan')
beta_deform = -stats.norm.ppf(P_deform_failure) if 0 < P_deform_failure < 1 else float('nan')

print(f"\n" + "=" * 60)
print(f"STOCHASTICKÁ ANALÝZA (MC, N={N_sim:,}, log-normální, CoV={CoV})")
print("=" * 60)
print(f"\nMS pružnosti (σ_max ≤ R_e):")
print(f"  μ(σ_max) = {np.mean(sigma_max_mc):.2f} MPa, σ = {np.std(sigma_max_mc):.2f} MPa")
print(f"  P(porucha) = {P_yield_failure*100:.2f}%")
print(f"  β_yield ≈ {beta_yield:.3f}")

print(f"\nMS deformace (w ≤ w_max):")
print(f"  μ(w) = {np.mean(w_mc):.4f} mm, σ = {np.std(w_mc):.4f} mm")
print(f"  P(porucha) = {P_deform_failure*100:.4f}%")
print(f"  β_deform ≈ {beta_deform:.3f}")

# ============================================================
# 3. CITLIVOSTNÍ ANALÝZA
# ============================================================

variables_yield = {
    'h_3': h3_mc, 'M': M_mc, 'K_t2': Kt2_mc, 't': t_mc, 'R_e': Re_mc,
}
variables_deform = {
    'h_3': h3_mc, 'L': L_mc, 'M': M_mc, 't': t_mc, 'E': E_mc, 'w_max': wm_mc,
}

corrs_y = np.array([np.corrcoef(v, g_yield)[0, 1] for v in variables_yield.values()])
alpha_sq_y = corrs_y**2 / (corrs_y**2).sum()

corrs_d = np.array([np.corrcoef(v, g_deform)[0, 1] for v in variables_deform.values()])
alpha_sq_d = corrs_d**2 / (corrs_d**2).sum()

print("\nCitlivosti — MS pružnosti:")
for name, c, a2 in zip(variables_yield.keys(), corrs_y, alpha_sq_y):
    print(f"  ρ(g_y, {name:>5}) = {c:+.3f},  α² = {a2*100:.1f}%")

print("\nCitlivosti — MS deformace:")
for name, c, a2 in zip(variables_deform.keys(), corrs_d, alpha_sq_d):
    print(f"  ρ(g_d, {name:>5}) = {c:+.3f},  α² = {a2*100:.1f}%")

# ============================================================
# 4. GRAFY
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Příklad 4E — stupňovitý prut: MS pružnosti a deformace\n'
             f'(MC, N={N_sim:,}, log-normální, CoV={CoV})',
             fontsize=13, fontweight='bold')

ax = axes[0, 0]
bins = np.linspace(0, max(np.percentile(sigma_max_mc, 99.9), R_e_mean*1.3), 100)
ax.hist(sigma_max_mc, bins=bins, density=True, alpha=0.6, color='red', label='σ_max')
ax.hist(Re_mc, bins=bins, density=True, alpha=0.6, color='blue', label='R_e')
ax.axvline(R_e_mean, color='blue', linestyle='--', alpha=0.7)
ax.axvline(np.mean(sigma_max_mc), color='red', linestyle='--', alpha=0.7)
ax.set_xlabel('Napětí [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'MS pružnosti: P_f = {P_yield_failure*100:.2f}%')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[0, 1]
bins_w = np.linspace(0, max(np.percentile(w_mc, 99.9), w_max_mean*1.5), 100)
ax.hist(w_mc, bins=bins_w, density=True, alpha=0.6, color='red', label='w (průhyb)')
ax.hist(wm_mc, bins=bins_w, density=True, alpha=0.6, color='blue', label='w_max')
ax.set_xlabel('Průhyb [mm]'); ax.set_ylabel('Hustota')
ax.set_title(f'MS deformace: P_f = {P_deform_failure*100:.4f}%')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 0]
ax.hist(g_yield, bins=100, density=True, alpha=0.7, color='steelblue', edgecolor='white')
ax.axvline(0, color='red', linewidth=2, linestyle='--', label='g = 0 (porucha)')
ax.set_xlabel('g = R_e − σ_max [MPa]'); ax.set_ylabel('Hustota')
ax.set_title('Funkce poruchy — MS pružnosti')
ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1, 1]
names_y = list(variables_yield.keys())
colors_y = ['red' if c < 0 else 'blue' for c in corrs_y]
ax.barh(names_y, alpha_sq_y * 100, color=colors_y, alpha=0.7, edgecolor='white')
ax.set_xlabel('Příspěvek k rozptylu [%]')
ax.set_title('Citlivostní analýza — MS pružnosti')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/tomas/Projects/RST/solutions/priklad_4E_vysledky.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy do solutions/priklad_4E_vysledky.png")

# Souhrn klíčových čísel pro tex:
print("\n" + "=" * 60)
print("SOUHRN PRO REPORT:")
print("=" * 60)
print(f"  σ_nom,3 = {sig_nom3:.1f} MPa")
print(f"  K_t2 = {Kt2}")
print(f"  σ_max = {sig_max2:.1f} MPa")
print(f"  k = {R_e_mean/sig_max2:.3f}")
print(f"  P_f (MS pružnosti) = {P_yield_failure*100:.2f}%")
print(f"  β_yield = {beta_yield:.3f}")
print(f"  w_det = {w_calc:.3f} mm")
print(f"  P_f (MS deformace) = {P_deform_failure*100:.4f}%")
print(f"  β_deform = {beta_deform:.3f}")
