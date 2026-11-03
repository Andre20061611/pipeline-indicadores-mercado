# IA.md — Como usei IA neste projeto

> Relatório gerado pelo Claude a partir do histórico desta conversa. Reflete só o que aparece nela.
> O trabalho anterior (extração de CDI, IPCA e dólar, e as decisões 1 a 6 do README) aparece aqui apenas
> por código e texto colados, então não dá para avaliar como foi conduzido.
> Boa parte das minhas mensagens foi ditada por voz. Erros como "iFinance" e "SR6" vêm da transcrição.

## 1. Como fui direcionada

- **Nível de detalhe das instruções:** baixo. Minhas mensagens foram curtas e reativas, em geral
  "qual o próximo passo?", "como posso testar?", "não entendi". Quase nunca abri uma tarefa com uma
  especificação detalhada. A IA conduziu o passo a passo, e eu executei, testei e reportei.
- **Contexto e restrições:** dei em momentos pontuais, e foram eles que mais moldaram o resultado:
  - o README deve seguir o formato "o que decidi / por quê";
  - a ordem de trabalho: replicar a atualização incremental e deixar o dashboard por último;
  - o pipeline deve parar se uma etapa falhar;
  - o IPCA fica em tabela separada;
  - um princípio constante: não preencher nem inventar dados.
  Também li para a IA o trecho do enunciado do case sobre o dashboard.
- **Planos antes do código:** não pedi planos explicitamente. Em dois momentos (a junção das séries e o
  dashboard) a IA conduziu uma conversa de decisões antes de escrever o código, e eu respondi com meus
  motivos. Nos outros (extração do Ibovespa, incrementais, `atualizar_tudo.py`), o código veio primeiro e eu testei.
- **Previsões:** a IA pediu previsões antes de vários testes. Respondi algumas (contagem do Ibovespa: 1256,
  real 1248; junção: 8 vazios e cerca de 1256 linhas). Em outras, não registrei previsão (testes do dólar,
  do Ibovespa, do IPCA e do dashboard).
- **Verificação:** rodei os scripts, colei saídas e prints, e conferi fontes externas (Google Finanças, B3,
  API do Banco Central). Esse ciclo pegou erros meus: um `s` sobrando em `juntar_series.py`, o nome antigo do
  script do CDI em `atualizar_tudo.py` depois que renomeei, e a ausência do `requirements.txt`.
- **Pedidos de explicação e de ritmo:** perguntei o que são `yfinance`, pregão e `requirements.txt`, e pedi
  para ir mais devagar ("vamos devagar que eu não entendi").

## 2. Pedidos principais

1. **Validar o CSV do Ibovespa** ("Deu isso, está correto?", "Como posso testar?"). Resultado: formato e período
   corretos, 1248 registros, fechamento de 30/10/2026 conferido no Google Finanças (167.921,80) e na B3 (167.920),
   contra 167.922 no meu arquivo.
2. **Reescrever o README no formato de decisões, por perguntas e respostas com minhas palavras:** decisão 7
   (Ibovespa), 8 (junção), 9 a 11 (atualização incremental e parada do pipeline) e Limitações. Depois pedi o
   README inteiro atualizado a partir do texto que colei.
3. **Replicar a atualização incremental do CDI para dólar, Ibovespa e IPCA** e automatizar tudo com
   `atualizar_tudo.py`, deixando o dashboard por último.
4. **Definir o dashboard por perguntas** (pergunta principal, comparações, ferramenta) e gerar o código-base
   do `dashboard.py` em Streamlit com Plotly.
5. **Ajustar o visual do dashboard:** deixar mais discreto o traço vertical do cursor, como no Google Finance.
   Esse pedido terminou sem confirmação de que a solução funcionou.

## 3. Correções e questionamentos

Não houve rejeição forte de uma proposta técnica da IA. Os momentos abaixo são correções de fato,
questionamentos e pedidos de mudança de ritmo.

- **Formato do README:** quando a IA começou a propor seções soltas (fonte, validação, limitação), disse que o
  README era organizado por decisões. Motivo: era o formato que eu já vinha usando.
- **Fonte da conferência:** esclareci que conferi no Google Finanças e não no Yahoo, que foi a fonte dos dados.
- **Nome do script do dólar:** corrigi a IA. É `extrair_dolar.py`, e ela tinha suposto `transformar_dolar.py`.
- **Script antigo do CDI:** percebi que o `extrair_cdi.py` não se atualizava sozinho, e a IA confirmou que era
  um resto do começo do projeto. Achei que bastava apagá-lo. A IA recomendou renomear o `transformar_cdi.py`
  para manter o padrão, e eu segui a recomendação.
- **Saída com "none":** perguntei se o Ibovespa estava todo vazio. Não estava; a tabela impressa só mostra as
  linhas com algum vazio (8 no total). Foi uma leitura minha equivocada, esclarecida pela IA.
- **Método de trabalho:** pedi que a IA me fizesse perguntas e montasse o texto com as minhas respostas, em vez
  de entregar o texto pronto.
