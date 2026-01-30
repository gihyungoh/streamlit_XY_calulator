import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


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


def draw_ellipse(X2, Y2):
    theta = np.linspace(0, 2 * np.pi, 400)
    x = X2 * np.cos(theta)
    y = Y2 * np.sin(theta)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x, y, label="Ellipse")
    ax.axhline(0, color="gray", linewidth=0.5)
    ax.axvline(0, color="gray", linewidth=0.5)

    ax.set_aspect("equal")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("X2-단축 / Y2-장축 타원")
    ax.legend()
    ax.grid(True)

    return fig


st.set_page_config(page_title="계산기", layout="centered")
st.title("📐 계산기 (H = 0.2 ~ 1.2)")

A_input = st.number_input("A 값", min_value=0.0, value=1.0)
B_input = st.number_input("B 값", min_value=0.0, value=2.0)
H = st.number_input("H 값", min_value=0.2, max_value=1.2, value=0.3, step=0.1)

A, B = sorted([A_input, B_input])
st.caption(f"✅ 내부 계산값 → A = {A}, B = {B}")

if st.button("계산"):
    X2, Y2, X, Y = calc_all_interpolated(A_input, B_input, H)

    st.subheader("📊 계산 결과")
    st.write(f"X2 (단축 반지름): {X2:.3f}")
    st.write(f"Y2 (장축 반지름): {Y2:.3f}")
    st.write(f"X: {X:.3f}")
    st.write(f"Y: {Y:.3f}")

    if X2 > 0 and Y2 > 0:
        st.subheader("🟢 타원 시각화")
        fig = draw_ellipse(X2, Y2)
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.warning("A, B 값이 0보다 커야 타원을 그릴 수 있습니다.")
