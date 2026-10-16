import yfinance as yf
import pandas as pd



START_DATE = "2000-01-01"

TICKERS = [
    "ICICIBANK.NS",  # ICICI Bank
    "HDFCBANK.NS",   # HDFC Bank
    "TCS.NS",        # Tata Consultancy Services
    "LT.NS",         # Larsen & Toubro
    "ITC.NS"         # ITC Limited 
    ]



def main():
    all_df = []

    for stock in TICKERS:
        raw_dataframe = fetch_stock_df(stock)

        if raw_dataframe is None:
            print(f"{stock} failed")
            continue

        try:
            cleaned_df = clean_stock(raw_dataframe, stock)
        except Exception as e:
            print(f"Cleaning failure for {stock} : {e}")
            continue

        if validate(cleaned_df, stock) is False:
            continue

    
        all_df.append(cleaned_df)

        #Summary line
        print(f"{stock:<12} | Rows: {len(cleaned_df):>5} | Dates: {cleaned_df['date'].min()} to {cleaned_df['date'].max()}")

    #Check if no data fetched for any ticker
    if not all_df:
        print("No data fetched for any ticker")
        return None

    #if list not empty, convert list to a pandas dataframe
    final_df = pd.concat(all_df, ignore_index=True)

    
    ##TEST PRINTS
    # print(final_df.to_string(index=False))
    # print(final_df.head())
    # print(final_df)
    #print(final_df.shape())


    print(f"\nFinal Consolidated Shape: {final_df.shape[0]} rows x {final_df.shape[1]} columns")

    return final_df



def fetch_stock_df(stock):

    if not isinstance(stock, str) or not stock.strip():
        print(f"Invalid or blank ticker: '{stock}'")
        return None

    stock_obj = yf.Ticker(stock)

    try:
        stock_data_df = stock_obj.history(period="max", auto_adjust=False)
    except Exception as e:
        print(f"{e} occured. {stock} failure.")
        return None

    if stock_data_df.empty:
        print("EMPTY DATA FRAME")
        return None
        
    stock_data = stock_data_df.reset_index()

    return stock_data

def clean_stock(df, ticker):
    #Remove Div and Stock split cols, bcoz Adjusted Close and Close retreived
    df = df.drop(columns=["Dividends", "Stock Splits"],errors="ignore")

    # #add column
    df.insert(loc=1, column="stock", value=ticker)

    #rename df column headings to lowercase
    df = df.rename(columns={"Date": "date", "Open": "open", "High" : "high", "Low" : "low","Close": "close", "Adj Close": "adj_close", "Volume": "volume"})

    # conversion of date column to datetime formatted string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    #date starting 1st Jan 2000
    df = df[df["date"] >= START_DATE]

    #remove the last row, as data might contain unfinished trading days --- BUT this removes the last row, even if trading day has concluded.
    df = df.iloc[:-1]

    #remove index
    df = df.reset_index(drop=True)

    # print(df)
    return df



def validate(df, ticker):

    #Check if dataframe is empty
    if df.empty:
        print("EMPTY DATAFRAME")
        return False

    #Check for duplicated values
    if df["date"].duplicated().any():
        count_of_duplicates = df["date"].duplicated().sum()
        print(f"{ticker} has duplicates. duplicates: {count_of_duplicates}")
        return False


    price_columns = ["open", "high", "low", "close", "adj_close"]

    #Check for price values less than 0
    for cols in price_columns:
        if (df[cols] <= 0).any():
            print(f"In {ticker} columns, found non-postive values.")
            return False

    #Check for negative volume
    if (df["volume"] < 0).any() :
        print(f"For {ticker}, NEGATIVE VOLUME detected")
        return False

    #Check HIGH < LOW
    if (df["high"] < df["low"]).any():
        print(f"ERROR! High cannot be lower than low. [in {ticker} data]")
        return False

    #Check for NaN values
    if df[price_columns].isna().any().any():
        print(f"Nan values")
        return False

    # ------------------------------------------------------------------------#

    #Count number of rows where volume is 0
    volume_is_zero_rows = (df["volume"] == 0).sum()
    if volume_is_zero_rows > 0:
        print(f"{ticker}: {volume_is_zero_rows} trading days with 0 volume recorded.")

    
    #Count number of rows where: 1. HIGH < OPEN    2. HIGH < CLOSE
    #bitwise "or" to be used instead of or keyword
    high_below_open_or_close = ((df["high"] < df["open"]) | (df["high"] < df["close"])).sum()    
    if high_below_open_or_close > 0:
        print(f"[NOTE] {ticker}: {high_below_open_or_close} rows where High is below Open or Close.")

    return True
   

if __name__ == "__main__":
   main()
   