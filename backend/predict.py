import os
import json
import numpy as np
import tensorflow as tf
from backend.preprocess import preprocess_image

MODEL_DIR = "models"

# -------------------------------------------------
# DISEASE → CATEGORY MAP (FROM DATASET)
# -------------------------------------------------
DISEASE_CATEGORY_MAP = {
    # --- COTTON ---
    "healthy": "Healthy",
    "leaf curl": "Viral",
    "bacterial_blight in cotton": "Bacterial",
    "anthracnose on cotton": "Fungal",
    "bollrot on cotton": "Fungal",
    "wilt": "Fungal",
    "american bollworm on cotton": "Insect - Chewing",
    "bollworm on cotton": "Insect - Chewing",
    "pink bollworm in cotton": "Insect - Chewing",
    "army worm": "Insect - Chewing",
    "cotton aphid": "Insect - Sucking",
    "cotton mealy bug": "Insect - Sucking",
    "cotton whitefly": "Insect - Sucking",
    "thrips on cotton": "Insect - Sucking",
    "red cotton bug": "Insect - Sucking",

    # --- MAIZE ---
    "common_rust": "Fungal",
    "gray leaf spot": "Fungal",
    "maize ear rot": "Fungal",
    "maize fall armyworm": "Insect - Chewing",
    "maize stem borer": "Insect - Chewing",

    # --- RICE ---
    "bacterial blight in rice": "Bacterial",
    "brownspot": "Fungal",
    "rice blast": "Fungal",
    "tungro": "Viral",

    # --- SUGARCANE ---
    "mosaic sugarcane": "Viral",
    "redrot sugarcane": "Fungal",
    "redrust sugarcane": "Fungal",
    "yellow rust sugarcane": "Fungal",

    # --- WHEAT ---
    "flag smut": "Fungal",
    "leaf smut": "Fungal",
    "wheat black rust": "Fungal",
    "wheat brown leaf rust": "Fungal",
    "wheat_yellow_rust": "Fungal",
    "wheat leaf blight": "Fungal",
    "wheat powdery mildew": "Fungal",
    "wheat scab": "Fungal",
    "wheat aphid": "Insect - Sucking",
    "wheat stem fly": "Insect - Chewing",
    "wheat mite": "Mite"
}

# -------------------------------------------------
def load_model_and_classes(crop):
    crop = crop.lower()
    model = tf.keras.models.load_model(
        os.path.join(MODEL_DIR, f"{crop}_model.h5")
    )
    with open(os.path.join(MODEL_DIR, f"{crop}_classes.json")) as f:
        classes = json.load(f)
    return model, classes


# -------------------------------------------------
def predict_disease(image_path, crop):
    model, classes = load_model_and_classes(crop)

    img = preprocess_image(image_path)
    preds = model.predict(img)[0]

    idx = int(np.argmax(preds))
    confidence = float(preds[idx]) * 100
    label = classes[idx]
    label_lower = label.lower()

    is_healthy = label_lower == "healthy"

    # Severity
    if is_healthy:
        severity = "Low"
    elif confidence >= 80:
        severity = "High"
    elif confidence >= 50:
        severity = "Medium"
    else:
        severity = "Low"

    # Category (NO UNKNOWN NOW)
    category = DISEASE_CATEGORY_MAP.get(label_lower, "Fungal")

    explanation = (
        "The leaf shows no disease symptoms."
        if is_healthy else
        f"The model detected visual patterns corresponding to {label}."
    )

    return {
        "crop": crop.capitalize(),
        "status": "Healthy" if is_healthy else "Diseased",
        "disease": "None" if is_healthy else label,
        "confidence": round(confidence, 2),
        "severity": severity,
        "category": category,
        "explanation": explanation
    }