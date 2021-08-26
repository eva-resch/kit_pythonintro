"""
Represents the main structure of the neural network including the different types of nodes:
    Input_node: for the value (1 or 0) represented by each of the 27x18 = 486 pixels; has only outgoing edges
    Hidden_node: which will be connected within the network; has both incoming and outgoing edges
    Output_node: there are three representing the possible actions "left", "right" and "jump"; has only incoming edges
and the connecting edges.
"""
    
from random import randint
from node import *


class Edge:
    """
    A directed edge with a weight between two nodes.

    Attributes
    ----------
    begin : Input_node or Hidden_node
    end : Hidden_node or Output_node
    weight: -1 or 1
    """
    # TODO: Catch exception when used
    def __init__(self, begin: Node, end: Node, weight: int):
        """
        Parameters
        ----------
        begin : Node
        end : Node
        weight: -1 or 1

        Raises
        ------
        AssertionError : if the begin is an Output_node or the end an Input_node
        AssertionError : if the end is in a lower or equal layer as the begin
        AssertionError: if the given weight is not 1 or -1
        """
        assert (begin is not Output_node) and (end is not Input_node)
        assert begin.layer < end.layer
        assert abs(weight) == 1

        self.begin = begin
        self.end = end
        self.weight = weight

        # We can already set new incoming edges of the nodes in this constructor
        begin.add_output_edge(self)
        end.add_input_edge(self)

        #Update the layer of this end node, including all the following nodes.
        end.update()





class Network:
    def __init__(self):
        """
        Initialize new network that has no hidden nodes (as described in the NEAT paper)

        ----------------------------------------------------------------------------------------------------------------
        Careful with indices of nodes: 0-485 are the input nodes, 486, 487, 488 are the three output nodes
        Then  we categorize all hidden nodes by their 'innovation number' -> index
        """
        self.nodes = []
        self.edges = []
        self.fitness = 0
        
        # Create input nodes
        for x in range(486):
            self.nodes.append(Input_node())

        # Create output nodes
        for x in range(3):
            #Set output node layer to 2
            node = Output_node()
            node.set_layer(2)
            self.nodes.append(node)


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
        # TODO: Netzwerk auswerten. Die Frage ist, wann das Netzwerk ausgewertet werden soll.

        # Initialize input nodes with values
        for x in range(len(values)):
            self.nodes[x].reset_out(values(x))

        

        return [self.nodes[486] > 0, self.nodes[487] > 0, self.nodes[488] > 0]

    # TODO: Edge mutation implementieren
    def edge_mutation(Network):

        # Step 1: choose a connection with some randomized function and try to create an edge
        # For now: Chose a random node
        # TODO: create actual probability distribution
        # TODO: avoid choosing output nodes (this is actually somewhat solved at the moment because of the assertion)
        while True:
            # Idea: at some point we will find a connection that is allowed so we just try as long as we have to
            try:
                node1 = randint(0, len(Network.nodes))
                node2 = randint(0, len(Network.nodes))
                weight = randint(0,1)
                if weight == 0:
                    weight = -1
                edge = Edge(Network.nodes(node1), Network.nodes(node2), weight)

            except AssertionError:
                continue

            break

        # Step 2: fill in the new edge into the network. Keep in mind that we have to update the Nodes / Layers.
        # TODO: update input_edges for end and output_edges for begin
        # TODO: update layer: collect all input_edges and calculate minimum layer, add +1
        # TODO: for every node that follows after the new edge: update layer as well (recursion?)
        Network.edges.append(edge)

        return Network

    # TODO: Node mutation implementieren
    def node_mutation(Network):
        return Network
