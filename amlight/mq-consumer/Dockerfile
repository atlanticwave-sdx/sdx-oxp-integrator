# pull os base image
FROM kytos-base

# set work directory

WORKDIR /
RUN mkdir -p /mq-consumer
COPY ./amlight/mq-consumer/ /mq-consumer
RUN for repo in mq-consumer; do cd ${repo}; python3 setup.py develop; cd ..; done
RUN touch /var/log/kytos.log
