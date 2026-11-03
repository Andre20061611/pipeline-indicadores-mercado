# IA.md — Relatório 1: Claude (Anthropic)

Conversa de acompanhamento do case "Pipeline de Indicadores de Mercado" (Vêneto Family Office). Período: 31/10/2026 a 02/11/2026. Boa parte da conversa foi por voz (transcrições com hesitações) e o resto por texto, com prints de tela e de erros do terminal.

> **Escopo.** Este relatório cobre apenas o que aconteceu nesta conversa. Parte do trabalho (série do IPCA, junção das séries diárias, atualização incremental, `atualizar_tudo.py` e a primeira versão do dashboard) foi feita em outra conversa, com outra IA. Aqui esse material só aparece porque André colou transcrições e o README, então não consigo atestar como ele foi construído.

## 1. Como fui direcionada

- **Contexto:** André abriu dizendo que estava num processo seletivo com case técnico em que podia usar IA, que não tinha visto a matéria na faculdade, e enviou o PDF do case. Esse PDF (critérios, pesos, estrutura do repositório e do README) foi a principal fonte de restrições da conversa.
- **Plano antes do código:** André não pediu um plano. O plano (desenhar fontes, tratamentos, base e dashboard; começar por uma série; validar na fonte oficial; registrar decisões no README) foi proposto por mim, e ele o seguiu: assistiu a vídeos sobre ETL, escolheu o CDI como primeira série e foi avançando na ordem.
- **Nível de detalhe das instruções:** instruções curtas, muitas por voz. A pergunta mais frequente foi "qual o próximo passo?". Pediu explicações quando não entendia (o que é `cd`, como funciona `git commit -m`, onde colar cada texto) e mandou prints dos erros do terminal em vez de descrevê-los.
- **Restrições que ele mesmo colocou:** queria fazer por partes e deixar o estilo do dashboard por último; queria que o README fosse pessoal e fiel ao que ele fez ("para não ficar algo que eu não fiz"); e propôs que eu fizesse perguntas para ele responder e escrever.
- **Código pronto:** em alguns momentos pediu o código pronto (ajuste da data final do dashboard, redesenho visual, correção de erro).

## 2. Pedidos principais

1. Perguntou se dava para fazer o case junto com a IA ou se deveria estudar antes. Recomendei uma base mínima (ETL, Python e Git) e depois fazer junto.
2. Pediu ajuda para achar e validar a série do CDI quando o site do SGS dava erro. Pesquisei um candidato (série 12) e ele conferiu os valores direto na API do Banco Central.
3. Pediu o passo a passo do ambiente: repositório no GitHub, instalação do Git, clone, commits e os primeiros scripts em Python (CDI, dólar e Ibovespa).
4. Pediu ajuda para montar e revisar o README: esqueleto, decisões, limitações e uma revisão final com 8 pontos a corrigir.
5. Pediu ajustes no dashboard: encerrar as três séries em 30/09/2026 e redesenhar o visual (cores da Vêneto, formatos brasileiros, caixa de valores em cinza-escuro). Também executou, a meu pedido, um teste do zero seguindo só o README.

## 3. Correções e questionamentos

André raramente rejeitou uma sugestão de forma direta. O mais comum foi pedir esclarecimento ou trazer um resultado que contradizia o que eu tinha dito. Os momentos concretos:

- **Cálculo do CDI.** Ao rodar a conta que mencionei, chegou a 12,798576 e perguntou se deveria alterar o texto. Isso expôs que a conta somava a taxa diária em vez de compô-la. Corrigi a fórmula e ele ainda pediu como fazer a conta no papel, para entender.
- **Passo desnecessário.** Avisou que não tinha feito o passo de criar o arquivo pelo PowerShell, porque já o tinha criado pelo Explorador de Arquivos. Era um passo redundante meu.
- **Caminhos e pastas.** Os prints e mensagens de erro dele mostraram problemas que eu não tinha previsto (PowerShell aberto em `System32`, `python` apontando para um atalho quebrado, caminho `src\src` duplicado, `dolar.csv` salvo na pasta errada). Cada um corrigiu minhas instruções.
- **Datas finais do dashboard.** Eu estava descrevendo o que a outra IA tinha dito. Ele discordou ("você se confundiu"), olhou a tela e trouxe as datas reais: CDI em 29/10, dólar em 30/10 e IPCA em 30/09. A partir disso pediu para encerrar todas na mesma data.
- **Caixa de valores.** Notou que a caixa que aparece ao passar o mouse no gráfico principal ficou vazia e pediu um cinza-escuro fosco, como a do Ibovespa.
- **README.** Reescreveu partes do que sugeri (por exemplo, o motivo da escolha do Streamlit e a explicação de que o Ibovespa não é um investimento), confirmou que os episódios dos erros 404 e 502 e do script renomeado aconteceram com ele e conferiu a diferença entre o arquivo e o Google Finance na decisão do Ibovespa.

