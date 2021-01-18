import PySimpleGUI as sg
from everything_bagel_dictionary import everything_bagel
import pickle
with open("ex2_layout.p", "rb") as fh:
    the_layout = pickle.load(fh)
print(the_layout)
layout = []
exit_button_row = [[
    sg.Button('Exit')
]
]
appstate = None
layout = layout + [[the_layout]] + exit_button_row
window = sg.Window('PGAppAnalytics', layout)
while True:
    event, values = window.read()
    print("event pressed = ", event)
    if event == 'Exit':
        break
    everything_bagel(window, event, values, appstate)
window.close()
