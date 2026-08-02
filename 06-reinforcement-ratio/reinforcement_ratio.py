# PythonForStructures - Tool #06
# Reinforcement Ratio Checker — ACI 318-19 (SI units)
# Checks provided steel against BOTH the minimum (9.6.1.2) and
# maximum (tension-controlled strain limit, 9.3.3.1) requirements.

import numpy as np
import matplotlib.pyplot as plt

# --- INPUTS ---
fc  = 28.0     # concrete compressive strength (MPa)
fy  = 420.0    # steel yield strength (MPa)
bw  = 300.0    # beam width (mm)
d   = 450.0    # effective depth (mm)
As_provided = 1200.0   # actual steel area provided (mm^2)

# --- MINIMUM REINFORCEMENT — ACI 318-19 Eq. 9.6.1.2(a),(b) ---
As_min_a = (0.25 * np.sqrt(fc) / fy) * bw * d
As_min_b = (1.4 / fy) * bw * d
As_min = max(As_min_a, As_min_b)

# --- MAXIMUM REINFORCEMENT — tension-controlled limit (εt >= 0.005) ---
# beta_1 per ACI 318-19 Table 22.2.2.4.3
if fc <= 28:
    beta1 = 0.85
else:
    beta1 = max(0.65, 0.85 - 0.05 * (fc - 28) / 7)

eps_cu = 0.003
eps_t_min = 0.005   # tension-controlled limit for beams (Pu < 0.10 f'c Ag)
rho_max = 0.85 * beta1 * (fc / fy) * (eps_cu / (eps_cu + eps_t_min))
As_max = rho_max * bw * d

# --- CHECK ---
rho_provided = As_provided / (bw * d)
status_min = "PASS" if As_provided >= As_min else "FAIL (under-reinforced)"
status_max = "PASS" if As_provided <= As_max else "FAIL (over-reinforced, not tension-controlled)"

print(f"As,min = {As_min:.0f} mm^2  -> {status_min}")
print(f"As,max = {As_max:.0f} mm^2  -> {status_max}")
print(f"As,provided = {As_provided:.0f} mm^2  (rho = {rho_provided:.4f})")

# --- VISUAL: range bar showing min / provided / max ---
fig, ax = plt.subplots(figsize=(9, 3.2))

ax.barh(0, As_max - As_min, left=As_min, height=0.4,
        color='#D5F5E3', edgecolor='#27AE60', label='Acceptable range')

marker_color = '#27AE60' if (As_min <= As_provided <= As_max) else '#C0392B'
ax.plot(As_provided, 0, marker='D', markersize=16, color=marker_color, zorder=5)
ax.annotate(f'As,provided\n{As_provided:.0f} mm²', xy=(As_provided, 0),
            xytext=(As_provided, 0.55), ha='center', fontsize=10, weight='bold',
            color=marker_color)

ax.axvline(As_min, color='#7D3C98', ls='--', lw=1.2)
ax.text(As_min, -0.55, f'As,min\n{As_min:.0f} mm²', ha='center', fontsize=9, color='#7D3C98')
ax.axvline(As_max, color='#7D3C98', ls='--', lw=1.2)
ax.text(As_max, -0.55, f'As,max\n{As_max:.0f} mm²', ha='center', fontsize=9, color='#7D3C98')

ax.set_xlim(0, As_max * 1.25)
ax.set_ylim(-1, 1)
ax.get_yaxis().set_visible(False)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.set_xlabel('Steel Area (mm²)')
verdict = "WITHIN ACI 318-19 LIMITS" if (As_min <= As_provided <= As_max) else "OUTSIDE ACI 318-19 LIMITS"
ax.set_title(f'Reinforcement Ratio Check — {verdict}', fontsize=12, weight='bold',
             color=marker_color)

plt.tight_layout()
plt.savefig('reinforcement_ratio.png', dpi=150, bbox_inches='tight')
