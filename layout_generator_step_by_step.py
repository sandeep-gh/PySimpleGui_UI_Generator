import PySimpleGUI as sg
import layout_directive_definitions as lddm

# - - - - - - - - - - - - - - - - gelem functions- - - - - - - - - - - - - - -


def get_key_from_label(label):
    return label.lower().replace(" ", "_")


def get_gstyle(gelem_cons, key_prefix, style, label):
    '''
    '''
    adict = None
    if gelem_cons == sg.Button:
        adict = {**{'button_text': label}, **style}

    if gelem_cons == sg.Text:
        adict = {**{'text': label}, **style}

    if gelem_cons == sg.InputText:
        adict = {**{'text': label}, **style}

    if gelem_cons == sg.Checkbox:
        adict = {**{'text': label}, **style}

    if adict == None:
        adict = style
    return {**adict, **{'key': key_prefix + get_key_from_label(label)}}


# - - - - - - - - - - - - - - - - layout generators/compositors - - - - - - - - - - - - - - -
def layout_horizontal_generator(gelem_iter_func):
    '''
    given a list of gelem_generator, creates a layout generator that stacks the
    gelem_generators horizontally
    '''
    def f(labels): return [[gelem for gelem in gelem_iter_func(labels)
                            ]]
    return f


def layout_vertical_generator(gelem_iter_func):
    '''
    given a list of gelem_generator, creates a layout generator that stacks the
    gelem_generators vertically
    '''
    def f(labels): return [[gelem]
                           for gelem in gelem_iter_func(labels)]
    return f


