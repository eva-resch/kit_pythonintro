from src.neat.network import Network
from time import time
from pickle import dump, load
import numpy as np
from copy import deepcopy


class Population:
    """
    Class representing a whole population of 'Network' instances, each belonging to a certain generation.
    Between generations there is: selection of the fittest networks; mutation of those selected networks.

    Methods
    -------
        load_from_file(filename):
            Gets the path 'filename' for a pickeled file, then unpickles it to get the saved population.
        save_to_file(filename):
            Pickles the current population and saves it to the path 'filename'.
        create_next_generation(self): list(Network)
            Takes current generation 'self', selects and mutates to get new generation 'list(Network)'.
    """
    def __init__(self, seed, size):
        """
        Initialise a new population of 'size'=n elements of 'Network', all of which will be directly mutated by adding
        an edge.
        There are the attributes 'seed' for the random generator, 'generation_count' and an identifying 'name',
        the current time stamp.

        Parameters
        ----------
            seed: int
                For the random generator
            size: int
                The amount of instances of 'Network', that will make up the population
        """
        self.seed = seed
        self.size = size

        self.name = str(time())
        # The attribute 'generation_count' will be incremented automatically by the game Gadakeco.
        self.generation_count = 1

        self.current_generation = []
        for i in range(size):
            new = Network()
            self.current_generation.append(new.edge_mutation())

    @staticmethod
    def load_from_file(filename):
        print("called load_from_file")
        return load(filename)

    def save_to_file(self, filename):
        dump(self, filename)
        print("called save_to_file")

    def create_next_generation(self):
        """
        Step 1: Take list 'current_generation', sort in descending order by return values of given 'key'-function, in
                this case by fitness value
        Step 2: Take the first 10% of the ordered 'current_generation' to use it unmodified for new generation
                -> 'new_10'
        Step 3: Make 8 deepcopies of 'new_10' for the 80% mutated by adding a new edge and use 'edge_mutation'
                Make a deepcopy of 'new_10' for the 10% mutated by adding a new node and use 'node_mutation'

        Returns
        -------
            new_generation: list(Network)
                    new generation with best networks and mutations
        """

        # TODO: Überprüfen, dass Größe nicht zu groß (oder klein) wird. (Eher zu groß, da obere Gaußklammer verwendet)

        # Step 1
        ordered_current_generation = sorted(self.current_generation, reverse=True, key=Network.get_fitness)

        # Step 2
        new_10 = ordered_current_generation[: np.ceil(0.1*len(ordered_current_generation))]
        new_generation = new_10

        # Step 3
        for i in range(8):
            for net in new_10:
                new_generation.append(deepcopy(net).edge_mutation())

        for net in new_10:
            new_generation.append(deepcopy(net).node_mutation())

        return new_generation
