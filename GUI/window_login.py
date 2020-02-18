import PySimpleGUI as sg 
import pickle as p
import os
import shutil

sg.ChangeLookAndFeel('DarkBlue')

userlist = p.load(open('users.p', 'rb'))



'''
layout_areyousure = [
    [sg.Text('Are you sure?')],
    [sg.Button('Yes'), sg.Button('No')]
]'''

def login():
    
    layout_login = [
            [sg.Text('User'), 
                sg.Listbox(userlist, size=(10, 2), key='input_user')],
            [sg.Button('Delete User'),sg.Button('New User'), sg.Button('Login')]
        ]

    window = sg.Window('SPEX control', layout_login)
    path = '/home/pi/Documents/SPEX_users'
    while True:
        event, values = window.read()

        if event=='New User':
            layout_newuser = [
                [sg.Text('User name: '), 
                    sg.InputText(focus=True)],
                [sg.Cancel(), sg.Submit()]
            ]

            window2 = sg.Window('NewUser', layout_newuser)
            event2, values2 = window2.read()
            window2.close()
            if event2 == 'Cancel':
                pass
            
            # values2[0]== string colocada no InputText
            elif len(values2[0]) == 0 or values2[0] in userlist:
                if len(values2[0]) == 0:
                    sg.PopupOK('Coloca nome direito caralho.')
                if values2[0] in userlist:
                    sg.PopupOK('Clones não são bem vindos aqui.')
            else:
                userlist.append(values2[0])
                p.dump(userlist, open('users.p', 'wb'))
                os.mkdir(path + values2[0], 0755)
                

        if event=='Delete User':
            try:
                if len(values['input_user'][0]) > 0:
                    popup = sg.PopupYesNo('Are you sure you want to delete your whole research?\n Make sure you have a back up of your results.')
                    if popup=='Yes':
                        shutil.rmtree(path + values['input_user'][0])
                        userlist.remove(values['input_user'][0])
                        p.dump(userlist, open('users.p', 'wb'))
            except:
                popup = sg.PopupOK('Select user to delete on last screen first.')

        if event==None:
            window.close()
            return None

        if event=='Login':
            if len(values['input_user']) == 0:
                sg.PopupOK('Please select a user.')
            else:
                p.dump(userlist, open('users.p', 'wb'))
                window.close()
                return values['input_user']

