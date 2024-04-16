"""Module with the Constants used in the kytos/listen_events Napp"""
ADMIN_EVENTS = [
        "version/control.initialize",
        "kytos/topology.switch.enabled",
        "kytos/topology.switch.disabled",
        "kytos/topology.switch.metadata.added",
        "kytos/topology.interface.metadata.added",
        "kytos/topology.link.metadata.added",
        "kytos/topology.switch.metadata.removed",
        "kytos/topology.interface.metadata.removed",
        "kytos/topology.link.metadata.removed",
        ]
OPERATIONAL_EVENTS = [
        "topology_loaded",
        "kytos/topology.link_up",
        "kytos/topology.link_down",
        ]
HEADERS = {"Content-type": "application/json"}
USER_COLLECTION='user'
MQ_NAME='events'
MQ_HOST='192.168.0.12'
MQ_PORT='5672'
PUB_TOPIC='topo'
PUB_QUEUE='sdx_q1'
SUB_QUEUE='connection'
SUB_EXCHANGE='connection'
SUB_TOPIC='administrative'
SLEEP_TIME='5'
RABBITMQ_DEFAULT_HOST='rabbitmq3'
RABBITMQ_DEFAULT_USER='mq_user'
RABBITMQ_DEFAULT_PASS='mq_pwd'
