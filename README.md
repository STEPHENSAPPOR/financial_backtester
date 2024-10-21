# Financial Backtester

## Overview

**Financial Backtester** is a Django-based backend application designed to fetch financial data from public APIs, allowing users to backtest their trading strategies and generate reports.

## Features

- Fetch daily stock prices from Alpha Vantage API.
- Store financial data in a PostgreSQL database.
- Implement a basic backtesting module for trading strategies.
- Generate performance reports including total return and max drawdown.
- Integrate a pre-trained machine learning model for future stock price predictions.
- Generate visual reports with key financial metrics.

## Technologies Used

- Python 3.9
- Django 4.x
- PostgreSQL
- Docker
- GitHub Actions (for CI/CD)
- Alpha Vantage API

## Installation

### Prerequisites

- Python 3.9+
- PostgreSQL
- Docker
- Docker Compose
- An Alpha Vantage API key

### Clone the Repository

```bash
git clone https://github.com/STEPHENSAPPOR/financial_backtester.git
cd financial_backtester

