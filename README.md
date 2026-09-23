# Stock Price Tracer

股票價格追蹤系統，第一階段以 **台灣市場與美國市場**為主，提供股票價格查詢，後續擴充技術指標、K 線、成交量、振幅與快取等功能。

---

## 1. 專案目標

建立一個具備以下能力的股票價格追蹤系統：

* 支援台灣股票市場
* 支援美國股票市場
* 透過 `Market` 指定市場
* 透過 `Symbol` 指定股票代號
* 自動轉換成資料來源所需的 `Ticker`
* 股票即時/歷史價格查詢
* OHLCV 資料取得
* 成交量顯示
* 技術指標計算
* 振幅計算
* SQLite 資料儲存
* Cache 快取
* API Route
* 前端顯示模式與時間範圍選擇
* 使用 Functional Programming（FP）方式設計核心邏輯

---

# 2. 系統架構

```text
                        ┌─────────────────────┐
                        │      Frontend       │
                        │     Streamlit       │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │      API Route      │
                        │   /stocks /health   │
                        └──────────┬──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │       Service       │
                        │   Stock Service     │
                        └──────┬───────┬──────┘
                               │       │
                  ┌────────────┘       └────────────┐
                  ▼                                 ▼
          ┌───────────────┐                 ┌───────────────┐
          │     Cache     │                 │    Provider   │
          │ Stock Cache   │                 │ Yahoo Finance │
          └───────┬───────┘                 └───────┬───────┘
                  │                                  │
                  │ Cache Hit                        │ Cache Miss
                  │                                  ▼
                  │                         ┌─────────────────┐
                  │                         │   Market Data   │
                  │                         │     OHLCV       │
                  │                         └────────┬────────┘
                  │                                  │
                  └──────────────────┬───────────────┘
                                     ▼
                           ┌─────────────────────┐
                           │       SQLite        │
                           │  Repository / View  │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │   Domain Functions  │
                           │ Indicators / Logic  │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │      Response       │
                           └─────────────────────┘
```

---

# 3. Functional Programming 設計

本專案核心邏輯採用 **Functional Programming（FP）** 思維。

核心原則：

1. 純函數優先
2. 函數輸入明確
3. 函數輸出明確
4. 避免全域狀態
5. 將 API、資料庫、Cache 等 I/O 與核心邏輯分離
6. Domain Logic 不直接依賴資料庫或外部 API

例如：

```text
Market + Symbol
        │
        ▼
    Ticker
```

這個轉換應該是一個純函數：

```python
def build_ticker(market, symbol):
    ...
```

而不是讓 `build_ticker()` 自己去呼叫 Yahoo Finance 或 SQLite。

---

# 4. Market / Symbol / Ticker

系統使用三個不同概念：

| 變數       | 說明         | 範例                |
| -------- | ---------- | ----------------- |
| `Market` | 市場         | `TW`, `US`        |
| `Symbol` | 使用者輸入的股票代號 | `2330`, `AAPL`    |
| `Ticker` | 資料來源實際查詢代號 | `2330.TW`, `AAPL` |

例如：

```text
Market = TW
Symbol = 2330
        │
        ▼
Ticker = 2330.TW
```

或：

```text
Market = US
Symbol = AAPL
        │
        ▼
Ticker = AAPL
```

市場由 `Market` 控制，而不是透過 `Symbol` 猜測市場。

---

# 5. 專案目錄

```text
StockPriceTracer/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── market.py
│   │   ├── stock.py
│   │   └── indicators.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── stocks.py
│   │       └── health.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── schema.py
│   │   ├── repository.py
│   │   └── views.py
│   │
│   ├── cache/
│   │   ├── __init__.py
│   │   └── stock_cache.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── stock_service.py
│   │
│   └── providers/
│       ├── __init__.py
│       └── yahoo_finance.py
│
├── tests/
│   ├── test_market.py
│   ├── test_stock.py
│   ├── test_indicators.py
│   └── test_cache.py
│
├── data/
│   └── .gitkeep
│
├── notebooks/
│   └── .gitkeep
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 6. 各模組職責

## `app/config/`

負責系統設定。

### `settings.py`

集中管理：

* SQLite 路徑
* Cache 設定
* API 設定
* 預設市場
* 其他環境設定

---

## `app/domain/`

系統核心商業邏輯。

這一層應盡量保持純函數，不直接處理：

* HTTP
* SQLite
* Yahoo Finance
* Cache
* Streamlit

### `market.py`

負責：

* Market 驗證
* Symbol 驗證
* Market + Symbol → Ticker
* 市場相關轉換

---

### `stock.py`

負責股票資料的 Domain Model，例如：

* 股票基本資料
* OHLCV 結構
* 股票查詢結果

---

### `indicators.py`

負責技術指標計算，例如：

* 漲跌幅
* 振幅
* 成交量
* 移動平均線
* 其他技術指標

所有計算盡量設計成：

```text
Input Data
    │
    ▼
Pure Function
    │
    ▼
Calculated Data
```

---

# 7. Provider

```text
app/providers/
└── yahoo_finance.py
```

Provider 負責與外部資料來源溝通。

目前第一階段使用：

```text
Yahoo Finance
```

Provider 的主要責任：

```text
Ticker
  │
  ▼
Yahoo Finance
  │
  ▼
Raw Market Data
```

Provider 不負責：

* 技術指標計算
* 前端顯示
* Cache 決策
* API Route
* SQLite View

這樣未來可以替換資料來源，而不需要修改 Domain Logic。

---

# 8. Service

```text
app/services/
└── stock_service.py
```

Service 負責協調系統各模組。

例如股票查詢流程：

```text
Market
   +
Symbol
   │
   ▼
build_ticker()
   │
   ▼
Cache
   │
   ├── Hit ───────► 回傳資料
   │
   └── Miss
          │
          ▼
       Provider
          │
          ▼
       SQLite
          │
          ▼
        Cache
          │
          ▼
       回傳資料
```

Service 是「流程協調者」，而不是存放所有商業邏輯的地方。

---

# 9. Cache

```text
app/cache/
└── stock_cache.py
```

Cache 用來減少重複查詢外部資料來源。

基本流程：

```text
Request
   │
   ▼
Check Cache
   │
   ├── Cache Hit
   │      │
   │      ▼
   │    Return
   │
   └── Cache Miss
          │
          ▼
       Provider
          │
          ▼
        SQLite
          │
          ▼
        Cache
          │
          ▼
        Return
```

Cache 本身不負責計算技術指標。

---

# 10. SQLite Database

```text
app/database/
├── connection.py
├── schema.py
├── repository.py
└── views.py
```

## `connection.py`

負責：

* 建立 SQLite Connection
* 管理 Connection Lifecycle
* Database 路徑

---

## `schema.py`

負責建立資料表與 Index。

例如：

```text
stocks
stock_prices
```

未來可依需求增加其他資料表。

---

## `repository.py`

負責資料庫 CRUD。

例如：

```text
save_stock()
get_stock()
save_pric_
```
