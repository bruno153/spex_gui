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

values = exp_setup()
values['nm_pos_ex'] = 400

sg.ChangeLookAndFeel('DarkBlue')

def measure(values, pin_list):
    #varables from setup
    if values['radio_ex']:
        nm_start = values['input_ex_st']
        nm_stop = values['input_ex_en']
    else:
        nm_start = values['input_em_st']
        nm_stop = values['input_em_en']
    nm_step = values['input_in_nm']
    time_step = values['integration_time']
    samples_per_second = 16
    samples_per_measurement = floor(samples_per_second*time_step)

    #process calculation
    nm_pos = values['nm_pos_ex']
    sample_list = []
    measurement_pos = []
    measurement_result = []

    #dummy values
    measure_time = 1/samples_per_second

    #Going to initial position popup
    loading_popup = sg.Popup('Movendo os monocromadores para as posições iniciais, aguarde.',
                             non_blocking=True, auto_close=True, auto_close_duration=1)

    #set to initial position
    wave_step(nm_start-nm_pos, pin_list)
    nm_pos = nm_start

    #setup GUI
    layout_measure = [
        [sg.Text('Measuring: '), 
            sg.Text(str(nm_pos), size=(3, 1), key='text.nm')],
        [sg.Text('Last measure: '), 
            sg.Text('', justification='right', size=(8,1), key='last_measure')],
        [sg.Text('Sample number: '), 
            sg.Text(str(len(sample_list)), size=(2, 1), key='text.sample')],
        [sg.Graph(canvas_size=(600, 300), graph_bottom_left=(nm_start-5,-30), 
            graph_top_right=(nm_stop+5,32000), background_color='white', key='graph')],
        [sg.Button('Export csv...', disabled=True, key='btn_csv'),
            sg.Button('Show plot', disabled=True, key='btn_plot')],
        [sg.Button('Pause'), sg.Button('Resume'), sg.Button('Quit')]
    ]

    window = sg.Window('Working...', layout_measure)
    window.finalize()
    graph = window['graph']

    #draw axis
    graph.DrawLine((nm_start, 0), (nm_stop, 0))

    for x in range(nm_start, nm_stop+1, 20):
        graph.DrawLine((x,-3), (x,3))
        if x != 0:
            graph.DrawText( x, (x,-10), color='green')


    while True:
        event, values = window.read(timeout=10)
        if event == 'Pause':
            event, values = window.read()
        if event == 'Quit' or None:
            break
            
        #measure from adc
        sample_list.append(rnd.randint(0, 32676))
        if len(sample_list) == samples_per_measurement: #took all measurements in the set
            measurement_pos.append(nm_pos)
            last_measure = sum(sample_list)/len(sample_list)
            measurement_result.append(last_measure)

            #draw a line between the last two measurements
            #if there's at least two elements in the measurement
            if len(measurement_pos) > 1:
                graph.DrawLine((measurement_pos[-1], measurement_result[-1]), (measurement_pos[-2], measurement_result[-2]))

            sample_list = []
            nm_pos += nm_step
            if nm_pos <= nm_stop:
                pass
                #move stepper, but don't want to overshoot
               # wave_step(nm_step, pin_list)
            
        if nm_pos > nm_stop: #the experiment has ended
            sg.PopupOK('End of the measures.\n Remeber to save CSV.')
            break
        
        #update window
        window.Element('text.nm').update(str(nm_pos))
        window.Element('text.sample').update(str(len(sample_list)))
        window.Element('last_measure').update(str(last_measure))

    window.Element('btn_csv').update(disabled=False)
    window.Element('btn_plot').update(disabled=False)
    # np_array_pos = np.array(measurement_pos_pos)
    # np_array_results = np.array(measurement_pos_results)
    
    while True:
        event, values = window.read()
        
        if event == 'Quit' or None:
            break
        
        if event=='btn_csv':
            save_csv_path = sg.PopupGetFile('Save experiment results as..', 
                                            save_as=True, file_types= (('save files', '.csv'),),)
            file = open(PureWindowsPath(save_csv_path), 'w')
            for i in range (0, len(measurement_pos)):
                file.write(str(measurement_pos[i]) + ',' + str(measurement_result[i]) + '\n')
            file.close()
        # if event=='btn_plot':
            # plt.plot(measurement_pos, measurement_result) # figure with plot
            # plt.xlabel('nm')
            # plt.ylabel('signal')
            # plt.title('Measurements Results')
            # plt.show()
    window.close()
    return measurement_pos, measurement_result
    
measure(values, pin_list)