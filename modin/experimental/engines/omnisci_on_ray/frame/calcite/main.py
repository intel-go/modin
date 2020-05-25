from modin.experimental.engines.omnisci_on_ray.frame.calcite.rel_writer import RelWriter

from modin.experimental.engines.omnisci_on_ray.frame.calcite.builder import Builder
from modin.experimental.engines.omnisci_on_ray.frame.calcite.rex.input_ref import InputRef

writer = RelWriter()

builder = Builder()

rel = builder.scan(["table"]).project([InputRef(0), InputRef(1)], ["f1", "f2"]).build()
rel.explain(writer)

print(writer.as_string())