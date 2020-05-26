class RexNode(dict):
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)


class LocalRef(RexNode):
    def __init__(self, inp, name, typ):
        super().__init__(input=inp, name=name, type=typ)


class Literal(RexNode):
    def __init__(self, typ, value):
        super().__init__(type=typ, value=value)


class InputRef(RexNode):
    def __init__(self, inp):
        super().__init__(input=inp)


class CorrelVariable(RexNode):
    def __init__(self, name, typ):
        super().__init__(name=name, type=typ)


class OpExpr(RexNode):
    def __init__(self, op, operands, res_type):
        super().__init__(op=op, operands=operands, type=res_type)
