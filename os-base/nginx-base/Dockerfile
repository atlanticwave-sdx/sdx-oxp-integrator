# -*- coding: utf-8 -*-
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.

# Base Image
FROM swaggerapi/swagger-ui

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

COPY ./os-base/nginx-base/default.conf.template /etc/nginx/templates/default.conf.template
