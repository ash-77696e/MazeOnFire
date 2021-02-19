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

# white: free, black: wall, purple: start/goal, green: optimal path, blue: all visited, red: fire
color_set = ['white', 'black', 'purple', 'blue', 'green', 'red', 'pink']
range_set = np.array([-0.5, 0.5, 2.5, 4.5, 5.5, 6.5, 7.5, 8.5])

def main():
    #test_fire_strategies()
    test_path_algorithms()
    #run_strat_trials()

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

        while status != 'Success':
            maze = generate_maze(dimension, density)
            status, trial_maze = dfs(maze, (0, 0), (dimension - 1, dimension - 1))
        
        currentIterSuccesses = 0
        fireTrials = 0

        while fireTrials < 10:
            fire_maze, fireCoord = init_fire(maze)
            status, trial_maze = dfs(fire_maze, (0, 0), fireCoord)

            while status != 'Success':
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
    
def test_fire_strategies():
    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    dimension = int(sys.argv[1])
    density = float(sys.argv[2])
    flammability = float(sys.argv[3])

    maze = generate_maze(dimension, density)
    fire_maze, fireCoord = init_fire(maze)

    status, fire_result = strategy_one(maze, fire_maze, (0, 0), (dimension - 1, dimension - 1), flammability)
    status, fire_result2 =  strategy_two(maze, fire_maze, (0,0), (dimension - 1, dimension - 1), 0.3)
    status, fire_result3 =  strategy_three(maze, fire_maze, (0,0), (dimension - 1, dimension - 1), flammability)

    plt.imshow(fire_result, cmap = cmap, norm = norm)
    plt.savefig('fire_strat1.jpg')

    plt.imshow(fire_result2, cmap = cmap, norm = norm)
    plt.savefig('fire_strat2.jpg')

    plt.imshow(fire_result3, cmap = cmap, norm = norm)
    plt.savefig('fire_strat3.jpg')

def test_path_algorithms():
    dimension = int(sys.argv[1])
    density = float(sys.argv[2])

    cmap = colors.ListedColormap(color_set)
    norm = colors.BoundaryNorm(range_set, len(color_set))
    plt.figure(figsize = (8, 8))
    plt.axis('off')

    maze = generate_maze(dimension, density)

    #prob_success = success_chance(dimension, density)
    #print('Probabilty S can be reached from G is: ' + str(prob_success))

    #diff_explored = difference_explored(dimension, density)
    #print('Average difference explored between BFS and A* is: ' + str(diff_explored))
    
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
    
    
    plt.imshow(astar_maze, cmap = cmap, norm = norm)
    plt.savefig('astar_maze.jpg')
    
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

def success_chance(dimension, density): # runs 100 trials per obstacle density and returns the chance a path can be found from S to G
    num_success = 0
    for i in range(0, 100):
        maze_trial = generate_maze(dimension, density)
        status, maze_copy = dfs(maze_trial, (0, 0), (dimension - 1, dimension - 1))
        if status == 'Success':
            num_success += 1

    return (num_success / 100)

def difference_explored(dimension, density):
    total_difference = 0

    for i in range(0, 100):
        maze_trial = generate_maze(dimension, density)
        status, maze_copy, num_explored_bfs = bfs(maze_trial, (0, 0), (dimension - 1, dimension - 1))
        status, maze_copy, num_explored_astar = astar(maze_trial, (0, 0), (dimension - 1, dimension - 1))
        total_difference += (num_explored_bfs - num_explored_astar)
    
    return (total_difference / 100)

if __name__ == '__main__':
    main()