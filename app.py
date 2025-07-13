from flask import Flask, render_template, request
from black_scholes import black_scholes, generate_bs_heatmap
from binomial_model import binomial_option_price
from heston_model import heston_price, generate_heston_heatmap
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    call_result = None
    put_result = None
    plot_path = None
    bs_plot_path = None
    heatmap_path = None
    s_plot_path = None
    rho_plot_path = None
    model = None

    if request.method == 'POST':
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        model = request.form['model']
        steps = int(request.form.get('steps', 100))
        show_heatmap = 'show_heatmap' in request.form

        call_price = put_price = None

        if model == 'black_scholes':
            call_price = black_scholes(S, K, T, r, sigma, 'call')
            put_price = black_scholes(S, K, T, r, sigma, 'put')

            if show_heatmap:
                heatmap_path = generate_bs_heatmap(K, r, sigma, T, 'call')  # Heatmap uses 'call' by default

            # Plot: Option Price vs Stock Price
            S_values = np.linspace(0.5 * S, 1.5 * S, 100)
            call_prices = [black_scholes(s, K, T, r, sigma, 'call') for s in S_values]

            os.makedirs('static', exist_ok=True)
            bs_plot_path = 'static/bs_vs_s.png'
            plt.figure()
            plt.plot(S_values, call_prices, label="Call Option")
            plt.title("Call Option Price vs Stock Price (Black-Scholes)")
            plt.xlabel('Stock Price (S)')
            plt.ylabel('Option Price')
            plt.grid(True)
            plt.legend()
            plt.savefig(bs_plot_path)
            plt.close()

        elif model == 'binomial':
            call_price = binomial_option_price(S, K, T, r, sigma, steps=steps, option_type='call')
            put_price = binomial_option_price(S, K, T, r, sigma, steps=steps, option_type='put')

            prices = [binomial_option_price(S, K, T, r, sigma, steps=s, option_type='call') for s in range(1, steps + 1)]

            plt.figure()
            plt.plot(range(1, steps + 1), prices, marker='o', label="Call Option")
            plt.title("Call Option Price vs Steps (Binomial)")
            plt.xlabel('Steps')
            plt.ylabel('Option Price')
            plt.grid(True)
            plt.legend()
            os.makedirs('static', exist_ok=True)
            plot_path = 'static/option_price_plot.png'
            plt.savefig(plot_path)
            plt.close()

        elif model == 'heston':
            kappa = float(request.form['kappa'])
            theta = float(request.form['theta'])
            sigma_h = float(request.form['sigma_h'])
            rho = float(request.form['rho'])
            v0 = float(request.form['v0'])

            call_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'call')
            put_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'put')

            # Option Price vs S (Call)
            S_vals = np.linspace(50, 150, 100)
            s_prices = [heston_price(S_, K, T, r, kappa, theta, sigma_h, rho, v0, 'call') for S_ in S_vals]
            plt.figure()
            plt.plot(S_vals, s_prices, label="Call Option")
            plt.title("Call Option Price vs Stock Price (Heston)")
            plt.xlabel('Stock Price (S)')
            plt.ylabel('Option Price')
            plt.grid(True)
            plt.legend()
            os.makedirs('static', exist_ok=True)
            s_plot_path = 'static/heston_vs_s.png'
            plt.savefig(s_plot_path)
            plt.close()

            # Option Price vs ρ (Call)
            rho_vals = np.linspace(-1, 1, 100)
            rho_prices = [heston_price(S, K, T, r, kappa, theta, sigma_h, rho_, v0, 'call') for rho_ in rho_vals]
            plt.figure()
            plt.plot(rho_vals, rho_prices, label="Call Option")
            plt.title("Call Option Price vs Correlation ρ (Heston)")
            plt.xlabel('Correlation ρ')
            plt.ylabel('Option Price')
            plt.grid(True)
            plt.legend()
            rho_plot_path = 'static/heston_vs_rho.png'
            plt.savefig(rho_plot_path)
            plt.close()

            if show_heatmap:
                heatmap_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'call')


    return render_template(
    'index.html',
    call_price=call_price,
    put_price=put_price,
    plot_path=plot_path,
    bs_plot_path=bs_plot_path,
    heatmap_path=heatmap_path,
    s_plot_path=s_plot_path,
    rho_plot_path=rho_plot_path
)


if __name__ == '__main__':
    app.run(debug=True)
