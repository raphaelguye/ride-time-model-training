# Ride Time Model Training

## Overview
The Ride Time Model Training project aims to develop a machine learning model that predicts the duration of cycling routes based on historical ride data and enriched weather features. The model will be trained using past ride data in GPX or FIT format, along with corresponding weather data.

## Project Structure
```
RideTimeModelTraining
├── data
│   ├── raw                # Contains raw historical ride data files (.gpx/.fit)
│   └── processed
│       └── features.csv   # Processed feature matrix ready for model training
├── models
│   └── model.pkl          # Serialized XGBoost model after training
├── src
│   ├── ingestion
│   │   └── parse_gpx.py   # Code to parse GPX files and extract ride metadata
│   ├── weather
│   │   └── fetch_weather.py # Fetches historical weather data for rides
│   ├── features
│   │   └── build_features.py # Transforms raw ride and weather data into features
│   └── training
│       └── train.py        # Handles training of the regression model
├── tracking
│   └── mlflow              # Directory for tracking parameters, metrics, and artifacts
├── spec
│   └── training.yaml        # Project specifications including purpose, goals, and requirements
├── requirements.txt         # Lists required Python packages and their versions
└── README.md                # Documentation for the project
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd RideTimeModelTraining
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Prepare your raw ride data files in the `data/raw` directory.

4. Run the ingestion and processing scripts to prepare the feature matrix:
   ```
   python src/ingestion/parse_gpx.py
   python src/weather/fetch_weather.py
   python src/features/build_features.py
   ```

5. Train the model:
   ```
   python src/training/train.py
   ```

## Usage
After training, the model will be saved as `models/model.pkl`, and training metrics will be logged in the `tracking/mlflow` directory. You can use the trained model for predictions on new ride data.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you would like to add.

## License
This project is licensed under the MIT License. See the LICENSE file for details.