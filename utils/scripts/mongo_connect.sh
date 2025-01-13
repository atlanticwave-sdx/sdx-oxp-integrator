#/bin/bash
mongosh "mongodb://192.168.0.6:27027,mongo2t:27028,mongo3t:27029/?replicaSet=rs0&username='mq_producer_user'&password='mq_producer_pwd'"
