# ============================================================
# STEP 4 — SCORING ENGINE
# Takes mission requirements as input
# Outputs a ranked recommendation for each mission
#
# Weights come from our EDA findings — not random numbers.
# Each weight reflects what a soldier actually needs.
# ============================================================

import pandas as pd
import numpy as np

# Load clean dataset
df = pd.read_csv("origami_clean.csv")

# ── Mission weight profiles ───────────────────────────────────
# These weights are YOUR decisions based on EDA findings
# Himalaya: compression + thermal matter most (altitude survival)
# Jungle: speed + blast matter most (ambush combat)
# Base Camp: blast + reliability matter most (permanent target)

MISSION_PROFILES = {

    "Himalaya Patrol": {
        "Compression_Ratio"      : 0.30,
        "Thermal_Eff_pct"        : 0.25,
        "Blast_Attn_pct"         : 0.20,
        "Deployment_Reliability" : 0.15,
        "Deploy_Time_min"        : 0.10,
    },

    "Jungle Combat": {
        "Deploy_Time_min"        : 0.30,
        "Blast_Attn_pct"         : 0.25,
        "Deployment_Reliability" : 0.20,
        "Compression_Ratio"      : 0.15,
        "Thermal_Eff_pct"        : 0.10,
    },

    "Base Camp": {
        "Blast_Attn_pct"         : 0.30,
        "Deployment_Reliability" : 0.25,
        "Deploy_Time_min"        : 0.20,
        "Compression_Ratio"      : 0.15,
        "Thermal_Eff_pct"        : 0.10,
    },
}

# ── Normalization ─────────────────────────────────────────────
# Before scoring we normalize every column to 0-1
# So a 58% blast and a 0.94 compression can be compared fairly
#
# Two types:
# Higher is better → normal normalize (compression, blast, thermal, reliability)
# Lower is better  → invert normalize (deploy time — faster = better)

def normalize_higher_is_better(series):
    rng = series.max() - series.min()
    if rng == 0:
        return series * 0 + 0.5
    return (series - series.min()) / rng

def normalize_lower_is_better(series):
    # Invert: lowest value gets score of 1.0
    rng = series.max() - series.min()
    if rng == 0:
        return series * 0 + 0.5
    return 1 - (series - series.min()) / rng

# Build normalized version of dataset
df_norm = df.copy()
df_norm["Compression_Ratio"]       = normalize_higher_is_better(df["Compression_Ratio"])
df_norm["Blast_Attn_pct"]          = normalize_higher_is_better(df["Blast_Attn_pct"])
df_norm["Thermal_Eff_pct"]         = normalize_higher_is_better(df["Thermal_Eff_pct"])
df_norm["Deployment_Reliability"]  = normalize_higher_is_better(df["Deployment_Reliability"])
df_norm["Deploy_Time_min"]         = normalize_lower_is_better(df["Deploy_Time_min"])
# Deploy time is INVERTED because 8 min is better than 50 min

# ── Scoring function ──────────────────────────────────────────
# ── Hard constraints per mission ──────────────────────────────
# These are NOT weights — they are disqualifiers.
# A pattern either meets them or scores zero.
#
# Himalaya : Deploy ≤ 12 min (cold exposure is survival risk)
# Jungle   : DoF ≤ 2 (one soldier, under fire, no complex folds)
# Base Camp: Must be Cyclic (permanent target, needs repeat protection)

MISSION_CONSTRAINTS = {
    "Himalaya Patrol": {
        "column"   : "Deploy_Time_min",
        "operator" : "<=",
        "value"    : 12,
        "reason"   : "≤12 min deploy (cold exposure risk at altitude)"
    },
    "Jungle Combat": {
        "column"   : "Degrees_of_Freedom",
        "operator" : "<=",
        "value"    : 2,
        "reason"   : "DoF ≤ 2 (single soldier deployment under stress)"
    },
    "Base Camp": {
        "column"   : "Reusability",
        "operator" : "==",
        "value"    : "Cyclic",
        "reason"   : "Must be reusable (permanent target, repeat attacks)"
    },
}

