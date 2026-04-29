"""
Příklad 5E — Časový průběh napětí ve vrubech
============================================
Součást se dvěma zápichy:
  - Vlevo: pevný svar (přivařena k základnímu rámu) — přenese tah i tlak
  - Vpravo: kontakt s rámem (δ = 0) — přenese pouze tlak, při tahu se rozevře

Klíčový princip (jednostranný kontakt):
  Souměrně střídavé vnější zatížení F = ±1000 N degeneruje kvůli
  jednostrannému kontaktu na PULZUJÍCÍ (míjivý) cyklus ve vrubu:
    - F táhne (od rámu)  → kontakt rozevřen → N = F = 1000 N
    - F tlačí (do rámu)  → kontakt nese    → N = 0
  Výsledek: σ ∈ {0; σ_max}, R = σ_min/σ_max = 0.

Geometrie:
  D = 50 mm, d = 35 mm (v zápichu), r = 5 mm, L = 500 mm
  Tolerance ±0,5 mm

Součinitel tvaru K_t:
  Peterson Chart 2.19 (kruhový hřídel, U-vrub, tah)
  D/d = 50/35 = 1,429;  r/d = 5/35 = 0,143
  → K_t ≈ 2,10  (rozsah 2,0–2,2 dle čtení grafu)

Předpětí F_0 = 1,4·10⁵ N v zadání:
  Per sage konsensus: význam nejasný (možná tuhost kontaktu / značení svaru).
  Standardní interpretace zadání tento údaj nepoužívá. Pro úplnost
  je výpočet "s předpětím" uveden v komentáři, ale není primárním
  výsledkem.
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARAMETRY
# ============================================================

D = 50.0          # mm — velký průměr
d = 35.0          # mm — průměr v zápichu
r = 5.0           # mm — poloměr zápichu
L = 500.0         # mm — délka

F_max = 1000.0    # N — maximální tahová síla v cyklu
F_min = 0.0       # N — minimální (jednostranný kontakt → 0)

tol = 0.5         # mm — tolerance rozměrů


# ============================================================
# SOUČINITEL KONCENTRACE NAPĚTÍ — PETERSON
# ============================================================

def Kt_peterson_ugroove_tension(D, d, r):
    """
    K_t pro kruhový hřídel s U-vrubem, axiální tah.
    Peterson's Stress Concentration Factors, Chart 2.19.

    Kalibrace: pro D=50, d=35, r=5 → K_t = 2,10
    (čtení z Petersonova grafu pro D/d=1,43, r/d=0,143).

    Pro stochastickou analýzu: Neuberova dimenzionální závislost
    škálovaná tak, aby v referenčním bodě dávala chart hodnotu 2,10.
    Tím zachová správné citlivosti dK_t/dD, dK_t/dd, dK_t/dr.
    """
    h = (D - d) / 2.0
    Kt_neuber = 1.0 + 2.0 * np.sqrt(h / r)
    # Reference: D=50, d=35, r=5 → Neuber = 3,449, Peterson chart = 2,10
    KT_REF_PETERSON = 2.10
    KT_REF_NEUBER = 1.0 + 2.0 * np.sqrt(7.5 / 5.0)  # = 3,449
    scale = (KT_REF_PETERSON - 1.0) / (KT_REF_NEUBER - 1.0)
    return 1.0 + scale * (Kt_neuber - 1.0)


# Deterministický K_t
Kt = Kt_peterson_ugroove_tension(D, d, r)
t_depth = (D - d) / 2.0
A_d = np.pi * d**2 / 4.0

print("=" * 60)
print("PŘÍKLAD 5E — ČASOVÝ PRŮBĚH NAPĚTÍ VE VRUBECH")
print("=" * 60)
print(f"\nGeometrie:")
print(f"  D = {D} mm, d = {d} mm, r = {r} mm")
print(f"  Hloubka vrubu t = {t_depth} mm")
print(f"  Plocha v zápichu A_d = {A_d:.2f} mm²")
print(f"  D/d = {D/d:.3f}, r/d = {r/d:.3f}")
print(f"  K_t (Peterson Chart 2.19) = {Kt:.3f}")

# ============================================================
# 1. DETERMINISTICKÝ VÝPOČET — JEDNOSTRANNÝ KONTAKT (R = 0)
# ============================================================

print(f"\n{'='*60}")
print("DETERMINISTICKÝ VÝPOČET (pulzující cyklus, R = 0)")
print("=" * 60)

sigma_nom_max = F_max / A_d
sigma_nom_min = F_min / A_d  # = 0

sigma_max = Kt * sigma_nom_max
sigma_min = Kt * sigma_nom_min  # = 0

sigma_m = (sigma_max + sigma_min) / 2.0
sigma_a = (sigma_max - sigma_min) / 2.0
R_ratio = sigma_min / sigma_max if sigma_max > 0 else 0.0

print(f"  σ_nom_max = F_max/A_d = {sigma_nom_max:.3f} MPa")
print(f"  σ_max = K_t · σ_nom_max = {Kt:.3f} · {sigma_nom_max:.3f} = {sigma_max:.3f} MPa")
print(f"  σ_min = 0 MPa")
print(f"  σ_m   = {sigma_m:.3f} MPa")
print(f"  σ_a   = {sigma_a:.3f} MPa")
print(f"  R     = σ_min/σ_max = {R_ratio:.3f}")

# Alternativa s předpětím (per konsensus: nejasné, jen pro úplnost)
F_pretension = 1.4e5  # N — z obrázku, význam neověřen
sigma_pre_max = Kt * (F_pretension + F_max) / A_d
sigma_pre_min = Kt * F_pretension / A_d
print(f"\n[Alternativa — F_0 = {F_pretension:.0f} N jako předpětí, neověřeno]:")
print(f"  σ_max = {sigma_pre_max:.2f} MPa, σ_min = {sigma_pre_min:.2f} MPa")
print(f"  σ_a   = {(sigma_pre_max - sigma_pre_min)/2:.2f} MPa (cyklus posunut na úroveň předpětí)")

# ============================================================
# 2. ČASOVÝ PRŮBĚH NAPĚTÍ
# ============================================================

freq = 1.0
t_total = 5.0 / freq
dt = 0.001
t_arr = np.arange(0, t_total, dt)

# Pulzující F(t) = (F_max/2)(1 - cos 2πft) — od 0 do F_max
F_t = F_max * (1.0 - np.cos(2.0 * np.pi * freq * t_arr)) / 2.0
sigma_t = Kt * F_t / A_d

print(f"\n{'='*60}")
print("ČASOVÝ PRŮBĚH NAPĚTÍ")
print("=" * 60)
print(f"  Pulzující obdélníková/harmonická vlna 0 ↔ {sigma_max:.3f} MPa")
print(f"  Frekvence: {freq} Hz, počet zobrazených cyklů: 5")

# ============================================================
# 3. STOCHASTICKÁ ANALÝZA
# ============================================================

N_sim = 100_000
np.random.seed(42)

sigma_dim = tol / 3.0  # 3σ pravidlo: tol = ±0,5 mm → σ ≈ 0,167 mm

D_mc = np.random.normal(D, sigma_dim, N_sim)
d_mc = np.random.normal(d, sigma_dim, N_sim)
r_mc = np.maximum(np.random.normal(r, sigma_dim, N_sim), 0.5)

Kt_mc = Kt_peterson_ugroove_tension(D_mc, d_mc, r_mc)
A_mc = np.pi * d_mc**2 / 4.0
sigma_max_mc = Kt_mc * F_max / A_mc
sigma_a_mc = sigma_max_mc / 2.0  # R = 0
sigma_m_mc = sigma_max_mc / 2.0

print(f"\n{'='*60}")
print(f"STOCHASTICKÁ ANALÝZA (N = {N_sim:,})")
print("=" * 60)
print(f"  σ_max: μ = {np.mean(sigma_max_mc):.3f} MPa,  "
      f"σ = {np.std(sigma_max_mc):.3f} MPa,  "
      f"CoV = {np.std(sigma_max_mc)/np.mean(sigma_max_mc):.4f}")
print(f"  σ_a:   μ = {np.mean(sigma_a_mc):.3f} MPa,  σ = {np.std(sigma_a_mc):.3f} MPa")
print(f"  K_t:   μ = {np.mean(Kt_mc):.3f},  σ = {np.std(Kt_mc):.3f}")

q025, q500, q975 = np.quantile(sigma_max_mc, [0.025, 0.5, 0.975])
print(f"  σ_max kvantily: 2,5 % = {q025:.3f},  50 % = {q500:.3f},  97,5 % = {q975:.3f} MPa")

# ============================================================
# 4. GRAFY
# ============================================================

import os
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Příklad 5E — Časový průběh napětí ve vrubech\n'
             'Pulzující cyklus 0→1000 N (jednostranný kontakt), '
             'D=50/d=35 mm, r=5 mm, K_t (Peterson) ≈ 2,10',
             fontsize=12, fontweight='bold')

# Síla
ax = axes[0, 0]
ax.plot(t_arr, F_t, 'b-', linewidth=1.5)
ax.set_xlabel('Čas [s]')
ax.set_ylabel('F [N]')
ax.set_title('Zatěžující síla F(t)')
ax.grid(True, alpha=0.3)
ax.set_ylim(-100, F_max * 1.2)

# Napětí v zápichu
ax = axes[0, 1]
ax.plot(t_arr, sigma_t, 'r-', linewidth=1.5, label='σ(t) v zápichu')
ax.axhline(sigma_max, color='red', linestyle='--', alpha=0.5,
           label=f'σ_max = {sigma_max:.2f} MPa')
ax.axhline(sigma_m, color='green', linestyle='--', alpha=0.5,
           label=f'σ_m = {sigma_m:.2f} MPa')
ax.fill_between(t_arr, sigma_m - sigma_a, sigma_m + sigma_a, alpha=0.1, color='red')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title('Napětí v zápichu σ(t)')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)

# Histogram σ_max
ax = axes[1, 0]
ax.hist(sigma_max_mc, bins=80, density=True, alpha=0.7,
        color='steelblue', edgecolor='white')
ax.axvline(sigma_max, color='red', linewidth=2, linestyle='--',
           label=f'Determ. = {sigma_max:.3f} MPa')
ax.set_xlabel('σ_max [MPa]')
ax.set_ylabel('Hustota')
ax.set_title(f'Rozložení maximálního napětí (N={N_sim:,})')
ax.legend()
ax.grid(True, alpha=0.3)

# Stochastický obal
ax = axes[1, 1]
n_curves = 50
for i in range(n_curves):
    F_t_i = F_max * (1.0 - np.cos(2.0 * np.pi * freq * t_arr)) / 2.0
    sigma_t_i = Kt_mc[i] * F_t_i / A_mc[i]
    ax.plot(t_arr, sigma_t_i, 'b-', alpha=0.1, linewidth=0.5)
ax.plot(t_arr, sigma_t, 'r-', linewidth=2, label='Deterministický')
ax.set_xlabel('Čas [s]')
ax.set_ylabel('σ [MPa]')
ax.set_title(f'Stochastický obal σ(t) ({n_curves} realizací)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'priklad_5E_vysledky.png'),
            dpi=150, bbox_inches='tight')
plt.close()

# Haighův diagram
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))
ax2.set_title('Příklad 5E — Haighův diagram (σ_a vs σ_m)',
              fontsize=13, fontweight='bold')

ax2.scatter(sigma_m_mc[:5000], sigma_a_mc[:5000], alpha=0.15, s=5,
            color='blue', label='Stochastické realizace')
ax2.plot(sigma_m, sigma_a, 'ro', markersize=10, zorder=5,
         label=f'Deterministický bod (σ_m={sigma_m:.2f}, σ_a={sigma_a:.2f})')

Re = 500
sigma_c = 300
sm_line = np.linspace(0, Re, 100)
sa_goodman = sigma_c * (1.0 - sm_line / Re)
ax2.plot(sm_line, sa_goodman, 'g--', linewidth=2,
         label=f'Goodman (R_e={Re}, σ_c={sigma_c} MPa)')

ax2.set_xlabel('σ_m [MPa]')
ax2.set_ylabel('σ_a [MPa]')
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, Re * 1.05)
ax2.set_ylim(0, sigma_c * 1.05)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'priklad_5E_haigh.png'),
            dpi=150, bbox_inches='tight')
plt.close()

print(f"\nGrafy uloženy do {OUT_DIR}/priklad_5E_vysledky.png")
print(f"                  {OUT_DIR}/priklad_5E_haigh.png")
