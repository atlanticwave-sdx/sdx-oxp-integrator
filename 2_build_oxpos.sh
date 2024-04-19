#!/bin/sh
docker build --no-cache -f kytos-sdx-topology/Dockerfile -t amlight .
docker build --no-cache -f kytos-sdx-topology/Dockerfile -t sax .
docker build --no-cache -f kytos-sdx-topology/Dockerfile -t tenet .
