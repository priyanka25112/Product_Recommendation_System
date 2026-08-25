import pandas as pd
import pickle

from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD TF-IDF MODEL
# ============================================================

model_path = r"C:\Users\priya\Desktop\Product_Recommendation_System\Models\tfidf_model.pkl"

with open(model_path, "rb") as file:
    model = pickle.load(file)

df = model["data"]
tfidf_matrix = model["tfidf_matrix"]


# ============================================================
# 2. CALCULATE COSINE SIMILARITY
# ============================================================

similarity_matrix = cosine_similarity(tfidf_matrix)

print("Cosine similarity calculated successfully!")


# ============================================================
# 3. RECOMMENDATION FUNCTION
# ============================================================

def recommend_products(product_id, top_n=5):

    # Find selected product
    product_index = df.index[
        df["ID"] == product_id
    ].tolist()

    if not product_index:
        print("\nProduct ID not found.")
        return

    product_index = product_index[0]

    # Selected product
    selected_product = df.iloc[product_index]

    selected_title = selected_product["Title"]
    selected_category = selected_product["Category"]

    # ========================================================
    # GET COSINE SIMILARITY SCORES
    # ========================================================

    similarity_scores = list(
        enumerate(
            similarity_matrix[product_index]
        )
    )

    # Remove selected product
    similarity_scores = [
        item
        for item in similarity_scores
        if item[0] != product_index
    ]

    # ========================================================
    # FILTER BY SAME CATEGORY ONLY
    # ========================================================

    same_category_products = []

    for index, score in similarity_scores:

        product_category = df.iloc[index]["Category"]

        if str(product_category).strip().lower() == \
           str(selected_category).strip().lower():

            # Ignore zero similarity
            if score > 0:
                same_category_products.append(
                    (index, score)
                )

    # ========================================================
    # SORT BY SIMILARITY
    # ========================================================

    same_category_products = sorted(
        same_category_products,
        key=lambda x: x[1],
        reverse=True
    )

    # ========================================================
    # DISPLAY SELECTED PRODUCT
    # ========================================================

    print("\n" + "=" * 55)
    print("SELECTED PRODUCT")
    print("=" * 55)

    print(f"Product : {selected_title}")
    print(f"Category: {selected_category}")
    print(f"Brand   : {selected_product['Brand']}")
    print(f"Price   : ${selected_product['Price']}")

    # ========================================================
    # DISPLAY RECOMMENDATIONS
    # ========================================================

    print("\n" + "=" * 55)
    print("RECOMMENDED PRODUCTS")
    print("=" * 55)

    if len(same_category_products) == 0:

        print("\nNo similar products found in the same category.")

    else:

        for number, (index, score) in enumerate(
            same_category_products[:top_n],
            start=1
        ):

            print(
                f"\n{number}. "
                f"{df.iloc[index]['Title']}"
            )

            print(
                f"   Category        : "
                f"{df.iloc[index]['Category']}"
            )

            print(
                f"   Brand           : "
                f"{df.iloc[index]['Brand']}"
            )

            print(
                f"   Price           : "
                f"${df.iloc[index]['Price']}"
            )

            print(
                f"   Similarity Score: "
                f"{score:.3f}"
            )

    print("\n" + "=" * 55)


# ============================================================
# 4. TEST RECOMMENDATION
# ============================================================

if __name__ == "__main__":

    # Select first product
    product_id = int(df.iloc[0]["ID"])

    # Generate recommendations
    recommend_products(
        product_id,
        top_n=5
    )