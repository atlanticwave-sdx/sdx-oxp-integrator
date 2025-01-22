services:
  mongo:
    image: mongo-db
    container_name: mongodb
    hostname: mongodb
    volumes:
      - ./utils/scripts/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
      - mongodb-data:/data/db/
      - mongodb-log:/var/log/mongodb/
    env_file:
      - .env
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_INITDB_ROOT_USERNAME}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_INITDB_ROOT_PASSWORD}
    networks:
      kytos_network:
        ipv4_address: 192.168.0.6
    ports:
      - 27017:27017

  mq1:
    image: rabbitmq:latest
    pull_policy: always
    env_file:
      - .env
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 5s
      timeout: 5s
      retries: 60

  ampath:
    container_name: ampath
    image: ampath
    privileged: true
    tty: true
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.2
    ports:
      - 6653:6653
      - 8181:8181
    env_file: 
      - .env
    volumes:
      - ./utils:/utils
    depends_on:
      - mongo

  sax:
    container_name: sax
    image: sax
    privileged: true
    tty: true
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.3
    ports:
      - 6654:6653
      - 8282:8181
    env_file: 
      - .env
    volumes:
      - ./utils:/utils
    depends_on:
      - mongo

  tenet:
    container_name: tenet
    image: tenet
    privileged: true
    restart: always
    tty: true
    networks:
      kytos_network:
        ipv4_address: 192.168.0.4
    ports:
      - 6655:6653
      - 8383:8181
    env_file: 
      - .env
    volumes:
      - ./utils:/utils
    depends_on:
      - mongo

  mininet:
    container_name: mininet
    image: mininet
    privileged: true
    tty: true
    networks:
      kytos_network:
        ipv4_address: 192.168.0.11
    volumes:
      - /lib/modules:/lib/modules
      - ./utils:/utils
    depends_on:
      - ampath
      - sax
      - tenet

  ampath-topology-conversion:
    container_name: ampath-topology-conversion
    image: topology-conversion
    privileged: true
    tty: true
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.15
    ports:
      - 8015:8000
    env_file:
      - .env
    volumes:
      - ./utils:/utils

  sax-topology-conversion:
    container_name: sax-topology-conversion
    image: topology-conversion
    privileged: true
    tty: true
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.16
    ports:
      - 8016:8000
    env_file:
      - .env
    volumes:
      - ./utils:/utils

  tenet-topology-conversion:
    container_name: tenet-topology-conversion
    image: topology-conversion
    privileged: true
    tty: true
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.17
    ports:
      - 8017:8000
    env_file:
      - .env
    volumes:
      - ./utils:/utils

  resty:
    container_name: resty
    image: open-resty
    restart: always
    networks:
      kytos_network:
        ipv4_address: 192.168.0.13
    ports:
      - 80:80
      - 443:443


networks:
  kytos_network:
    ipam:
      driver: default
      config:
        - subnet: 192.168.0.0/24
          gateway: 192.168.0.1

volumes:
  mongodb-data:
    driver: local
    name: mongo-data
  mongodb-log:
    driver: local
    name: mongo-log
