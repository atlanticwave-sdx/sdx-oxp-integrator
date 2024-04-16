#!/bin/sh
TOPOLOGY_API="http://0.0.0.0:8181/api/kytos/listen_events/v1/shelve/events"
echo "##### shelve topology #####"
curl -H 'Content-Type: application/json' -X GET $TOPOLOGY_API
