import math
import matplotlib.pyplot as plt


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


class Bird:
    def __init__(self):
        self.position = Vector(0, 0)

    def move(self):
        ...

    def draw(self, ax, forces=False):
        ax.scatter([self.position.x], [self.position.y])
        if forces:
            ax.set_xlim(self.position.x - 2, self.position.x + 2)
            ax.set_ylim(self.position.y - 2, self.position.y + 2)
            ax.plot([self.position.x, 1], [self.position.y, 1])


def main():
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15, 10), dpi=75)
    ax[0].set_aspect('equal')
    ax[0].set_xlim(-1, 11)
    ax[0].set_ylim(-1, 11)
    ax[1].set_aspect('equal')

    folder = "result/"

    a = Vector(5, 10)
    b = Bird()

    b.draw(ax[0])
    b.draw(ax[1], forces=True)

    print(a)
    print(a.length())
    a.normalize()
    print(a)

    fig.savefig(folder + "pipop.png")


if __name__ == '__main__':
    main()
