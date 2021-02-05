import numpy as np
from astar import *
from random import *

def advance_fire_one_step(maze, q):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] != 1 and maze[x][y] != 6:
                k = 0
                if x - 1 >= 0:
                    if maze[x - 1][y] == 6:
                        k += 1
                if x + 1 < dimension:
                    if maze[x + 1][y] == 6:
                        k += 1
                if y - 1 >= 0:
                    if maze[x][y - 1] == 6:
                        k += 1
                if y + 1 < dimension:
                    if maze[x][y + 1] == 6:
                        k += 1
            prob = 1 - (1 - q) ** k
            if random() <= prob:
                maze_copy[x][y] = 6
    
    return maze_copy

