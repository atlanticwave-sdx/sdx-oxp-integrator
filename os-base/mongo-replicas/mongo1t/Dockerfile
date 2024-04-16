FROM mongo-db

# custom label for the docker image
LABEL version="0.1" maintainer="lmarinve@fiu.edu"
ENV MONGO_INITDB_ROOT_USERNAME admin_user
ENV MONGO_INITDB_ROOT_PASSWORD admin_pwd
ENV MONGO_INITDB_DATABASE admin
# set work directory
WORKDIR /
COPY os-base/mongo-base/node1.conf /etc/mongo.conf
ENTRYPOINT [ "/usr/bin/mongod", "--config", "/etc/mongo.conf"]
