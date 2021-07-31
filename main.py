import math
import matplotlib.pyplot as plt
import random
import os
import glob
from PIL import Image


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        self.x = self.x / self.length()
        self.y = self.y / self.length()

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)
        
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Vector(x, y)

    def __mod__(self, other):
        x = self.x % other.x
        y = self.y % other.y
        return Vector(x, y)


class Bird:
    def __init__(self, origin, dim):
        self.position = Vector(origin.x + random.random() * dim.x, origin.y + random.random() * dim.y)
        self.vitesse = Vector(random.random() - 0.5, random.random() - 0.5)
        self.origin = origin
        self.dim = dim
        self.fleeing_radius = 1.

    def move(self, new_position):
        self.position = new_position

    def next_position(self):
        new_position = self.position + self.vitesse
        new_position = self.clamp_position(new_position)
        return new_position

    def clamp_position(self, position_to_clamp):
        new_pos = ((position_to_clamp - self.origin) % Vector(10, 10)) + self.origin
        return new_pos


    def draw(self, ax, forces=False):
        ax.scatter([self.position.x], [self.position.y], c="b")
        if forces:
            ax.add_patch(plt.Circle((self.position.x, self.position.y), self.fleeing_radius, ec='r', fill=False))
            ax.plot([self.position.x, self.position.x + self.vitesse.x ], [self.position.y, self.position.y + self.vitesse.y])

def to_gif():
    frames = []
    imgs = glob.glob("result/*.png")
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save('animated.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=150, loop=0)

def main():
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 10), dpi=75)
    ax[0].set_aspect('equal')
    ax[1].set_aspect('equal')

    folder = "result/"

    for file in glob.glob(folder + "*.png"):
        os.remove(file)

    origin, dim = Vector(0, 0), Vector(10, 10)
    n_step = 30
    n_bird = 20
    random.seed(1)

    #liste temporaire de Boids
    boids_list = []
    bird1 = Bird(origin, dim)
    boids_list.append(bird1)
    for i in range(n_bird):
        boids_list.append(Bird(origin, dim))

    #boucle de mouvement de Boids temporaire
    for step in range(n_step):
        print("computing step : {}".format(step))
        next_boids_position = []
        for elem in boids_list:
            next_boids_position.append(elem.next_position())

        for elem, next_pos in zip(boids_list, next_boids_position):
            elem.move(next_pos)
            elem.draw(ax[0])

        ax[0].set_xlim(origin.x - 1, origin.x + dim.x + 1)
        ax[0].set_ylim(origin.y - 1, origin.y + dim.y + 1)
        ax[0].set_title("Step: {}".format(step))

        for elem in boids_list:
            elem.draw(ax[1], forces=True)
        
        ax[1].set_xlim(bird1.position.x - 2, bird1.position.x + 2)
        ax[1].set_ylim(bird1.position.y - 2, bird1.position.y + 2)

        ax[0].scatter([bird1.position.x], [bird1.position.y], facecolors='c', marker="o", color="r", s=64)

        fig.savefig(folder + "step_" + str(f'{step:04}') + ".png")
        ax[0].clear()
        ax[1].clear()

    print("converting to gif")
    to_gif()


if __name__ == '__main__':
    main()