- **Autocorreção:** disse que o IPCA entraria "no último mês de novembro" e depois corrigi para "no último dia de novembro".
- **Visual do dashboard:** informei que o traço continuava branco depois da primeira solução.

## 4. Divisão das decisões

**Decididas por mim, com meus motivos** (as alternativas, na maior parte, foram apresentadas pela IA):

- Manter todas as datas na junção (outer join) e deixar vazio o que não existe, em vez de preencher ou descartar.
- IPCA em tabela separada, por ser mensal.
- Parar o pipeline inteiro se uma etapa falhar, para não montar uma base incompleta sem aviso.
- Tentar a atualização incremental e replicá-la nas quatro séries; dashboard por último.
- Dashboard: pergunta principal ("como o meu dinheiro no CDI está rendendo"); mostrar o rendimento acumulado
  (juros compostos) e não só a taxa diária; olhar para trás, sem projeção futura; comparar CDI com dólar e IPCA;
  Ibovespa em gráfico à parte; partida comum em 01/11/2021; IPCA em degraus, subindo no último dia do mês;
  valor em reais com a porcentagem discreta embaixo; dólar sem suavização; Streamlit como ferramenta.

**Sugeridas pela IA e aceitas sem alteração:**

- Fonte e biblioteca do Ibovespa (`yfinance`, ticker `^BVSP`) e o código de `extrair_ibovespa.py`.
- Todo o código dos scripts: junção, incrementais, `atualizar_tudo.py`, `requirements.txt`, `dashboard.py` (base).
- O tratamento do erro 404 como "sem dado novo" e dos demais erros como falha.
- O filtro de datas posteriores à última do arquivo (Ibovespa e IPCA).
- O procedimento de teste (apagar 3 linhas, rodar de novo, rodar sem apagar).
- Os comandos de Git e as conferências no GitHub.
- O texto das decisões 10 e 11 e das Limitações, escrito pela IA a partir das minhas respostas.

**Onde a IA me corrigiu:**

- Eu disse que a única fonte oficial do Ibovespa era o Yahoo. A fonte oficial é a B3; o Yahoo só republica.
- Disse que o Ibovespa batia com a B3 antes de ter conferido lá. Conferi depois: 167.920 contra 167.922.
- Propus mostrar "quanto meu dinheiro vale no futuro". A IA alertou que seria uma projeção, e escolhi olhar para trás.
- Escrevi que o Ibovespa "não vai ter uma variação tão boa". A IA apontou que os dados mostram alta no período e
  sugeriu justificar a exclusão pelo risco diferente da renda variável.
- O horário da conferência: no README estava 16:56, e eu havia dito 17:18.

## 5. Pontos de atenção (o que a IA pode ter errado e merece verificação humana)

- **Nada foi executado pela IA.** Todos os resultados vieram de testes que rodei. O `dashboard.py` que a IA
  escreveu não foi validado por ela, e a versão final que colei tem mudanças (cores, formatação, `FIM = 2026-09-30`,
  rodapé) cuja origem não aparece na conversa. Os valores do gráfico não foram conferidos de forma independente.
- **Erro 404 do Banco Central:** a afirmação de que a API responde 404 quando não há dado no período é inferida
  do comportamento. A IA pediu que eu abrisse o link no navegador, e a conferência não foi registrada. A Decisão 9
  do README diz isso como fato.
- **Linha repetida do Ibovespa ("1 registro novo"):** a IA supôs que o Yahoo devolveu de novo a última data. A data
  da linha não foi impressa, então a causa não foi confirmada; o filtro resolveu o sintoma.
- **Os 8 vazios do Ibovespa:** a IA atribuiu a vésperas de Natal e Ano Novo pelo padrão das datas. Não houve
  checagem no calendário oficial da B3, e a falha do Yahoo continua como alternativa. A primeira hipótese da IA
  (feriado de 20 de novembro) estava errada.
- **Afirmações sem pesquisa:** "o IPCA de outubro sai por volta da segunda semana de novembro" e "o CDI costuma ser
  divulgado com um dia de defasagem". Vale conferir.
- **Queda de 13,88% do Ibovespa em 26/10:** a IA confirmou por busca na web. Eu mesma conferi só o fechamento de 30/10.
- **Erros da IA ao longo do caminho:** um comando PowerShell que falhou (faltaram parênteses); a primeira versão do
  CDI incremental quebrava no 404; a primeira versão do Ibovespa incremental imprimia "Registros novos: 1" sem dado novo;
  o nome do script do dólar foi chutado errado; a IA disse que o projeto usava "quatro" bibliotecas e listou três.
- **Pendências no README e no repositório (pelo histórico):** o "[13,65%]" entre colchetes na Decisão 2; o horário da
  Decisão 7 (16:56) e a B3 (167.920) não aparecem no texto que colei; não sei se o README no GitHub é idêntico ao texto
  que a IA redigiu; `streamlit` e `plotly` ainda não estão no `requirements.txt`; `dashboard.py` não foi commitado e as
  decisões do dashboard não foram registradas no README.
- **Traço do cursor:** a solução `spikethickness=-2` é uma hipótese da IA (contorno branco do Plotly), não confirmada.
