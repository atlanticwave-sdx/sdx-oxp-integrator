from sdx_topology_validator import validate

data = {
    "id": "urn:sdx:topology:amlight.net",
    "name": "AmLight-OXP",
    "version": 2,
    "model_version": "1.0.0",
    "timestamp": "2021-07-07T21:19:40Z",
    "nodes": [
        {
            "id": "urn:sdx:node:amlight.net:Ampath1",
            "name": "Ampath1",
            "location": {
                "address": "Equinix MI1, Miami, FL",
                "latitude": 25.76,
                "longitude": -80.19,
            },
            "ports": [
                {
                    "id": "urn:sdx:port:amlight.net:Ampath1:1",
                    "name": "Ampath1-eth1",
                    "node": "urn:sdx:node:amlight.net:Ampath1",
                    "type": "1GE",
                    "status": "up",
                    "state": "enabled",
                }
            ],
        }
    ],
    "links": [
        {
            "id": "urn:sdx:link:amlight.net:Ampath3/2_Ampath1/2",
            "name": "Link1",
            "ports": [
                {
                    "id": "urn:sdx:port:amlight.net:Ampath1:1",
                    "name": "Ampath1-eth1",
                    "node": "urn:sdx:node:amlight.net:Ampath1",
                    "type": "1GE",
                    "status": "up",
                    "state": "enabled",
                }
            ],
            "type": "intra",
            "bandwidth": 500000,
            "residual_bandwidth": 80,
            "latency": 25,
            "packet_loss": 0.1,
            "availability": 99.5,
            "status": "up",
            "state": "enabled",
        }
    ],
}

validation_result = validate(data)
print(validation_result)
