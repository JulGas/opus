import numpy as np
"""
    Monte Carlo pricing for European and Asian options.

    Parameters:
    S           : Spot price
    K           : Strike price
    T           : Time to maturity (years)
    r           : Risk-free interest rate (decimal)
    sigma       : Volatility (decimal)
    simulations : Number of Monte Carlo simulations
    steps       : Steps for Asian option (ignored for European)
    option_type       : Initially set to 'European'; 'Asian' selectable

    Returns:
    Option price (Call/Put)
    """

# =================== MONTE CARLO CALL OPTION FUNCTIONS ===================== #
def monte_carlo_call(S, K, T, r, sigma, simulations=10000, steps=100, option_type="European"):
    if option_type == "European":
        Z = np.random.randn(simulations)
        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        payoff = np.maximum(ST - K, 0)
        return np.exp(-r * T) * np.mean(payoff)

    elif option_type == "Asian":
        dt = T / steps
        Z = np.random.randn(simulations, steps)
        S_paths = np.zeros((simulations, steps + 1))
        S_paths[:, 0] = S

        drift = (r - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * Z

        for t in range(1, steps + 1):
            S_paths[:, t] = S_paths[:, t - 1] * np.exp(drift + diffusion[:, t - 1])

        S_avg = np.mean(S_paths, axis=1)
        payoff = np.maximum(S_avg - K, 0)
        return np.exp(-r * T) * np.mean(payoff)

    else:
        raise ValueError(f"Unsupported option_type: {option_type}")

def monte_carlo_greeks_call(S, K, T, r, sigma, simulations=10000, epsilon=1e-4):
    def price_fn(S_, K_, T_, r_, sigma_):
        return monte_carlo_call(S_, K_, T_, r_, sigma_, simulations=simulations, option_type="European")

    base_price = price_fn(S, K, T, r, sigma)

    price_up = price_fn(S + epsilon, K, T, r, sigma)
    price_down = price_fn(S - epsilon, K, T, r, sigma)
    delta = (price_up - price_down) / (2 * epsilon)
    gamma = (price_up - 2 * base_price + price_down) / (epsilon ** 2)

    T_eps = max(T - epsilon, 1e-6)
    theta = (price_fn(S, K, T_eps, r, sigma) - price_fn(S, K, T + epsilon, r, sigma)) / (2 * epsilon)

    vega = (price_fn(S, K, T, r, sigma + epsilon) - price_fn(S, K, T, r, sigma - epsilon)) / (2 * epsilon)

    rho = (price_fn(S, K, T, r + epsilon, sigma) - price_fn(S, K, T, r - epsilon, sigma)) / (2 * epsilon)

    return {
        "price": base_price,
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }

# =================== MONTE CARLO PUT OPTION FUNCTIONS ====================== #
def monte_carlo_put(S, K, T, r, sigma, simulations=10000, steps=100, option_type="European"):
    if option_type == "European":
        Z = np.random.randn(simulations)
        ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        payoff = np.maximum(K - ST, 0)
        return np.exp(-r * T) * np.mean(payoff)

    elif option_type == "Asian":
        dt = T / steps
        Z = np.random.randn(simulations, steps)
        S_paths = np.zeros((simulations, steps + 1))
        S_paths[:, 0] = S

        drift = (r - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * Z

        for t in range(1, steps + 1):
            S_paths[:, t] = S_paths[:, t - 1] * np.exp(drift + diffusion[:, t - 1])

        S_avg = np.mean(S_paths, axis=1)
        payoff = np.maximum(K - S_avg, 0)
        return np.exp(-r * T) * np.mean(payoff)

    else:
        raise ValueError(f"Unsupported option_type: {option_type}")

def monte_carlo_greeks_put(S, K, T, r, sigma, simulations=10000, epsilon=1e-4):
    def price_fn(S_, K_, T_, r_, sigma_):
        return monte_carlo_put(S_, K_, T_, r_, sigma_, simulations=simulations, option_type="European")

    base_price = price_fn(S, K, T, r, sigma)

    price_up = price_fn(S + epsilon, K, T, r, sigma)
    price_down = price_fn(S - epsilon, K, T, r, sigma)
    delta = (price_up - price_down) / (2 * epsilon)
    gamma = (price_up - 2 * base_price + price_down) / (epsilon ** 2)

    T_eps = max(T - epsilon, 1e-6)
    theta = (price_fn(S, K, T_eps, r, sigma) - price_fn(S, K, T + epsilon, r, sigma)) / (2 * epsilon)

    vega = (price_fn(S, K, T, r, sigma + epsilon) - price_fn(S, K, T, r, sigma - epsilon)) / (2 * epsilon)

    rho = (price_fn(S, K, T, r + epsilon, sigma) - price_fn(S, K, T, r - epsilon, sigma)) / (2 * epsilon)

    return {
        "price": base_price,
        "delta": delta,
        "gamma": gamma,
        "theta": theta,
        "vega": vega,
        "rho": rho
    }
