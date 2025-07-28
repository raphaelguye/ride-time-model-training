# Ride Time Model Training

## Overview
The Ride Time Model Training project aims to develop a machine learning model that predicts the duration of cycling routes based on historical ride data and enriched weather features. The model will be trained using past ride data in GPX or FIT format, along with corresponding weather data.

## Project Structure
```
RideTimeModelTraining
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


4. Run the ingestion script to prepare the ride data:
   ```
   cd RideTimeModelTraining
   source venv/bin/activate && python -m src.ingestion.parse_gpx
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