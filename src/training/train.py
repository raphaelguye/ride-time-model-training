import pandas as pd
import xgboost as xgb
import mlflow
import mlflow.xgboost
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split

def train_model(data_path):
    print(f"Loading data from {data_path}...")
    data = pd.read_csv(data_path)

    print("Preparing features and target variable...")
    # Drop non-numeric columns and end_hour if present
    non_feature_cols = ['duration_minutes', 'start_location', 'date', 'end_hour']
    X = data.drop(columns=[col for col in non_feature_cols if col in data.columns])
    y = data['duration_minutes']

    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Initializing XGBoost model...")
    model = xgb.XGBRegressor(objective='reg:squarederror')

    print("Starting MLflow run...")
    mlflow.start_run()

    print("Training the model...")
    model.fit(X_train, y_train)

    print("Making predictions on the test set...")
    predictions = model.predict(X_test)

    print("Calculating evaluation metrics...")
    rmse = root_mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"RMSE: {rmse:.2f}, R2: {r2:.3f}")
    print("Logging metrics to MLflow...")
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)

    print("Saving the model to MLflow...")
    mlflow.xgboost.log_model(model, "model")

    print("Ending MLflow run.")
    mlflow.end_run()

if __name__ == "__main__":
    train_model('data/processed/ride_data.csv')