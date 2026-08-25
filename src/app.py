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
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

    /* =====================================================
       GENERAL
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* =====================================================
       RECOMMENDATION TITLE
       ===================================================== */

    .recommendation-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
        white-space: nowrap;
    }

    /* =====================================================
       PRODUCT INFORMATION
       ===================================================== */

    .product-info {
        font-size: 13px;
        margin-top: 3px;
    }

    /* =====================================================
       PRICE
       ===================================================== */

    .price {
        font-size: 16px;
        font-weight: 700;
    }

    /* =====================================================
       SIMILARITY SCORE
       ===================================================== */

    .score {
        font-size: 13px;
        font-weight: 600;
    }

    /* =====================================================
       RECOMMENDATION COLUMNS
       ===================================================== */

    div[data-testid="column"] {
        padding-left: 5px;
        padding-right: 5px;
    }

</style>
""", unsafe_allow_html=True)


# ==========================================================
# TITLE
# ==========================================================

st.title("🛍️ Product Recommendation System")

st.write(
    "Enter a Product ID to discover similar products."
)

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

        # ==================================================
        # SEND REQUEST TO BENTOML
        # ==================================================

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


            # ==================================================
            # API RETURNED ERROR
            # ==================================================

            if "error" in result:

                st.error(
                    result["error"]
                )


            else:

                st.success(
                    "✅ Recommendations found!"
                )


                # ==================================================
                # SELECTED PRODUCT
                # ==================================================

                selected = result.get(
                    "selected_product"
                )


                if selected:

                    st.subheader(
                        "🎯 Selected Product"
                    )


                    selected_col1, selected_col2 = st.columns(
                        [1, 2]
                    )


                    # ==========================================
                    # SELECTED PRODUCT IMAGE
                    # ==========================================

                    with selected_col1:

                        image = selected.get(
                            "image"
                        )


                        if image:

                            st.image(
                                image,
                                use_container_width=True
                            )

                        else:

                            st.info(
                                "Image unavailable"
                            )


                    # ==========================================
                    # SELECTED PRODUCT DETAILS
                    # ==========================================

                    with selected_col2:

                        st.markdown(
                            f"## {selected.get('title', 'Product')}"
                        )


                        st.write(
                            f"**Brand:** "
                            f"{selected.get('brand', 'N/A')}"
                        )


                        st.write(
                            f"**Category:** "
                            f"{selected.get('category', 'N/A')}"
                        )


                        st.write(
                            f"**Product ID:** "
                            f"{selected.get('id', 'N/A')}"
                        )


                        st.markdown(
                            f"### ₹{selected.get('price', 'N/A')}"
                        )


                st.divider()


                # ==================================================
                # RECOMMENDATIONS
                # ==================================================

                st.subheader(
                    "✨ Recommended Products"
                )


                recommendations = result.get(
                    "recommendations",
                    []
                )


                # ==================================================
                # NO RECOMMENDATIONS
                # ==================================================

                if not recommendations:

                    st.warning(
                        "No recommendations found."
                    )


                else:

                    # ==================================================
                    # 4 PRODUCTS PER ROW
                    # ==================================================

                    for start in range(
                        0,
                        len(recommendations),
                        4
                    ):

                        row = recommendations[
                            start:start + 4
                        ]


                        # ==========================================
                        # CREATE 4 COLUMNS
                        # ==========================================

                        columns = st.columns(
                            4,
                            gap="small"
                        )


                        # ==========================================
                        # DISPLAY PRODUCTS
                        # ==========================================

                        for index, (column, product) in enumerate(
                            zip(columns, row),
                            start=start + 1
                        ):

                            with column:

                                # ==================================
                                # PRODUCT DATA
                                # ==================================

                                image = product.get(
                                    "image"
                                )


                                title = product.get(
                                    "title",
                                    "Recommended Product"
                                )


                                product_id_value = product.get(
                                    "id",
                                    "N/A"
                                )


                                category = product.get(
                                    "category",
                                    "N/A"
                                )


                                price = product.get(
                                    "price",
                                    "N/A"
                                )


                                score = product.get(
                                    "similarity_score"
                                )


                                # ==================================
                                # RECOMMENDATION NUMBER
                                # ==================================

                                st.markdown(
                                    f"### 🛍️ Recommendation #{index}"
                                )


                                # ==================================
                                # PRODUCT IMAGE
                                # ==================================

                                if image:

                                    st.image(
                                        image,
                                        use_container_width=True
                                    )

                                else:

                                    st.info(
                                        "Image unavailable"
                                    )


                                # ==================================
                                # PRODUCT
                                # ==================================

                                st.markdown(
                                    "**Product**"
                                )


                                st.write(
                                    f"🛍️ {title}"
                                )


                                # ==================================
                                # PRODUCT ID
                                # ==================================

                                st.markdown(
                                    "**Product ID**"
                                )


                                st.code(
                                    str(product_id_value),
                                    language=None
                                )


                                # ==================================
                                # CATEGORY
                                # ==================================

                                st.markdown(
                                    "**Category**"
                                )


                                st.write(
                                    category
                                )


                                # ==================================
                                # PRICE
                                # ==================================

                                st.markdown(
                                    "**Price**"
                                )


                                st.write(
                                    f"₹{price}"
                                )


                                # ==================================
                                # SIMILARITY SCORE
                                # ==================================

                                if score is not None:

                                    try:

                                        score_percentage = (
                                            float(score) * 100
                                        )


                                        st.markdown(
                                            "**⭐ Similarity Score**"
                                        )


                                        st.write(
                                            f"{score_percentage:.1f}%"
                                        )


                                        # --------------------------
                                        # SCORE PROGRESS
                                        # --------------------------

                                        st.progress(
                                            min(
                                                max(
                                                    score_percentage / 100,
                                                    0
                                                ),
                                                1
                                            )
                                        )

                                    except (ValueError, TypeError):

                                        st.write(
                                            "N/A"
                                        )


                        # ==========================================
                        # SPACE BETWEEN ROWS
                        # ==========================================

                        st.markdown(
                            "<br>",
                            unsafe_allow_html=True
                        )


        # ==================================================
        # API ERROR
        # ==================================================

        else:

            st.error(
                f"API Error: {response.status_code}"
            )


            st.code(
                response.text
            )


    # ======================================================
    # CONNECTION ERROR
    # ======================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to BentoML. "
            "Make sure BentoML is running on port 3000."
        )


    # ======================================================
    # TIMEOUT ERROR
    # ======================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out. "
            "Please check whether BentoML is running correctly."
        )


    # ======================================================
    # OTHER ERROR
    # ======================================================

    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )