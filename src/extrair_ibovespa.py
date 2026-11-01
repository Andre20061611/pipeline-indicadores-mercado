import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

RAIZ = Path(__file__).resolve().parent.parent
pasta_data = RAIZ / "data"
pasta_data.mkdir(exist_ok=True)
arquivo = pasta_data / "ibovespa.csv"

hoje = date.today()

# 1. Descobre de onde começar
existente = None
if arquivo.exists() and arquivo.stat().st_size > 0:
    existente = pd.read_csv(arquivo, parse_dates=["data"])
    ultima = existente["data"].max().date()
    inicio = ultima + timedelta(days=1)
    print("Última data no arquivo:", ultima)
else:
    inicio = date(2021, 10, 31)
    print("Arquivo não existe ou está vazio: carga completa")

if inicio > hoje:
    print("Já está atualizado.")
    raise SystemExit

# 2. Pede só o período que falta (o end do yfinance é exclusivo)
fim = hoje + timedelta(days=1)
df = yf.Ticker("^BVSP").history(start=inicio.isoformat(), end=fim.isoformat())

if df.empty:
    print("Nenhum dado novo publicado pelo Yahoo Finance.")
    raise SystemExit

# 3. Converte os tipos
df = df.reset_index()
df["data"] = pd.to_datetime(df["Date"]).dt.tz_localize(None).dt.normalize()
df["valor"] = df["Close"].astype(float)
novos = df[["data", "valor"]]
if existente is not None:
    novos = novos[novos["data"] > pd.Timestamp(ultima)]
if novos.empty:
    print("Nenhum dado novo publicado pelo Yahoo Finance.")
    raise SystemExit
print("Registros novos:", len(novos))

# 4. Junta com o que já existia, sem duplicar datas
if existente is not None:
    base = pd.concat([existente, novos])
else:
    base = novos

base = base.drop_duplicates(subset="data").sort_values("data").reset_index(drop=True)
base.to_csv(arquivo, index=False)
print("Total no arquivo:", len(base))
print(base.tail())