# PythonForStructures - Post #1
# Shear & Moment Diagrams: Simply Supported Beam + Point Load

import numpy as np
import matplotlib.pyplot as plt

# --- INPUTS (change these 3 numbers) ---
L = 6.0      # span length (m)
P = 80.0     # point load (kN)
a = 2.0      # load position from left support (m)

# --- REACTIONS ---
Rb = P * a / L
Ra = P - Rb

# --- BUILD DIAGRAMS ---
x = np.linspace(0, L, 500)
shear  = np.where(x < a, Ra, Ra - P)
moment = np.where(x < a, Ra * x, Ra * x - P * (x - a))

# --- PLOT ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7))
ax1.fill_between(x, shear, color='#2E86DE', alpha=0.3)
ax1.plot(x, shear, color='#2E86DE', lw=2)
ax1.axhline(0, color='black', lw=0.8)
ax1.set_title('Shear Force Diagram (kN)')
ax1.grid(alpha=0.3)

ax2.fill_between(x, moment, color='#EE5253', alpha=0.3)
ax2.plot(x, moment, color='#EE5253', lw=2)
ax2.axhline(0, color='black', lw=0.8)
ax2.set_title('Bending Moment Diagram (kN·m)')
ax2.set_xlabel('Distance along beam (m)')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('beam_diagram.png', dpi=120)
print(f"Ra = {Ra:.1f} kN | Rb = {Rb:.1f} kN")
print(f"Max moment = {moment.max():.1f} kN·m at x = {x[moment.argmax()]:.2f} m")
