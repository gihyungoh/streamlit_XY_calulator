import math
import streamlit as st
import numpy as np


def calc_all_interpolated(A, B, H):
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


def draw_ellipse_streamlit(X2, Y2):
    theta = np.linspace(0, 2 * np.pi, 200)
    x = X2 * np.cos(theta)
    y = Y2 * np.sin(theta)

    chart_data = {
        "x": x,
        "y": y
    }

    st.line_chart(chart_data, x="x", y="y", use_container_width=True)


st.title("📐 계산기")

A = st.number_input("A 값", min_value=0.1, value=1.0)
B = st.number_input("B 값", min_value=0.1, value=2.0)
H = st.number_input("H 값", min_value=0.2, max_value=1.2, value=0.3, step=0.1)

if st.button("계산"):
    X2, Y2, X, Y = calc_all_interpolated(A, B, H)

    st.write(f"X2: {X2:.3f}")
    st.write(f"Y2: {Y2:.3f}")
    st.write(f"X: {X:.3f}")
    st.write(f"Y: {Y:.3f}")

    st.subheader("🟢 타원")
    draw_ellipse_streamlit(X2, Y2)
