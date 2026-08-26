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

st.markdown(
    """
    <style>

    /* =====================================================
       GENERAL
       ===================================================== */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    h1 {
        font-size: 42px;
        font-weight: 800;
    }


    /* =====================================================
       RECOMMENDATION TITLE
       ===================================================== */

    .recommendation-title {
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
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
        font-size: 18px;
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
    """,
    unsafe_allow_html=True
)


# ==========================================================
# TITLE
# ==========================================================

st.title(
    "🛍️ Product Recommendation System"
)

st.write(
    "Enter a Product ID to discover similar products."
)

st.divider()


# ==========================================================
# BENTOML API
# ==========================================================

API_URL = (
    "https://product-recommendation-system-z1xn.onrender.com"
    "/recommend"
)


# ==========================================================
# PRODUCT ID INPUT
# ==========================================================

col1, col2, col3 = st.columns(
    [1, 2, 1]
)

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
        "product_id": int(product_id),
        "top_n": 5
    }

    try:

        # ==================================================
        # SEND REQUEST TO BENTOML
        # ==================================================

        response = requests.post(
            API_URL,
            json=payload,
            timeout=60
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
                                width=350
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
                        # CREATE COLUMNS
                        # ==========================================

                        columns = st.columns(
                            len(row),
                            gap="medium"
                        )


                        # ==========================================
                        # DISPLAY PRODUCTS
                        # ==========================================

                        for index, (
                            column,
                            product
                        ) in enumerate(
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


                                brand = product.get(
                                    "brand",
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
                                # PRODUCT CARD
                                # ==================================

                                with st.container(
                                    border=True
                                ):

                                    # ==============================
                                    # RECOMMENDATION NUMBER
                                    # ==============================

                                    st.markdown(
                                        f"### 🛍️ Recommendation #{index}"
                                    )


                                    # ==============================
                                    # PRODUCT IMAGE
                                    # ==============================

                                    if image:

                                        st.image(
                                            image,
                                            width=180
                                        )

                                    else:

                                        st.info(
                                            "Image unavailable"
                                        )


                                    # ==============================
                                    # PRODUCT TITLE
                                    # ==============================

                                    st.markdown(
                                        f"**{title}**"
                                    )


                                    # ==============================
                                    # PRODUCT ID
                                    # ==============================

                                    st.write(
                                        f"🆔 Product ID: "
                                        f"{product_id_value}"
                                    )


                                    

                                    # ==============================
                                    # CATEGORY
                                    # ==============================

                                    st.write(
                                        f"📂 Category: "
                                        f"{category}"
                                    )


                                    # ==============================
                                    # PRICE
                                    # ==============================

                                    st.markdown(
                                        f"### ₹{price}"
                                    )


                                    # ==============================
                                    # SIMILARITY SCORE
                                    # ==============================

                                    if score is not None:

                                        try:

                                            score_percentage = (
                                                float(score) * 100
                                            )


                                            st.write(
                                                "⭐ Similarity Score"
                                            )


                                            st.write(
                                                f"**{score_percentage:.1f}%**"
                                            )


                                            # ==========================
                                            # SCORE PROGRESS
                                            # ==========================

                                            st.progress(
                                                min(
                                                    max(
                                                        score_percentage
                                                        / 100,
                                                        0
                                                    ),
                                                    1
                                                )
                                            )


                                        except (
                                            ValueError,
                                            TypeError
                                        ):

                                            st.write(
                                                "Similarity: N/A"
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
                f"❌ API Error: "
                f"{response.status_code}"
            )


            st.code(
                response.text
            )


    # ======================================================
    # CONNECTION ERROR
    # ======================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to the "
            "recommendation service. "
            "Please try again in a few seconds."
        )


    # ======================================================
    # TIMEOUT ERROR
    # ======================================================

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Request timed out. "
            "The recommendation service may be "
            "starting up. Please try again."
        )


    # ======================================================
    # OTHER ERROR
    # ======================================================

    except Exception as e:

        st.error(
            f"❌ Error: {e}"
        )