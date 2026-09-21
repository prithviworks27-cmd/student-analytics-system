"""
generate_training_data.py
--------------------------
Creates a synthetic dataset of (attendance %, marks %) -> risk label,
used to train the At-Risk classifier. Run this once to produce
training_data.csv, which train_model.py then reads.
"""

import random
import csv

random.seed(42)   # makes the "random" data reproducible - same output every run

rows = []
for _ in range(300):
    attendance_pct = round(random.uniform(30, 100), 1)
    marks_pct = round(random.uniform(20, 100), 1)

    # Rule of thumb for generating a label: genuinely at-risk students
    # tend to be low in BOTH attendance and marks, not just one.
    risk_score = (100 - attendance_pct) * 0.5 + (100 - marks_pct) * 0.5
    noise = random.uniform(-10, 10)   # real life isn't a clean formula
    label = "At Risk" if (risk_score + noise) > 45 else "Safe"

    rows.append([attendance_pct, marks_pct, label])

with open("training_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["attendance_pct", "marks_pct", "risk_label"])
    writer.writerows(rows)

print(f"Generated {len(rows)} training rows -> training_data.csv")