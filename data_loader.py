import yfinance as yf
import pandas as pd

def load_data(symbol, period="5y"):
    """
    ดึงข้อมูลราคาหุ้นจาก Yahoo Finance
    symbol = ชื่อหุ้น เช่น 'AAPL'
    period = ระยะเวลา เช่น '1y', '5y', 'max'
    """

    df = yf.download(symbol, period=period)

    # แก้ MultiIndex → SingleIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    df.dropna(inplace=True)
    return df