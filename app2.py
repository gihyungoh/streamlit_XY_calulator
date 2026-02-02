import streamlit as st

st.set_page_config(page_title="Ellipse Regression Calculator", layout="centered")

st.title("A, B, z 기반 X, Y 계산기")
st.markdown("타원 넓이 = 사각형 넓이의 **70%** 조건 기반 선형회귀 모델")

# =====================
# 입력 UI
# =====================
st.header("입력값")

A = st.number_input("A (사각형 가로 길이)", min_value=0.0, value=10.0, step=0.1)
B = st.number_input("B (사각형 세로 길이)", min_value=0.0, value=10.0, step=0.1)

z = st.selectbox(
    "z 값 선택",
    options=[
        6.666666667,
        4.0,
        2.857142857,
        2.222222222,
        1.818181818
    ]
)

# =====================
# X2, Y2 계산
# =====================
X2 = 0.9446 * A
Y2 = 0.9446 * B

# =====================
# z 구간별 회귀계수
# =====================
def regression_coefficients(z):
    if z == 6.666666667:
        return 0.63, -0.05, 0.12, 0.12, 0.74, 0.18
    elif z == 4.0:
        return 0.61, -0.04, 0.15, 0.14, 0.72, 0.22
    elif z == 2.857142857:
        return 0.59, -0.03, 0.18, 0.16, 0.70, 0.25
    elif z == 2.222222222:
        return 0.57, -0.02, 0.21, 0.18, 0.68, 0.28
    elif z == 1.818181818:
        return 0.55, -0.01, 0.24, 0.20, 0.66, 0.31
    else:
        return None

coeffs = regression_coefficients(z)

# =====================
# 결과 계산
# =====================
if coeffs:
    a, b, c, d, e, f = coeffs
    X = a * A + b * B + c
    Y = d * A + e * B + f

    st.header("계산 결과")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("X2 (타원 가로 지름)", f"{X2:.4f}")
        st.metric("X", f"{X:.4f}")
    with col2:
        st.metric("Y2 (타원 세로 지름)", f"{Y2:.4f}")
        st.metric("Y", f"{Y:.4f}")

# =====================
# 수식 표시
# =====================
with st.expander("사용된 수식 보기"):
    st.latex(r"X2 = 0.9446 \cdot A")
    st.latex(r"Y2 = 0.9446 \cdot B")
    st.markdown("**z 구간별 선형회귀식**")
    st.latex(r"X = \alpha A + \beta B + \gamma")
    st.latex(r"Y = \delta A + \epsilon B + \zeta")
