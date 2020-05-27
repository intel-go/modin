from .rel import *
from .rex import *
from .datatype import DataType
class Builder:
    stack = []

    def build(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None

    def scan(self, tables, fields):
        self.stack.append(EnumerableTableScan(tables, fields))
        return self

    def filter(self, condition):
        inp = self.stack.pop()
        self.stack.append(LogicalFilter(inp, condition))
        return self

    def project(self, exprs, fields):
        inp = self.stack.pop()
        self.stack.append(LogicalProject(inp, exprs, fields))
        return self

    def OR(self, exprs):
        res_type = DataType("BOOLEAN", False)
        return OpExpr("OR", exprs, res_type)

    def EQ(self, lhs, rhs):
        res_type = DataType("BOOLEAN", False)
        return OpExpr("=", [lhs, rhs], res_type)

    def lit(self, value):
        return Literal("INTEGER", value)