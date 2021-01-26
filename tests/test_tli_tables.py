import time
import pickle
import PySimpleGUI as sg
from layout_directive_definitions import Gelem, BlockLD, BlockLI, TreeNodeLI, ListNodeLI
import layout_generator_step_by_step as lg

text_gelem = Gelem(sg.Text,  sty={"auto_size_text": 'False',
                                  "size": (8, 4)
                                  })

# a row template with 2 cols
rowT = BlockLD([('lc_', text_gelem), ('rc_', text_gelem)])
bli = BlockLI(rowT, [('k1', 'v1'), ('k2', 'v2'), ('k3', 'v3')], stacked='V')

keys_values_set = [(('ak1', 'ak2', 'ak3'), ('av1', 'av2', 'av3')),
                   (('bk1', 'bk2', 'bk3'), ('bv1', 'bv2', 'bv3')),
                   (('ck1', 'ck2', 'ck3'), ('cv1', 'cv2', 'cv3')),
                   ]


def cb_gen(tid): return BlockLI.bli_single(
    [tid, Gelem(sg.Checkbox, {'text': 'tbl ' + tid})], (tid,))


tli = ListNodeLI([TreeNodeLI(cb_gen(str(idx)),
                             BlockLI(rowT, [(k, v) for k, v in zip(
                                 keys, values)], stacked='V', framed=True), stacked='V'
                             )
                  for idx, (keys, values) in enumerate(keys_values_set)])
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
