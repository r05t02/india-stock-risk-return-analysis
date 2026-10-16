import yfinance as yf
import pandas as pd

START_DATE = "2000-01-01"


tickers = [
    "ICICIBANK.NS",  # ICICI Bank
    "HDFCBANK.NS",   # HDFC Bank
    "TCS.NS",        # Tata Consultancy Services
    "LT.NS",         # Larsen & Toubro
    "ITC.NS"         # ITC Limited 
    ]

def main():
    all_df = []

    for stock in tickers:
        raw_dataframe = fetch_stock_df(stock)

        cleaned_df = clean_stock(raw_dataframe, stock)

        all_df.append(cleaned_df)

    final_df = pd.concat(all_df, ignore_index=True)


    ##TEST PRINTS
    # print(final_df.to_string(index=False))
    # print(final_df.head())
    print(final_df)

    return final_df



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

    df = df.rename(columns={"Date": "date", "Open": "open", "High" : "high", "Low" : "low","Close": "close", "Adj Close": "adj_close", "Volume": "volume"})

    # df.insert(loc=1, column="Stock", value="RELIANCE.NS") insert column

    # conversion of date column to datetime formatted string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    #date starting 1st Jan 2000
    df = df[df["date"] >= START_DATE]

    #remove index
    df = df.reset_index(drop=True)


    # print(df)
    return df


if __name__ == "__main__":
   main()
   