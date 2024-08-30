import pandas as pd

# Read the Parquet file
df = pd.read_parquet('data/2022-01-01.parquet')

# Display the first few rows of the dataframe
print(df.head())

# Print the columns
columns = df.columns
print(columns)
