import streamlit as st
import requests

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="Product Recommendation System",
    page_icon="🛍️",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================
st.title("🛍️ Product Recommendation System")
st.write("Enter a Product ID to discover similar products.")

st.divider()

# ==========================================================
# BENTOML API
# ==========================================================
API_URL = "http://localhost:3000/recommend"

# ==========================================================
# PRODUCT ID INPUT
# ==========================================================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    product_id = st.number_input(
        "🔢 Enter Product ID",
        min_value=1,
        step=1,
        value=1
    )

    get_recommendations = st.button(
        "🔍 Get Recommendations",
        use_container_width=True
    )

# ==========================================================
# GET RECOMMENDATIONS
# ==========================================================
if get_recommendations:

    payload = {
        "product_id": int(product_id)
    }

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=30
        )

        # ==================================================
        # SUCCESS
        # ==================================================
        if response.status_code == 200:

            result = response.json()

            st.success("✅ Recommendations found!")

            st.subheader("✨ Recommended Products")

            # ==================================================
            # GET RECOMMENDATIONS
            # ==================================================
            if isinstance(result, dict):

                if "recommendations" in result:
                    recommendations = result["recommendations"]
                else:
                    recommendations = [result]

            elif isinstance(result, list):

                recommendations = result

            else:

                recommendations = [result]

            # ==================================================
            # DISPLAY PRODUCTS
            # ==================================================
            if isinstance(recommendations, list):

                if len(recommendations) == 0:

                    st.warning("No recommendations found.")

                else:

                    for i, product in enumerate(
                        recommendations,
                        start=1
                    ):

                        st.divider()

                        st.write(
                            f"### 🛍️ Recommendation #{i}"
                        )

                        # ==========================================
                        # DICTIONARY PRODUCT
                        # ==========================================
                        if isinstance(product, dict):

                            product_name = (
                                product.get("product_name")
                                or product.get("name")
                                or product.get("title")
                                or "Recommended Product"
                            )

                            product_id_value = (
                                product.get("product_id")
                                if product.get("product_id") is not None
                                else product.get("id", "N/A")
                            )

                            category = (
                                product.get("category")
                                or product.get("product_category")
                                or "Product"
                            )

                            price = product.get("price")

                            similarity = (
                                product.get("similarity")
                                if product.get("similarity") is not None
                                else product.get("similarity_score")
                            )

                            if similarity is None:
                                similarity = product.get("score")

                            # ==========================================
                            # SIMILARITY SCORE
                            # ==========================================
                            if similarity is not None:

                                try:

                                    score = float(similarity)

                                    if 0 <= score <= 1:
                                        score = score * 100

                                    score_text = f"{score:.1f}%"

                                except:
                                    score_text = str(similarity)

                            else:

                                score_text = "N/A"

                            # ==========================================
                            # PRODUCT INFORMATION
                            # ==========================================
                            c1, c2, c3, c4 = st.columns(4)

                            with c1:
                                st.write("**Product**")
                                st.write(f"🛍️ {product_name}")

                            with c2:
                                st.write("**Product ID**")
                                st.write(product_id_value)

                            with c3:
                                st.write("**Category**")
                                st.write(category)

                            with c4:
                                st.write("**Price**")

                                if price is not None:
                                    st.write(f"₹{price}")
                                else:
                                    st.write("Not available")

                            st.metric(
                                "⭐ Similarity Score",
                                score_text
                            )

                        # ==========================================
                        # STRING PRODUCT
                        # ==========================================
                        else:

                            st.write(f"🛍️ {product}")

            # ==================================================
            # NON-LIST RESULT
            # ==================================================
            else:

                st.write(recommendations)

        # ==================================================
        # API ERROR
        # ==================================================
        else:

            st.error(
                f"❌ API Error: {response.status_code}"
            )

            st.code(response.text)

    # ======================================================
    # CONNECTION ERROR
    # ======================================================
    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to BentoML server."
        )

        st.info(
            "Make sure BentoML is running at "
            "http://localhost:3000"
        )

    # ======================================================
    # TIMEOUT
    # ======================================================
    except requests.exceptions.Timeout:

        st.error(
            "⏱️ Request timed out."
        )

    # ======================================================
    # OTHER ERROR
    # ======================================================
    except Exception as e:

        st.error(
            f"❌ Unexpected error: {str(e)}"
        )