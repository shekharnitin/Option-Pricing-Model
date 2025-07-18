from flask import Flask, render_template, request
from black_scholes import black_scholes, generate_bs_heatmap
from binomial_model import binomial_option_price
from heston_model import heston_price, generate_heston_heatmap
import matplotlib.pyplot as plt
import numpy as np
import os
import yfinance as yf
import datetime

app = Flask(__name__)
os.makedirs('static', exist_ok=True)

# For demo/testing, set a fixed date. For production, use datetime.date.today()
today = datetime.date.today()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Set defaults
    default_values = {
        'S': 100, 'K': 100, 'T': 1, 'r': 0.05, 'sigma': 0.2, 'model': 'binomial', 'steps': 100,
        'kappa': 1.5, 'theta': 0.04, 'sigma_h': 0.3, 'rho': -0.7, 'v0': 0.04, 'show_heatmap': False
    }

    call_price = put_price = plot_path = bs_plot_path = heatmap_call_path = heatmap_put_path = s_plot_path = rho_plot_path = error = None

    # Use defaults or POST values
    form_data = {}
    for key in default_values:
        form_data[key] = request.form.get(key, default_values[key])
        if key not in ("model", "show_heatmap"):
            try:
                form_data[key] = float(form_data[key])
            except (ValueError, TypeError):
                form_data[key] = default_values[key]
    form_data['steps'] = int(request.form.get('steps', default_values['steps']))
    form_data['model'] = request.form.get('model', default_values['model'])
    form_data['show_heatmap'] = 'show_heatmap' in request.form
    


    # Use custom mode by default
    # If GET request, calculate using defaults
    if request.method == 'GET':
        S = default_values['S']
        K = default_values['K']
        T = default_values['T']
        r = default_values['r']
        sigma = default_values['sigma']
        model = default_values['model']
        steps = default_values['steps']
        kappa = default_values['kappa']
        theta = default_values['theta']
        sigma_h = default_values['sigma_h']
        rho = default_values['rho']
        v0 = default_values['v0']
        show_heatmap = default_values['show_heatmap']

        try:
            if model == 'binomial':
                call_price = binomial_option_price(S, K, T, r, sigma, steps, 'call')
                put_price = binomial_option_price(S, K, T, r, sigma, steps, 'put')
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
                if show_heatmap:
                    heatmap_call_path = generate_bs_heatmap(K, r, sigma, T, 'call')
                    heatmap_put_path = generate_bs_heatmap(K, r, sigma, T, 'put')
            elif model == 'heston':
                call_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'call')
                put_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'put')
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
                if show_heatmap:
                    heatmap_call_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'call')
                    heatmap_put_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'put')
        except Exception as e:
            error = f"Default calculation failed: {e}"


    if request.method == 'POST':
        form_data = request.form.to_dict()  # Always set form_data so input values persist
        input_mode = request.form.get('input_mode', 'custom')

        if input_mode == 'live':
            form_data['input_mode'] = input_mode
            # Grab all live mode fields—validate
            ticker = request.form.get('ticker', '').upper().strip()
            K_live = request.form.get('K_live', '')
            expiry_live = request.form.get('expiry_live', '')
            r_live = request.form.get('r_live', '')
            sigma_live = request.form.get('sigma_live', '')
            # Validate required
            req_fields = []
            if not ticker:
                req_fields.append("Ticker symbol is required.")
            if not K_live:
                req_fields.append("Strike price is required.")
            if not expiry_live:
                req_fields.append("Expiry date is required.")
            if not r_live:
                req_fields.append("Risk-free rate is required.")
            if req_fields:
                error = " ".join(req_fields)
                return render_template('index.html', error=error, form_data=form_data)
            try:
                K = float(K_live)
                r = float(r_live) 
                expiry = datetime.datetime.strptime(expiry_live, "%Y-%m-%d").date()
                T = (expiry - today).days / 365.0
            except Exception as e:
                error = "Invalid input: " + str(e)
                return render_template('index.html', error=error, form_data=form_data)
            # Live query
            try:
                stock = yf.Ticker(ticker)
                df = stock.history(period="1mo")
                S = float(df['Close'][-1])
            except Exception as e:
                error = f"Could not fetch data for ticker '{ticker}': {e}"
                return render_template('index.html', error=error, form_data=form_data)
            # Volatility
            try:
                if sigma_live:
                    sigma = float(sigma_live) / 100
                else:
                    returns = np.log(df['Close'] / df['Close'].shift(1)).dropna()
                    sigma = returns.std() * np.sqrt(252)
            except Exception as e:
                error = "Error calculating volatility: " + str(e)
                return render_template('index.html', error=error, form_data=form_data)

            # Pricing
            try:
                call_price = black_scholes(S, K, T, r, sigma, 'call')
                put_price = black_scholes(S, K, T, r, sigma, 'put')
            except Exception as e:
                error = "Pricing failed: " + str(e)
                return render_template('index.html', error=error, form_data=form_data)

            # Plot
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
            
            # Keep form fields filled after success
            form_data.update({'S': S, 'K': K, 'T': T, 'r': r, 'sigma': sigma, 'ticker': ticker,
                              'expiry': expiry.strftime('%Y-%m-%d'), 'sigma_live': sigma_live, 
                              'input_mode': 'live', 'K_live': K_live, 'expiry_live': expiry_live, 'r_live': r_live})

        else:
            form_data['input_mode'] = input_mode
            # Custom mode
            try:
                S = float(request.form.get('S', form_data.get('S', 100)))
                K = float(request.form.get('K', form_data.get('K', 100)))
                expiry_custom = request.form.get('expiry_custom', '')
                if expiry_custom:
                    try:
                        expiry = datetime.datetime.strptime(expiry_custom, "%Y-%m-%d").date()
                        T = (expiry - today).days / 365.0
                    except Exception as e:
                        error = f"Invalid custom expiry date: {e}"
                        return render_template('index.html', error=error, form_data=form_data)
                else:
                    T = float(request.form.get('T', form_data.get('T', 1)))
                r = float(request.form.get('r', form_data.get('r', 0.05)))
                sigma = float(request.form.get('sigma', form_data.get('sigma', 0.2)))
                model = request.form.get('model', form_data.get('model', 'binomial'))
                steps = int(request.form.get('steps', form_data.get('steps', 100)))
                kappa = float(request.form.get('kappa', form_data.get('kappa', 1.5)))
                theta = float(request.form.get('theta', form_data.get('theta', 0.04)))
                sigma_h = float(request.form.get('sigma_h', form_data.get('sigma_h', 0.3)))
                rho = float(request.form.get('rho', form_data.get('rho', -0.7)))
                v0 = float(request.form.get('v0', form_data.get('v0', 0.04)))
                show_heatmap = 'show_heatmap' in request.form
            except Exception as e:
                error = "Invalid input: " + str(e)
                return render_template('index.html', error=error, form_data=form_data)
            
            if model == 'binomial':
                call_price = binomial_option_price(S, K, T, r, sigma, steps, 'call')
                put_price = binomial_option_price(S, K, T, r, sigma, steps, 'put')
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
                if show_heatmap:
                    heatmap_call_path = generate_bs_heatmap(K, r, sigma, T, 'call')
                    heatmap_put_path = generate_bs_heatmap(K, r, sigma, T, 'put')
            elif model == 'heston':
                call_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'call')
                put_price = heston_price(S, K, T, r, kappa, theta, sigma_h, rho, v0, 'put')
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
                if show_heatmap:
                    heatmap_call_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'call')
                    heatmap_put_path = generate_heston_heatmap(K, T, r, kappa, theta, sigma_h, v0, 'put')

    return render_template(
        'index.html',
        call_price=call_price,
        put_price=put_price,
        plot_path=plot_path,
        bs_plot_path=bs_plot_path,
        heatmap_call_path=heatmap_call_path,
        heatmap_put_path=heatmap_put_path,
        s_plot_path=s_plot_path,
        rho_plot_path=rho_plot_path,
        form_data=form_data,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)
