from .rex_node import RexNode


class InputRef(RexNode):
    def __init__(self, inp):
        super().__init__(input=inp)
