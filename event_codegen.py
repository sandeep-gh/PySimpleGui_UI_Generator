# generates event handling code for layout
import os
from string import Template
import layout_directive_definitions as lddm
import ast
from ast import Pass
import re
from dataclasses import dataclass, make_dataclass, field
from typing import Any

action_body = """
def on_event(window, values, event, appstate):
\tif event in event_toggler_dict:
\t\tfor exclusive_toggler in event_toggler_dict[event]:
\t\t\texclusive_toggler.set_active(window, event)
\tevent_app_action_module = importlib.import_module("${lid}_app_actions")
\tprint("calling = ", "on_" + event + "_click")
\tgetattr(event_app_action_module, "on_" + event + "_click")(window, values, appstate)
"""

# - - - - - - - - - - - - - - - - - - ast funcs - - - - - - - - - - - - - - - - -


def get_funcs_in_module(module_name):
    root = ast.parse(open(module_name).read())
    defined_funcs = set([anode.name for anode in ast.walk(
        root) if isinstance(anode, ast.FunctionDef)])
    return defined_funcs


def add_func_to_ast(func_name, ast_root,  defined_funcs):
    if func_name in defined_funcs:
        return
    fn_args = ast.arguments([ast.arg('window'), ast.arg('values'), ast.arg('appstate')], [], None, [], None,
                            None, [])
    afuncNode = ast.FunctionDef(
        func_name, args=fn_args, decorator_list=[], lineno=None, body=[Pass()], types_ignores=[])
    ast_root.body.append(afuncNode)
    return afuncNode

# ........................................................................................

# - - - - - - - - - - - -  gen app/event actions - - - - - - - - - - - -


def get_ast_assignment_stmt(target, dictname, key):
    '''

    '''

    assign_stmt = ast.Assign(targets=[ast.Attribute(value=ast.Name(id='appstate', ctx=ast.Load()), attr=target, ctx=ast.Store())],
                             value=ast.Subscript(value=ast.Name(id=dictname, ctx=ast.Load()),
                                                 slice=ast.Index(value=ast.Constant(
                                                     value=key, kind=None)),
                                                 ctx=ast.Load()), type_comment=None, lineno=None)

    return assign_stmt


def add_ast_assignment_stmt_func(funcdefnode, stmts):
    '''

    '''
    idx = 0
    for stmt in stmts:
        funcdefnode.body.insert(idx, stmt)
        idx = idx+1


def add_assignment_ast_func(funcdefnode, target, dictname, key):
    '''
    adds statement: target = dictname[key] to ast
    '''

    assign_stmt = ast.Assign(targets=[ast.Attribute(value=ast.Name(id='appstate', ctx=ast.Load()), attr=target, ctx=ast.Store())],
                             value=ast.Subscript(value=ast.Name(id=dictname, ctx=ast.Load()),
                                                 slice=ast.Index(value=ast.Constant(
                                                     value=key, kind=None)),
                                                 ctx=ast.Load()), type_comment=None, lineno=None)

    funcdefnode.body.insert(0, assign_stmt)


def update_ast_func_appstate(gelem, label, func_name, ast_func):
    if gelem.appstate_attrib is not None:
        event_name = gelem.gid + get_key_from_label(label)
        add_assignment_ast_func(
            ast_func, gelem.appstate_attrib, "values", event_name)


def gen_app_actions_bld(bld, all_labels_keysuffix_pair, add_event_to_ast):
    appstate_attribs = []
    ast_assign_stmts = []
    inst_labelt = [_[0] for _ in all_labels_keysuffix_pair]
    inst_suffixt = [_[1] for _ in all_labels_keysuffix_pair]
    for gpos, (prefix, gelem) in enumerate(bld.layout_seq):
        gelem_labels = [_[gpos] for _ in inst_labelt]
        gelem_suffixs = [_[gpos] for _ in inst_suffixt]
        for (glabel, key_suffix) in zip(gelem_labels, gelem_suffixs):
            label, event_name = lddm.get_label_key(glabel, prefix, key_suffix)

            func_name = "on_" + event_name + "_click"
            ast_func = add_event_to_ast(func_name)
            if gelem.appstate_attrib is not None:
                ast_assign_stmts.append(get_ast_assignment_stmt(
                    gelem.appstate_attrib, "values", event_name))
                appstate_attribs.append(gelem.appstate_attrib)

    if ast_func is not None:  # if ast_func is not already been generated
        # we are assuming the last gelem is the submit button
        add_ast_assignment_stmt_func(ast_func, ast_assign_stmts)
    return appstate_attribs


