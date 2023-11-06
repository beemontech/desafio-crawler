# Crawler - [Quotes](https://quotes.toscrape.com/):

O projeto foi construído usando `Flask` e `Scrapy` como serviços principais.

## Requisitos:

- Docker ou (Docker & docker-compose)

## Build

Entre na pasta raís do projeto e copie o conteudo do `.env.example` para um novo arquivo `.env`

```bash
cp .env.example .env
```

Para buildar o projeto digite o comando abaixo:

```bash
docker compose build
```

**Atenção:** Se a versão do seu docker instalado não tiver o compose, use o `docker-compose` ao invés de `docker`

```bash
docker-compose build
```

Despois de fazer o build digite o comando abaixo para rodar o projeto:

```bash
docker compose up
```

ou (se não tiver o compose no seu docker cli)

```bash
docker-compose up
```

Feito isso, você pode abrir o seu navegador em [http://localhost:8000](http://localhost:8000) e seguir as instruções.

## Testes

Os testes foram feitos usando a lib `pytest`.
Para rodar os testes precisamos acessar o container da aplicação. Faça isso digitando o comando abaixo

```bash
docker compose exec flask sh
```

Agora é só digitar o comando(dentro do container):

```bash
pytest
```

## Screenshots

As capturas de telas são salvas em `crawler/screenshots`.

## Banco de dados

Para armanezar os dados, foi utilizado Mongo DB

## Tarefas assíncronas

Para executar o crawler de forma assíncrona, foi utilizado [celery](https://docs.celeryq.dev/en/stable/) junto com `redis` como [backend e broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html). No projeto existe a possibilidade de agendar a execução para 5min, mas isso é facilmente estendível para qualquer momento no futuro, graças ao celery.
