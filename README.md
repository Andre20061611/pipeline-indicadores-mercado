# Pipeline de Indicadores de Mercado

Este projeto é direcionado para investidores que preferem investir no CDI diário. 

## Como executar

1. Instalar Python e Git.
2. Clone o repositório com `git clone https://github.com/Andre20061611/pipeline-indicadores-mercado.git`
3. Entre na pasta do projeto com `cd pipeline-indicadores-mercado`
4. Instale as dependências com `py -m pip install -r requirements.txt`
5. Rode a extração com `py src/extrair_cdi.py`
6. Rode a transformação com `py src/transformar_cdi.py`

## Decisões
### 1. Começar pelo CDI

- **O que decidi:** Começar o pipeline pelo CDI.


- **Por quê:** O CDI é o indicador com o qual tenho mais familiaridade, porque já investi em bancos que uso como o cofrinho e acompanho esse rendimento. Isso me ajudou a validar os dados, como eu já tinha uma ideia dos valores esperados, quando fui calcular o rendimento consegui perceber se o resultado estava mais ou menos certo ou se havia algo errado. Além disso, o CDI foi o mais simples de começar, porque é uma série diária de uma única fonte oficial, o Banco Central, e a própria API já entrega os dados apenas em dias úteis, sem eu precisar fazer nenhum tratamento extra. Isso me permitiu montar um fluxo completo, de ponta a ponta, antes de partir para as outras séries.

### 2. Validar a série na fonte oficial

- **O que decidi:** Busquei os dados direto na fonte oficial, o Banco Central do Brasil, usando a série 12 do SGS (taxa diária do CDI), e conferi se os valores faziam sentido antes de seguir.


- **Por quê:** O case avisa que a IA pode errar ou trazer dados antigos, então não quis depender de números que ela me desse. O site do SGS deu erro no meu navegador, e por isso abri a série 12 pelo link da API do Banco Central, que a IA me passou. Lá vi o histórico dos últimos cinco anos, com valores diários perto de 0,05 (% ao dia). Para saber se era mesmo o CDI, calculei o rendimento anual. Na primeira conta somei a taxa diária 252 vezes e deu 12,80%, que não batia com a Selic de 13,75%. Revisando, entendi que o CDI rende por juros compostos, e o certo é compor os dias: (1 + taxa/100) elevado a 252. Refeita a conta, deu cerca de [13,65%] ao ano, um pouco abaixo da Selic, como se espera do CDI. Conferir o código também importa, porque existem versões diárias, anualizadas e acumuladas com números diferentes, e usar a errada traria outra unidade sem nenhum aviso.

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

### **7. Ibovespa: Yahoo Finance, fechamento diário**

- **O que decidi:** Usei o Yahoo Finance, pela biblioteca yfinance, com o ticker ^BVSP, e guardei o fechamento diário do Ibovespa em pontos, mantendo somente os dias em que a bolsa abriu, sem preencher fins de semana e feriados.


- **Por quê:** O Ibovespa não vem do Banco Central, porque ele é calculado e divulgado pela B3, a bolsa brasileira, e não faz parte da base de séries do Banco Central. O Yahoo apenas republica esses dados, mas entrega o histórico de forma prática pela biblioteca. Como ele não é uma fonte oficial, conferi o último fechamento, de 30/10/2026, no Google Finance: o site relatou 167.921,80 às 16:56 e o meu arquivo consta 167.922, diferença apenas de arredondamento."




## Limitações


Já extraí as quatro séries, CDI, IPCA, dólar PTAX e Ibovespa, e cada uma está salva em um arquivo CSV separado na pasta data. Datas e valores já foram convertidos para os tipos corretos, e mantive só os dias úteis em cada série.

Ainda não juntei as séries numa base única pela data, e ainda não montei o dashboard. Minha ideia é seguir essa ordem: primeiro juntar e tratar tudo no Python, para não deixar nenhuma limitação, e só depois montar o dashboard para mostrar ao usuário.

O Ibovespa vem do Yahoo Finance, pela biblioteca yfinance, que é não oficial. Ela não tem a garantia de uma fonte como o Banco Central e pode mudar, falhar ou ter um dia faltando sem aviso. Por isso conferi o último fechamento em outras duas fontes.

O Ibovespa tem 1248 registros e o dólar tem 1256, uma diferença de 8 que ainda não investiguei. Pretendo descobrir a causa quando juntar as séries pela data.

Pretendo fazer a atualização incremental, que é um bônus do case, mas ainda não comecei.

Tive algumas dificuldades pelo caminho, não sabia onde encontrar as taxas do CDI, precisei pesquisar como configurar o formato da data no Python e pedi ajuda à IA para entender como executar o código. No código do Ibovespa, o mais difícil foi lidar com o fuso horário das datas, que o Yahoo entrega e as outras séries não têm, e organizar a lógica do código inteiro. Como estou em um dos períodos iniciais do curso, sigo aprendendo no processo e conferindo o que a IA me sugere, de acordo com meus estudos.