# ── Scoring function ──────────────────────────────────────────
def score_mission(mission_name):
    weights    = MISSION_PROFILES[mission_name]
    constraint = MISSION_CONSTRAINTS[mission_name]
    result     = df[["Pattern", "Domain", "Fold_Type"]].copy()

    # Calculate weighted score for each pattern
    total_score = pd.Series(0.0, index=df.index)
    for col, weight in weights.items():
        total_score += df_norm[col] * weight

    result["Score"] = (total_score * 100).round(1)

    # Add key columns for context
    result["Compression"]  = df["Compression_Ratio"]
    result["Blast_pct"]    = df["Blast_Attn_pct"]
    result["Thermal_pct"]  = df["Thermal_Eff_pct"]
    result["Deploy_min"]   = df["Deploy_Time_min"]
    result["Reliability"]  = df["Deployment_Reliability"]
    result["Reusability"]  = df["Reusability"]
    result["DoF"]          = df["Degrees_of_Freedom"]

    # ── Apply hard constraint ─────────────────────────────────
    col = constraint["column"]
    val = constraint["value"]
    op  = constraint["operator"]

    if op == "<=":
        meets = df[col] <= val
    elif op == "==":
        meets = df[col] == val
    elif op == ">=":
        meets = df[col] >= val

    result["Meets_Constraint"] = meets

    # Disqualify patterns that fail constraint
    result.loc[~meets, "Score"] = 0.0

    # Sort by score
    result = result.sort_values("Score", ascending=False)\
                   .reset_index(drop=True)
    result.index = result.index + 1
    result.index.name = "Rank"

    return result, constraint

# ── Run all three missions ────────────────────────────────────
missions    = ["Himalaya Patrol", "Jungle Combat", "Base Camp"]
all_results = {}

for mission in missions:
    print("\n" + "=" * 60)
    print(f"  MISSION: {mission.upper()}")
    print("=" * 60)

    result, constraint = score_mission(mission)
    all_results[mission] = result

    # Show constraint being applied
    print(f"\n  Hard Constraint: {constraint['reason']}")

    # Show which patterns passed and failed
    passed = result[result["Meets_Constraint"] == True]
    failed = result[result["Meets_Constraint"] == False]
    print(f"  Passed: {list(passed['Pattern'])}")
    print(f"  Failed: {list(failed['Pattern'])}")

    # Top 3 qualifying patterns only
    print(f"\n  Top 3 QUALIFYING patterns:\n")
    top3 = passed.head(3)[["Pattern", "Score",
                            "Reusability", "DoF", "Deploy_min"]]
    print(top3.to_string())

    winner = passed.iloc[0]
    print(f"\n  ★ Recommendation: {winner['Pattern']}")
    print(f"    Score      : {winner['Score']}/100")
    print(f"    Compression: {winner['Compression']}")
    print(f"    Blast      : {winner['Blast_pct']}%")
    print(f"    Thermal    : {winner['Thermal_pct']}%")
    print(f"    Deploy     : {winner['Deploy_min']} min")
    print(f"    Reliability: {winner['Reliability']}")
    print(f"    Reusability: {winner['Reusability']}")
    print(f"    DoF        : {winner['DoF']}")

# ── Final summary ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FINAL MILITARY RECOMMENDATION SUMMARY")
print("=" * 60)
for mission in missions:
    passed = all_results[mission][
        all_results[mission]["Meets_Constraint"] == True
    ]
    winner = passed.iloc[0]
    print(f"\n  {mission:20s} → {winner['Pattern']:25s}"
          f"(Score: {winner['Score']}/100)")

# Save results
for mission in missions:
    filename = mission.lower().replace(" ", "_") + "_scores.csv"
    all_results[mission].to_csv(filename)

print("\n✓ All score files saved")

# ── Final summary ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FINAL MILITARY RECOMMENDATION SUMMARY")
print("=" * 60)
for mission in missions:
    winner = all_results[mission].iloc[0]
    score  = all_results[mission].iloc[0]["Score"]
    print(f"\n  {mission:20s} → {winner['Pattern']:25s} (Score: {score}/100)")

# Save all results
for mission in missions:
    filename = mission.lower().replace(" ", "_") + "_scores.csv"
    all_results[mission].to_csv(filename)

print("\n✓ All score files saved")