def stitch_layouts(all_layouts=[], cstacked='H', cframed=False):
    '''
    input: all_layouts is a list of Column or Frame element
    returns: a Column or Frame element that stacks the layouts vertically or horizontally
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


def build_li_set(layout_generator, all_blabels, stacked='H', framed=False):
    '''
    build a layout instance from a generator and set of labelers
    '''
    if stacked == 'V':
        layout_elem = [[layout_generator(glabels)]
                       for glabels in all_blabels]

    if stacked == 'H':
        layout_elem = [[
            layout_generator(glabels) for glabels in all_blabels
        ]]
    if framed:
        flayout_elem = sg.Frame("", layout_elem)
    else:
        flayout_elem = sg.Column(layout_elem)

    return flayout_elem

# - - - - - - - - - - - - - - - - end layout generators/compositors - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - layout directives: block/tree/list - - - - - - - - - - - -


def get_layout_generator_bld(bld):
    '''
    create layout generator from bld
    returns a generator that takes keys and labels (for each gelem)
    '''
    key_prefixes = [_[0] for _ in bld.layout_seq]
    gelems = [_[1] for _ in bld.layout_seq]

    gcons = [  # get all the element constructors in that order
        _.gcons for _ in gelems]
    styles = [
        _.sty for _ in gelems]

    def gelem_iter(labels, key_prefixes=key_prefixes, gcons=gcons, styles=styles):
        for gcon, key_prefix, sty, label in zip(gcons, key_prefixes, styles, labels):
            yield gcon(**get_gstyle(gcon, key_prefix,  sty, label))

    # choose a h or v generator for gelems
    def layout_instance_generator(gelem_labels):
        return sg.Column(
            [layout_horizontal_generator, layout_vertical_generator][
                bld.stacked == 'V'](gelem_iter)(gelem_labels)
        )

    if bld.framed:
        def final_layout_instance_generator(gelem_labels): return sg.Frame("",
                                                                           [[layout_instance_generator(gelem_labels)]])
    else:
        final_layout_instance_generator = layout_instance_generator
    return final_layout_instance_generator


def get_layout_generator_tnld(tnld):
    '''
    returns a layout generator that takes input as label and returns a
    Frame or Column element
    '''
    left_layout_gen = get_layout_generator(tnld.left_ld)
    if tnld.right_ld is None:
        if tnld.framed == True:
            def final_layout_gen(keys, labels): return sg.Frame(
                "", left_layout_gen(keys, labels))
            return final_layout_gen
        else:
            return left_layout_gen
    right_layout_gen = get_layout_generator(tnld.right_ld)
    def final_layout_gen(keys, labels): return stitch_layouts(
        [left_layout_gen(keys, labels), right_layout_gen(keys, labels)], tnld.stacked, tnld.framed)
    return final_layout_gen


def get_layout_generator(ld):
    '''
    returns a layout generator that takes input as label and returns a
    Frame or Column element
    '''
    if isinstance(ld, lddm.TreeNodeLD):
        return get_layout_generator_tnld(ld)
    elif isinstance(ld, lddm.BlockLD):
        return getattr(ld, "instance_generator")


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

# - - - - - - - - - - - - - - - - end layout directives: block/tree - - - - - - - - - - - -
# < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < >  < > #
# - - - - - - - - - - - - - - - - layout instances: block/list/tree  - - - - - - - - - - - -


def walk_tnli(tnli):
    if isinstance(tnli.left_li, lddm.BlockLI):
        yield tnli.left_li
    elif isinstance(tnli.left_li, lddm.TreeNodeLI):
        yield from walk_tnli(tnli.left_li)
    elif isinstance(tnli.left_li, lddm.ListNodeLI):
        yield from walk_li(tnli.left_li)

    if isinstance(tnli.right_li, lddm.BlockLI):
        yield tnli.right_li
    elif isinstance(tnli.right_li, lddm.TreeNodeLI):
        yield from walk_tnli(tnli.right_li)
    elif isinstance(tnli.right_li, lddm.ListNodeLI):
        yield from walk_li(tnli)


def walk_li(li):
    if isinstance(li, lddm.ListNodeLI):
        for _ in li.all_li:
            yield from walk_li(_)
    elif isinstance(li, lddm.TreeNodeLI):
        yield from walk_tnli(li)
    elif isinstance(li, lddm.BlockLI):
        yield li


def set_li_layout(sli):
    '''
    sli: a sequence of li's
    set li.layout for each li in sli
    '''
    for bli in walk_li(sli):
        bli.layout = get_layout_block(
            bli.bld,  bli.all_blabels, bli.stacked, bli.framed)


def compose_layout_lnli(lnli):
    return stitch_layouts([compose_layout_li(_) for _ in lnli.all_li], lnli.stacked, lnli.framed)


def compose_layout_tnli(tnli):
    left_layout = compose_layout_li(tnli.left_li)
    assert left_layout is not None
    if tnli.right_li is None:
        final_layout = left_layout
        if tnli.framed:
            # TODO: is final_layout never a list??
            final_layout = sg.Frame("", [[final_layout]])
        return final_layout

    right_li = tnli.right_li
    right_layout = compose_layout_li(right_li)
    assert right_layout is not None
    final_layout = stitch_layouts(
        [left_layout, right_layout], tnli.stacked, tnli.framed)

    return final_layout


def compose_layout_li(lin):
    if isinstance(lin, lddm.TreeNodeLI):
        return compose_layout_tnli(lin)
    if isinstance(lin, lddm.ListNodeLI):
        return compose_layout_lnli(lin)
    elif isinstance(lin, lddm.BlockLI):
        print("d", lin.layout)
        return lin.layout

# . . . . . . . . . . . . . . . . . . end compose layouts . . . . . . . . . . . .


def get_layout_block(bld, all_blabels, stacked='H', framed=False):
    '''
    returns a list consisting either list (of Column or Frame) or of
    column or frame element
    '''
    layout_generator = get_layout_generator_bld(bld)
    return build_li_set(layout_generator, all_blabels, stacked, framed)


def build_layout_treenode_set(tnld, labelers, stacked='H', framed=False):
    '''

    '''
    set_bld_layout_generator(tnld)
    layout_generator = get_layout_generator_tnld(tnld)
    return build_li_set(layout_generator, labelers, stacked, framed)
