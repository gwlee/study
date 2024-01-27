import sqlite3
import yfinance as yf
import time

# SQLite 데이터베이스 연결
conn = sqlite3.connect('stocks.db')

for name in ['AAPL','MSFT']:
  print (name)
  rec = yf.Ticker(name)
  rec_h = rec.history(start='2024-01-20',end='2024-01-27')
  for idx, row in rec_h.iterrows():
    cursor = conn.cursor()
    cursor.execute("INSERT INTO stock_prices (symbol, date, open, high, low, close, adj_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name, idx.strftime('%Y-%m-%d'), row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']))            
    conn.commit()

# SQLite 연결 종료
conn.close()
