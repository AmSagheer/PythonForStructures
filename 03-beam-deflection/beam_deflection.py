# PythonForStructures - Tool #03
# Beam Deflection Checker — ACI 318-19 Table 24.2.2 Serviceability Limits
# Simply supported beam, point load. Checks computed deflection against
# all 4 ACI deflection limit categories.

import numpy as np
import matplotlib.pyplot as plt

# --- INPUTS ---
L  = 10.0        # span length (m)
P  = 150.0       # point load (kN)
a  = 2.0        # load position from left support (m)
E  = 200e6      # modulus of elasticity (kN/m^2)
I  = 0.0002     # moment of inertia (m^4)

# --- DEFLECTED SHAPE (simply supported beam, point load) ---
b = L - a
x1 = np.linspace(0, a, 250)
x2 = np.linspace(a, L, 250)
y1 = (P*b*x1/(6*L*E*I)) * (L**2 - b**2 - x1**2)
y2 = (P*a*(L-x2)/(6*L*E*I)) * (2*L*x2 - a**2 - x2**2)
x = np.concatenate([x1, x2])
y_mm = np.concatenate([y1, y2]) * 1000     # positive = downward magnitude

max_defl = y_mm.max()
x_at_max = x[np.argmax(y_mm)]

# --- ACI 318-19 TABLE 24.2.2 — MAXIMUM PERMISSIBLE DEFLECTIONS ---
L_mm = L * 1000
limits = {
    "Flat roof (not supporting elements\nlikely to be damaged) — L/180": L_mm/180,
    "Floor (not supporting elements\nlikely to be damaged) — L/360":     L_mm/360,
    "Roof/floor supporting elements\nlikely to be damaged — L/480":      L_mm/480,
    "Roof/floor supporting elements\nNOT likely to be damaged — L/240":  L_mm/240,
}

print(f"Computed deflection = {max_defl:.2f} mm at x = {x_at_max:.2f} m\n")
print("ACI 318-19 Table 24.2.2 check:")
rows = []
for case, limit in limits.items():
    status = "PASS" if max_defl <= limit else "FAIL"
    short_case = case.splitlines()[0] + " " + case.splitlines()[1]
    rows.append([short_case, f"{limit:.1f}", status])
    print(f"  {case.splitlines()[0]:<45s} limit={limit:6.1f} mm  -> {status}")

# --- FIGURE: deflected shape (top) + ACI compliance table (bottom) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8),
                                gridspec_kw={'height_ratios': [1, 1.1]})

# deflected shape
y_plot = -y_mm
ax1.plot(x, y_plot, color='#2E86DE', lw=2.5)
ax1.fill_between(x, y_plot, 0, color='#2E86DE', alpha=0.15)
ax1.axhline(0, color='black', lw=1)
ax1.plot(0, 0, marker='^', color='black', markersize=12)
ax1.plot(L, 0, marker='^', color='black', markersize=12)
ax1.plot(a, 0, marker='v', color='#EE5253', markersize=10)
ax1.annotate(f'P = {P} kN', xy=(a, 0), xytext=(a, max(y_plot)*0.3 + 1.5),
             ha='center', fontsize=10, color='#EE5253')
ax1.annotate(f'Max deflection\n{max_defl:.2f} mm at x={x_at_max:.2f} m',
             xy=(x_at_max, -max_defl), xytext=(x_at_max + 0.6, -max_defl - 2),
             fontsize=10, color='#2E86DE',
             arrowprops=dict(arrowstyle='->', color='#2E86DE'))
ax1.set_xlabel('Distance along beam (m)')
ax1.set_ylabel('Deflection (mm)')
ax1.set_title('Beam Deflection — Simply Supported, Point Load')
ax1.grid(alpha=0.3)

# ACI compliance table
ax2.axis('off')
tbl = ax2.table(
    cellText=rows,
    colLabels=["ACI 318-19 Table 24.2.2 — Deflection Limit Case", "Limit (mm)", "Status"],
    cellLoc='center', loc='center'
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 2.4)
for j in range(3):
    tbl[0, j].set_facecolor('#1B4F72')
    tbl[0, j].set_text_props(color='white', weight='bold')
for i in range(1, len(rows)+1):
    status = rows[i-1][2]
    color = '#D5F5E3' if status == 'PASS' else '#FADBD8'
    tbl[i, 2].set_facecolor(color)
    tbl[i, 2].set_text_props(weight='bold')
tbl[0, 0].set_width(0.55)
for i in range(len(rows)+1):
    tbl[i, 0].set_width(0.55)
ax2.set_title(f'Computed deflection = {max_defl:.2f} mm  →  checked against all 4 ACI cases',
              fontsize=11, weight='bold', pad=10)

plt.tight_layout()
plt.savefig('beam_deflection_aci.png', dpi=150, bbox_inches='tight')
