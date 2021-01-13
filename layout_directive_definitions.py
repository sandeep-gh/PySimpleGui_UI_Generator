class Gelem:
    def __init__(self, gid, banner_prefix,  cons, sty, ex_toggle_attrs=None):
        self.gid = gid
        self.banner_prefix = banner_prefix
        self.gcons = cons
        self.sty = sty
        self.ex_toggle_attrs = ex_toggle_attrs


class BlockLD:
    def __init__(self, layout_seq,  stacked='H', framed=False):
        '''
        label: an identifier for the block
        '''
        self.layout_seq = layout_seq
        self.stacked = stacked
        self.framed = framed


# class BlockSetLD:
#     def __init__(self, bld,  stacked='H', framed=False):
#         self.bld = bld
#         self.stacked = stacked
#         self.framed = framed

class TreeNodeLD:
    def __init__(self, left_ld, right_ld, stacked='H', framed=False):
        '''
        left_lt: is BlockSetLD/TreeNodeLD
        right-lt: is None/BlockSetLD/TreeNodeLD
        '''
        self.left_ld = left_ld
        self.right_ld = right_ld
        self.stacked = stacked
        self.framed = framed


class BlockLI:
    def __init__(self, bld, labels, stacked='H', framed=False, layout=None):
        '''
        label: an identifier for the block
        '''
        self.bld = bld
        self.labels = labels
        self.stacked = stacked
        self.framed = framed
        self.layout = layout


class TreeNodeLI:
    def __init__(self, left_li, right_li, stacked='H', framed=False):
        '''
        left_lt: is TreeNodeLI
        right-lt: is TreeNodeLI or BlockNodeLI
        '''
        self.left_li = left_li
        self.right_li = right_li
        self.stacked = stacked
        self.framed = framed

# class TreeLayoutDirective:
#     def __init__(self, tlt, labels=[""], stacked='H', framed=False):
#         self.tlt = tlt
#         self.labels = labels
#         self.stacked = stacked
#         self.framed = framed
