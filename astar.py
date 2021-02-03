import heapq
import numpy as np

def astar(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]
    fringe = []

    heapq.heappush(fringe, (0 + euclidean_distance(start, goal), (start, 0)))
    
    closed_set = []
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

        if curX + 1 < dimension and maze[curX + 1][curY] != 1 and (curX + 1, curY) not in closed_set:
            if (curX + 1, curY) not in fringe:
                heapq.heappush(fringe, (euclidean_distance((curX + 1, curY), goal), ((curX + 1, curY), 1 + distance)))
                prev[(curX + 1, curY)] = current

        if curY + 1 < dimension and maze[curX][curY + 1] != 1 and (curX, curY + 1) not in closed_set:
            if (curX, curY + 1) not in fringe:
                heapq.heappush(fringe, (euclidean_distance((curX, curY + 1), goal), ((curX, curY + 1), 1 + distance)))
                prev[(curX, curY + 1)] = current

        if curX - 1 >= 0 and maze[curX - 1][curY] != 1 and (curX - 1, curY) not in closed_set:
            if (curX - 1, curY) not in fringe:
                heapq.heappush(fringe, (euclidean_distance((curX - 1, curY), goal), ((curX - 1, curY), 1 + distance)))
                prev[(curX - 1, curY)] = current
        
        if curY - 1 >= 0 and maze[curX][curY - 1] != 1 and (curX, curY - 1) not in closed_set:
            if (curX, curY - 1) not in fringe:
                heapq.heappush(fringe, (euclidean_distance((curX, curY - 1), goal), ((curX, curY - 1), 1 + distance)))
                prev[(curX, curY - 1)] = current
        
        closed_set.append(current)

        if current != start:
            maze_copy[curX][curY] = 5
    
    return 'Failure', maze_copy

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))