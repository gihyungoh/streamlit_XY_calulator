import streamlit as st

# -----------------------------
# Piecewise function
# -----------------------------
def calc_XY_piecewise(A, B, z):
    if z < 0.8:
        X = 0.30 + 0.50*A + 0.48*B - 0.20*z
        Y = 0.60 + 0.45*A + 0.50*B + 0.40*z
        zone = "z < 0.8"
    elif z < 1.2:
        X = 0.42 + 0.48*A + 0.47*B - 0.31*z
        Y = 0.55 + 0.47*A + 0.48*B + 0.31*z
        zone = "0.8 ≤ z < 1.2"
    else:
        X = 0.55 + 0.46*A + 0.45*B - 0.42*z
        Y = 0.50 + 0.48*A + 0.46*B + 0.42*z
        zone = "z ≥ 1.2"

    return X, Y, zone


# -----------------------------
# Streamlit GUI
# -----------------------------
st.set_page_config(page_title="X, Y Calculator", layout="centered")

st.title("🧮 X, Y 계산기")
st.write("A, B, z 값을 입력하면 X, Y를 계산합니다.")

# Input layout
col1, col2, col3 = st.columns(3)

with col1:
    A = st.number_input("A 값", value=1.0, step=0.1, format="%.3f")
with col2:
    B = st.number_input("B 값", value=1.0, step=0.1, format="%.3f")
with col3:
    z = st.number_input("z 값", value=1.0, step=0.1, format="%.3f")

st.markdown("---")

# Button
if st.button("✅ 계산하기", use_container_width=True):
    X, Y, zone = calc_XY_piecewise(A, B, z)

    st.success(f"적용된 구간: **{zone}**")

    colX, colY = st.columns(2)
    colX.metric("X 값", f"{X:.4f}")
    colY.metric("Y 값", f"{Y:.4f}")

# Footer
st.markdown("---")
st.caption("Streamlit GUI · Streamlit Cloud 실행 가능")
