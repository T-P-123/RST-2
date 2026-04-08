"""
Příklad 3E — Pravděpodobnost bezporuchového provozu klínových řemenů
====================================================================
Data:
  Provozní napětí S [MPa]: 223; 116; 158.5; 199; 136.5; 169.5; 267.5; 127; 184; 151
  Meze pevnosti R [MPa]: 211; 269.5; 192; 301.5; 220.5; 243.5; 182.5; 257; 234; 199.5; 216; 205

Úkol: Jaká je pravděpodobnost bezporuchového provozu?
P(bezporuchový provoz) = P(R > S) = P(R - S > 0)

Přístup:
1. Odhadnout parametry rozdělení S a R z dat
2. Analytický výpočet P(R > S) za předpokladu normálního rozdělení
3. Monte Carlo simulace
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# ============================================================
# DATA
# ============================================================

S_data = np.array([223, 116, 158.5, 199, 136.5, 169.5, 267.5, 127, 184, 151])
R_data = np.array([211, 269.5, 192, 301.5, 220.5, 243.5, 182.5, 257, 234, 199.5, 216, 205])

n_S = len(S_data)
n_R = len(R_data)

# ============================================================
# 1. STATISTICKÝ POPIS DAT
# ============================================================

print("=" * 60)
print("PŘÍKLAD 3E — BEZPORUCHOVÝ PROVOZ KLÍNOVÝCH ŘEMENŮ")
print("=" * 60)

# Provozní napětí S
S_mean = np.mean(S_data)
S_std = np.std(S_data, ddof=1)
S_cov = S_std / S_mean

print(f"\nProvozní napětí S (n={n_S}):")
print(f"  Střední hodnota: μ_S = {S_mean:.2f} MPa")
print(f"  Směrodatná odchylka: σ_S = {S_std:.2f} MPa")
print(f"  Variační koeficient: CoV_S = {S_cov:.4f}")
print(f"  Min = {S_data.min():.1f}, Max = {S_data.max():.1f} MPa")

# Mez pevnosti R
R_mean = np.mean(R_data)
R_std = np.std(R_data, ddof=1)
R_cov = R_std / R_mean

print(f"\nMez pevnosti R (n={n_R}):")
print(f"  Střední hodnota: μ_R = {R_mean:.2f} MPa")
print(f"  Směrodatná odchylka: σ_R = {R_std:.2f} MPa")
print(f"  Variační koeficient: CoV_R = {R_cov:.4f}")
print(f"  Min = {R_data.min():.1f}, Max = {R_data.max():.1f} MPa")

# Test normality (Shapiro-Wilk)
_, p_S = stats.shapiro(S_data)
_, p_R = stats.shapiro(R_data)
print(f"\nTest normality (Shapiro-Wilk):")
print(f"  S: p-value = {p_S:.4f} {'(normální ✓)' if p_S > 0.05 else '(ne normální ✗)'}")
print(f"  R: p-value = {p_R:.4f} {'(normální ✓)' if p_R > 0.05 else '(ne normální ✗)'}")

# ============================================================
# 2. ANALYTICKÝ VÝPOČET P(R > S) — normální rozdělení
# ============================================================

print("\n" + "=" * 60)
print("ANALYTICKÝ VÝPOČET (předpoklad normálního rozdělení)")
print("=" * 60)

# Z = R - S ~ N(μ_R - μ_S, sqrt(σ_R² + σ_S²))
Z_mean = R_mean - S_mean
Z_std = np.sqrt(R_std**2 + S_std**2)

print(f"\nRezerva Z = R - S:")
print(f"  μ_Z = μ_R - μ_S = {Z_mean:.2f} MPa")
print(f"  σ_Z = √(σ_R² + σ_S²) = {Z_std:.2f} MPa")

# Index spolehlivosti
beta = Z_mean / Z_std
print(f"\nIndex spolehlivosti: β = μ_Z / σ_Z = {beta:.4f}")

# Pravděpodobnost poruchy
P_failure = stats.norm.cdf(-beta)
P_reliability = 1 - P_failure

print(f"\nPravděpodobnost poruchy: P_f = Φ(-β) = {P_failure:.6f} = {P_failure*100:.4f}%")
print(f"Pravděpodobnost bezporuchového provozu: P_s = 1 - P_f = {P_reliability:.6f} = {P_reliability*100:.4f}%")

# ============================================================
# 3. MONTE CARLO SIMULACE
# ============================================================

N_sim = 1_000_000
np.random.seed(42)

# Generování vzorků z odhadnutých normálních rozdělení
R_mc = np.random.normal(R_mean, R_std, N_sim)
S_mc = np.random.normal(S_mean, S_std, N_sim)

Z_mc = R_mc - S_mc
P_failure_mc = np.sum(Z_mc <= 0) / N_sim
P_reliability_mc = 1 - P_failure_mc

print(f"\n" + "=" * 60)
print(f"MONTE CARLO SIMULACE (N = {N_sim:,})")
print("=" * 60)
print(f"P(porucha) = {P_failure_mc:.6f} = {P_failure_mc*100:.4f}%")
print(f"P(bezporuchový provoz) = {P_reliability_mc:.6f} = {P_reliability_mc*100:.4f}%")

# Porovnání s log-normálním rozdělením
print(f"\n" + "=" * 60)
print("POROVNÁNÍ S LOG-NORMÁLNÍM ROZDĚLENÍM")
print("=" * 60)

# Fit log-normálního rozdělení
# Pro log-normální: ln(X) ~ N(μ_ln, σ_ln)
# μ_ln = ln(μ) - 0.5*σ_ln², σ_ln² = ln(1 + CoV²)

sigma_ln_S = np.sqrt(np.log(1 + S_cov**2))
mu_ln_S = np.log(S_mean) - 0.5 * sigma_ln_S**2

sigma_ln_R = np.sqrt(np.log(1 + R_cov**2))
mu_ln_R = np.log(R_mean) - 0.5 * sigma_ln_R**2

print(f"S ~ LN(μ_ln={mu_ln_S:.4f}, σ_ln={sigma_ln_S:.4f})")
print(f"R ~ LN(μ_ln={mu_ln_R:.4f}, σ_ln={sigma_ln_R:.4f})")

# MC s log-normálním
R_mc_ln = np.random.lognormal(mu_ln_R, sigma_ln_R, N_sim)
S_mc_ln = np.random.lognormal(mu_ln_S, sigma_ln_S, N_sim)
Z_mc_ln = R_mc_ln - S_mc_ln

P_failure_ln = np.sum(Z_mc_ln <= 0) / N_sim
P_reliability_ln = 1 - P_failure_ln

print(f"P(bezporuchový provoz, log-norm.) = {P_reliability_ln:.6f} = {P_reliability_ln*100:.4f}%")

# ============================================================
# 4. GRAFY
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Příklad 3E — Pravděpodobnost bezporuchového provozu klínových řemenů',
             fontsize=13, fontweight='bold')

# Data histogramy
x_range = np.linspace(50, 400, 500)

ax = axes[0, 0]
ax.hist(S_data, bins=8, density=True, alpha=0.5, color='red', edgecolor='white', label='Data S')
ax.hist(R_data, bins=8, density=True, alpha=0.5, color='blue', edgecolor='white', label='Data R')
ax.plot(x_range, stats.norm.pdf(x_range, S_mean, S_std), 'r-', linewidth=2, label=f'S ~ N({S_mean:.0f}, {S_std:.0f})')
ax.plot(x_range, stats.norm.pdf(x_range, R_mean, R_std), 'b-', linewidth=2, label=f'R ~ N({R_mean:.0f}, {R_std:.0f})')
ax.set_xlabel('Napětí [MPa]')
ax.set_ylabel('Hustota')
ax.set_title('Rozdělení S (provozní napětí) a R (mez pevnosti)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Rezerva Z = R - S
ax = axes[0, 1]
ax.hist(Z_mc[:100000], bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
z_range = np.linspace(Z_mean - 4*Z_std, Z_mean + 4*Z_std, 500)
ax.plot(z_range, stats.norm.pdf(z_range, Z_mean, Z_std), 'r-', linewidth=2)
ax.axvline(x=0, color='black', linewidth=2, linestyle='--', label='Z = 0 (porucha)')
ax.fill_between(z_range[z_range < 0], stats.norm.pdf(z_range[z_range < 0], Z_mean, Z_std),
                alpha=0.3, color='red', label=f'P(porucha) = {P_failure:.4f}')
ax.set_xlabel('Z = R - S [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'Rezerva spolehlivosti Z, β = {beta:.3f}')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# QQ plot pro S
ax = axes[1, 0]
stats.probplot(S_data, dist="norm", plot=ax)
ax.set_title('QQ plot — Provozní napětí S')
ax.grid(True, alpha=0.3)

# QQ plot pro R
ax = axes[1, 1]
stats.probplot(R_data, dist="norm", plot=ax)
ax.set_title('QQ plot — Mez pevnosti R')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_3E_vysledky.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy do solutions/priklad_3E_vysledky.png")

# Souhrnná tabulka
print(f"\n" + "=" * 60)
print("SOUHRNNÁ TABULKA VÝSLEDKŮ")
print("=" * 60)
print(f"{'Metoda':<35} {'P(bezporuchový) [%]':>20}")
print("-" * 60)
print(f"{'Analyticky (normální)':<35} {P_reliability*100:>20.4f}")
print(f"{'Monte Carlo (normální)':<35} {P_reliability_mc*100:>20.4f}")
print(f"{'Monte Carlo (log-normální)':<35} {P_reliability_ln*100:>20.4f}")
