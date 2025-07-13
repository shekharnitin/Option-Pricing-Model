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
    result = None
    plot_path = None
    bs_plot_path = None
    bs_heatmap_path = None
    s_plot_path = None
    rho_plot_path = None
    heston_heatmap_path = None


    if request.method == 'POST':
        S = float(request.form['S'])
        K = float(request.form['K'])
        T = float(request.form['T'])
        r = float(request.form['r'])
        sigma = float(request.form['sigma'])
        option_type = request.form['option_type']
        model = request.form['model']
        steps = int(request.form.get('steps', 100))
        show_heatmap = 'show_heatmap' in request.form


        if model == 'black_scholes':
            result = black_scholes(S, K, T, r, sigma, option_type)
            if show_heatmap:
                heatmap_path = generate_bs_heatmap(K, r, sigma, T, option_type)
            S_values = np.linspace(0.5 * S, 1.5 * S, 100)
            bs_prices = [black_scholes(s, K, T, r, sigma, option_type) for s in S_values]
            os.makedirs('static', exist_ok=True)
            bs_plot_path = 'static/bs_vs_s.png'
            plt.figure()
            plt.plot(S_values, bs_prices)
            plt.title(f'{option_type.capitalize()} Option Price vs Stock Price (Black-Scholes)')
            plt.xlabel('Stock Price (S)')
            plt.ylabel('Option Price')
            plt.grid(True)
            plt.savefig(bs_plot_path)
            plt.close()
        elif model == 'binomial':
            result = binomial_option_price(S, K, T, r, sigma, steps=steps, option_type=option_type)
            # Generate plot
            prices = [binomial_option_price(S, K, T, r, sigma, steps=s, option_type=option_type) for s in range(1, steps + 1)]
            plt.figure()
            plt.plot(range(1, steps + 1), prices, marker='o')
            plt.title(f'{option_type.capitalize()} Option Price vs Steps (Binomial)')
            plt.xlabel('Steps')
            plt.ylabel('Option Price')
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
            result = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, option_type)
            # Option Price vs S
            S_vals = np.linspace(50, 150, 100)
            s_prices = [heston_price(S_, K, T, r, kappa, theta, sigma_h, rho, v0, option_type) for S_ in S_vals]
            plt.figure()
            plt.plot(S_vals, s_prices)
            plt.title(f'{option_type.capitalize()} Option Price vs Stock Price (Heston)')
            plt.xlabel('Stock Price (S)')
            plt.ylabel('Option Price')
            plt.grid(True)
            os.makedirs('static', exist_ok=True)
            s_plot_path = 'static/heston_vs_s.png'
            plt.savefig(s_plot_path)
            plt.close()

            # Option Price vs Correlation
            rho_vals = np.linspace(-1, 1, 100)
            rho_prices = [heston_price(S, K, T, r, kappa, theta, sigma_h, rho_, v0, option_type) for rho_ in rho_vals]
            plt.figure()
            plt.plot(rho_vals, rho_prices)
            plt.title(f'{option_type.capitalize()} Option Price vs Correlation (ρ) (Heston)')
            plt.xlabel('Correlation ρ')
            plt.ylabel('Option Price')
            plt.grid(True)
            rho_plot_path = 'static/heston_vs_rho.png'
            plt.savefig(rho_plot_path)
            plt.close()
            if show_heatmap:
                heatmap_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, option_type)





    return render_template('index.html', result=result, plot_path=plot_path, bs_plot_path=bs_plot_path, heatmap_path=heatmap_path, s_plot_path=s_plot_path, rho_plot_path=rho_plot_path)

if __name__ == '__main__':
    app.run(debug=True)
