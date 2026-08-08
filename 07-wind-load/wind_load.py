# PythonForStructures - Tool #07
# Wind Load Calculator — ASCE 7 Velocity Pressure & Windward Wall Pressure
# Covers: velocity pressure (Eq. 26.10-1) + MWFRS windward wall design pressure.
# Does NOT cover: components & cladding, leeward/side walls, roof, or
# topographic/flexible-structure effects beyond the defaults below.

import numpy as np
import matplotlib.pyplot as plt
from brand import *

apply_style()

# --- INPUTS ---
V   = 115.0    # basic wind speed (mph), from ASCE 7 wind speed map
z   = 30.0     # height above ground (ft)
exposure = "C"  # B, C, or D

Kzt = 1.0      # topographic factor (1.0 = no hill/escarpment effect)
Kd  = 0.85     # wind directionality factor (buildings, MWFRS)
Ke  = 1.0      # ground elevation factor (1.0 = near sea level)
G   = 0.85     # gust effect factor (rigid structures)
Cp_windward = 0.8    # windward wall external pressure coefficient
GCpi = 0.18          # internal pressure coefficient (enclosed building)

# --- EXPOSURE CATEGORY CONSTANTS (ASCE 7, Table 26.11-1) ---
exposure_params = {
    "B": {"alpha": 7.0,  "zg": 1200},
    "C": {"alpha": 9.5,  "zg": 900},
    "D": {"alpha": 11.5, "zg": 700},
}
alpha = exposure_params[exposure]["alpha"]
zg    = exposure_params[exposure]["zg"]

# --- VELOCITY PRESSURE EXPOSURE COEFFICIENT ---
z_eff = max(z, 15 if exposure != "D" else 7)  # zmin per ASCE 7
Kz = 2.01 * (z_eff / zg) ** (2 / alpha)

# --- VELOCITY PRESSURE (ASCE 7 Eq. 26.10-1) ---
qz = 0.00256 * Kz * Kzt * Kd * Ke * V**2   # psf

# --- WINDWARD WALL DESIGN PRESSURE (MWFRS, Eq. 27.3-1) ---
p_base = qz * G * Cp_windward
p_add  = qz * GCpi     # worst-case: internal suction adds to external pressure
p_max  = p_base + p_add
p_min  = p_base - p_add

print(f"Kz  = {Kz:.3f}")
print(f"qz  = {qz:.1f} psf")
print(f"Windward wall pressure: {p_min:.1f} to {p_max:.1f} psf")
print(f"Governing (worst case): {p_max:.1f} psf")

# --- VISUAL: Kz profile with height (left) + pressure summary (right) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5), gridspec_kw={'width_ratios': [1.1, 1]})

heights = np.linspace(15, 200, 100)
Kz_profile = 2.01 * (np.maximum(heights, 15) / zg) ** (2 / alpha)
add_blueprint_grid(ax1, alpha=0.15)
ax1.plot(Kz_profile, heights, color=STEEL_BLUE, lw=2.5)
ax1.plot(Kz, z, marker='D', markersize=13, color=GOLD_DARK, zorder=5,
         markeredgecolor=INK_NAVY, markeredgewidth=1)
ax1.annotate(f'  z = {z:.0f} ft\n  Kz = {Kz:.3f}', xy=(Kz, z), fontsize=9.5,
             color=INK_NAVY, weight='bold', va='center')
ax1.set_xlabel('Kz (velocity pressure exposure coefficient)')
ax1.set_ylabel('Height above ground (ft)')
ax1.set_title(f'Exposure {exposure} — Kz vs. Height', fontsize=12)
ax1.spines[['top', 'right']].set_visible(False)
ax1.spines['left'].set_color(BLUEPRINT_BLUE)
ax1.spines['bottom'].set_color(BLUEPRINT_BLUE)

ax2.axis('off')
rows = [
    ["Basic wind speed (V)", f"{V:.0f} mph"],
    ["Exposure category", exposure],
    ["Velocity pressure (qz)", f"{qz:.1f} psf"],
    ["Windward wall pressure", f"{p_min:.1f} – {p_max:.1f} psf"],
]
tbl = ax2.table(cellText=rows, cellLoc='left', loc='center', colWidths=[0.62, 0.38])
tbl.auto_set_font_size(False)
tbl.set_fontsize(10.5)
tbl.scale(1, 2.4)
for i in range(len(rows)):
    tbl[i, 0].set_text_props(color=BLUEPRINT_BLUE)
    tbl[i, 1].set_text_props(weight='bold', color=INK_NAVY)
    for j in range(2):
        tbl[i, j].set_edgecolor(FOG_GREY)

gold_highlight_box(ax2, 0.5, 0.08, f'Governing pressure: {p_max:.1f} psf', fontsize=11)
ax2.set_title('Design Summary (MWFRS, windward wall)', fontsize=12)

add_brand_footer(fig, 7, "Wind Load (ASCE 7)")
plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('wind_load.png', dpi=150, bbox_inches='tight', facecolor=PAPER_WHITE)
