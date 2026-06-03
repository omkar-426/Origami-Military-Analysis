import pandas as pd

data = {
    "Pattern": [
        "Miura-ori", "Yoshimura", "Waterbomb", "Resch",
        "Kresling", "Eggbox", "Ron-Resch",
        "Hexagonal Twist", "Triangulated Cylinder"
    ],
    "Domain": [
        "Aerospace", "Aerospace", "Medical", "Architecture",
        "Robotics", "Architecture", "Architecture",
        "Medical", "Robotics"
    ],
    "Fold_Type": [
        "Rigid", "Non-Rigid", "Rigid", "Non-Rigid",
        "Rigid", "Non-Rigid", "Semi-Rigid",
        "Semi-Rigid", "Rigid"
    ],
    "Poisson_Ratio": [
        -0.82, 0.31, 0.15, 0.28,
         0.09, -0.35, 0.22, 0.18, 0.12
    ],
    "Compression_Ratio": [
        0.94, 0.87, 0.76, 0.65,
        0.83, 0.71, 0.68, 0.60, 0.79
    ],
    "Degrees_of_Freedom": [
        1, 3, 2, 5, 1, 4, 6, 3, 2
    ],
    "Energy_Absorption_Jg": [
        2.8, 1.9, 3.4, 2.1,
        4.7, 2.3, 2.6, 3.1, 4.1
    ],
    "Blast_Attenuation_pct": [
        58, 28, 32, 22,
        45, 25, 20, 30, 40
    ],
    "Reusability": [
        "Cyclic", "One-time", "One-time", "One-time",
        "Cyclic", "One-time", "One-time",
        "Cyclic", "Cyclic"
    ],
    "Thermal_Efficiency_pct": [
        45, 20, 15, 65,
        30, 35, 60, 25, 40
    ],
    "Deployment_Time_min": [
        15, 25, 10, 45,
         8, 30, 50, 20, 12
    ],
    "Size_Stable": [
        False, True, True, True,
        True, True, True, True, True
    ],
    "Deployment_Reliability": [
        0.97, 0.78, 0.85, 0.70,
        0.91, 0.74, 0.67, 0.82, 0.89
    ],
}

df = pd.DataFrame(data)

# Save it
# Reset index cleanly before saving
df = df.reset_index(drop=True)

# Save — index=False means no row numbers saved as extra column
df.to_csv("origami_military_dataset.csv", index=False)

# Verify what was saved
verify = pd.read_csv("origami_military_dataset.csv")
print(f"\nSaved columns ({len(verify.columns)}):")
for col in verify.columns:
    print(f"  {col}")
print("Dataset saved.")
print(f"Shape: {df.shape}")
print("\n", df.to_string(index=False))