# ============================================================
# STEP 5 — VISUALISATION (Fixed)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import warnings
warnings.filterwarnings("ignore")

df       = pd.read_csv("origami_clean.csv")
himalaya = pd.read_csv("himalaya_patrol_scores.csv")
jungle   = pd.read_csv("jungle_combat_scores.csv")
basecamp = pd.read_csv("base_camp_scores.csv")

BG       = "#111827"
CARD     = "#1f2937"
TEXT     = "#e2e8f0"
MUTED    = "#94a3b8"
TEAL     = "#5eead4"
AMBER    = "#fbbf24"
CORAL    = "#f87171"
LAVENDER = "#a5b4fc"
SLATE    = "#334155"

MISSION_COLORS = {
    "Himalaya Patrol" : LAVENDER,
    "Jungle Combat"   : TEAL,
    "Base Camp"       : AMBER,
}

plt.rcParams.update({
    "font.family"      : "DejaVu Sans",
    "font.size"        : 10,
    "text.color"       : TEXT,
    "axes.facecolor"   : CARD,
    "axes.labelcolor"  : TEXT,
    "axes.edgecolor"   : SLATE,
    "xtick.color"      : MUTED,
    "ytick.color"      : MUTED,
    "grid.color"       : SLATE,
    "grid.linewidth"   : 0.5,
    "figure.facecolor" : BG,
})

# ════════════════════════════════════════════════════════════
# CHART A — fixed: disqualified label only on disqualified rows
# ════════════════════════════════════════════════════════════

fig, axes = plt.subplots(1, 3, figsize=(22, 8))
fig.patch.set_facecolor(BG)
fig.suptitle(
    "Chart A — Pattern Suitability Scores by Mission",
    fontsize=16, fontweight="bold", color=TEXT, y=1.02
)

mission_data = {
    "Himalaya Patrol" : himalaya,
    "Jungle Combat"   : jungle,
    "Base Camp"       : basecamp,
}

for ax, (mission, data) in zip(axes, mission_data.items()):

    # Sort all patterns by score for consistent y positions
    data_sorted = data.sort_values("Score").reset_index(drop=True)
    patterns_ordered = data_sorted["Pattern"].tolist()
    scores = data_sorted["Score"].tolist()
    meets  = data_sorted["Meets_Constraint"].tolist()

    for i, (pattern, score, qualifies) in enumerate(
        zip(patterns_ordered, scores, meets)
    ):
        if qualifies:
            # Qualified bar
            is_winner = score == data_sorted[
                data_sorted["Meets_Constraint"]
            ]["Score"].max()
            color = AMBER if is_winner else MISSION_COLORS[mission]
            ax.barh(pattern, score,
                    color=color, edgecolor="none", height=0.55)
            ax.text(
                score + 1, i,
                f"{score}",
                va="center", fontsize=8.5,
                color=AMBER if is_winner else TEXT
            )
        else:
            # Disqualified — grey stub + label
            ax.barh(pattern, 2.5,
                    color=SLATE, edgecolor="none", height=0.55)
            ax.text(
                3.5, i,
                "disqualified",
                va="center", fontsize=6.5,
                color=CORAL, alpha=0.85
            )

    ax.set_title(mission, fontsize=11,
                 fontweight="bold", color=TEXT, pad=12)
    ax.set_xlim(0, 118)
    ax.set_xlabel("Score (0 – 100)", fontsize=9, color=MUTED)
    ax.set_yticks(range(len(patterns_ordered)))
    ax.set_yticklabels(patterns_ordered, fontsize=8.5)
    ax.grid(axis="x", alpha=0.3)
    ax.set_facecolor(CARD)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("outputs/chart_a_scores.png",
            dpi=150, bbox_inches="tight", facecolor=BG)
print("✓ Chart A saved")
plt.show()

# ════════════════════════════════════════════════════════════
# CHART B — fixed: proper circles using equal aspect ratio
# ════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(11, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_aspect("equal")   # ← this fixes ovals into circles
ax.axis("off")

fig.suptitle(
    "Chart B — Constraint Pass / Fail per Mission",
    fontsize=14, fontweight="bold", color=TEXT, y=0.97
)

patterns = df["Pattern"].tolist()
n = len(patterns)

