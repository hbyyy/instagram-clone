FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade

COPY        ./.requirements/base.txt /tmp/
COPY        ./.requirements/product.txt /tmp/
RUN         pip install -r /tmp/product.txt

COPY        . /srv/instagram
WORKDIR     /srv/instagram/app
CMD         python manage.py runserver 0:8000