def gen_event_action_lookup_bld(bld, all_labels_keysuffix_pair, lid, fh):
    '''
    generate event-name -to-> event_action mapping
    '''
    adict = {}

    for labelt, suffixt in all_labels_keysuffix_pair:
        for (prefix, gelem), label, suffix in zip(bld.layout_seq, labelt, suffixt):
            label, event_name = lddm.get_label_key(label, prefix, suffix)
            adict[event_name] = lid + "_event_actions"

    adict_str = str(adict).replace(
        "'" + lid + "_event_actions" + "'", lid + "_event_actions")
    fh.write(lid + "_dict = " + adict_str + "\n")
    fh.write(
        "everything_bagel_dict = {**everything_bagel_dict, **" + lid + "_dict}\n")

# .......................................................................................

# - - - - - - - - - - - - - - - - navigation function - - - - - - - - - - - - - - - -


def walk_tli(tnli):
    if isinstance(tnli.left_li, lddm.BlockLI):
        yield (tnli.left_li.bld, tnli.left_li.all_labels_keysuffix_pair)
    if isinstance(tnli.left_li, lddm.TreeNodeLI):
        walk_tli(tnli.left_li)

    if isinstance(tnli.right_li, lddm.BlockLI):
        yield (tnli.right_li.bld, tnli.right_li.all_labels_keysuffix_pair)
    if isinstance(tnli.right_li, lddm.TreeNodeLI):
        walk_tli(tnli.rigt_li)


def walk_tld(tnld):
    if isinstance(tnld.left_ld, lddm.BlockLD):
        yield tnld.left_ld
    if isinstance(tnld.left_ld, lddm.TreeNodeLD):
        walk_tld(tnld.left_ld)

    if isinstance(tnld.right_ld, lddm.BlockLD):
        yield tnld.right_ld
    if isinstance(tnld.right_ld, lddm.TreeNodeLD):
        walk_tld(tnld.rigt_ld)


# - - - - - - - - - - - - - - - - exclusive toggle - - - - - - - - - - - - - - - -

def gen_exclusive_toggle_code_snippet(gelem_name, toggle_attr, toggle_on_val, toggle_off_val, default_active):
    toggler_id = gelem_name + "_" + toggle_attr  # should be prefix name
    toggler_instance_expr = Template(
        "__${gelem_name}_${toggle_attr}_toggler=ToggleExclusive('${toggle_attr}', ${toggle_on_val}, ${toggle_off_val}, '${curr_active_elem}')").substitute(gelem_name=gelem_name,
                                                                                                                                                           toggle_attr=toggle_attr,
                                                                                                                                                           toggle_on_val=toggle_on_val,
                                                                                                                                                           toggle_off_val=toggle_off_val,
                                                                                                                                                           curr_active_elem=default_active
                                                                                                                                                           )

    return toggler_instance_expr


def gen_code_exclusive_toggle_gelem_attr(lid, prefix, gelem, toggle_attr, toggle_values,  default_event):

    toggler_inst_expr = gen_exclusive_toggle_code_snippet(
        prefix, toggle_attr, toggle_values[0], toggle_values[1], default_event
    )

    toggler_name = Template("__${gelem_name}_${toggle_attr}_toggler").substitute(
        gelem_name=prefix, toggle_attr=toggle_attr)
    return [toggler_name, toggler_inst_expr]


def gen_code_exclusive_toggle(lid, bld_walker, ea_code_fh):

    for (bld, all_labels_keysuffix_pair) in bld_walker():

        inst_labelt = [_[0] for _ in all_labels_keysuffix_pair]
        inst_suffixt = [_[1] for _ in all_labels_keysuffix_pair]
        for gpos, (prefix, gelem) in enumerate(bld.layout_seq):
            gelem_labels = [_[gpos] for _ in inst_labelt]
            gelem_suffixs = [_[gpos] for _ in inst_suffixt]

            if gelem.ex_toggle_attrs is not None:
                all_togglers = []
                toggler_declarations = []
                event_toggler_mapping = {}
                for attr, vals in gelem.ex_toggle_attrs.items():
                    [toggler_name, toggler_decl] = gen_code_exclusive_toggle_gelem_attr(lid, prefix,
                                                                                        gelem, attr, vals, (gelem_labels[0], gelem_suffixs[0]))
                    all_togglers.append(toggler_name)
                    toggler_declarations.append(toggler_decl)
                if all_togglers:
                    for label, key_suffix in gelem_labels, gelem_suffixs:
                        label, event_name = lddm.get_label_key(
                            label, prefix, key_suffix)
                        event_toggler_mapping[event_name] = all_togglers
                if toggler_declarations:
                    ea_code_fh.write("\n".join(toggler_declarations) + "\n")
                    ea_code_fh.write(
                        "all_togglers = all_togglers + [" + ",".join(all_togglers) + "]\n")

                    event_toggler_mapping_str = re.sub(
                        r'\'(__[^,]*toggler)\'(,|])', r"\1\2", str(event_toggler_mapping))
                    ea_code_fh.write("adict = " +
                                     event_toggler_mapping_str + "\n")
                    ea_code_fh.write(
                        "event_toggler_dict = {**event_toggler_dict, **adict}\n")


