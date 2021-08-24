def sgn(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

class Input_node:
    def __init__(self, value):
        """
        Der Konstruktor weist dem Input-Node den Wert 1 zu, falls der Block begehbar ist. Ansonsten wird 0 zugewiesen.
        """
        self.out = value
        self.output_edges = []

    def get_out(self):
        """
        Gibt den Output-Wert zurueck.
        """
        return self.out

    def add_out_edge(self, edge):
        self.output_edges.append(edge)

    def get_output_edges(self):
        return self.output_edges


class Hidden_node:
    def __init__(self, layer):
        # self.layer = layer
        self.out = 0
        self.input_edges = []
        self.output_edges = []

    def get_out(self):
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
    def __init__(self, begin, end, weight):
        #TO-DO: Assertion für Input-/Output-Knoten?
        self.begin = begin
        self.end = end
        self.weight = weight





class Network:
    def __init__(self):
        self.fitness = 0

    def update_fitness(self, points, time):
        """
        Berechnet und aktualisiert den Fitness-Wert des Netzwerks 
        basierend auf den Punkten (des 'Spielers') und der vergangenen Zeit.
        """
        self.fitness = points - 50 * time

    def evaluate(self, values):
        """
        Wertet das Netzwerk aus. 
        
        Argumente:
            values: eine Liste von 27x18 = 486 Werten, welche die aktuelle diskrete Spielsituation darstellen
                    die Werte haben folgende Bedeutung:
                     1 steht fuer begehbaren Block
                    -1 steht fuer einen Gegner
                     0 leerer Raum
        Rueckgabewert:
            Eine Liste [a, b, c] aus 3 Boolean, welche angeben:
                a, ob die Taste "nach Links" gedrueckt ist
                b, ob die Taste "nach Rechts" gedrueckt ist
                c, ob die Taste "springen" gedrueckt ist.
        """

        return [False, False, False]
