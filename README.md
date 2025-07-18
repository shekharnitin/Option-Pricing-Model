# Option Pricing Calculator

A robust, interactive web application for **European option pricing and visualization** using cutting-edge quantitative models, suitable for financial professionals, quantitative researchers, and students. Developed with an emphasis on clarity, flexibility, and user experience.

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

**🌐 Live Demo:**  
The application is deployed and accessible at:  
[https://option-pricing-model.onrender.com/](https://option-pricing-model.onrender.com/)

## 🚀 Features

- **Multi-Model Support**  
  Calculate **Call** and **Put** option prices with:
  - **Binomial Tree Model**
  - **Black-Scholes Model**
  - **Heston Stochastic Volatility Model**

- **Rich Visualizations**
  - Price vs. Stock Price plots
  - Price vs. Number of Steps (Binomial Model)
  - Price vs. Correlation (Heston Model)
  - Heatmaps for Black-Scholes & Heston
  - Dynamic Matplotlib-based plots

- **Modern Responsive UI**
  - Light/Dark mode toggle
  - Collapsible parameter sidebar
  - Custom scrollbars & theme-based styles

- **User-Friendly & Educational**
  - Intuitive controls and clear parameter selection
  - Real-time feedback on pricing model parameter changes

## 🧪 Live Demo

Explore the deployed version here:  
👉 **[Option Pricing Model Web App](https://option-pricing-model.onrender.com/)**

## 🛠️ Tech Stack

| Frontend    | Backend        | Visualization      | Models                            |
|-------------|---------------|--------------------|------------------------------------|
| HTML5, CSS3 | Python (Flask)| Matplotlib, NumPy  | Binomial, Black-Scholes, Heston    |
| Bootstrap 5 |               |                    |                                    |

## 🖥️ Screenshots

> *[Screenshots or animated GIFs of key app pages or plots would be here to illustrate features to recruiters and users.]*

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

## Option Pricing Models

- **Black-Scholes:** Analytical formula for European options, assuming constant volatility and no dividends.
- **Binomial Tree:** Flexible discrete-time model, visualizing convergence and effect of step size.
- **Heston Model:** Accounts for stochastic volatility, enabling pricing in more realistic markets.

## 📂 Folder Structure

Option-Pricing-Model/
│
├── app.py # Flask app entry point
├── black_scholes.py # Black-Scholes implementation
├── binomial_model.py # Binomial Model implementation
├── heston_model.py # Heston Model implementation
├── requirements.txt
├── static/ # CSS, assets
├── templates/ # HTML templates
└── README.md

## 💡 Why This Project Stands Out

- **Clear, Modularized Financial Engineering Code**
- **Practical Application of Mathematical Finance Theory**
- **Rich, Modern Visualizations**
- **Designed for Both Professional & Educational Use**
- **Clean, Scalable Flask Architecture**
- **Conforms to Software Engineering Best Practices**

## 🌐 Connect

- [LinkedIn](https://www.linkedin.com/in/shekharnitin)
- [GitHub](https://github.com/shekharnitin)