# . . . . . . . . . . . . . . . . . . end exclusive toggle . . . . . . . . . . . .
#                                                                                #
# - - - - - - - - - - - - - - - - - - slides - - - - - - - - - - - - - - - - - - -


# . . . . . . . . . . . . . . . . . . end slides . . . . . . . . . . . . . . . . .
# < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < > #
# - - - - - - - - - - - - - - - - layout instance code gen - - - - - - - - - - - - - -
# TODO: currently two version are kept: one for tnld and another for tnli. Not sure both are required
def gen_event_actions_li(tnli, lid):  # TODO: add code for lnli
    # codegen setup
    fh = open("everything_bagel_dictionary.py", "w")
    fh.write(Template("import ${lid}_event_actions\n").substitute(lid=lid))
    fh.write("everything_bagel_dict = {}\n")
    if os.path.exists(lid + "_app_actions.py"):
        defined_funcs = get_funcs_in_module(lid + "_app_actions.py")
        apps_event_ast_root = ast.parse(open(lid + "_app_actions.py").read())
    else:
        defined_funcs = set()
        apps_event_ast_root = ast.parse("")

    def event_ast_adder(func_name,
                        apps_event_ast_root=apps_event_ast_root,
                        defined_funcs=defined_funcs):
        return add_func_to_ast(func_name, apps_event_ast_root, defined_funcs)
    # event_actions.py header
    ea_code_fh = open(lid + "_event_actions.py", "w")
    ea_code_fh.write(
        "from everything_bagel_common import ToggleExclusive, ToggleExclusiveOther\n")
    ea_code_fh.write("import importlib\n")
    ea_code_fh.write("all_togglers = [" + "]\n")
    ea_code_fh.write("event_toggler_dict = {}\n")

    # -------------------------- codegen body - --------------------------------------------
    appstate_attribs = []
    for bld, all_labels_keysuffix_pair in walk_tli(tnli):
        gen_event_action_lookup_bld(bld, all_labels_keysuffix_pair, lid, fh)
        # app_actions.py body
        [appstate_attribs.append(_) for _ in
            gen_app_actions_bld(bld, all_labels_keysuffix_pair, event_ast_adder)]

    # appstate = make_dataclass('appstate', [(fname, Any, field(default=None)) for fname in appstate_attribs
    # ])
    # -------------------------- codegen closeout -------------------------------------------

    gen_code_exclusive_toggle(
        lid, lambda tnli=tnli: walk_tli(tnli), ea_code_fh)

    fh.write("""def everything_bagel(window, event, values, appstate):\n
    \tif event in everything_bagel_dict:\n
    \t\teverything_bagel_dict[event].on_event(window, values, event, appstate)""")
    fh.close()
    with open(lid + "_app_actions.py", "w") as fh:
        fh.write(ast.unparse(apps_event_ast_root))

    # event_actions.py on_action command
    ea_code_fh.write(
        Template(action_body).substitute(lid=lid))
    ea_code_fh.close()
    return appstate_attribs
# . . . . . . . . . . . . . . . . . . end layout instance code gen . . . . . . . . . . . .
# < >  < >  < >  < >  < >  < >  < >  < >  < > < >  < >  < >  < >  < >  < >  < >  < >  < > #
# - - - - - - - - - - - - - - - - build appstate - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - -  code gen APIs - - - - - - - - - - - - - - - -

def gen_event_actions(tnld, labels):
    lid = "test_bld"
    # codegen setup
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
    def bld_walkder(tnld=tnld, lables=labels):
        for bld in walk_tld(tnld):
            yield (bld, labels)
    gen_code_exclusive_toggle(lid, bld_walker, ea_code_fh)

    fh.write("""def everything_bagel(window, event, values, appstate):\n
    \tif event in everything_bagel_dict:\n
    \t\teverything_bagel_dict[event].on_event(window, event, values, appstate)""")
    fh.close()
    with open(lid + "_app_actions.py", "w") as fh:
        fh.write(ast.unparse(apps_event_ast_root))

    # event_actions.py on_action command
    ea_code_fh.write(
        Template(action_body).substitute(lid=lid))
    ea_code_fh.close()
