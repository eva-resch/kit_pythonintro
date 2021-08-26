
class Node:
    def __init__(self, layer=None):
        self.layer = layer
        self.out = None
        self.input_edges = []
        self.output_edges = []

    def reset_out(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for inp in self.input_edges:
            sum += inp.weight * inp.begin.get_out()
        self.out = sgn(sum)

    def update(self):
        #TODO: Document
        layers = []
        for edge in self.input_edges:
            layers.append(edge.begin.get_layer())

        minimum = min(layers)

        if minimum + 1 < self.layer:
            self.layer = minimum
            # TODO: attention with output nodes, are there any possible problems (e.g. None reference)?
            for edge in self.output_edges:
                edge.end.update()

    def get_out(self):
        return self.out

    def add_input_edge(self, edge):
        self.input_edges.append(edge)

    def add_output_edge(self, edge):
        self.output_edges.append(edge)

    def get_input_edges(self):
        return self.input_edges

    def get_output_edges(self):
        return self.output_edges

    def get_layer(self):
        return self.layer
    
    def set_layer(self, layer):
        self.layer = layer

class Input_node(Node):
    def __init__(self):
        super().__init__(layer=1)

class Hidden_node(Node):
    pass
    
class Output_node(Node):
    pass

def sgn(x):
    # Returns sign of a given argument x.
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
