daemon = False
chdir = '/srv/instagram/app'
bind = 'unix:/run/instagram_server.sock'
accesslog = '/var/log/gunicorn/instagram-access.log'
errorlog = '/var/log/gunicorn/instagram-error.log'
capture_output = True