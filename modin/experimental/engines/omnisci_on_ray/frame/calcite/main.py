from modin.experimental.engines.omnisci_on_ray.frame.calcite.rel import *
from modin.experimental.engines.omnisci_on_ray.frame.calcite.rex import *
from modin.experimental.engines.omnisci_on_ray.frame.calcite.builder import Builder
from modin.experimental.engines.omnisci_on_ray.frame.calcite.rel_writer import RelWriter


writer = RelWriter()

builder = Builder()

rel = builder.scan(["table"]).project([InputRef(0), InputRef(1)], ["f1", "f2"]).build()
rel.explain(writer)

print(writer.as_string())