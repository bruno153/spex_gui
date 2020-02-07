import PySimpleGUI as sg
import pickle as p
import gpiozero as io
from time import sleep

from window_exp_setup import exp_setup
from window_measure import measure
from window_login import login
from window_manual_control import manual_control
from window_splash import splash

from gpiozero.pins.mock import MockFactory
io.Device.pin_factory = MockFactory()

# Pin setup
pin_list = {}

pin_list['stepPin'] = io.DigitalOutputDevice(19)
pin_list['dirPin'] = io.DigitalOutputDevice(26)
pin_list['stepInterval'] = .005 # milliseconds
pin_list['stopPin1'] = io.DigitalInputDevice(20) # positivo
pin_list['stopPin2'] = io.DigitalInputDevice(21) # negativo
vcc = io.DigitalOutputDevice(16)
vcc.on()
#stopref1 = io.Device.pin_factory.pin(22)
#stopref2 = io.Device.pin_factory.pin(23)

#stopref1.drive_high()
#stopref2.drive_high()

pin_list['stepPin'].off()

splash()

user = login()
if user == None:
	exit()
print(user)

values_manual_control = manual_control(pin_list, pin_list)
values_exp = exp_setup(pin_list)

#merge two dictionaries into values
values_manual_control.update(values_exp)
values = values_manual_control

measure(values, pin_list)