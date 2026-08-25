import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Load cleaned dataset
file_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Data\cleaned_products.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Number of products:", len(df))

# 2. Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english"
)

# 3. Convert CombinedFeatures into numerical vectors
tfidf_matrix = vectorizer.fit_transform(
    df["CombinedFeatures"]
)

# 4. Display results
print("\nTF-IDF completed successfully!")
print("TF-IDF matrix shape:", tfidf_matrix.shape)
print(
    "Number of features:",
    len(vectorizer.get_feature_names_out())
)

# 5. Save the TF-IDF model
model_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Models\tfidf_model.pkl"

with open(model_path, "wb") as file:
    pickle.dump(
        {
            "vectorizer": vectorizer,
            "tfidf_matrix": tfidf_matrix,
            "data": df
        },
        file
    )

print("\nTF-IDF model saved successfully!")
print("Saved to:")
print(model_path)