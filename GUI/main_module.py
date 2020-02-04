import PySimpleGUI as sg
import pickle as p
import gpiozero as io

from window_exp_setup import exp_setup
from window_measure import measure
from window_login import login
from window_manual_control import manual_control

from gpiozero.pins.mock import MockFactory
io.Device.pin_factory = MockFactory()

# Pin setup
pin_list = {}

pin_list['stepPin'] = io.DigitalOutputDevice(17)
pin_list['dirPin'] = io.DigitalOutputDevice(27)
pin_list['stepInterval'] = .005 # milliseconds
pin_list['stopPin1'] = io.DigitalInputDevice(22) # positivo
pin_list['stopPin2'] = io.DigitalInputDevice(23) # negativo

stopref1 = io.Device.pin_factory.pin(22)
stopref2 = io.Device.pin_factory.pin(23)

stopref1.drive_high()
stopref2.drive_high()

pin_list['stepPin'].off()



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
