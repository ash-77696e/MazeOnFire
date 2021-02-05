import numpy as np

def dfs(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    fringe = [start] # stack data structure
    prev = {start : None}

    while len(fringe) != 0:
        current = fringe.pop()
        if current == goal:            
            parent = prev[current] # set path from goal to start as optimal
            while parent != start:
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            return 'Success', maze_copy

        curX, curY = current

        if maze_copy[curX][curY] == 5:
            continue

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

        if current != start:
            maze_copy[curX][curY] = 5 # mark current as visited

    return 'Failure', maze_copy