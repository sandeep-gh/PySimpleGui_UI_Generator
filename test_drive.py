import PySimpleGUI as sg
from layout_directive_definitions import Gelem, BlockLayoutTemplate, BlockLayoutDirective
import layout_generator_step_by_step as lg

blt = BlockLayoutTemplate("a block", 'H', False, [
    Gelem("button1", "button 1", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  }),
    Gelem("button2", "button 2", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  })
]
)

tlt
bld = BlockLayoutDirective("many of one ", blt, [
                           "A", "B"], stacked='H', framed=False)
the_layout = lg.get_layout_blockset(bld)
layout = []
exit_button_row = [[
    sg.Button('Exit')
]
]
print(the_layout)
#layout = layout + [[the_layout]] + exit_button_row
layout = layout + the_layout + exit_button_row

window = sg.Window('PGAppAnalytics', layout)

# # # print(slider_state)
while True:
    event, values = window.read()
    if event == 'Exit':
        break
window.close()
