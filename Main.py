import numpy as np
import matplotlib.pyplot as plt
from random import *

def main():
    maze = generate_maze(10, 0.3)
    plt.imshow(maze)
    plt.show()

def generate_maze(dimension, density):
    maze = np.zeros((dimension, dimension), int)
    maze[0][0] = 2 # start
    maze[dimension - 1][dimension - 1] = 3 # goal

    for x in range(0, dimension):
        for y in range(0, dimension):
            if (x == 0 and y == 0) or (x == dimension - 1 and y == dimension - 1):
                continue
            if(random() < density):
                maze[x][y] = 1 # fill with wall

    return maze


main()