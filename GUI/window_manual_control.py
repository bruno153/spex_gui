# -*- coding: utf-8 -*-
# import sys
# sys.path.append('../')

import PySimpleGUI as sg
from Hardware.DeclarativeStepControler import wave_step
from mcp3208 import MCP3208
import time
from random import randint
# Create input on channel 0 of MCP3208
adc_photo = MCP3208()
# adc_photo = []            #------------------Change to test on pc ------------
# start of GUI design
sg.ChangeLookAndFeel('DarkBlue')

def _mean_list(list):
    return sum(list)/len(list)

def sample_measure(adc_photo, SAMPLES=180):
    '''180 is roughly 10 ms of measurement time'''
    '''.return the mean value of SAMPLES measures of the mcp3208.'''
    measure_photo = [None]*SAMPLES
    start = time.monotonic()
    for i in range (0, SAMPLES):
        measure_photo[i] = adc_photo.read(0)    #------------------Change to test on pc ------------
        # measure_photo[i] = randint(0, 4100)
    currend = time.monotonic()
    mean_photo = _mean_list(measure_photo)
    elapsed_time = currend - start
    return mean_photo, elapsed_time

def manual_control(pin_list_ex, pin_list_em):
    # Defaut mono values
    ex_val = 4000
    em_val = 3000
    RATE = 100
    sg.SetOptions(text_justification='left')
    layout_manualControl = [
        [sg.Text('Manual Control', font=('Helvetica', 16))],
        [sg.Radio('Excitation', 'control', default=True, key='ex'), sg.Radio('Emission', 'control', key='em')],
        [sg.Button('', size=(8, 1), key='-100', image_filename='GUI/assets/buttons/-100.png', image_size=(60,60), border_width=0), 
            sg.Button('', size=(7, 1), key='-10', image_filename='GUI/assets/buttons/-10.png', image_size=(60,60), border_width=0),
            sg.Button('', size=(7, 1), key='-1', image_filename='GUI/assets/buttons/-1.png', image_size=(60,60), border_width=0), 
            sg.Button('', size=(7, 1), key='-0.1', image_filename='GUI/assets/buttons/-0.1.png', image_size=(60,60), border_width=0),
            sg.Button('', size=(7, 1), key='+0.1', image_filename='GUI/assets/buttons/+0.1.png', image_size=(60,60), border_width=0),
            sg.Button('', size=(7, 1), key='+1', image_filename='GUI/assets/buttons/+1.png', image_size=(60,60), border_width=0), 
            sg.Button('', size=(8, 1), key='+10', image_filename='GUI/assets/buttons/+10.png', image_size=(60,60), border_width=0), 
            sg.Button('', size=(7, 1), key='+100', image_filename='GUI/assets/buttons/+100.png', image_size=(60,60), border_width=0)
        ],
        [sg.Button('Set value', size=(10,1), key='set_btn'), 
            sg.Button('Go to value', size=(10,1), key='goto_btn'), 
            sg.Input(size=(6,1), key='set_goto_val')],
        [sg.Text('Current excitation: ', size=(22, 1)), 
            sg.Text(str(ex_val/10), justification='right', size=(5, 1), key='ex_val')],
        [sg.Text('Current emition: ', size=(22, 1)), 
            sg.Text(str(em_val/10), justification='right', size=(5, 1), key='em_val')],
        [sg.Text('Measure: ', size=(22, 1)), 
            sg.Text('0', size=(22,1), justification='right', key='measure')],
        [sg.Graph(canvas_size=(460, 270), graph_bottom_left=(0,0), 
                  graph_top_right=(3*RATE, 4100), background_color='white', key='graph')],
        [sg.Submit(), sg.Quit()]

    ]
    i=0
    points = [(i, .01) for i in range (0, 3*RATE)]
    window_manualControl = sg.Window('SPEX control', layout_manualControl)
    window_manualControl.Finalize()
    graph = window_manualControl['graph']

    while True:
        manCtrl_event, values = window_manualControl.read(timeout=10)
        
        # quit condition
        if manCtrl_event in (None, 'Quit'):
            window_manualControl.close()
            return None
            
        if manCtrl_event=='Submit':
            break
        
        #Set and goto buttons handler
        if manCtrl_event=='set_btn':
            try:
                temp_val = int(float(values['set_goto_val'])*10)
                if values['ex']:
                    ex_val = temp_val
                    window_manualControl['ex_val'].Update(ex_val/10)
                else:
                    em_val = temp_val
                    window_manualControl['em_val'].Update(em_val/10)
            except:
                sg.PopupOK('Escreva um número (use ponto para o decimal)', title='Erro')
            window_manualControl['set_goto_val'].Update('')
            
        if manCtrl_event=='goto_btn':
            try:
                temp_val = int(float(values['set_goto_val'])*10)
                if values['ex'] is True:
                    delta_val = temp_val - ex_val
                    ex_val = temp_val
                    window_manualControl['ex_val'].Update(ex_val/10)
                    # we go a little behind (2nm) to avoid hysteresis
                    wave_step(delta_val/10 - 2, pin_list_ex)
                    wave_step(2, pin_list_ex)
                else:
                    delta_val = temp_val - em_val
                    em_val = temp_val
                    window_manualControl['em_val'].Update(em_val/10)
                    # we go a little behind (2nm) to avoid hysteresis
                    wave_step(delta_val/10 - 2, pin_list_em)
                    wave_step(2, pin_list_em)
            except:
                sg.PopupOK('Escreva um número (use ponto para o decimal)', title='Erro')
            window_manualControl['set_goto_val'].Update('')
        
        #Step Motor control handler
        if manCtrl_event in ('-100', '-10', '-1', '-0.1', '+100', '+10', '+1', '+0.1'):
            val = int(float(manCtrl_event)*10)
            if values['ex']:
                wave_step(val/10, pin_list_ex)
                ex_val = ex_val + val
                window_manualControl['ex_val'].Update(ex_val/10)
            else:
                wave_step(val/10, pin_list_em)
                em_val = em_val + val
                window_manualControl['em_val'].Update(em_val/10)
        
        #'Real Time' measurement handler
        graph.Erase()
        if i >= 3*RATE:
            i = 0
        data, measure_time = sample_measure(adc_photo)
        points[i] = (i, data)
        for j in range (0, 3*RATE):
            graph.DrawPoint((points[j]), 3, color='green')
        window_manualControl['measure'].Update('{0:.4f}, '.format(data) + '{0:.3f}'.format(measure_time))
        i = i + 1
        
    dic = {'nm_pos_ex': ex_val/10, 'nm_pos_em': em_val/10}
    window_manualControl.close()
    return dic