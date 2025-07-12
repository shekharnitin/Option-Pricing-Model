def binomial_option_price(S, K, T, r, sigma, steps=100, option_type='call'):
    from math import exp, sqrt

    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp(r * dt) - d) / (u - d)

    prices = [S * (u ** j) * (d ** (steps - j)) for j in range(steps + 1)]

    if option_type == 'call':
        values = [max(0, price - K) for price in prices]
    else:
        values = [max(0, K - price) for price in prices]

    for i in range(steps - 1, -1, -1):
        values = [
            exp(-r * dt) * (p * values[j + 1] + (1 - p) * values[j])
            for j in range(i + 1)
        ]

    return round(values[0], 2)
