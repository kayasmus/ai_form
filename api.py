from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import numpy as np
import cv2
import pickle
import json
import tensorflow as tf
import mediapipe as mp
from pathlib import Path
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MODELS_DIR = Path(__file__).parent / "models/maurice_model/saved_models"

model = tf.keras.models.load_model(str(MODELS_DIR / "lateral_raise_savedmodel"), compile=False)
with open(MODELS_DIR / "lateral_raise_X_scaler.pkl", "rb") as f:
    X_scaler = pickle.load(f)
with open(MODELS_DIR / "lateral_raise_y_scaler.pkl", "rb") as f:
    y_scaler = pickle.load(f)
with open(MODELS_DIR / "lateral_raise_meta.json") as f:
    meta = json.load(f)

mp_pose = mp.solutions.pose
LM = mp_pose.PoseLandmark
pose = mp_pose.Pose(static_image_mode=True, model_complexity=1,
                    min_detection_confidence=0.5)

FEATURE_LIST = [
    "left_arm_raise", "right_arm_raise",
    "left_elbow_angle", "right_elbow_angle",
    "torso_lean", "arm_symmetry",
    "left_wrist_above_shoulder", "right_wrist_above_shoulder",
]

def get_coords(landmarks, lm_enum):
    lm = landmarks[lm_enum.value]
    return np.array([lm.x, lm.y, lm.z])

def angle_between(a, b, c):
    ba, bc = a - b, c - b
    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    return np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))

def midpoint(a, b):
    return (a + b) / 2.0

def extract_features(landmarks):
    ls = get_coords(landmarks, LM.LEFT_SHOULDER)
    rs = get_coords(landmarks, LM.RIGHT_SHOULDER)
    le = get_coords(landmarks, LM.LEFT_ELBOW)
    re = get_coords(landmarks, LM.RIGHT_ELBOW)
    lw = get_coords(landmarks, LM.LEFT_WRIST)
    rw = get_coords(landmarks, LM.RIGHT_WRIST)
    lh = get_coords(landmarks, LM.LEFT_HIP)
    rh = get_coords(landmarks, LM.RIGHT_HIP)
    mid_s = midpoint(ls, rs)
    mid_h = midpoint(lh, rh)
    spine = mid_s - mid_h
    vertical = np.array([0, -1, 0])
    cosine = np.dot(spine, vertical) / (np.linalg.norm(spine) + 1e-6)
    lr = angle_between(lh, ls, le)
    rr = angle_between(rh, rs, re)
    return {
        "left_arm_raise": lr, "right_arm_raise": rr,
        "left_elbow_angle": angle_between(ls, le, lw),
        "right_elbow_angle": angle_between(rs, re, rw),
        "torso_lean": np.degrees(np.arccos(np.clip(cosine, -1, 1))),
        "arm_symmetry": abs(lr - rr),
        "left_wrist_above_shoulder": float(ls[1] - lw[1]),
        "right_wrist_above_shoulder": float(rs[1] - rw[1]),
    }

def get_fault(features, prediction):
    ideal = dict(zip(FEATURE_LIST, prediction))
    avg_raise = (features["left_arm_raise"] + features["right_arm_raise"]) / 2
    ideal_raise = (ideal["left_arm_raise"] + ideal["right_arm_raise"]) / 2
    avg_elbow = (features["left_elbow_angle"] + features["right_elbow_angle"]) / 2
    ideal_elbow = (ideal["left_elbow_angle"] + ideal["right_elbow_angle"]) / 2
    faults = []
    if ideal_raise - avg_raise > 15: faults.append((ideal_raise - avg_raise, "Raise arms higher"))
    if avg_raise - ideal_raise > 8:  faults.append((avg_raise - ideal_raise, "Arms too high"))
    if ideal_elbow - avg_elbow > 20: faults.append((ideal_elbow - avg_elbow, "Bend elbows less"))
    if features["torso_lean"] - ideal["torso_lean"] > 10: faults.append((10, "Stop swinging"))
    if features["arm_symmetry"] - ideal["arm_symmetry"] > 15: faults.append((15, "Even out your arms"))
    if not faults: return "Good form!"
    faults.sort(reverse=True)
    return faults[0][1]

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    frame = np.array(img)
    result = pose.process(frame)
    if not result.pose_landmarks:
        return {"detected": False, "score": 0, "fault": "No pose detected"}
    landmarks = result.pose_landmarks.landmark
    features = extract_features(landmarks)
    avg_raise = (features["left_arm_raise"] + features["right_arm_raise"]) / 2
    if avg_raise < 30:
        return {"detected": True, "score": 100, "fault": ""}
    vec = np.array([[features[f] for f in FEATURE_LIST]], dtype=np.float32)
    pred_scaled = model.predict(X_scaler.transform(vec), verbose=0)
    prediction = y_scaler.inverse_transform(pred_scaled)[0]
    errors = np.abs(np.array([features[f] for f in FEATURE_LIST]) - prediction)
    score = max(0.0, 100.0 * (1.0 - float(np.mean(errors)) / 30.0))
    fault = get_fault(features, prediction)
    return {"detected": True, "score": round(score, 1), "fault": fault}

@app.get("/", response_class=HTMLResponse)
async def index():
    return open(Path(__file__).parent / "index.html").read()
