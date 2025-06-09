import streamlit as st
from models.black_scholes import (
    black_scholes_call, black_scholes_put,
    black_scholes_greeks_call, black_scholes_greeks_put
)
from models.binomial import (
    binomial_call, binomial_put,
    binomial_greeks_call, binomial_greeks_put
)
from models.monte_carlo import (
    monte_carlo_call, monte_carlo_put,
    monte_carlo_greeks_call, monte_carlo_greeks_put
)

st.set_page_config(page_title="OPUS", layout="centered")
st.title("Option Pricing & Uncertainty Sensitivities")

tab1, tab2, tab3 = st.tabs(["Black-Scholes", "Binomial Tree", "Monte Carlo"])

# ------------- BLACK-SCHOLES ----------------
with tab1:
    st.header("Black-Scholes Model")
    with st.form("bs_form"):
        S = st.number_input("Spot Price (S)", value=100.0)
        K = st.number_input("Strike Price (K)", value=100.0)
        T = st.number_input("Time to Maturity (T, years)", value=1.0)
        r = st.number_input("Risk-Free Rate (r, %)", value=2.0) / 100
        sigma = st.number_input("Volatility (σ, %)", value=20.0) / 100
        opt_type = st.selectbox("Option Type", ["Call", "Put"])
        submitted = st.form_submit_button("Calculate")

    if submitted:
        if opt_type == "Call":
            price = black_scholes_call(S, K, T, r, sigma)
            greeks = black_scholes_greeks_call(S, K, T, r, sigma)
        else:
            price = black_scholes_put(S, K, T, r, sigma)
            greeks = black_scholes_greeks_put(S, K, T, r, sigma)

        st.success(f"{opt_type} Option Price: ${price:.2f}")
        st.subheader("Formula")
        st.latex(r"""
        C = S \cdot N(d_1) - K e^{-rT} \cdot N(d_2)
        """)
        st.latex(fr"""
        d_1 = \frac{{\ln(\frac{{{S}}}{{{K}}}) + ({r} + \frac{{{sigma}^2}}{2}) {T}}}{{{sigma} \sqrt{{{T}}}}}, \quad
        d_2 = d_1 - {sigma} \sqrt{{{T}}}
        """)
        st.subheader("Greeks")
        st.markdown(f"""
        - Δ (Delta): {greeks['delta']:.4f}  
        - Γ (Gamma): {greeks['gamma']:.6f}  
        - Θ (Theta, per year): {greeks['theta']:.4f}  
        - 𝜈 (Vega): {greeks['vega']:.4f}  
        - ρ (Rho): {greeks['rho']:.4f}
        """)

# ------------- BINOMIAL ----------------
with tab2:
    st.header("Binomial Tree Model")
    with st.form("binomial_form"):
        S = st.number_input("Spot Price", value=100.0, key="b1")
        K = st.number_input("Strike Price", value=100.0, key="b2")
        T = st.number_input("Time to Maturity (T, years)", value=1.0, key="b3")
        r = st.number_input("Risk-Free Rate (%)", value=2.0, key="b4") / 100
        sigma = st.number_input("Volatility (%)", value=20.0, key="b5") / 100
        steps = st.number_input("Steps", value=100, min_value=1, step=1)
        exercise = st.selectbox("Exercise Type", ["European", "American"])
        opt_type = st.selectbox("Option Type", ["Call", "Put"], key="btype")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        if opt_type == "Call":
            price = binomial_call(S, K, T, r, sigma, steps, option_type=exercise)
            greeks = binomial_greeks_call(S, K, T, r, sigma, steps, option_type=exercise)
        else:
            price = binomial_put(S, K, T, r, sigma, steps, option_type=exercise)
            greeks = binomial_greeks_put(S, K, T, r, sigma, steps, option_type=exercise)

        st.success(f"{exercise} {opt_type} Option Price: ${price:.2f}")
        st.subheader("Greeks")
        st.markdown(f"""
        - Δ (Delta): {greeks['delta']:.4f}  
        - Γ (Gamma): {greeks['gamma']:.6f}  
        - Θ (Theta, per step): {greeks['theta']:.4f}  
        - 𝜈 (Vega): {greeks['vega']:.4f}  
        - ρ (Rho): {greeks['rho']:.4f}
        """)

# ------------- MONTE CARLO ----------------
with tab3:
    st.header("Monte Carlo Simulation")
    S = st.number_input("Spot Price", value=100.0, key="m1")
    K = st.number_input("Strike Price", value=100.0, key="m2")
    T = st.number_input("Time to Maturity (years)", value=1.0, key="m3")
    r = st.number_input("Risk-Free Rate (%)", value=2.0, key="m4") / 100
    sigma = st.number_input("Volatility (%)", value=20.0, key="m5") / 100
    steps = st.slider("Steps (for Asian)", 10, 500, 100)
    sims = st.slider("Simulations", 1000, 50000, 10000, step=1000)
    opt_type = st.selectbox("Option Type", ["Call", "Put"], key="mopt")
    style = st.selectbox("Style", ["European", "Asian"])

    if st.button("Calculate Monte Carlo Price"):
        if style == "European":
            price = monte_carlo_call(S, K, T, r, sigma, sims) if opt_type == "Call" else monte_carlo_put(S, K, T, r, sigma, sims)
        else:
            price = monte_carlo_call(S, K, T, r, sigma, sims, steps=steps, option_type="Asian") if opt_type == "Call" else monte_carlo_put(S, K, T, r, sigma, sims, steps=steps, option_type="Asian")

        st.success(f"{style} {opt_type} Option Price: ${price:.2f}")

        st.subheader("Formula")
        if style == "European":
            st.latex(r"""
                C = e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]
            """ if opt_type == "Call" else r"""
                P = e^{-rT} \cdot \mathbb{E}[\max(K - S_T, 0)]
            """)
        else:
            st.latex(r"""
                C = e^{-rT} \cdot \mathbb{E}\left[\max\left(\frac{1}{n} \sum_{i=1}^n S_{t_i} - K, 0\right)\right]
            """ if opt_type == "Call" else r"""
                P = e^{-rT} \cdot \mathbb{E}\left[\max\left(K - \frac{1}{n} \sum_{i=1}^n S_{t_i}, 0\right)\right]
            """)

        # Greeks only for European
        if style == "European":
            if opt_type == "Call":
                greeks = monte_carlo_greeks_call(S, K, T, r, sigma, sims)
            else:
                greeks = monte_carlo_greeks_put(S, K, T, r, sigma, sims)

            st.subheader("Greeks")
            st.markdown(f"""
            - Δ (Delta): {greeks['delta']:.4f}  
            - Γ (Gamma): {greeks['gamma']:.6f}  
            - Θ (Theta): {greeks['theta']:.4f}  
            - 𝜈 (Vega): {greeks['vega']:.4f}  
            - ρ (Rho): {greeks['rho']:.4f}
            """)
