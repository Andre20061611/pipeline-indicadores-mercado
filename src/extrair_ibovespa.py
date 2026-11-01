import yfinance as yf
import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

ibov = yf.Ticker("^BVSP")
df = ibov.history(start="2021-10-31", end="2026-11-01")

df = df.reset_index()
df["data"] = pd.to_datetime(df["Date"]).dt.tz_localize(None).dt.normalize()
df["valor"] = df["Close"].astype(float)
df = df[["data", "valor"]]

print(df.dtypes)
print(df.head())
print(df.tail())
print(len(df))

pasta_data = RAIZ / "data"
pasta_data.mkdir(exist_ok=True)
df.to_csv(pasta_data / "ibovespa.csv", index=False)