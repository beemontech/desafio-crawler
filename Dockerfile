FROM python:3.12-slim-bullseye
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
ENV APP_FOLDER=/app

RUN : "---------- install generic build container deps ----------" \
    && set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        openssh-client \
        build-essential

RUN : "---------- install scrapy build container deps ----------" \
    && apt-get install -y --no-install-recommends \
        libxml2-dev \
        libxslt1-dev \
        libssl-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_FOLDER}

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . ${APP_FOLDER}
