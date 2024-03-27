FROM amlight/kytos:2023.1

# LABEL about the custom image
LABEL maintainer="lmarinve@fiu.edu"
LABEL version="0.1"
LABEL description="Base Image"

# Disable Prompt During Packages Installation
ARG DEBIAN_FRONTEND=noninteractive
ARG branch_python_openflow=master
ARG branch_kytos_utils=master
ARG branch_kytos=master
ARG branch_of_core=master
ARG branch_flow_manager=master
ARG branch_topology=master
ARG branch_of_lldp=master
ARG branch_pathfinder=master
ARG branch_mef_eline=master
ARG branch_maintenance=master
ARG branch_coloring=master
ARG branch_sdntrace=master
ARG branch_flow_stats=master
ARG branch_sdntrace_cp=master
# USAGE: ... --build-arg release_ui=download/2022.2.0 ...
ARG release_ui=latest/download

# http://bugs.python.org/issue19846
ENV LANG=C.UTF-8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN set -e
RUN apt-get update

RUN apt-get install --assume-yes build-essential ca-certificates curl dirmngr dpkg-dev gcc git \
gnupg gunicorn iputils-ping libbz2-dev libc6-dev libexpat1-dev libffi-dev \
liblzma-dev libncurses5-dev libgdbm-dev libnss3-dev libreadline-dev \
libsqlite3-dev libssl-dev lsof make mininet netbase netcat python3-venv \
software-properties-common uuid-dev wget xz-utils zlib1g-dev

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3-setuptools python3-pip rsyslog iproute2 procps curl jq git-core patch \
        openvswitch-switch mininet iputils-ping vim tmux less \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN sed -i '/imklog/ s/^/#/' /etc/rsyslog.conf

RUN git config --global url."https://github.com".insteadOf git://github.com


WORKDIR /

RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN apt update
RUN apt-get install gnupg2
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list
RUN apt update
RUN apt-get install -y mongodb-org-shell

RUN apt install python3-pip --assume-yes
RUN apt-get purge --assume-yes --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
rm -rf /var/lib/apt/lists/*

RUN pip3 install pipenv

COPY ./os_base/kytos_base/requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./os_base/kytos_base/Pipfile Pipfile
