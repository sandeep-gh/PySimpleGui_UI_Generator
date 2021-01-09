# generates event handling code for layout
import os
from string import Template
import layout_directive_definitions as lddm
from layout_generator_step_by_step import get_key_from_label
import ast
from ast import Pass

action_body = """
def on_event(window, event):
\tif event in event_toggler_dict:
\t\tfor exclusive_toggler in event_toggler_dict[event]:
\t\t\texclusive_toggler.set_active(window, event)
\tevent_app_action_module = importlib.import_module("${lid}_app_actions")
\tappstate=None
\tprint("calling = ", "on_" + event + "_click")
\tgetattr(event_app_action_module, "on_" + event + "_click")(window, appstate)
"""


def get_funcs_in_module(module_name):
    root = ast.parse(open(module_name).read())
    defined_funcs = set([anode.name for anode in ast.walk(
        root) if isinstance(anode, ast.FunctionDef)])
    return defined_funcs


def add_func_to_ast(func_name, ast_root,  defined_funcs):
    if func_name in defined_funcs:
        return
    fn_args = ast.arguments([ast.arg('event'), ast.arg('appstate')], [], None, [], None,
                            None, [])
    afuncNode = ast.FunctionDef(
        func_name, args=fn_args, decorator_list=[], lineno=None, body=[Pass()], types_ignores=[])
    ast_root.body.append(afuncNode)


def gen_app_actions_bld(bld, labels, add_event_to_ast):
    for gelem in bld.layout_seq:
        for label in labels:
            event_name = gelem.gid + get_key_from_label(label)
            func_name = "on_" + event_name + "_click"
            add_event_to_ast(func_name)


def gen_event_action_lookup_bld(bld, labels, lid, fh):
    '''
    generate event-name -to-> event_action mapping
    '''

    adict = {}
    for gelem in bld.layout_seq:
        for label in labels:
            event_name = gelem.gid + get_key_from_label(label)
            adict[event_name] = lid + "_event_actions"

    adict_str = str(adict).replace(
        "'" + lid + "_event_actions" + "'", lid + "_event_actions")
    fh.write(lid + "_dict = " + adict_str + "\n")
    fh.write(
        "everything_bagel_dict = {**everything_bagel_dict, **" + lid + "_dict}\n")


def walk_tld(tnld):
    if isinstance(tnld.left_ld, lddm.BlockLD):
        yield tnld.left_ld
    if isinstance(tnld.left_ld, lddm.TreeNodeLD):
        walk_tld(tnld.left_ld)

    if isinstance(tnld.right_ld, lddm.BlockLD):
        yield tnld.right_ld
    if isinstance(tnld.right_ld, lddm.TreeNodeLD):
        walk_tld(tnld.rigt_ld)


def gen_event_actions(tnld, labels):
    lid = "test_bld"
    # -------------------------- codegen setup --------------------------------------------
    fh = open("everything_bagel_dictionary.py", "w")
    fh.write(Template("import ${lid}_event_actions\n").substitute(
        lid=lid))
    fh.write("everything_bagel_dict = {}\n")
    if os.path.exists(lid + "_app_actions.py"):
        defined_funcs = get_funcs_in_module(lid + "_app_actions.py")
        apps_event_ast_root = ast.parse(open(lid + "_app_actions.py").read())
    else:
        defined_funcs = set()
        apps_event_ast_root = ast.parse("")

    def event_ast_adder(func_name, apps_event_ast_root=apps_event_ast_root,
                        defined_funcs=defined_funcs): return add_func_to_ast(func_name, apps_event_ast_root, defined_funcs)
    # event_actions.py header
    ea_code_fh = open(lid
                      + "_event_actions.py", "w")
    ea_code_fh.write(
        "from everything_bagel_common import ToggleExclusive, ToggleExclusiveOther\n")
    ea_code_fh.write("import importlib\n")
    ea_code_fh.write("all_togglers = [" + "]\n")
    ea_code_fh.write("event_toggler_dict = {}\n")

    # -------------------------- codegen body - --------------------------------------------
    for bld in walk_tld(tnld):
        gen_event_action_lookup_bld(bld, labels, lid, fh)
        # app_actions.py body
        gen_app_actions_bld(bld, labels, event_ast_adder)

    # -------------------------- codegen closeout -------------------------------------------
    fh.write("""def everything_bagel(window, event):\n
    \tif event in everything_bagel_dict:\n
    \t\teverything_bagel_dict[event].on_event(window, event)""")
    fh.close()
    with open(lid + "_app_actions.py", "w") as fh:
        fh.write(ast.unparse(apps_event_ast_root))

    # event_actions.py on_action command
    ea_code_fh.write(
        Template(action_body).substitute(lid=lid))
    ea_code_fh.close()