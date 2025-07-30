import os
import mlflow.pyfunc
from fastapi import FastAPI
from pydantic import BaseModel

class RideFeatures(BaseModel):
    distance_km: float
    elevation_gain: float
    start_hour: int
    end_hour: int
    weekday: int
    temperature: float
    wind_speed: float
    rain: bool

app = FastAPI(title="Ride Duration Prediction API")

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Load model from a hardcoded path
model_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "mlruns", "0", "models", "m-9d791e1c965f4306ae867c99415328ac", "artifacts"
)
# load the model from model_path
model = mlflow.pyfunc.load_model(model_path)

@app.post("/predict")
def predict(features: RideFeatures):
    input_df = features.model_dump()
    # MLflow expects a DataFrame
    import pandas as pd
    df = pd.DataFrame([input_df])
    prediction = model.predict(df)
    return {"duration_minutes": float(prediction[0])}
