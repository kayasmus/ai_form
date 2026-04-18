"""
Generate Synthetic Bad-Form Data
=================================
Takes good-form columns from paired_data.csv (real side-on videos) and creates
additional synthetic (bad, good) pairs for training.

Applies outlier filter (delta < 40°) to synthetic data before saving.

Output:
    synthetic_paired_data.csv
"""

import numpy as np
import pandas as pd
from pathlib import Path

# ── Config ─────────────────────────────────────────────────────────────────────
INPUT_CSV  = str(Path(__file__).parent / "paired_data.csv")
OUTPUT_CSV = str(Path(__file__).parent / "synthetic_paired_data.csv")
VARIANTS_PER_FRAME = 5
RANDOM_SEED = 42
OUTLIER_DELTA = 40.0  # filter out synthetic pairs where delta > this

np.random.seed(RANDOM_SEED)

FEATURE_COLS = [
    "left_arm_raise", "right_arm_raise",
    "left_elbow_angle", "right_elbow_angle",
    "torso_lean", "arm_symmetry",
    "left_wrist_above_shoulder", "right_wrist_above_shoulder",
]

LATERAL_RAISE_MISTAKES = [
    {
        "name": "arms_too_high",
        "description": "Raising arms past shoulder height — traps take over",
        "perturbations": {
            "left_arm_raise":  (25.0, 8.0),
            "right_arm_raise": (25.0, 8.0),
            "torso_lean":      (5.0,  2.0),
        }
    },
    {
        "name": "arms_too_low",
        "description": "Not raising arms high enough — half reps",
        "perturbations": {
            "left_arm_raise":  (-25.0, 8.0),
            "right_arm_raise": (-25.0, 8.0),
        }
    },
    {
        "name": "elbows_too_bent",
        "description": "Bending elbows excessively — turns into a curl",
        "perturbations": {
            "left_elbow_angle":  (-30.0, 10.0),
            "right_elbow_angle": (-30.0, 10.0),
        }
    },
    {
        "name": "torso_swinging",
        "description": "Using momentum — body swings to cheat the weight up",
        "perturbations": {
            "torso_lean":      (12.0, 5.0),
            "left_arm_raise":  (10.0, 5.0),
            "right_arm_raise": (10.0, 5.0),
        }
    },
    {
        "name": "asymmetric_raise",
        "description": "One arm higher than the other — uneven strength",
        "perturbations": {
            "left_arm_raise":  (15.0, 5.0),
            "right_arm_raise": (-10.0, 5.0),
            "arm_symmetry":    (20.0, 5.0),
        }
    },
    {
    "name": "bad_posture_good_arms",
    "description": "Torso and elbow issues but arm height correct",
    "perturbations": {
        "torso_lean":        (10.0, 4.0),
        "left_elbow_angle":  (-20.0, 8.0),
        "right_elbow_angle": (-20.0, 8.0),
        "arm_symmetry":      (10.0, 4.0),
    }
    },
]

FEATURE_BOUNDS = {
    "left_arm_raise":             (5,    170),
    "right_arm_raise":            (5,    170),
    "left_elbow_angle":           (30,   180),
    "right_elbow_angle":          (30,   180),
    "torso_lean":                 (60,   130),  # side-on: ~90° is upright
    "arm_symmetry":               (0,    80),
    "left_wrist_above_shoulder":  (-0.4, 0.4),
    "right_wrist_above_shoulder": (-0.4, 0.4),
}


def apply_perturbation(good_row, mistake_template):
    bad = {}
    for feat in FEATURE_COLS:
        good_val = good_row[feat]
        if feat in mistake_template["perturbations"]:
            bias, noise_std = mistake_template["perturbations"][feat]
            bad_val = good_val + bias + np.random.normal(0, noise_std)
        else:
            noise = np.random.normal(0, 2.0) if "angle" in feat or "raise" in feat or "lean" in feat or "symmetry" in feat else np.random.normal(0, 0.005)
            bad_val = good_val + noise
        if feat in FEATURE_BOUNDS:
            lo, hi = FEATURE_BOUNDS[feat]
            bad_val = np.clip(bad_val, lo, hi)
        bad[feat] = bad_val
    return bad


def passes_outlier_filter(bad_row, good_row):
    """Return True if all feature deltas are within OUTLIER_DELTA."""
    for feat in FEATURE_COLS:
        if abs(bad_row[feat] - good_row[feat]) > OUTLIER_DELTA:
            return False
    return True


def main():
    print("=" * 60)
    print("GENERATING SYNTHETIC BAD-FORM DATA")
    print("=" * 60)

    df = pd.read_csv(INPUT_CSV)
    print(f"\nLoaded {len(df)} rows from {INPUT_CSV}")

    # Extract good-form values from paired_data columns
    good_df = pd.DataFrame()
    for feat in FEATURE_COLS:
        good_df[feat] = df[f"{feat}_good"]
    good_df["pair"]  = df["pair"]
    good_df["frame"] = df["frame"]

    print(f"Good-form frames available: {len(good_df)}")
    print(f"Variants per frame: {VARIANTS_PER_FRAME}")
    print(f"Outlier filter: delta > {OUTLIER_DELTA}° removed\n")

    rows = []
    filtered = 0

    for _, good_row in good_df.iterrows():
        chosen = np.random.choice(len(LATERAL_RAISE_MISTAKES), size=VARIANTS_PER_FRAME, replace=True)
        for mistake_idx in chosen:
            template = LATERAL_RAISE_MISTAKES[mistake_idx]
            bad_features = apply_perturbation(good_row, template)

            if not passes_outlier_filter(bad_features, good_row):
                filtered += 1
                continue

            row = {
                "pair":    good_row["pair"],
                "frame":   good_row["frame"],
                "variant": template["name"],
            }
            for feat in FEATURE_COLS:
                row[f"{feat}_bad"]  = bad_features[feat]
                row[f"{feat}_good"] = good_row[feat]

            rows.append(row)

    synthetic_df = pd.DataFrame(rows)
    synthetic_df.to_csv(OUTPUT_CSV, index=False)

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Generated:      {len(rows)} synthetic pairs")
    print(f"  Filtered out:   {filtered} pairs (delta > {OUTLIER_DELTA}°)")
    print(f"  Variant distribution:")
    for variant, count in synthetic_df["variant"].value_counts().items():
        print(f"    {variant}: {count}")
    print(f"\nSaved to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
