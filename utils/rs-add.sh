#!/bin/bash

sleep 10

while ! nc -z 192.168.0.6 27017; do
  sleep 1 # wait 1 second before check for mongo1 again
done

mongosh "mongodb://admin:admin_pwd@192.168.0.6:27017/?authSource=admin" <<EOF

ampath = db.getSiblingDB('ampath')
use ampath
ampath.createUser(
  {
    user: "ampath_user",
    pwd: "ampath_pw",
    roles: [
        {
          role: "readWrite",
          db: "ampath"
        }
    ]
  }
)

sax = db.getSiblingDB('sax')
use sax
sax.createUser(
  {
    user: "sax_user",
    pwd: "sax_pw",
    roles: [
        {
          role: "readWrite",
          db: "sax"
        }
    ]
  }
)

tenet = db.getSiblingDB('tenet')
use tenet
tenet.createUser(
  {
    user: "tenet_user",
    pwd: "tenet_pw",
    roles: [
        {
          role: "readWrite",
          db: "tenet"
        }
    ]
  }
)

mq_producer = db.getSiblingDB('mq_producer')
use mq_producer
mq_producer.createUser(
  {
    user: "mq_producer_user",
    pwd: "mq_producer_pwd",
    roles: [
        {
          role: "readWrite",
          db: "mq_producer"
        }
    ]
  }
)

mq_consumer = db.getSiblingDB('mq_consumer')
use mq_consumer
mq_consumer.createUser(
  {
    user: "mq_consumer_user",
    pwd: "mq_consumer_pwd",
    roles: [
        {
          role: "readWrite",
          db: "mq_consumer"
        }
    ]
  }
)

topology_events = db.getSiblingDB('topology_events')
use topology_events
topology_events.createUser(
  {
    user: "topology_events_user",
    pwd: "topology_events_pwd",
    roles: [
        {
          role: "readWrite",
          db: "topology_events"
        }
    ]
  }
)


exit
EOF

