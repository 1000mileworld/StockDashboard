import pandas as pd
import yfinance as yf #pip install yfinance --upgrade --no-cache-dir (try this if not working)
import asyncio

def saveSP500():
    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    df.to_csv('SP500.csv')

def loadSP500():
    df = pd.read_csv('SP500.csv')
    ticker = df['Symbol'].tolist()
    company = df['Security'].tolist()
    return ticker,company

def validateInput(input,ticker,company):
    #company list should be alphabetized, ticker not necessarily
    isValid = False
    convertedTicker = "N/A"
    convertedCompany = "N/A"

    if input.upper() in ticker:
        isValid = True
        convertedTicker = input.upper()
        convertedCompany = company[ticker.index(input.upper())]
    elif input.title() in company: #captalize first letter of each word
        isValid = True
        convertedCompany = input.title()
        convertedTicker = ticker[company.index(input.title())]
    
    return isValid, convertedTicker, convertedCompany  

def getYF_data(symbol):
    df = yf.download(symbol, period="1y", auto_adjust=True, prepost=True, threads=True, progress=False)
    low = df['Low'].min()
    high = df['High'].max()
    open = df['Open'][-1]
    close = df['Close'][-1]
    return low, high, open, close  

def getHistorical(symbol,lookback):
    if lookback=='realTime': return [], []

    df = yf.download(symbol, period=lookback, auto_adjust=True, prepost=True, threads=True, progress=False)
    df['time'] = pd.to_datetime(df.index)
    df['dates'] = df['time'].dt.date
    x_val = [date.strftime("%Y-%m-%d") for date in df['dates']]
    #y_val = list(df['Close'])
    y_val = [round(price,2) for price in df['Close']]

    return x_val, y_val