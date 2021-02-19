import numpy as np

"""
This file provides the implementation for the DFS search algorithm to find a valid path from a specified 
starting node to a specified goal node in the maze.

Authors: Ashwin Haridas, Ritin Nair
"""

"""
This function provides the implementation for the DFS search procedure through a given maze from a specified starting point to
a specified goal.
Input: The maze to run the search algorithm on, the starting point, and the goal point
Output: Staus of the the search and a maze that contains the path from the specified start 
        to the specified goal and has all explored nodes marked
"""
def dfs(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    fringe = [start] # stack data structure
    prev = {start : None}

    while len(fringe) != 0: # while the fringe is not empty
        current = fringe.pop()
        if current == goal: # current cell is the goal     
            parent = prev[current] # set path from goal to start as optimal
            while parent != start: # trace back from goal to start to find the cells on the path
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            return 'Success', maze_copy

        curX, curY = current

        if maze_copy[curX][curY] == 5: # avoid exploring cells that have already been visited
            continue
        
        # all valid neighbors of the current cell are added to the fringe and have the current cell set as their parent
        if curY - 1 >= 0 and maze_copy[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5: # attempt to move down
            fringe.append((curX, curY - 1))
            prev[(curX, curY - 1)] = current

        if curX - 1 >= 0 and maze_copy[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5: # attempt to move left
            fringe.append((curX - 1, curY))
            prev[(curX - 1, curY)] = current

        if curY + 1 < dimension and maze_copy[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5: # attempt to move up
            fringe.append((curX, curY + 1))
            prev[(curX, curY + 1)] = current

        if curX + 1 < dimension and maze_copy[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5: # attempt to move right
            fringe.append((curX + 1, curY))
            prev[(curX + 1, curY)] = current

        if current != start: # to avoid overwriting the goal value
            maze_copy[curX][curY] = 5 # mark current as visited

    return 'Failure', maze_copy