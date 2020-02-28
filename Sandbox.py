from GUI.window_exp_setup import exp_setup
import gpiozero as io
from gpiozero.pins.mock import MockFactory
import os
from pathlib import Path, PureWindowsPath
# import matplotlib.pyplot as plt
# import numpy as np
import PySimpleGUI as sg
from math import floor
from Hardware.StepControler import wave_step
#for test purposes ONLY
import random as rnd

#pin setup
io.Device.pin_factory = MockFactory()

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

# file = open(os.path.join('C:/Users/rafae/Desktop', 'hue.txt'), "w")
# file.write('omgwtfbbq')
# file.close()


sg.ChangeLookAndFeel('DarkBlue')

type_label = 'Kinetics'
type_kinectics = True
nm_start = 400
nm_stop = 600
nm_ex_fixed = 350
nm_em_fixed = 450
reaction_time = 120
seconds_step = 10
nm_step = 5        # step size between measures
integration_time = 3
blank_sub_file = 'asdfsag.csv'
correction_file = 'bbbbb.csv'
measurement_pos = [rnd.randint(0, 100)]*100
measurement_photo = [rnd.randint(0, 100)]*100

def _save():
    save_csv_path = sg.PopupGetFile('Save experiment results as..',
                                    save_as=True,
                                    file_types= (('save files', '.csv'),),)
    try:
        file = open((save_csv_path), 'w')
        file.write('# Blank subtraction file: '+ blank_sub_file +'\n')
        file.write('# Correction factor file: '+ correction_file +'\n#\n')
        file.write('# Experiment type: '+ type_label +'\n')
        if type_kinectics is False:
            file.write('# Start: '+ str(nm_start)+ ' nm, End: '+ str(nm_stop)+' nm\n')
            file.write('# Increment: '+ str(nm_step)+ ' nm,')
            file.write(' Integration Time: '+str(integration_time)+' seconds\n')
            file.write('#' + '_'*100+'\n')
            file.write('# Wavelenght (nm), measured value\n')
        else:
            file.write('# Total reaction time: ' + str(reaction_time) + ' seconds,')
            file.write(' Step time: '+ str(seconds_step) +' seconds\n')
            file.write('# Excitation value: ' +str(nm_ex_fixed) + ' nm, ')
            file.write('Emition value: '+ str(nm_em_fixed)+ ' nm\n')
            file.write('#' + '_'*60+'\n')
            file.write('# Time (seconds), measured value\n')
            
        for i in range (0, len(measurement_pos)):
            file.write(str(measurement_pos[i]) + ', ' + str(measurement_photo[i]) + '\n')
        file.write('#' + '_'*60+'\n')
        file.close()
    except:
        sg.PopupOK('Empty name or you canceled the save operation.\nNOT RECOMENDED.')
        raise
_save()