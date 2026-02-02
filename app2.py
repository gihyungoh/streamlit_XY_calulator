# ============================================
# Streamlit GUI for Ellipse Auto Fitting
# ============================================

import streamlit as st
import numpy as np
import pandas as pd
import math
from scipy.optimize import least_squares

# ============================================
# Page config
# ============================================
st.set_page_config(
    page_title="Ellipse Auto Fitting",
    layout="centered"
)

st.title("🔵 Ellipse Auto Fitting Tool")
st.caption("Ellipse area = 70% of rectangle area")

# ============================================
# Constant (area constraint)
# ============================================
k = math.sqrt(2.8 / math.pi)

# ============================================
# Model
# ============================================
def model(params, A, B, r):
    a0,a1,b0,b1,c0,c1, \
    d0,d1,e0,e1,f0,f1 = params

    X = k * ((a0 + a1*r) * A + (b0 + b1*r) * B) + (c0 + c1*r)
    Y = k * ((d0 + d1*r) * A + (e0 + e1*r) * B) + (f0 + f1*r)

    return X, Y

def residuals(params, A, B, r, X_meas, Y_meas):
    X_pred, Y_pred = model(params, A, B, r)

    res_X = X_pred - X_meas
    res_Y = Y_pred - Y_meas

    # enforce X <= Y
    penalty = np.maximum(0.0, X_pred - Y_pred)

    return np.concatenate([res_X, res_Y, 10.0 * penalty])

# ============================================
# Fit function
# ============================================
def fit_model(df):
    A = df["A"].values
    B = df["B"].values
    r = df["r"].values
    X_meas = df["X_meas"].values
    Y_meas = df["Y_meas"].values

    p0 = np.zeros(12)

    result = least_squares(
        residuals,
        p0,
        args=(A, B, r, X_meas, Y_meas),
        loss="soft_l1"
    )

    return result.x, result

# ============================================
# Sidebar - Data upload & fitting
# ============================================
st.sidebar.header("📂 Training Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("CSV loaded successfully")

elif st.sidebar.button("Use sample data"):
    df = pd.DataFrame({
        "A": [10, 8, 12, 9],
        "B": [12, 10, 15, 11],
        "r": [4.0, 2.5, 5.0, 3.0],
        "X_meas": [6.21, 5.10, 7.20, 5.80],
        "Y_meas": [9.83, 7.60, 11.40, 8.90],
    })
    st.sidebar.success("Sample data loaded")

else:
    df = None

# ============================================
# Fitting
# ============================================
if df is not None:
    st.subheader("📊 Training Data")
    st.dataframe(df)

    if st.button("🚀 Run Auto Fitting"):
        with st.spinner("Fitting model..."):
            params, result = fit_model(df)

        st.success("Fitting completed!")

        st.session_state["params"] = params

        st.subheader("✅ Fitted Parameters")
        st.code(
            "\n".join(
                [f"{n} = {v:.6f}" for n, v in zip(
                    ["a0","a1","b0","b1","c0","c1",
                     "d0","d1","e0","e1","f0","f1"],
                    params
                )]
            )
        )

        st.write("Cost:", result.cost)

# ============================================
# Prediction GUI
# ============================================
st.subheader("🎯 Prediction")

if "params" not in st.session_state:
    st.info("먼저 CSV를 업로드하고 Auto Fitting을 실행하세요.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        A_in = st.number_input("A", value=10.0)
    with col2:
        B_in = st.number_input("B", value=12.0)
    with col3:
        r_in = st.number_input("Compression ratio (r)", value=4.0)

    if st.button("📐 Predict Ellipse Size"):
        X_out, Y_out = model(st.session_state["params"], A_in, B_in, r_in)

        st.success("Prediction completed ✅")

        c1, c2 = st.columns(2)
        with c1:
            st.metric("X (minor axis)", f"{X_out:.4f}")
        with c2:
            st.metric("Y (major axis)", f"{Y_out:.4f}")

        area_ratio = (math.pi / 4) * X_out * Y_out / (A_in * B_in)
        st.caption(f"Ellipse / Rectangle Area Ratio = {area_ratio:.3f}")

# ============================================
# Footer
# ============================================
st.markdown("---")
st.caption("© Ellipse Auto Fitting – Streamlit App")
