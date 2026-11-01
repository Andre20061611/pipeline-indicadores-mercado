import requests
import pandas as pd
from pathlib import Path
from datetime import date

RAIZ = Path(__file__).resolve().parent.parent
pasta_data = RAIZ / "data"
pasta_data.mkdir(exist_ok=True)
arquivo = pasta_data / "ipca.csv"

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
hoje = date.today()

# 1. Descobre de onde começar (IPCA é mensal: próximo mês)
existente = None
ultima = None
if arquivo.exists() and arquivo.stat().st_size > 0:
    existente = pd.read_csv(arquivo, parse_dates=["data"])
    ultima = existente["data"].max()
    inicio = (ultima + pd.DateOffset(months=1)).date()
    print("Última data no arquivo:", ultima.date())
else:
    inicio = date(2021, 10, 31)
    print("Arquivo não existe ou está vazio: carga completa")

if inicio > hoje:
    print("Já está atualizado.")
    raise SystemExit

# 2. Pede só o período que falta
params = {
    "formato": "json",
    "dataInicial": inicio.strftime("%d/%m/%Y"),
    "dataFinal": hoje.strftime("%d/%m/%Y"),
}
resposta = requests.get(URL, params=params)
if resposta.status_code == 404:
    print("Nenhum dado novo publicado pelo Banco Central.")
    raise SystemExit
resposta.raise_for_status()
dados = resposta.json()

if not dados:
    print("Nenhum dado novo publicado pelo Banco Central.")
    raise SystemExit

# 3. Converte os tipos
novos = pd.DataFrame(dados)
novos["data"] = pd.to_datetime(novos["data"], format="%d/%m/%Y")
novos["valor"] = novos["valor"].astype(float)

# só o que é depois da última data do arquivo
if ultima is not None:
    novos = novos[novos["data"] > ultima]
if novos.empty:
    print("Nenhum dado novo publicado pelo Banco Central.")
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