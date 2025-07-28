import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def train_model(data_path):
    # Load the processed feature dataset
    data = pd.read_csv(data_path)

    # Define features and target variable
    X = data.drop(columns=['duration_minutes'])
    y = data['duration_minutes']

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the XGBoost model
    model = xgb.XGBRegressor(objective='reg:squarederror')

    # Start MLflow tracking
    mlflow.start_run()

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Calculate metrics
    rmse = mean_squared_error(y_test, predictions, squared=False)
    r2 = r2_score(y_test, predictions)

    # Log metrics to MLflow
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    # Save the model
    mlflow.xgboost.log_model(model, "model")

    # End MLflow run
    mlflow.end_run()

if __name__ == "__main__":
    train_model('data/processed/features.csv')