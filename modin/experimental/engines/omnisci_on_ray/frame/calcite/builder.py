from .rel.table_scan import EnumerableTableScan
from .rel.project import LogicalProject
from .rel.filter import LogicalFilter

from .rex.input_ref import InputRef
from .rex.literal import Literal
from .rex.local_ref import LocalRef

class Builder:
    stack = []

    def build(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None

    def scan(self, tables):
        self.stack.append(EnumerableTableScan(tables))
        return self

    def filter(self, condition):
        inp = self.stack.pop()
        self.stack.append(LogicalFilter(inp, condition))
        return self

    def project(self, exprs, fields):
        inp = self.stack.pop()
        self.stack.append(LogicalProject(inp, exprs, fields))
        return self
