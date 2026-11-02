import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
pasta_data = RAIZ / "data"

INICIO = pd.Timestamp("2021-11-01")
FIM = pd.Timestamp("2026-09-30")
CAPITAL = 1000

st.set_page_config(page_title="Indicadores de Mercado", layout="wide")
st.title("Quanto R$ 1.000 viraram desde novembro de 2021?")

# 1. Lê os dados do pipeline
base = pd.read_csv(pasta_data / "base_diaria.csv", parse_dates=["data"])
ipca = pd.read_csv(pasta_data / "ipca.csv", parse_dates=["data"])

base = base[(base["data"] >= INICIO) & (base["data"] <= FIM)].reset_index(drop=True)

# 2. CDI: compõe a taxa diária
cdi = base[["data", "cdi"]].dropna()
cdi["valor"] = CAPITAL * (1 + cdi["cdi"] / 100).cumprod()

# 3. Dólar: quantos dólares R$ 1.000 compravam no primeiro dia
dolar = base[["data", "dolar"]].dropna()
dolares = CAPITAL / dolar["dolar"].iloc[0]
dolar["valor"] = dolares * dolar["dolar"]

# 4. IPCA: degrau no último dia de cada mês, de novembro de 2021 até setembro de 2026
ipca = ipca[ipca["data"] >= INICIO].copy()
ipca["data"] = ipca["data"] + pd.offsets.MonthEnd(0)
ipca = ipca[ipca["data"] <= FIM].copy()
ipca["valor"] = CAPITAL * (1 + ipca["valor"] / 100).cumprod()

# 5. Gráfico principal
fig = go.Figure()
fig.add_trace(go.Scatter(x=cdi["data"], y=cdi["valor"], name="CDI"))
fig.add_trace(go.Scatter(x=dolar["data"], y=dolar["valor"], name="Dólar"))
fig.add_trace(go.Scatter(x=ipca["data"], y=ipca["valor"], name="IPCA", line_shape="hv"))
fig.update_layout(yaxis_title="R$", legend_title="Série")
st.plotly_chart(fig, use_container_width=True)

# 6. Valor final e porcentagem de cada série
colunas = st.columns(3)
for coluna, nome, serie in zip(colunas, ["CDI", "Dólar", "IPCA"], [cdi, dolar, ipca]):
    final = serie["valor"].iloc[-1]
    variacao = (final / CAPITAL - 1) * 100
    coluna.metric(nome, f"R$ {final:,.2f}")
    coluna.caption(f"rendeu {variacao:.1f}% até {serie['data'].iloc[-1].date()}")

# 7. Ibovespa à parte, só como referência
st.subheader("Para conhecer: Ibovespa (pontos)")
ibov = base[["data", "ibovespa"]].dropna()
fig2 = go.Figure(go.Scatter(x=ibov["data"], y=ibov["ibovespa"], name="Ibovespa"))
fig2.update_layout(yaxis_title="pontos")
st.plotly_chart(fig2, use_container_width=True)