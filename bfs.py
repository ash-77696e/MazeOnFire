import queue
import numpy as np

def bfs(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]   
    fringe = []

    fringe.append(start)
    prev = {start : None}

    while len(fringe) != 0:
        current = fringe.pop(0)

        if current == goal:
            parent = prev[current]
            while parent != start:
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            return 'Success!', maze_copy
        
        curX, curY = current

        if maze_copy[curX][curY] == 5:
            continue

        if curX + 1 < dimension and maze[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5 and maze_copy[curX + 1][curY] != 7:
            fringe.append((curX + 1, curY))
            prev[(curX + 1, curY)] = current
        
        if curY + 1 < dimension and maze[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5 and maze_copy[curX][curY + 1] != 7:
            fringe.append((curX, curY + 1))
            prev[(curX, curY + 1)] = current

        if curX - 1 >= 0 and maze[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5 and maze_copy[curX - 1][curY] != 7:
            fringe.append((curX - 1, curY))
            prev[(curX - 1, curY)] = current

        if curY - 1 >= 0 and maze[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5 and maze_copy[curX][curY - 1] != 7:
            fringe.append((curX, curY - 1))
            prev[(curX, curY - 1)] = current

        if(current != start):
            maze_copy[curX][curY] = 5
        
    return 'No Solution', maze_copy    