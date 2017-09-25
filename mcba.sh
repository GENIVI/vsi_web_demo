#!/bin/sh

# NOTE: mcba kernel module is used for hardware interface
# compatible with socket CAN
# See: https://github.com/rkollataj/mcba_usb
modprobe mcba_usb
ip link add dev can0 type mcba_usb
ip link set can0 up
