# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import PySimpleGUI as sg
from math import sin
from Hardware.StepControler import wave_step

sg.ChangeLookAndFeel('DarkBlue')

def manual_control(pin_list_ex, pin_list_em):
	ex_val = 4000
	em_val = 3000

	sg.SetOptions(text_justification='left')
	layout_manualControl = [
		[sg.Text('Manual Control', font=('Helvetica', 16))],
		[sg.Radio('Excitation', 'control', default=True, key='ex'), sg.Radio('Emission', 'control', key='em')],
		[sg.Button('-100 nm', size=(8, 1), key='-100'), sg.Button('-10 nm', size=(7, 1), key='-10'),
		sg.Button('-1 nm', size=(7, 1), key='-1'), sg.Button('-0.1 nm', size=(7, 1), key='-0.1')],
		[sg.Button('+100 nm', size=(8, 1), key='+100'), sg.Button('+10 nm', size=(7, 1), key='+10'), 
		sg.Button('+1 nm', size=(7, 1), key='+1'), sg.Button('+0.1 nm', size=(7, 1), key='+0.1')],
		[sg.Text('Current excitation: ', size=(13, 1)), sg.Text(str(ex_val/10), size=(5, 1), key='ex_val'), 
		sg.Button('Set value', size=(7,1), key='set_ex_btn'), sg.Input(size=(5,1), key='set_ex_val')],
		[sg.Text('Current emition: ', size=(13, 1)), sg.Text(str(em_val/10), size=(5, 1), key='em_val'),
		sg.Button('Set value', size=(7,1), key='set_em_btn'), sg.Input(size=(5,1), key='set_em_val')],
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

		if manCtrl_event=='set_ex_btn':
			ex_val = int(float(values['set_ex_val'])*10)
			window_manualControl['ex_val'].Update(ex_val/10)
			
		if manCtrl_event=='set_em_btn':
			em_val = int(float(values['set_em_val'])*10)
			window_manualControl['em_val'].Update(em_val/10)

		if manCtrl_event in ('-100', '-10', '-1', '-0.1', '+100', '+10', '+1', '+0.1'):
			val = int(float(manCtrl_event)*10)
			if values['ex']:
				wave_step(val, pin_list_ex)
				ex_val = ex_val + val
				window_manualControl['ex_val'].Update(ex_val/10)
			else:
				wave_step(val, pin_list_em)
				em_val = em_val + val
				window_manualControl['em_val'].Update(em_val/10)

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
	
# PARA RODAR A JANELA, BASTA DESCOMENTAR E RODAR window_manual_Control.py
#manual_control({},{})