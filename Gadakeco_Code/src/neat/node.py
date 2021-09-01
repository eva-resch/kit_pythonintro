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
        result = 0
        for edge in self.input_edges:
            result += edge.get_weight() * edge.get_begin().get_out()
        self.out = sgn(result)

    def update(self, current_layer):
        """
        After a new incoming edge has been added, the layer might be different and needs to be updated.
        First we need the layers of all predecessors, in which we will find the maximum.
        Then we will set the layer to be larger than this maximum, in order to not have any conflicts with the edges.
        Now all the outgoing nodes need to be updated as well.
        If the layer is already large enough or it indicates an end node, we are finished.
        """
        if self.layer == -1:
            # If arrived at output node, end recursive call.
            pass

        self.layer = current_layer + 1
        for next_edge in self.output_edges:
            next_edge.get_end().update(self.layer)

    # Getter methods
    def get_layer(self):
        return self.layer

    def get_out(self):
        return self.out

    def get_input_edges(self):
        return self.input_edges

    def get_output_edges(self):
        return self.output_edges

    # Setter method for 'layer'. 'out' will be calculated when needed.
    def set_layer(self, layer):
        self.layer = layer

    # The 'input_edges' and 'output_edges' will be modified through these methods, but cannot be set separately.
    def add_input_edge(self, edge):
        self.input_edges.add(edge)

    def remove_input_edge(self, edge):
        self.input_edges.remove(edge)

    def add_output_edge(self, edge):
        self.output_edges.add(edge)

    def remove_output_edge(self, edge):
        self.output_edges.remove(edge)


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
