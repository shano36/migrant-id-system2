from data_preprocessing import preprocess_data
from XGBmodel import train_xgboost, evaluate_model
from predict_future import predict_future_data
from sklearn.model_selection import train_test_split
import pandas as pd

def main():
    # Step 1: Preprocess historical data
    print("📦 Preprocessing historical data...")
    X, y, scaler = preprocess_data('merged_migration_data.csv')

    # Step 2: Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Step 3: Train the XGBoost model
    print("🚀 Training XGBoost model...")
    model, y_pred = train_xgboost(X_train, y_train, X_test, y_test)

    # Step 4: Evaluate model performance
    print("📊 Evaluating model...")
    rmse, r2 = evaluate_model(y_test, y_pred)
    print(f"✅ RMSE: {rmse:.2f}")
    print(f"✅ R² Score: {r2:.4f}")

    # Step 5: Predict migration for future forecasted data
    print("🔮 Predicting future migration data...")
    future_predictions = predict_future_data(model, scaler, 'future_forecast.csv')

    # Step 6: Save the results
    output_path = 'future_predictions.csv'
    future_predictions.to_csv(output_path, index=False)
    print(f"📁 Predictions saved to: {output_path}")
    print(future_predictions.head())

if __name__ == "__main__":
    main()
