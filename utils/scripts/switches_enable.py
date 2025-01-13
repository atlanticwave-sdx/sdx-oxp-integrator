#!/bin/bash

AMLIGHT=http://0.0.0.0:8181
SAX=http://0.0.0.0:8282
TENET=http://0.0.0.0:8383

# Enable all switches
for sw in $(curl -s $AMLIGHT/api/kytos/topology/v3/switches | jq -r '.switches[].id'); do curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/switches/$sw/enable; curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/interfaces/switch/$sw/enable; done
for sw in $(curl -s $SAX/api/kytos/topology/v3/switches | jq -r '.switches[].id'); do curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/switches/$sw/enable; curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/interfaces/switch/$sw/enable; done
for sw in $(curl -s $TENET/api/kytos/topology/v3/switches | jq -r '.switches[].id'); do curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/switches/$sw/enable; curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/interfaces/switch/$sw/enable; done

# give a few seconds for link discovery (LLDP)
sleep 10