col_labels = [
    "Himalaya Patrol\nDeploy ≤ 12 min",
    "Jungle Combat\nDoF ≤ 2",
    "Base Camp\nCyclic only",
]
col_colors = [LAVENDER, TEAL, AMBER]

constraints_check = [
    df["Deploy_Time_min"] <= 12,
    df["Degrees_of_Freedom"] <= 2,
    df["Reusability"] == "Cyclic",
]

# Column headers
for j, (label, color) in enumerate(zip(col_labels, col_colors)):
    ax.text(
        (j + 1) * 2.5, n * 1.1 + 0.3,
        label,
        ha="center", va="bottom",
        fontsize=9, fontweight="bold", color=color
    )

# Rows
for i, pattern in enumerate(patterns):
    y = (n - i - 1) * 1.1

    # Alternating row background
    if i % 2 == 0:
        rect = mpatches.FancyBboxPatch(
            (0.8, y - 0.45), 8.8, 0.9,
            boxstyle="round,pad=0.05",
            facecolor=CARD, edgecolor="none", zorder=0
        )
        ax.add_patch(rect)

    # Pattern label
    ax.text(
        0.9, y, pattern,
        ha="left", va="center",
        fontsize=9, color=TEXT
    )

    # Circles per mission
    for j, mask in enumerate(constraints_check):
        x = (j + 1) * 2.5
        passes = mask.iloc[i]

        if passes:
            circ = plt.Circle(
                (x, y), 0.32,
                color=TEAL, zorder=3
            )
            ax.add_patch(circ)
            ax.text(
                x, y, "✓",
                ha="center", va="center",
                fontsize=11, color=BG,
                fontweight="bold", zorder=4
            )
        else:
            circ = plt.Circle(
                (x, y), 0.32,
                color=SLATE, zorder=3
            )
            ax.add_patch(circ)
            ax.text(
                x, y, "✗",
                ha="center", va="center",
                fontsize=11, color=CORAL,
                fontweight="bold", zorder=4
            )

# Legend
legend_items = [
    mpatches.Patch(color=TEAL,  label="✓  Passes constraint"),
    mpatches.Patch(color=SLATE, label="✗  Disqualified"),
]
ax.legend(
    handles=legend_items,
    loc="lower right",
    bbox_to_anchor=(9.8, -0.5),
    fontsize=9, framealpha=0.15,
    labelcolor=TEXT
)

ax.set_xlim(0.5, 10)
ax.set_ylim(-1.2, n * 1.1 + 1.2)

plt.tight_layout()
plt.savefig("outputs/chart_b_constraints.png",
            dpi=150, bbox_inches="tight", facecolor=BG)
print("✓ Chart B saved")
plt.show()

# ════════════════════════════════════════════════════════════
# CHART C — Bubble plot (unchanged, was working fine)
# ════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(13, 9))
fig.patch.set_facecolor(BG)
ax.set_facecolor(CARD)

bubble_colors = [
    TEAL if r == "Cyclic" else CORAL
    for r in df["Reusability"]
]
sizes = df["Compression_Ratio"] * 900

ax.scatter(
    df["Deploy_Time_min"],
    df["Blast_Attn_pct"],
    s=sizes, c=bubble_colors,
    alpha=0.80, edgecolors=TEXT, linewidths=0.6, zorder=3
)

for _, row in df.iterrows():
    ax.annotate(
        row["Pattern"],
        (row["Deploy_Time_min"], row["Blast_Attn_pct"]),
        textcoords="offset points", xytext=(9, 4),
        fontsize=8.5, color=TEXT, alpha=0.9
    )

ax.axvline(x=12, color=LAVENDER,
           linestyle="--", linewidth=1.2, alpha=0.7)
ax.text(12.6, 54, "Himalaya Limit\n(12 min)",
        fontsize=7.5, color=LAVENDER, alpha=0.85)

ax.axhline(y=40, color=AMBER,
           linestyle="--", linewidth=1.2, alpha=0.7)
ax.text(42, 41, "Strong Protection\nThreshold (40%)",
        fontsize=7.5, color=AMBER, alpha=0.85)

ax.fill_between([0, 12], [40, 40], [65, 65],
                alpha=0.07, color=TEAL)
