#!/bin/sh
docker build --no-cache -f kytos/Dockerfile -t mq-producer .
docker build --no-cache -f amlight/Dockerfile -t mq-consumer .
