# pull os base image
FROM flask-base

# set work directory

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./topology-conversion/ /usr/src/app

EXPOSE 8000

ENTRYPOINT ["python3"]
CMD ["-m", "swagger_server"]
# CMD ["-m", "uvicorn", "swagger_server.app:asgi_app", "--host", "0.0.0.0", "--port", "80800"]