ax.text(1.5, 54, "Ideal Zone\n(Fast + Safe)",
        fontsize=8, color=TEAL, alpha=0.65)

legend_items = [
    mpatches.Patch(color=TEAL,  label="Cyclic — reusable after blast"),
    mpatches.Patch(color=CORAL, label="One-time — single use only"),
]
ax.legend(handles=legend_items, fontsize=8.5,
          framealpha=0.15, labelcolor=TEXT, loc="upper right")

ax.set_xlabel("Deployment Time (minutes)  —  Lower is Better",
              fontsize=10, color=MUTED)
ax.set_ylabel("Blast Attenuation %  —  Higher is Better",
              fontsize=10, color=MUTED)
ax.set_title(
    "Chart C — Deployment Speed vs Blast Protection\n"
    "(Bubble size = Compression Ratio)",
    fontsize=13, fontweight="bold", color=TEXT, pad=15
)
ax.grid(True, alpha=0.2)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("outputs/chart_c_bubble.png",
            dpi=150, bbox_inches="tight", facecolor=BG)
print("✓ Chart C saved")
plt.show()

# ════════════════════════════════════════════════════════════
# CHART D — Radar (unchanged, was working fine)
# ════════════════════════════════════════════════════════════

fig, ax = plt.subplots(figsize=(10, 10),
                        subplot_kw=dict(polar=True))
fig.patch.set_facecolor(BG)
ax.set_facecolor(CARD)

dimensions = [
    "Compression", "Blast\nProtection",
    "Thermal\nEfficiency", "Deploy\nSpeed", "Reliability"
]
N      = len(dimensions)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles += angles[:1]

def norm(col, invert=False):
    s = df[col]
    n = (s - s.min()) / (s.max() - s.min())
    return (1 - n) if invert else n

mi = df[df["Pattern"] == "Miura-ori"].index[0]
kr = df[df["Pattern"] == "Kresling"].index[0]

def rvals(idx):
    v = [
        norm("Compression_Ratio").iloc[idx],
        norm("Blast_Attn_pct").iloc[idx],
        norm("Thermal_Eff_pct").iloc[idx],
        norm("Deploy_Time_min", invert=True).iloc[idx],
        norm("Deployment_Reliability").iloc[idx],
    ]
    return v + v[:1]

mv = rvals(mi)
kv = rvals(kr)

ax.plot(angles, mv, color=AMBER, linewidth=2.5)
ax.fill(angles, mv, color=AMBER, alpha=0.12)
ax.scatter(angles[:-1], mv[:-1], color=AMBER, s=55, zorder=5)

ax.plot(angles, kv, color=LAVENDER, linewidth=2.5)
ax.fill(angles, kv, color=LAVENDER, alpha=0.12)
ax.scatter(angles[:-1], kv[:-1], color=LAVENDER, s=55, zorder=5)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(dimensions, fontsize=10.5, color=TEXT)
ax.set_yticks([0.25, 0.5, 0.75, 1.0])
ax.set_yticklabels(["0.25","0.5","0.75","1.0"],
                   fontsize=7, color=MUTED)
ax.set_ylim(0, 1.15)
ax.grid(color=SLATE, linewidth=0.8)
ax.spines["polar"].set_color(SLATE)

legend_items = [
    Line2D([0],[0], color=AMBER, linewidth=2.5,
           label="Miura-ori  —  Jungle + Base Camp"),
    Line2D([0],[0], color=LAVENDER, linewidth=2.5,
           label="Kresling   —  Himalaya Patrol"),
]
ax.legend(handles=legend_items, loc="upper right",
          bbox_to_anchor=(1.38, 1.18),
          fontsize=9.5, framealpha=0.15, labelcolor=TEXT)

ax.set_title(
    "Chart D — Miura-ori vs Kresling\n"
    "Head to Head Across All Dimensions",
    fontsize=13, fontweight="bold", color=TEXT, pad=28
)

plt.tight_layout()
plt.savefig("outputs/chart_d_radar.png",
            dpi=150, bbox_inches="tight", facecolor=BG)
print("✓ Chart D saved")
plt.show()

print("\n✓ All 4 charts saved to outputs/ folder")