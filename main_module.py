import PySimpleGUI as sg
import pickle as p
import gpiozero as io
#from time import sleep

import matplotlib.pyplot as plt
import numpy as np

from GUI.window_exp_setup import exp_setup
from GUI.window_measure import measure
from GUI.window_login import login
from GUI.window_manual_control import manual_control
from GUI.window_splash import splash

#from gpiozero.pins.mock import MockFactory
#io.Device.pin_factory = MockFactory()

# Pin setup
pin_list = {}

pin_list['stepPin'] = io.DigitalOutputDevice(19)
pin_list['dirPin'] = io.DigitalOutputDevice(26)
pin_list['stepInterval'] = .005 # milliseconds
pin_list['stopPin1'] = io.DigitalInputDevice(20, pull_up=True) # positivo
pin_list['stopPin2'] = io.DigitalInputDevice(21, pull_up=True) # negativo
vcc = io.DigitalOutputDevice(16)
vcc.on()
# stopref1 = io.Device.pin_factory.pin(22)
# stopref2 = io.Device.pin_factory.pin(23)

# stopref1.drive_high()
# stopref2.drive_high()

pin_list['stepPin'].off()

#splash()

#login screen
user = login()
if user == None:
	exit()
print(user)

#manual control window
values_manual_control = manual_control(pin_list, pin_list)

if values_manual_control is None: #retornamos None para indicar uma saida do programa
	sg.PopupOK('Thank you for using LightWay')
	print('manual_control retornou None')
	exit()

#experiment setup window
values_exp = exp_setup()
if values_exp is None:
	sg.PopupOK('Thank you for using LightWay')
	print('exp_setup retornou None')
	exit()

#merge two dictionaries into values
values_manual_control.update(values_exp)
values = values_manual_control

#get the measured values
# measure_pos, measure_results = measure(values, pin_list)
# measure_pos = np.array(measure_pos)
# measure_results = np.array(measure_results)

# plt.plot(measure_pos, measure_results) # figure with plot
# plt.xlabel('nm')
# plt.ylabel('signal')
# plt.title('Measurements Results')
# plt.show()