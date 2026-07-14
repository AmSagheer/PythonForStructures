# PythonForStructures - Tool #02
# ACI 318-19 Load Combinations Generator (Table 5.3.1)
# Input your loads. Get a visual table. See the governing one highlighted.

import pandas as pd
import matplotlib.pyplot as plt

# --- INPUTS (kN or kN/m — your choice, stay consistent) ---
D  = 50.0    # Dead Load
L  = 60.0    # Live Load
Lr = 10.0    # Roof Live Load
S  =  5.0    # Snow Load
R  =  0.0    # Rain Load
W  = 15.0    # Wind Load
E  = 12.0    # Earthquake Load

roof_load = max(Lr, S, R)   # governing roof-type load

# --- ACI 318-19 TABLE 5.3.1 BASIC LOAD COMBINATIONS ---
combos = {
    "1.4D"                               : 1.4*D,
    "1.2D + 1.6L + 0.5(Lr/S/R)"          : 1.2*D + 1.6*L + 0.5*roof_load,
    "1.2D + 1.6(Lr/S/R) + 1.0L"          : 1.2*D + 1.6*roof_load + 1.0*L,
    "1.2D + 1.6(Lr/S/R) + 0.5W"          : 1.2*D + 1.6*roof_load + 0.5*W,
    "1.2D + 1.0W + 1.0L + 0.5(Lr/S/R)"   : 1.2*D + 1.0*W + 1.0*L + 0.5*roof_load,
    "1.2D + 1.0E + 1.0L + 0.2S"          : 1.2*D + 1.0*E + 1.0*L + 0.2*S,
    "0.9D + 1.0W"                         : 0.9*D + 1.0*W,
    "0.9D + 1.0E"                         : 0.9*D + 1.0*E,
}

df = pd.DataFrame(list(combos.items()), columns=["Load Combination", "Value (kN)"])
df = df.sort_values("Value (kN)", ascending=False).reset_index(drop=True)
df.index += 1
df["Value (kN)"] = df["Value (kN)"].round(1)

# --- RENDER AS A CLEAN TABLE IMAGE ---
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.axis('off')

tbl = ax.table(
    cellText=df.values,
    colLabels=["Load Combination", "Value (kN)"],
    rowLabels=[str(i) for i in df.index],
    cellLoc='center',
    loc='center'
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 2.0)

# style header row
for j in range(2):
    cell = tbl[0, j]
    cell.set_facecolor('#1B4F72')
    cell.set_text_props(color='white', weight='bold')

# highlight governing row (index 1 = top row after sort)
for j in range(2):
    cell = tbl[1, j]
    cell.set_facecolor('#F9E79F')
    cell.set_text_props(weight='bold')

# widen combination column
for i in range(len(df) + 1):
    tbl[i, 0].set_width(0.62)
    tbl[i, 1].set_width(0.22)

plt.title("ACI 318-19 Load Combinations — Table 5.3.1\nGoverning combination highlighted",
          fontsize=12, weight='bold', pad=14)
plt.tight_layout()
plt.savefig('load_combinations_table.png', dpi=150, bbox_inches='tight')

print(f"Governing: {df.iloc[0]['Load Combination']} = {df.iloc[0]['Value (kN)']} kN")
print("Table saved as load_combinations_table.png")