FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade

COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

COPY        . /srv/instagram
WORKDIR     /srv/instagram/app
CMD         python manage.py runserver 0:8000