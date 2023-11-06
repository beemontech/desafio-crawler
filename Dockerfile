FROM python:3.10.13-alpine

LABEL MAINTAINER="Ailson da Cruz <ailsoncgt@gmail.com>"

WORKDIR /var/www/

ADD ./requirements.txt /var/www/requirements.txt
RUN pip install -r requirements.txt
RUN pip install -U "celery[redis]"
ADD . /var/www/

ENTRYPOINT sh -c "flask --app app.app --debug run --host=0.0.0.0 & celery -A app.celery_app worker -l error -E & celery -A app.celery_app beat -l error"
