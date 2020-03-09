# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:24:28 2020

Controlador dos motores de passo, versão python
para raspy

@author: Bruno Yamada, Rafael Zuolo
"""

import gpiozero as io
from time import sleep
from gpiozero.tools import all_values, negated

def manual_step(targetstep, pin_list):
    stepInterval = pin_list['stepInterval']
    dirPin = pin_list['dirPin']
    stepPin = pin_list['stepPin']
    stopPin1 = pin_list['stopPin1']
    stopPin2 = pin_list['stopPin2']
    enablePin = pin_list['enablePin']
    stepPin.source_delay = 0.0025
    
    enablePin.on()
    if targetstep > 0:
        dirPin.on()
        stepPin.source = all_values(negated(stopPin2), stepGenerator(targetstep, enablePin))
    else:
        dirPin.off()
        targetstep = -targetstep
        stepPin.source = all_values(negated(stopPin1), stepGenerator(targetstep, enablePin))
    

def stepGenerator(targetstep, enablePin):
    blink = False
    enablePin.on()
    for i in range (0, 2*targetstep + 1):
        yield blink
        blink = not blink
        #print(blink)
    enablePin.off()

def waveToSteps(wave):
    wave2 = wave
    rate = 50 # steps/nm
    return int(rate*wave2)

def wave_step(targetwave, pin_list):
    manual_step(waveToSteps(targetwave), pin_list)