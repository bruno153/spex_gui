# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:24:28 2020

Controlador dos motores de passo, versão python
para raspy

@author: Bruno Yamada, Rafael Zuolo
"""

import gpiozero as io
from time import sleep

def manual_step(targetstep, pin_list):
	stepInterval = pin_list['stepInterval']
	dirPin = pin_list['dirPin']
	stepPin = pin_list['stepPin']
	stopPin1 = pin_list['stopPin1']
	stopPin2 = pin_list['stopPin2']
    enablePin = pin_list['enablePin']
    enablePin.on()
	while targetstep != 0:	
		if targetstep > 0 and stopPin2.value == 0: # gpio 23
			dirPin.on()
			stepPin.on()
			sleep(stepInterval)
			targetstep = targetstep - 1
		if targetstep < 0 and stopPin1.value == 0: # gpio 22
			dirPin.off()
			stepPin.on()
			sleep(stepInterval)
			targetstep = targetstep + 1
		stepPin.off()
		#print(stepPin.value)
    enablePin.off()
    
def waveToSteps(wave):
    wave2 = wave	
    rate = 50 # steps/nm
    return int(rate*wave2)
	
def wave_step(targetwave, pin_list):
	manual_step(waveToSteps(targetwave), pin_list)