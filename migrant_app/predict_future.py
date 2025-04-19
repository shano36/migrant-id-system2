import pandas as pd

def predict_future_data(model, scaler, future_data_file):
    # Load the full future forecast CSV
    full_df = pd.read_csv(future_data_file)

    # Keep a copy of metadata columns
    metadata_cols = full_df[['Date', 'State']].copy()

    # Drop non-feature columns before scaling
    features_df = full_df.drop(columns=['Date', 'State', 'Estimated_Migrant_Workers'])

    # Scale only the feature columns
    scaled_features = scaler.transform(features_df)

    # Predict using the trained model
    predictions = model.predict(scaled_features)

    # Combine predictions back with metadata
    full_df['Predicted_Migrant_Workers'] = predictions

    return full_df
