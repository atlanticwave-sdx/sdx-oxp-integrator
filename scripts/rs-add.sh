#!/bin/bash

sleep 30

while ! nc -z 192.168.0.6 27027; do
  sleep 1 # wait 1 second before check for mongo1t again
done

while ! nc -z 192.168.0.7 27028; do
  sleep 1 # wait 1 second before check for mongo2t again
done

while ! nc -z 192.168.0.8 27029; do
  sleep 1 # wait 1 second before check for mongo3t again
done

mongosh "mongodb://192.168.0.6:27027/?replicaSet=rs0&authSource=admin" <<EOF
rs.status()
print("done connecting to replicaset with user/db admin.");

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

