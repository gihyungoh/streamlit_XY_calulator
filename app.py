import math
import streamlit as st
import numpy as np
import plotly.graph_objects as go


def calc_all_interpolated(A, B, H):
    A, B = sorted([A, B])

    k = math.sqrt(2.8 / math.pi)
    X2 = k * A   # 단축 반지름
    Y2 = k * B   # 장축 반지름

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


def draw_ellipse_plotly(X2, Y2):
    theta = np.linspace(0, 2 * np.pi, 400)
    x = X2 * np.cos(theta)
    y = Y2 * np.sin(theta)

    fig = go.Figure()

    # ✅ 타원
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        name="Ellipse"
    ))

    # ✅ 단축 (X 방향)
    fig.add_trace(go.Scatter(
        x=[-X2, X2], y=[0, 0],
        mode="lines+markers",
        name=f"단축 = {2*X2:.3f}",
        line=dict(dash="dash")
    ))

    # ✅ 장축 (Y 방향)
    fig.add_trace(go.Scatter(
        x=[0, 0], y=[-Y2, Y2],
        mode="lines+markers",
        name=f"장축 = {2*Y2:.3f}",
        line=dict(dash="dash")
    ))

    max_r = max(X2, Y2) * 1.2

    fig.update_layout(
        title="타원 (X/Y 스케일 동일)",
        xaxis=dict(
            scaleanchor="y",
            range=[-max_r, max_r],
            zeroline=True
        ),
        yaxis=dict(
            range=[-max_r, max_r],
            zeroline=True
        ),
        width=500,
        height=500,
        showlegend=True
    )

    return fig


# ================= Streamlit UI =================

st.title("📐 계산기")

A = st.number_input("A 값", min_value=0.1, value=1.0)
B = st.number_input("B 값", min_value=0.1, value=2.0)
H = st.number_input("H 값", min_value=0.2, max_value=1.2, value=0.3, step=0.1)

if st.button("계산"):
    X2, Y2, X, Y = calc_all_interpolated(A, B, H)

    st.subheader("📊 계산 결과")
    st.write(f"단축 반지름 X2: {X2:.3f}")
    st.write(f"장축 반지름 Y2: {Y2:.3f}")
    st.write(f"단축 길이: {2*X2:.3f}")
    st.write(f"장축 길이: {2*Y2:.3f}")
    st.write(f"X: {X:.3f}")
    st.write(f"Y: {Y:.3f}")

    st.subheader("🟢 타원 시각화")
    fig = draw_ellipse_plotly(X2, Y2)
    st.plotly_chart(fig, use_container_width=True)
