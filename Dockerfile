FROM        python:3.7-slim

RUN         apt -y update && apt -y dist-upgrade
RUN         apt -y install nginx

COPY        ./requirements.txt /tmp/
RUN         pip install -r /tmp/requirements.txt

COPY        . /srv/instagram
WORKDIR     /srv/instagram/app
RUN         mkdir /var/log/gunicorn

RUN         rm /etc/nginx/sites-enabled/default
RUN         cp /srv/instagram/.config/instagram.nginx /etc/nginx/sites-enabled/

