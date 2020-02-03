import PySimpleGUI as sg 
import time

sg.ChangeLookAndFeel('DarkBlue')

layout_measure = [
	[sg.Text('0', key='text', size=(3,1))],
	[sg.Button('Pause'), sg.Button('Resume'), sg.Button('Quit')]
]

window = sg.Window('Working...', layout_measure)

measured = 0

while True:
	event, values = window.read(timeout=10)

	
	if event == 'Pause':
		event, values = window.read()
	if event == 'Quit' or None:
		break
	time.sleep(1)
	measured=measured+1
	window.Element('text').update(str(measured))

window.close()
