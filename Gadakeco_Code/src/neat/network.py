"""
Represents the main structure of the neural network including the different types of nodes:
    Input_node: for the value (1 or 0) represented by each of the 27x18 = 486 pixels; has only outgoing edges
    Hidden_node: which will be connected within the network; has both incoming and outgoing edges
    Output_node: there are three representing the possible actions "left", "right" and "jump"; has only incoming edges
and the connecting edges.
"""

import math
import numpy as np
from random import randint
from src.neat.node import *


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
        assert (not isinstance(begin, OutputNode)) and (not isinstance(end, InputNode))
        assert (begin.layer < end.layer) or (end.layer == -1)
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
            self.nodes.append(InputNode())

        # Create output nodes for the 3 possible choices left, right and jump.
        for x in range(3):
            self.nodes.append(OutputNode())

    # Create getter methods for the attributes of network
    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def get_fitness(self):
        return self.fitness

    def update_fitness(self, points, time):
        # Calculate and updates the networks fitness value based on the players points and the time gone by.
        self.fitness = points - 50 * time

    def evaluate(self, values):
        """
        Evaluates the network given the input 'values' of the pixels by calculating the value of each node.
        
        Parameters
        ----------
            values: list[int]
                representing the 27x18 = 486 pixels and their current value (1: accessible, -1: enemy, 0: empty)

        Returns
        -------
            list[bool]
                representing for each of the three options "left", "right" and "jump" if they are pressed or not.
        """

        # Initialize input nodes with values
        for i in range(len(values)):
            self.nodes[i].set_out(values[i])

        # Order all hidden nodes by layer and calculate their value.
        ordered_nodes = sorted(self.nodes[489:], key=Node.get_layer)
        for node in ordered_nodes:
            node.activate()

        # Evaluate the three output nodes.
        for i in range(3):
            node = self.nodes[486+i]
            node.activate()

        # Booleans representing, if the button should be pressed or not.
        left = self.nodes[486].get_out() > 0
        right = self.nodes[487].get_out() > 0
        jump = self.nodes[488].get_out() > 0

        output_nodes = self.nodes[486:489]

        # TODO: nachdenken, ob das der beste Fix fuer das negative Fitness Problem ist
        fitness = self.get_fitness()
        if fitness < 0:
            left = False
            right = False
            jump = False

        return [left, right, jump]

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
        while True:
            # Idea: at some point we will find a connection that is allowed so we just try as long as we have to
            try:
                # Choose between an input and a hidden node, but not the three output nodes!
                decision_index = randint(0, len(self.nodes)-4)

                # If the 'decision_index' is in the range 0-485 an input node will be chosen, else a hidden node.
                if decision_index < 486:
                    # TODO: wollen wir wirklich auch die Position, an der die Figur gerade steht so stark bewerten?
                    mean_row = 12
                    sd_row = 4
                    mean_col = 13
                    sd_col = 15

                    # TODO: Fragestunde!! Ist die Auswahl der Spalten unabh. von der der Zeilen oder brauchen wir Kovarianzmatrix für multivariate Normalverteilung?
                    # Try to find values within the grid of pixels (27x18)
                    while True:
                        [row, col] = np.random.multivariate_normal([mean_row, mean_col], [[sd_row, 0], [0, sd_col]])
                        if (0 < row < 18) and (0 < col < 27):
                            break

                    # Match the found values to a specific row and column
                    row = math.floor(row)
                    col = math.floor(col)
                    index_1 = 27*row + col
                else:
                    # Choose a hidden node following a discrete equal distribution.
                    index_1 = randint(489, len(self.nodes)-1)

                index_2 = randint(486, len(self.nodes)-1)
                node_1 = self.nodes[index_1]
                node_2 = self.nodes[index_2]

                weight = randint(0, 1)
                if weight == 0:
                    weight = -1

                # When initialising a new edge, layers update automatically for all following nodes
                # Through sorting by layer an edge can be build whenever the nodes are in different layers.
                if isinstance(node_2, OutputNode):
                    edge = Edge(node_1, node_2, weight)
                elif node_1.get_layer() < node_2.get_layer():
                    edge = Edge(node_1, node_2, weight)
                # TODO: Fragestunde!! Ist das erlaubt?
                elif node_2.get_layer() < node_1.get_layer():
                    edge = Edge(node_2, node_1, weight)
                else:
                    # When the layers are the same
                    raise AssertionError

                # Check if the edge exists already.
                if edge in self.edges:
                    continue

                self.edges.add(edge)

            except AssertionError:
                continue
            break

        # need to return self!
        return self

    def node_mutation(self):
        """
        Function to mutate the network 'self' by splitting up an edge and inserting a new node.
        The edge is chosen at random and then the updating steps take place with creating the new node and edges, adding
        the new edges and removing the old ones.
        """
        edge_index = randint(0, len(self.edges)-1)
        edge = list(self.edges)[edge_index]
        begin_node = edge.begin
        end_node = edge.end
        edge_weight = edge.weight
        new_layer = begin_node.get_layer() + 1

        # Set layer of end node to push it forward if needed to make room for new node.
        if end_node.get_layer() != -1:
            end_node.set_layer(max(end_node.get_layer(), new_layer+1))

        # Create new node and connecting edges
        node = HiddenNode(layer=new_layer)
        new_edge_1 = Edge(begin_node, node, weight=1)
        new_edge_2 = Edge(node, end_node, edge_weight)

        # Update edges for network
        self.edges.remove(edge)
        self.edges.add(new_edge_1)
        self.edges.add(new_edge_2)

        # Update edges of 'begin_node', 'end_node' and new 'node'.
        begin_node.get_output_edges().remove(edge)
        end_node.get_input_edges().remove(edge)

        # Add new node to network
        self.nodes.append(node)

        # need to return self
        return self
