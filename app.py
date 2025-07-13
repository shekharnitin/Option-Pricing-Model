from flask import Flask, render_template, request
from black_scholes import black_scholes, generate_bs_heatmap
from binomial_model import binomial_option_price
from heston_model import heston_price, generate_heston_heatmap
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)
os.makedirs('static', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default parameters
    default_values = {
        'S': 100,
        'K': 100,
        'T': 1,
        'r': 0.05,
        'sigma': 0.2,
        'model': 'binomial',
        'steps': 100,
        'kappa': 1.5,
        'theta': 0.04,
        'sigma_h': 0.3,
        'rho': -0.7,
        'v0': 0.04,
        'show_heatmap': False
    }

    # Fill with POST values or defaults
    form_data = {}
    for key in default_values:
        form_data[key] = request.form.get(key, default_values[key])
        if key != 'model' and key != 'show_heatmap':
            try:
                form_data[key] = float(form_data[key])
            except ValueError:
                form_data[key] = default_values[key]

    form_data['steps'] = int(form_data['steps']) if 'steps' in request.form else default_values['steps']
    form_data['model'] = request.form.get('model', default_values['model'])
    form_data['show_heatmap'] = 'show_heatmap' in request.form

    call_price = None
    put_price = None
    plot_path = None
    bs_plot_path = None
    heatmap_path = None
    s_plot_path = None
    rho_plot_path = None

    S = form_data['S']
    K = form_data['K']
    T = form_data['T']
    r = form_data['r']
    sigma = form_data['sigma']
    model = form_data['model']
    steps = form_data['steps']

    if model == 'binomial':
        call_price = binomial_option_price(S, K, T, r, sigma, steps, 'call')
        put_price = binomial_option_price(S, K, T, r, sigma, steps, 'put')

        # Plot
        call_prices = [binomial_option_price(S, K, T, r, sigma, s, 'call') for s in range(1, steps + 1)]
        put_prices = [binomial_option_price(S, K, T, r, sigma, s, 'put') for s in range(1, steps + 1)]
        plot_path = 'static/option_price_plot.png'
        plt.figure()
        plt.plot(range(1, steps + 1), call_prices, marker='o', label="Call Option", color='blue')
        plt.plot(range(1, steps + 1), put_prices, marker='x', label="Put Option", color='orange')
        plt.title("Option Prices vs Steps (Binomial)")
        plt.xlabel('Steps')
        plt.ylabel('Option Price')
        plt.grid(True)
        plt.legend()
        plt.savefig(plot_path)
        plt.close()

    elif model == 'black_scholes':
        call_price = black_scholes(S, K, T, r, sigma, 'call')
        put_price = black_scholes(S, K, T, r, sigma, 'put')

        # Plot: Call Option Price vs Stock Price
        S_values = np.linspace(0.5 * S, 1.5 * S, 100)
        call_prices = [black_scholes(s, K, T, r, sigma, 'call') for s in S_values]
        put_prices = [black_scholes(s, K, T, r, sigma, 'put') for s in S_values]
        bs_plot_path = 'static/bs_vs_s.png'
        plt.figure()
        plt.plot(S_values, call_prices, label="Call Option", color='green')
        plt.plot(S_values, put_prices, label="Put Option", color='red')
        plt.title("Option Prices vs Stock Price (Black-Scholes)")
        plt.xlabel('Stock Price (S)')
        plt.ylabel('Option Price')
        plt.grid(True)
        plt.legend()
        plt.savefig(bs_plot_path)
        plt.close()

        if form_data['show_heatmap']:
            heatmap_path = generate_bs_heatmap(K, r, sigma, T, 'call')

    

    elif model == 'heston':
        kappa = form_data['kappa']
        theta = form_data['theta']
        sigma_h = form_data['sigma_h']
        rho = form_data['rho']
        v0 = form_data['v0']

        call_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'call')
        put_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'put')

        # Option Price vs Stock Price (Call)
        S_vals = np.linspace(50, 150, 100)
        call_prices = [heston_price(s_, K, T, r, kappa, theta, sigma_h, rho, v0, 'call') for s_ in S_vals]
        put_prices = [heston_price(s_, K, T, r, kappa, theta, sigma_h, rho, v0, 'put') for s_ in S_vals]
        s_plot_path = 'static/heston_vs_s.png'
        plt.figure()
        plt.plot(S_vals, call_prices, label="Call Option", color='purple')
        plt.plot(S_vals, put_prices, label="Put Option", color='brown')
        plt.title("Option Prices vs Stock Price (Heston)")
        plt.xlabel('Stock Price (S)')
        plt.ylabel('Option Price')
        plt.grid(True)
        plt.legend()
        plt.savefig(s_plot_path)
        plt.close()

        # Option Price vs ρ (Call)
        rho_vals = np.linspace(-1, 1, 100)
        call_rho_prices = [heston_price(S, K, T, r, kappa, theta, sigma_h, r_, v0, 'call') for r_ in rho_vals]
        put_rho_prices = [heston_price(S, K, T, r, kappa, theta, sigma_h, r_, v0, 'put') for r_ in rho_vals]
        rho_plot_path = 'static/heston_vs_rho.png'
        plt.figure()
        plt.plot(rho_vals, call_rho_prices, label="Call Option", color='green')
        plt.plot(rho_vals, put_rho_prices, label="Put Option", color='red')
        plt.title("Option Prices vs Correlation ρ (Heston)")
        plt.xlabel('Correlation ρ')
        plt.ylabel('Option Price')
        plt.grid(True)
        plt.legend()
        plt.savefig(rho_plot_path)
        plt.close()

        if form_data['show_heatmap']:
            heatmap_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'call')

    return render_template(
        'index.html',
        call_price=call_price,
        put_price=put_price,
        plot_path=plot_path,
        bs_plot_path=bs_plot_path,
        heatmap_path=heatmap_path,
        s_plot_path=s_plot_path,
        rho_plot_path=rho_plot_path,
        form_data=form_data
    )

if __name__ == '__main__':
    app.run(debug=True)
