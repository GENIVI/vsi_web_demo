**(C) 2017 Jaguar Land Rover**<br>

All files and artifacts in this repository are licensed under the
provisions of the license provided by the LICENSE file in this repository.

# GENIVI W3C INSTRUMENT CLUSTER

This repository contains a simple demo for an HTML/JavaScript instrument
cluster using [Crossbar](http://crossbar.io) as an implementation of the
W3C Automotive Group's [Vehicle Information Service Specification (VISS)](http://w3c.github.io/automotive/vehicle_data/vehicle_information_service.html).


## Prerequisites

To run this demo you need Python3 and Crossbar installed. We trust that you
know how to install Python3 on your preferred operating system. Crossbar is
best installed using pip, which for Python3 is of course, pip3r.

The installer pulls all the necessary dependencies, however it also
requires a working C compiler and the development packages for an SSL
implementation, typically openssl, to build the native bindings.

Once you have all requirements met you can install Crossbar with

`sudo pip3 install crossbar`

The demo uses the [GENIVI Vehicle Signal Interface
(VSI)](https://github.com/GENIVI/vehicle_signal_interface). VSI uses shared
memory segments that are placed into `/var/run/shm`. If this directory does
not exist you need to create it and make sure that it is readable and
writable by the user running this demo.


## Running the Demo

To start the demo simply use the supplied script:

`./w3c-cluster.sh start`

This starts the demo in the background. Output is written to the file
specified as `LOG_FILE` in the script. The default is `cluster.log`.

To stop the demo use the script again:

`./w3c-cluster.sh stop`


## Playing with the Demo

Once the demo is running you can start playing with it. First load the
instrument cluster into you web browser: `http://localhost:8080`.

The cluster understands a limited set of signals that you can send to it
using `curl`. The signals and their value ranges are:

| Signal Name                | Signal Number | Value Range                   |
| -------------------------- | ------------- | ----------------------------- |
| vehicle.ignition           |  1            | off, accessory, run, start    |
| vehicle.turnsignal.left    |  2            | false, true                   |
| vehicle.turnsignal.right   |  3            | false, true                   |
| vehicle.speed              |  4            | 0 - 220                       |
| vehicle.fuel               |  5            | 0 - 100                       |
| vehicle.battery            |  6            | 100 - 140                     |
| vehicle.engine.rpm         |  7            | 0 - 100                       |
| vehicle.engine.temperature |  8            | 0 - 120                       |
| vehicle.engine.oilpressure |  9            | 0 - 160                       |
| vehicle.transmission.gear  |  10           | park, reverse, neutral, drive |

To send a signal to the instrument cluster use:

`curl -H "Content-Type: application/json" -d '{"procedure": "org.genivi.set", "args": ["vehicle.ignition", "accessory"]}' http://localhost:8080/call`

This example will put the instrument cluster in *accessory* mode and cause
it to perform a *predrive check* (moving the needles and flashing the
      indicators).

You can issue any other signal by replacing its name in the call and set
the appropriate value. However, the instrument cluster has to be in
*accessory*, *run* or *start* mode to be able to accept any other settings.

It is also possible to retrieve the current value of a signal with:

`curl -H "Content-Type: application/json" -d '{"procedure": "org.genivi.get", "args": ["vehicle.ignition"]}' http://localhost:8080/call`
