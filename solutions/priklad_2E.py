"""
Příklad 2E — Osový kvadratický moment L-profilu k ose x a y
============================================================
Z-profil (úhelník) s rozměry z obrázku:
  - Horní příruba: šířka 30mm (vlevo) + 70mm (vpravo) = celkem offset, tloušťka 30mm
  - Stojina: šířka 30mm, výška 140mm
  - Dolní příruba: 30mm + 170mm, tloušťka 30mm

Interpretace obrázku (Z-profil / nerovnoramenný úhelník):
  Profil se skládá ze 3 obdélníků:
  1. Horní příruba: šířka (30+70)=100mm, výška 30mm, levý okraj na x=-30
  2. Stojina: šířka 30mm, výška 140mm
  3. Dolní příruba: šířka (30+170)=200mm, výška 30mm

Souřadný systém: počátek v levém dolním rohu dolní příruby.

Stochastické veličiny: normální rozdělení, CoV = 0.2
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================================
# 1. DETERMINISTICKÉ ŘEŠENÍ
# ============================================================

# Rozměry profilu (mm) — interpretace z obrázku 2E
# Profil (pohled na průřez):
#
#         |--30--|--70--|
#    y'   +------+------+  <- horní příruba, tloušťka 30mm
#   /     |  30mm       |
#  /      +--+----------+
# /       |30|              <- stojina, 30mm × 140mm
#         |  |   140mm
#         |  |
#    +----+--+              <- dolní příruba
#    | 30 |  | 170mm   |
#    +----+--+-----------+  tloušťka 30mm
#    x
#
# Počátek v levém dolním rohu celého profilu

# Dolní příruba (rectangle 3)
b3 = 30.0 + 170.0   # = 200 mm šířka
h3 = 30.0            # mm výška
x3_left = 0.0        # levý okraj
y3_bot = 0.0         # spodní okraj

# Stojina (rectangle 2)
b2 = 30.0            # mm šířka
h2 = 140.0           # mm výška
x2_left = 0.0        # levý okraj (zarovnán s levým okrajem dolní příruby)
y2_bot = h3           # spodní okraj = horní okraj dolní příruby = 30mm

# Horní příruba (rectangle 1)
# z obrázku: 30mm vlevo + 70mm vpravo od osy stojiny
# stojina je 0..30mm, takže horní příruba je od -30 (ne, nemůže být záporné s naším počátkem)
# Reinterpretace: horní příruba od x=-30 do x=30+70=100?
# Ale počátek je v levém dolním rohu dolní příruby.
# Stojina začíná na x=0, tedy osa stojiny je na x=15mm.
# Horní příruba: 30mm vlevo od levého okraje stojiny to 70mm vpravo od pravého okraje stojiny
# => od x = 0-30 = -30 do x = 30+70 = 100
# Ale to by znamenalo záporné x. Zkusím jinou interpretaci.

# Alternativní interpretace z 3D obrázku:
# Profil je Z-tvar (nebo nerovnoramenný úhelník)
# Horní příruba je posunuta doleva, dolní doprava
#
# Obrázek ukazuje:
#   y, y' nahoře
#   30mm — šířka horního ramene vlevo
#   70mm — výška/šířka horního ramene
#   30mm — tloušťka
#   140mm — výška stojiny
#   C — těžiště
#   30mm — tloušťka dolní části
#   30mm, 170mm — rozměry dolní příruby
#
# Zjednodušená interpretace jako 3 obdélníky v lokálním souřadném systému:

# Obdélník 1: Horní příruba
# Šířka = 30 + 70 = 100mm (30 vlevo od stojiny, 70 = šířka stojiny + přesah)
# Hmm, zpřesním. Podívejme se na obrázek znovu:
# Nahoře: 30mm (vlevo), 70mm (dole od toho = výška horní části)
# Vlevo od středu: 30mm šířka
# 140mm výška střední části
# Dole: 30mm výška, pak 30mm + 170mm šířky

# Myslím, že správná interpretace je:
# Profil je "Z" nebo "reversed C":
# 1) Horní příruba: 100mm × 30mm (30+70=100 šířka, 30 tloušťka)
#    - umístěna vlevo nahoře
# 2) Stojina: 30mm × 140mm
# 3) Dolní příruba: 200mm × 30mm (30+170=200 šířka, 30 tloušťka)
#    - umístěna vpravo dole

# Celková výška = 30 + 140 + 30 = 200mm

# Souřadný systém: počátek v levém dolním rohu dolní příruby
# Dolní příruba: x=[0, 200], y=[0, 30]
# Stojina: x=[0, 30], y=[30, 170]
# Horní příruba: x=[-70, 30], y=[170, 200]
#
# Ale to dává záporné x, což je OK pro výpočet, ale posunu počátek.
# Posunu vše o 70 doprava:
# Dolní příruba: x=[70, 270], y=[0, 30]
# Stojina: x=[70, 100], y=[30, 170]
# Horní příruba: x=[0, 100], y=[170, 200]

# Hmm, to stále nevypadá správně. Zkusím jiný přístup.
# Prostě definuju 3 obdélníky svými rozměry a pozicí těžiště.

def compute_section_properties(rectangles):
    """
    Vypočítá těžiště a osové kvadratické momenty složeného průřezu.
    rectangles = [(b, h, xc, yc), ...] kde:
      b = šířka, h = výška, xc,yc = souřadnice těžiště obdélníku
    """
    A_total = 0.0
    Sx = 0.0  # statický moment k ose x (pro výpočet yc)
    Sy = 0.0  # statický moment k ose y (pro výpočet xc)

    for b, h, xc, yc in rectangles:
        A = b * h
        A_total += A
        Sx += A * yc
        Sy += A * xc

    xC = Sy / A_total
    yC = Sx / A_total

    # Steinerova věta: Ix = Σ(Ix_i + A_i * dy_i²)
    Ix = 0.0
    Iy = 0.0

    for b, h, xc, yc in rectangles:
        A = b * h
        Ix_own = b * h**3 / 12
        Iy_own = b**3 * h / 12
        Ix += Ix_own + A * (yc - yC)**2
        Iy += Iy_own + A * (xc - xC)**2

    return A_total, xC, yC, Ix, Iy


# Definice profilu — Z-profil
# Obrázek 2E ukazuje:
# - Nahoře: rozměry 30mm a 70mm pro horní příruba
# - Stojina 30mm × 140mm
# - Dole: 30mm a 170mm
# - Všechny tloušťky 30mm

# Interpretace jako Z-profil:
# Horní příruba je posunuta vlevo od stojiny
# Dolní příruba je posunuta vpravo od stojiny

# Referenční bod: levý dolní roh stojiny = (0, 0)
# Celková výška profilu = 30 + 140 + 30 = 200mm

# Stojina: šířka 30, výška 140, těžiště na (15, 30+70) = (15, 100)
# Ale celková výška stojiny = 200mm (celý profil)?
# Ne, stojina je jen střední část = 140mm.

# Dolní příruba: šířka 200mm (30+170), výška 30mm
# Levý okraj na x=0 (zarovnán se stojinou vlevo)
# Těžiště: (100, 15)

# Stojina: šířka 30mm, výška 140mm
# Levý okraj na x=0
# Těžiště: (15, 30+70) = (15, 100)

# Horní příruba: šířka 100mm (30+70), výška 30mm
# Pravý okraj zarovnán s pravým okrajem stojiny (x=30)
# Tedy levý okraj na x = 30-100 = -70
# Těžiště: (-70+50, 170+15) = (-20, 185)

# Obdélníky: (b, h, xc, yc)
rects_det = [
    (200.0, 30.0, 100.0, 15.0),       # Dolní příruba
    (30.0, 140.0, 15.0, 100.0),        # Stojina
    (100.0, 30.0, -20.0, 185.0),       # Horní příruba
]

A, xC, yC, Ix, Iy = compute_section_properties(rects_det)

print("=" * 60)
print("PŘÍKLAD 2E — DETERMINISTICKÉ ŘEŠENÍ")
print("=" * 60)
print(f"Plocha průřezu: A = {A:.0f} mm²")
print(f"Těžiště: xC = {xC:.2f} mm, yC = {yC:.2f} mm")
print(f"Osový kvadratický moment:")
print(f"  Ix = {Ix:.0f} mm⁴ = {Ix/1e6:.4f} × 10⁶ mm⁴")
print(f"  Iy = {Iy:.0f} mm⁴ = {Iy/1e6:.4f} × 10⁶ mm⁴")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo
# ============================================================

N_sim = 100_000
CoV = 0.2
np.random.seed(42)

# Střední hodnoty rozměrů (mm)
dims_mean = {
    'b_bottom': 200.0,   # šířka dolní příruby
    'h_bottom': 30.0,    # výška dolní příruby
    'b_web': 30.0,       # šířka stojiny
    'h_web': 140.0,      # výška stojiny
    'b_top': 100.0,      # šířka horní příruby
    'h_top': 30.0,       # výška horní příruby
}

# Generování vzorků
samples = {}
for key, mu in dims_mean.items():
    sigma = mu * CoV
    samples[key] = np.random.normal(mu, sigma, N_sim)
    # Zajistit kladné rozměry
    samples[key] = np.maximum(samples[key], 1.0)

Ix_mc = np.zeros(N_sim)
Iy_mc = np.zeros(N_sim)
xC_mc = np.zeros(N_sim)
yC_mc = np.zeros(N_sim)

for i in range(N_sim):
    b_bot = samples['b_bottom'][i]
    h_bot = samples['h_bottom'][i]
    b_web = samples['b_web'][i]
    h_web = samples['h_web'][i]
    b_top = samples['b_top'][i]
    h_top = samples['h_top'][i]

    # Pozice těžišť obdélníků
    rects = [
        (b_bot, h_bot, b_bot/2, h_bot/2),                                  # Dolní příruba
        (b_web, h_web, b_web/2, h_bot + h_web/2),                          # Stojina
        (b_top, h_top, b_web/2 - b_top/2, h_bot + h_web + h_top/2),       # Horní příruba
    ]
    A_i, xC_i, yC_i, Ix_i, Iy_i = compute_section_properties(rects)
    Ix_mc[i] = Ix_i
    Iy_mc[i] = Iy_i
    xC_mc[i] = xC_i
    yC_mc[i] = yC_i

print("\n" + "=" * 60)
print("STOCHASTICKÁ ANALÝZA (Monte Carlo, N=100 000, CoV=0.2)")
print("=" * 60)
print(f"Ix: μ = {np.mean(Ix_mc)/1e6:.4f} × 10⁶ mm⁴,  σ = {np.std(Ix_mc)/1e6:.4f} × 10⁶ mm⁴,  "
      f"CoV = {np.std(Ix_mc)/np.mean(Ix_mc):.4f}")
print(f"Iy: μ = {np.mean(Iy_mc)/1e6:.4f} × 10⁶ mm⁴,  σ = {np.std(Iy_mc)/1e6:.4f} × 10⁶ mm⁴,  "
      f"CoV = {np.std(Iy_mc)/np.mean(Iy_mc):.4f}")
print(f"xC: μ = {np.mean(xC_mc):.2f} mm,  σ = {np.std(xC_mc):.2f} mm")
print(f"yC: μ = {np.mean(yC_mc):.2f} mm,  σ = {np.std(yC_mc):.2f} mm")

# Kvantily
for q_val in [0.025, 0.5, 0.975]:
    print(f"  Ix ({q_val*100:.1f}%) = {np.quantile(Ix_mc, q_val)/1e6:.4f} × 10⁶ mm⁴")

# ============================================================
# 3. GRAFY
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Příklad 2E — Osové kvadratické momenty Z-profilu\n'
             '(Monte Carlo, N=100 000, CoV=0.2)', fontsize=13, fontweight='bold')

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
ax2.set_title('Příklad 2E — Průřez Z-profilu', fontsize=13, fontweight='bold')

# Obdélníky
colors = ['#4ECDC4', '#45B7D1', '#96CEB4']
labels = ['Dolní příruba', 'Stojina', 'Horní příruba']
rects_draw = [
    (0, 0, 200, 30),          # Dolní příruba
    (0, 30, 30, 140),         # Stojina
    (-70, 170, 100, 30),      # Horní příruba
]
for (rx, ry, rw, rh), color, label in zip(rects_draw, colors, labels):
    rect = patches.Rectangle((rx, ry), rw, rh, linewidth=2,
                              edgecolor='black', facecolor=color, alpha=0.7, label=label)
    ax2.add_patch(rect)

ax2.plot(xC, yC, 'ro', markersize=10, zorder=5, label=f'Těžiště C ({xC:.1f}, {yC:.1f})')
ax2.axhline(y=yC, color='red', linestyle=':', alpha=0.5)
ax2.axvline(x=xC, color='red', linestyle=':', alpha=0.5)
ax2.set_xlim(-100, 230)
ax2.set_ylim(-20, 220)
ax2.set_aspect('equal')
ax2.set_xlabel('x [mm]')
ax2.set_ylabel('y [mm]')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/tmp/RST-2/solutions/priklad_2E_profil.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nGrafy uloženy.")
