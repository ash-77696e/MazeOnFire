import numpy as np

def dfs(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]

    fringe = [start] # stack data structure
    closed_set = []
    prev = {start : None}

    while len(fringe) != 0:
        current = fringe.pop()
        if current == goal:            
            parent = prev[current]
            while parent != start:
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            return 'Success', maze_copy

        curX, curY = current

        if curX + 1 < dimension and maze[curX + 1][curY] != 1 and (curX + 1, curY) not in closed_set:
            if (curX + 1, curY) not in fringe:
                fringe.append((curX + 1, curY))
                prev[(curX + 1, curY)] = current
        
        if curY + 1 < dimension and maze[curX][curY + 1] != 1 and (curX, curY + 1) not in closed_set:
            if (curX, curY + 1) not in fringe:
                fringe.append((curX, curY + 1))
                prev[(curX, curY + 1)] = current

        if curX - 1 >= 0 and maze[curX - 1][curY] != 1 and (curX - 1, curY) not in closed_set:
            if (curX - 1, curY) not in fringe:
                fringe.append((curX - 1, curY))
                prev[(curX - 1, curY)] = current

        if curY - 1 >= 0 and maze[curX][curY - 1] != 1 and (curX, curY - 1) not in closed_set:
            if (curX, curY - 1) not in fringe:
                fringe.append((curX, curY - 1))
                prev[(curX, curY - 1)] = current

        closed_set.append(current)

        if current != start:
            maze_copy[curX][curY] = 5

    return 'Failure', maze_copy