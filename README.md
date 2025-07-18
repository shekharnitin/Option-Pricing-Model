# Option Pricing Calculator

A robust, interactive web application for **European option pricing and visualization** using cutting-edge quantitative models, suitable for financial professionals, quantitative researchers, and students. Developed with an emphasis on clarity, flexibility, and user experience.

**🌐 Live Demo:**  
The application is deployed and accessible at:  
[https://option-pricing-model.onrender.com/](https://option-pricing-model.onrender.com/)

## 🚀 Features

- **Multi-Model Support**  
  Calculate **Call** and **Put** option prices with:
  - **Binomial Tree Model**
  - **Black-Scholes Model**
  - **Heston Stochastic Volatility Model**

- **Live Mode and Custom Mode**
  - Live Mode allows you to fetch live market data using yfinance.
  - Custom Mode empowers you to input each parameter manually.

- **Rich Visualizations**
  - Price vs. Stock Price plots
  - Price vs. Number of Steps (Binomial Model)
  - Price vs. Correlation (Heston Model)
  - Heatmaps for Black-Scholes & Heston models
  - Dynamic, interactive Matplotlib-based charts

- **Modern Responsive UI**
  - Supports Light/Dark mode
  - Collapsible parameter sidebar
  - Custom scrollbars & theme-based styles

- **User-Friendly & Educational**
  - Intuitive controls and clear, guided parameter selection
  - Real-time feedback on pricing model parameter changes

## 📚 Table of Contents

- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots](#-screenshots)
- [Getting Started](#getting-started)
- [Option Pricing Models](#option-pricing-models)
- [Folder Structure](#folder-structure)
- [License](#license)
- [Connect](#connect)

## 🛠️ Tech Stack

| Frontend    | Backend        | Visualization      | Models                            |
|-------------|---------------|--------------------|------------------------------------|
| HTML5, CSS3 | Python (Flask)| Matplotlib, NumPy  | Binomial, Black-Scholes, Heston    |
| Bootstrap 5 |               |                    |                                    |

## Getting Started

**Prerequisites:**
- Python 3.7+
- pip

**Installation & Run:**

git clone https://github.com/shekharnitin/Option-Pricing-Model.git
cd Option-Pricing-Model
pip install -r requirements.txt
python app.py

Navigate to [http://localhost:5000](http://localhost:5000).

**Live Mode is enabled by default.**  
Interactively adjust parameters and see results update instantly in both the local version and the [deployed app](https://option-pricing-model.onrender.com/).

## Option Pricing Models

- **Black-Scholes:** Analytical formula for European options, assuming constant volatility and no dividends.
- **Binomial Tree:** Flexible discrete-time model, visualizing convergence and the effect of step size.
- **Heston Model:** Accounts for stochastic volatility, pricing options in more realistic markets.

## 📂 Folder Structure

Option-Pricing-Model/
│
├── app.py # Flask app entry point
├── black_scholes.py # Black-Scholes implementation
├── binomial_model.py # Binomial Model implementation
├── heston_model.py # Heston Model implementation
├── requirements.txt
├── static/ # CSS, assets
├── templates/ # HTML template
└── README.md

## 💡 Why This Project Stands Out

- **Clear, Modularized Financial Engineering Code**
- **Practical Application of Mathematical Finance Theory**
- **Live Mode for Real-Time Financial Analysis**
- **Rich, Modern Visualizations**
- **Designed for Both Professional & Educational Use**
- **Clean, Scalable Flask Architecture**
- **Conforms to Software Engineering Best Practices**

## 🌐 Connect

- [LinkedIn](https://www.linkedin.com/in/shekharnitin)
- [GitHub](https://github.com/shekharnitin)
