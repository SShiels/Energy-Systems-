import sys
from pathlib import Path

import pandas as pd

# ---- settings -------------------------------------------------------------
INPUT_FILE = r"C:\Users\Sophie\Downloads\results_cv5_EN_RF_2xGP_merged.csv"   # path to your .csv or .xlsx (or pass as argument)
SEPARATOR = "/"               # e.g. "Scenario_0.5"; change to " " or " | " if you like
SCEN_COL = "Scenario / Variables"
PROP_COL = "Init_Prop"
# ---------------------------------------------------------------------------

path = Path(sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE)

if path.suffix.lower() in (".xlsx", ".xls"):
    df = pd.read_excel(path)
else:
    df = pd.read_csv(path)

df.columns = df.columns.str.strip()  # guard against stray whitespace in headers

for col in (SCEN_COL, PROP_COL):
    if col not in df.columns:
        sys.exit(f"Column '{col}' not found. Columns are: {list(df.columns)}")

has_prop = df[PROP_COL].notna()
df.loc[has_prop, SCEN_COL] = (
    df.loc[has_prop, SCEN_COL].astype(str) + SEPARATOR + df.loc[has_prop, PROP_COL].astype(str)
)

df = df.drop(columns=[PROP_COL])

out_path = path.with_name(path.stem + "_merged" + path.suffix)
if path.suffix.lower() in (".xlsx", ".xls"):
    df.to_excel(out_path, index=False)
else:
    df.to_csv(out_path, index=False)

print(f"Updated {has_prop.sum()} rows. Saved to: {out_path}")