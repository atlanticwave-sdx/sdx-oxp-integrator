# pull os base image
FROM kytos-base

# set work directory

WORKDIR /
RUN mkdir -p /mq-producer
COPY ./kytos/mq-producer/ /mq-producer
RUN for repo in mq-producer; do cd ${repo}; python3 setup.py develop; cd ..; done
RUN touch /var/log/kytos.log
