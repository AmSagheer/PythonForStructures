# PythonForStructures - Tool #05
# Rebar Weight & Cost Estimator — Are you over-ordering?
# Computes exact tonnage + cost from a bar schedule, using the
# standard unit weight formula (density = 7850 kg/m^3).

import numpy as np
import matplotlib.pyplot as plt

# --- INPUTS: Bar Schedule (diameter mm, count, cut length m) ---
# Example: one floor's worth of beam + column reinforcement
bar_schedule = [
    {"dia": 16, "count": 420, "length": 6.0},   # beam main bars
    {"dia": 12, "count": 680, "length": 2.4},   # stirrups/links
    {"dia": 20, "count": 180, "length": 6.0},   # column main bars
    {"dia": 25, "count": 96,  "length": 6.0},   # heavy column bars
]

STEEL_PRICE_PER_TON = 800   # USD/ton -- update to your local market rate
STEEL_DENSITY = 7850        # kg/m^3

# --- CALCULATE ---
def unit_weight_kg_per_m(dia_mm):
    # exact formula: density x cross-section area
    area_m2 = (np.pi / 4) * (dia_mm / 1000) ** 2
    return STEEL_DENSITY * area_m2

total_weight_kg = 0
rows = []
for bar in bar_schedule:
    w_per_m = unit_weight_kg_per_m(bar["dia"])
    bar_weight = w_per_m * bar["length"] * bar["count"]
    total_weight_kg += bar_weight
    rows.append([f"Ø{bar['dia']}mm", bar["count"], f"{bar['length']}m",
                 f"{w_per_m:.3f}", f"{bar_weight:,.1f}"])

total_tons = total_weight_kg / 1000
total_cost = total_tons * STEEL_PRICE_PER_TON

# --- THE RISK ANGLE: typical site over-order allowance ---
TYPICAL_WASTE_ALLOWANCE = 0.07   # many sites add a flat 5-10% "just in case"
naive_estimate_tons = total_tons * (1 + TYPICAL_WASTE_ALLOWANCE)
naive_cost = naive_estimate_tons * STEEL_PRICE_PER_TON
potential_savings = naive_cost - total_cost

print(f"Exact quantity   : {total_tons:.3f} tons  (${total_cost:,.0f})")
print(f"Typical site est.: {naive_estimate_tons:.3f} tons  (${naive_cost:,.0f})")
print(f"Potential savings from exact calc: ${potential_savings:,.0f}")

# --- VISUAL: bar schedule table (top) + cost comparison (bottom) ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 7.5),
                                gridspec_kw={'height_ratios': [1, 0.8]})

# bar schedule table
ax1.axis('off')
tbl = ax1.table(cellText=rows,
                 colLabels=["Bar", "Count", "Length", "Unit Wt (kg/m)", "Weight (kg)"],
                 cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 2.2)
for j in range(5):
    tbl[0, j].set_facecolor('#1B4F72')
    tbl[0, j].set_text_props(color='white', weight='bold')
ax1.set_title(f'Bar Schedule  →  Total = {total_tons:.3f} tons  (${total_cost:,.0f})',
              fontsize=12, weight='bold', pad=10)

# cost comparison bar chart
labels = ['Exact\nCalculation', 'Typical Site\nEstimate (+7%)']
costs = [total_cost, naive_cost]
colors = ['#2ECC71', '#E67E22']
bars = ax2.bar(labels, costs, color=colors, width=0.5)
for bar, cost in zip(bars, costs):
    ax2.text(bar.get_x() + bar.get_width()/2, cost + 15, f'${cost:,.0f}',
              ha='center', fontsize=11, weight='bold')
ax2.annotate(f'Potential savings:\n${potential_savings:,.0f}',
             xy=(0.5, max(costs)*0.55), fontsize=11, color='#C0392B',
             weight='bold', ha='center')
ax2.set_ylabel('Cost (USD)')
ax2.set_title('Exact Calculation vs. Typical Site Waste Allowance', fontsize=12, weight='bold')
ax2.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.savefig('rebar_estimator.png', dpi=150, bbox_inches='tight')
