import time
import pickle
import PySimpleGUI as sg
from layout_directive_definitions import Gelem, BlockLD, BlockLI, TreeNodeLI, ListNodeLI, TI, CI, SI, JI, EI
import layout_generator_step_by_step as lg


def text_gelem(): return Gelem(sg.Text,  sty={"auto_size_text": 'False',
                                              "size": (8, 4)
                                              })


row_gelems_t = [text_gelem(), text_gelem()]


def atbl_li(labelgi, suffixgi):
    return BlockLI.bli(row_gelems_t, ('lc_', 'rc_',), labelgi,
                       CI(suffixgi, SI()), sframed=True, sstacked='V')  # add column id to suffix


def all_tbl_li(all_tbl_labels):
    return ListNodeLI([atbl_li(tbl_labels, TI(idx, 2)) for idx, tbl_labels in EI(all_tbl_labels)])


tli = all_tbl_li([[('t1r1c1', 't1r1c2'), ('t1r2c1', 't1r2c2'),  ('t1r3c1', 't1r3c2')],
                  [('t2r1c1', 't1r1c2'), ('t2r2c1', 't2r2c2'),  ('t2r3c1', 't2r3c2')],
                  [('t3r1c1', 't3r1c2'), ('t3r2c1', 't3r2c2'),  ('t3r3c1', 't3r3c2')]
                  ]
                 )

lg.set_li_layout(tli)
the_layout = lg.compose_layout_li(tli)
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
