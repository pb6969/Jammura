import pandas as pd
import yfinance as yf

print("HELLO USER")
ticker = input("Enter the ticker for stock (use NSE tickers like RELIANCE.NS): ")

year = int(input("Enter Year : "))
month = int(input("Enter Month : "))
date = int(input("Enter Date : "))


start_date = date - 10
start_month = month
start_year = year

if start_date <= 0:
    start_date = 31 + start_date
    if start_month == 1:
        start_month = 12
        start_year -= 1
    else:
        start_month -= 1

sdate = f"{start_year}-{start_month}-{start_date}"
t_day = f"{year}-{month}-{date}"

print(f"Fetching data from {sdate} to {t_day}...")


data = yf.download(ticker.upper(), sdate, t_day)


if data.empty:
    print(f" No data found for {ticker.upper()} between {sdate} and {t_day}.")
    print("Make sure you are using a valid NSE ticker, e.g., RELIANCE.NS, TCS.NS, INFY.NS")
    exit()


if isinstance(data.columns, pd.MultiIndex):
    data.columns = [col[0] for col in data.columns]


for col in ['Open', 'High', 'Low', 'Close']:
    data[col] = pd.to_numeric(data[col], errors='coerce')

data = data.dropna()

if data.empty:
    print("After cleaning, no valid numeric data available. Try another ticker/date.")
    exit()


close_price = list(data['Close'])

uptrend = sum(close_price[i+1] > close_price[i] for i in range(len(close_price)-1))
downtrend = sum(close_price[i+1] < close_price[i] for i in range(len(close_price)-1))

if uptrend > downtrend:
    trend = 'uptrend'
elif downtrend > uptrend:
    trend = 'downtrend'
else:
    trend = 'sideways'

print("Initial Trend:", trend)


high = list(data['High'])
low = list(data['Low'])
open_ = list(data['Open'])
close = list(data['Close'])

diff_high_low = high[-1] - low[-1]
diff_close_open = abs(close[-1] - open_[-1])
partition = (diff_close_open / diff_high_low) * 100 if diff_high_low != 0 else 0

print("Partition:", partition)

Bullish, Bearish, Sideways = [], [], []

if trend != 'sideways':  
    if partition < 40:
        if close[-1] > open_[-1]:  
            if high[-1] - close[-1] > open_[-1] - low[-1]:
                if trend == "downtrend":
                    Bearish.append(ticker.upper())
                elif trend == "uptrend":
                    Bearish.append(ticker.upper())
            elif high[-1] - close[-1] < open_[-1] - low[-1]:
                if trend == "uptrend":
                    Bullish.append(ticker.upper())
                elif trend == "downtrend":
                    Bullish.append(ticker.upper())
            else:
                Sideways.append(ticker.upper())
        else:  
            if high[-1] - open_[-1] > close[-1] - low[-1]:
                if trend == "downtrend":
                    Bearish.append(ticker.upper())
                elif trend == "uptrend":
                    Bearish.append(ticker.upper())
            elif high[-1] - open_[-1] < close[-1] - low[-1]:
                if trend == "uptrend":
                    Bullish.append(ticker.upper())
                elif trend == "downtrend":
                    Bullish.append(ticker.upper())
            else:
                Sideways.append(ticker.upper())

    elif partition > 40:
        if close[-1] > open_[-1]: 
            if high[-1] - close[-1] > open_[-1] - low[-1]:
                if close[-1] - open_[-1] >= high[-1] - close[-1]:
                    if trend == "uptrend":
                        Bullish.append(ticker.upper())
                    elif trend == "downtrend":
                        Bullish.append(ticker.upper())
                else:
                    if trend == "downtrend":
                        Bearish.append(ticker.upper())
                    elif trend == "uptrend":
                        Bearish.append(ticker.upper())
            elif high[-1] - close[-1] < open_[-1] - low[-1]:
                if trend == "uptrend":
                    Bullish.append(ticker.upper())
                elif trend == "downtrend":
                    Bullish.append(ticker.upper())
            else:
                if close[-1] - open_[-1] > max(high[-1]-close[-1], open_[-1]-low[-1]):
                    if trend == "uptrend":
                        Bullish.append(ticker.upper())
                    elif trend == "downtrend":
                        Bullish.append(ticker.upper())
                else:
                    Sideways.append(ticker.upper())

        else: 
            if high[-1] - open_[-1] > close[-1] - low[-1]:
                if open_[-1] - close[-1] > high[-1] - open_[-1]:
                    if trend == "downtrend":
                        Bearish.append(ticker.upper())
                    elif trend == "uptrend":
                        Bearish.append(ticker.upper())
                else:
                    if trend == "downtrend":
                        Bearish.append(ticker.upper())
                    elif trend == "uptrend":
                        Bearish.append(ticker.upper())
            elif high[-1] - open_[-1] < close[-1] - low[-1]:
                if open_[-1] - close[-1] >= close[-1] - low[-1]:
                    if trend == "downtrend":
                        Bearish.append(ticker.upper())
                    elif trend == "uptrend":
                        Bearish.append(ticker.upper())
                else:
                    if trend == "uptrend":
                        Bullish.append(ticker.upper())
                    elif trend == "downtrend":
                        Bullish.append(ticker.upper())
            else:
                if open_[-1] - close[-1] > max(high[-1]-open_[-1], close[-1]-low[-1]):
                    if trend == "downtrend":
                        Bearish.append(ticker.upper())
                    elif trend == "uptrend":
                        Bearish.append(ticker.upper())
                else:
                    Sideways.append(ticker.upper())
else:
    Sideways.append(ticker.upper())



if Bullish:
    print(f"{ticker.upper()} Will be Bullish")
elif Bearish:
    print(f"{ticker.upper()} Will be Bearish")
elif Sideways:
    print(f"{ticker.upper()} Will be Sideways. So do not BUY it")
