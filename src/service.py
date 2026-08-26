import os
import pickle
import requests
import bentoml

from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. LOAD MODEL
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(
    BASE_DIR,
    "Models",
    "tfidf_model.pkl"
)

with open(model_path, "rb") as file:
    model = pickle.load(file)

df = model["data"]
tfidf_matrix = model["tfidf_matrix"]


# ============================================================
# 2. CALCULATE COSINE SIMILARITY
# ============================================================

similarity_matrix = cosine_similarity(tfidf_matrix)

print("Model loaded successfully!")


# ============================================================
# 3. GET PRODUCT IMAGE
# ============================================================

def get_product_image(product_id):

    try:

        response = requests.get(
            f"https://dummyjson.com/products/{product_id}",
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            if data.get("thumbnail"):
                return data["thumbnail"]

            images = data.get("images", [])

            if images:
                return images[0]

    except Exception as e:

        print(
            f"Image fetch failed for product {product_id}: {e}"
        )

    return None


# ============================================================
# 4. BENTOML SERVICE
# ============================================================

@bentoml.service(
    name="product_recommendation_service"
)
class ProductRecommendationService:

    @bentoml.api
    def recommend(
        self,
        product_id: int,
        top_n: int = 5
    ):

        # ----------------------------------------------------
        # Find product
        # ----------------------------------------------------

        product_index = df.index[
            df["ID"] == product_id
        ].tolist()

        if not product_index:

            return {
                "error": "Product ID not found"
            }

        product_index = product_index[0]

        selected_product = df.iloc[product_index]

        selected_category = str(
            selected_product["Category"]
        ).strip().lower()

        # ----------------------------------------------------
        # Calculate similarity
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Same category filtering
        # ----------------------------------------------------

        recommendations = []

        for index, score in similarity_scores:

            category = str(
                df.iloc[index]["Category"]
            ).strip().lower()

            if category == selected_category:

                if score > 0:

                    recommendations.append(
                        (index, score)
                    )

        # ----------------------------------------------------
        # Sort by similarity
        # ----------------------------------------------------

        recommendations = sorted(
            recommendations,
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = recommendations[:top_n]

        # ----------------------------------------------------
        # Create result
        # ----------------------------------------------------

        result = {

            "selected_product": {

                "id": int(
                    selected_product["ID"]
                ),

                "title": str(
                    selected_product["Title"]
                ),

                "category": str(
                    selected_product["Category"]
                ),

                "brand": str(
                    selected_product["Brand"]
                ),

                "price": float(
                    selected_product["Price"]
                ),

                "image": get_product_image(
                    int(selected_product["ID"])
                )
            },

            "recommendations": []
        }

        # ----------------------------------------------------
        # Add recommendations
        # ----------------------------------------------------

        for index, score in recommendations:

            product = df.iloc[index]

            product_id_value = int(
                product["ID"]
            )

            result["recommendations"].append(

                {

                    "id": product_id_value,

                    "title": str(
                        product["Title"]
                    ),

                    "category": str(
                        product["Category"]
                    ),

                    "brand": str(
                        product["Brand"]
                    ),

                    "price": float(
                        product["Price"]
                    ),

                    "similarity_score": round(
                        float(score),
                        3
                    ),

                    "image": get_product_image(
                        product_id_value
                    )
                }
            )

        return result
    