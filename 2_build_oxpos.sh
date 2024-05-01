#!/bin/sh
docker build --no-cache -f os-base/oxpo/Dockerfile -t amlight .
docker build --no-cache -f os-base/oxpo/Dockerfile -t sax .
docker build --no-cache -f os-base/oxpo/Dockerfile -t tenet .
