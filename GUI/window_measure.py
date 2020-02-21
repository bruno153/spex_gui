import PySimpleGUI as sg
import time
from math import floor
from gpiozero import MCP3208

import matplotlib.pyplot as plt
import numpy as np

import random as rnd        # for test purposes ONLY

sg.ChangeLookAndFeel('DarkBlue')

def _mean_list(list):
    return sum(list)/len(list)


def _sample_measure(adc_photo, adc_diode, SAMPLES=5000):
    '''.return the mean value of SAMPLES measures of the mcp3208.'''
    measure_photo = [None]*SAMPLES
    measure_diode = [None]*SAMPLES
    start = time.monotonic()
    for i in range (0, SAMPLES):
        measure_photo[i] = adc_photo.value
        measure_diode[i] = adc_diode.value
    currend = time.monotonic()
    mean_photo = _mean_list(measure_photo)
    mean_diode = _mean_list(measure_diode)
    elapsed_time = currend - start
    return mean_photo, mean_diode, elapsed_time

def _timed_measure(adc_photo, adc_diode, time, SAMPLES=1000):
    '''return mean value of as many measures can be made in 'time' seconds.'''
    measure_photo = [None]*SAMPLES
    measure_diode = [None]*SAMPLES
    mean_photo = []
    mean_diode = []
    start = time.monotonic()
    currend = start
    correction = 0.0                    # we compensate the list managing time
    while currend - correction - start < time:
        for i in range (0, SAMPLES):
            measure_photo[i] = adc_photo.value
            measure_diode[i] = adc_diode.value
        currend = time.monotonic()
        mean_photo.append(_mean_list(measure_photo))
        mean_diode.append(_mean_list(measure_diode))
        correction += time.monotonic() - currend
    return _mean_list(mean_photo), _mean_list(mean_photo)

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
        reaction_time = values['input_ti']  # total experiment time
        seconds_step = values['input_in_s'] # rest time between measures
        

    #Going to initial position popup
    loading_popup = sg.Popup('Movendo os monocromadores para as posições iniciais, aguarde.',
                             non_blocking=True, auto_close=True, auto_close_duration=1)

    # moving the monocrom to start positions
    wave_step(values['input_ex_st'] - values['nm_pos_ex'], pin_list_ex)
    wave_step(values['input_em_st'] - values['nm_pos_em'], pin_list_em)

    nm_step = values['input_in_nm']             # step size between measures
    time_step = values['integration_time']
    # samples_per_second = 30000
    # samples_per_measurement = floor(samples_per_second*time_step)

    #process calculation valrables and lists
    sample_list_photo = []      # for block reads of ADC
    sample_list_diode = []      # for block reads of ADC
    measurement_pos = []        # seconds or nm of the measure
    measurement_photo = []      # the result integrated of the PM
    measurement_diode = []      # the result integrate of diode
    last_measure = -1


    #dummy values
    # measure_time = 1/samples_per_second

    #setup ADC
    # Data collection setup
    #RATE = samples_per_second

    
    # Create single-ended input on channel 0 and 1
    adc_photo = MCP3208(channel=0)
    adc_diode = MCP3208(channel=1)

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
    
    # used for kinectics experiment
    rest_flag = False
    start_exp_time = time.monotonic()        
    currend_integration_time = 0           
    lap_time = start_exp_time
    
    time_spent_on_adc = 0.50
    # WINDOW MAIN LOOP
    while True:
        event, values = window.read(timeout=10)
        currend_time = time.monotonic()
        
        if type_kinectics is True and currend_time - lap_time >= seconds_step:
            '''Rest time is over, we need to start the ADC reads.'''
            rest_flag = False
            
        if event == 'Pause':
            event, values = window.read()
        if event == 'Quit' or None:
            answer = sg.PopupYesNo('Are you sure you want to quit?')
            if answer=='Yes':
                return None

        if rest_flag is False:
            '''No rest! Read ADC!'''
            sample_list_photo.append(None)
            sample_list_diode.append(None)
            sample_list_photo, sample_list_diode = _timed_measure(adc_photo, adc_diode, time_spent_on_adc)
            currend_integration_time += time_spent_on_adc
            
            if currend_integration_time >= time_step:
                '''integrated the right amount of time.'''
                rest_flag = True
                measurement_photo.append(_mean_list(sample_list_photo))
                measurement_diode.append(_mean_list(sample_list_diode))
                last_measure = measure_photo[-1]
                if type_kinectics is False:
                    measurement_pos.append(nm_pos)
                    rest_flag = False
                else:
                    measurement_pos.append(currend_time - start_exp_time)
                    lap_time = time.monotonic()
                
                #draw a line between the last two measurements
                #if there's at least two elements in the measurement
                if len(measurement_pos) > 1:
                    graph.DrawLine((measurement_pos[-1], measurement_photo[-1]), 
                                   (measurement_pos[-2], measurement_photo[-2]))

                sample_list_photo, sample_list_diode = [], []
                
                if type_kinectics is False and nm_pos < nm_stop:
                    #move stepper, but don't want to overshoot
                    wave_step(nm_step, pin_list)
                    nm_pos += nm_step

            if (type_kinectics is False and nm_pos >= nm_stop or
                type_kinectics is True and currend_time - start_exp_time > reaction_time): 
                #the experiment has ended
                sg.PopupOK('End of the measures.\n REMEBER TO SAVE .CSV')
                break
            
            #update window
            window.Element('text.nm').update(str(nm_pos))
            window.Element('text_sample').update(str(len(sample_list)))
            window.Element('last_measure').update(str(int(last_measure)))
            # print(startTime - stopTime)
            # print(startADCTime - startTime)
            # print('\n\n')
            
    # Update buttons states
    window.Element('btn_csv').update(disabled=False)
    window.Element('btn_plot').update(disabled=False)
    window.Element('Pause').update(disabled=True)

    np_array_pos = np.array(measurement_pos)        # for matplotlib
    np_array_results = np.array(measurement_photo)  # for matplotlib
    np_array_lamp = np.array(measurement_diode)     # for matplotlib

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
                file.write(str(measurement_pos[i]) + ',' + str(measurement_photo[i]) + '\n')
            file.close()
        if event=='btn_plot':
            plt.plot(measurement_pos, measurement_photo) # figure with plot
            plt.xlabel('nm')
            plt.ylabel('signal')
            plt.title('Measurements Results')
            plt.show(block=False)
    plt.close()
    window.close()
    return measurement_pos, measurement_photo