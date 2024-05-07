# pull os base image
FROM async-base

# set work directory

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./topology-conversion/ /usr/src/app

EXPOSE 8000

ENTRYPOINT ["python3"]
CMD ["-m", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
