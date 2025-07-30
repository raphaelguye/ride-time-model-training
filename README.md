# Ride Time Model Training

## Overview
The Ride Time Model Training project aims to develop a machine learning model that predicts the duration of cycling routes based on historical ride data and enriched weather features. The model will be trained using past ride data in GPX or FIT format, along with corresponding weather data.

## Project Structure
```
ride-time-model-training
├── data
│   ├── raw                # Contains raw historical ride data files (.gpx/.fit)
│   └── processed
│       └── ride_data.csv  # Processed rides -parsed and sanitized- with weather aggregated
├── models
│   └── model.pkl          # Serialized XGBoost model after training
├── src
│   ├── ingestion
│   │   └── parse_gpx.py   # Code to parse GPX files and extract ride metadata
│   ├── weather
│   │   └── fetch_weather.py # Fetches historical weather data for rides
│   └── training
│       └── train.py        # Handles training of the regression model
├── tracking
│   └── mlflow              # Directory for tracking parameters, metrics, and artifacts
├── requirements.txt         # Lists required Python packages and their versions
└── README.md                # Documentation for the project
```

## Setup Instructions

1. Install the required packages in venv:
   ```
   python3 -m venv venv && source venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Prepare your raw ride data files in the `data/raw` directory.


3. Run the ingestion script to prepare the ride data:
   ```
   source venv/bin/activate && python -m src.ingestion.parse_gpx
   ```

4. Train the model using the processed `ride_data.csv` from the previous step:
   ```
   source venv/bin/activate && python -m src.training.train
   ```
   The trained model and experiment artifacts will be saved in the `mlruns` directory on the root of the project.

   To view experiment runs and model artifacts in your browser, launch the MLflow UI:
   ```
   source venv/bin/activate && python -m mlflow ui
   ```

5. Configure the model to use for prediction:
   
   Create a `.env` file at the project root and fill it witht the model id generated in the previous step in `mlruns/0/models`:
   ```
   MODEL_ID=m-561e797988974a489....
   ```

6. Run the prediction API server:
   ```
   source venv/bin/activate && uvicorn src.api.serve:app --reload
   ```
   The API will be available at http://localhost:8000

   Example: Get a prediction with curl
   ```sh
   curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "distance_km": 40.0,
       "elevation_gain": 500,
       "start_hour": 8,
       "weekday": 2,
       "temperature": 15.5,
       "wind_speed": 5.0,
       "rain": false
     }'
   ```
