from .rel.rel_node import RelNode
from .rex.rex_node import RexNode


class RelWriter:
    values = {}
    rel_id_map = {}
    previous_id = -1
    rel_list = []

    def explain(self, rel, values):
        json_map = {}
        json_map["id"] = None
        json_map["relOp"] = rel.name()
        for k, v in values.items():
            if isinstance(v, RelNode):
                continue
            json_map[k] = v

        l = self.explain_inputs(rel.get_inputs())

        if len(l) != 1 or l[0] != self.previous_id:
            json_map["inputs"] = l

        id = len(self.rel_id_map)
        self.rel_id_map[rel] = id
        json_map["id"] = id
        self.rel_list.append(json_map)
        self.previous_id = id

    def explain_inputs(self, inputs):
        l = []
        for inp in inputs:
            id = self.rel_id_map.get(inp)
            if id == None:
                inp.explain(self)
                id = self.previous_id
            l.append(id)
        return l

    def done(self, rel):
        values_copy = self.values.copy()
        self.values.clear()
        self.explain(rel, values_copy)
        return self

    def as_string(self):
        import json
        json_map = {}
        json_map["rels"] = self.rel_list
        return json.dumps(json_map)

    def item(self, term, value):
        self.values[term] = value
        return self
