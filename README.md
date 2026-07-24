# 🌱 Crop Disease Detection and Soil-Based Crop Recommendation System

## 📌 Project Overview

The Crop Disease Detection and Soil-Based Crop Recommendation System is an AI-powered web application that detects diseases in crop leaves using a Convolutional Neural Network (CNN) and recommends suitable crops based on soil parameters. The system helps farmers identify plant diseases early, improve crop management, and make informed agricultural decisions.

---

## 🚀 Features

- 🌿 CNN-based crop disease detection using leaf images
- 🌱 Soil-based crop recommendation using NPK, pH, and moisture values
- ⚡ FastAPI backend for prediction APIs
- 📷 Image upload and disease prediction
- 📊 Disease confidence score prediction
- 🌦️ Weather integration using OpenWeatherMap API
- 💡 Disease treatment and preventive recommendations
- 📱 User-friendly interface

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI

### AI / Machine Learning
- TensorFlow
- Keras
- CNN (MobileNetV2)
- NumPy
- OpenCV

### Database
- PostgreSQL

### APIs
- OpenWeatherMap API

---

## 📂 Project Structure

```
Crop-Disease-Detection/
│
├── backend/
│   ├── app.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── frontend/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/crop-disease-detection.git
```

### 2. Navigate to the project

```bash
cd crop-disease-detection
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI server

```bash
uvicorn backend.app:app --reload
```

### 5. Open the application

```
http://127.0.0.1:8000
```

---

## 🌾 Soil Parameters Used

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- pH Value
- Moisture

---

## 🌿 Supported Crops

- Rice
- Wheat
- Cotton
- Maize
- Sugarcane

---

## 📈 Future Enhancements

- IoT sensor integration
- Mobile application support
- Fertilizer recommendation
- Pest detection
- Multilingual support
- Farmer dashboard with analytics

---

## ⚠️ Note

The trained deep learning model (`.h5`) is **not included** in this repository because it exceeds GitHub's file size limit.

To run the project:

- Place your trained model inside the `backend/models/` directory.
- Update the model path in the configuration if required.

---

## 📄 License

This project is developed for educational and research purposes.
