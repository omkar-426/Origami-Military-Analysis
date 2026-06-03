# ============================================================
# STEP 3 — EXPLORATORY DATA ANALYSIS (EDA)
# We ask questions. The data answers.
# No charts yet. Just numbers and logic.
# ============================================================

import pandas as pd
import numpy as np

# Load the clean dataset
df = pd.read_csv("origami_clean.csv")

print("=" * 55)
print("ORIGAMI MILITARY DATASET — EDA")
print("=" * 55)

# ── Q1: Which pattern packs the smallest? ────────────────────
print("\n📦 Q1: Which pattern compresses the most?")
print("   (Best for soldiers carrying it on long patrols)")
print()

q1 = df[["Pattern", "Compression_Ratio"]]\
       .sort_values("Compression_Ratio", ascending=False)
print(q1.to_string(index=False))

best_compression = q1.iloc[0]
print(f"\n→ Winner: {best_compression['Pattern']} "
      f"({best_compression['Compression_Ratio']} ratio)")
print(f"  Meaning: packs to "
      f"{round((1 - best_compression['Compression_Ratio']) * 100, 1)}%"
      f" of original volume")

# ── Q2: Which pattern survives the most blasts? ──────────────
print("\n\n💥 Q2: Which pattern protects best against blasts?")
print("   (Critical for jungle combat, IED threats)")
print()

q2 = df[["Pattern", "Blast_Attn_pct", "Reusability", "Energy_Absorption_Jg"]]\
       .sort_values("Blast_Attn_pct", ascending=False)
print(q2.to_string(index=False))

best_blast = q2.iloc[0]
print(f"\n→ Winner: {best_blast['Pattern']} "
      f"({best_blast['Blast_Attn_pct']}% blast blocked)")
print(f"  Reusable after blast: {best_blast['Reusability']}")

# ── Q3: Do fast-deploying patterns sacrifice protection? ──────
print("\n\n⚡ Q3: Does faster deployment mean less protection?")
print("   (Trade-off analysis: speed vs safety)")
print()

q3 = df[["Pattern", "Deploy_Time_min", "Blast_Attn_pct"]]\
       .sort_values("Deploy_Time_min")
print(q3.to_string(index=False))

# Calculate correlation
corr = df["Deploy_Time_min"].corr(df["Blast_Attn_pct"])
print(f"\n→ Correlation between deploy speed and blast protection: {corr:.2f}")
if corr < -0.3:
    print("  Finding: Faster patterns tend to protect LESS")
elif corr > 0.3:
    print("  Finding: Faster patterns actually protect MORE")
else:
    print("  Finding: Speed and protection are INDEPENDENT")
    print("  Meaning: you don't have to sacrifice one for the other")

# ── Q4: Which domain has most reliable patterns? ─────────────
print("\n\n🛡️  Q4: Which engineering domain produces most")
print("   reliable patterns for military use?")
print()

q4 = df.groupby("Domain")["Deployment_Reliability"]\
       .agg(["mean", "min", "max", "count"])\
       .round(2)\
       .sort_values("mean", ascending=False)
q4.columns = ["Avg Reliability", "Worst", "Best", "Count"]
print(q4.to_string())

best_domain = q4.index[0]
print(f"\n→ Most reliable domain: {best_domain}")
print(f"  Avg reliability: {q4.iloc[0]['Avg Reliability']}")

# ── Q5: The unexpected finding ────────────────────────────────
print("\n\n🔍 Q5: Do auxetic patterns (negative Poisson ratio)")
print("   actually perform better in military metrics?")
print("   (We never planned this question — data led us here)")
print()

auxetic     = df[df["Poisson_Ratio"] < 0]
non_auxetic = df[df["Poisson_Ratio"] >= 0]

print("AUXETIC PATTERNS (ν < 0):")
print(auxetic[["Pattern", "Poisson_Ratio",
               "Blast_Attn_pct", "Deployment_Reliability"]]\
      .to_string(index=False))

print("\nNON-AUXETIC PATTERNS (ν ≥ 0):")
print(non_auxetic[["Pattern", "Poisson_Ratio",
                    "Blast_Attn_pct", "Deployment_Reliability"]]\
      .to_string(index=False))

print(f"\nAverage blast attenuation:")
print(f"  Auxetic patterns    : "
      f"{auxetic['Blast_Attn_pct'].mean():.1f}%")
print(f"  Non-auxetic patterns: "
      f"{non_auxetic['Blast_Attn_pct'].mean():.1f}%")

print(f"\nAverage reliability:")
print(f"  Auxetic patterns    : "
      f"{auxetic['Deployment_Reliability'].mean():.2f}")
print(f"  Non-auxetic patterns: "
      f"{non_auxetic['Deployment_Reliability'].mean():.2f}")

diff = auxetic['Blast_Attn_pct'].mean() - \
       non_auxetic['Blast_Attn_pct'].mean()

if diff > 5:
    print(f"\n→ Unexpected finding: Auxetic patterns block "
          f"{diff:.1f}% more blast pressure on average")
    print("  This suggests auxetic behavior is genuinely "
          "advantageous for military shelters")
else:
    print(f"\n→ Finding: Auxetic behavior alone doesn't "
          f"determine blast performance")
    print("  Other geometric factors matter more")

# ── Summary of findings ───────────────────────────────────────
print("\n" + "=" * 55)
print("EDA SUMMARY — KEY FINDINGS")
print("=" * 55)
