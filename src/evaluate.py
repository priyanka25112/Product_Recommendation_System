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

def get_recommendations(product_index, top_n=5):

    selected_category = str(
        df.iloc[product_index]["Category"]
    ).strip().lower()

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

    # Same-category products only
    recommendations = [
        item
        for item in similarity_scores
        if str(
            df.iloc[item[0]]["Category"]
        ).strip().lower() == selected_category
    ]

    # Sort by similarity
    recommendations = sorted(
        recommendations,
        key=lambda x: x[1],
        reverse=True
    )

    return recommendations[:top_n]


# ============================================================
# 4. EVALUATION
# ============================================================

def evaluate_system(top_n=5):

    total_products = len(df)

    total_recommendations = 0
    same_category_recommendations = 0

    similarity_scores = []

    # Evaluate a maximum of 100 products
    number_of_products = min(
        total_products,
        100
    )

    print("\n" + "=" * 60)
    print("RECOMMENDATION SYSTEM EVALUATION")
    print("=" * 60)

    for product_index in range(number_of_products):

        recommendations = get_recommendations(
            product_index,
            top_n
        )

        for recommended_index, score in recommendations:

            total_recommendations += 1

            selected_category = str(
                df.iloc[product_index]["Category"]
            ).strip().lower()

            recommended_category = str(
                df.iloc[recommended_index]["Category"]
            ).strip().lower()

            # Check category relevance
            if selected_category == recommended_category:

                same_category_recommendations += 1

            similarity_scores.append(score)

    # ========================================================
    # CATEGORY RELEVANCE
    # ========================================================

    if total_recommendations > 0:

        category_relevance = (
            same_category_recommendations
            / total_recommendations
        ) * 100

    else:

        category_relevance = 0

    # ========================================================
    # AVERAGE SIMILARITY
    # ========================================================

    if similarity_scores:

        average_similarity = sum(
            similarity_scores
        ) / len(similarity_scores)

    else:

        average_similarity = 0

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    print(
        f"\nProducts evaluated       : "
        f"{number_of_products}"
    )

    print(
        f"Recommendations generated: "
        f"{total_recommendations}"
    )

    print(
        f"Category relevance       : "
        f"{category_relevance:.2f}%"
    )

    print(
        f"Average similarity score : "
        f"{average_similarity:.3f}"
    )

    print("\n" + "=" * 60)

    print("EVALUATION COMPLETED")
    print("=" * 60)


# ============================================================
# 5. RUN EVALUATION
# ============================================================

if __name__ == "__main__":

    evaluate_system(
        top_n=5
    )