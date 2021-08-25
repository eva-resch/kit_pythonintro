"""
Represents the main structure of the neural network including the different types of nodes:
    Input_node: for the value (1 or 0) represented by each of the 27x18 = 486 pixels; has only outgoing edges
    Hidden_node: which will be connected within the network; has both incoming and outgoing edges
    Output_node: there are three representing the possible actions "left", "right" and "jump"; has only incoming edges
and the connecting edges.
"""

class Node:
    def __init__(self):
        self.layer = 0
        self.out = 0
        self.input_edges = []
        self.output_edges = []
    
    def get_out(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for inp in self.input_edges:
            sum += inp.weight * inp.begin.get_out()
        self.out = sgn(sum)
        return self.out

    def add_input_edge(self, edge):
        self.input_edges.append(edge)

    def add_output_edge(self, edge):
        self.output_edges.append(edge)

    def get_input_edges(self):
        return self.input_edges

    def get_output_edges(self):
        return self.output_edges

    

class Input_node:
    def __init__(self, value):
        'Value is 1 if the corresponding block is accessible, else 0'
        self.out = value
        self.output_edges = []

    def add_output_edge(self, edge):
        self.output_edges.append(edge)

    def get_out(self):
        return self.out

    def get_output_edges(self):
        return self.output_edges


class Hidden_node:
    def __init__(self, layer):
        # self.layer = layer
        self.out = 0
        self.input_edges = []
        self.output_edges = []

    def get_out(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for inp in self.input_edges:
            sum += inp.weight * inp.begin.get_out()
        self.out = sgn(sum)
        return self.out

    def add_input_edge(self, edge):
        self.input_edges.append(edge)

    def add_output_edge(self, edge):
        self.output_edges.append(edge)

    def get_input_edges(self):
        return self.input_edges

    def get_output_edges(self):
        return self.output_edges


class Output_node:
    def __init__(self):
        self.out = 0
        # self.layer = 100
        self.input_edges = []

    def get_out(self):
        """
        Calculating the value of the node by using the given formula:
            signum(sum over (weight of incoming edge)x(value of prior node))
        """
        sum = 0
        for inp in self.input_edges:
            sum += inp.weight * inp.begin.get_out()
        self.out = sgn(sum)
        return self.out

    def add_input_edge(self, edge):
        self.input_edges.append(edge)

    def get_input_edges(self):
        return self.input_edges


class Edge:
    """
    A directed edge with a weight between two nodes.

    Attributes
    ----------
    begin : Input_node or Hidden_node
    end : Hidden_node or Output_node
    weight: int
    """
    # TODO: Catch exception
    def __init__(self, begin, end, weight):
        """
        Parameters
        ----------
        begin : Input_node or Hidden_node
        end : Hidden_node or Output_node
        weight: int

        Raises
        ------
        AssertionError : if the begin is an Output_node or the end an Input_node
        AssertionError : if the end is in a lower or equal layer as the begin
        """
        # TODO: Assert that the begin is in a lower layer than the end.
        assert (begin is not Output_node) and (end is not Input_node)
        self.begin = begin
        self.end = end
        self.weight = weight


class Network:
    def __init__(self, values):
        # TODO: Implement initial edges. The question is how we implement those (e.g. at random, all connected to all, etc.)
        """
        Initialize new network that has no hidden nodes (as described in the NEAT paper)
        """
        self.fitness = 0
        
        # Create input nodes
        Nodes = []
        for value in values:
            Nodes.append(Input_node(value))

        # Create output nodes
        for x in range(3):
            Nodes.append(Output_node())


    def update_fitness(self, points, time):
        # Calculate and updates the networks fitness value based on the players points and the time gone by.
        self.fitness = points - 50 * time

    def evaluate(self, values):
        """
        Wertet das Netzwerk aus. 
        
        Parameters
        ----------
            values: eine Liste von 27x18 = 486 Werten, welche die aktuelle diskrete Spielsituation darstellen
                    die Werte haben folgende Bedeutung:
                     1 steht fuer begehbaren Block
                    -1 steht fuer einen Gegner
                     0 leerer Raum

        Returns
        -------
            Eine Liste [a, b, c] aus 3 Boolean, welche angeben:
                a, ob die Taste "nach Links" gedrueckt ist
                b, ob die Taste "nach Rechts" gedrueckt ist
                c, ob die Taste "springen" gedrueckt ist.
        """


        return [False, False, False]


def sgn(x):
    # Returns sign of a given argument x.
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1
