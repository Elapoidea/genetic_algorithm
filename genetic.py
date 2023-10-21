from random import randint;
from copy import deepcopy;
from config import *;

class Individual:
    def __init__(self, chromosome, chromosome_length):
        self.chromosome = chromosome;
        self.chromosome_length = chromosome_length;
        self.score = 0;

    def mutate(self):
        if randint(1, 100) <= MUTATE_CHANCE:
            line = randint(1, self.chromosome_length-1);
    
            self.chromosome = [1 - self.chromosome[i] if i < line else self.chromosome[i] for i in range(self.chromosome_length)]

            print("Mutated!");


        # self.chromosome = list(map(lambda gene: gene if randint(1, 100) >= MUTATE_CHANCE else 1 - gene, self.chromosome));

    def randomize(self):
        self.chromosome = [randint(0, 1) for _ in range(self.chromosome_length)];

    def cross(self, other):
        line = randint(1, self.chromosome_length-1);
        self.chromosome = [self.chromosome[i] if i < line else other.chromosome[i] for i in range(self.chromosome_length)]

class Population:
    def __init__(self, population_size, chromosome_length, score_function, fitness_function):
        self.fitness_function = fitness_function;
        self.score_function = score_function;
        self.organisms = [];

        for _ in range(population_size):
            i = Individual([], chromosome_length);
            i.randomize();
        
            self.organisms.append(i);

        self.sort();
    
    def sort(self):
        self.organisms.sort(key=lambda e : self.fitness_function(e));
    
    def calculate_scores(self):
        for i, s in enumerate(self.score_function(self)):
            self.organisms[i].score = s;

    def next_generation(self):
        fittest = self.organisms[::-1][:int(len(self.organisms)/2)]
        new_generation = [];

        for i in range(0, len(fittest), 2):
            child1 = deepcopy(fittest[i]);
            child2 = deepcopy(fittest[i]);

            child1.cross(deepcopy(fittest[i + 1]));
            child2.cross(deepcopy(fittest[i + 1]));

            child1.mutate();
            child2.mutate();

            child3 = deepcopy(fittest[i]);
            child4 = deepcopy(fittest[i]);

            child3.cross(deepcopy(fittest[i + 1]));
            child4.cross(deepcopy(fittest[i + 1]));

            child3.mutate();
            child4.mutate();

            new_generation.append(child1);
            new_generation.append(child2);
            new_generation.append(child3);
            new_generation.append(child4);
        

        self.organisms = new_generation;
        self.calculate_scores();
        self.sort();

class Phylogeny:
    def __init__(self, population_size, chromosome_length, score_function, fitness_function):
        self.population_size = population_size;
        self.population = Population(population_size, chromosome_length, score_function, fitness_function);
        self.generations = 0;

    def evolve(self, generations, display=False):
        for _ in range(generations):
            self.population.next_generation();
            self.generations += 1;
    
            if display: self.display();


    def display(self):
        print(f'Generation #{self.generations}:')

        average = 0;

        for i in self.population.organisms:
            average += i.score / self.population_size

        print(f'Average score of generation: {average}');

        # for organism in self.population.organisms:
        #     print(''.join(map(str, organism.chromosome)))

        print('\n')

if __name__ == '__main__':
    x = Phylogeny(POPULATION_SIZE, CHROMOSOME_LENGTH);
    x.evolve(20, True);


