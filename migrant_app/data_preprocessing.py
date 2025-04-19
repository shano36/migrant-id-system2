import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Identify non-numeric columns (e.g., 'Date', 'State')
    non_numeric_cols = df.select_dtypes(include=['object']).columns.tolist()

    # You may want to exclude 'Date' and 'State' columns from the features
    features = df.drop(columns=['Estimated_Migrant_Workers', 'Date', 'State'])

    # Fill missing values only for numeric columns
    features.fillna(features.median(numeric_only=True), inplace=True)

    # Scale the numeric features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    X = pd.DataFrame(scaled_features, columns=features.columns)
    y = df['Estimated_Migrant_Workers']

    return X, y, scaler
