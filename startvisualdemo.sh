#!/bin/sh

python3 datagenerator.py &

/usr/bin/google-chrome http://localhost:8080
