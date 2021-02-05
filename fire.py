import numpy as np
from astar import *
from bfs import *
from random import *

def advance_fire_one_step(maze, q):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    for x in range(0, dimension):
        for y in range(0, dimension):
            if maze[x][y] != 1 and maze[x][y] != 7 and maze[x][y] != 4:
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
                    if maze_copy[x][y] != 6:
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

    return fire_maze

def strategy_one(maze, fire, start, goal, q):
    fire_maze = np.copy(fire)
    status, traversal_path = bfs(fire_maze, start, goal)
    if status == 'No Solution':
        print('No path possible')
        return fire_maze

    dimension = maze.shape[0]

    curX = 0
    curY = 0

    while fire_maze[curX][curY] != 7:
        if fire_maze[curX][curY] == 4:
            print('Escaped')
            return fire_maze

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

        fire_maze = advance_fire_one_step(fire_maze, 0.7)
        
    print('Died')
    return fire_maze



