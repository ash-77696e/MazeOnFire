import heapq
import numpy as np


def astar(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]
    fringe = []

    heapq.heappush(fringe, (0 + euclidean_distance(start, goal), (start, 0)))
    
    prev = {start : None}

    while len(fringe) != 0:
        popped = heapq.heappop(fringe)
        priority, item = popped
        current, distance = item

        if current == goal:
            parent = prev[current]
            while parent != start:
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            return 'Success', maze_copy
        
        curX, curY = current

        if maze_copy[curX][curY] == 5:
            continue

        if curX + 1 < dimension and maze_copy[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX + 1, curY), goal) + distance + 1, ((curX + 1, curY), 1 + distance)))
            prev[(curX + 1, curY)] = current

        if curY + 1 < dimension and maze_copy[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX, curY + 1), goal) + distance + 1, ((curX, curY + 1), 1 + distance)))
            prev[(curX, curY + 1)] = current

        if curX - 1 >= 0 and maze_copy[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX - 1, curY), goal) + distance + 1, ((curX - 1, curY), 1 + distance)))
            prev[(curX - 1, curY)] = current
        
        if curY - 1 >= 0 and maze_copy[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX, curY - 1), goal) + distance + 1, ((curX, curY - 1), 1 + distance)))
            prev[(curX, curY - 1)] = current
        
        if current != start:
            maze_copy[curX][curY] = 5
    
    return 'Failure', maze_copy


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))