#!/usr/bin/python

import time
import sys
import os
import grovepi
import math

sensor_reading = 1234.5

print ("{\"time\":\"%s\",\"reading1\":%f}" % (time.ctime(), sensor_reading))