# Origami Military Shelter Analysis
### Deployable Field Structures for Indian Army — Himalayas & Northeast Jungle

A data analysis project examining 9 origami crease patterns 
to recommend deployable field shelters for Indian Army soldiers 
in two extreme terrain conditions.

---

## Key Results

| Mission | Winner | Score |
|---|---|---|
| Himalaya Patrol | Kresling | 63.0/100 |
| Jungle Combat | Miura-ori | 91.0/100 |
| Base Camp | Miura-ori | 92.7/100 |

> Miura-ori and Kresling are like a long sword and a short sword.
> Same function, similar strengths, but one is built for open field
> and the other for close quarters. The mission decides the weapon.

---

## Project Structure

origami_engineering_analysis/
├── dataset.py               # Build dataset from literature
├── step2_cleaning.py        # Data cleaning and validation
├── step3_eda.py             # Exploratory data analysis
├── step4_scoring.py         # Mission scoring engine
├── step5_visualisation.py   # All 4 charts
├── findings.md              # Written findings
├── origami_military_dataset.csv
├── origami_clean.csv
└── outputs/
├── chart_a_scores.png
├── chart_b_constraints.png
├── chart_c_bubble.png
└── chart_d_radar.png

## What this project covers

- Dataset built from published engineering literature
- Data cleaning and validation
- Exploratory data analysis — 5 key questions
- Mission-based weighted scoring engine with hard constraints
- 4 visualisation charts

## Data Sources
- Schenk & Guest 2013 — Poisson ratios (Miura-ori)
- JAXA IKAROS mission 2010 — Compression ratios
- Bhovad et al. 2019 — Energy absorption (Kresling)
- Notre Dame Kinetic Structure Lab — Thermal efficiency

## 📓 Full Analysis on Kaggle
[View Kaggle Notebook](https://www.kaggle.com/code/omcaru/origami-military-shelter-analysis-indian-army-fi)

---
*Tools: Python · Pandas · NumPy · Matplotlib*