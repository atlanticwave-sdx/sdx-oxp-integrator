#!/bin/bash

AMLIGHT=http://0.0.0.0:8181
SAX=http://0.0.0.0:8282
TENET=http://0.0.0.0:8383

# give a few seconds for link discovery (LLDP)
sleep 5

# enable all links
for l in $(curl -s $AMLIGHT/api/kytos/topology/v3/links | jq -r '.links[].id'); do curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/links/$l/enable; done
for l in $(curl -s $SAX/api/kytos/topology/v3/links | jq -r '.links[].id'); do curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/links/$l/enable; done
for l in $(curl -s $TENET/api/kytos/topology/v3/links | jq -r '.links[].id'); do curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/links/$l/enable; done
