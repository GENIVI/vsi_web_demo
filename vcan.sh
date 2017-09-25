#!/bin/sh

modprobe vcan
ip link add dev can0 type vcan
ip link set can0 up
