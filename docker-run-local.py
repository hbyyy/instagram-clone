#!/usr/bin/env python


import os
import subprocess
from pathlib import Path

HOME = str(Path.home())
SOURCE = os.path.join(HOME, 'projects', 'wps12th', 'python', 'instagram')
SECRETS_FILE = os.path.join(SOURCE, 'app', 'secret.json')
DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '8001:80'),
    ('-d', ''),
    ('--name', 'instagram'),

]


def run(cmd):
    subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    run('docker build -t  lloasd33/wps-instagram -f Dockerfile .')
    run('docker stop instagram')
    run('docker run {options} lloasd33/wps-instagram /bin/bash'.format(
        options=' '.join([
            f'{key} {value} ' for key, value in DOCKER_OPTIONS])
    ))

    run(f'docker cp {SECRETS_FILE} instagram:/srv/instagram/app')


    # run(f'docker exec -it -d instagram gunicorn -b unix:/run/instagram.sock config.wsgi')
    # run(f'docker exec -it -d instagram nginx -g "daemon off;"')
