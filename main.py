import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import time
from random import *
from dfs import *
from bfs import *
from astar import *
from fire import *

"""
This python file is the main runner. It allows the user to test the three path finding algorithms and the three fire strategies.
Uncommenting the function that you want to test and passing the appropriate arguments via the command line (arguments are commented above each function)
will allow you to run the function.
Authors: Ashwin Haridas, Ritin Nair
"""

# white: free, black: wall, purple: start/goal, green: optimal path, blue: all visited, red: fire
color_set = ['white', 'black', 'purple', 'blue', 'green', 'red', 'pink']
range_set = np.array([-0.5, 0.5, 2.5, 4.5, 5.5, 6.5, 7.5, 8.5])

"""
Main function where you can run the path-finding algorithms or fire strategies
"""
def main():
    #test_fire_strategies()
    #test_path_algorithms()
    pass

"""
This function was made to run the compute the average success rate of each of the strategy trials
Command line arguments: dimension, density, flammability, and strategy (s1, s2, s3) in that order
"""
def run_strat_trials():
    dimension = int(sys.argv[1])
    density = float(sys.argv[2])
    flammability = float(sys.argv[3])
    strategy = sys.argv[4]
    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    mazeTrials = 0
    totalSuccesses = 0

    while mazeTrials < 10:
        maze = generate_maze(dimension, density)

        status, trial_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))

        while status != 'Success': # generate a valid maze (path from start to goal)
            maze = generate_maze(dimension, density)
            status, trial_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))
        
        currentIterSuccesses = 0
        fireTrials = 0

        while fireTrials < 10:
            fire_maze, fireCoord = init_fire(maze)
            status, trial_maze = dfs(fire_maze, (0, 0), fireCoord)

            while status != 'Success': # generate a valid initial fire
                fire_maze, fireCoord = init_fire(maze)
                status, trial_maze = dfs(fire_maze, (0, 0), fireCoord)

            if strategy == 's1':
                status, fire_result = strategy_one(maze, fire_maze, (0, 0), (dimension - 1, dimension - 1), flammability)
            elif strategy == 's2':
                status, fire_result = strategy_two(maze, fire_maze, (0, 0), (dimension - 1, dimension - 1), flammability)
            elif strategy == 's3':
                status, fire_result = strategy_three(maze, fire_maze, (0, 0), (dimension - 1, dimension - 1), flammability)

            if status == 'Escaped':
                currentIterSuccesses += 1
        
            fireTrials += 1
        
        totalSuccesses += currentIterSuccesses
        mazeTrials += 1
    
    print(totalSuccesses)

"""
This function was made to test our fire strategies.
Command line arguments: dimension, density, and flammability in that order
"""
def test_fire_strategies():
    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    dimension = int(sys.argv[1])
    density = float(sys.argv[2])
    flammability = float(sys.argv[3])

    maze = generate_maze(dimension, density)
    fire_maze, fireCoord = init_fire(maze) # initialize fire in maze

    # test each strategy
    status, fire_result = strategy_one(maze, fire_maze, (0, 0), (dimension - 1, dimension - 1), flammability)
    status, fire_result2 =  strategy_two(maze, fire_maze, (0,0), (dimension - 1, dimension - 1), flammability)
    status, fire_result3 =  strategy_three(maze, fire_maze, (0,0), (dimension - 1, dimension - 1), flammability)

    # plot result and save as image
    plt.imshow(fire_result, cmap = cmap, norm = norm)
    plt.savefig('fire_strat1.jpg')

    plt.imshow(fire_result2, cmap = cmap, norm = norm)
    plt.savefig('fire_strat2.jpg')

    plt.imshow(fire_result3, cmap = cmap, norm = norm)
    plt.savefig('fire_strat3.jpg')

"""
This function was made to test our path-finding algorithms
Command line arguments: dimension, density in that order
"""
def test_path_algorithms():
    dimension = int(sys.argv[1])
    density = float(sys.argv[2])

    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    maze = generate_maze(dimension, density) # generate maze
    
    # run each algorithm on maze and time them
    start_time = time.time()
    status, astar_maze, num_explored_nodes = astar(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)
    print(num_explored_nodes)
    
    start_time = time.time()
    status, bfs_maze, num_explored_nodes = bfs(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)
    print(num_explored_nodes)
    
    start_time = time.time()
    status, dfs_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))
    end_time = time.time()
    print(status)
    print(end_time - start_time)
    
    # plot each result and save as image
    plt.imshow(astar_maze, cmap = cmap, norm = norm)
    plt.savefig('astar_maze.jpg')
    
    plt.imshow(bfs_maze, cmap = cmap, norm = norm)
    plt.savefig('bfs_maze')
    
    plt.imshow(dfs_maze, cmap = cmap, norm = norm)
    plt.savefig('dfs_maze')

"""
This function was made to generate a maze
Input: dimension of maze, density (probabiliy of wall)
Output: maze with walls
"""
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

"""
This function was made to find the probability that a maze would be solved with DFS at an obstacle density
Input: dimension of maze, obstacle density
Output: average success rate at that obstacle density
"""
def success_chance(dimension, density): # runs 100 trials per obstacle density and returns the chance a path can be found from S to G
    num_success = 0
    for i in range(0, 100):
        maze_trial = generate_maze(dimension, density) # create maze
        status, maze_copy = dfs(maze_trial, (0, 0), (dimension - 1, dimension - 1)) # run dfs
        if status == 'Success':
            num_success += 1

    return (num_success / 100)

"""
This function was made to find the average difference of nodes explored between BFS and A* at an obstacle density
Input: dimension of maze, obstacle density
Output: average difference of nodes explored at that density
"""
def difference_explored(dimension, density):
    total_difference = 0

    for i in range(0, 100):
        maze_trial = generate_maze(dimension, density) # generate maze
        status, maze_copy, num_explored_bfs = bfs(maze_trial, (0, 0), (dimension - 1, dimension - 1)) # run bfs and get number of explored nodes
        status, maze_copy, num_explored_astar = astar(maze_trial, (0, 0), (dimension - 1, dimension - 1)) # run A* and get number of explored nodes
        total_difference += (num_explored_bfs - num_explored_astar)
    
    return (total_difference / 100)

if __name__ == '__main__':
    main()