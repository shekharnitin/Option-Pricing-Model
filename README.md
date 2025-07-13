# 📈 Option Pricing Calculator

An interactive Flask-based web application to calculate and visualize European option prices using multiple models: **Binomial Tree**, **Black-Scholes**, and **Heston Stochastic Volatility**.

---

## 🚀 Features

- 🔢 **Calculate Option Prices** for both **Call** and **Put** options.
- 🧠 **Pricing Models Supported**:
  - Binomial Tree
  - Black-Scholes
  - Heston Model
- 🌗 **Dark/Light Mode** toggle
- 📊 **Visualizations**:
  - Price vs Stock Price
  - Price vs Number of Steps (Binomial)
  - Price vs Correlation (Heston)
  - Heatmaps for Black-Scholes & Heston
- 📉 Dynamic plots using Matplotlib
- 🧮 Sidebar with collapsible animation for parameter selection
- 🌐 Responsive UI with custom scrollbar & theme-based styles
- 🔗 Footer with social links (LinkedIn & GitHub)

---

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Backend**: Python (Flask)
- **Plotting**: Matplotlib, NumPy
- **Models**:
  - `black_scholes.py`
  - `binomial_model.py`
  - `heston_model.py`

---

## 🧪 Demo

You can test it locally using:

```bash
git clone https://github.com/yourusername/option-pricing-calculator.git
cd option-pricing-calculator
pip install -r requirements.txt
python app.py
