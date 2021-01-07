import PySimpleGUI as sg
import layout_directive_definitions as lddm

# - - - - - - - - - - - - - - - - layout decorator functions- - - - - - - - - - - - - - -


def get_key_from_label(label):
    return label.lower().replace(" ", "_")


def get_gstyle(gelem_cons, gid, pre, label, style={}, labeler=None):
    '''
    gstyle: style for a gelem
    key = gid + get_key_from_label(label)
    button_text, text, default_text = pre+label
    '''
    adict = None
    if gelem_cons == sg.Button:
        if labeler is not None:
            adict = {**{'button_text': labeler(pre, label)}, **style}
        else:
            adict = {**{'button_text': pre + label}, **style}

    if gelem_cons == sg.Text:
        adict = {**{'text': pre + label}, **style}

    if gelem_cons == sg.InputText:
        adict = {**{'default_text': pre + label}, **style}

    if adict == None:
        adict = style
    return {**adict, **{'key': gid + get_key_from_label(label)}}


# - - - - - - - - - - - - - - - - layout composition functions- - - - - - - - - - - - - - -
# TODO: make it return sg.Column
def layout_horizontal_generator(gelem_generators):
    '''
    input: a list of layout generators
    returns a list of list. The inner list contains a column or frame element
    '''
    def f(l): return [[ge_cons(l) for ge_cons in gelem_generators
                       ]]
    return f


def layout_vertical_generator(gelem_generators):
    '''
    input: a list of layout generators
    returns a list of column or frame element
    '''
    def f(l): return [[ge_cons(l)] for ge_cons in gelem_generators]
    return f


def stitch_layouts(all_layouts=[], cstacked='H', cframed=False):
    '''
    input: all_layouts is a list of Column or Frame element

    returns: a Column or Frame element
    '''
    if cstacked == 'V':
        layout_elem = [[le] for le in all_layouts
                       ]
    if cstacked == 'H':
        layout_elem = [[layout for layout in all_layouts]]
    if cframed:
        clayout_elem = sg.Frame("", layout_elem)
    else:
        clayout_elem = sg.Column(layout_elem)

    return clayout_elem


def build_layout_set(layout_generator, labels, stacked='H', framed=False):
    '''
    tnld: treenode layout directive/definition/template
    assumes all child bld  have an attached generator

    returns
      - a Column or Frame element
    '''
    if stacked == 'V':
        layout_elem = [[layout_generator(label)] for label in labels]

    if stacked == 'H':
        layout_elem = [[
            layout_generator(label) for label in labels
        ]]
    if framed:
        flayout_elem = sg.Frame("", layout_elem)
    else:
        flayout_elem = sg.Column(layout_elem)

    return flayout_elem


# - - - - - - - - - - - - - - - - layout generator functions - - - - - - - - - - - - - - - -


def get_layout_generator_bld(bld):
    '''
    bld: block layout definition/directive/template
    key of a gelem of bld = gid + get_key_from_label
    returns: a Frame or Column element
    '''
    gids = [
        cls.gid for cls in bld.layout_seq]
    gcons = [  # get all the element constructors in that order
        cls.gcons for cls in bld.layout_seq]
    banner_prefixes = [
        cls.banner_prefix for cls in bld.layout_seq]
    styles = [
        cls.sty for cls in bld.layout_seq]

    labelers = []
    for cls in bld.layout_seq:
        if hasattr(cls, 'labeler'):
            labelers.append(cls.labeler)
        else:
            labelers.append(None)

    gelem_generators = [
        lambda l, gid=gid, gcons=gcons, sty=sty, pre=pre, labeler=labeler: gcons(**get_gstyle(gcons, gid,  pre, l, sty, labeler)) for gid, gcons, pre, sty, labeler in zip(gids, gcons, banner_prefixes, styles, labelers)
    ]

    # choose a h or v generator for gelems
    def layout_instance_generator(l):
        return sg.Column(
            [layout_horizontal_generator, layout_vertical_generator][
                bld.stacked == 'V'](gelem_generators)(l)
        )

    if bld.framed:
        def final_layout_instance_generator(l): return sg.Frame("",
                                                                [[layout_instance_generator(l)]])
    else:
        final_layout_instance_generator = layout_instance_generator
    return final_layout_instance_generator


def get_layout_generator(ld):
    '''
    returns a layout generator that takes input as label and returns a
    Frame or Column element
    '''
    if isinstance(ld, lddm.TreeNodeLD):
        return get_layout_generator_tnld(ld)
    elif isinstance(ld, lddm.BlockLD):
        return getattr(ld, "instance_generator")


def get_layout_generator_tnld(tnld):
    '''
    returns a layout generator that takes input as label and returns a
    Frame or Column element
    '''
    left_layout_gen = get_layout_generator(tnld.left_ld)
    if tnld.right_ld is None:
        if tnlt.framed == True:
            def final_layout_gen(l): return sg.Frame("", left_layout_gen(l))
            return final_layout_gen
        else:
            return left_layout_gen
    right_layout_gen = get_layout_generator(tnld.right_ld)
    def final_layout_gen(l): return stitch_layouts(
        [left_layout_gen(l), right_layout_gen(l)], tnld.stacked, tnld.framed)
    return final_layout_gen


def set_bld_layout_generator(ld):
    '''
    ld: a block or tree directive
    sets generator for each bld within a TreeNodeLD
    '''
    if ld is None:
        return
    if isinstance(ld, lddm.TreeNodeLD):
        set_bld_layout_generator(ld.left_ld)
        set_bld_layout_generator(ld.right_ld)
    elif isinstance(ld, lddm.BlockLD):
        setattr(ld, "instance_generator",
                get_layout_generator_bld(ld))


# . . . . . . . . . . . . . . . . . . end layout template functions . . . . . . . . . . . .


def get_layout_block(bld, labels=[""], stacked='H', framed=False):
    '''
    returns a list consisting either list (of Column or Frame) or of
    column or frame element
    '''
    layout_generator = get_layout_generator_bld(bld)
    return build_layout_set(layout_generator, labels, stacked, framed)


def build_layout_treenode_set(tnld, labels=[""], stacked='H', framed=False):
    '''

    '''
    set_bld_layout_generator(tnld)
    layout_generator = get_layout_generator_tnld(tnld)
    return build_layout_set(layout_generator, labels, stacked, framed)
