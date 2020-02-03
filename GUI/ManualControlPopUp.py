# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import pickle as p
from math import sin
from random import randint
sg.ChangeLookAndFeel('DarkBlue')

sg.SetOptions(text_justification='left')
layout_manualControl = [
   [sg.Text('Manual Control', font=('Helvetica', 16))],
   [sg.Radio('Excitation', 'control', default=True, enable_events=True, key='ex'), sg.Radio('Emission', 'control', enable_events=True, key='em')],
   [sg.Button('-100 nm', size=(8, 1)), sg.Button('-10 nm', size=(7, 1)), sg.Button('-1 nm', size=(7, 1)), sg.Button('-0.1 nm', size=(7, 1))],
   [sg.Button('+100 nm', size=(8, 1)), sg.Button('+10 nm', size=(7, 1)), sg.Button('+1 nm', size=(7, 1)), sg.Button('+0.1 nm', size=(7, 1))],
   [sg.Graph(canvas_size=(150, 150), graph_bottom_left=(0,0), graph_top_right=(200, 200), background_color='white', key='graph'),
    sg.Text('Valor medido: '), sg.Text('0',background_color='white', text_color='black', size=(3,1), key='medida')],
    [sg.Quit()]

]
x=0
i=0
points = [(i, 100) for i in range (0, 200)]
window_manualControl = sg.Window('SPEX control', layout_manualControl)
window_manualControl.Finalize()
graph = window_manualControl['graph']

while True:
     event, values = window_manualControl.read(timeout=10)
     if event is (None or 'Quit'):
          break

     if event=='ex':#----------------SETAR
          x=randint(0, 200)
          i = 0
          window_manualControl.Element('medida').Update(str(x))
     if event=='em':
          x=randint(0, 200)
          i = 0
     graph.Erase()
     if i >= 200:
          i = 0
     points[i] = (i, 100*sin(3.1415629*1310*x) + 100)
     for j in range (0, 200):
          graph.DrawPoint((points[j]), 1, color='green')
     x = x + 1
     i = i + 1
     print(event)
window_manualControl.close()
