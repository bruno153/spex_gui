import PySimpleGUI as sg 
import pickle as p
import os
import shutil
from pathlib import Path

sg.ChangeLookAndFeel('DarkBlue')
try:
    userlist = p.load(open('users.p', 'rb'))
except:
    raise
path = Path.home()/'Documents'/'SPEX_users'


'''
layout_areyousure = [
    [sg.Text('Are you sure?')],
    [sg.Button('Yes'), sg.Button('No')]
]'''

def login():
    global path
    layout_login = [
            [sg.Text('User'), 
                sg.Listbox(userlist, size=(10, 2), key='input_user')],
            [sg.Button('Delete User'),sg.Button('New User'), sg.Button('Login')]
        ]

    window = sg.Window('SPEX control', layout_login)
    while True:
        event, values = window.read()
        window.close()
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
                path_new = path/values2[0]
                path_new.mkdir()                

        if event=='Delete User':
            try:
                if len(values['input_user'][0]) > 0:
                    popup = sg.PopupYesNo('Are you sure you want to delete your whole research?\n Make sure you have a back up of your results.')
                    if popup=='Yes':
                        path_new = path/values['input_user']
                        shutil.rmtree(path_new)
                        userlist.remove(values['input_user'][0])
                        p.dump(userlist, open('users.p', 'wb'))
            except:
                popup = sg.PopupOK('Select user to delete on last screen first.')

        if event==None:
            return None, None

        if event=='Login':
            if len(values['input_user']) == 0:
                sg.PopupOK('Please select a user.')
            else:
                p.dump(userlist, open('users.p', 'wb'))
                path = path/values['input_user']
                window.close()
                return values['input_user'], path

