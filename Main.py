import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from random import *

## white: free, black: wall, purple: start/goal, green: optimal path, blue: all visited, red: fire
color_set = ['white', 'black', 'purple']
range_set = np.array([-0.5, 0.5, 2.5, 4.5])

def main():
    dimension = int(sys.argv[1])
    density = float(sys.argv[2])
    algorithm = sys.argv[3]
    print(algorithm)
    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')
    maze = generate_maze(dimension, density)
    plt.imshow(maze, cmap = cmap, norm = norm)
    plt.show()

def generate_maze(dimension, density):
    maze = np.zeros((dimension, dimension), int)
    maze[0][0] = 3 # start
    maze[dimension - 1][dimension - 1] = 4 # goal

    for x in range(0, dimension):
        for y in range(0, dimension):
            if (x == 0 and y == 0) or (x == dimension - 1 and y == dimension - 1):
                continue # ignore start and goal
            if random() < density:
                maze[x][y] = 1 # fill with wall

    return maze

main()