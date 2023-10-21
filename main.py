from turtle import *;
from colorsys import hsv_to_rgb;
from genetic import *;
from config import *;
from math import pi, cos, ceil;
import time;

screen = Screen();
screen.setup(RIGHT - LEFT + 2 * PADDING, TOP - BOTTOM + 2 * PADDING);

def point_in_box(pos):
    return pos[0] >= LEFT and pos[0] <= RIGHT and pos[1] <= TOP and pos[1] >= BOTTOM;

def draw_box():
    screen.bgcolor(BACKGROUND);
    b = Turtle();
    b.speed(0);
    b.ht();
    b.pencolor(BOX_COLOUR);
    b.penup();

    for p in [(LEFT, TOP), (LEFT, BOTTOM), (RIGHT, BOTTOM), (RIGHT, TOP)]:
        b.goto(p[0], p[1]);
        b.pendown();

def draw_population(population):
    screen.clearscreen()
    draw_box();

    a = population.organisms;

    pens = [];
    lengths = [1 for _ in range(POPULATION_SIZE)];
    heights = [1 for _ in range(POPULATION_SIZE)];

    for i in range(POPULATION_SIZE):
        t = Turtle();

        t.penup();
        t.speed(0);
        t.ht();
        t.goto(-ceil(i/2) * cos(i * pi), BOTTOM);
        #t.goto(POPULATION_SIZE / 2 - i, BOTTOM + PADDING + i * 2);
        # t.goto(0, BOTTOM);
        t.pendown();
        t.left(INITIAL_ANGLE)

        pens.append(t);


    for gene_i in range(CHROMOSOME_LENGTH):
        for i, t in enumerate(pens):
            if t.pos()[1] - BOTTOM > heights[i]: heights[i] = t.pos()[1] - BOTTOM;
            if not point_in_box(t.pos()): continue;

            t.pencolor(hsv_to_rgb(i / POPULATION_SIZE, 0.75, lengths[i] / CHROMOSOME_LENGTH * 0.7 + 0.3));

            gene = a[i].chromosome[gene_i];
    
            if gene == 1:
                t.right(ANGLE);

            if gene == 0:
                t.left(ANGLE);

            t.forward(STRENGTH);

            lengths[i] += 1;
    
    # print(heights);

    # for i in range(len(lengths)):
        # print(1.2 - 0.2 * (TOP - BOTTOM) / (heights[i]), heights[i]);
        # print(1 / (6 - 5 * heights[i] / (TOP - BOTTOM)), heights[i] / (TOP - BOTTOM));

    # return [(heights[i] - BOTTOM + STRENGTH) / j for i, j in enumerate(lengths)];
    #return [1 / (6 - 5 * heights[i] / (TOP - BOTTOM)) for i, j in enumerate(lengths)]
    return [(heights[i] / (TOP - BOTTOM))**2 * ((TOP - BOTTOM) / STRENGTH) / j for i, j in enumerate(lengths)]



if __name__ == '__main__':
    x = Phylogeny(POPULATION_SIZE, CHROMOSOME_LENGTH, draw_population, lambda x : x.score);
    x.evolve(1000, True);

    # Make all organisms draw at the same time with multiple asynchronous instances of turtles.

    exitonclick();


