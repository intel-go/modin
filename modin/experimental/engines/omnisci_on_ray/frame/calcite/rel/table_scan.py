from .rel_node import RelNode


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


class LogicalTableScan(TableScan):
    def __init__(self, table):
        super().__init__(table)

    def name(self):
        return "LogicalTableScan"


class EnumerableTableScan(TableScan):
    def __init__(self, table):
        super().__init__(table)

    def name(self):
        return "EnumerableTableScan"
