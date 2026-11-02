# Pipeline de Indicadores de Mercado

Este projeto reúne quatro indicadores do mercado financeiro brasileiro dos últimos cinco anos (CDI, IPCA, dólar PTAX e Ibovespa), trata os dados e os organiza em uma base. O dashboard é voltado para a equipe comercial da Vêneto e mostra quanto R$ 1.000 investidos em novembro de 2021 valeriam hoje no CDI, no dólar e na inflação (IPCA), com o Ibovespa à parte, como referência de renda variável. O dashboard mostra o que já aconteceu e não faz previsões.


## Como executar o dashboard

1. Instalar Python e Git.


2. Clone o repositório com `git clone https://github.com/Andre20061611/pipeline-indicadores-mercado.git`


3. Entre na pasta do projeto com `cd pipeline-indicadores-mercado`


4. Instale as dependências com `py -m pip install -r requirements.txt`


5. Rode o pipeline completo com `py src/atualizar_tudo.py`
- ####  Esse comando atualiza as quatro séries (CDI, dólar, Ibovespa e IPCA) e depois junta CDI, dólar e Ibovespa em `data/base_diaria.csv`. O IPCA fica em `data/ipca.csv`, em tabela separada.


6. Depois de rodar o pipeline, abra o dashboard com `py -m streamlit run src/dashboard.py`.


## Decisões
### 1. Começar pelo CDI

- **O que decidi:** Começar o pipeline pelo CDI.


- **Por quê:** O CDI é o indicador com o qual tenho mais familiaridade, porque já investi em bancos que uso como o cofrinho e acompanho esse rendimento. Isso me ajudou a validar os dados, como eu já tinha uma ideia dos valores esperados, quando fui calcular o rendimento consegui perceber se o resultado estava mais ou menos certo ou se havia algo errado. Além disso, o CDI foi o mais simples de começar, porque é uma série diária de uma única fonte oficial, o Banco Central, e a própria API já entrega os dados apenas em dias úteis, sem eu precisar fazer nenhum tratamento extra. Isso me permitiu montar um fluxo completo, de ponta a ponta, antes de partir para as outras séries.

### 2. Validar a série na fonte oficial

- **O que decidi:** Busquei os dados direto na fonte oficial, o Banco Central do Brasil, usando a série 12 do SGS (taxa diária do CDI), e conferi se os valores faziam sentido antes de seguir.


- **Por quê:** O case avisa que a IA pode errar ou trazer dados antigos, então não quis depender de números que ela me desse. O site do SGS deu erro no meu navegador, e por isso abri a série 12 pelo link da API do Banco Central, que a IA me passou. Lá vi os últimos registros, com valores diários perto de 0,05 (% ao dia). Para saber se era mesmo o CDI, calculei o rendimento anual. Na primeira conta somei a taxa diária 252 vezes e deu 12,80%, que não batia com a Selic de 13,75%. Revisando, entendi que o CDI rende por juros compostos, e o certo é compor os dias: (1 + taxa/100) elevado a 252. Refeita a conta, deu cerca de 13,65% ao ano, um pouco abaixo da Selic, como se espera do CDI. Conferir o código também importa, porque existem versões diárias, anualizadas e acumuladas com números diferentes, e usar a errada traria outra unidade sem nenhum aviso.

### 3. Converter datas e valores

- **O que decidi:** Converti a coluna de data para o tipo data, com pd.to_datetime e o formato dia/mês/ano explícito, e a coluna de valor para número decimal, com astype(float).


- **Por quê:** Ao olhar os dados que vieram da API, vi que data e valor chegavam como texto. Com texto não dá para fazer conta com o valor nem ordenar por período, porque a ordem seguiria as letras e não o calendário. Também informei o formato da data para evitar troca de dia e mês, pois quando testei sem o formato e 01/11/2021 foi lida como 11 de janeiro.


### 4. Manter apenas dias úteis

- **O que decidi:** Optei por não preencher os fins de semana e feriados, mantendo na base apenas os dias úteis.


- **Por quê:** O CDI só rende em dias úteis, então não existe taxa para sábado, domingo ou feriado. Preencher esses dias com algum valor seria inventar um dado que não existe e poderia distorcer o cálculo do rendimento acumulado. Na prática, não precisei aplicar nenhum filtro: a API do Banco Central só publica a taxa nos dias úteis, então a série já chega no formato que eu queria, e o meu papel foi não alterar isso.

### 5. IPCA: série 433, mantido mensal


- **O que decidi:** Usei a série 433 do SGS, o IPCA cheio mensal, e mantive uma linha por mês, sem transformar em dado diário.


- **Por quê:** Na minha pesquisa inicial apareceu o IPCA-15, que é só uma prévia de como a inflação do mês deve fechar. Escolhi o IPCA cheio porque é o número oficial fechado do mês, o que define se um investimento rendeu acima da inflação. Conferi a série comparando setembro de 2026 com o site do IBGE, e o valor de 0,82 bateu. Mantive o dado mensal porque o IPCA é divulgado uma vez por mês, e transformá-lo em diário significaria inventar valores que o IBGE nunca divulgou.


