import numpy as np
from astar import *
from bfs import *
from random import *

def advance_fire_one_step(maze, q):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] != 1 and maze[x][y] != 7 and maze[x][y] != 4 and maze[x][y] != 3:
                k = 0
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
                prob = 1 - (1 - q) ** k
                if random() <= prob:
                    maze_copy[x][y] = 7
    
    return maze_copy

def init_fire(maze):
    fire_maze = np.copy(maze)
    dimension = fire_maze.shape[0]
    randX = randint(1, dimension - 1)
    randY = randint(1, dimension - 1)

    while fire_maze[randX][randY] == 1:
        randX = randint(1, dimension - 1)
        randY = randint(1, dimension - 1)
    
    fire_maze[randX][randY] = 7

    print(str(randX) + ','  + str(randY))

    return fire_maze, (randX, randY)

def strategy_one(maze, fire, start, goal, q):
    fire_maze = np.copy(fire)
    status, traversal_path, num_explored_nodes = bfs(fire_maze, start, goal)

    if status == 'No Solution':
        return 'No Path Possible', fire_maze

    dimension = maze.shape[0]

    curX = 0
    curY = 0

    while fire_maze[curX][curY] != 7:
        if fire_maze[curX][curY] == 4:
            return 'Escaped', fire_maze

        if fire_maze[curX][curY] != 3:
            fire_maze[curX][curY] = 6
        
        if curX + 1 < dimension and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4) and fire_maze[curX + 1][curY] != 6:
            curX = curX + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4) and fire_maze[curX - 1][curY] != 6:
            curX = curX - 1
        elif curY + 1 < dimension and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4) and fire_maze[curX][curY + 1] != 6:
            curY = curY + 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1] == 6 or traversal_path[curX][curY - 1] == 4) and fire_maze[curX][curY - 1] != 6:
            curY = curY - 1

        fire_maze = advance_fire_one_step(fire_maze, q)
        
    return 'Died', fire_maze

def strategy_two(maze, fire, start, goal, q):
    fire_maze = np.copy(fire)
    temp_maze = np.copy(fire)
    dimension = maze.shape[0]
    temp_start = start

    curX = 0
    curY = 0

    while fire_maze[curX][curY] != 4: # goal
        
        if fire_maze[curX][curY] == 7:
            return 'Died', fire_maze

        status, traversal_path, num_explored_nodes = bfs(temp_maze, temp_start, goal) 

        if status == 'No Solution':
            return 'No Path Possible', fire_maze
        
        if curX + 1 < dimension and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4):
            curX = curX + 1
        elif curY + 1 < dimension and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4):
            curY = curY + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4):
            curX = curX - 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1 ] == 6 or traversal_path[curX][curY - 1] == 4):
            curY = curY - 1
        
        if fire_maze[curX][curY] == 4:
            break

        fire_maze[curX][curY] = 6
        temp_start = (curX, curY)

        fire_maze = advance_fire_one_step(fire_maze, q)
        temp_maze = reset_path(fire_maze, dimension) # avoid backtracking unless necessary

    return 'Escaped', fire_maze


def strategy_three(maze, fire, start, goal, q):
    dimensions = maze.shape[0]
    fire_maze = np.copy(fire)
    curX = 0
    curY = 0
    n = find_time_steps(start, goal)

    probability_maze = init_probability_maze(fire_maze, dimensions)
    probability_maze = calculate_fire_probability(probability_maze, fire_maze, dimensions, 0.3, n)
    status, traversal_path = astar_fire(fire_maze, start, goal, probability_maze)

    if status == 'No Solution':
        return 'No Path Possible', fire_maze

    while fire_maze[curX][curY] != 4:

        if fire_maze[curX][curY] == 7:
            return 'Died', fire_maze


        if curX + 1 < dimensions and (traversal_path[curX + 1][curY] == 6 or traversal_path[curX + 1][curY] == 4):
            curX = curX + 1
        elif curY + 1 < dimensions and (traversal_path[curX][curY + 1] == 6 or traversal_path[curX][curY + 1] == 4):
            curY = curY + 1
        elif curX - 1 >= 0 and (traversal_path[curX - 1][curY] == 6 or traversal_path[curX - 1][curY] == 4):
            curX = curX - 1
        elif curY - 1 >= 0 and (traversal_path[curX][curY - 1 ] == 6 or traversal_path[curX][curY - 1] == 4):
            curY = curY - 1
        
        if fire_maze[curX][curY] == 4:
            break

        fire_maze[curX][curY] = 6
        current = (curX, curY)
        n = find_time_steps(current, goal)
        fire_maze = advance_fire_one_step(fire_maze, q)   
        temp_maze = reset_path(fire_maze, dimensions)
        probability_maze = init_probability_maze(fire_maze, dimensions)
        probability_maze = calculate_fire_probability(probability_maze, fire_maze, dimensions, q, n)
        status, traversal_path = astar_fire(temp_maze, current, goal, probability_maze)

        if status == 'No Solution':
            return 'No Path Possible', fire_maze

    return 'Escaped', fire_maze


def init_probability_maze (fire_maze, dimensions):
    probability_maze = np.zeros((dimensions, dimensions))
    for x in range(0, dimensions):
        for y in range(0, dimensions):
            if(fire_maze[x][y] == 7):
                probability_maze[x][y] = 1
    
    return probability_maze

def calculate_fire_probability(probability_maze, fire_maze, dimensions, q, n):
    old_prob_maze = np.copy(probability_maze)
    maze_result = np.zeros((dimensions, dimensions))
    for i in range(0, int(n)):
        maze_result = np.zeros((dimensions, dimensions))
        for x in range(0, dimensions):
            for y in range(0, dimensions):
                if fire_maze[x][y] == 7:
                    maze_result[x][y] = 1
                elif (fire_maze[x][y] != 1 or fire_maze[x][y] != 3 or fire_maze[x][y] != 4):
                    k = 0
                    if x - 1 >= 0:
                        k += old_prob_maze[x - 1][y]
                    if x + 1 < dimensions:
                        k += old_prob_maze[x + 1][y]
                    if y - 1 >= 0:
                        k += old_prob_maze[x][y - 1]
                    if y + 1 < dimensions:
                        k += old_prob_maze[x][y + 1]
                    prob = 1 - (1 - q) ** k
                    maze_result[x][y] = prob
            
        old_prob_maze = np.copy(maze_result)
    
    return maze_result

def reset_path(maze, dimension):
    temp_maze = np.copy(maze)
    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] == 6:
                temp_maze[x][y] = 0
    
    return temp_maze

def find_time_steps(current, goal):
    return np.ceil( euclidean_distance(current, goal) / 5)