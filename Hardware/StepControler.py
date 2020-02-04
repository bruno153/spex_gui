# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:24:28 2020

Controlador dos motores de passo, versão python
para raspy

@author: rafael
"""

import gpiozero as io
from time import sleep

# from gpiozero.pins.mock import MockFactory
# io.Device.pin_factory = MockFactory()

# stepPin = io.DigitalOutputDevice(17)
# dirPin = io.DigitalOutputDevice(27)
# stepInterval = .005 # milliseconds
# stopPin1 = io.DigitalInputDevice(22) # positivo
# stopPin2 = io.DigitalInputDevice(23) # negativo




#stepPin.off()
#wavelength = Serial.parseInt() # FUNÇÃO QUE VEM DO FRONT END ---------------


def manual_step(targetstep, pin_list):
	stepInterval = pin_list['stepInterval']
	dirPin = pin_list['dirPin']
	stepPin = pin_list['stepPin']
	stopPin1 = pin_list['stopPin1']
	stopPin2 = pin_list['stopPin2']
	while targetstep != 0:	
		if targetstep > 0 and stopPin2.value == 1: # pin 23
			dirPin.off()
			stepPin.on()
			print(stepPin.value)
			sleep(stepInterval)
			targetstep = targetstep - 1
		if targetstep < 0 and stopPin1.value == 1: # pin 22
			dirPin.on()
			stepPin.on()
			sleep(stepInterval)
			targetstep = targetstep + 1
		stepPin.off()
		print(stepPin.value)

def waveToSteps(wave):
    wave2 = wave	
    rate = 5 # steps/nm
    return int(rate*wave2)


# while True():
    # Serial.println("Insert next wavelength:\n") # DEVE SER INTEGRADO NO FRONT----
    # targetwave = Serial.parseInt()
    # Serial.print("Setting wavelength set at ")
    # Serial.print(targetwave/10)
    # Serial.print(".")
    # Serial.print(targetwave%10)
    # Serial.println(" nm.")
    # targetstep = waveToSteps(wavelength-targetwave)
    # Serial.print("This should take ")
    # Serial.print(targetstep)
    # Serial.println(" steps.")

    # while targetstep != 0:
        # if targetstep > 0 and stopPin2.value() == 1: # gpio 23
            # dirPin.off()
            # stepPin.on()
            # sleep(stepInterval)
            # targetstep = targetstep - 1

        # if targetstep < 0 and stopPin1.value() == 1: # pino 22
            # dirPin.on()
            # stepPin.on()
            # sleep(stepInterval)
            # targetstep = targetstep + 1

        # stepPin.off()

    # Serial.println("Done!")
    # wavelength = targetwave