### 6. Dólar PTAX venda: série 1, apenas dias úteis


- **O que decidi:** Usei a série 1 do SGS, que traz o dólar PTAX de venda, em base diária, e mantive somente os dias úteis, sem preencher fins de semana e feriados.


- **Por quê:** Conferi o código na API do Banco Central e o valor mais recente, de R$ 5,42, bateu com a cotação que aparece no site do próprio Banco Central. A PTAX é a taxa de referência do dia, calculada como a média das consultas feitas aos bancos, e não a última cotação do mercado, então ela só existe quando há negociação. Por isso mantive a mesma decisão do CDI: preencher os dias sem dado criaria cotações que não existiram.

### 7. Ibovespa: Yahoo Finance, fechamento diário


- **O que decidi:** Usei o Yahoo Finance, pela biblioteca yfinance, com o ticker ^BVSP, e guardei o fechamento diário do Ibovespa em pontos, mantendo somente os dias em que a bolsa abriu, sem preencher fins de semana e feriados.


- **Por quê:** O Ibovespa não vem do Banco Central, e sim da B3, a bolsa brasileira, que calcula e divulga o índice. O Yahoo apenas republica esses dados, mas entrega o histórico de forma prática pela biblioteca. Como não é uma fonte oficial, conferi o último fechamento, de 30/10/2026, no Google Finance: o arquivo do pipeline traz 167.922,00, e o Google mostrou 167.921,80 às 16:56. A diferença é de 0,20 ponto em quase 168 mil, desprezível, e provavelmente vem do horário da consulta, já que o Google pode ter mostrado um valor anterior ao fechamento. Por isso considerei o dado do Yahoo confiável para este projeto.

### 8. Junção das séries diárias: manter todas as datas


-  **O que decidi:** Juntei CDI, dólar e Ibovespa numa base única pela data, mantendo todas as datas de todas as séries e deixando vazio onde uma série não tem valor. O IPCA ficou numa tabela separada.


- **Por quê:** Cada série tem o seu próprio calendário. Na junção vi dois casos. O Ibovespa ficou com 8 vazios, nas vésperas de Natal e Ano Novo, dias em que o Banco Central publica o dólar mas a bolsa está fechada. E o CDI ficou com 1 vazio em 30/10/2026, porque conferi na API do Banco Central e o dado desse dia ainda não tinha sido publicado. Tirar essas datas faria eu perder informação real, e preencher criaria valores que não existiram, então deixei vazio. O IPCA é mensal, e juntá-lo à base diária deixaria quase todas as linhas dele vazias, então ele ficou em tabela separada.


### 9. Atualização incremental do CDI

-  **O que decidi:** Fiz o script do CDI pedir ao Banco Central só as datas depois da última que já está no arquivo, sem repetir datas existentes. Se o arquivo não existe ou está vazio, ele faz a carga completa. Se a fonte não tem dado novo, o script avisa e termina, sem erro.


-  **Por quê:** Ao juntar as séries vi que o CDI de 30/10/2026 não existia na fonte, o que mostrou que o dado chega com atraso, então o pipeline precisa conseguir se atualizar depois. Como a data identifica cada linha, o script nunca grava a mesma data duas vezes, e rodar várias vezes não estraga o arquivo. Na primeira versão o script quebrou, porque o Banco Central responde com erro 404 quando não há dado no período. Passei a tratar só o 404 como "sem dado novo" e deixei os outros erros, como queda de internet, quebrarem o script, para não confundir um problema real com a falta de dado novo.


### 10. Atualização incremental do dólar, do Ibovespa e do IPCA

-  **O que decidi:** Levei a atualização incremental do CDI para as outras três séries. Cada script lê a última data do próprio arquivo, pede à fonte só o que veio depois e não grava a mesma data duas vezes. Se o arquivo não existe, faz a carga completa.


- **Por quê:** Cada série tem o seu ritmo de publicação, então o pipeline precisa se atualizar sozinho. No Ibovespa, a primeira versão mostrou “1 registro novo” quando não havia nenhum, porque o Yahoo devolveu de novo a linha da última data. Passei a filtrar só as datas depois da última do arquivo, e o drop_duplicates serviu de segunda proteção. No IPCA, que é mensal, o próximo período é o mês seguinte e não o dia seguinte. Isso apareceu na prática: numa rodada do IPCA a API do Banco Central deu erro 502, o script parou, e na segunda tentativa funcionou. Foi o caso que eu tinha previsto na decisão anterior: um erro do servidor é um problema real, e não falta de dado novo.


### 11. Parar o pipeline quando uma etapa falha

- **O que decidi:** Criei o atualizar_tudo.py, que roda as quatro extrações e depois a junção, em ordem. Se qualquer etapa falha, o pipeline avisa qual foi e para na hora.


