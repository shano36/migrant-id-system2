import pandas as pd

# Load all datasets into pandas DataFrames
migration_df = pd.read_csv('migration_data.csv')
economic_df = pd.read_csv('economic_data.csv')
agriculture_df = pd.read_csv('agriculture_data.csv')
climate_df = pd.read_csv('climate_data.csv')
population_df = pd.read_csv('population_data.csv')

# Merge all datasets on 'State' and 'Date' columns
merged_df = pd.merge(migration_df, economic_df, on=['State', 'Date'], how='inner')
merged_df = pd.merge(merged_df, agriculture_df, on=['State', 'Date'], how='inner')
merged_df = pd.merge(merged_df, climate_df, on=['State', 'Date'], how='inner')
merged_df = pd.merge(merged_df, population_df, on=['State', 'Date'], how='inner')

# Display the first few rows of the merged dataset
print(merged_df.head())

# Optionally, save the merged dataset to a new CSV file
merged_df.to_csv('merged_migration_data.csv', index=False)
