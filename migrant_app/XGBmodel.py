# tuned_xgboost.py
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

def train_xgboost(X_train, y_train, X_test, y_test):
    print("🎯 Running hyperparameter tuning...")

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }

    xgb = XGBRegressor(objective='reg:squarederror', random_state=42)
    grid = GridSearchCV(estimator=xgb, param_grid=param_grid,
                        cv=3, scoring='neg_root_mean_squared_error', verbose=1, n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    print(f"✅ Best parameters: {grid.best_params_}")

    y_pred = best_model.predict(X_test)
    return best_model, y_pred

def evaluate_model(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return rmse, r2
