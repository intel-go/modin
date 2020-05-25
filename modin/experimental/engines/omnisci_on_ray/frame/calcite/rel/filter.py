from .rel_node import RelNode


class Filter(RelNode):
    def __init__(self, inp, condition):
        self.inp = inp
        self.condition = condition

    def get_inputs(self):
        return [self.inp]

    def explain_terms(self, writer):
        return super().explain_terms(writer).item("condition", condition)


class LogicalFilter(Filter):
    def __init__(self, *args):
        super().__init(*args)

    def name(self):
        return "LogicalFilter"
