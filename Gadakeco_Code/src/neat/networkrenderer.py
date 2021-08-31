import pygame
from neat.node import *
import random

TILESIZE = 10


def render_network(surface, network, values):
    """
    Zeichnet die Minimap und den Netzwerkgraphen 
    
    Argumente:
        surface: ein pygame.Surface der Groesse 750 x 180 Pixel.
                 Darauf soll der Graph und die Minimap gezeichnet werden.
        network: das eigen implementierte Netzwerk (in network.py), dessen Graph gezeichnet werden soll.
        values: eine Liste von 27x18 = 486 Werten, welche die aktuelle diskrete Spielsituation darstellen
                die Werte haben folgende Bedeutung:
                 1 steht fuer begehbaren Block
                -1 steht fuer einen Gegner
                 0 leerer Raum
                Die Spielfigur befindet sich immer ca. bei der Position (10, 9) und (10, 10).
    """
    colors = {1: (255, 255, 255), -1: (255, 0, 0), 2: (255, 0, 0, 128), 3: (0, 255, 0), 4: (0, 0, 0), 5: (71, 60, 139)}
    # draw slightly gray background for the minimap
    pygame.draw.rect(surface, (128, 128, 128, 128), (0, 0, 27 * TILESIZE, 18 * TILESIZE))
    # draw minimap
    for y in range(18):
        for x in range(27):
            if values[y * 27 + x] != 0:
                color = colors[values[y * 27 + x]]
                surface.fill(color, (TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE))
                pygame.draw.rect(surface, (0, 0, 0), (TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE), 1)

    # Zeichnen Sie hier das Netzwerk auf das Surface.

    """
    --------------------------------------------------------------------------------------------------------------------
    """

    # import the information we want to draw
    nodes = network.get_nodes()
    edges = network.get_edges()

    input_nodes = nodes[:486]
    hidden_nodes = nodes[489:]
    output_nodes = nodes[486:489]

    # create a dict for the position of all nodes
    nodes_dict = {}

    # map position of input_nodes with xy coordinates
    for x in range(27):
        for y in range(18):
            nodes_dict[input_nodes[y * 27 + x]] = (TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE)

    # draw activated input_nodes
    for node in input_nodes:
        if node.get_output_edges():
            position = nodes_dict[node]
            pygame.draw.rect(surface, colors[5], position, 1)

    # draw output_nodes
    y_pos = 4 * TILESIZE
    x_pos = 70 * TILESIZE

    for node in output_nodes:
        nodes_dict[node] = (x_pos, y_pos, TILESIZE, TILESIZE)
        position = nodes_dict[node]
        surface.fill(colors[1], position)
        pygame.draw.rect(surface, (0, 0, 0), position, 1)
        y_pos += 5 * TILESIZE

    # draw hidden_nodes. For this we want to look at the layers of those nodes

    # first get a list of the nodes sorted by the layer

    sort_by_layer = {}
    for node in hidden_nodes:
        if node.get_layer() not in sort_by_layer:
            sort_by_layer[node.get_layer()] = [node]
        else:
            sort_by_layer[node.get_layer()].append(node)

    number_layers = len(sort_by_layer)
    width = 35*TILESIZE
    height = 18*TILESIZE
    dist = 30*TILESIZE

    # this surface is only for reference, to see where we can draw hidden nodes. To be removed after completion
    pygame.draw.rect(surface, colors[2], (dist, 0, width, height))

    for i in range(number_layers):
        numb = len(sort_by_layer[i+2])
        x_pos = dist + width * (i + 1)/(number_layers + 1)
        index_y = 0
        for node in sort_by_layer[i+2]:
            y_pos = height * (index_y + 1)/(numb + 1)
            nodes_dict[node] = (x_pos, y_pos, TILESIZE, TILESIZE)
            position = nodes_dict[node]
            surface.fill(colors[1], position)
            pygame.draw.rect(surface, colors[4], position, 1)
            index_y += 1

    # draw the connecting lines
    for edge in edges:
        begin = edge.begin
        end = edge.end
        weight = edge.weight
        begin_pos = nodes_dict[begin]
        end_pos = nodes_dict[end]

        # if weight is -1, draw red line, if weight is 1 draw green line
        if weight == -1:
            pygame.draw.line(surface, colors[-1], begin_pos[:2], end_pos[:2], width=1)
        else:
            pygame.draw.line(surface, colors[3], begin_pos[:2], end_pos[:2], width=1)
