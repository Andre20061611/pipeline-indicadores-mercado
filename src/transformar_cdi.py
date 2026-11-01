import requests
import os
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
params = {
    "formato": "json",
    "dataInicial": "31/10/2021",
    "dataFinal": "31/10/2026",
}

dados = requests.get(URL, params=params).json()
df = pd.DataFrame(dados)

print(df.dtypes)

df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
df["valor"] = df["valor"].astype(float)

print(df.dtypes)
print(df.head())
os.makedirs("data", exist_ok=True)
df.to_csv("data/cdi.csv", index=False)