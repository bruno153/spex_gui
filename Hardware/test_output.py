import PySimpleGUI as sg

layout = [      
    [sg.Text('Script output....', size=(40, 1))],      
    [sg.Output(size=(88, 20))],      
    [sg.Button('script1'), sg.Button('script2'), sg.Button('EXIT')],      
    [sg.Text('Manual command', size=(15, 1)), sg.InputText(focus=True), sg.Button('Run', bind_return_key=True)]      
]

window = sg.Window('Script launcher', layout)

while True:
	event, values = window.read(timeout = 1000)
	print("hello!")
