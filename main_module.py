#!/usr/bin/python3
import PySimpleGUI as sg
import pickle as p
import gpiozero as io
#from gpiozero.pins.mock import MockFactory
#io.Device.pin_factory = MockFactory()
from time import sleep

# import matplotlib.pyplot as plt
# import numpy as np

from GUI.window_exp_setup import exp_setup
from GUI.window_measure import measure
from GUI.window_login import login
from GUI.window_manual_control import manual_control
from GUI.window_splash import splash

# Pin setup emition
pin_list_em = {}
pin_list_em['stepPin'] = io.DigitalOutputDevice(16)
pin_list_em['dirPin'] = io.DigitalOutputDevice(12)
pin_list_em['stepInterval'] = .005 # milliseconds
pin_list_em['stopPin1'] = io.DigitalInputDevice(7, pull_up=True) # positivo
pin_list_em['stopPin2'] = io.DigitalInputDevice(1, pull_up=True) # negativo
pin_list_em['enablePin'] = io.DigitalOutputDevice(5, active_high=False)

# Pin setup excitation
pin_list_ex = {}
pin_list_ex['stepPin'] = io.DigitalOutputDevice(19)
pin_list_ex['dirPin'] = io.DigitalOutputDevice(26)
pin_list_ex['stepInterval'] = .005 # milliseconds
pin_list_ex['stopPin1'] = io.DigitalInputDevice(20, pull_up=True) # positivo
pin_list_ex['stopPin2'] = io.DigitalInputDevice(21, pull_up=True) # negativo
pin_list_ex['enablePin'] = io.DigitalOutputDevice(13, active_high=False)
# stopref1 = io.Device.pin_factory.pin(22)
# stopref2 = io.Device.pin_factory.pin(23)

# stopref1.drive_high()
# stopref2.drive_high()

pin_list_em['stepPin'].off()
pin_list_ex['stepPin'].off()

#splash()

#login screen
user, work_path = login()
if user == None:
    exit()

#manual control window
values_manual_control = manual_control(pin_list_ex, pin_list_em)

if values_manual_control is None: #retornamos None para indicar uma saida do programa
    sg.PopupOK('Thank you for using LightWay')
    print('manual_control retornou None')
    exit()

#experiment setup window
values_exp = exp_setup(work_path)
if values_exp is None:
    sg.PopupOK('Thank you for using LightWay')
    print('exp_setup retornou None')
    exit()

#merge two dictionaries into values
values_manual_control.update(values_exp)
values = values_manual_control

#get the measured values
measure_pos, measure_results = measure(values, pin_list_ex, pin_list_em, work_path)
sg.PopupOK('Thank you for using LightWay')
