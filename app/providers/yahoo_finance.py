import yfinance as yf
ticker = input()
market = ".TW"
if market == ".TW":
    ticker = ticker+market
def get_stock_history(ticker):
    symbol = yf.Ticker(ticker)
    return symbol.history(period="max")
data = get_stock_history(ticker)
print(data)