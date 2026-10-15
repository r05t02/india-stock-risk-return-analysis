import yfinance as yf
import pandas as pd


tickers = [
    "ICICIBANK.NS",  # ICICI Bank
    "HDFCBANK.NS",   # HDFC Bank
    "TCS.NS",        # Tata Consultancy Services
    "LT.NS",         # Larsen & Toubro
    "ITC.NS"         # ITC Limited 
    ]

def main():
    for stock in tickers:
        fetch_stock_df(stock)

        clean_stock(fetch_stock_df(stock), stock)




    

def fetch_stock_df(stock):
    stock = yf.Ticker(stock)

    stock_data_df = stock.history(period="max", auto_adjust=False)
    stock_data = stock_data_df.reset_index()

    return stock_data

def clean_stock(df, ticker):
    #Remove Div and Stock split cols, bcoz Adjusted Close and Close retreived
    df = df.drop(columns=["Dividends", "Stock Splits"])

    # #add column
    df.insert(loc=1, column="stock", value=ticker)

    df = df.rename(columns={"Date": "date", "Stock": "stock", "Open": "open", "High" : "high", "Low" : "low","Close": "close", "Adj Close": "adj_close", "Volume": "volume"})

    # df.insert(loc=1, column="Stock", value="RELIANCE.NS") insert column

    # conversion of date column to datetime formatted string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    #date starting 1st Jan 2000
    df = df[df["date"] >= "2000-01-01"]

    #remove index
    df = df.reset_index(drop=True)


    print(df)


if __name__ == "__main__":
   main()
   