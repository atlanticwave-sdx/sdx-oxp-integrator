#!/bin/bash

# Start Open vSwitch
service openvswitch-switch start
ovs-vsctl set-manager ptcp:6640

# Stop (can ignore this line haha)
# service openvswitch-switch stop
tmux new-sess -d -s mn python /link-hosts.py

tail -f /dev/null
