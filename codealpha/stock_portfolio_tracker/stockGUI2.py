import requests
import pandas as pd
import tkinter as tk
from tkinter import messagebox

# Dictionary to store registered users and their passwords
registered_users = {}
logged_in_user = None
portfolio = {}

# Function to authenticate user credentials
def authenticate(username, password):
    # Check if username exists and if the provided password matches the stored password
    return username in registered_users and registered_users[username] == password

# Function to handle user registration
def register():
    username = entry_username.get()
    password = entry_password.get()
    if username.isalpha() and password.isdigit():
        if username not in registered_users:
            registered_users[username] = password
            messagebox.showinfo("Registration", "Registration successful.")
            show_login_ui()  # Navigate to login after successful registration
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        messagebox.showerror("Registration Failed", "Invalid username or password. Username should be text only and password should be number only.")

# Function to handle user login
def login():
    global logged_in_user
    username = entry_username.get()
    password = entry_password.get()
    if authenticate(username, password):
        logged_in_user = username
        messagebox.showinfo("Login", f"Welcome, {username}!")
        show_portfolio_ui()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to handle logout
def logout():
    global logged_in_user
    logged_in_user = None
    show_login_ui()

# Function to display portfolio UI after successful login
def show_portfolio_ui():
    login_frame.pack_forget()
    portfolio_frame.pack()

# Function to display login UI
def show_login_ui():
    portfolio_frame.pack_forget()
    login_frame.pack()

# Function to get real-time stock data
def get_stock_data(symbol):
    api_key = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key from Alphavantage
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    
    # Check if the response contains data and the required fields
    if 'Global Quote' in data and '05. price' in data['Global Quote']:
        return data['Global Quote']
    else:
        messagebox.showerror("Error", f"Failed to retrieve data for {symbol}. Please check the symbol.")
        return None

# Function to add a stock to the portfolio
def add_stock():
    symbol = entry_symbol.get().upper()
    stock_data = get_stock_data(symbol)
    if stock_data:
        portfolio[symbol] = stock_data
        messagebox.showinfo("Success", f"{symbol} added to portfolio.")
    else:
        messagebox.showerror("Error", f"Failed to add {symbol} to portfolio. Please check the symbol.")

# Function to remove a stock from the portfolio
def remove_stock():
    symbol = entry_symbol.get().upper()
    if symbol in portfolio:
        del portfolio[symbol]
        messagebox.showinfo("Success", f"{symbol} removed from portfolio.")
    else:
        messagebox.showerror("Error", f"{symbol} is not in the portfolio.")

# Function to display the portfolio without visualization
def display_portfolio():
    if portfolio:
        # Extract stock symbols and quantities from the portfolio dictionary
        symbols = list(portfolio.keys())
        quantities = [portfolio[symbol]['05. price'] for symbol in symbols]  # Access '05. price' field from stock data

        # Create DataFrame from the extracted data
        df = pd.DataFrame({'Symbol': symbols, 'Price': quantities})

        # Show portfolio information in a message box
        messagebox.showinfo("Portfolio", df.to_string())
    else:
        messagebox.showinfo("Portfolio", "Portfolio is empty.")

# Function to register a user
def register():
    username = entry_username.get()
    password = entry_password.get()
    if username.isalpha() and password.isdigit():
        if username not in registered_users:
            registered_users[username] = password
            messagebox.showinfo("Registration", "Registration successful.")
            show_login_ui()  # Navigate to login after successful registration
        else:
            messagebox.showerror("Registration Failed", "Username already exists.")
    else:
        messagebox.showerror("Registration Failed", "Invalid username or password. Username should be text only and password should be number only.")

# Main program loop to Display UI using Python Tkinter 
def main():
    global entry_symbol, entry_username, entry_password, login_frame, portfolio_frame, portfolio, logged_in_user
    
    root = tk.Tk()
    root.title("Stock Portfolio Tracker")
    root.configure(bg="#E6E6FA")  # Set background color to lavender

    # Frames for login and portfolio UI
    login_frame = tk.Frame(root, bg="gray")  # Set background color to gray
    portfolio_frame = tk.Frame(root)

    # Login UI
    label_username = tk.Label(login_frame, text="Username:", bg="gray", font=("Arial", 24, "bold"))  # Set background color and font, increase font size
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(login_frame, font=("Arial", 24))  # Set font, increase font size
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(login_frame, text="Password:", bg="gray", font=("Arial", 24, "bold"))  # Set background color and font, increase font size
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(login_frame, show="*", font=("Arial", 24))  # Set font, increase font size
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_login = tk.Button(login_frame, text="Login", command=login, bg="#4CAF50", fg="white", font=("Arial", 24, "bold"), width=15, height=2)  # Set background color, foreground color, and font, increase font size, adjust button size
    button_login.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    button_register = tk.Button(login_frame, text="Register", command=register, bg="#4CAF50", fg="white", font=("Arial", 24, "bold"), width=15, height=2)  # Set background color, foreground color, and font, increase font size, adjust button size
    button_register.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Portfolio UI
    label_symbol = tk.Label(portfolio_frame, text="Enter Stock Symbol:", font=("Arial", 32, "bold"))  # Set font, increase font size
    label_symbol.pack()

    entry_symbol = tk.Entry(portfolio_frame, font=('Arial', 48))  # Set font and increase size
    entry_symbol.pack(pady=20, padx=40)

    button_add = tk.Button(portfolio_frame, text="Add Stock", command=add_stock, bg="#4CAF50", fg="white", width=60, height=3, font=('Arial', 32, 'bold'))  # Increase button size and set font, increase font size
    button_add.pack(pady=20)

    button_remove = tk.Button(portfolio_frame, text="Remove Stock", command=remove_stock, bg="#f44336", fg="white", width=60, height=3, font=('Arial', 32, 'bold'))  # Increase button size and set font, increase font size
    button_remove.pack(pady=20)

    button_display = tk.Button(portfolio_frame, text="Display Portfolio", command=display_portfolio, bg="#2196F3", fg="white", width=60, height=3, font=('Arial', 32, 'bold'))  # Increase button size and set font, increase font size
    button_display.pack(pady=20)

    button_logout = tk.Button(portfolio_frame, text="Logout", command=logout, bg="gray", fg="white", width=10, height=2, font=('Arial', 28, 'bold'))  # Increase button size and set font, increase font size
    button_logout.pack(pady=20)

    # Initial setup
    show_login_ui()

    root.mainloop()

if __name__ == "__main__":
    main()
