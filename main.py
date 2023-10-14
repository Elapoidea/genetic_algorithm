from random import randint;
from copy import deepcopy;

MUTATE_CHANCE = 10;
CHROMOSOME_LENGTH = 40;
POPULATION_SIZE = 40; # MUST BE A MULTIPLE OF 4

class Individual:
    def __init__(self, chromosome, chromosome_length):
        self.chromosome = chromosome;
        self.chromosome_length = chromosome_length;

    def mutate(self):
        self.chromosome = list(map(lambda gene: gene if randint(0, 100) > MUTATE_CHANCE else 1 - gene, self.chromosome));

    def randomize(self):
        self.chromosome = [randint(0, 1) for _ in range(self.chromosome_length)];

    def cross(self, other):
        line = randint(1, self.chromosome_length-1);
        self.chromosome = [self.chromosome[i] if i < line else other.chromosome[i] for i in range(self.chromosome_length)]

class Population:
    def __init__(self, population_size, chromosome_length, fitness_function):
        self.organisms = [];

        for _ in range(population_size):
            i = Individual([], chromosome_length);
            i.randomize();
        
            self.organisms.append(i);

        self.fitness_function = fitness_function;

    def next_generation(self):
        self.organisms.sort(key=lambda e : self.fitness_function(e));
        fittest = self.organisms[::-1][:int(len(self.organisms)/2)]
        new_generation = [x for x in fittest];

        for i in range(0, len(fittest), 2):
            organism1 = deepcopy(fittest[i]);
            organism1.cross(deepcopy(fittest[i + 1]));
            organism1.mutate();

            new_generation.append(organism1);
        
            organism2 = deepcopy(fittest[i]);
            organism2.cross(deepcopy(fittest[i + 1]));
            organism2.mutate();

            new_generation.append(organism2);


        self.organisms = new_generation;
        self.organisms.sort(key=lambda e : self.fitness_function(e));
        


class Phylogeny:
    def __init__(self, population_size, chromosome_length):
        self.population_size = population_size;
        self.population = Population(population_size, chromosome_length, lambda x : x.chromosome.count(1));
        self.generations = 1;

    def evolve(self, generations, display=False):
        if display: self.display();

        for _ in range(generations):
            self.population.next_generation();
            self.generations += 1;
    
            if display: self.display();


    def display(self):
        print(f'Generation #{self.generations}:')

        for organism in self.population.organisms:
            print(''.join(map(str, organism.chromosome)))

        print('\n')

if __name__ == "__main__":
    x = Phylogeny(POPULATION_SIZE, CHROMOSOME_LENGTH);
    x.evolve(20, True);

