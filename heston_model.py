from scipy.integrate import quad
import numpy as np
from cmath import exp, log, sqrt
import matplotlib.pyplot as plt
import os 

def heston_price(S, K, T, r, kappa, theta, sigma, rho, v0, option_type):
    def integrand(phi, j):
        u = 0.5 if j == 1 else -0.5
        b = kappa - rho * sigma if j == 1 else kappa
        a = kappa * theta

        d = sqrt((rho * sigma * phi * 1j - b)**2 - sigma**2 * (2 * u * phi * 1j - phi**2))
        g = (b - rho * sigma * phi * 1j + d) / (b - rho * sigma * phi * 1j - d)

        C = r * phi * 1j * T + a / sigma**2 * ((b - rho * sigma * phi * 1j + d) * T - 2 * log((1 - g * exp(d * T)) / (1 - g)))
        D = (b - rho * sigma * phi * 1j + d) / sigma**2 * ((1 - exp(d * T)) / (1 - g * exp(d * T)))

        return (exp(-phi * 1j * log(K)) * exp(C + D * v0 + 1j * phi * log(S))).real / (phi * 1j)

    P1 = 0.5 + 1/np.pi * quad(lambda phi: integrand(phi, 1).real, 0, 100)[0]
    P2 = 0.5 + 1/np.pi * quad(lambda phi: integrand(phi, 2).real, 0, 100)[0]

    call_price = S * P1 - K * np.exp(-r * T) * P2

    if option_type == 'call':
        return round(call_price, 2)
    else:
        put_price = call_price - S + K * np.exp(-r * T)
        return round(put_price, 2)

def generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, option_type):
    S_vals = np.linspace(50, 150, 40)
    rho_vals = np.linspace(-0.95, 0.95, 40)

    heatmap_data = np.zeros((len(S_vals), len(rho_vals)))

    for i, S in enumerate(S_vals):
        for j, rho in enumerate(rho_vals):
            try:
                heatmap_data[i, j] = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, option_type)
            except:
                heatmap_data[i, j] = np.nan  # skip failed evals

    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, aspect='auto', origin='lower',
               extent=[rho_vals[0], rho_vals[-1], S_vals[0], S_vals[-1]],
               cmap='coolwarm')
    plt.colorbar(label='Option Price')
    plt.xlabel('Correlation (ρ)')
    plt.ylabel('Stock Price (S)')
    plt.title(f'{option_type.capitalize()} Option Price Heatmap (Heston)')

    os.makedirs('static', exist_ok=True)
    heatmap_path = 'static/heston_heatmap.png'
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path
