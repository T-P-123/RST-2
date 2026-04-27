"""
Příklad 2E — Osový kvadratický moment nesymetrického průřezu (3 obdélníky)
==========================================================================
Průřez složený ze 3 obdélníků (počátek v levém dolním rohu obalu):

    +-100-+
    | (3) | 30 mm  horní pásnice (užší, vlevo zarovnaná)
    +-----+----+
    |30|        ^
    |  | (2)    | 140 mm  stojina (zarovnaná k levému okraji)
    |  |        |
    +--+        v
    +----------------------+
    |        (1)           | 30 mm  spodní pásnice (širší)
    +----------------------+
    <------- 200 mm ------->

Rozměry:
  - Spodní pásnice (1): 200 × 30 mm
  - Stojina (2):         30 × 140 mm  (vlevo)
  - Horní pásnice (3):  100 × 30 mm   (vlevo)
  - 70 mm = hloubka 3D tělesa (extruze), neovlivňuje 2D průřez

Stochastické veličiny: normální rozdělení, CoV = 0.2
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


def compute_section_properties(rectangles):
    """rectangles = [(b, h, xc, yc), ...]; vrací (A, xC, yC, Ix', Iy')."""
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
        Ix += b * h**3 / 12 + A * (yc - yC) ** 2
        Iy += b**3 * h / 12 + A * (xc - xC) ** 2
    return A_total, xC, yC, Ix, Iy


# ============================================================
# 1. DETERMINISTICKÉ ŘEŠENÍ
# ============================================================
b1, h1 = 200.0, 30.0   # spodní pásnice
b2, h2 = 30.0, 140.0   # stojina
b3, h3 = 100.0, 30.0   # horní pásnice

# Souřadnice těžišť dílčích obdélníků (počátek = levý dolní roh obalu)
rects_det = [
    (b1, h1, b1 / 2, h1 / 2),                      # (1) 100, 15
    (b2, h2, b2 / 2, h1 + h2 / 2),                 # (2) 15, 100
    (b3, h3, b3 / 2, h1 + h2 + h3 / 2),            # (3) 50, 185
]

A, xC, yC, Ix_p, Iy_p = compute_section_properties(rects_det)

# Momenty k vnějším osám (okraje obalu)
Ix_outer = Ix_p + A * yC**2
Iy_outer = Iy_p + A * xC**2

print("=" * 60)
print("PŘÍKLAD 2E — DETERMINISTICKÉ ŘEŠENÍ (nesymetrický průřez)")
print("=" * 60)
print(f"\nPlocha: A = {A:.0f} mm²")
print(f"Těžiště: x_C = {xC:.2f} mm, y_C = {yC:.2f} mm")
print(f"\nTěžišťové momenty:")
print(f"  Ix' = {Ix_p/1e6:.4f} × 10⁶ mm⁴")
print(f"  Iy' = {Iy_p/1e6:.4f} × 10⁶ mm⁴")
print(f"\nMomenty k vnějším osám:")
print(f"  Ix  = {Ix_outer/1e6:.4f} × 10⁶ mm⁴")
print(f"  Iy  = {Iy_outer/1e6:.4f} × 10⁶ mm⁴")

# ============================================================
# 2. STOCHASTICKÁ ANALÝZA — Monte Carlo
# ============================================================
N_sim = 100_000
CoV = 0.2
np.random.seed(42)

dims_mean = {
    "b1": 200.0, "h1": 30.0,
    "b2": 30.0,  "h2": 140.0,
    "b3": 100.0, "h3": 30.0,
}

samples = {}
for key, mu in dims_mean.items():
    sigma = mu * CoV
    s = np.random.normal(mu, sigma, N_sim)
    samples[key] = np.maximum(s, 1.0)

Ix_mc = np.zeros(N_sim)
Iy_mc = np.zeros(N_sim)
xC_mc = np.zeros(N_sim)
yC_mc = np.zeros(N_sim)

for i in range(N_sim):
    b1i, h1i = samples["b1"][i], samples["h1"][i]
    b2i, h2i = samples["b2"][i], samples["h2"][i]
    b3i, h3i = samples["b3"][i], samples["h3"][i]
    rects = [
        (b1i, h1i, b1i / 2, h1i / 2),
        (b2i, h2i, b2i / 2, h1i + h2i / 2),
        (b3i, h3i, b3i / 2, h1i + h2i + h3i / 2),
    ]
    A_i, xC_i, yC_i, Ix_i, Iy_i = compute_section_properties(rects)
    Ix_mc[i] = Ix_i
    Iy_mc[i] = Iy_i
    xC_mc[i] = xC_i
    yC_mc[i] = yC_i

print(f"\n{'='*60}")
print(f"STOCHASTICKÁ ANALÝZA (Monte Carlo, N={N_sim:,}, CoV={CoV})")
print("=" * 60)
print(f"Ix': μ = {np.mean(Ix_mc)/1e6:.4f} × 10⁶ mm⁴, σ = {np.std(Ix_mc)/1e6:.4f}, "
      f"CoV = {np.std(Ix_mc)/np.mean(Ix_mc):.4f}")
print(f"Iy': μ = {np.mean(Iy_mc)/1e6:.4f} × 10⁶ mm⁴, σ = {np.std(Iy_mc)/1e6:.4f}, "
      f"CoV = {np.std(Iy_mc)/np.mean(Iy_mc):.4f}")
print(f"xC:  μ = {np.mean(xC_mc):.2f} mm, σ = {np.std(xC_mc):.2f} mm")
print(f"yC:  μ = {np.mean(yC_mc):.2f} mm, σ = {np.std(yC_mc):.2f} mm")
for q_val in [0.025, 0.5, 0.975]:
    print(f"  Ix' ({q_val*100:.1f}%) = {np.quantile(Ix_mc, q_val)/1e6:.4f} × 10⁶ mm⁴")

# ============================================================
# 3. GRAFY
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Příklad 2E — Osové kvadratické momenty (těžišťové)\n"
             f"Monte Carlo, N={N_sim:,}, CoV={CoV}", fontsize=13, fontweight="bold")

axes[0].hist(Ix_mc / 1e6, bins=80, density=True, alpha=0.7, color="steelblue", edgecolor="white")
axes[0].axvline(Ix_p / 1e6, color="red", linewidth=2, linestyle="--",
                label=f"Determin. = {Ix_p/1e6:.2f}×10⁶")
axes[0].set_xlabel("Ix' [×10⁶ mm⁴]")
axes[0].set_ylabel("Hustota pravděpodobnosti")
axes[0].set_title("Těžišťový moment Ix'")
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].hist(Iy_mc / 1e6, bins=80, density=True, alpha=0.7, color="steelblue", edgecolor="white")
axes[1].axvline(Iy_p / 1e6, color="red", linewidth=2, linestyle="--",
                label=f"Determin. = {Iy_p/1e6:.2f}×10⁶")
axes[1].set_xlabel("Iy' [×10⁶ mm⁴]")
axes[1].set_ylabel("Hustota pravděpodobnosti")
axes[1].set_title("Těžišťový moment Iy'")
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "priklad_2E_histogramy.png"), dpi=150, bbox_inches="tight")
plt.close()

# Vizualizace průřezu — 3 obdélníky
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 8))
ax2.set_title("Příklad 2E — Nesymetrický průřez (3 obdélníky)", fontsize=13, fontweight="bold")

colors = ["#4ECDC4", "#45B7D1", "#FFA07A"]
labels = [f"(1) Spodní pásnice {b1:.0f}×{h1:.0f}",
          f"(2) Stojina {b2:.0f}×{h2:.0f}",
          f"(3) Horní pásnice {b3:.0f}×{h3:.0f}"]
rects_draw = [
    (0, 0, b1, h1),                  # spodní pásnice
    (0, h1, b2, h2),                 # stojina
    (0, h1 + h2, b3, h3),            # horní pásnice
]
for (rx, ry, rw, rh), color, label in zip(rects_draw, colors, labels):
    rect = patches.Rectangle((rx, ry), rw, rh, linewidth=2,
                             edgecolor="black", facecolor=color, alpha=0.75, label=label)
    ax2.add_patch(rect)

ax2.plot(xC, yC, "ro", markersize=10, zorder=5,
         label=f"Těžiště C ({xC:.2f}, {yC:.2f})")
ax2.axhline(y=yC, color="red", linestyle=":", alpha=0.6, label=f"osa x' (y={yC:.2f})")
ax2.axvline(x=xC, color="blue", linestyle=":", alpha=0.6, label=f"osa y' (x={xC:.2f})")

# Kóty
ax2.annotate("", xy=(0, -10), xytext=(b1, -10),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(b1 / 2, -18, f"{b1:.0f} mm", ha="center", fontsize=9)

ax2.annotate("", xy=(b1 + 12, 0), xytext=(b1 + 12, h1),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(b1 + 16, h1 / 2, f"{h1:.0f}", ha="left", fontsize=9)

ax2.annotate("", xy=(-15, h1), xytext=(-15, h1 + h2),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(-20, h1 + h2 / 2, f"{h2:.0f}", ha="right", fontsize=9, rotation=90)

ax2.annotate("", xy=(b2 + 5, h1), xytext=(b2 + 5, h1 + h2),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(b2 + 9, h1 + h2 / 2, f"({b2:.0f})", ha="left", fontsize=8, color="gray")

ax2.annotate("", xy=(0, h1 + h2 + h3 + 8), xytext=(b3, h1 + h2 + h3 + 8),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(b3 / 2, h1 + h2 + h3 + 14, f"{b3:.0f}", ha="center", fontsize=9)

ax2.annotate("", xy=(b3 + 10, h1 + h2), xytext=(b3 + 10, h1 + h2 + h3),
             arrowprops=dict(arrowstyle="<->", color="black"))
ax2.text(b3 + 14, h1 + h2 + h3 / 2, f"{h3:.0f}", ha="left", fontsize=9)

ax2.set_xlim(-40, b1 + 30)
ax2.set_ylim(-30, h1 + h2 + h3 + 30)
ax2.set_aspect("equal")
ax2.set_xlabel("x [mm]")
ax2.set_ylabel("y [mm]")
ax2.legend(loc="upper right", fontsize=9)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "priklad_2E_profil.png"), dpi=150, bbox_inches="tight")
plt.close()

print("\nGrafy uloženy.")
