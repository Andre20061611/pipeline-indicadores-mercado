import requests

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
params = {
    "formato": "json",
    "dataInicial": "31/10/2021",
    "dataFinal": "31/10/2026",
}

resposta = requests.get(URL, params=params)
resposta.raise_for_status()
dados = resposta.json()

print(len(dados))
print(dados[0])
print(dados[-1])