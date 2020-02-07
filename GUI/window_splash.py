import PySimpleGUI as sg


def splash():
	gif = 'assets/frames_png/'
	layout = [  
	            [sg.Image('assets/frames_png/0001.png', key='_IMAGE_', background_color='blue')]
	         ]

	window = sg.Window('My new window', no_titlebar=True, background_color='blue', transparent_color='blue', keep_on_top = True).Layout(layout)

	for i in range(1, 101):
		event, values = window.Read(timeout=10)
		if event in (None, 'Exit', 'Cancel'):
			break
		window.Element('_IMAGE_').Update(gif+"{:04d}".format(i)+'.png')
		window.Refresh()
	window.close()