#!/usr/bin/env python
# import subprocess
#
# access_key = subprocess.run('aws configure get aws_access_key_id --profile wps-secrets-manager',
#                             stdout=subprocess.PIPE,
#                             shell=True
#                             ).stdout.decode('utf-8').strip()
# secret_access_key = subprocess.run('aws configure get aws_secret_access_key --profile wps-secrets-manager',
#                                    stdout=subprocess.PIPE,
#                                    shell=True
#                                    ).stdout.decode('utf-8').strip()

import boto3
import subprocess

session = boto3.session.Session(
    profile_name='wps-secrets-manager'
)
credentials = session.get_credentials()
access_key = credentials.access_key
secret_access_key = credentials.secret_key

print(access_key, secret_access_key)

DOCKER_OPTIONS = [
    ('--rm', ''),
    ('-it', ''),
    ('-p', '8001:8000'),
    ('--name', 'instagram'),
    ('--env', f'AWS_SECRETS_MANAGER_ACCESS_KEY_ID={access_key}'),
    ('--env', f'AWS_SECRETS_MANAGER_SECRET_ACCESS_KEY={secret_access_key}')
]
subprocess.run('docker stop instagram', shell=True)
subprocess.run('docker run {options} lloasd33/wps-instagram'.format(
    options=' '.join([
        f'{key} {value} ' for key, value in DOCKER_OPTIONS])
), shell=True)
