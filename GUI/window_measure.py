import PySimpleGUI as sg
import time
from math import floor
from Hardware.StepControler import wave_step
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn

import random as rnd      #for test purposes ONLY

import matplotlib.pyplot as plt
import numpy as np

sg.ChangeLookAndFeel('DarkBlue')

def measure(values, pin_list_ex, pin_list_em, work_path):
    loading_popup = sg.Popup('Moving to start position. Please wait...',
                             non_blocking=True, auto_close=True, auto_close_duration=1)
    #varables from setup
    if values['radio_ex']:
        nm_start = values['input_ex_st']
        nm_stop = values['input_ex_en']
        pin_list = pin_list_ex
        nm_pos = nm_start
        reaction_time = 0
        seconds_step=0
        type_kinectics = False
    elif values['radio_em']:
        nm_start = values['input_em_st']
        nm_stop = values['input_em_en']
        pin_list = pin_list_em
        nm_pos = nm_start
        reaction_time=0
        seconds_step=0
        type_kinectics = False

    else:
        type_kinectics = True
        reaction_time = values['input_ti']
        seconds_step = values['input_in_s']
        

    #Going to initial position popup
    loading_popup = sg.Popup('Movendo os monocromadores para as posições iniciais, aguarde.',
                             non_blocking=True, auto_close=True, auto_close_duration=1)

    # moving the monocrom to start positions
    wave_step(values['input_ex_st'] - values['nm_pos_ex'], pin_list_ex)
    wave_step(values['input_em_st'] - values['nm_pos_em'], pin_list_em)

    nm_step = values['input_in_nm']
    time_step = values['integration_time']
    samples_per_second = 32
    samples_per_measurement = floor(samples_per_second*time_step)

    #process calculation valrables and lists
    sample_list = []
    lamp_sample_list = []
    measurement_pos = []
    measurement_result = []
    lamp_correction = []
    last_measure = -1


    #dummy values
    measure_time = 1/samples_per_second

    #setup ADC
    # Data collection setup
    RATE = samples_per_second

    # Create the I2C bus with a fast frequency
    i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

    # Create the ADC object using the I2C bus and the correct gain:
    # gain=8 for .500 ~ v aprox
    ads = ADS.ADS1115(i2c, 8)
    # Create single-ended input on channel 0 and 1
    chan0 = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)

    # ADC Configuration
    ads.mode = Mode.CONTINUOUS
    ads.data_rate = RATE

    #setup GUI
    if type_kinectics is False:
        graph_label_start = nm_start
        graph_label_stop = nm_stop
    else:
        graph_label_start = 0
        graph_label_stop = reaction_time
        nm_pos = '---'

    layout_measure = [
        [sg.Text('Measuring: '),
            sg.Text(str(nm_pos), size=(3, 1), key='text.nm')],
        [sg.Text('Last measure: '),
            sg.Text('', justification='right', size=(8,1), key='last_measure')],
        [sg.Text('Sample number: '),
            sg.Text(str(len(sample_list)), size=(2, 1), key='text_sample')],
        [sg.Graph(canvas_size=(600, 300), 
                  graph_bottom_left=(graph_label_start - 5,-30), # compensate for borders
                  graph_top_right=(graph_label_stop + 5,32000),  # compensate for borders
                  background_color='white', key='graph')],
        [sg.Button('Export csv...', disabled=True, key='btn_csv'),
            sg.Button('Show plot', disabled=True, key='btn_plot')],
        [sg.Button('Pause/Resume', key ='Pause'), sg.Button('Quit')]
    ]

    window = sg.Window('Working...', layout_measure)
    window.finalize()
    graph = window['graph']

    #draw axis

    graph.DrawLine((graph_label_start, 0), (graph_label_stop, 0))

    for x in range(graph_label_start, graph_label_stop+1, 20):
        graph.DrawLine((x,-3), (x,3))
        if x != 0:
            graph.DrawText( x, (x,-10), color='green')

    # Ready to start experiment
    sg.PopupOK('Press \'OK\' to start.', title='Ready to go', non_blocking=False)

    start_exp_time = time.monotonic()
    lap_time = start_exp_time - seconds_step
    while True:
        event, values = window.read(timeout=max(measure_time*1000, 10))
        currend_time = time.monotonic()

        if event == 'Pause':
            event, values = window.read()
        if event == 'Quit' or None:
            break

        #measure from adc
        if type_kinectics is False or currend_time - lap_time >= seconds_step:
            sample_list.append(chan0.value)
            print(sample_list[-1])
            lamp_sample_list.append(chan1.value)
            if len(sample_list) == samples_per_measurement: #took all measurements in the set
                # print((nm_pos, sum(sample_list)/len(sample_list)))
                if type_kinectics is False:
                    measurement_pos.append(nm_pos)
                else:
                    measurement_pos.append(currend_time - start_exp_time)
                last_measure = sum(sample_list)/len(sample_list)
                lamp_last_measure = sum(lamp_sample_list)/len(lamp_sample_list)
                measurement_result.append(last_measure)
                lamp_correction.append(lamp_last_measure)
                lap_time = currend_time

                #draw a line between the last two measurements
                #if there's at least two elements in the measurement
                if len(measurement_pos) > 1:
                    graph.DrawLine((measurement_pos[-1], measurement_result[-1]), (measurement_pos[-2], measurement_result[-2]))

                sample_list = []
                lamp_sample_list = []
                if type_kinectics is False and nm_pos < nm_stop:
                    #move stepper, but don't want to overshoot
                    nm_pos += nm_step
                    wave_step(nm_step, pin_list)

            if (type_kinectics is False and nm_pos > nm_stop or
             type_kinectics is True and currend_time - start_exp_time > reaction_time): 
                #the experiment has ended
                sg.PopupOK('End of the measures.\n REMEBER TO SAVE .CSV')
                break
            
            #update window
            window.Element('text.nm').update(str(nm_pos))
            window.Element('text_sample').update(str(len(sample_list)))
            window.Element('last_measure').update(str(int(last_measure)))
            stopTime = time.monotonic()
            # print(startTime - stopTime)
            # print(startADCTime - startTime)
            # print('\n\n')

    # Update buttons states
    window.Element('btn_csv').update(disabled=False)
    window.Element('btn_plot').update(disabled=False)
    window.Element('Pause').update(disabled=True)

    np_array_pos = np.array(measurement_pos)         # for matplotlib
    np_array_results = np.array(measurement_result)  # for matplotlib
    np_array_lamp = np.array(lamp_correction)

    while True:
        event, values = window.read()

        if event == 'Quit' or None:
            break

        if event=='btn_csv':
            save_csv_path = sg.PopupGetFile('Save experiment results as..',
                                            initial_folder=str(work_path),
                                            save_as=True,
                                            file_types= (('save files', '.csv'),),)
            try:
                file = open((save_csv_path), 'w')
            except:
                sg.PopupOK('Empty name or you canceled the save operation.\nNOT RECOMENDED.')
            file.write('Wavelenght, measured value, lamp value')
            for i in range (0, len(measurement_pos)):
                file.write(str(measurement_pos[i]) + ',' + str(measurement_result[i]) + '\n')
            file.close()
        if event=='btn_plot':
            plt.plot(measurement_pos, measurement_result) # figure with plot
            plt.xlabel('nm')
            plt.ylabel('signal')
            plt.title('Measurements Results')
            plt.show(block=False)
    plt.close()
    window.close()
    return measurement_pos, measurement_result