- **Por quê:** Prefiro interromper o programa por completo a deixar ele prosseguir com algum dado faltando. Se uma série falhasse e as outras seguissem, a base ficaria com informações cortadas, sem ninguém perceber, e isso poderia prejudicar os outros dados. Parar também deixa claro onde está o problema: o programa mostra qual etapa está rodando, qual falhou e, no fim, “Pipeline concluído com sucesso” quando tudo deu certo. Isso funcionou na prática: quando renomeei o script do CDI e esqueci de atualizar a lista, o pipeline apontou a etapa com erro e parou.


### 12. Dashboard: comparar CDI, IPCA e dólar a partir de R$ 1.000

- **O que decidi:** mostrar CDI, IPCA e dólar no mesmo gráfico, na mesma unidade: quanto R$ 1.000 investidos em novembro de 2021 valeriam hoje em cada referência.


- **Por quê:** O dashboard mostra o que já aconteceu, para o investidor entender o que cada área rendeu nos últimos cinco anos. As três séries originais vêm em unidades diferentes (taxa diária, variação mensal e cotação), e só ficam comparáveis quando todas viram o valor de R$ 1.000 ao longo do tempo. O gráfico mostra o passado e não prevê o futuro. O IPCA entra como régua da inflação: quando o CDI fica acima dele, o investimento teve ganho real.


### 13. Dashboard: Ibovespa em gráfico separado, em pontos

- **O que decidi:** Optei por deixar o gráfico do Ibovespa separado das outras três séries, em pontos


- **Por quê:** O Ibovespa não é um investimento, é um índice que mede o desempenho médio das ações mais negociadas da B3. Ele vem em pontos e não em reais, então colocá-lo no mesmo gráfico dos outros seria comparar coisas diferentes. Além disso, a renda variável depende de oferta e demanda, o que traz um risco diferente do CDI. Deixei separado para apresentar ao investidor uma referência nova, sem misturar com as outras três.


### 14. Dashboard: encerrar as três séries em 30/09/2026


- **O que decidi:** Encerrar CDI, dólar e IPCA na mesma data, 30 de setembro de 2026, tanto no gráfico principal quanto nos valores finais.


- **Por quê:** Eu queria uma comparação justa entre as três referências. Quando olhei o dashboard, cada série terminava em uma data diferente: o CDI em 29/10, o dólar em 30/10 e o IPCA em 30/09. Como o IPCA é mensal e o último mês fechado é setembro, usei essa como data comum, o último dia em que as três têm dado. Assim ninguém compara um mês de inflação a mais de um mês de CDI e dólar. O custo é perder outubro no gráfico, que ainda não tem IPCA publicado.


### 15. Dashboard: Streamlit com Plotly


- **O que decidi:** Decidi construir o dashboard com Streamlit e Plotly, em uma página web interativa aberta pelo navegador.


- **Por quê:** O Streamlit reaproveita o pandas e a base que o pipeline gera, então o dashboard fica ligado ao pipeline em vez de ser um trabalho separado, e quando os dados são atualizados o dashboard lê os arquivos novos. O Plotly gera gráficos interativos: ao passar o mouse, aparecem os valores de cada dia. Ele também permite desenhar o IPCA em degraus, como uso no gráfico, o que deixa a página mais informativa para o usuário.






## Limitações


- **O dashboard mostra o passado, não prevê o futuro.** Ele mostra quanto R$ 1.000 teriam virado desde novembro de 2021, e o que rendeu antes não garante o que vai render depois.


- **Período cortado em 30/09/2026.** Encerrei CDI, dólar e IPCA na mesma data para a comparação ser justa. Por isso outubro de 2026 ficou fora do dashboard, mesmo com CDI e dólar já tendo dados. O Ibovespa também usa esse corte.


- **O Ibovespa vem de uma fonte não oficial.** Ele é obtido pelo Yahoo Finance, pela biblioteca yfinance, que não tem a garantia de uma fonte como o Banco Central e pode mudar, falhar ou ter um dia faltando sem aviso. Por isso conferi o último fechamento em outras fontes.


- **A base diária tem vazios reais.** O Ibovespa tem 8, nas vésperas de Natal e Ano Novo, quando a bolsa fecha e o Banco Central publica o dólar. O CDI tem 1, em 30/10/2026, porque o dado ainda não tinha sido publicado. Deixei os vazios em vez de preencher, para não inventar valores.


- **Se a API do Banco Central falhar, o pipeline para.** Escolhi parar em vez de seguir com dados faltando, e a solução é rodar de novo depois.


- **Os fins de semana e feriados não são preenchidos.** Mantive só os dias úteis, como as fontes publicam.


- **O período do dashboard é fixo no código.** O pipeline se atualiza sozinho, mas o dashboard termina em 30/09/2026 por definição; para incluir meses novos, é preciso mudar a data final no código.


- **Os comandos são para Windows.** Usei `py` para rodar o Python. Em Mac ou Linux, o comando seria `python3`.