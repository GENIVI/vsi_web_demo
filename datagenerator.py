#!/usr/bin/env python3

import math
from itertools import cycle
import os
import time

step_length = math.pi * 2 * 0.01

speeds      = [20, 50, 100]
rpms        = [10, 30, 50]
temperature = [60, 80, 120]
#ignition    = ["off", "accessory", "run", "start"]
ignition    = ["run", "accessory", "start"]
oilpressure = [30, 60, 90]
fuel        = [100, 90, 80]
battery     = [140, 130, 120]
left        = ["false", "true"]
right       = ["true", "false"]
gear        = ["drive", "park", "reverse", "neutral"]

values = [
    ("vehicle.speed", cycle(speeds)),
    ("vehicle.engine.rpm", cycle(rpms)),
    ("vehicle.engine.temperature", cycle(temperature)),
    ("vehicle.ignition", cycle(ignition)),
    ("vehicle.engine.oilpressure", cycle(oilpressure)),
    ("vehicle.fuel", cycle(fuel)),
    ("vehicle.battery", cycle(battery)),
    ("vehicle.turnsignal.left", cycle(left)),
    ("vehicle.turnsignal.right", cycle(right)),
    ("vehicle.transmission.gear", cycle(gear)),
]

def demo():
      while True:
          for value_name, value_cycle in values:
              setValue(value_name, next(value_cycle))
          time.sleep(2)          

def setValue(value_name, value):
    os.system("/opt/vsi_web_demo/set {} {}".format(value_name, value))    

if __name__ == "__main__":
    demo()
