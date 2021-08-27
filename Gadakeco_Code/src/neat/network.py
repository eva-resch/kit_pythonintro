"""
Represents the main structure of the neural network including the different types of nodes:
    Input_node: for the value (1 or 0) represented by each of the 27x18 = 486 pixels; has only outgoing edges
    Hidden_node: which will be connected within the network; has both incoming and outgoing edges
    Output_node: there are three representing the possible actions "left", "right" and "jump"; has only incoming edges
and the connecting edges.
"""

import numpy as np
import math
from random import randint, gauss
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
    """
    Simulates a neural network trained in the process NEAT with all nodes and edges.
    Used by src/neat/population as an individuum within the described population.py

    Methods
    -------
        update_fitness(self, points, time):
            Given the formula the fitness of the network 'self' will be updated
        evaluate(self, values): [bool, bool, bool]
            Given the 'values' representing the surroundings the next action will be determined: if the network should
            press "left", "right" or "jump".
        edge_mutation(self):
            Takes the network 'self', chooses two random nodes given a certain distribution and connects them with a new
            edge.
        node_mutation(self):
            Takes the network 'self', chooses a random edge and breaks it up into two with a new node inbetween.
    """
    def __init__(self):
        """
        Initialize new network that has no hidden nodes (as described in the NEAT paper).

        ----------------------------------------------------------------------------------------------------------------
        Careful with indices of nodes: 0-485 are the input nodes, 486, 487, 488 are the three output nodes
        Then  we categorize all hidden nodes by their 'innovation number' -> index
        """

        # Edges are implemented as a set to make removing easier, nodes as a list to make indexing easier.
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
        """
        Function to mutate the given network 'self' by adding a new edge.
        Therefore one node will be chosen to be the beginning: proportional to the number of both input and hidden nodes
        either a hidden node following a equal distribution or an input node following a normal distribution centered
        around the position of the playing figure will be used.
        The ending node will be chosen out of the hidden and output nodes following an equal distribution.
        The weight of the edge will be random either 1 or -1.
        The resulting edge must be both valid and non-existing in the network.
        Now we can add the edge to the network, this includes updating.
        """
        # TODO: create actual probability distribution
        # TODO: avoid choosing output nodes (this is actually somewhat solved at the moment because of the assertion)
        while True:
            # Idea: at some point we will find a connection that is allowed so we just try as long as we have to
            try:
                # Choose between an input and a hidden node, but not the three output nodes!
                decision_index = randint(0, len(self.nodes)-3)

                # If the 'decision_index' is in the range 0-485 an input node will be chosen, else a hidden node.
                if decision_index < 486:
                    row = gauss(8.5, math.sqrt(8.5))

                    col = gauss(9, 9)
                    if col <= 9:
                        col = max(0, math.ceil(col))
                    else:
                        col = min(26, math.floor(col))

                    input_node = self.nodes[row*27 + col]





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

        self.edges.add(edge)

    def node_mutation(self):
        """
        Function to mutate the network 'self' by splitting up an edge and inserting a new node.
        The edge is chosen at random and then the updating steps take place with creating the new node and edges, adding
        the new edges and removing the old ones.
        """
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
