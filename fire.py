import numpy as np
from astar import *
from bfs import *
from random import *
"""
This file contains the implementation for initializing the fire maze, spreading the fire, and
three strategies a mazerunner could use to escape a maze that is on fire.

Authors: Ashwin Haridas, Ritin Nair
"""

"""
This function uses the probability of a fire spreading to a cell based on the number of neighbors of the cell that are on fire and
the flammability on all cells of the maze to spread the fire after one time step.

Input: The fire maze and the flammability
Output: The fire maze with the fire after one time step
"""
def advance_fire_one_step(maze, q):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    # go through every cell in the maze and based on some probability assign the cell to be on fire
    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] != 1 and maze[x][y] != 7 and maze[x][y] != 4 and maze[x][y] != 3: # not a wall, on fire, start, or goal
                k = 0 # this is the number of neighbors of the current cell that are on fire
                if x - 1 >= 0:
                    if maze[x - 1][y] == 7:
                        k += 1
                if x + 1 < dimension:
                    if maze[x + 1][y] == 7:
                        k += 1
                if y - 1 >= 0:
                    if maze[x][y - 1] == 7:
                        k += 1
                if y + 1 < dimension:
                    if maze[x][y + 1] == 7:
                        k += 1
                prob = 1 - (1 - q) ** k # this formula calculates the probability that the cell should catch on fire
                if random() <= prob: # sets the cell on fire based on the above probability
                    maze_copy[x][y] = 7
    
    return maze_copy

"""
This function picks a random cell in the maze that is not a wall and sets it on fire to initialize the fire maze.
Input: The maze to be set on fire
Output: The fire maze and the cell that the fire starts at
"""

def init_fire(maze):
    fire_maze = np.copy(maze)
    dimension = fire_maze.shape[0]

    # pick a random cell to be on fire
    randX = randint(1, dimension - 1)
    randY = randint(1, dimension - 1)

    while fire_maze[randX][randY] == 1: # keep changing the values of the cell's coordinate until the cell is valid/not a wall
        randX = randint(1, dimension - 1)
        randY = randint(1, dimension - 1)
    
    fire_maze[randX][randY] = 7 # set the cell on fire

    return fire_maze, (randX, randY)

"""
This function is the first strategy for having the runner escape the fire maze. It works by finding the shortest path from the start
to the goal using BFS and following that path until the runner either escapes, is blocked off by the fire, or dies to the fire.

Input: The maze, the initial fire maze, the starting point, the goal point, and the flammability of the fire
Output: The status of the traversal and the fire maze
"""
def strategy_one(maze, fire, start, goal, q):
    fire_maze = np.copy(fire)
    status, traversal_path, num_explored_nodes = bfs(fire_maze, start, goal) # finds the shortest path from the start to the goal if one exists

    if status == 'No Solution':
        return 'No Path Possible', fire_maze

    dimension = maze.shape[0]

    curX = 0
    curY = 0

    while fire_maze[curX][curY] != 7: # while the runner is not on a cell that is on fire
        if fire_maze[curX][curY] == 4: # the runner has reached the goal and escaped successfully
            return 'Escaped', fire_maze

        if fire_maze[curX][curY] != 3: # not the start
            fire_maze[curX][curY] = 6
        
        # calculate which cell is the next one on the path to the goal
        if curX + 1 < dimension and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4) and fire_maze[curX + 1][curY] != 6:
            curX = curX + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4) and fire_maze[curX - 1][curY] != 6:
            curX = curX - 1
        elif curY + 1 < dimension and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4) and fire_maze[curX][curY + 1] != 6:
            curY = curY + 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1] == 6 or traversal_path[curX][curY - 1] == 4) and fire_maze[curX][curY - 1] != 6:
            curY = curY - 1

        # after the runner has effectively moved to the above mentioned cell the fire must be advanced one step
        fire_maze = advance_fire_one_step(fire_maze, q)
        
    return 'Died', fire_maze

"""
This function is the second strategy for the mazerunner escaping a maze that is on fire. At each step the path to the
goal is recomputed using BFS to account for the current state of the fire in the maze.

Input: The maze, the initial fire maze, the starting point, the goal point, and the flammability of the fire
Output: The status of the traversal and the fire maze
"""

def strategy_two(maze, fire, start, goal, q):
    fire_maze = np.copy(fire)
    temp_maze = np.copy(fire)
    dimension = maze.shape[0]
    temp_start = start

    curX = 0
    curY = 0

    while fire_maze[curX][curY] != 4: # goal
        
        if fire_maze[curX][curY] == 7: # runner is at a cell that is on fire
            return 'Died', fire_maze

        # calculate the path from the current cell to the goal at every step
        status, traversal_path, num_explored_nodes = bfs(temp_maze, temp_start, goal)

        if status == 'No Solution': # the BFS call resulted in no path from the start to the goal being possible 
            return 'No Path Possible', fire_maze
        
        # move to the next cell on the path
        if curX + 1 < dimension and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4):
            curX = curX + 1
        elif curY + 1 < dimension and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4):
            curY = curY + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4):
            curX = curX - 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1 ] == 6 or traversal_path[curX][curY - 1] == 4):
            curY = curY - 1
        
        if fire_maze[curX][curY] == 4: # goal is reached
            break

        fire_maze[curX][curY] = 6
        temp_start = (curX, curY)

        # advance the fire one step after the runner takes a step 
        fire_maze = advance_fire_one_step(fire_maze, q)
        temp_maze = reset_path(fire_maze, dimension) # allows BFS to let the runner go back up the current path if necessary

    return 'Escaped', fire_maze

