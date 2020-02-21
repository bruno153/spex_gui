# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 08:48:28 2020

Módulo de uso do MCP3208, versão python
para raspy

@author: Rafael Zuolo
"""
# the GPIO ports to be used are:
# clock_pin=11, mosi_pin=10, miso_pin=9, select_pin=8

from gpiozero import MCP3208
import time

SAMPLES = 1000

adc_photo = MCP3208(channel=0)
adc_diode = MCP3208(channel=1)

data_photo = [None]*SAMPLES
data_diode = [None]*SAMPLES
start = time.monotonic()

# Read the same channel over and over
for i in range(SAMPLES):
    data_photo[i] = adc_photo.value
    data_diode[i] = adc_diode.value
end = time.monotonic()
total_time = end - start
for i in range (0, len(data_photo)):
    print('{}, {}\n'.format(data_photo[i], data_diode[i]))
print("Time of capture: {}s".format(total_time))
print("Actual sample rate={}".format(2*SAMPLES / total_time))

