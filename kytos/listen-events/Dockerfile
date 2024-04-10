# pull os base image
FROM kytos-base

# set work directory

WORKDIR /
RUN mkdir -p /listen-events
COPY ./kytos/listen-events/ /listen-events
RUN for repo in listen-events; do cd ${repo}; python3 setup.py develop; cd ..; done
RUN touch /var/log/kytos.log
