import pandas as pd

# Dataset path
file_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Data\product_description.csv"

# Read dataset
df = pd.read_csv(file_path)

print("\n===== DATASET INFORMATION =====")

# Number of rows and columns
print("\nDataset Shape:")
print(df.shape)

# Column names
print("\nColumn Names:")
print(df.columns.tolist())

# First 5 rows
print("\nFirst 5 Rows:")
print(df.head())

# Data types
print("\nData Types:")
print(df.dtypes)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())