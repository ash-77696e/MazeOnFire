import queue
import numpy as np
"""
This file contains the implementation for the BFS search algorithm used to find a path in the maze from the specified start node
to the specified goal node. 

Authors: Ashwin Haridas, Ritin Nair
"""

"""
This function uses the BFS search procedure to find a path from a specified starting point to a specified goal point.
Input: The maze to be searched and the specified starting and goal points
Output: The status of the search, a maze containing the path from the start to the goal and all visited nodes marked, and the number
        of explored nodes through the BFS search process
"""
def bfs(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]   
    fringe = [] # queue data structure

    fringe.append(start)
    prev = {start : None}

    if start == goal:
        return 'Start is goal', maze_copy, 1

    while len(fringe) != 0: # while the fringe is not empty
        current = fringe.pop(0) # remove the first element in the list to simulate a queue structure

        if current == goal: # current is goal
            parent = prev[current]
            while parent != start: # go through all the parents of nodes on the path to mark the path from the start to the goal
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]

            num_explored_nodes = explored_nodes(maze_copy) # find the number of nodes explored in the maze
            return 'Success!', maze_copy, num_explored_nodes
        
        curX, curY = current

        if maze_copy[curX][curY] == 5: # avoid unnecessarily exploring nodes that have already been visited
            continue
        
        # all neighbors of a cell are added to the fringe and have the current cell set as their parent
        if curX + 1 < dimension and maze[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5 and maze_copy[curX + 1][curY] != 7 and maze_copy[curX + 1][curY] != 8:
            fringe.append((curX + 1, curY))
            prev[(curX + 1, curY)] = current
        
        if curY + 1 < dimension and maze[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5 and maze_copy[curX][curY + 1] != 7 and maze_copy[curX][curY + 1] != 8:
            fringe.append((curX, curY + 1))
            prev[(curX, curY + 1)] = current

        if curX - 1 >= 0 and maze[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5 and maze_copy[curX - 1][curY] != 7 and maze_copy[curX - 1][curY] != 8 :
            fringe.append((curX - 1, curY))
            prev[(curX - 1, curY)] = current

        if curY - 1 >= 0 and maze[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5 and maze_copy[curX][curY - 1] != 7 and maze_copy[curX][curY - 1] != 8 :
            fringe.append((curX, curY - 1))
            prev[(curX, curY - 1)] = current

        if(current != start): # avoid overwriting the goal value
            maze_copy[curX][curY] = 5

    num_explored_nodes = explored_nodes(maze_copy) # calculate the number of nodes explored in the BFS search
    return 'No Solution', maze_copy, num_explored_nodes   

"""
This function counts the number of nodes that were explored in the maze by the BFS search algorithm.
Input: the maze to count the number of explored nodes for
Output: the number of explored nodes
"""

def explored_nodes(maze):
    # count number of explored nodes
    dimension = maze.shape[0]
    num_explored_nodes = 0
    for x in range(0, dimension):
        for y in range(0, dimension):
            if (x == 0 and y == 0) or (x == dimension - 1 and y == dimension - 1): #ignore start and goal
                continue
            if maze[x][y] == 5 or maze[x][y] == 6: # cells marked with these values have been explored
                num_explored_nodes += 1
    return num_explored_nodes    