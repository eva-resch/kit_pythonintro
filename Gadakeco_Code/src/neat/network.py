"""
Represents the main structure of the neural network including the different types of nodes:
    Input_node: for the value (1 or 0) represented by each of the 27x18 = 486 pixels; has only outgoing edges
    Hidden_node: which will be connected within the network; has both incoming and outgoing edges
    Output_node: there are three representing the possible actions "left", "right" and "jump"; has only incoming edges
and the connecting edges.
"""

import numpy as np
from random import randint
from node import *


class Edge:
    """
    A directed edge with a weight between two nodes.

    Attributes
    ----------
    begin : Node
    end : Node
    weight: -1 or 1
    """

    # TODO: Catch exception when used
    def __init__(self, begin: Node, end: Node, weight: int):
        """
        Raises an AssertionError for invalid input, else sets the attributes.
        When a new edge is added, the layers might change, therefore they need to be updated. This will affect the 'end'
        node and all their successors, as specified in the class 'Node'.

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

        # Add information about new edge to both the 'begin' and 'end' node
        begin.add_output_edge(self)
        end.add_input_edge(self)

        # Update the layer of the 'end' node, including all the following nodes.
        end.update()


class Network:
    def __init__(self):
        """
        Initialize new network that has no hidden nodes (as described in the NEAT paper).

        ----------------------------------------------------------------------------------------------------------------
        Careful with indices of nodes: 0-485 are the input nodes, 486, 487, 488 are the three output nodes
        Then  we categorize all hidden nodes by their 'innovation number' -> index
        """

        #TODO: Kanten müssen als Menge und nicht Liste implementiert werden, damit finden und löschen anhand der ID möglich ist
        # -> gemacht! Gerne Augen aufhalten wegen mögl. Fehlern.
        self.nodes = []
        self.edges = set()
        self.fitness = 0

        # Create input nodes for the 27x18=486 pixels.
        for x in range(486):
            self.nodes.append(Input_node())

        # Create output nodes for the 3 possible choices left, right and jump.
        for x in range(3):
            self.nodes.append(Output_node())

    def update_fitness(self, points, time):
        # Calculate and updates the networks fitness value based on the players points and the time gone by.
        self.fitness = points - 50 * time

    def evaluate(self, values):
        """
        Evaluates the network given the input 'values' of the pixels by calculating the value of each node.
        
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
            self.nodes[x].set_out(values(x))

        left = self.nodes[486].get_out() > 0
        right = self.nodes[487].get_out() > 0
        jump = self.nodes[488].get_out() > 0

        return [left, right, jump]

    def get_fitness(self):
        return self.fitness

    def edge_mutation(self):
        # Step 1: choose a connection with some randomized function and try to create an edge
        # For now: Chose a random node
        # TODO: create actual probability distribution
        # TODO: avoid choosing output nodes (this is actually somewhat solved at the moment because of the assertion)
        while True:
            # Idea: at some point we will find a connection that is allowed so we just try as long as we have to
            try:
                node1 = randint(0, len(self.nodes))
                node2 = randint(0, len(self.nodes))
                weight = randint(0, 1)
                if weight == 0:
                    weight = -1
                # When initialising a new edge, layers update automatically for all following nodes
                edge = Edge(self.nodes[node1], self.nodes[node2], weight)
                # Check if the edge exists already.
                if edge in self.edges:
                    continue

            except AssertionError:
                continue

            break

        # Step 2: fill in the new edge into the network.
        self.edges.add(edge)

    # TODO: Node mutation implementieren
    def node_mutation(self):
        # Choose random edge -> needs list for indexing, not set!
        edge_index = randint(0, len(self.edges))
        edge = list(self.edges)[edge_index]
        begin_node = edge.begin
        end_node = edge.end
        edge_weight = edge.weight

        # Create new node and connecting edges
        node = Hidden_node(layer=begin_node+1)
        new_edge_1 = Edge(begin_node, node, weight=1)
        new_edge_2 = Edge(node, end_node, edge_weight)

        # Update edges for network
        self.edges.remove(edge)
        self.edges.add(new_edge_1)
        self.edges.add(new_edge_2)

        # Update edges of 'begin_node', 'end_node' and new 'node'.
        begin_node.get_output_edges.remove(edge)
        begin_node.add_output_edge(new_edge_1)

        node.add_input_edge(new_edge_1)
        node.add_output_edge(new_edge_2)

        end_node.get_input_edge.remove(edge)
        end_node.add_input_edge(new_edge_2)

        # Update layers for 'end_node' and all their successors
        end_node.update()
