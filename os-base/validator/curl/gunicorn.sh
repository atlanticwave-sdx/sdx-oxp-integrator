#!/bin/sh

pipenv install --dev
pipenv run gunicorn 'swagger_server.__main__:app' -w 4 -b 0.0.0.0:8080 \
	--daemon \
	--access-logfile var/log/gunicorn/access_gunicorn.log \
	--error-logfile var/log/gunicorn/error_gunicorn.log \
	--capture-output \
	--log-level='debug'

