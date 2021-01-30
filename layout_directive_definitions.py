def get_key_from_label(label):
    return label.lower().replace(" ", "_")


def get_label_key(label, key_prefix, key_suffix):
    if label is None:
        label = key_prefix
        key_prefix = get_key_from_label(label)
        if key_suffix is None:
            key_suffix = ""
    key = key_prefix + key_suffix
    return (label, key)


class Gelem:
    def __init__(self, cons, sty, ex_toggle_attrs=None, appstate_attrib=None):
        '''
        gid: an internal identifer for this elem
        banner_prefix: ???
        cons: the pysg constructor (e.g., sg.Button, etc.)
        sty: dictionary specifying other stylings
        ex_toggle_attrs : TBD
        appstate_attrib: attribute in appstate associated with this gelem
        '''
        #self.gid = gid
        #self.banner_prefix = banner_prefix
        self.gcons = cons
        self.sty = sty
        self.ex_toggle_attrs = ex_toggle_attrs
        self.appstate_attrib = appstate_attrib


class BlockLD:
    def __init__(self, layout_seq,  stacked='H', framed=False):
        '''
        layout_seq : a list of (key-prefix, gelem)
        stacked : directive for stacking, horizontally ('H') or vertically ('V')  the gelem in the layout_seq
        framed: frame each instance of BlockLD
        '''
        self.layout_seq = layout_seq
        self.stacked = stacked
        self.framed = framed


class TreeNodeLD:
    def __init__(self, left_ld, right_ld, stacked='H', framed=False):
        '''
        left_ld: is BlockSetLD/TreeNodeLD
        right-ld: is None/BlockSetLD/TreeNodeLD
        stacked: directive for stacking left  and right layouts
        framed : make a frame around left and right layout
        '''
        self.left_ld = left_ld
        self.right_ld = right_ld
        self.stacked = stacked
        self.framed = framed


def NoneSeq():
    while True:
        yield None


def make_tuple_iter(val, tuple_sz):
    tres = tuple([val for _ in range(tuple_sz)])
    while True:
        yield tres


TI = make_tuple_iter


def conc_iter(iter1, iter2):
    for a, b in zip(iter1, iter2):
        yield tuple([_+b for _ in a])


CI = conc_iter


def jx_tup_iter(iter1, iter2):
    for t1, t2 in zip(iter1, iter2):
        yield (*t1, *t2)


JI = jx_tup_iter


def sseq_iter():
    x = 0
    while True:
        yield str(x)
        x = x + 1


SI = sseq_iter


def senumerate(iter):
    for idx, val in enumerate(iter):
        yield (str(idx), val)


EI = senumerate


class BlockLI:
    def __init__(self, bld, all_labels_keysuffix_pair, stacked='H', framed=False, layout=None):
        '''
        bld: a block/treeNode ld
        labelers: TBD
        stacked: directive to control stacking of bld instances
        framed: make a frame around all the generated layout
        layout: the final layout
        '''
        self.bld = bld
        self.stacked = stacked
        self.framed = framed
        self.all_labels_keysuffix_pair = all_labels_keysuffix_pair
        self.layout = layout

    @classmethod
    def bli_single(cls, layout_seq, labels=None, stacked='H', framed=False):
        '''
        generate a single instance from layout_seq.
        If labels is None then key-prefix is used as label and key suffix is empty.

        '''
        bld = BlockLD(layout_seq, stacked, framed)
        if labels is None:
            labels = [((None for _ in layout_seq), (None for _ in layout_seq))]
        return cls(bld, labels)

    @classmethod
    def bli(cls, gelem_group, prefix_group, labelgi, suffixgi, istacked=True, iframed=False, sstacked='H', sframed=False):
        bld = BlockLD([(prefix, gelem) for prefix, gelem in zip(
            prefix_group, gelem_group)], istacked, iframed)
        return cls(bld, [(lt, st) for lt, st in zip(labelgi, suffixgi)], sstacked, sframed)

    @classmethod
    def bli_set(cls, layout_seq, all_labels_keysuffix_pair, istacked='H', iframed=False, sstacked='H', sframed=False, fill_val=None):
        '''
        generate multiple instance of the layout_set
        all_labels_keysuffix_pair: is a list of (label-tuple, key-tuple),
        where label-tuple defines the label of each element of the layout-sequence
        and key-tuple defines key-suffixes for each element of layout sequence

        prefix_tuple
        layout_tuple
        label_tuple
        suffix_tuple
        '''
        bld = BlockLD(layout_seq, istacked, iframed)
        return cls(bld,  all_labels_keysuffix_pair, sstacked, sframed)

    @classmethod
    def bli_set2(cls, layout_seq, all_labels, all_suffixes, istacked='H', iframed=False, sstacked='H', sframed=False, ):
        '''
        generate multiple instance of the layout_set
        all_labels_keysuffix_pair: is a list of (label-tuple, key-tuple),
        where label-tuple defines the label of each element of the layout-sequence
        and key-tuple defines key-suffixes for each element of layout sequence

        fill
        '''
        pass


class ListNodeLI:
    def __init__(self, all_li,  stacked='H', framed=False):
        '''
        all_li: a list of layout instances (tree/list/block)
        framed: make a frame around generated layout
        '''
        self.all_li = all_li
        self.stacked = stacked
        self.framed = framed


class TreeNodeLI:
    def __init__(self, left_li, right_li, stacked='H', framed=False):
        '''
        left_li: is TreeNodeLI/ListNodeLI/BlockLI
        right-lt: is TreeNodeLI/ListNodeLI/BlockLI
        '''
        self.left_li = left_li
        self.right_li = right_li
        self.stacked = stacked
        self.framed = framed
