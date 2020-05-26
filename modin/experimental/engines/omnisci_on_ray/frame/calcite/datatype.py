class DataTypeField(dict):
    def __init__(self):
        dict.__init__(self)

class DataType(dict):
    def __init__(self, name, nullable):
        dict.__init__(self, type=name, nullable=nullable)