Observação de fidelidade: também houve correções minhas a ele. Por exemplo, ele justificou a escolha do CDI com uma previsão política sobre a taxa de juros, e eu corrigi que a taxa é definida pelo Copom e que o dashboard mostra apenas o passado.

## 4. Divisão das decisões

**Decididas por André**
- Começar pelo CDI (familiaridade e simplicidade técnica).
- Manter apenas dias úteis, sem preencher fins de semana e feriados.
- Usar 30/09/2026 como data final comum das três séries (escolheu entre as opções que apresentei).
- Usar Streamlit com Plotly, com a justificativa dele.
- Deixar o Ibovespa em gráfico separado, em pontos.
- Usar a paleta da Vêneto como base do visual e enviar o site de referência.
- Deixar o estilo por último e só avançar depois de commitar.
- Exigir que o README refletisse o que ele fez, e eliminar do texto o que não fez ou não conferiu.

**Sugeridas por mim e aceitas sem alteração (ou com ajustes mínimos)**
- A ordem das etapas, a estrutura `src/` e `data/` e o uso de `py` em vez de `python`.
- Os códigos de série 12 (CDI) e 1 (dólar), aceitos depois de ele conferir os valores na API.
- O esqueleto do README (Como executar, Decisões, Limitações) e o formato "O que decidi / Por quê".
- Os textos dos itens 12, 14 e 16 e o bloco de Limitações, que redigi a partir das ideias dele. Ele os adotou com poucas mudanças, então vale ele conseguir explicar cada frase.
- O código do redesenho visual do dashboard (formatos brasileiros, linha de referência em R$ 1.000, rodapé com fontes e cores).
- Os títulos das mensagens de commit.

**Fora desta conversa:** a série 433 (IPCA), a junção das séries, a atualização incremental, `atualizar_tudo.py` e a primeira versão do dashboard vieram da outra IA.

## 5. Pontos de atenção

- **Código de série do dólar.** A série 1 veio de resultados de busca e foi validada só pelo valor (R$ 5,42, igual ao do site do Banco Central). Eu não li a descrição oficial dela no SGS. Convém conferir que ela corresponde mesmo ao "dólar PTAX venda" pedido no case.
- **Código de série do CDI.** A série 12 foi validada pela magnitude (cerca de 13,65% ao ano composto, compatível com a Selic de 13,75% da página do Banco Central), e não pela descrição oficial no SGS, que estava fora do ar.
- **Limites da API.** O limite de 20 registros no formato `ultimos/N` e o de 10 anos em séries diárias vieram de um guia de terceiros. André não testou isso. A janela de 5 anos funcionou.
- **Código que eu não executei.** Não consigo rodar código. Tudo que escrevi foi testado por André e dependeu dos prints dele. Um erro de sintaxe apareceu no dashboard; atribuí a causa a um parêntese perdido ao copiar, mas foi um palpite.
- **Diagnóstico errado da pasta `data`.** Presumi que uma pasta `data` dentro de `src` era um engano sem conteúdo. Na verdade, o script do dólar tinha salvo ali o `dolar.csv`, porque o caminho era relativo. Corrigi depois que ele descreveu o conteúdo.
- **Cores aproximadas.** Os valores hexadecimais da paleta foram estimados a partir de um print, e a tipografia da marca não foi reproduzida.
- **Texto em Markdown.** Expliquei que dois "R$" na mesma linha fazem o GitHub tratar o trecho como fórmula e sugeri a barra invertida. Nesta conversa ele não confirmou que a correção funcionou.
- **Frases redigidas por mim no README.** Itens 12, 14, 16, a abertura e as Limitações partiram de textos meus. Precisam ser conferidos e entendidos por ele, em especial a afirmação de que o IPCA serve como régua para medir ganho real.
- **Itens 9, 10 e 11 do README** (atualização incremental e parada do pipeline) vieram da outra conversa. Não vi o código deles e não verifiquei se a descrição bate com o comportamento real.
- **Transcrições de voz.** Parte das mensagens veio de transcrição, com termos truncados ("PCA", "petax", "gatekeep"). Interpretei pelo contexto, e algumas interpretações podem ter sido erradas.
