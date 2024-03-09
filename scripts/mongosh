#!/bin/bash

mongosh --host "rs0/mongo1t" -u "admin_user" -p "admin_pwd" --authenticationDatabase "admin" <<EOF
rs.status()
print("done connecting to replicaset with user/db admin.");
exit
EOF

mongosh --host "rs0/mongo1t" -u "mq_producer_user" -p "mq_producer_pwd" --authenticationDatabase "mq_producer" <<EOF
rs.status()
print("done connecting to replicaset with user/db mq_producer.");
exit
EOF

mongosh --host "rs0/mongo1t" -u "mq_consumer_user" -p "mq_consumer_pwd" --authenticationDatabase "mq_consumer" <<EOF
rs.status()
print("done connecting to replicaset with user/db mq_consumer.");
exit
EOF

