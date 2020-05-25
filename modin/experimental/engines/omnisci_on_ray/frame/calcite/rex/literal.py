from .rex_node import RexNode


class Literal(RexNode):
    def __init__(self, typ, value):
        super().__init__(type=typ, value=value)
