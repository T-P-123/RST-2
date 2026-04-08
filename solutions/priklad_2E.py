"""
Příklad 2E — Osový kvadratický moment L-profilu k ose x a y
============================================================
L-profil (rovnoramenný úhelník) s rozměry z obrázku:

Průřez (pohled 2D, počátek v levém dolním rohu):

    |30|
    +--+
    |  |  ^
    |  |  | 30 mm (horní část)
    |  |  |
    |  +  + - - - - (y=170)
    |  |  |
    |  |  | 140 mm (střední část)
    |  |  |
    |  |  v
    +--+--+---------170mm--------+
    |          30mm               |  30 mm (výška)
    +--+--+----------------------+
    |30|
       ȳ

Rozměry průřezu:
  - Svislé rameno: šířka 30 mm, celková výška 200 mm (30+140+30)
  - Vodorovné rameno: celková šířka 200 mm (30+170), výška 30 mm
  - Sdílený roh: 30 × 30 mm v levém dolním rohu
  - 70 mm = hloubka 3D tělesa (extruze), neovlivňuje 2D průřez

Stochastické veličiny: normální rozdělení, CoV = 0.2
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================================
# 1. DETERMINISTICKÉ ŘEŠENÍ
# ============================================================

def compute_section_properties(rectangles):
    """
    Vypočítá těžiště a osové kvadratické momenty složeného průřezu.
    rectangles = [(b, h, xc, yc), ...] kde:
      b = šířka, h = výška, xc,yc = souřadnice těžiště obdélníku
    """
    A_total = 0.0
    Sx = 0.0
    Sy = 0.0

    for b, h, xc, yc in rectangles:
        A = b * h
        A_total += A
        Sx += A * yc
        Sy += A * xc

    xC = Sy / A_total
    yC = Sx / A_total

    Ix = 0.0
    Iy = 0.0

    for b, h, xc, yc in rectangles:
        A = b * h
        Ix_own = b * h**3 / 12
        Iy_own = b**3 * h / 12
        Ix += Ix_own + A * (yc - yC)**2
        Iy += Iy_own + A * (xc - xC)**2

    return A_total, xC, yC, Ix, Iy


# Rozměry L-profilu
t = 30.0         # mm — tloušťka obou ramen
h_total = 200.0  # mm — celková výška svislého ramena (30+140+30)
b_total = 200.0  # mm — celková šířka vodorovného ramena (30+170)

# Rozklad na 2 nepřekrývající se obdélníky:
# 1) Vodorovné rameno (celé): b_total × t, těžiště v (b_total/2, t/2)
# 2) Svislé rameno (nad sdíleným rohem): t × (h_total - t), těžiště v (t/2, t + (h_total-t)/2)

rects_det = [
    (b_total, t, b_total/2, t/2),                         # Vodorovné rameno: 200×30
    (t, h_total - t, t/2, t + (h_total - t)/2),           # Svislé rameno (nad rohem): 30×170
]

A, xC, yC, Ix, Iy = compute_section_properties(rects_det)

print("=" * 60)
print("PŘÍKLAD 2E — DETERMINISTICKÉ ŘEŠENÍ (L-PROFIL)")
print("=" * 60)
print(f"\nGeometrie:")
print(f"  Svislé rameno: {t:.0f} × {h_total:.0f} mm")
print(f"  Vodorovné rameno: {b_total:.0f} × {t:.0f} mm")
print(f"  Sdílený roh: {t:.0f} × {t:.0f} mm")

print(f"\nPlocha průřezu:")
A1 = b_total * t
A2 = t * (h_total - t)
print(f"  A₁ (vodorovné) = {b_total} × {t} = {A1:.0f} mm²")
print(f"  A₂ (svislé nad rohem) = {t} × {h_total - t} = {A2:.0f} mm²")
print(f"  A = A₁ + A₂ = {A:.0f} mm²")

print(f"\nTěžiště:")
print(f"  x_C = {xC:.2f} mm")
print(f"  y_C = {yC:.2f} mm")

print(f"\nOsové kvadratické momenty (Steinerova věta):")

# Podrobný výpočet pro kontrolu
d1y = t/2 - yC
d2y = (t + (h_total - t)/2) - yC
Ix1 = b_total * t**3 / 12 + A1 * d1y**2
Ix2 = t * (h_total - t)**3 / 12 + A2 * d2y**2

print(f"\n  I_x:")
print(f"    Ix₁ = {b_total}·{t}³/12 + {A1:.0f}·({t/2:.1f} - {yC:.2f})² "
      f"= {b_total*t**3/12:.0f} + {A1 * d1y**2:.0f} = {Ix1:.0f} mm⁴")
print(f"    Ix₂ = {t}·{h_total-t}³/12 + {A2:.0f}·({t + (h_total-t)/2:.1f} - {yC:.2f})² "
      f"= {t*(h_total-t)**3/12:.0f} + {A2 * d2y**2:.0f} = {Ix2:.0f} mm⁴")
print(f"    Ix = {Ix1:.0f} + {Ix2:.0f} = {Ix:.0f} mm⁴ = {Ix/1e6:.4f} × 10⁶ mm⁴")

d1x = b_total/2 - xC
d2x = t/2 - xC
Iy1 = b_total**3 * t / 12 + A1 * d1x**2
Iy2 = t**3 * (h_total - t) / 12 + A2 * d2x**2

print(f"\n  I_y:")
print(f"    Iy₁ = {b_total}³·{t}/12 + {A1:.0f}·({b_total/2:.1f} - {xC:.2f})² "
      f"= {b_total**3*t/12:.0f} + {A1 * d1x**2:.0f} = {Iy1:.0f} mm⁴")
print(f"    Iy₂ = {t}³·{h_total-t}/12 + {A2:.0f}·({t/2:.1f} - {xC:.2f})² "
      f"= {t**3*(h_total-t)/12:.0f} + {A2 * d2x**2:.0f} = {Iy2:.0f} mm⁴")
print(f"    Iy = {Iy1:.0f} + {Iy2:.0f} = {Iy:.0f} mm⁴ = {Iy/1e6:.4f} × 10⁶ mm⁴")

print(f"\n  *** Ix = {Ix/1e6:.4f} × 10⁶ mm⁴ ***")
print(f"  *** Iy = {Iy/1e6:.4f} × 10⁶ mm⁴ ***")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo
# ============================================================

N_sim = 100_000
CoV = 0.2
np.random.seed(42)

# Střední hodnoty rozměrů L-profilu (mm)
# Nezávislé rozměry: tloušťka t, šířka vodorovného ramena b_h, výška svislého ramena h_v
# b_h = 170 mm (přesah za stojinu), h_v_above = 140 mm (výška nad rohem), horní = 30mm
# Ale protože t, b_total, h_total jsou odvozeny z podrozměrů:
#   tloušťka t = 30 mm
#   přesah dolní příruby = 170 mm
#   výška stojiny nad přírubou = 140 mm
#   výška horní části = 30 mm

dims_mean = {
    't': 30.0,              # tloušťka ramen
    'overhang_h': 170.0,    # přesah vodorovného ramena (= b_total - t)
    'h_web': 140.0,         # výška stojiny mezi rameny
    'h_top': 30.0,          # výška horní části svislého ramena
}

samples = {}
for key, mu in dims_mean.items():
    sigma = mu * CoV
    samples[key] = np.random.normal(mu, sigma, N_sim)
    samples[key] = np.maximum(samples[key], 1.0)

Ix_mc = np.zeros(N_sim)
Iy_mc = np.zeros(N_sim)
xC_mc = np.zeros(N_sim)
yC_mc = np.zeros(N_sim)

for i in range(N_sim):
    ti = samples['t'][i]
    b_tot_i = ti + samples['overhang_h'][i]     # celková šířka vodorovného ramena
    h_tot_i = ti + samples['h_web'][i] + samples['h_top'][i]  # celková výška svislého

    rects = [
        (b_tot_i, ti, b_tot_i/2, ti/2),                           # Vodorovné rameno
        (ti, h_tot_i - ti, ti/2, ti + (h_tot_i - ti)/2),          # Svislé rameno (nad rohem)
    ]
    A_i, xC_i, yC_i, Ix_i, Iy_i = compute_section_properties(rects)
    Ix_mc[i] = Ix_i
    Iy_mc[i] = Iy_i
    xC_mc[i] = xC_i
    yC_mc[i] = yC_i

print(f"\n{'='*60}")
print(f"STOCHASTICKÁ ANALÝZA (Monte Carlo, N={N_sim:,}, CoV={CoV})")
print("=" * 60)
print(f"Ix: μ = {np.mean(Ix_mc)/1e6:.4f} × 10⁶ mm⁴,  σ = {np.std(Ix_mc)/1e6:.4f} × 10⁶ mm⁴,  "
      f"CoV = {np.std(Ix_mc)/np.mean(Ix_mc):.4f}")
print(f"Iy: μ = {np.mean(Iy_mc)/1e6:.4f} × 10⁶ mm⁴,  σ = {np.std(Iy_mc)/1e6:.4f} × 10⁶ mm⁴,  "
      f"CoV = {np.std(Iy_mc)/np.mean(Iy_mc):.4f}")
print(f"xC: μ = {np.mean(xC_mc):.2f} mm,  σ = {np.std(xC_mc):.2f} mm")
print(f"yC: μ = {np.mean(yC_mc):.2f} mm,  σ = {np.std(yC_mc):.2f} mm")

for q_val in [0.025, 0.5, 0.975]:
    print(f"  Ix ({q_val*100:.1f}%) = {np.quantile(Ix_mc, q_val)/1e6:.4f} × 10⁶ mm⁴")

# ============================================================
# 3. GRAFY
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Příklad 2E — Osové kvadratické momenty L-profilu\n'
             f'(Monte Carlo, N={N_sim:,}, CoV={CoV})', fontsize=13, fontweight='bold')

axes[0].hist(Ix_mc/1e6, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes[0].axvline(Ix/1e6, color='red', linewidth=2, linestyle='--',
                label=f'Determin. = {Ix/1e6:.2f}×10⁶')
axes[0].set_xlabel('Ix [×10⁶ mm⁴]')
axes[0].set_ylabel('Hustota pravděpodobnosti')
axes[0].set_title('Osový kvadratický moment Ix')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(Iy_mc/1e6, bins=80, density=True, alpha=0.7, color='steelblue', edgecolor='white')
axes[1].axvline(Iy/1e6, color='red', linewidth=2, linestyle='--',
                label=f'Determin. = {Iy/1e6:.2f}×10⁶')
axes[1].set_xlabel('Iy [×10⁶ mm⁴]')
axes[1].set_ylabel('Hustota pravděpodobnosti')
axes[1].set_title('Osový kvadratický moment Iy')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_2E_histogramy.png', dpi=150, bbox_inches='tight')
plt.close()

# Vizualizace průřezu
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 8))
ax2.set_title('Příklad 2E — L-profil (úhelník)', fontsize=13, fontweight='bold')

# Obdélníky
colors = ['#4ECDC4', '#45B7D1']
labels = ['Vodorovné rameno (200×30)', 'Svislé rameno (30×170)']
rects_draw = [
    (0, 0, b_total, t),                    # Vodorovné rameno
    (0, t, t, h_total - t),                # Svislé rameno (nad rohem)
]
for (rx, ry, rw, rh), color, label in zip(rects_draw, colors, labels):
    rect = patches.Rectangle((rx, ry), rw, rh, linewidth=2,
                              edgecolor='black', facecolor=color, alpha=0.7, label=label)
    ax2.add_patch(rect)

ax2.plot(xC, yC, 'ro', markersize=10, zorder=5, label=f'Těžiště C ({xC:.1f}, {yC:.1f})')
ax2.axhline(y=yC, color='red', linestyle=':', alpha=0.5, label=f'osa x\' (y={yC:.1f})')
ax2.axvline(x=xC, color='blue', linestyle=':', alpha=0.5, label=f'osa y\' (x={xC:.1f})')

# Kóty
ax2.annotate('', xy=(0, -10), xytext=(200, -10),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax2.text(100, -18, '200 mm', ha='center', fontsize=9)

ax2.annotate('', xy=(210, 0), xytext=(210, 30),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax2.text(225, 15, '30', ha='left', fontsize=9)

ax2.annotate('', xy=(-15, 0), xytext=(-15, 200),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax2.text(-20, 100, '200 mm', ha='right', fontsize=9, rotation=90)

ax2.annotate('', xy=(40, 30), xytext=(40, 170),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax2.text(45, 100, '140', ha='left', fontsize=9)

ax2.annotate('', xy=(0, 208), xytext=(30, 208),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax2.text(15, 215, '30', ha='center', fontsize=9)

ax2.set_xlim(-40, 250)
ax2.set_ylim(-30, 230)
ax2.set_aspect('equal')
ax2.set_xlabel('x [mm]')
ax2.set_ylabel('y [mm]')
ax2.legend(loc='upper right', fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_2E_profil.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy.")