"""
This function is the third strategy for the mazerunner escaping a maze this is on fire. It uses a modified version of the 
A* algorithm to find a path from the start to the goal that accounts for the current state of the fire in the maze and what the
fire will look like in future steps as well. This is done by checking the probability of cells in the maze being on fire at
some n time steps into the future.

Input: The maze, the initial fire maze, the starting point, the goal point, and the flammability of the fire
Output: The status of the traversal and the fire maze
"""
def strategy_three(maze, fire, start, goal, q):
    dimensions = maze.shape[0]
    fire_maze = np.copy(fire)
    curX = 0
    curY = 0
    n = find_time_steps(start, goal)

    # create a probability maze to predict the probability of each cell being on fire at n steps into the future
    probability_maze = init_probability_maze(fire_maze, dimensions)
    probability_maze = calculate_fire_probability(probability_maze, fire_maze, dimensions, q, n)

    status, traversal_path = astar_fire(fire_maze, start, goal, probability_maze) # find a path from the start to the goal

    if status == 'No Solution':
        return 'No Path Possible', fire_maze

    while fire_maze[curX][curY] != 4: # while the runner is not at the goal

        if fire_maze[curX][curY] == 7: # the runner is at a cell that is on fire
            return 'Died', fire_maze

        # find the next cell on the path
        if curX + 1 < dimensions and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4):
            curX = curX + 1
        elif curY + 1 < dimensions and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4):
            curY = curY + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4):
            curX = curX - 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1 ] == 6 or traversal_path[curX][curY - 1] == 4):
            curY = curY - 1
        
        if fire_maze[curX][curY] == 4: # the runner is at the goal
            break

        fire_maze[curX][curY] = 6
        current = (curX, curY)
        n = find_time_steps(current, goal)

        # advance the fire one step after the runner takes a step in the maze
        fire_maze = advance_fire_one_step(fire_maze, q)   
        temp_maze = reset_path(fire_maze, dimensions)

        # recalculate a path to the goal from the new current cell with a new probability maze
        probability_maze = init_probability_maze(fire_maze, dimensions)
        probability_maze = calculate_fire_probability(probability_maze, fire_maze, dimensions, q, n)
        status, traversal_path = astar_fire(temp_maze, current, goal, probability_maze) 

        if status == 'No Solution':
            return 'No Path Possible', fire_maze

    return 'Escaped', fire_maze

"""
This function initializes the probability maze by going through the current fire maze and checking all the cells that are on fire.
It gives these cells a probability of 1 because it is guaranteed they will stay on fire.

Input: The fire maze and the dimensions of the maze
Output: The initialized probability maze

"""
def init_probability_maze (fire_maze, dimensions):
    probability_maze = np.zeros((dimensions, dimensions))
    for x in range(0, dimensions):
        for y in range(0, dimensions):
            if(fire_maze[x][y] == 7): # cell is on fire
                probability_maze[x][y] = 1
    
    return probability_maze

"""
This function creates a probability maze that contains the probability of each cell in the maze being on
fire at n time steps into the future. 

Input: The initialized probability maze, the fire maze, the dimensions of the maze, the flammability, the number of steps
       to ahead to base the maze on
Output: The probability maze
"""
def calculate_fire_probability(probability_maze, fire_maze, dimensions, q, n):
    old_prob_maze = np.copy(probability_maze)
    maze_result = np.zeros((dimensions, dimensions))
    for i in range(0, int(n)):
        maze_result = np.zeros((dimensions, dimensions))
        for x in range(0, dimensions):
            for y in range(0, dimensions):
                if fire_maze[x][y] == 7: # cell is on fire
                    maze_result[x][y] = 1
                elif (fire_maze[x][y] != 1 or fire_maze[x][y] != 3 or fire_maze[x][y] != 4): # walls, start, and goal can not be on fire
                    k = 0 # expected number of neighbors of the current cell that are on fire
                    if x - 1 >= 0:
                        k += old_prob_maze[x - 1][y]
                    if x + 1 < dimensions:
                        k += old_prob_maze[x + 1][y]
                    if y - 1 >= 0:
                        k += old_prob_maze[x][y - 1]
                    if y + 1 < dimensions:
                        k += old_prob_maze[x][y + 1]
                    prob = 1 - (1 - q) ** k # probability that the current cell will be on fire
                    maze_result[x][y] = prob
            
        old_prob_maze = np.copy(maze_result) # keeps track of the probability maze from the previous time step to use in calculations 
    
    return maze_result

"""
This function allows the runner to go back to cells they have already gone to on the path in case they need to do so.

Input: The maze and its dimensions
Output: A copy of the maze with the path removed
"""
def reset_path(maze, dimension):
    temp_maze = np.copy(maze)
    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] == 6:
                temp_maze[x][y] = 0 # resets the path
    
    return temp_maze

"""
This function makes the number of time steps to predict ahead for in the probability maze based on the euclidean
distance from the current cell to the goal. This ratio was picked after testing to find what the optimal amount of
steps to predict ahead for at each part of the maze was.

Input: The current cell and the goal
Output: The number of steps to predict ahead for
"""
def find_time_steps(current, goal):
    return np.ceil( euclidean_distance(current, goal) / 5)