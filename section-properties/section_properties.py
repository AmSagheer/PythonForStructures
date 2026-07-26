# PythonForStructures - Tool #04
# Section Property Calculator — Rectangular & I-Sections
# Area, centroid, moment of inertia, section modulus, radius of gyration.

import numpy as np
import matplotlib.pyplot as plt

# --- INPUTS: I-Section (mm) ---
bf = 300     # flange width
tf = 12      # flange thickness
d  = 300     # overall depth
tw = 8       # web thickness

# --- CALCULATE PROPERTIES (about strong axis, x-x) ---
# Break into 3 rectangles: top flange, web, bottom flange
hw = d - 2*tf   # clear web height

# Areas
A_f = bf * tf
A_w = tw * hw
A_total = 2*A_f + A_w

# Centroid (symmetric section -> at mid-depth)
y_bar = d / 2

# Moment of inertia about x-x (centroidal), using parallel axis theorem
# Flange centroids are at distance (d/2 - tf/2) from NA
y_f = d/2 - tf/2
I_f_own = (bf * tf**3) / 12
I_f = 2 * (I_f_own + A_f * y_f**2)

I_w = (tw * hw**3) / 12   # web centroid coincides with NA

I_total = I_f + I_w

# Section modulus (top/bottom fiber, symmetric -> same both sides)
c = d / 2
S = I_total / c

# Radius of gyration
r = np.sqrt(I_total / A_total)

# --- OUTPUT ---
print(f"Area              A  = {A_total:,.0f} mm^2")
print(f"Moment of Inertia Ix = {I_total:,.0f} mm^4")
print(f"Section Modulus   Sx = {S:,.0f} mm^3")
print(f"Radius of Gyration rx = {r:.1f} mm")

# --- VISUAL: section diagram (left) + properties table (right) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.5),
                                gridspec_kw={'width_ratios': [1, 1.1]})

# draw I-section
x0 = -bf/2
ax1.add_patch(plt.Rectangle((x0, d - tf), bf, tf, facecolor='#2E86DE', edgecolor='black'))
ax1.add_patch(plt.Rectangle((x0, 0), bf, tf, facecolor='#2E86DE', edgecolor='black'))
ax1.add_patch(plt.Rectangle((-tw/2, tf), tw, hw, facecolor='#2E86DE', edgecolor='black'))
ax1.axhline(d/2, color='#EE5253', ls='--', lw=1.2)
ax1.text(bf/2 + 8, d/2, 'N.A.', color='#EE5253', va='center', fontsize=9)

# dimension labels
ax1.annotate('', xy=(x0, d + 15), xytext=(x0+bf, d + 15),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax1.text(0, d + 22, f'bf = {bf} mm', ha='center', fontsize=9)
ax1.annotate('', xy=(bf/2 + 25, 0), xytext=(bf/2 + 25, d),
             arrowprops=dict(arrowstyle='<->', color='black'))
ax1.text(bf/2 + 32, d/2, f'd = {d} mm', va='center', fontsize=9, rotation=90)

ax1.set_xlim(-bf, bf)
ax1.set_ylim(-20, d + 40)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.set_title('I-Section', fontsize=12, weight='bold')

# properties table
ax2.axis('off')
rows = [
    ["Area (A)", f"{A_total:,.0f} mm²"],
    ["Moment of Inertia (Ix)", f"{I_total:,.0f} mm⁴"],
    ["Section Modulus (Sx)", f"{S:,.0f} mm³"],
    ["Radius of Gyration (rx)", f"{r:.1f} mm"],
]
tbl = ax2.table(cellText=rows,
                 colLabels=["Section Property", "Value"],
                 cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 2.6)
for j in range(2):
    tbl[0, j].set_facecolor('#1B4F72')
    tbl[0, j].set_text_props(color='white', weight='bold')
ax2.set_title('Computed Properties (about x-x)', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig('section_properties.png', dpi=150, bbox_inches='tight')
