from .rex_node import RexNode


class CorrelVariable(RexNode):
    def __init__(self, name, typ):
        super().__init__(name=name, type=typ)
