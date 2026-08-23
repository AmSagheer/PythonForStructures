# PythonForStructures - Tool #08
# Concrete Strength Test Acceptance Checker — ACI 318-19 Sec. 26.12.3.1
# Verified against the published ACI worked example dataset.

import numpy as np
import matplotlib.pyplot as plt
from brand import *

apply_style()

# --- INPUTS ---
fc_specified = 24.0   # specified compressive strength, f'c (MPa)

# strength test results (each = avg of cylinder pair), MPa
# this exact dataset matches the published ACI E702 worked example
test_results = [29.0, 29.3, 29.7, 30.3, 28.8, 27.8, 27.3,
                 25.0, 23.4, 26.1, 23.0, 24.3, 23.0, 23.0, 23.0]

tests = np.array(test_results)
n = len(tests)

# --- CRITERION 1: running average of any 3 consecutive tests >= f'c ---
running_avg = np.array([tests[i-2:i+1].mean() if i >= 2 else np.nan
                         for i in range(n)])
crit1_fail = np.where((~np.isnan(running_avg)) & (running_avg < fc_specified))[0]

# --- CRITERION 2: individual test tolerance ---
if fc_specified <= 35:
    tolerance = 3.5
else:
    tolerance = 0.10 * fc_specified
individual_limit = fc_specified - tolerance
crit2_fail = np.where(tests < individual_limit)[0]

# --- DESCRIPTIVE STATS ---
mean_strength = tests.mean()
std_dev = tests.std(ddof=1)

print(f"Mean strength = {mean_strength:.2f} MPa, Std Dev = {std_dev:.2f} MPa")
print(f"Individual test limit (f'c - {tolerance:.1f}) = {individual_limit:.1f} MPa")
print(f"Criterion 2 failures (individual test too low): tests {[i+1 for i in crit2_fail]}")
print(f"Criterion 1 failures (3-test running avg < f'c): tests {[i+1 for i in crit1_fail]}")

# --- VISUAL: test results bar + running average line, pass/fail highlighted ---
fig, ax = plt.subplots(figsize=(10, 5))
add_blueprint_grid(ax, alpha=0.15)

x = np.arange(1, n + 1)
bar_colors = [RED_FAIL if i in crit2_fail else STEEL_BLUE for i in range(n)]
ax.bar(x, tests, color=bar_colors, width=0.55, zorder=3, label='Individual test')

ax.plot(x[2:], running_avg[2:], color=GOLD_DARK, lw=2.2, marker='o',
        markersize=5, zorder=4, label='3-test running average')
for i in crit1_fail:
    ax.plot(x[i], running_avg[i], marker='o', markersize=9,
            color=RED_FAIL, zorder=5)

ax.axhline(fc_specified, color=INK_NAVY, ls='-', lw=1.5, zorder=2)
ax.text(n + 0.3, fc_specified, f"f'c = {fc_specified:.0f}", va='center',
        fontsize=9.5, color=INK_NAVY, weight='bold')
ax.axhline(individual_limit, color=RED_FAIL, ls='--', lw=1.2, alpha=0.7, zorder=2)
ax.text(n + 0.3, individual_limit, f"limit = {individual_limit:.1f}", va='center',
        fontsize=8.5, color=RED_FAIL)

ax.set_xlabel('Strength Test Number')
ax.set_ylabel('Compressive Strength (MPa)')
ax.set_title("Concrete Strength Acceptance — ACI 318-19 Sec. 26.12.3.1", fontsize=13)
ax.set_xlim(0.3, n + 1.8)
ax.legend(loc='lower left', fontsize=9, framealpha=0.9)
ax.spines[['top', 'right']].set_visible(False)

n_fail = len(set(crit1_fail) | set(crit2_fail))
verdict = f"{n_fail} test(s) flag a code violation" if n_fail else "All tests meet ACI 318-19 criteria"
gold_highlight_box(ax, n * 0.45, tests.max() * 1.02, verdict, fontsize=10)

add_brand_footer(fig, 8, "Concrete Strength")
plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig('concrete_strength.png', dpi=150, bbox_inches='tight', facecolor=PAPER_WHITE)
