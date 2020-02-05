#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

HOME = str(Path.home())
IDENTITY_FILE = os.path.join(HOME, '.ssh', 'wps12thself.pem')
SOURCE = os.path.join(HOME, 'projects', 'wps12th', 'python', 'instagram')
HOST = '15.164.226.135'
USER = 'ubuntu'
TARGET = f'{USER}@{HOST}'
SECRETS_FILE = os.path.join(SOURCE, 'app', 'secret.json')
print(HOME, IDENTITY_FILE, SOURCE)


def run(cmd, ignore_error=False):
    process = subprocess.run(cmd, shell=True)
    if not ignore_error:
        process.check_returncode()


def ssh_run(cmd):
    run(f'ssh -i {IDENTITY_FILE} {TARGET} -C {cmd}')


DOCKER_IMAGE_TAG = 'lloasd33/wps-instagram'


# 1 도커 이미지 업데이트
def local_build_push():
    print(f'=========================local_build_push==============================')
    run(f'docker build -t {DOCKER_IMAGE_TAG} .')
    run(f'docker push {DOCKER_IMAGE_TAG}')


# 2 서버 업데이트
def server_init():
    print('============================server_init===========================')
    ssh_run(f'sudo apt -y update &&'
            f'sudo DEBIAN_FRONTEND=noninteractive apt dist-upgrade -y &&'
            f'sudo apt -y autoremove')
    ssh_run(f'sudo apt -y install docker.io')


def server_pull_run():
    print('========================server_pull_run===============================')
    ssh_run(f'docker stop instagram')
    ssh_run(f'docker pull {DOCKER_IMAGE_TAG}')
    ssh_run(f'sudo docker run -d --rm -it -p 8000:80 --name=instagram lloasd33/wps-instagram /bin/bash')


def copy_secret():
    print('========================copy_secret===============================')
    run(f'scp -i {IDENTITY_FILE} {SECRETS_FILE} {TARGET}:/tmp')
    ssh_run(f'docker cp /tmp/secret.json instagram:/srv/instagram/app')


def server_run():
    print('=========================server_run==============================')
    # ssh_run(f'docker exec -it -d instagram python manage.py runserver 0:8000')
    # ssh_run(f'docker exec -it -d instagram gunicorn -b unix:/run/instagram_server.sock config.wsgi')
    # ssh_run(f'docker exec -it -d instagram nginx -g \"daemon off;\"')
    ssh_run(f'docker exec -d instagram python manage.py collectstatic')
    ssh_run(f'docker exec -d instagram supervisord -c ../.config/supervisord_server.conf -n')


if __name__ == '__main__':
    try:
        local_build_push()
        server_init()
        server_pull_run()
        copy_secret()
        server_run()
    except subprocess.CalledProcessError as e:
        print('deploy error!')
        print(f'cmd : {e.cmd}')
        print(f'stderror : {e.stderr}')
        print(f'returncode : {e.returncode}')
        print(f'stdout : {e.stdout}')
        print(f'outpit : {e.output}')
