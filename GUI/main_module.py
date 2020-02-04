import PySimpleGUI as sg
import pickle as p

from window_exp_setup import exp_setup
from window_measure import measure
from window_login import login


user = login()
if user == None:
	exit()

print(user)
values = exp_setup()
measure(values)
