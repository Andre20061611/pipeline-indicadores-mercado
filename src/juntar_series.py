import pandas as pd
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
pasta_data = RAIZ / "data"

cdi = pd.read_csv(pasta_data / "cdi.csv", parse_dates=["data"]).rename(columns={"valor": "cdi"})
dolar = pd.read_csv(pasta_data / "dolar.csv", parse_dates=["data"]).rename(columns={"valor": "dolar"})
ibov = pd.read_csv(pasta_data / "ibovespa.csv", parse_dates=["data"]).rename(columns={"valor": "ibovespa"})

print("cdi:", len(cdi), "dolar:", len(dolar), "ibovespa:", len(ibov))

base = cdi.merge(dolar, on="data", how="outer").merge(ibov, on="data", how="outer")
base = base.sort_values("data").reset_index(drop=True)

print("linhas da base:", len(base))
print(base.isna().sum())
print(base[base.isna().any(axis=1)])

base.to_csv(pasta_data / "base_diaria.csv", index=False)