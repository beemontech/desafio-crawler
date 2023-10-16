
## WebCrawler - IMDB

Este é um projeto desenvolvido em Python, para coletar os dados dos:
- Top 250 filmes segundo IMDb 
- Os 100 Filmes com a pior avaliação segundo IMDb
- Os 100 Mais populares segundo IMDb
- Os 10 Principais em Bilheterias(US) 
Os dados serão armazenados em um Banco de dados e também poderão ser armazenados em arquivos do tipo:
- CSV, XLSX(Excel) ou Json.
Foram utilizados Selenium, Shedule, pandas e Unittest para realização do projeto.



## Instruções Gerais

Crie um abiente virtual na raiz do projeto:
```
python3 -m venv venv
```
Ative o ambiente virtual:
- No Linux/Mac:
  ```
  source venv/bin/activate
  ```
- No Windows:
  ```
  venv\Scripts\activate
  ```

Instale as dependências do projeto:
```
pip install -r requirements.txt
```

Por fim execute o comando:
```
python app.py
``` 
O WebCrawler será Iniciado.




## Descrição
O Crawler poderá facilmente ser configurado para coletar:

- A cada hora,
- Diariamente, 
- Semanalmente, entre outras opções.

OBS ""(O Crawler está configurado para rodar localmente, más o ideal será hospedar em algum serviço de nuvem.)

O Crawler inicia pela url: https://www.imdb.com/chart/top/?ref_=nv_mv_250, onde irá coletar os 250 melhores filmes do IMDb. Para cada filme, foi feita a seguinte coleta:

- Titulo,
- Ano de lançamento,
- Duração do filme,
- Classificação indicativa,
- Quantidade de estrelas,
- Quantidade de avaliações,
- Descrição do filme,
- Direção,
- Atores,
- Link para compra (prime)

Ao final da coleta dessa categoria, é tirado um screenshot da coleta, salva os dados em um arquivo a escolher: 
- CSV, XLSX(Excel), ou Json
Salva os dados em uma tabela no banco de dados SqLite e vai para a proxima Url https://www.imdb.com/chart/bottom/?ref_=chttp_ql_7, Que coletará os 100 piores filmes do IMDb.
O processo será idêntico ao processo anterior, e assim sucessivamente. Todo o processo é salvo no log.

Esse processo só é alterado na coleta da https://www.imdb.com/chart/boxoffice/?ref_=chtbtm_ql_1, Principais bilheterias, onde além dos dados coletados anteriormente, serão coletados os dados:

- Arrecadação fim de semana Bruto,
- Total Bruto,
- Lançamento de semanas,

Todos os dados foram coletados no formato String(texto), com excessão destes 3, que foram facilmente convertidos para float, e a partir dai podemos calcular:

- Percentual de arrecadação por filme,
- Percentual de arrecadação por final de semana,
- Média de Público e bilheteria, mensal, semestral, anual entre outros.




## Apêndice

Um Script de Teste será acionado ao término do Crawler.
O Script consiste em um teste simples, que faz a leitura das pastas que deverão conter os arquivos coletados. Caso o numero de arquivos já pré-definidos no código seja diferente aos da coleta, então o teste falhará.

        
Por motivo do agendador de execução, um Método para excluir esses arquivos foi criado. O Método self.remove_arq() responsável por limpar os arquivos.

Ex:

"" Se por acaso for configurado o agendador, ao término da coleta, lá estariam os arquivos coletados, e não faria sentido rodar novamente e duplicar os mesmos dados coletados, além de fazer os testes falharem .""
