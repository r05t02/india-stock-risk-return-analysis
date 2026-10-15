import yfinance as yf
import pandas as pd

RELIANCE = yf.Ticker("RELIANCE.NS")
print("\n")

rel_data = RELIANCE.history(period="max", auto_adjust=False) #pandas df

rel_data = rel_data.reset_index()
# print(rel_data)

# conversion of date column to datetime formatted string
rel_data["Date"] = rel_data["Date"].dt.strftime("%Y-%m-%d")
#1. rel_data["Date"] = pd.to_datetime(rel_data["Date"])
#2. rel_data["Date"] = rel_data["Date"].dt.date("%Y-%m-%d")


#Printing the Stock symbol along the Stock Data
rel_data.insert(loc=1, column="Stock", value="RELIANCE.NS")

#date starting 1st Jan 2000
rel_data = rel_data[rel_data["Date"] >= "2000-01-01"]

#Remove Div and Stock split cols, bcoz Adjusted Close and Close retreived
rel_data = rel_data.drop(columns=["Dividends", "Stock Splits"])

# print(rel_data.head().to_string(index=False))
# print(rel_data.info())


# Sumamry Statistics
# print(rel_data.describe())


## To check the trading days where colume is equal to 0
# rel_data = rel_data[rel_data["Volume"] <= 0 ]
# print(rel_data)

print(type(rel_data.head().to_string(index=False))) #---prints out the data in string format#



with open("rel_stock_data.csv", "w") as file:
    file.write("hello")








