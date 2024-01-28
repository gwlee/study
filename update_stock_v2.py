import sqlite3
import yfinance as yf
import time

# SQLite 데이터베이스 연결
conn = sqlite3.connect('stocks.db')

#table이 없으면 테이블 생성해서 주가 업데이트
if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=stock_prices").fetchone():
    conn.execute("""CREATE TABLE "stock_prices" (
    "symbol" TEXT,
    "date" DATE,
    "open" REAL,
    "high" REAL,
    "low" REAL,
    "close" REAL,
    "adj_close" REAL,
    "volume" INTEGER)""")
    conn.commit()

else:
    for name in ['AAPL','MSFT']:
      print (name)
      rec = yf.Ticker(name)
      rec_h = rec.history(start='2023-01-01',end='2023-12-31')
      for idx, row in rec_h.iterrows():
        cursor = conn.cursor()
        cursor.execute("INSERT INTO stock_prices (symbol, date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, idx.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))            
        conn.commit()

# SQLite 연결 종료
conn.close()
