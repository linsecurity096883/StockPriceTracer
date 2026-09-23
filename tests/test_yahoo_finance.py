import yfinance as yf


def test_yfinance_connection(ticker: str = "0050.TW") -> bool:
    try:
        data = yf.Ticker(ticker).history(period="5d")

        if data.empty:
            print(f"❌ yfinance 連線失敗")
            return False

        print(f"✅ yfinance 連線成功")

        return True

    except Exception as error:
        print(f"❌ yfinance 連線失敗")
        print(f"   錯誤：{error}")

        return False