# pull os base image
FROM flask-base

# set work directory

WORKDIR /
RUN mkdir -p /validator
COPY ./os-base/validator/ /validator
COPY ./os-base/validator/curl/gunicorn.sh .
