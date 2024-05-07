# -*- coding: utf-8 -*-
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

# Base Image
FROM python:3.11-slim-bookworm
# LABEL about the custom image
LABEL maintainer="lmarinve@fiu.edu"
LABEL version="0.1"
LABEL description="Base Image"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive

# http://bugs.python.org/issue19846
ENV LANG=C.UTF-8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN set -e
RUN apt-get update
# RUN apt install python3-pip --assume-yes
RUN apt-get install --no-install-recommends --assume-yes python3-pip netcat-traditional tmux \
gcc python3-dev git
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN pip install connexion[swagger-ui,uvicorn]
RUN pip install requests
RUN pip install pytz
