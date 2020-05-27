class RelNode:
    def name(self):
        pass

    def get_inputs(self):
        pass

    def explain(self, writer):
        print(writer)
        self.explain_terms(writer).done(self)

    def explain_terms(self, writer):
        return writer


class Filter(RelNode):
    def __init__(self, inp, condition):
        self.inp = inp
        self.condition = condition

    def get_inputs(self):
        return [self.inp]

    def explain_terms(self, writer):
        return super().explain_terms(writer).item("condition", self.condition)


class LogicalFilter(Filter):
    def __init__(self, *args):
        super().__init__(*args)

    def name(self):
        return "LogicalFilter"


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


class TableScan(RelNode):
    table = ""

    def __init__(self, table):
        self.table = table

    def name(self):
        return "TableScan"

    def get_inputs(self):
        return []

    def explain_terms(self, writer):
        return super().explain_terms(writer).item("table", self.table)


class EnumerableTableScan(TableScan):
    def __init__(self, table, field_names):
        super().__init__(table)
        self.field_names = field_names

    def name(self):
        return "EnumerableTableScan"

    def explain_terms(self, writer):
        return super().explain_terms(writer).item("fieldNames", self.field_names)
