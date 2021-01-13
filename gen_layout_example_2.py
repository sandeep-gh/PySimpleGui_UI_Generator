import time
import pickle
import PySimpleGUI as sg
from layout_directive_definitions import Gelem, BlockLD, BlockLI
from layout_directive_definitions import TreeNodeLD, TreeNodeLI
import layout_generator_step_by_step as lg
import event_codegen as ecm

bld1 = BlockLD([
    Gelem("button1", "button 1", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  }, ex_toggle_attrs=[('button_color',  (
                                                      ('white', 'green'), ('blue', 'black')))]),
    Gelem("button2", "button 2", sg.Button,  sty={"auto_size_button": 'False',
                                                  "size": (8, 4)
                                                  })
], stacked='H', framed=True
)

bli1 = BlockLI(bld1, ['A', 'B'])

bld2 = BlockLD([
    Gelem("text1", "text 1", sg.Text,  sty={"auto_size_text": 'False',
                                            "size": (8, 4)
                                            }),
    Gelem("text2", "text 2", sg.Text,  sty={"auto_size_text": 'False',
                                            "size": (8, 4)
                                            })
], stacked='H', framed=False
)

bli2 = BlockLI(bld2, ['A', 'B'])

tnli = TreeNodeLI(bli1,
                  bli2,  stacked='H', framed=True)

lg.set_tnli_layout(tnli)
the_layout = lg.compose_layout_li(tnli)

ecm.gen_event_actions_li(tnli)

with open("ex2_layout.p", "wb") as fh:
    pickle.dump(the_layout, fh)
