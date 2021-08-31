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
        self.out = 0
        self.input_edges = set()
        self.output_edges = set()

    def activate(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for edge in self.input_edges:
            sum += edge.weight * edge.begin.get_out()
        self.out = sgn(sum)

    def update(self):
        """
        After a new incoming edge has been added, the layer might be different and needs to be updated.
        First we need the layers of all predecessors, in which we will find the maximum.
        Then we will set the layer to be larger than this maximum, in order to not have any conflicts with the edges.
        Now all the outgoing nodes need to be updated as well.
        If the layer is already large enough or it indicates an end node, we are finished.
        """
        layers = []
        for edge in self.input_edges:
            layers.append(edge.begin.get_layer())

        maximum = max(layers)

        if self.layer == -1:
            # If arrived at output node, end recursive call.
            pass
        elif self.layer <= maximum:
            self.layer = maximum + 1
            for next in self.output_edges:
                next.end.update()

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


class InputNode(Node):
    def __init__(self):
        super().__init__(layer=1)

    def set_out(self, value):
        # For setting the initial values for input nodes
        self.out = value


class HiddenNode(Node):
    pass


class OutputNode(Node):
    def __init__(self):
        super().__init__(layer=-1)


def sgn(x):
    # Returns sign of a given argument x.
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
