import yfinance as yf
def check_packages():
    packages = {
        "Streamlit": "streamlit",
        "yfinance": "yfinance",
        "Pandas": "pandas",
        "NumPy": "numpy",
        "Plotly": "plotly"
    }

    all_success = True

    for name, module_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, "__version__", "未知版本")
            print(f"✅ {name}: {version}")

        except ImportError as e:
            print(f"❌ {name}: 載入失敗")
            print(f"   錯誤：{e}")
            all_success = False

    if all_success:
        return True
    else:
        return False

def check_yfinance_connection(ticker: str = "0050.TW") -> bool:
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
def system_health_ok():
    test_packages_ok = check_packages()
    test_yfinance_connection_ok = check_yfinance_connection()
    if test_packages_ok and test_yfinance_connection_ok:
        print("Stock Price Tracer 系統正常")
        return True
    else:
        print("Stock Price Tracer 系統錯誤")
        return False

def system_boot_check():
    system_boot_ok = system_health_ok()
    if system_boot_ok:
        print("啟動成功")