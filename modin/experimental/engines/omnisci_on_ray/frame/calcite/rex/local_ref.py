from .rex_node import RexNode


class LocalRef(RexNode):
    def __init__(self, inp, name, typ):
        super().__init__(input=inp, name=name, type=typ)
