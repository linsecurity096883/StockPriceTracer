import streamlit
import yfinance as yf
import pandas as pd
import numpy as np
import plotly
def test_packages():
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
        return "\n🎉 所有套件載入成功！",True
    else:
        return "\n⚠️ 有套件載入失敗，請檢查上方錯誤資訊。",False