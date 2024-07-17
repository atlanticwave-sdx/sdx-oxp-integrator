FROM italovalcy/mininet:2.3.0d6

RUN apt-get update && apt-get install -y tmux \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

USER root
WORKDIR /root

COPY ./os-base/mininet/start_mininet.sh /
COPY ./os-base/mininet/link-hosts.py /
COPY ./os-base/mininet/link-old-hosts.py /
RUN chmod +x /start_mininet.sh
RUN chmod 775 /link-hosts.py
RUN chmod 775 /link-old-hosts.py

ENTRYPOINT ["/start_mininet.sh"]
