import pygame
from neat.node import *

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

    # import the information we need to draw the network
    nodes = network.get_nodes()
    edges = network.get_edges()

    input_nodes = nodes[:486]
    hidden_nodes = nodes[489:]
    output_nodes = nodes[486:489]

    # create a dict for the position of all nodes. This is needed to draw the edges later.
    nodes_dict = {}

    # draw activated input_nodes. With index = 27*y+x the coordinates are given by the index via mod '%' and div '//'.
    index = 0
    for node in input_nodes:
        if node.get_output_edges():
            x = index % 27
            y = index // 27
            position = (TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE)
            nodes_dict[input_nodes[index]] = position
            pygame.draw.rect(surface, colors[5], position, 1)
        index += 1

    # draw output_nodes
    y_pos = 4 * TILESIZE
    x_pos = 70 * TILESIZE

    for node in output_nodes:
        position = (x_pos, y_pos, TILESIZE, TILESIZE)
        nodes_dict[node] = position
        surface.fill(colors[1], position)
        pygame.draw.rect(surface, (0, 0, 0), position, 1)
        y_pos += 5 * TILESIZE

    # draw hidden_nodes. We order the nodes by layer.

    # step 1: sort the nodes by layer
    sort_by_layer = {}
    for node in hidden_nodes:
        if node.get_layer() not in sort_by_layer:
            sort_by_layer[node.get_layer()] = [node]
        else:
            sort_by_layer[node.get_layer()].append(node)

    # step 2: define variables we need
    number_layers = len(sort_by_layer)
    width = 35*TILESIZE
    height = 18*TILESIZE
    dist = 30*TILESIZE

    # step 3: arrange the nodes based on their layer and the number of nodes per layer
    for i in range(number_layers):
        numb = len(sort_by_layer[i+2])
        x_pos = dist + width * (i + 1)/(number_layers + 1)
        index_y = 0
        for node in sort_by_layer[i+2]:
            y_pos = height * (index_y + 1)/(numb + 1)
            position = (x_pos, y_pos, TILESIZE, TILESIZE)
            nodes_dict[node] = position
            surface.fill(colors[1], position)
            pygame.draw.rect(surface, colors[4], position, 1)
            index_y += 1

    # draw the edges by going through all existing edges
    for edge in edges:
        begin = edge.get_begin()
        end = edge.get_end()
        weight = edge.get_weight()
        begin_pos = list(nodes_dict[begin][:2])
        end_pos = list(nodes_dict[end][:2])

        # add half a TILESIZE so that the edge starts in the middle of a tile
        begin_pos[0] += 0.5 * TILESIZE
        begin_pos[1] += 0.5 * TILESIZE
        end_pos[0] += 0.5 * TILESIZE
        end_pos[1] += 0.5 * TILESIZE

        # if weight is -1, draw red line, if weight is 1 draw green line
        if weight == -1:
            pygame.draw.line(surface, colors[-1], begin_pos, end_pos, width=1)
        else:
            pygame.draw.line(surface, colors[3], begin_pos, end_pos, width=1)
