#!/bin/bash

AMLIGHT=http://0.0.0.0:8181
SAX=http://0.0.0.0:8282
TENET=http://0.0.0.0:8383

# give a few seconds for link discovery (LLDP)
sleep 5

# Switches Metadata
curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/switches/aa:00:00:00:00:00:00:01/metadata -d '{"lat": "25.77", "lng": "-80.19", "address": "Miami", "iso3166_2_lvl4": "US-FL"}'
curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/switches/aa:00:00:00:00:00:00:02/metadata -d '{"lat": "26.38", "lng": "-80.11", "address": "BocaRaton", "iso3166_2_lvl4": "US-FL"}'
curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/switches/cc:00:00:00:00:00:00:03/metadata -d '{"lat": "-3", "lng": "-40", "address": "Fortaleza", "iso3166_2_lvl4": "BR-CE"}'
curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/switches/cc:00:00:00:00:00:00:04/metadata -d '{"lat": "-3", "lng": "-20", "address": "Fortaleza", "iso3166_2_lvl4": "BR-CE"}'
curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/switches/dd:00:00:00:00:00:00:05/metadata -d '{"lat": "-33", "lng": "18", "address": "CapeTown", "iso3166_2_lvl4": "ZA-WC"}'
curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/switches/dd:00:00:00:00:00:00:06/metadata -d '{"lat": "-26", "lng": "28", "address": "Johanesburgo", "iso3166_2_lvl4": "ZA-GP"}'

# Interfaces Links Metadata

curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/interfaces/aa:00:00:00:00:00:00:01:1/metadata -d '{"sdx_nni": "tenet.ac.za:Novi05:1"}'
curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/interfaces/aa:00:00:00:00:00:00:02:3/metadata -d '{"sdx_nni": "tenet.ac.za:Novi05:3"}'
curl -H 'Content-type: application/json' -X POST $AMLIGHT/api/kytos/topology/v3/interfaces/aa:00:00:00:00:00:00:02:4/metadata -d '{"sdx_nni": "sax.net:Novi03:4"}'
curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/interfaces/cc:00:00:00:00:00:00:03:4/metadata -d '{"sdx_nni": "ampath.net:Novi02:4"}'
curl -H 'Content-type: application/json' -X POST $SAX/api/kytos/topology/v3/interfaces/cc:00:00:00:00:00:00:04:7/metadata -d '{"sdx_nni": "tenet.ac.za:Novi05:7"}'
curl -H 'Content-type: application/json' -X POST $TENET/api/kytos/topology/v3/interfaces/dd:00:00:00:00:00:00:05:7/metadata -d '{"sdx_nni": "sax.net:Novi04:7"}'
