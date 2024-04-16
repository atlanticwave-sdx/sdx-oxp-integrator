FROM mongo:5.0

# custom label for the docker image
LABEL version="0.1" maintainer="lmarinve@fiu.edu"
ENV MONGO_INITDB_ROOT_USERNAME admin_user
ENV MONGO_INITDB_ROOT_PASSWORD admin_pwd
ENV MONGO_INITDB_DATABASE admin
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dnsutils \
    iproute2 \
    iputils-ping \
    lsof \
    netcat

RUN mkdir -p /data/db
RUN mkdir -p /mongo-base/
COPY os-base/mongo-base/ /mongo-base/
RUN chmod 600 /mongo-base/m103-keyfile
RUN chmod 755 /mongo-base/*.conf
