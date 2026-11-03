import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
pasta_data = RAIZ / "data"

INICIO = pd.Timestamp("2021-11-01")
FIM = pd.Timestamp("2026-09-30")
CAPITAL = 1000

CORES = {
    "CDI": "#E3C675",
    "Dólar": "#7FA6D9",
    "IPCA": "#FFFFFF",
    "Ibovespa": "#7BC4B5",
}
GRADE = "#2A3B57"
CINZA = "#8A97AD"
FUNDO_CAIXA = "rgba(43, 48, 60, 0.92)"
BORDA_CAIXA = "#4A5568"

st.set_page_config(page_title="Indicadores de Mercado", layout="wide")

# Visual: esconde o menu do Streamlit e reduz o espaço no topo
st.markdown(
    """
    <style>
    [data-testid="stToolbar"], [data-testid="stDeployButton"], #MainMenu {display: none;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


def brl(valor):
    """Formata como moeda brasileira: R$ 1.803,82"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(valor):
    """Formata variação com sinal e vírgula: +80,4%"""
    return f"{valor:+.1f}%".replace(".", ",")


st.title("Quanto R$ 1.000 viraram desde novembro de 2021?")
st.caption(
    "Comparação entre CDI, dólar e inflação (IPCA), partindo de R$ 1.000 em 01/11/2021."
)

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


def estilo(figura, prefixo=""):
    figura.update_layout(
        separators=",.",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#FFFFFF",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=FUNDO_CAIXA,
            bordercolor=BORDA_CAIXA,
            font=dict(color="#FFFFFF", size=13),
        ),
        legend=dict(orientation="h", y=1.12, x=0, title_text=""),
        margin=dict(l=0, r=0, t=30, b=0),
    )
    figura.update_xaxes(
        gridcolor=GRADE,
        tickformat="%m/%Y",
        hoverformat="%d/%m/%Y",
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikecolor=CINZA,
        spikethickness=-2,
        spikedash="dot",
    )
    figura.update_yaxes(gridcolor=GRADE, tickprefix=prefixo, tickformat=",.0f")


# 5. Gráfico principal
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=cdi["data"],
        y=cdi["valor"],
        name="CDI",
        line=dict(color=CORES["CDI"]),
        hovertemplate="R$ %{y:,.2f}",
    )
)
fig.add_trace(
    go.Scatter(
        x=dolar["data"],
        y=dolar["valor"],
        name="Dólar",
        line=dict(color=CORES["Dólar"]),
        hovertemplate="R$ %{y:,.2f}",
    )
)
fig.add_trace(
    go.Scatter(
        x=ipca["data"],
        y=ipca["valor"],
        name="Inflação (IPCA)",
        line=dict(color=CORES["IPCA"], shape="hv"),
        hovertemplate="R$ %{y:,.2f}",
    )
)
fig.add_hline(
    y=CAPITAL,
    line_dash="dot",
    line_color=CINZA,
    annotation_text="R$ 1.000 investidos",
    annotation_position="bottom left",
    annotation_font_color=CINZA,
)
estilo(fig, prefixo="R$ ")
st.plotly_chart(fig, use_container_width=True, theme=None)

# 6. Valor final de cada série, com a variação no período
cartoes = [
    (
        "CDI (100% do CDI)",
        cdi,
        "normal",
        "R$ 1.000 aplicados a 100% do CDI, com juros compostos dia a dia.",
    ),
    (
        "Dólar",
        dolar,
        "normal",
        "Quanto valeriam, em reais, os dólares que R$ 1.000 compravam em 01/11/2021.",
    ),
    (
        "Inflação (IPCA)",
        ipca,
        "off",
        "Quanto R$ 1.000 precisariam virar para manter o poder de compra. "
        "Quando o CDI fica acima desse valor, houve ganho real.",
    ),
]

colunas = st.columns(3)
for coluna, (nome, serie, cor_delta, ajuda) in zip(colunas, cartoes):
    final = serie["valor"].iloc[-1]
    variacao = (final / CAPITAL - 1) * 100
    data_final = serie["data"].iloc[-1].strftime("%d/%m/%Y")
    coluna.metric(
        nome,
        brl(final),
        delta=pct(variacao),
        delta_color=cor_delta,
        help=ajuda,
    )
    coluna.caption(f"Posição em {data_final}")

# 7. Ibovespa à parte, só como referência
st.subheader("Para conhecer: Ibovespa")
st.caption(
    "Índice das ações mais negociadas da B3, medido em pontos. "
    "Por não ser um valor em reais, fica separado dos gráficos acima."
)
ibov = base[["data", "ibovespa"]].dropna()

fig2 = go.Figure(
    go.Scatter(
        x=ibov["data"],
        y=ibov["ibovespa"],
        name="Ibovespa",
        line=dict(color=CORES["Ibovespa"]),
        hovertemplate="%{y:,.0f} pontos",
    )
)
estilo(fig2)
fig2.update_layout(showlegend=False)
st.plotly_chart(fig2, use_container_width=True, theme=None)

# 8. Rodapé com fontes e aviso
st.divider()
st.caption(
    "Fontes: Banco Central do Brasil (CDI, IPCA e dólar PTAX venda) e Yahoo Finance (Ibovespa). "
    "Período: 01/11/2021 a 30/09/2026. Valores brutos, antes de impostos e taxas. "
    "O desempenho passado não garante resultados futuros."
)