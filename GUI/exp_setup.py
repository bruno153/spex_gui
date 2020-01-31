import PySimpleGUI as sg
import pickle as p

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
	[sg.Text('Total reaction time', size=(20,1)), sg.Input(size=(4,1), disabled=True, key='input_ti'), sg.Text('s', justification='left')]
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

	if event==None:
		break
	print(event)

window.close()
