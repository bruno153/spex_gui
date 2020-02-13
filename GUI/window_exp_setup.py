import PySimpleGUI as sg
from window_manual_control import manual_control

sg.ChangeLookAndFeel('DarkBlue')


def exp_setup(pin_list):
	sg.SetOptions(text_justification='left')
	layout = [
		[sg.Text('Experiment', size=(20,1)), sg.Radio('Excitation', 'RADIO1', default=True, enable_events=True, key='radio_ex'),
			sg.Radio('Emission', 'RADIO1',  enable_events=True, key='radio_em'), sg.Radio('Kinectics', 'RADIO1', enable_events=True, key='radio_ki')],
		[sg.Text('Excitation', size=(20,1)), sg.Input('400', size=(4,1), key='input_ex_st'), sg.Text('nm', justification='left'),
			sg.Input('600', size=(4,1), key='input_ex_en'), sg.Text('nm', justification='left')],
		[sg.Text('Emission', size=(20,1)), sg.Input('300', size=(4,1), key='input_em_st'), sg.Text('nm', justification='left'),
			sg.Input(size=(4,1), disabled=True, key='input_em_en'), sg.Text('nm', justification='left')],
		[sg.Text('Increment', size=(20,1)), sg.Input('1', size=(4,1), key='input_in_nm'), 
			sg.Text('nm', justification='left'), sg.Input(size=(4,1), disabled=True, key='input_in_s'), sg.Text('s', justification='left')],
		[sg.Text('Integration time', size=(20,1)), 
			sg.Slider(range=(1, 30), orientation='h', size=(20, 20), default_value=1, key='integration_time', enable_events=True, disable_number_display=True), 
			sg.Text('0.1 s', justification='left', key='text.slider')],
		[sg.Text('Total reaction time', size=(20,1)), sg.Input(size=(4,1), disabled=True, key='input_ti'), sg.Text('s', justification='left')],
		[sg.Text('Measure: ', size=(20,1)), sg.Text('0.0', size=(4,1), key='measure')],
		[sg.Button('Submit'), sg.Quit()]
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

		if event=='integration_time':
			window.Element('text.slider').Update(str(values['integration_time']/10)+' s')
		
		# if event=='manual_control':
			# manual_control()
		
		if event in (None, 'Quit'):
			window.close()
			return None
		if event=='Submit':
			break

		#print(event)
	window.close()
	
	for i in values:
		try:
			values[i] = int(values[i])
		except:
			pass


	values['integration_time'] = values['integration_time']/10
	return values
