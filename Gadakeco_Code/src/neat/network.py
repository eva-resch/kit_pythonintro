def sgn(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1

class Input_node:
    def __init__(self, input):
        """
        Der Konstruktor weißt dem Input-Node den Wert 1 zu, falls der Block begehbar ist. Ansonsten wird 0 zugewiesen.
        """
        self.out = input
        self.output_edges = []

    def get_out(self):
        """
        Gibt den Output-Wert zurueck.
        """
        return self.out

    def add_out_edge(self, edge):
        self.output_edges.append(edge)


class Hidden_node:
    def __init__(self):
        self.input = None
        self.out = None

    def get_input(self):
        return self.input

    def get_out(self):
        return self.out

class Output_node:
    pass








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
