import time
import pickle
import PySimpleGUI as sg
from layout_directive_definitions import Gelem, BlockLD, BlockLI, TreeNodeLI
import layout_generator_step_by_step as lg

button_gelem = Gelem(sg.Button,  sty={"auto_size_button": 'False',
                                      "size": (8, 4)
                                      }, ex_toggle_attrs=[('button_color',  (
                                          ('white', 'green'), ('blue', 'black')))])

bld1 = BlockLD([('k_', button_gelem)], stacked='H', framed=True)

# create two instance of bld1 with labels A and B
bli1 = BlockLI(bld1, [(['A'], ['']), (['B'], [''])], stacked='V', framed=True)


bli1 = BlockLI.bli_single([('my button', button_gelem)])

tnli = TreeNodeLI(bli1,
                  None,  stacked='H', framed=True)

lg.set_li_layout(tnli)
the_layout = lg.compose_layout_li(tnli)
print(the_layout)

layout = []
exit_button_row = [[
    sg.Button('Exit')
]
]
layout = layout + [[the_layout]] + exit_button_row
window = sg.Window('PGAppAnalytics', layout)
while True:
    event, values = window.read()
    print("event pressed = ", event)
    if event == 'Exit':
        break
window.close()
