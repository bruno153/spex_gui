import PySimpleGUI as sg
from time import sleep


gif = 'assets/frames_png/'

layout = [  [sg.Text('Loading....', font='ANY 15')],
            [sg.Image('assets/frames_png/0038.png', key='_IMAGE_')],
           [sg.Button('Cancel')]
         ]

window = sg.Window('My new window').Layout(layout)

for i in range(1, 101):
	event, values = window.Read(timeout=25)
	if event in (None, 'Exit', 'Cancel'):
		break
	print(gif+"{:04d}".format(i)+'.png')
	window.Element('_IMAGE_').Update(gif+"{:04d}".format(i)+'.png')
	window.Refresh()