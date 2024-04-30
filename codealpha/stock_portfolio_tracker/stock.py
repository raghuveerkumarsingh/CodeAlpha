import requests
import pandas as pd

# Function to get real-time stock data
def get_stock_data(symbol):
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['Global Quote']

# Function to add a stock to the portfolio
def add_stock(portfolio, symbol):
    stock_data = get_stock_data(symbol)
    if stock_data:
        portfolio[symbol] = stock_data
        print(f"{symbol} added to portfolio.")
    else:
        print(f"Failed to add {symbol} to portfolio. Please check the symbol.")

# Function to remove a stock from the portfolio
def remove_stock(portfolio, symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"{symbol} removed from portfolio.")
    else:
        print(f"{symbol} is not in the portfolio.")

# Function to display the portfolio
def display_portfolio(portfolio):
    if portfolio:
        df = pd.DataFrame.from_dict(portfolio, orient='index')
        print(df)
    else:
        print("Portfolio is empty.")

# Sample portfolio
portfolio = {}

# Main program loop
while True:
    print("\nStock Portfolio Tracker")
    print("1. Add Stock")
    print("2. Remove Stock")
    print("3. Display Portfolio")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        symbol = input("Enter stock symbol: ").upper()
        add_stock(portfolio, symbol)
    elif choice == '2':
        symbol = input("Enter stock symbol to remove: ").upper()
        remove_stock(portfolio, symbol)
    elif choice == '3':
        display_portfolio(portfolio)
    elif choice == '4':
        print("Exiting program...")
        break
    else:
        print("Invalid choice. Please try again.")
