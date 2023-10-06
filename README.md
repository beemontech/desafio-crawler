# beeMôn - Practical test

Website to craw: [imdb.com](https://www.imdb.com/chart/top/?ref_=nv_mv_250)

# Requirements

- Docker/docker-compose

# Setup

Build the docker image with docker-compose

`docker-compose build`

# Run the project

Run the container

```
docker-compose up -d mongodb splash app
docker-compose run crawler bash
```

Inside the container run the crawler

```
cd crawler/
scrapy crawl imdb
```

You can check the loaded data into MongoDB by accessing the web app `http://localhost:8000/`, and in your folder, you have a screenshot of the crawled page (`crawler/imdb_com.png`).

# Run the tests

Inside the container run the suit test

```
docker-compose exec -it app bash

pip install -r requirements-test.txt
pytest -v
```
