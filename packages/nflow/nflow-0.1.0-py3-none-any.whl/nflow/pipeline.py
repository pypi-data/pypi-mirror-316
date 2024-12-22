class Pipeline:
    def __init__(self, name):
        self.name = name
        self.operators = []
        self.links = []
        self.id = f"pipeline-{name}"

    def link(self, src_operator, src_pad, dst_operator, dst_pad):
        self.links.append((src_operator, src_pad, dst_operator, dst_pad))
        print(f"Linked {src_operator.operator_type} ({src_pad}) -> {dst_operator.operator_type} ({dst_pad})")

    def register(self):
        print(f"Registering pipeline '{self.name}'...")
        return self.id
