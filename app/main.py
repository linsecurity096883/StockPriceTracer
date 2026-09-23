import streamlit
import yfinance as yf
import pandas as pd
import numpy as np
import plotly
from tests.test_packages import test_packages
from tests.test_yahoo_finance import test_yfinance_connection
def main():
    test_packages_ok = test_packages()
    test_yfinance_connection_ok = test_yfinance_connection()
    if test_packages_ok and test_yfinance_connection_ok:
        print("Stock Price Tracer 啟動成功")
    else:
        print("Stock Price Tracer 啟動失敗")

if __name__ == "__main__":
    main()

