import PySimpleGUI as sg 
import pickle as p

sg.ChangeLookAndFeel('DarkBlue')

userlist = p.load(open('users.p', 'rb'))



'''
layout_areyousure = [
	[sg.Text('Are you sure?')],
	[sg.Button('Yes'), sg.Button('No')]
]'''

def login():
	while True:
		layout_login = [
			[sg.Text('User'), sg.InputCombo(userlist, key='input_user')],
			[sg.Button('Login'), sg.Button('Delete User'),sg.Button('New User')]
		]


		window = sg.Window('SPEX control', layout_login)

		event, values = window.read()

		window.close()

		if event=='New User':
			layout_newuser = [
				[sg.Text('User name: '), sg.InputText(focus=True)],
				[sg.Cancel(), sg.Submit()]
			]

			window2 = sg.Window('NewUser', layout_newuser)
			event2, values2 = window2.read()
			window2.close()
			if len(values2[0]) == 0 or values2[0] in userlist:
				if len(values2[0]) == 0:
					sg.PopupOK('Coloca nome direito caralho.')
				if values2[0] in userlist:
					sg.PopupOK('Clones não são bem vindos aqui.')
			else:
				userlist.append(values2[0])	
				p.dump(userlist, open('users.p', 'wb'))

		if event=='Delete User':
			if len(values['input_user']) > 0 :
				popup = sg.PopupYesNo('Are you sure you want to delete your whole research?')
				if popup=='Yes':
					userlist.remove(values['input_user'])
					p.dump(userlist, open('users.p', 'wb'))
			else:
				popup = sg.PopupOK('Select user to delete on last screen first.')

		if event==None:
			break

		if event=='Login':
			p.dump(userlist, open('users.p', 'wb'))
			window.close()
			return values['input_user']

