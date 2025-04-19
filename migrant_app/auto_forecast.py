import pandas as pd
from prophet import Prophet
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

# ✅ List of Indian states
indian_states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# ✅ Features to forecast
features_to_forecast = [
    'GSDP_per_capita_Lakhs', 'Avg_Wage', 'Unemployment_Rate_%',
    'Corn_Yield_kg_per_ha', 'Rice_Yield_kg_per_ha', 'Wheat_Yield_kg_per_ha',
    'T2M', 'RH2M', 'WS2M', 'PRECTOTCORR', 'ALLSKY_SFC_SW_DWN', 'PS', 'Population'
]

# ✅ Load dataset
df = pd.read_csv('merged_migration_data.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
df = df.sort_values('Date')

# ✅ Forecasting function
def forecast_feature(state_df, feature, months=72):
    ts = state_df[['Date', feature]].rename(columns={'Date': 'ds', feature: 'y'}).dropna()
    if len(ts) < 24:
        return None
    model = Prophet()
    model.fit(ts)
    future = model.make_future_dataframe(periods=months, freq='MS')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].rename(columns={'yhat': feature})

# ✅ Main loop
all_forecasts = []

for state in tqdm(indian_states, desc="📊 Forecasting for each state"):
    state_df = df[df['State'] == state].copy()
    if state_df.empty:
        print(f"⚠️ No data for {state}")
        continue

    state_df['Date'] = pd.to_datetime(state_df['Date'])
    merged_forecast = None

    for feature in features_to_forecast:
        fcast = forecast_feature(state_df, feature)
        if fcast is None:
            print(f"⚠️ Skipping {feature} for {state}")
            continue
        if merged_forecast is None:
            merged_forecast = fcast
        else:
            merged_forecast = merged_forecast.merge(fcast, on='ds')

    if merged_forecast is None:
        continue

    # Add constant/mocked value for Estimated_Migrant_Workers (or you can predict it separately)
    merged_forecast['Estimated_Migrant_Workers'] = 0  # Placeholder

    merged_forecast['State'] = state
    merged_forecast['Date'] = merged_forecast['ds'].dt.strftime('%Y-%m')
    
    # Reorder to final format
    ordered_cols = ['Date', 'State', 'Estimated_Migrant_Workers'] + features_to_forecast
    merged_forecast = merged_forecast[ordered_cols]

    # Filter only future predictions
    merged_forecast = merged_forecast[merged_forecast['Date'] >= '2025-01']
    all_forecasts.append(merged_forecast)

# ✅ Final save
result_df = pd.concat(all_forecasts, ignore_index=True)
result_df.to_csv('future_forecast.csv', index=False)
print("✅ Forecast saved as 'forecast_formatted.csv'")
