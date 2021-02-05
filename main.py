import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
from random import *
from dfs import *
from bfs import *
from astar import *

## white: free, black: wall, purple: start/goal, green: optimal path, blue: all visited, red: fire
color_set = ['white', 'black', 'purple', 'blue', 'green', 'red']
range_set = np.array([-0.5, 0.5, 2.5, 4.5, 5.5, 6.5, 7.5])

def main():
    dimension = int(sys.argv[1])
    density = float(sys.argv[2])

    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    '''
    maze = generate_maze(dimension, density)

    status, astar_maze = astar(maze, (0, 0), (dimension - 1, dimension - 1))
    print(status)

    status, dfs_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))
    print(status)

    status, bfs_maze = bfs(maze, (0, 0), (dimension - 1, dimension - 1))
    print(status)

    plt.imshow(astar_maze, cmap = cmap, norm = norm)
    plt.savefig('astar.jpg')
    plt.imshow(dfs_maze, cmap = cmap, norm = norm)
    plt.savefig('dfs.jpg')
    plt.imshow(bfs_maze, cmap = cmap, norm = norm)
    plt.savefig('bfs.jpg')
    '''
    maze = generate_maze(dimension, density)
    
    start_time = time.time()
    status, astar_maze = astar(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)

    start_time = time.time()
    status, bfs_maze = bfs(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)

    start_time = time.time()
    status, dfs_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)

    plt.imshow(astar_maze, cmap = cmap, norm = norm)
    plt.savefig('astar.jpg')

    plt.imshow(bfs_maze, cmap = cmap, norm = norm)
    plt.savefig('bfs_maze')

    plt.imshow(dfs_maze, cmap = cmap, norm = norm)
    plt.savefig('dfs_maze')

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
# test
main()
