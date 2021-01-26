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


class BlockLI:
    def __init__(self, bld, all_blabels, stacked='H', framed=False, layout=None):
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
        self.all_blabels = all_blabels
        self.layout = layout

    @classmethod
    def bli_single(cls, layout_seq, labels, stacked='H', framed=False):
        '''
        generate a single instance from layout_seq
        '''
        bld = BlockLD(layout_seq, stacked, framed)
        return cls(bld, labels)

    @classmethod
    def bli_set(cls, layout_seq, all_bkeys, all_blabels, istacked='H', iframed=False, sstacked='H', sframed=False, ):
        '''
        generate multiple instance of the layout_set
        '''
        bld = BlockLD(layout_seq, istacked, iframed)
        return cls(bld, all_bkeys, all_blabels, sstacked, sframed)


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
