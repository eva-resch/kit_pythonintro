import pygame
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
    colors = {1: (255, 255, 255), -1: (255, 0, 0), 2: (255, 0, 0, 128), 3: (0, 255, 0)}
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
            pygame.draw.rect(surface, colors[3], position, 1)

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
    hidden_nodes_sorted = sorted(hidden_nodes, key=node.get_layer)

    # this is only for testing!
    y_pos = 0
    x_pos = 30 * TILESIZE
    for node in hidden_nodes_sorted:
        nodes_dict[node] = (y_pos, x_pos, TILESIZE, TILESIZE)
        x_pos += 5 * TILESIZE

    # next, make a list of all available positions
    # for now, we want to work with 4 possible layers
    available_positions = []

    # this surface is only for reference, to see where we can draw hidden nodes. To be removed after completion
    pygame.draw.rect(surface, colors[2], (30 * TILESIZE, 0, 35 * TILESIZE, 18 * TILESIZE))

    # draw the connecting lines
    for edge in edges:
        begin = edge.begin
        end = edge.end
        weight = edge.weight
        begin_pos = nodes_dict[begin]
        end_pos = nodes_dict[end]

        # if weight is -1, draw red line, if weight is 1 draw green line
        if weight == -1:
            pygame.draw.line(surface, colors[-1], begin_pos[:2], end_pos[:2], width=2)
        else:
            pygame.draw.line(surface, colors[3], begin_pos[:2], end_pos[:2], width=2)