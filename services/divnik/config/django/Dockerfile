FROM python:3.7

MAINTAINER pomo_mondreganto

ENV PYTHONUNBUFFERED=1

#RUN apk add libpq-dev

COPY ./src/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY ./src /app

COPY ./config/django/entrypoint.sh /entrypoint.sh
COPY ./config/db_check.py /db_check.py
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
