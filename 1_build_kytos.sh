#!/bin/sh
docker build -f os-base/kytos-base/Dockerfile -t kytos-base .
docker build --no-cache -f os-base/mininet/Dockerfile -t mininet .
docker build --no-cache -f os-base/mongo-base/Dockerfile -t mongo-db .
docker build --no-cache -f os-base/flask-base/Dockerfile -t flask-base .
docker build --no-cache -f os-base/async-base/Dockerfile -t async-base .
docker build --no-cache -f os-base/resty-base/Dockerfile -t open-resty .
