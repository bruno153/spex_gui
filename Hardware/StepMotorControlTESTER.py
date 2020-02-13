# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 09:24:28 2020

Controlador dos motores de passo, versão python
para raspy

@author: rafael
"""

import gpiozero as io
from time import sleep


stepPin = io.DigitalOutputDevice(19)
dirPin = io.DigitalOutputDevice(26)
stepInterval = .005 # milliseconds
stopPin1 = io.DigitalInputDevice(20) # positivo
stopPin2 = io.DigitalInputDevice(21) # negativo

stepPin.off()


while True:

	numTestes = int(input("Insert number of tests: "))
	targetstep = float(input("Insert number of steps "))
	temp = targetstep
	for i in range (0, numTestes):
		while targetstep != 0:
			if targetstep > 0 and stopPin2.value == 1: # gpio 23
				dirPin.off()
				stepPin.on()
				print(stepPin.value)
				sleep(stepInterval)
				targetstep = targetstep - 1

			if targetstep < 0 and stopPin1.value == 1: # pino 22
				dirPin.on()
				stepPin.on()
				sleep(stepInterval)
				targetstep = targetstep + 1

			stepPin.off()
			print(stepPin.value)
		targetstep = temp
		print("Done!")