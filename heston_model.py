from scipy.integrate import quad
import numpy as np
from cmath import exp, log, sqrt

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
