from .rel_node import RelNode, RelDataType


class Project(RelNode):
    exps = []
    fields = []
    inp = []

    def __init__(self, inp, exps, fields):
        self.exps = exps
        self.fields = fields
        self.inp = inp

    def get_inputs(self):
        return [self.inp]

    def explain_terms(self, writer):
        super().explain_terms(writer)
        writer.item("fields", self.fields)
        writer.item("exprs", self.exps)
        return writer


class LogicalProject(Project):
    def __init__(self, *args):
        super().__init__(*args)

    def name(self):
        return "LogicalProject"
