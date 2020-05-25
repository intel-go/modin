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


class RelDataType:
    pass
