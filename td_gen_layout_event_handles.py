import PySimpleGUI as sg
import time
from layout_directive_definitions import Gelem, BlockLD
from layout_directive_definitions import TreeNodeLD
import random
import event_codegen as ecm
import layout_generator_step_by_step as lg
from everything_bagel_dictionary import everything_bagel
import event_codegen as ecm

bld1 = BlockLD([
    Gelem("button1", "button 1", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  }),
    Gelem("button2", "button 2", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  })
], stacked='H', framed=True
)

bld2 = BlockLD([
    Gelem("text1", "text 1", sg.Text,  sty={"auto_size_text": 'False',
                                            "size": (8, 4)
                                            }),
    Gelem("text2", "text 2", sg.Text,  sty={"auto_size_text": 'False',
                                            "size": (8, 4)
                                            })
], stacked='H', framed=False
)

tnld = TreeNodeLD(bld1,
                  bld2,  stacked='H', framed=True)

for bld in ecm.walk_tld(tnld):
    print(bld)

lg.set_bld_layout_generator(tnld)
ecm.gen_event_actions(tnld, ['A', 'B'])
lgen = lg.get_layout_generator_tnld(tnld)
the_layout = lg.build_layout_set(
    lgen, ['A', 'B'], stacked='H', framed=False)

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
    everything_bagel(window, event)
window.close()
