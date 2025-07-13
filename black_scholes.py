import math
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return round(price, 2)

def generate_bs_heatmap(K, r, sigma, T, option_type):
    S_vals = np.linspace(50, 150, 50)  # stock price range
    T_vals = np.linspace(0.1, 2, 50)   # time to maturity

    heatmap_data = np.zeros((len(S_vals), len(T_vals)))

    for i, S in enumerate(S_vals):
        for j, t in enumerate(T_vals):
            heatmap_data[i, j] = black_scholes(S, K, t, r, sigma, option_type)

    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, aspect='auto', origin='lower',
               extent=[T_vals[0], T_vals[-1], S_vals[0], S_vals[-1]],
               cmap='viridis')
    plt.colorbar(label='Option Price')
    plt.xlabel('Time to Maturity (T)')
    plt.ylabel('Stock Price (S)')
    plt.title(f'{option_type.capitalize()} Option Price Heatmap (Black-Scholes)')

    os.makedirs('static', exist_ok=True)
    heatmap_path = 'static/bs_heatmap.png'
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path
