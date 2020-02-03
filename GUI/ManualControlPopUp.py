# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import pickle as p
from math import sin

sg.ChangeLookAndFeel('DarkBlue')

exVal = 400.0
emVal = 300.0

sg.SetOptions(text_justification='left')
layout_manualControl = [
   [sg.Text('Manual Control', font=('Helvetica', 16))],
   [sg.Radio('Excitation', 'control', default=True, key='ex'), sg.Radio('Emission', 'control', key='em')],
   [sg.Button('-100 nm', size=(8, 1), key='-100'), sg.Button('-10 nm', size=(7, 1), key='-10'), sg.Button('-1 nm', size=(7, 1), key='-1'), sg.Button('-0.1 nm', size=(7, 1), key='-0.1')],
   [sg.Button('+100 nm', size=(8, 1), key='+100'), sg.Button('+10 nm', size=(7, 1), key='+10'), sg.Button('+1 nm', size=(7, 1), key='+1'), sg.Button('+0.1 nm', size=(7, 1), key='+0.1')],
   [sg.Text('Current excitation: ', size=(15, 1)), sg.Text(str(exVal), size=(4, 1), key='exVal')],
   [sg.Text('Current emition: ', size=(15, 1)), sg.Text(str(emVal), size=(4, 1), key='emVal')],
   [sg.Text('Measure: ', size=(15, 1)), sg.Text('0', size=(4,1), justification='right', key='measure')],
   [sg.Graph(canvas_size=(270, 270), graph_bottom_left=(0,0), graph_top_right=(200, 200), background_color='white', key='graph')],
   [sg.Quit()]

]
x=0
i=0
points = [(i, 100) for i in range (0, 200)]
window_manualControl = sg.Window('SPEX control', layout_manualControl)
window_manualControl.Finalize()
graph = window_manualControl['graph']

while True:
     manCtrl_event, values = window_manualControl.read(timeout=10)
     if manCtrl_event in (None, 'Quit'):
          break

     elif manCtrl_event in ('-100', '-10', '-1', '-0.1', '+100', '+10', '+1', '+0.1'):
          val = float(manCtrl_event)
          if values['ex']:
               exVal = exVal + val
               window_manualControl['exVal'].Update('{0:.1f}'.format(exVal))
          else:
               emVal = emVal + val
               window_manualControl['emVal'].Update('{0:.1f}'.format(emVal))

     graph.Erase()
     if i >= 200:
          i = 0
     points[i] = (i, 100*sin(3.1415629*1310*x) + 100)
     for j in range (0, 200):
          graph.DrawPoint((points[j]), 1, color='green')
     window_manualControl['measure'].Update('{0:.1f}'.format(100*sin(3.1415629*1310*x) + 100))
     x = x + 1
     i = i + 1

window_manualControl.close()
