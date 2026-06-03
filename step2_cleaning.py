# ============================================================
# STEP 2 — DATA CLEANING
# Load the raw CSV, find problems, fix them, save clean version
# ============================================================

import pandas as pd

# ── Load the raw dataset ─────────────────────────────────────
df = pd.read_csv("origami_military_dataset.csv")

# Drop ghost columns — any column with "Unnamed" in the name
# These appear when CSV has trailing commas during save
unnamed_cols = [col for col in df.columns if "Unnamed" in col]
if unnamed_cols:
    df = df.drop(columns=unnamed_cols)
    print(f"✓ Dropped ghost columns: {unnamed_cols}")
else:
    print("✓ No ghost columns found")

print("=" * 50)
print("STEP 2A — FIRST LOOK AT RAW DATA")
print("=" * 50)

# Basic shape
print(f"\nRows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

# Column names and their data types
print("\nColumn names and types:")
print(df.dtypes)

# ── Check 1: Missing values ───────────────────────────────────
print("\n" + "=" * 50)
print("CHECK 1 — MISSING VALUES")
print("=" * 50)
missing = df.isnull().sum()
print(missing)
print(f"\nTotal missing cells: {missing.sum()}")
# What we expect: 0 missing — we built this dataset ourselves
# If any show up, something went wrong during save/load

# ── Check 2: Duplicate rows ───────────────────────────────────
print("\n" + "=" * 50)
print("CHECK 2 — DUPLICATE ROWS")
print("=" * 50)
duplicates = df.duplicated().sum()
print(f"Duplicate rows found: {duplicates}")
# What we expect: 0 — each pattern is unique

# ── Check 3: Unique values in text columns ────────────────────
print("\n" + "=" * 50)
print("CHECK 3 — UNIQUE VALUES IN CATEGORY COLUMNS")
print("=" * 50)
for col in ["Domain", "Fold_Type", "Reusability", "Size_Stable"]:
    print(f"\n{col}: {df[col].unique()}")
# Why: catch typos like "Cyclic " vs "Cyclic" (space makes them different)
# Also check if Size_Stable loaded as text or boolean

# ── Check 4: Numeric ranges ───────────────────────────────────
print("\n" + "=" * 50)
print("CHECK 4 — NUMERIC RANGES (min / max)")
print("=" * 50)
numeric_cols = [
    "Poisson_Ratio", "Compression_Ratio", "Degrees_of_Freedom",
    "Energy_Absorption_Jg", "Blast_Attenuation_pct",
    "Thermal_Efficiency_pct", "Deployment_Time_min",
    "Deployment_Reliability"
]
for col in numeric_cols:
    print(f"{col:30s} min={df[col].min():.2f}  max={df[col].max():.2f}")
# Why: catch impossible values
# e.g. Reliability > 1.0 would be impossible
# e.g. Negative deployment time would be a mistake

# ════════════════════════════════════════════════════════════
# FIXES
# ════════════════════════════════════════════════════════════

print("\n" + "=" * 50)
print("APPLYING FIXES")
print("=" * 50)

# Fix 1 — Rename long column names
df = df.rename(columns={
    "Deployment_Time_min": "Deploy_Time_min",
    "Blast_Attenuation_pct": "Blast_Attn_pct",
    "Thermal_Efficiency_pct": "Thermal_Eff_pct"
})
print("✓ Fix 1: Renamed long column names")

# Fix 2 — Convert Size_Stable to proper boolean
# CSV saves True/False as strings "TRUE"/"FALSE"
# We convert back to actual Python boolean
df["Size_Stable"] = df["Size_Stable"].map(
    {"TRUE": True, "FALSE": False, True: True, False: False}
)
print("✓ Fix 2: Size_Stable converted to boolean")

# Fix 3 — Convert Reusability to numeric
# "Cyclic" = 1 (reusable, better for military)
# "One-time" = 0 (single use)
# Why numeric: scoring engine needs numbers, not text
df["Reusability_Score"] = df["Reusability"].map(
    {"Cyclic": 1, "One-time": 0}
)
print("✓ Fix 3: Reusability converted to numeric (Cyclic=1, One-time=0)")

# Fix 4 — Round all floats to 2 decimal places
# For consistency in display
float_cols = df.select_dtypes(include="float").columns
df[float_cols] = df[float_cols].round(2)
print("✓ Fix 4: Float columns rounded to 2 decimal places")

# Fix 5 — Strip whitespace from all text columns
# Catches invisible spaces like "Cyclic " vs "Cyclic"
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].str.strip()
print("✓ Fix 5: Whitespace stripped from text columns")

# ── Final check after fixes ───────────────────────────────────
print("\n" + "=" * 50)
print("CLEAN DATASET — FINAL STATE")
print("=" * 50)
print(f"\nShape: {df.shape}")
print("\nColumn types after fixes:")
print(df.dtypes)
print("\nFull clean dataset:")
print(df.to_string(index=False))

# ── Save clean version ────────────────────────────────────────
df.to_csv("origami_clean.csv", index=False)
print("\n✓ Clean dataset saved → origami_clean.csv")

# Prove Size_Stable is actually boolean in Python
print("\nSize_Stable dtype:", df["Size_Stable"].dtype)
print("Miura-ori Size_Stable value:", df.loc[df["Pattern"]=="Miura-ori", "Size_Stable"].values[0])
print("Type:", type(df.loc[df["Pattern"]=="Miura-ori", "Size_Stable"].values[0]))