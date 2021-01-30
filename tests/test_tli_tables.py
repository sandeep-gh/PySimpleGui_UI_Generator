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

keys_values_set = [(('ak1', 'ak2', 'ak3'), ('av1', 'av2', 'av3')),
                   (('bk1', 'bk2', 'bk3'), ('bv1', 'bv2', 'bv3')),
                   (('ck1', 'ck2', 'ck3'), ('cv1', 'cv2', 'cv3')),
                   ]


def mlk2(ls1, ls2, key_suffix):
    '''
    this is for multiple instances of 2-wide bld

    '''
    if key_suffix is None:
        # make label the key suffix
        pass
    if isinstance(key_suffix, str):
        return [((x1, x2), (key_suffix, key_suffix)) for x1, x2 in zip(ls1, ls2)]
        pass

    return [((x1, x2), (ks, ks)) for x1, x2, ks in zip(ls1, ls2, key_suffix)]
    # TODO
    # if key_suffix is a simple list


# make_label_keysuffix([(k,v) for k, v in zip(keys, values)], str(ridx))
# for ridx, (keys, values) in enumerate(keys_values_set)])
tli = ListNodeLI([BlockLI(rowT, mlk2(keys, values, [str(tidx) + str(ridx) for ridx in range(len(keys))]), stacked='V', framed=True)
                  for tidx, (keys, values) in enumerate(keys_values_set)])
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
