import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# List of Indian states (in your specified order)
indian_states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

# Column names as per your dataset
columns = [
    "Date", "State", "Estimated_Migrant_Workers", "GSDP_per", "Avg_Wage", "Unemploy",
    "Corn_Yield", "Rice_Yield", "Wheat_Yield", "T2M", "RH2M", "WS2M",
    "PRECTOTCORR", "ALLSKY_SFC_SW_DWN", "PS", "Population"
]

# Generate list of dates from 2025-01 to 2030-12
start_date = datetime.strptime("2025-01", "%Y-%m")
end_date = datetime.strptime("2030-12", "%Y-%m")
dates = []
current = start_date
while current <= end_date:
    dates.append(current.strftime("%Y-%m"))
    current += relativedelta(months=1)

# Create DataFrame
data = []

for state in indian_states:
    for date in dates:
        data.append([date, state] + [None] * (len(columns) - 2))  # Fill rest with empty

# Convert to DataFrame and save to CSV
df = pd.DataFrame(data, columns=columns)
df.to_csv("future_forecast_template_all_states.csv", index=False)

print("✅ File 'future_forecast_template_all_states.csv' generated with all states and months.")
