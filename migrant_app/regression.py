import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("merged_migration_data.csv")

# Features and Target
features = [
    'GSDP_per_capita_Lakhs', 'Avg_Wage', 'Unemployment_Rate_%',
    'Corn_Yield_kg_per_ha', 'Rice_Yield_kg_per_ha', 'Wheat_Yield_kg_per_ha',
    'T2M', 'RH2M', 'WS2M', 'PRECTOTCORR', 'ALLSKY_SFC_SW_DWN', 'PS',
    'Population'
]
target = 'Estimated_Migrant_Workers'

X = df[features]
y = df[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Function to evaluate model
def evaluate_model(y_true, y_pred):
    return {
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "MAE": mean_absolute_error(y_true, y_pred),
        "R2 Score": r2_score(y_true, y_pred)
    }

# Hyperparameter tuning for Random Forest
rf_param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

rf_model = RandomForestRegressor(random_state=42)
rf_grid_search = GridSearchCV(estimator=rf_model, param_grid=rf_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
rf_grid_search.fit(X_train, y_train)

# Best Random Forest Model
rf_best_model = rf_grid_search.best_estimator_

# Hyperparameter tuning for XGBoost
xgb_param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb_model = XGBRegressor(random_state=42)
xgb_grid_search = GridSearchCV(estimator=xgb_model, param_grid=xgb_param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
xgb_grid_search.fit(X_train, y_train)

# Best XGBoost Model
xgb_best_model = xgb_grid_search.best_estimator_

# Train and predict with the best models
rf_preds = rf_best_model.predict(X_test)
xgb_preds = xgb_best_model.predict(X_test)

# Evaluate models
print("Random Forest (Tuned):", evaluate_model(y_test, rf_preds))
print("XGBoost (Tuned):", evaluate_model(y_test, xgb_preds))

# Feature importance for Random Forest
rf_importances = rf_best_model.feature_importances_
rf_indices = np.argsort(rf_importances)[::-1]
rf_sorted_features = np.array(features)[rf_indices]

# Feature importance for XGBoost
xgb_importances = xgb_best_model.feature_importances_
xgb_indices = np.argsort(xgb_importances)[::-1]
xgb_sorted_features = np.array(features)[xgb_indices]

# Plot feature importance for Random Forest
plt.figure(figsize=(10, 6))
sns.barplot(x=rf_importances[rf_indices], y=rf_sorted_features)
plt.title("Random Forest Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.show()

# Plot feature importance for XGBoost
plt.figure(figsize=(10, 6))
sns.barplot(x=xgb_importances[xgb_indices], y=xgb_sorted_features)
plt.title("XGBoost Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.show()

# Cross-validation scores
rf_cv_score = cross_val_score(rf_best_model, X, y, cv=5, scoring='neg_mean_squared_error')
xgb_cv_score = cross_val_score(xgb_best_model, X, y, cv=5, scoring='neg_mean_squared_error')

print(f"Random Forest CV Score (neg MSE): {np.mean(rf_cv_score)}")
print(f"XGBoost CV Score (neg MSE): {np.mean(xgb_cv_score)}")