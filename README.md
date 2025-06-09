# OPUS – Option Pricing & Uncertainty Sensitivities

OPUS is a modular and interactive [Streamlit](https://streamlit.io)-based application for pricing European, American, and Asian call and put options using **Black-Scholes**, **Binomial Tree**, and **Monte Carlo Simulation** models. It also provides analytical insights into first- and second-order option sensitivities (the **Greeks**).

## Supported Models

| Model         | European | American | Asian | Notes                                 |
|---------------|----------|----------|-------|----------------------------------------|
| Black-Scholes | ✅        | ❌        | ❌     | Closed-form solution for European only |
| Binomial Tree | ✅        | ✅        | ❌     | American via early exercise handling   |
| Monte Carlo   | ✅        | ❌        | ✅     | Suitable for path-dependent options    |

## Features

- **Black-Scholes**: Closed-form pricing and Greeks for European call options  
- **Binomial Tree**: Recombining lattice supporting early exercise for American calls  
- **Monte Carlo**: Supports both European and Asian options via path-averaging  
- **Computed Greeks**:
  - Delta (Δ)  
  - Gamma (Γ)  
  - Theta (Θ)  
  - Vega (𝜈)  
  - Rho (ρ)  
- Real-time LaTeX-rendered formulas  
- Flexible user-defined inputs: spot price, strike, volatility, time to maturity, number of steps, and simulation paths  
- Structured user interface with model separation via Streamlit tab navigation

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/julgas/opus.git
cd opus
pip install -r requirements.txt
streamlit run opus.py
