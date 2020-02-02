import PySimpleGUI as sg 
import time

sg.ChangeLookAndFeel('DarkBlue')

layout_setup = [
	[sg.Text('Icrement: '), sg.InputText()],
	[sg.OK()]
]

window = sg.Window('Setup', layout_setup)

event, values = window.read()

window.close()

increment = float(values[0])

layout_measure = [
	[sg.Text('0', key='text')],
	[sg.Button('Pause'), sg.Button('Resume'), sg.Button('Quit')]
]

window = sg.Window('Working...', layout_measure)

paused = False
start_time = time.time()
measured = 10

while True:
	if not paused:
		event, values = window.read(timeout=10)
		current_time = time.time() # if not paused, update time
	else:
		print('paused')
		event, values = window.read() # if paused, wait for user input
		current_time = time.time() 
		start_time = start_time + (time.time() - paused_time)
		paused = False


	if event == 'Quit' or None:
		break
	if event == 'Pause':
		paused_time = time.time()
		paused == True

	if current_time - start_time > increment:
		start_time = time.time()
		measured = measured + 1
		window['text'].update(str(measured))

window.close()
