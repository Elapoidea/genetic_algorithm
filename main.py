from turtle import *;
from colorsys import hsv_to_rgb;
from genetic import *;
from config import *;

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

def draw_organism(organism, number):
    o = Turtle();
    o.speed(0);
    o.ht();

    o.penup();
    o.goto(0, BOTTOM);
    o.pendown();
    o.left(INITIAL_ANGLE)

    length = 0;

    for gene in organism.chromosome:
        o.pencolor(hsv_to_rgb(number / POPULATION_SIZE, 0.75, 1 - length / CHROMOSOME_LENGTH * 0.6));

        if gene == 1:
            o.right(ANGLE);

        if gene == 0:
            o.left(ANGLE);

        o.forward(STRENGTH);

        if not point_in_box(o.pos()): break;
    
        length += 1;

    return (o.pos()[1] - BOTTOM + STRENGTH) / length;

def draw_population(population):
    screen.clearscreen()
    draw_box();

    a = population.organisms;

    for i in range(len(a)):
        a[i].score = draw_organism(a[i], i);


if __name__ == '__main__':
    x = Phylogeny(POPULATION_SIZE, CHROMOSOME_LENGTH, draw_population, lambda x : x.score);
    x.evolve(200);

    # Make all organisms draw at the same time with multiple asynchronous instances of turtles.

    exitonclick();


