#!/bin/sh
docker build --no-cache -f os-base/oxpo/Dockerfile -t ampath .
docker build --no-cache -f os-base/oxpo/Dockerfile -t sax .
docker build --no-cache -f os-base/oxpo/Dockerfile -t tenet .
docker build --no-cache -f topology-conversion/Dockerfile -t topology-conversion .
