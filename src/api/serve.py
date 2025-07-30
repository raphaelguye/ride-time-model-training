
import os
import mlflow.pyfunc
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class RideFeatures(BaseModel):
    distance_km: float
    elevation_gain: float
    start_hour: int
    weekday: int
    temperature: float
    wind_speed: float
    rain: bool

app = FastAPI(title="Ride Duration Prediction API")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Load model from a path using MODEL_ID from .env
MODEL_ID = os.getenv("MODEL_ID")
if not MODEL_ID:
    raise RuntimeError("MODEL_ID not set in .env file")
model_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "mlruns", "0", "models", MODEL_ID, "artifacts"
)
model = mlflow.pyfunc.load_model(model_path)

@app.post("/predict")
def predict(features: RideFeatures):
    input_df = features.model_dump()
    # MLflow expects a DataFrame
    import pandas as pd
    df = pd.DataFrame([input_df])
    prediction = model.predict(df)
    return {"duration_minutes": float(prediction[0])}
