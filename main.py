from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import psycopg2
import os

# Load Model
MODEL_PATH = "crop_disease_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def home():
    return {"message": "Crop Backend Running with ML Model + PostgreSQL!"}

# Test DB
@app.get("/test-db")
def test_db():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        conn.close()
        return {"status": "Database Connected Successfully"}
    except Exception as e:
        return {"status": "DB Error", "error": str(e)}

# ======================
#   PREDICT API
# ======================
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).resize((128, 128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_id = np.argmax(prediction[0])

    return {"prediction": int(class_id)}


