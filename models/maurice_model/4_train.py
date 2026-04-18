import pandas as pd
import numpy as np
import os
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from tensorflow import keras
from keras import layers, Sequential, Input, optimizers
from keras.callbacks import EarlyStopping

import pickle
import json

PREPROCESS_DIR = Path(__file__).parent.parent.parent / "preprocessing"

FEATURE_LIST = [
    "left_arm_raise",
    "right_arm_raise",
    "left_elbow_angle",
    "right_elbow_angle",
    "torso_lean",
    "arm_symmetry",
    "left_wrist_above_shoulder",
    "right_wrist_above_shoulder",
]

# ── Load data ─────────────────────────────────────────────────────────────────
real      = pd.read_csv(str(PREPROCESS_DIR / "paired_data.csv"))
synthetic = pd.read_csv(str(PREPROCESS_DIR / "synthetic_paired_data.csv"))

# Apply outlier filter to real data
for feat in FEATURE_LIST:
    real = real[abs(real[f"{feat}_bad"] - real[f"{feat}_good"]) < 40]

# Identity pairs from real good-form columns (teaches model not to over-correct)
identity_rows = []
for _, row in real.iterrows():
    r = {}
    for feat in FEATURE_LIST:
        r[f"{feat}_bad"]  = row[f"{feat}_good"]
        r[f"{feat}_good"] = row[f"{feat}_good"]
    identity_rows.append(r)
identity_df = pd.DataFrame(identity_rows)

feature_cols = [f"{feat}_bad"  for feat in FEATURE_LIST] + \
               [f"{feat}_good" for feat in FEATURE_LIST]

combined = pd.concat(
    [real[feature_cols], synthetic[feature_cols], identity_df[feature_cols]],
    ignore_index=True
)

print(f"Real:      {len(real)}")
print(f"Synthetic: {len(synthetic)}")
print(f"Identity:  {len(identity_df)}")
print(f"Combined:  {len(combined)}")

# ── Prepare X / y ─────────────────────────────────────────────────────────────
bad_cols  = [f"{feat}_bad"  for feat in FEATURE_LIST]
good_cols = [f"{feat}_good" for feat in FEATURE_LIST]

X = combined[bad_cols].values
y = combined[good_cols].values

# ── Split ─────────────────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Scale ─────────────────────────────────────────────────────────────────────
X_scaler = StandardScaler()
y_scaler = StandardScaler()

X_train_scaled = X_scaler.fit_transform(X_train)
X_test_scaled  = X_scaler.transform(X_test)
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled  = y_scaler.transform(y_test)

# ── Model ─────────────────────────────────────────────────────────────────────
model = Sequential([
    Input(shape=(len(FEATURE_LIST),)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.15),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.15),
    layers.Dense(32, activation='relu'),
    layers.Dense(len(FEATURE_LIST), activation='linear')
])

model.compile(
    loss='mse',
    optimizer=optimizers.Adam(learning_rate=1e-3),
    metrics=['mae']
)

model.summary()

es = EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)

history = model.fit(
    X_train_scaled, y_train_scaled,
    validation_data=(X_test_scaled, y_test_scaled),
    epochs=300,
    batch_size=32,
    callbacks=[es],
    verbose=1
)

# ── Evaluate ──────────────────────────────────────────────────────────────────
y_pred_scaled = model.predict(X_test_scaled)
y_pred_real   = y_scaler.inverse_transform(y_pred_scaled)
y_test_real   = y_scaler.inverse_transform(y_test_scaled)

abs_errors = np.abs(y_test_real - y_pred_real)

print("\n" + "="*60)
print("EVALUATION RESULTS")
print("="*60)

# Overall
print(f"\nOverall MAE:             {np.mean(abs_errors):.2f}°")
print(f"Mean max error/sample:   {np.mean(np.max(abs_errors, axis=1)):.2f}°")
print(f"Worst sample max error:  {np.max(abs_errors):.2f}°")

# Per-feature MAE
print("\nPer-feature MAE:")
for i, feat in enumerate(FEATURE_LIST):
    print(f"  {feat:<35} {np.mean(abs_errors[:, i]):.2f}°")

# Worst sample
worst_idx     = np.argmax(np.max(abs_errors, axis=1))
worst_feature = np.argmax(abs_errors[worst_idx])
print(f"\nWorst sample index:  {worst_idx}")
print(f"Worst feature:       {FEATURE_LIST[worst_feature]}")
print(f"Predicted:           {y_pred_real[worst_idx][worst_feature]:.2f}°")
print(f"Actual:              {y_test_real[worst_idx][worst_feature]:.2f}°")
print(f"Error:               {abs_errors[worst_idx][worst_feature]:.2f}°")

# ── Save ──────────────────────────────────────────────────────────────────────
os.makedirs("saved_models", exist_ok=True)

model.save("saved_models/lateral_raise_supervised.keras")

with open("saved_models/lateral_raise_X_scaler.pkl", "wb") as f:
    pickle.dump(X_scaler, f)

with open("saved_models/lateral_raise_y_scaler.pkl", "wb") as f:
    pickle.dump(y_scaler, f)

meta = {
    "exercise":        "lateral raise",
    "prediction_type": "absolute",
    "input_features":  bad_cols,
    "output_features": good_cols,
    "input_dim":       len(FEATURE_LIST),
    "output_dim":      len(FEATURE_LIST),
    "training_samples": len(combined),
    "real_samples":     len(real),
    "synthetic_samples": len(synthetic),
    "identity_samples": len(identity_df),
}

with open("saved_models/lateral_raise_meta.json", "w") as f:
    json.dump(meta, f, indent=2)

print("\nSaved to saved_models/")
print("  lateral_raise_supervised.keras")
print("  lateral_raise_X_scaler.pkl")
print("  lateral_raise_y_scaler.pkl")
print("  lateral_raise_meta.json")

#======================================================================
# Metric            v1 (451 samples)    v1 best (current)   v2 target
#----------------------------------------------------------------------
# MAE               5.90°               2.96°               < 2.5°
# Mean Max Error    17.27°              9.59°               < 8°
# Worst Max Error   45.16°              44.67°              < 30°
#======================================================================
