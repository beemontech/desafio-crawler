# Crawler - [Quotes](https://quotes.toscrape.com/):

O projeto foi construído usando `Flask` e `Scrapy` como serviços principais.

## Requisitos:

- Docker ou (Docker & docker-compose)

## Build

Para buildar o projeto, entre na pasta raíz e digite o comando abaixo:

```bash
docker compose build
```

**Atenção:** Se a versão do seu docker instalado não tiver o compose, utilise o `docker-compose` ao invés de `docker`

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
