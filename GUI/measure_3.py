import PySimpleGUI as sg 
import time
from math import floor

#for test purposes ONLY
import random as rnd

sg.ChangeLookAndFeel('DarkBlue')

#varables from setup
nm_start = 400
nm_stop = 600
nm_step = 1
time_step = 0.1
samples_per_second = 16
samples_per_measurement = floor(samples_per_second*time_step)

#process calculation
nm_pos = nm_start
sample_list = []
measurement = []

#dummy values
measure_time = 1/samples_per_second

layout_measure = [
	[sg.Text('Measuring: '), sg.Text(str(nm_pos), size=(3, 1), key='text.nm')],
	[sg.Text('Sample number: '), sg.Text(str(len(sample_list)), size=(2, 1), key='text.sample')],
	[sg.Button('Pause'), sg.Button('Resume'), sg.Button('Quit')] 
]

window = sg.Window('Working...', layout_measure)


while True:
	event, values = window.read(timeout=10)
	if event == 'Pause':
		event, values = window.read()
	if event == 'Quit' or None:
		break
	#simulate measurement time
	time.sleep(measure_time)
	#get simulated value
	sample_list.append(rnd.random())
	if len(sample_list) == samples_per_measurement: #took all measurements in the set 
		print((nm_pos, sum(sample_list)))
		measurement.append((nm_pos, sum(sample_list)))
		sample_list = []
		nm_pos += nm_step
	if nm_pos > nm_stop: #the experiment has ended
		break
	#update window
	window.Element('text.nm').update(str(nm_pos))
	window.Element('text.sample').update(str(len(sample_list)))

window.close()
