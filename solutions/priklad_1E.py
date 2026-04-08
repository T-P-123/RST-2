"""
Příklad 1E — Průběh vnitřních sil a momentů na nosníku
======================================================
Prostě podepřený nosník s převislým koncem.

Podpory:
  - A (x=0): kloubová podpora (pin) — reakce F_Ax, F_Ay
  - B (x=5m): válcová podpora (roller) — reakce F_By
  (kolečko u x=2m je jen místo aplikace momentu, NE vnitřní kloub!)

Zatížení:
  - Koncentrovaný moment M₀ = 20 kN·m v x=2m (proti směru hodinových ručiček)
  - Bodová síla F = 8 kN v x=3m (směr dolů)
  - Spojité zatížení q = 15 kN/m na intervalu x ∈ [5; 8] m (směr dolů)

Celková délka: 2+1+2+3 = 8 m (převislý konec 3m za podporou B)
Stochastické zatížení: normální rozdělení, CoV = 0.1

Znaménková konvence:
  - Fy kladné nahoru
  - M(x) = Σ F_{y,i}·(x - x_i) - Σ M_{CCW,j}  (ohybové momenty, prohnutí dolů kladné)
  - V(x) = Σ F_{y,i} (posouvající síla, kladná nahoru na levém řezu)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ============================================================
# 1. DETERMINISTICKÉ ŘEŠENÍ
# ============================================================

L_total = 8.0   # m
x_B = 5.0       # m — pozice podpory B (roller)

# Zatížení (střední hodnoty)
M0 = 20.0       # kN·m — koncentrovaný moment v x=2m (CCW kladný)
F = 8.0          # kN — bodová síla v x=3m (dolů)
q = 15.0         # kN/m — spojité zatížení od x=5m do x=8m (dolů)

x_M0 = 2.0      # m — pozice koncentrovaného momentu
x_F = 3.0        # m — pozice bodové síly
x_q_start = 5.0  # m
x_q_end = 8.0    # m


def solve_beam(M0, F, q, x_B=5.0, x_F=3.0, x_M0=2.0,
               x_q_start=5.0, x_q_end=8.0):
    """
    Prostě podepřený nosník: pin v A (x=0), roller v B (x=x_B).
    3 neznámé (F_Ay, F_Ax, F_By), 3 rovnice rovnováhy.
    """
    L_q = x_q_end - x_q_start
    F_q = q * L_q
    x_q_cg = x_q_start + L_q / 2

    F_Ax = 0.0  # žádné horizontální zatížení

    # ΣM_A = 0 (CCW kladné):
    # +M0 - F*x_F + F_By*x_B - F_q*x_q_cg = 0
    F_By = (F * x_F - M0 + F_q * x_q_cg) / x_B

    # ΣFy = 0:
    F_Ay = F + F_q - F_By

    return F_Ay, F_Ax, F_By


def compute_internal_forces(x_arr, F_Ay, F_Ax, F_By,
                             M0, F, q, x_M0=2.0, x_B=5.0, x_F=3.0,
                             x_q_start=5.0, x_q_end=8.0):
    """
    N(x), V(x), M(x) po délce nosníku.
    M(x) = Σ F_{y,i}·(x - x_i) - Σ M_{CCW,j}  (sagging positive)
    V(x) = Σ F_{y,i}  (upward positive on left cut face)
    """
    N = np.zeros_like(x_arr)
    V = np.zeros_like(x_arr)
    M = np.zeros_like(x_arr)

    for i, x in enumerate(x_arr):
        # Normálová síla
        n = 0.0

        # Posouvající síla — součet svislých sil nalevo od řezu
        v = F_Ay
        # Ohybový moment
        m = F_Ay * x

        # Koncentrovaný moment v x_M0 (CCW → odečteme)
        if x >= x_M0:
            m -= M0

        # Bodová síla F (dolů = záporná Fy)
        if x >= x_F:
            v -= F
            m -= F * (x - x_F)

        # Podpora B
        if x >= x_B:
            v += F_By
            m += F_By * (x - x_B)

        # Spojité zatížení (dolů = záporná Fy)
        if x > x_q_start:
            x_eff = min(x, x_q_end)
            dx = x_eff - x_q_start
            v -= q * dx
            m -= q * dx * (x - x_q_start - dx / 2)

        N[i] = n
        V[i] = v
        M[i] = m

    return N, V, M


# Deterministické řešení
F_Ay, F_Ax, F_By = solve_beam(M0, F, q)

print("=" * 60)
print("PŘÍKLAD 1E — DETERMINISTICKÉ ŘEŠENÍ")
print("=" * 60)
print(f"Podpora A (x=0): kloubová (pin)")
print(f"Podpora B (x=5): válcová (roller)")
print(f"Moment 20 kN·m v x=2m, síla 8 kN v x=3m, q=15 kN/m na [5,8]m")
print(f"\nReakce:")
print(f"  F_Ay = {F_Ay:.2f} kN")
print(f"  F_Ax = {F_Ax:.2f} kN")
print(f"  F_By = {F_By:.2f} kN")
print()

# Kontrola
F_q_total = q * (x_q_end - x_q_start)
x_q_cg = x_q_start + (x_q_end - x_q_start) / 2

print(f"Kontroly:")
sum_Fy = F_Ay + F_By - F - F_q_total
print(f"  ΣFy = {sum_Fy:.6f} kN (≈ 0)")

sum_MA = M0 - F * x_F + F_By * x_B - F_q_total * x_q_cg
print(f"  ΣM_A = {sum_MA:.6f} kN·m (≈ 0)")

# Kontrola ΣM_B
sum_MB_cross = (0 - x_B) * F_Ay + M0 + (x_F - x_B) * (-F) + (x_q_cg - x_B) * (-F_q_total)
print(f"  ΣM_B = {sum_MB_cross:.6f} kN·m (≈ 0)")

# Výpočet průběhů
x = np.linspace(0, L_total, 2000)
N_det, V_det, M_det = compute_internal_forces(x, F_Ay, F_Ax, F_By, M0, F, q)

# Kontrola M na volném konci
print(f"  M(8) = {M_det[-1]:.6f} kN·m (≈ 0 — volný konec)")
print(f"  V(8) = {V_det[-1]:.6f} kN (≈ 0 — volný konec)")

# Klíčové hodnoty
print(f"\nKlíčové hodnoty:")
print(f"  V_max = {np.max(V_det):.2f} kN")
print(f"  V_min = {np.min(V_det):.2f} kN")
print(f"  M_max = {np.max(M_det):.2f} kN·m")
print(f"  M_min = {np.min(M_det):.2f} kN·m")

# Klíčové body M diagramu
print(f"\n  M(0) = {M_det[0]:.2f} kN·m (pin → M=0)")
print(f"  M(2⁻) ≈ {F_Ay * 2:.2f} kN·m")
print(f"  M(2⁺) ≈ {F_Ay * 2 - M0:.2f} kN·m (skok -M₀)")
print(f"  M(3) = {F_Ay * 3 - M0:.2f} kN·m")
print(f"  M(5) = {F_Ay * 5 - M0 - F * 2:.2f} kN·m")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo
# ============================================================

N_sim = 100_000
CoV = 0.1

np.random.seed(42)
M0_samples = np.random.normal(M0, M0 * CoV, N_sim)
F_samples = np.random.normal(F, F * CoV, N_sim)
q_samples = np.random.normal(q, q * CoV, N_sim)

F_Ay_mc = np.zeros(N_sim)
F_By_mc = np.zeros(N_sim)

for i in range(N_sim):
    va, ha, vb = solve_beam(M0_samples[i], F_samples[i], q_samples[i])
    F_Ay_mc[i] = va
    F_By_mc[i] = vb

# Obálky průběhů
N_plot = 1000
x_plot = np.linspace(0, L_total, 500)
V_env_max = np.full_like(x_plot, -np.inf)
V_env_min = np.full_like(x_plot, np.inf)
M_env_max = np.full_like(x_plot, -np.inf)
M_env_min = np.full_like(x_plot, np.inf)

for i in range(N_plot):
    va, ha, vb = solve_beam(M0_samples[i], F_samples[i], q_samples[i])
    _, Vi, Mi = compute_internal_forces(x_plot, va, ha, vb,
                                         M0_samples[i], F_samples[i], q_samples[i])
    V_env_max = np.maximum(V_env_max, Vi)
    V_env_min = np.minimum(V_env_min, Vi)
    M_env_max = np.maximum(M_env_max, Mi)
    M_env_min = np.minimum(M_env_min, Mi)

print("\n" + "=" * 60)
print(f"STOCHASTICKÁ ANALÝZA (Monte Carlo, N={N_sim:,})")
print("=" * 60)
print(f"F_Ay:  μ = {np.mean(F_Ay_mc):.2f} kN,  σ = {np.std(F_Ay_mc):.2f} kN,  "
      f"CoV = {np.std(F_Ay_mc)/abs(np.mean(F_Ay_mc)):.4f}")
print(f"F_By:  μ = {np.mean(F_By_mc):.2f} kN,  σ = {np.std(F_By_mc):.2f} kN,  "
      f"CoV = {np.std(F_By_mc)/abs(np.mean(F_By_mc)):.4f}")

# ============================================================
# 3. GRAFY
# ============================================================

fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.suptitle('Příklad 1E — Průběh vnitřních sil a momentů\n'
             'Prostě podepřený nosník s převislým koncem (pin A + roller B)\n'
             f'(deterministický + stochastický obal, CoV=0.1)',
             fontsize=13, fontweight='bold')

# Značky
for ax in axes:
    ax.axvline(x=0, color='green', linestyle='--', alpha=0.5)
    ax.axvline(x=x_B, color='red', linestyle='--', alpha=0.5)
    ax.axvline(x=x_M0, color='orange', linestyle=':', alpha=0.4)
    ax.axvline(x=x_F, color='purple', linestyle=':', alpha=0.4)

# Normálová síla
axes[0].fill_between(x, 0, N_det, alpha=0.3, color='blue')
axes[0].plot(x, N_det, 'b-', linewidth=2, label='N(x)')
axes[0].axhline(y=0, color='k', linewidth=0.5)
axes[0].set_ylabel('N [kN]')
axes[0].set_title('Normálová síla N(x)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(-1, 1)

# Posouvající síla
axes[1].fill_between(x_plot, V_env_min, V_env_max, alpha=0.2, color='red',
                      label=f'Stochastický obal (N={N_plot})')
axes[1].fill_between(x, 0, V_det, alpha=0.3, color='blue')
axes[1].plot(x, V_det, 'b-', linewidth=2, label='V(x) deterministický')
axes[1].axhline(y=0, color='k', linewidth=0.5)
axes[1].set_ylabel('V [kN]')
axes[1].set_title('Posouvající síla V(x)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Ohybový moment
axes[2].fill_between(x_plot, M_env_min, M_env_max, alpha=0.2, color='red',
                      label=f'Stochastický obal (N={N_plot})')
axes[2].fill_between(x, 0, M_det, alpha=0.3, color='blue')
axes[2].plot(x, M_det, 'b-', linewidth=2, label='M(x) deterministický')
axes[2].axhline(y=0, color='k', linewidth=0.5)
axes[2].set_ylabel('M [kN·m]')
axes[2].set_xlabel('x [m]')
axes[2].set_title('Ohybový moment M(x)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

# Popisky podpor
for ax in axes:
    ylim = ax.get_ylim()
    ax.text(0, ylim[1]*0.95, ' A (pin)', fontsize=9, color='green', va='top')
    ax.text(x_B, ylim[1]*0.95, ' B (roller)', fontsize=9, color='red', va='top')

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_1E_diagram.png', dpi=150, bbox_inches='tight')
plt.close()

# Histogramy reakcí
fig2, axes2 = plt.subplots(1, 2, figsize=(12, 5))
fig2.suptitle('Příklad 1E — Histogramy reakcí (Monte Carlo)',
              fontsize=13, fontweight='bold')

axes2[0].hist(F_Ay_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes2[0].axvline(F_Ay, color='red', linewidth=2, linestyle='--', label=f'Determin. = {F_Ay:.2f}')
axes2[0].set_xlabel('F_Ay [kN]')
axes2[0].set_title('Reakce F_Ay')
axes2[0].legend()

axes2[1].hist(F_By_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes2[1].axvline(F_By, color='red', linewidth=2, linestyle='--', label=f'Determin. = {F_By:.2f}')
axes2[1].set_xlabel('F_By [kN]')
axes2[1].set_title('Reakce F_By')
axes2[1].legend()

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_1E_histogramy.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy.")
