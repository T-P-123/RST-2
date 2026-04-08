"""
Příklad 1E — Průběh vnitřních sil a momentů na nosníku
======================================================
Nosník s vetknutím (A), vnitřním kloubem, válcovou podporou (B).
Zatížení:
  - Koncentrovaný moment 20 kN·m (u kloubu, x=2m)
  - Bodová síla 8 kN (x=3m)
  - Spojité zatížení 15 kN/m (od x=5m do x=8m)
Podpory:
  - A (x=0): Vetknutí (V_A, H_A, M_A)
  - Kloub (x=2m): M=0 podmínka
  - B (x=5m): Válcová podpora (V_B)
Celková délka: 2+1+2+3 = 8 m
Stochastické zatížení: normální rozdělení, CoV = 0.1
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ============================================================
# 1. DETERMINISTICKÉ ŘEŠENÍ
# ============================================================

# Parametry
L_total = 8.0  # m
x_hinge = 2.0  # m — pozice kloubu
x_B = 5.0      # m — pozice podpory B

# Zatížení (střední hodnoty)
M0 = 20.0     # kN·m — koncentrovaný moment v x=2m (kladný = proti směru hod. ručiček)
F = 8.0        # kN — bodová síla v x=3m (dolů)
q = 15.0       # kN/m — spojité zatížení od x=5m do x=8m (dolů)

x_F = 3.0      # m — pozice bodové síly
x_q_start = 5.0  # m — začátek spojitého zatížení
x_q_end = 8.0    # m — konec spojitého zatížení

def solve_beam(M0, F, q, x_hinge=2.0, x_B=5.0, x_F=3.0,
               x_q_start=5.0, x_q_end=8.0, L=8.0):
    """
    Řeší nosník s vetknutím v A (x=0), kloubem v x_hinge,
    válcovou podporou v x_B.

    Neznámé: V_A, H_A, M_A, V_B (4 neznámé)
    Rovnice: ΣFx=0, ΣFy=0, ΣM_A=0, M(x_hinge)=0 (4 rovnice)

    Vrací funkce V(x), M(x) a reakční síly.
    """
    # Spojité zatížení — celková síla a těžiště
    L_q = x_q_end - x_q_start
    F_q = q * L_q  # celková síla od spojitého zatížení
    x_q_cg = x_q_start + L_q / 2  # těžiště spojitého zatížení

    # H_A = 0 (žádné horizontální zatížení)
    H_A = 0.0

    # Rovnice rovnováhy:
    # ΣFy = 0:  V_A + V_B - F - F_q = 0
    # ΣM_A = 0: M_A + M0 - F*x_F - F_q*x_q_cg + V_B*x_B = 0
    # M(x_hinge) = 0 (moment v kloubu od levé strany = 0):
    #   M_A + V_A * x_hinge + M0 = 0  (moment od sil nalevo od kloubu)
    #   (M0 je aplikován přímo v kloubu — konvence: patří k levé části)

    # Z podmínky kloubu (levá část, x = x_hinge):
    # M(x_hinge⁻) = M_A + V_A * x_hinge = 0
    # (moment M0 je aplikován přímo v kloubu, takže skok nastává v kloubu)
    # Tedy: M_A + V_A * x_hinge = 0 ... (i)
    # Poznámka: moment M0 způsobuje skok v x=2m, ale podmínka kloubu je M=0
    # Takže moment těsně nalevo od kloubu = 0 (ne včetně M0)

    # ΣM_A = 0:
    # M_A + V_B*x_B + M0 - F*x_F - F_q*x_q_cg = 0  ... (ii)

    # Z (i): M_A = -V_A * x_hinge
    # Z ΣFy: V_A = F + F_q - V_B  ... (iii)

    # Dosadíme (i) do (ii):
    # -V_A * x_hinge + V_B*x_B + M0 - F*x_F - F_q*x_q_cg = 0
    # Dosadíme (iii):
    # -(F + F_q - V_B)*x_hinge + V_B*x_B + M0 - F*x_F - F_q*x_q_cg = 0
    # -F*x_hinge - F_q*x_hinge + V_B*x_hinge + V_B*x_B + M0 - F*x_F - F_q*x_q_cg = 0
    # V_B*(x_hinge + x_B) = F*x_hinge + F_q*x_hinge - M0 + F*x_F + F_q*x_q_cg

    V_B = (F*x_hinge + F_q*x_hinge - M0 + F*x_F + F_q*x_q_cg) / (x_hinge + x_B)
    V_A = F + F_q - V_B
    M_A = -V_A * x_hinge

    return V_A, H_A, M_A, V_B


def compute_internal_forces(x_arr, V_A, H_A, M_A, V_B,
                             M0, F, q, x_hinge=2.0, x_B=5.0, x_F=3.0,
                             x_q_start=5.0, x_q_end=8.0):
    """
    Vypočítá N(x), V(x), M(x) po délce nosníku metodou řezů.
    Konvence: kladná posouvající síla = nahoru na levém řezu
    """
    N = np.zeros_like(x_arr)
    V = np.zeros_like(x_arr)
    M = np.zeros_like(x_arr)

    for i, x in enumerate(x_arr):
        # Normálová síla — žádné horizontální zatížení
        n = -H_A

        # Posouvající síla — součet svislých sil nalevo od řezu
        v = V_A
        m = M_A + V_A * x

        # Koncentrovaný moment v x_hinge
        if x >= x_hinge:
            m += M0

        # Bodová síla F v x_F
        if x >= x_F:
            v -= F
            m -= F * (x - x_F)

        # Podpora B v x_B
        if x >= x_B:
            v += V_B
            m += V_B * (x - x_B)

        # Spojité zatížení od x_q_start do min(x, x_q_end)
        if x > x_q_start:
            x_eff = min(x, x_q_end)
            dx = x_eff - x_q_start
            v -= q * dx
            m -= q * dx * (x - x_q_start - dx/2)

        N[i] = n
        V[i] = v
        M[i] = m

    return N, V, M


# Deterministické řešení
V_A, H_A, M_A, V_B = solve_beam(M0, F, q)

print("=" * 60)
print("PŘÍKLAD 1E — DETERMINISTICKÉ ŘEŠENÍ")
print("=" * 60)
print(f"Reakce:")
print(f"  V_A = {V_A:.2f} kN")
print(f"  H_A = {H_A:.2f} kN")
print(f"  M_A = {M_A:.2f} kN·m")
print(f"  V_B = {V_B:.2f} kN")
print()

# Kontrola rovnováhy
F_q_total = q * (x_q_end - x_q_start)
print(f"Kontrola ΣFy = {V_A + V_B - F - F_q_total:.6f} kN (≈ 0)")
sum_M_A = M_A + M0 - F*x_F - F_q_total*(x_q_start + (x_q_end-x_q_start)/2) + V_B*x_B
print(f"Kontrola ΣM_A = {sum_M_A:.6f} kN·m (≈ 0)")
print(f"Kontrola M(kloub) = {M_A + V_A*x_hinge:.6f} kN·m (≈ 0)")

# Výpočet průběhů
x = np.linspace(0, L_total, 2000)
N_det, V_det, M_det = compute_internal_forces(x, V_A, H_A, M_A, V_B, M0, F, q)

# Klíčové hodnoty
print(f"\nKlíčové hodnoty:")
print(f"  V_max = {np.max(np.abs(V_det)):.2f} kN")
print(f"  M_max = {np.max(M_det):.2f} kN·m")
print(f"  M_min = {np.min(M_det):.2f} kN·m")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo
# ============================================================

N_sim = 100_000
CoV = 0.1

# Generování náhodných zatížení (normální rozdělení)
np.random.seed(42)
M0_samples = np.random.normal(M0, M0 * CoV, N_sim)
F_samples = np.random.normal(F, F * CoV, N_sim)
q_samples = np.random.normal(q, q * CoV, N_sim)

# Pro každou realizaci spočítat reakce a klíčové hodnoty
V_A_mc = np.zeros(N_sim)
M_A_mc = np.zeros(N_sim)
V_B_mc = np.zeros(N_sim)
V_max_mc = np.zeros(N_sim)
M_max_mc = np.zeros(N_sim)
M_min_mc = np.zeros(N_sim)

x_key = np.linspace(0, L_total, 500)

for i in range(N_sim):
    va, ha, ma, vb = solve_beam(M0_samples[i], F_samples[i], q_samples[i])
    V_A_mc[i] = va
    M_A_mc[i] = ma
    V_B_mc[i] = vb

# Podrobný výpočet pro statistiku klíčových hodnot (menší vzorek pro diagramy)
N_plot = 1000
x_plot = np.linspace(0, L_total, 500)
V_envelope_max = np.full_like(x_plot, -np.inf)
V_envelope_min = np.full_like(x_plot, np.inf)
M_envelope_max = np.full_like(x_plot, -np.inf)
M_envelope_min = np.full_like(x_plot, np.inf)

for i in range(N_plot):
    va, ha, ma, vb = solve_beam(M0_samples[i], F_samples[i], q_samples[i])
    _, Vi, Mi = compute_internal_forces(x_plot, va, ha, ma, vb,
                                         M0_samples[i], F_samples[i], q_samples[i])
    V_envelope_max = np.maximum(V_envelope_max, Vi)
    V_envelope_min = np.minimum(V_envelope_min, Vi)
    M_envelope_max = np.maximum(M_envelope_max, Mi)
    M_envelope_min = np.minimum(M_envelope_min, Mi)

print("\n" + "=" * 60)
print("STOCHASTICKÁ ANALÝZA (Monte Carlo, N=100 000)")
print("=" * 60)
print(f"V_A:  μ = {np.mean(V_A_mc):.2f} kN,  σ = {np.std(V_A_mc):.2f} kN,  "
      f"CoV = {np.std(V_A_mc)/abs(np.mean(V_A_mc)):.4f}")
print(f"M_A:  μ = {np.mean(M_A_mc):.2f} kN·m,  σ = {np.std(M_A_mc):.2f} kN·m,  "
      f"CoV = {np.std(M_A_mc)/abs(np.mean(M_A_mc)):.4f}")
print(f"V_B:  μ = {np.mean(V_B_mc):.2f} kN,  σ = {np.std(V_B_mc):.2f} kN·m,  "
      f"CoV = {np.std(V_B_mc)/abs(np.mean(V_B_mc)):.4f}")

# ============================================================
# 3. GRAFY
# ============================================================

fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)
fig.suptitle('Příklad 1E — Průběh vnitřních sil a momentů\n'
             '(deterministický + stochastický obal, CoV=0.1)',
             fontsize=14, fontweight='bold')

# Normálová síla
axes[0].fill_between(x, 0, N_det, alpha=0.3, color='blue')
axes[0].plot(x, N_det, 'b-', linewidth=2, label='N(x) deterministický')
axes[0].axhline(y=0, color='k', linewidth=0.5)
axes[0].set_ylabel('N [kN]')
axes[0].set_title('Normálová síla N(x)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Značky podpor a kloubu
for ax in axes:
    ax.axvline(x=0, color='green', linestyle='--', alpha=0.5, label='A (vetknutí)')
    ax.axvline(x=x_hinge, color='orange', linestyle='--', alpha=0.5, label='Kloub')
    ax.axvline(x=x_B, color='red', linestyle='--', alpha=0.5, label='B (válcová)')

# Posouvající síla
axes[1].fill_between(x_plot, V_envelope_min, V_envelope_max, alpha=0.2, color='red',
                      label=f'Stochastický obal (N={N_plot})')
axes[1].fill_between(x, 0, V_det, alpha=0.3, color='blue')
axes[1].plot(x, V_det, 'b-', linewidth=2, label='V(x) deterministický')
axes[1].axhline(y=0, color='k', linewidth=0.5)
axes[1].set_ylabel('V [kN]')
axes[1].set_title('Posouvající síla V(x)')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Ohybový moment
axes[2].fill_between(x_plot, M_envelope_min, M_envelope_max, alpha=0.2, color='red',
                      label=f'Stochastický obal (N={N_plot})')
axes[2].fill_between(x, 0, M_det, alpha=0.3, color='blue')
axes[2].plot(x, M_det, 'b-', linewidth=2, label='M(x) deterministický')
axes[2].axhline(y=0, color='k', linewidth=0.5)
axes[2].set_ylabel('M [kN·m]')
axes[2].set_xlabel('x [m]')
axes[2].set_title('Ohybový moment M(x)')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_1E_diagram.png', dpi=150, bbox_inches='tight')
plt.close()

# Histogram reakcí
fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
fig2.suptitle('Příklad 1E — Histogramy reakcí (Monte Carlo, N=100 000)',
              fontsize=13, fontweight='bold')

axes2[0].hist(V_A_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes2[0].axvline(V_A, color='red', linewidth=2, linestyle='--', label=f'Determin. = {V_A:.2f}')
axes2[0].set_xlabel('V_A [kN]')
axes2[0].set_title('Reakce V_A')
axes2[0].legend()

axes2[1].hist(M_A_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes2[1].axvline(M_A, color='red', linewidth=2, linestyle='--', label=f'Determin. = {M_A:.2f}')
axes2[1].set_xlabel('M_A [kN·m]')
axes2[1].set_title('Momentová reakce M_A')
axes2[1].legend()

axes2[2].hist(V_B_mc, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes2[2].axvline(V_B, color='red', linewidth=2, linestyle='--', label=f'Determin. = {V_B:.2f}')
axes2[2].set_xlabel('V_B [kN]')
axes2[2].set_title('Reakce V_B')
axes2[2].legend()

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_1E_histogramy.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy do solutions/priklad_1E_diagram.png a priklad_1E_histogramy.png")
