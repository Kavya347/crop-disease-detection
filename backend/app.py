import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.predict import predict_disease
from backend.recommendation import recommend_action
from backend.weather import get_weather   # ✅ added

app = FastAPI()

# ----------------------
# Paths
# ----------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

templates = Jinja2Templates(directory="frontend/templates")

# ----------------------
# Static files
# ----------------------
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# ----------------------
# Routes
# ----------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict-ui", response_class=HTMLResponse)
async def predict_ui(
    request: Request,
    crop: str = Form(...),
    ph: float = Form(...),
    npk: str = Form(...),
    moisture: float = Form(...),
    image: UploadFile = File(...)
):
    # ----------------------
    # Save image
    # ----------------------
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    # ----------------------
    # ML Prediction
    # ----------------------
    result = predict_disease(image_path, crop)

    # ----------------------
    # Soil data
    # ----------------------
    soil = {
        "ph": ph,
        "npk": npk,
        "moisture": moisture
    }

    # ----------------------
    # 🌦 Live Weather (NO DEFAULT VALUES)
    # ----------------------
    weather_data = get_weather("Bangalore")
    weather = {
        "temp": f"{weather_data['temperature']}°C",
        "humidity": f"{weather_data['humidity']}%",
        "rain": f"{weather_data['rain_chance']}%"
    }

    # ----------------------
    # Recommendation
    # ----------------------
    rec_raw = recommend_action(result, soil)

    if isinstance(rec_raw, str):
        recommendation = {
            "soil_condition": "Normal",
            "treatment": rec_raw,
            "fertilizer": "Organic manure",
            "next_crop": "Maize, Wheat"
        }
    else:
        recommendation = {
            "soil_condition": rec_raw.get("soil_condition", "Normal"),
            "treatment": rec_raw.get("treatment", "Follow standard treatment"),
            "fertilizer": rec_raw.get("fertilizer", "Organic manure"),
            "next_crop": rec_raw.get("next_crop_recommendation", "Maize")
        }

    # ----------------------
    # Render Dashboard
    # ----------------------
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,

            # Prediction
            "crop": result["crop"],
            "disease": result["disease"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "category": result.get("category", "Unknown"),
            "explanation": result.get("explanation", "Leaf symptoms detected"),

            # Image
            "image_url": f"/uploads/{image.filename}",

            # Soil & Weather
            "soil": soil,
            "weather": weather,

            # Recommendation
            "recommendation": recommendation
        }
    )