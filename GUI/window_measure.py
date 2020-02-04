import PySimpleGUI as sg 
import time
from math import floor

#for test purposes ONLY
import random as rnd

sg.ChangeLookAndFeel('DarkBlue')

def waveToSteps(wave):
    wave2 = wave	
    rate = 5 # steps/nm
    return int(rate*wave2)


def measure(values, pin_list):
	#varables from setup
	if values['radio_ex'] == 1:
		nm_start = values['input_ex_st']
		nm_stop = values['input_ex_en']
	else:
		nm_start = values['input_em_st']
		nm_stop = values['input_em_en']
	nm_step = values['input_in_nm']
	time_step = values['integration_time']
	samples_per_second = 16
	samples_per_measurement = floor(samples_per_second*time_step)

	#process calculation
	nm_pos = values['nm_pos']
	sample_list = []
	measurement = []

	#dummy values
	measure_time = 1/samples_per_seconds

	#set to initial position
	manual_step(waveToSteps(nm_start-nm_pos))
	nm_pos = nm_start

	#setup GUI

	layout_measure = [
		[sg.Text('Measuring: '), sg.Text(str(nm_pos), size=(3, 1), key='text.nm')],
		[sg.Text('Sample number: '), sg.Text(str(len(sample_list)), size=(2, 1), key='text.sample')],
		[sg.Graph(canvas_size=(1200, 300), graph_bottom_left=(nm_start-5,-20), graph_top_right=(nm_stop+5,120), background_color='white', key='graph', tooltip='This is a cool graph!')],
		[sg.Button('Pause'), sg.Button('Resume'), sg.Button('Quit')] 
	]

	window = sg.Window('Working...', layout_measure)
	window.finalize()
	graph = window['graph']

	#draw axis
	graph.DrawLine((nm_start, 0), (nm_stop, 0))

	for x in range(nm_start, nm_stop+1, 20):    
	    graph.DrawLine((x,-3), (x,3))    
	    if x != 0:    
	        graph.DrawText( x, (x,-10), color='green')


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
			measurement.append((nm_pos, sum(sample_list)/len(sample_list)*100))

			#draw a line between the last two measurements
			#if there's at least two elements in the measurement
			if len(measurement) > 1:
				graph.DrawLine(measurement[-1], measurement[-2])
			
			sample_list = []
			nm_pos += nm_step
			
			#move stepper
			manual_step(waveToSteps(nm_step))
		if nm_pos > nm_stop: #the experiment has ended
			break
		#update window
		window.Element('text.nm').update(str(nm_pos))
		window.Element('text.sample').update(str(len(sample_list)))


	window.read()
	window.close()