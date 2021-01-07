import PySimpleGUI as sg
import time
from layout_directive_definitions import Gelem, BlockLD
from layout_directive_definitions import TreeNodeLD
import layout_generator_step_by_step as lg
import random


def get_the_layout():
    def frame_choice(): return random.choice([True, False])
    def stack_choice(): return random.choice(['H', 'V'])

    bld1 = BlockLD([
        Gelem("button1", "button 1", sg.Button,  sty={"auto_size_button": 'False',
                                                      "size": (8, 4)
                                                      }),
        Gelem("button2", "button 2", sg.Button,  sty={"auto_size_button": 'False',
                                                      "size": (8, 4)
                                                      })
    ], stacked=stack_choice(), framed=frame_choice()
    )

    bld2 = BlockLD([
        Gelem("text1", "text 1", sg.Text,  sty={"auto_size_text": 'False',
                                                "size": (8, 4)
                                                }),
        Gelem("text2", "text 2", sg.Text,  sty={"auto_size_text": 'False',
                                                "size": (8, 4)
                                                })
    ], stacked=stack_choice(), framed=frame_choice()
    )

    tnld = TreeNodeLD(bld1,
                      bld2,  stacked=stack_choice(), framed=frame_choice())
    lg.set_bld_layout_generator(tnld)
    lgen = lg.get_layout_generator_tnld(tnld)
    the_layout = lg.build_layout_set(
        lgen, ['A', 'B'], stacked=stack_choice(), framed=frame_choice())
    return the_layout


while True:
    the_layout = get_the_layout()
    layout = []
    exit_button_row = [[
        sg.Button('Exit')
    ]
    ]
    layout = layout + [[the_layout]] + exit_button_row
    window = sg.Window('PGAppAnalytics', layout)
    window.Finalize()
    while True:

        #event, values = window.read()
        event = 'Exit'
        time.sleep(2)

        if event == 'Exit':
            window.close()
            break
