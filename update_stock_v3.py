update_stock_v2.py


import sqlite3
import yfinance as yf
import time

# SQLite 데이터베이스 연결
conn = sqlite3.connect('stocks.db')

#table이 없으면 테이블 생성해서 주가 업데이트
if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=stocks").fetchone():
    conn.execute("""CREATE TABLE "stocks" (
    "symbol" TEXT,
    "date" DATE,
    "open" REAL,
    "high" REAL,
    "low" REAL,
    "close" REAL,
    "volume" INTEGER,
    "dividends" REAL,
    "stock_splits" TEXT,
    PRIMARY KEY("symbol","date"))""")
    conn.commit()

else:
    for name in ['AAPL','MSFT']:
      print (name)
      rec = yf.Ticker(name)
      rec_h = rec.history(start='2023-01-01',end='2023-12-31')
      for idx, row in rec_h.iterrows():
        cursor = conn.cursor()
        #중복인 symbol과 date가 있으면 업데이트 생략
        cursor.execute("INSERT OR IGNORE INTO stocks (symbol, date, open, high, low, close, volume, dividends, stock_splits) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, idx.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Volume'], row['Dividends'], row['Stock Splits'] ))
        conn.commit()

# SQLite 연결 종료
conn.close()
