import numpy as np
"""
     Cox-Ross-Rubinstein Binomial Tree pricing for European options.

    Parameters:
    S     : Spot price
    K     : Strike price
    T     : Time to maturity (in years)
    r     : Risk-free interest rate
    sigma : Volatility
    steps : Number of binomial steps
    option_type: Initially set to 'European'; 'American' selectable

    Returns:
    Option price (Call/Put)
    """
# ====================== BINOMIAL CALL OPTION FUNCTIONS ====================== #
def binomial_call(S, K, T, r, sigma, steps=100, option_type="European"):

    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    ST = np.array([S * (u**j) * (d**(steps - j)) for j in range(steps + 1)])
    option_values = np.maximum(ST - K, 0)

    for i in range(steps - 1, -1, -1):
        ST = ST[:i + 1] / u
        option_values = np.exp(-r * dt) * (p * option_values[1:i + 2] + (1 - p) * option_values[0:i + 1])

        if option_type == "American":
            option_values = np.maximum(option_values, ST - K)

    return option_values[0]

def binomial_greeks_call(S, K, T, r, sigma, steps=100, option_type="European"):
    dS = 0.01 * S
    dT = 1/365  # One day for theta
    dSigma = 0.01
    dR = 0.0001

    base_price = binomial_call(S, K, T, r, sigma, steps, option_type)

    price_up = binomial_call(S + dS, K, T, r, sigma, steps, option_type)
    price_down = binomial_call(S - dS, K, T, r, sigma, steps, option_type)
    delta = (price_up - price_down) / (2 * dS)

    gamma = (price_up - 2 * base_price + price_down) / (dS ** 2)

    T_theta = max(T - dT, 1e-5)
    price_theta = binomial_call(S, K, T_theta, r, sigma, steps, option_type)
    theta = (price_theta - base_price) / dT

    price_vega_up = binomial_call(S, K, T, r, sigma + dSigma, steps, option_type)
    price_vega_down = binomial_call(S, K, T, r, sigma - dSigma, steps, option_type)
    vega = (price_vega_up - price_vega_down) / (2 * dSigma)

    price_rho_up = binomial_call(S, K, T, r + dR, sigma, steps, option_type)
    price_rho_down = binomial_call(S, K, T, r - dR, sigma, steps, option_type)
    rho = (price_rho_up - price_rho_down) / (2 * dR)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }

# ====================== BINOMIAL PUT OPTION FUNCTIONS ======================= #
def binomial_put(S, K, T, r, sigma, steps=100, option_type="European"):
    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    ST = np.array([S * (u**j) * (d**(steps - j)) for j in range(steps + 1)])
    option_values = np.maximum(K - ST, 0)

    for i in range(steps - 1, -1, -1):
        ST = ST[:i + 1] / u
        option_values = np.exp(-r * dt) * (p * option_values[1:i + 2] + (1 - p) * option_values[0:i + 1])

        if option_type == "American":
            option_values = np.maximum(option_values, K - ST)

    return option_values[0]

def binomial_greeks_put(S, K, T, r, sigma, steps=100, option_type="European"):
    dS = 0.01 * S
    dT = 1 / 365 # One day for theta
    dSigma = 0.01
    dR = 0.0001

    base_price = binomial_put(S, K, T, r, sigma, steps, option_type)

    price_up = binomial_put(S + dS, K, T, r, sigma, steps, option_type)
    price_down = binomial_put(S - dS, K, T, r, sigma, steps, option_type)
    delta = (price_up - price_down) / (2 * dS)
    gamma = (price_up - 2 * base_price + price_down) / (dS ** 2)

    T_theta = max(T - dT, 1e-5)
    price_theta = binomial_put(S, K, T_theta, r, sigma, steps, option_type)
    theta = (price_theta - base_price) / dT

    price_vega_up = binomial_put(S, K, T, r, sigma + dSigma, steps, option_type)
    price_vega_down = binomial_put(S, K, T, r, sigma - dSigma, steps, option_type)
    vega = (price_vega_up - price_vega_down) / (2 * dSigma)

    price_rho_up = binomial_put(S, K, T, r + dR, sigma, steps, option_type)
    price_rho_down = binomial_put(S, K, T, r - dR, sigma, steps, option_type)
    rho = (price_rho_up - price_rho_down) / (2 * dR)

    return {
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }