"""
Příklad 5E — Časový průběh napětí ve vrubech
============================================
Rotační součást se dvěma zápichy, axiálně zatížená střídavou silou.

Geometrie (z výkresu):
  - Celková délka L_tot = 820 mm
  - Úseky: [0,200] D=50, [200,210] d=35 (levý vrub), [210,610] D=50,
           [610,620] d=35 (pravý vrub), [620,820] D=50
  - Síla F působí v x_F = 500 mm od levého vetknutí
  - Rádius zápichu r = 5 mm

Uložení:
  - Vlevo: pevné vetknutí (přenese tah i tlak)
  - Vpravo: jednostranný kontakt s tuhou stěnou (δ = 0)
            - Stav A: F → do stěny → kontakt aktivní (staticky neurčitý)
            - Stav B: F → od stěny → kontakt rozevřen (staticky určitý)

Zatížení:
  F = ±1,4·10⁵ N obdélníková střídavá vlna, tolerance +1000/−0 N

Součinitel tvaru K_t (Peterson Chart 2.19, U-vrub, axiální tah):
  D/d = 1,429, r/d = 0,143 → K_t ≈ 2,10
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRY
# ============================================================

D = 50.0
d = 35.0
r = 5.0

L1 = 200.0   # první úsek D
L2 = 10.0    # levý zápich (šířka)
L3 = 400.0   # střední úsek D
L4 = 10.0    # pravý zápich
L5 = 200.0   # poslední úsek D
L_tot = L1 + L2 + L3 + L4 + L5  # 820 mm

x_F = 500.0  # poloha síly od levého vetknutí

F0 = 1.4e5   # N — jmenovitá velikost síly
F_tol_plus = 1000.0
F_tol_minus = 0.0

tol = 0.5    # ±0,5 mm na všech rozměrech


# ============================================================
# K_T — PETERSON CHART 2.19 (U-vrub, axiální tah)
# ============================================================

def Kt_peterson_ugroove_tension(D, d, r):
    """K_t pro kruhový hřídel s U-vrubem v tahu.
    Kalibrace na bod D=50, d=35, r=5 → K_t = 2,10 (Peterson chart).
    Citlivosti dK_t/dD, dK_t/dd, dK_t/dr škálovány Neuberovou aproximací."""
    h = (D - d) / 2.0
    Kt_neuber = 1.0 + 2.0 * np.sqrt(np.maximum(h / r, 1e-9))
    KT_REF_PETERSON = 2.10
    KT_REF_NEUBER = 1.0 + 2.0 * np.sqrt(7.5 / 5.0)
    scale = (KT_REF_PETERSON - 1.0) / (KT_REF_NEUBER - 1.0)
    return 1.0 + scale * (Kt_neuber - 1.0)


# ============================================================
# OSOVÁ ANALÝZA — DVA STAVY JEDNOSTRANNÉHO KONTAKTU
# ============================================================

def axial_analysis(D, d, r, L1, L2, L3, L4, L5, x_F, F):
    """
    Spočítá vnitřní osové síly v levé a pravé části hřídele
    pro stav s jednostranným kontaktem vpravo.

    Vrací: N_left, N_right, K_t, A_d, A_D
    """
    A_D = np.pi * D**2 / 4.0
    A_d = np.pi * d**2 / 4.0
    Kt = Kt_peterson_ugroove_tension(D, d, r)

    # Levá část: 0 -> x_F.
    # Skladba: [0, L1] D, [L1, L1+L2] d, [L1+L2, x_F] D
    L_DL = L1 + (x_F - L1 - L2)   # délka v D (před vrubem + za vrubem do síly)
    L_dL = L2                     # délka v d (levý vrub)

    # Pravá část: x_F -> L_tot.
    # Skladba: [x_F, L1+L2+L3] D, [L1+L2+L3, L1+L2+L3+L4] d, zbytek D
    L_tot = L1 + L2 + L3 + L4 + L5
    L_DR = (L1 + L2 + L3 - x_F) + L5   # úseky D v pravé části
    L_dR = L4                          # pravý vrub

    # Poddajnosti (×E)
    C_L = L_DL / A_D + L_dL / A_d
    C_R = L_DR / A_D + L_dR / A_d

    # Pro F > 0 (do stěny): kontakt aktivní (Stav A)
    # Pro F < 0 (od stěny): R_R = 0 (Stav B)
    # Konvence: tah positivní, +x doprava.
    # Z FBD vpravo: N_left = F + R_R, N_right = R_R
    # Kompatibilita (Stav A): N_left·C_L + N_right·C_R = 0
    #   → R_R = -F · C_L / (C_L + C_R)

    F_arr = np.atleast_1d(F).astype(float)
    R_R = np.where(F_arr > 0,
                   -F_arr * C_L / (C_L + C_R),
                   0.0)
    N_left = F_arr + R_R
    N_right = R_R

    return (N_left if F_arr.size > 1 else float(N_left[0]),
            N_right if F_arr.size > 1 else float(N_right[0]),
            Kt, A_d, A_D)


# ============================================================
# DETERMINISTICKÝ VÝPOČET
# ============================================================

print("=" * 64)
print("PŘÍKLAD 5E — ČASOVÝ PRŮBĚH NAPĚTÍ VE VRUBECH")
print("=" * 64)

A_D = np.pi * D**2 / 4.0
A_d = np.pi * d**2 / 4.0
Kt = Kt_peterson_ugroove_tension(D, d, r)
print(f"\nGeometrie:")
print(f"  D = {D} mm, d = {d} mm, r = {r} mm")
print(f"  A_D = {A_D:.2f} mm², A_d = {A_d:.2f} mm²")
print(f"  L_tot = {L_tot} mm, x_F = {x_F} mm")
print(f"  D/d = {D/d:.3f}, r/d = {r/d:.3f}")
print(f"  K_t (Peterson) = {Kt:.3f}")

# Stav A: F kladná (do stěny)
N_LA, N_RA, _, _, _ = axial_analysis(D, d, r, L1, L2, L3, L4, L5, x_F, +F0)
# Stav B: F záporná (od stěny)
N_LB, N_RB, _, _, _ = axial_analysis(D, d, r, L1, L2, L3, L4, L5, x_F, -F0)

print(f"\n{'='*64}\nSTAV A — F = +{F0:.0f} N (do stěny, kontakt aktivní)")
print("=" * 64)
print(f"  N_levá  = {N_LA:+.1f} N  (tah)")
print(f"  N_pravá = {N_RA:+.1f} N  (tlak)")
print(f"  σ_levý  = K_t·N_L/A_d = {Kt:.3f}·{N_LA:.1f}/{A_d:.2f} = {Kt*N_LA/A_d:+.2f} MPa")
print(f"  σ_pravý = K_t·N_R/A_d = {Kt*N_RA/A_d:+.2f} MPa")

print(f"\n{'='*64}\nSTAV B — F = -{F0:.0f} N (od stěny, kontakt rozevřen)")
print("=" * 64)
print(f"  N_levá  = {N_LB:+.1f} N  (tlak)")
print(f"  N_pravá = {N_RB:+.1f} N")
print(f"  σ_levý  = {Kt*N_LB/A_d:+.2f} MPa")
print(f"  σ_pravý = {Kt*N_RB/A_d:+.2f} MPa")

# Maximum/minimum napětí v každém vrubu přes oba stavy
sig_L_A = Kt * N_LA / A_d
sig_L_B = Kt * N_LB / A_d
sig_R_A = Kt * N_RA / A_d
sig_R_B = Kt * N_RB / A_d

sig_L_max = max(sig_L_A, sig_L_B)
sig_L_min = min(sig_L_A, sig_L_B)
sig_R_max = max(sig_R_A, sig_R_B)
sig_R_min = min(sig_R_A, sig_R_B)

sig_L_a = (sig_L_max - sig_L_min) / 2.0
sig_L_m = (sig_L_max + sig_L_min) / 2.0
sig_R_a = (sig_R_max - sig_R_min) / 2.0
sig_R_m = (sig_R_max + sig_R_min) / 2.0

print(f"\n{'='*64}\nVRUBOVÁ NAPĚTÍ — SOUHRN")
print("=" * 64)
print(f"  Levý vrub:  σ_max = {sig_L_max:+.2f} MPa, σ_min = {sig_L_min:+.2f} MPa")
print(f"              σ_a   = {sig_L_a:.2f} MPa,    σ_m   = {sig_L_m:+.2f} MPa")
R_left = sig_L_min / sig_L_max if abs(sig_L_max) > 1e-9 else float('nan')
print(f"              R     = {R_left:.3f}  (asymetrický střídavý)")
print(f"  Pravý vrub: σ_max = {sig_R_max:+.2f} MPa, σ_min = {sig_R_min:+.2f} MPa")
print(f"              σ_a   = {sig_R_a:.2f} MPa,    σ_m   = {sig_R_m:+.2f} MPa")
print(f"              R     = ±∞ (míjivý tlak: 0 ↔ záporná hodnota)")

# ============================================================
# ČASOVÝ PRŮBĚH — OBDÉLNÍKOVÁ VLNA
# ============================================================

freq = 1.0
t_total = 4.0 / freq
dt = 0.001
t_arr = np.arange(0, t_total, dt)

# obdélníková vlna ±F0
F_t = F0 * np.sign(np.sin(2.0 * np.pi * freq * t_arr))
F_t[F_t == 0] = F0  # ošetřit nuly

sig_L_t = np.where(F_t > 0, sig_L_A, sig_L_B)
sig_R_t = np.where(F_t > 0, sig_R_A, sig_R_B)

# ============================================================
# STOCHASTICKÁ ANALÝZA — MONTE CARLO
# ============================================================

N_sim = 100_000
rng = np.random.default_rng(42)
sigma_dim = tol / 3.0

D_mc = rng.normal(D, sigma_dim, N_sim)
d_mc = rng.normal(d, sigma_dim, N_sim)
r_mc = np.maximum(rng.normal(r, sigma_dim, N_sim), 0.5)
L1_mc = rng.normal(L1, sigma_dim, N_sim)
L2_mc = rng.normal(L2, sigma_dim, N_sim)
L3_mc = rng.normal(L3, sigma_dim, N_sim)
L4_mc = rng.normal(L4, sigma_dim, N_sim)
L5_mc = rng.normal(L5, sigma_dim, N_sim)
xF_mc = rng.normal(x_F, sigma_dim, N_sim)
F_mc = rng.uniform(F0, F0 + F_tol_plus, N_sim)

A_D_mc = np.pi * D_mc**2 / 4.0
A_d_mc = np.pi * d_mc**2 / 4.0
Kt_mc = Kt_peterson_ugroove_tension(D_mc, d_mc, r_mc)

# Délky úseků v levé/pravé části (per realizace)
L_DL_mc = L1_mc + (xF_mc - L1_mc - L2_mc)
L_dL_mc = L2_mc
L_DR_mc = (L1_mc + L2_mc + L3_mc - xF_mc) + L5_mc
L_dR_mc = L4_mc

C_L_mc = L_DL_mc / A_D_mc + L_dL_mc / A_d_mc
C_R_mc = L_DR_mc / A_D_mc + L_dR_mc / A_d_mc

# Stav A: F = +F_mc
R_R_A = -F_mc * C_L_mc / (C_L_mc + C_R_mc)
N_LA_mc = F_mc + R_R_A
N_RA_mc = R_R_A

# Stav B: F = -F_mc, R_R = 0
N_LB_mc = -F_mc
N_RB_mc = np.zeros(N_sim)

sig_L_A_mc = Kt_mc * N_LA_mc / A_d_mc
sig_L_B_mc = Kt_mc * N_LB_mc / A_d_mc
sig_R_A_mc = Kt_mc * N_RA_mc / A_d_mc
sig_R_B_mc = Kt_mc * N_RB_mc / A_d_mc

sig_L_max_mc = np.maximum(sig_L_A_mc, sig_L_B_mc)
sig_L_min_mc = np.minimum(sig_L_A_mc, sig_L_B_mc)
sig_R_max_mc = np.maximum(sig_R_A_mc, sig_R_B_mc)
sig_R_min_mc = np.minimum(sig_R_A_mc, sig_R_B_mc)

sig_L_a_mc = (sig_L_max_mc - sig_L_min_mc) / 2.0
sig_R_a_mc = (sig_R_max_mc - sig_R_min_mc) / 2.0
sig_L_m_mc = (sig_L_max_mc + sig_L_min_mc) / 2.0
sig_R_m_mc = (sig_R_max_mc + sig_R_min_mc) / 2.0

print(f"\n{'='*64}\nSTOCHASTICKÁ ANALÝZA (N = {N_sim:,})")
print("=" * 64)


def stat(label, x):
    mu, sd = np.mean(x), np.std(x)
    cov = sd / abs(mu) if abs(mu) > 1e-9 else float('nan')
    q = np.quantile(x, [0.025, 0.975])
    print(f"  {label:18s} μ = {mu:+9.3f}, σ = {sd:7.3f}, "
          f"CoV = {cov:.4f}, 95% CI = [{q[0]:+.2f}; {q[1]:+.2f}]")


stat("σ_L_max [MPa]:", sig_L_max_mc)
stat("σ_L_min [MPa]:", sig_L_min_mc)
stat("σ_L_a   [MPa]:", sig_L_a_mc)
stat("σ_R_min [MPa]:", sig_R_min_mc)
stat("σ_R_a   [MPa]:", sig_R_a_mc)
stat("K_t       [-]:", Kt_mc)

# ============================================================
# GRAFY
# ============================================================

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

fig, axes = plt.subplots(3, 2, figsize=(14, 12))
fig.suptitle('Příklad 5E — Časový průběh napětí ve vrubech\n'
             'Hřídel s jednostranným kontaktem, F = ±140 kN, '
             'D=50 / d=35 mm, r=5 mm, K_t (Peterson) ≈ 2,10',
             fontsize=12, fontweight='bold')

# Síla F(t)
ax = axes[0, 0]
ax.plot(t_arr, F_t / 1000.0, 'b-', linewidth=1.5)
ax.axhline(0, color='k', linewidth=0.5)
ax.set_xlabel('Čas [s]')
ax.set_ylabel('F [kN]')
ax.set_title('Zatěžující síla F(t) — obdélníková vlna ±140 kN')
ax.grid(True, alpha=0.3)
ax.set_ylim(-180, 180)

# Schéma vnitřních sil v obou stavech
ax = axes[0, 1]
xs = [0, x_F, x_F, L_tot]
N_A = [N_LA, N_LA, N_RA, N_RA]
N_B = [N_LB, N_LB, N_RB, N_RB]
ax.plot(xs, np.array(N_A) / 1000.0, 'r-', linewidth=2, label=f'Stav A (F=+{F0/1000:.0f} kN)')
ax.plot(xs, np.array(N_B) / 1000.0, 'b-', linewidth=2, label=f'Stav B (F=-{F0/1000:.0f} kN)')
ax.axvline(x_F, color='k', linestyle=':', alpha=0.5, label=f'x_F = {x_F} mm')
ax.axvspan(L1, L1 + L2, alpha=0.2, color='gray')
ax.axvspan(L1 + L2 + L3, L1 + L2 + L3 + L4, alpha=0.2, color='gray', label='vruby')
ax.axhline(0, color='k', linewidth=0.5)
ax.set_xlabel('x [mm]')
ax.set_ylabel('N(x) [kN]')
ax.set_title('Vnitřní osová síla N(x) v obou stavech')
ax.legend(fontsize=8, loc='best')
ax.grid(True, alpha=0.3)

# Napětí v levém vrubu
ax = axes[1, 0]
ax.plot(t_arr, sig_L_t, 'r-', linewidth=1.5, label='σ_levý(t)')
ax.axhline(sig_L_max, color='red', linestyle='--', alpha=0.5,
           label=f'σ_max = {sig_L_max:+.1f} MPa')
ax.axhline(sig_L_min, color='red', linestyle='--', alpha=0.5,
           label=f'σ_min = {sig_L_min:+.1f} MPa')
ax.axhline(sig_L_m, color='green', linestyle=':', alpha=0.5,
           label=f'σ_m = {sig_L_m:+.1f} MPa')
ax.axhline(0, color='k', linewidth=0.5)
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title('Levý vrub — asymetrický střídavý cyklus')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Napětí v pravém vrubu
ax = axes[1, 1]
ax.plot(t_arr, sig_R_t, 'b-', linewidth=1.5, label='σ_pravý(t)')
ax.axhline(sig_R_max, color='blue', linestyle='--', alpha=0.5,
           label=f'σ_max = {sig_R_max:+.1f} MPa')
ax.axhline(sig_R_min, color='blue', linestyle='--', alpha=0.5,
           label=f'σ_min = {sig_R_min:+.1f} MPa')
ax.axhline(0, color='k', linewidth=0.5)
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title('Pravý vrub — míjivý tlak (0 ↔ záporná hodnota)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Histogram σ_L_min (kritická tlaková špička)
ax = axes[2, 0]
ax.hist(sig_L_min_mc, bins=80, density=True, alpha=0.7,
        color='salmon', edgecolor='white')
ax.axvline(sig_L_min, color='red', linewidth=2, linestyle='--',
           label=f'Determ. = {sig_L_min:.2f} MPa')
ax.set_xlabel('σ_L_min [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'Levý vrub — rozložení tlakové špičky (N={N_sim:,})')
ax.legend()
ax.grid(True, alpha=0.3)

# Histogram σ_R_min
ax = axes[2, 1]
ax.hist(sig_R_min_mc, bins=80, density=True, alpha=0.7,
        color='steelblue', edgecolor='white')
ax.axvline(sig_R_min, color='blue', linewidth=2, linestyle='--',
           label=f'Determ. = {sig_R_min:.2f} MPa')
ax.set_xlabel('σ_R_min [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'Pravý vrub — rozložení tlakové špičky (N={N_sim:,})')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'priklad_5E_vysledky.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# Haighův diagram pro oba vruby
fig2, ax2 = plt.subplots(1, 1, figsize=(9, 7))
ax2.set_title('Příklad 5E — Haighův diagram pro oba vruby',
              fontsize=13, fontweight='bold')

ax2.scatter(sig_L_m_mc[:5000], sig_L_a_mc[:5000], alpha=0.15, s=5,
            color='red', label='Levý vrub (MC)')
ax2.scatter(sig_R_m_mc[:5000], sig_R_a_mc[:5000], alpha=0.15, s=5,
            color='blue', label='Pravý vrub (MC)')
ax2.plot(sig_L_m, sig_L_a, 'r^', markersize=12, zorder=5,
         label=f'Levý determ. ({sig_L_m:+.0f}, {sig_L_a:.0f})')
ax2.plot(sig_R_m, sig_R_a, 'b^', markersize=12, zorder=5,
         label=f'Pravý determ. ({sig_R_m:+.0f}, {sig_R_a:.0f})')

Re = 500.0
sigma_c = 300.0
sm_line = np.linspace(-Re, Re, 200)
sa_goodman = np.maximum(sigma_c * (1.0 - np.abs(sm_line) / Re), 0.0)
ax2.plot(sm_line, sa_goodman, 'g--', linewidth=2,
         label=f'Goodman (R_e={Re:.0f}, σ_c={sigma_c:.0f} MPa)')

ax2.axvline(0, color='k', linewidth=0.5)
ax2.set_xlabel('σ_m [MPa]')
ax2.set_ylabel('σ_a [MPa]')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(-Re * 1.05, Re * 1.05)
ax2.set_ylim(0, sigma_c * 1.05)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'priklad_5E_haigh.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print(f"\nGrafy: {OUT_DIR}/priklad_5E_vysledky.png")
print(f"       {OUT_DIR}/priklad_5E_haigh.png")
