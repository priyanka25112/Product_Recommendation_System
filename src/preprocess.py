import pandas as pd

# Dataset path
file_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Data\product_description.csv"

# Load dataset
df = pd.read_csv(file_path)

print("Original dataset shape:", df.shape)

# -------------------------------------------------
# 1. Handle missing values
# -------------------------------------------------

df["Brand"] = df["Brand"].fillna("Unknown")

# -------------------------------------------------
# 2. Remove duplicate products
# -------------------------------------------------

df = df.drop_duplicates(subset=["ID"])

# -------------------------------------------------
# 3. Convert important text columns to string
# -------------------------------------------------

text_columns = [
    "Title",
    "Description",
    "Category",
    "Tags",
    "Brand"
]

for column in text_columns:
    df[column] = df[column].astype(str)

# -------------------------------------------------
# 4. Create combined text feature
# -------------------------------------------------

df["CombinedFeatures"] = (
    df["Title"] + " " +
    df["Description"] + " " +
    df["Category"] + " " +
    df["Tags"] + " " +
    df["Brand"]
)

# -------------------------------------------------
# 5. Save cleaned dataset
# -------------------------------------------------

output_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Data\cleaned_products.csv"

df.to_csv(output_path, index=False)

print("\nData cleaning completed successfully!")

print("Cleaned dataset shape:", df.shape)

print("\nMissing values in important columns:")

print(
    df[
        [
            "Title",
            "Description",
            "Category",
            "Tags",
            "Brand"
        ]
    ].isnull().sum()
)

print("\nCleaned dataset saved to:")
print(output_path)