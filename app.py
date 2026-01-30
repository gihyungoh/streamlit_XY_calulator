import math
import streamlit as st


def calc_all_interpolated(A, B, H):
    # ✅ A < B 자동 보정
    A, B = sorted([A, B])

    k = math.sqrt(2.8 / math.pi)
    X2 = k * A
    Y2 = k * B

    H_list = [0.3, 0.5, 0.7, 0.9, 1.1]
    coeffs = {
        0.3: (0.66, -0.95, 0.78,  0.15),
        0.5: (0.64, -0.70, 0.76,  0.05),
        0.7: (0.61, -0.45, 0.74, -0.05),
        0.9: (0.58, -0.20, 0.72, -0.15),
        1.1: (0.55,  0.05, 0.70, -0.25),
    }

    if H < 0.2 or H > 1.2:
        raise ValueError("H는 0.2 ~ 1.2 범위 내여야 합니다.")

    if H <= 0.3:
        a, b, c, d = coeffs[0.3]
    elif H >= 1.1:
        a, b, c, d = coeffs[1.1]
    else:
        for i in range(len(H_list) - 1):
            H1, H2 = H_list[i], H_list[i + 1]
            if H1 <= H <= H2:
                t = (H - H1) / (H2 - H1)
                a1, b1, c1, d1 = coeffs[H1]
                a2, b2, c2, d2 = coeffs[H2]

                a = a1 + t * (a2 - a1)
                b = b1 + t * (b2 - b1)
                c = c1 + t * (c2 - c1)
                d = d1 + t * (d2 - d1)
                break

    X = a * X2 + b
    Y = c * Y2 + d

    return X2, Y2, X, Y


st.set_page_config(page_title="계산기", layout="centered")
st.title("📐 계산기 (H = 0.2 ~ 1.2)")

A_input = st.number_input("PKG 가로", value=0.0)
B_input = st.number_input("PKG 세로", value=0.0)
H = st.number_input("PKG & CASE Gap", min_value=0.2, max_value=1.2, value=0.3, step=0.1)

if st.button("계산"):
    X2, Y2, X, Y = calc_all_interpolated(A_input, B_input, H)
    st.write(f"X2: {X2:.3f}")
    st.write(f"Y2: {Y2:.3f}")
    st.write(f"X: {X:.3f}")
    st.write(f"Y: {Y:.3f}")
