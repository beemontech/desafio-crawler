FROM python:3.10.13-alpine

LABEL MAINTAINER="Ailson da Cruz <ailsoncgt@gmail.com>"

WORKDIR /var/www/

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
ADD . /var/www/
