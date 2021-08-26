class Node:
    """
    Represents a general node in the network modelled in src/neat/network.

    Attributes
    ----------
        layer: int
            indicates distance to input layer; gets updated with every new incoming edge.
        out: int
            gives the value of the node; is calculated in 'activate' by the values of the incoming edges.
        input_edges: set(Edge)
            all the incoming edges of this node.
        output_edges: set(Edge)
            all the outgoing edges of this node.

    Methods
    -------
        activate(self):
            Gives back the value of this node according to the incoming edges, their weight and the value of the nodes.
        update(self):
            Recalculates the nodes layer after a change of the incoming edges.
    """
    def __init__(self, layer=None):
        self.layer = layer
        # TODO: brauchen wir das wirklich oder klappt das besser nur in "evaluate"? Bzw. können wir das überhaupt sinnvoll speichern?
        self.out = None
        self.input_edges = set()
        self.output_edges = set()

    def activate(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for inp in self.input_edges:
            sum += inp.weight * inp.begin.get_out()
        self.out = sgn(sum)

    def update(self):
        """
        After a new incoming edge has been added, the layer might be different and needs to be updated.
        First we need the layers of all predecessors, in which we will find the minimum.
        If this minimum is smaller than the nodes layer minus 1, we adapt the layer to minimum+1 and continue
        recursively on the following nodes with the same function. If the minimum is only by 1 smaller, nothing changes.
        """
        layers = []
        for edge in self.input_edges:
            layers.append(edge.begin.get_layer())

        minimum = min(layers)

        if minimum + 1 < self.layer:
            self.layer = minimum + 1
            # TODO: attention with output nodes, are there any possible problems (e.g. None reference)?
            for edge in self.output_edges:
                edge.end.update()

    def get_out(self):
        return self.out

    def add_input_edge(self, edge):
        self.input_edges.add(edge)

    def add_output_edge(self, edge):
        self.output_edges.add(edge)

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

    def set_out(self, value):
        # For setting the initial values for input nodes
        self.out = value

class Hidden_node(Node):
    pass
    
class Output_node(Node):
    def __init__(self):
        super().__init__(layer=2)

def sgn(x):
    # Returns sign of a given argument x.
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
