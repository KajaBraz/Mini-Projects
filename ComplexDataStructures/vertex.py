class Vertex:
    def __init__(self, val):
        self.value = val
        self.edges = {}

    def get_edges(self):
        return self.edges.keys()

    def add_edge(self, vertex):
        self.edges[vertex] = True
