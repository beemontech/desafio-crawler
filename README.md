# beeMôn - Practical test

Website to craw: [imdb.com](https://www.imdb.com/chart/top/?ref_=nv_mv_250)

# Requirements

- Docker/docker-compose


# Setup

Build the docker image with docker-compose

`docker-compose build`

# Run

Run the container

`docker-compose run crawler bash`

Inside the container run the crawler

```
cd crawler/
scrapy crawl imdb
```

You can check the exported data in the JSON file `IMDb_<timestamp>.json`