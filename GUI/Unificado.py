# -*- coding: utf-8 -*-

import PySimpleGUI as sg
import pickle as p
from math import sin

sg.ChangeLookAndFeel('DarkBlue')

sg.SetOptions(text_justification='left')
layout = [
	[sg.Text('Experiment', size=(20,1)), sg.Radio('Excitation', 'RADIO1', default=True, enable_events=True, key='radio_ex'),
		sg.Radio('Emission', 'RADIO1',  enable_events=True, key='radio_em'), sg.Radio('Kinectics', 'RADIO1', enable_events=True, key='radio_ki')],
	[sg.Text('Excitation', size=(20,1)), sg.Input(size=(4,1), key='input_ex_st'), sg.Text('nm', justification='left'),
		sg.Input(size=(4,1), key='input_ex_en'), sg.Text('nm', justification='left')],
	[sg.Text('Emission', size=(20,1)), sg.Input(size=(4,1), key='input_em_st'), sg.Text('nm', justification='left'),
		sg.Input(size=(4,1), disabled=True, key='input_em_en'), sg.Text('nm', justification='left')],
	[sg.Text('Increment', size=(20,1)), sg.Input(size=(4,1), key='input_in_nm'), sg.Text('nm', justification='left'), sg.Input(size=(4,1), disabled=True, key='input_in_s'), sg.Text('s', justification='left')],
	[sg.Text('Integration time', size=(20,1)), sg.Input(size=(4,1)), sg.Text('s', justification='left')],
	[sg.Text('Total reaction time', size=(20,1)), sg.Input(size=(4,1), disabled=True, key='input_ti'), sg.Text('s', justification='left')],
   [sg.Text('Measure: ', size=(20,1)), sg.Text('0.0', size=(4,1))],
   [sg.Button('Open Manual Control', key='manual_control'), sg.Quit()]
]

window = sg.Window('SPEX control', layout)



while True:
	event, values = window.read()

	if event=='radio_em':
		window.Element('input_ex_en').Update(disabled=True)
		window.Element('input_em_en').Update(disabled=False)
		window.Element('input_ti').Update(disabled=True)
		window.Element('input_in_s').Update(disabled=True)
		window.Element('input_in_nm').Update(disabled=False)

	if event=='radio_ex':
		window.Element('input_ex_en').Update(disabled=False)
		window.Element('input_em_en').Update(disabled=True)
		window.Element('input_ti').Update(disabled=True)
		window.Element('input_in_s').Update(disabled=True)
		window.Element('input_in_nm').Update(disabled=False)

	if event=='radio_ki':
		window.Element('input_ex_en').Update(disabled=True)
		window.Element('input_em_en').Update(disabled=True)
		window.Element('input_ti').Update(disabled=False)
		window.Element('input_in_s').Update(disabled=False)
		window.Element('input_in_nm').Update(disabled=True)

	if event in (None, 'Quit'):
		break

	if event=='manual_control':
		#-----------POPUP-LAYOUT--------------------
		exVal = 400.0
		emVal = 300.0

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

		#-------------------------------
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




window.close()

