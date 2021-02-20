import heapq
import numpy as np

"""
This file contains two implementations of A*: the general path-finding A* with Euclidean distance metric
and the modified A* we designed for Strategy 3 for the maze on fire.

Authors: Ashwin Haridas, Ritin Nair
"""

"""
This function is the implementation of our A* algorithm. It uses a MinHeap as the priority queue and the euclidean distance metric as the heuristic
Input: maze, start, goal
Output: status, solved maze, number of explored nodes
"""
def astar(maze, start, goal):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]
    fringe = [] # create priority queue data structure (min heap)

    heapq.heappush(fringe, (0 + euclidean_distance(start, goal), (start, 0))) # push start
    
    prev = {start : None}

    while len(fringe) != 0:
        popped = heapq.heappop(fringe) # get item with lowest distance
        priority, item = popped
        current, distance = item

        if current == goal:
            parent = prev[current]
            while parent != start: # backtrack to start and mark nodes for path
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]
            
            num_explored_nodes = explored_nodes(maze_copy)
            return 'Success', maze_copy, num_explored_nodes
        
        curX, curY = current

        if maze_copy[curX][curY] == 5: # ignore already visited node
            continue
        
        # find valid neighbors and add to queue with the priority being the euclidean distance to the goal + distance so far

        if curY - 1 >= 0 and maze_copy[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX, curY - 1), goal) + distance + 1, ((curX, curY - 1), 1 + distance)))
            prev[(curX, curY - 1)] = current

        if curX - 1 >= 0 and maze_copy[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX - 1, curY), goal) + distance + 1, ((curX - 1, curY), 1 + distance)))
            prev[(curX - 1, curY)] = current
        
        if curY + 1 < dimension and maze_copy[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX, curY + 1), goal) + distance + 1, ((curX, curY + 1), 1 + distance)))
            prev[(curX, curY + 1)] = current

        if curX + 1 < dimension and maze_copy[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5:
            heapq.heappush(fringe, (euclidean_distance((curX + 1, curY), goal) + distance + 1, ((curX + 1, curY), 1 + distance)))
            prev[(curX + 1, curY)] = current
        
        if current != start:
            maze_copy[curX][curY] = 5 # mark visited
    
    num_explored_nodes = explored_nodes(maze_copy)
    return 'Failure', maze_copy, num_explored_nodes

"""
This function is the implementation of the modified A* algorithm we use for strategy 3. It uses a MinHeap as the priority queue
and uses the probability that a cell is on fire along with the distance traveled as the heuristic

Input: maze, start, goal, probability maze
Output: status, solved_maze
"""
def astar_fire(maze, start, goal, prob_maze):
    maze_copy = np.copy(maze)
    dimension = maze_copy.shape[0]
    fringe = [] # create priorty queue data structure

    startX, startY = start

    heapq.heappush(fringe, (0 + prob_maze[startX][startY], (start, 0)) ) # push start

    prev = {start : None}

    while len(fringe) != 0:
        priority, item = heapq.heappop(fringe) # pop item
        current, distance = item

        if current == goal:
            parent = prev[current]
            while parent != start:
                parentX, parentY = parent
                maze_copy[parentX][parentY] = 6
                parent = prev[parent]

            return 'Success!', maze_copy
        
        curX, curY = current

        if maze_copy[curX][curY] == 5: # ignore visited cells
            continue
        
        # Here we first initialize a probabiliy weight factor which weights the distance less if the probability that a cell is on fire is small
        # If the probability that a cell will be on fire is high, we want to weight it more, so the factor is higher
        # We do this because we want to prioritize distance for those cells with low probability, and prioritize probability for those
        # cells with high probability

        prob_weight_factor = 0  
        if curY - 1 >= 0 and maze_copy[curX][curY - 1] != 1 and maze_copy[curX][curY - 1] != 5 and maze_copy[curX][curY - 1] != 7:
            if prob_maze[curX][curY - 1] >= 0 and prob_maze[curX][curY - 1] < 0.3:
                prob_weight_factor = (distance / 2)
            elif prob_maze[curX][curY - 1] >= 0.3 and prob_maze[curX][curY - 1] < 0.6:
                prob_weight_factor = distance
            else:
                prob_weight_factor = 2 * distance
            heapq.heappush(fringe, ( distance + 1 + prob_weight_factor * prob_maze[curX][curY - 1], ((curX, curY - 1) , distance + 1)))
            prev[(curX, curY - 1)] = current

        if curX - 1 >= 0 and maze_copy[curX - 1][curY] != 1 and maze_copy[curX - 1][curY] != 5 and maze_copy[curX - 1][curY] != 7:
            if prob_maze[curX - 1][curY] >= 0 and prob_maze[curX - 1][curY] < 0.3:
                prob_weight_factor = (distance / 2)
            elif prob_maze[curX - 1][curY] >= 0.3 and prob_maze[curX - 1][curY] < 0.6:
                prob_weight_factor = distance
            else:
                prob_weight_factor = 2 * distance
            heapq.heappush(fringe, ( distance + 1 + prob_weight_factor * prob_maze[curX - 1][curY], ((curX - 1, curY), distance + 1)))
            prev[(curX - 1, curY)] = current
        
        if curY + 1 < dimension and maze_copy[curX][curY + 1] != 1 and maze_copy[curX][curY + 1] != 5 and maze_copy[curX][curY + 1] != 7:
            if prob_maze[curX][curY + 1] >= 0 and prob_maze[curX][curY + 1] < 0.3:
                prob_weight_factor = (distance / 5)
            elif prob_maze[curX][curY + 1] >= 0.3 and prob_maze[curX][curY + 1] < 0.6:
                prob_weight_factor = distance
            else:
                prob_weight_factor = 2 * distance
            heapq.heappush(fringe, ( distance + 1 + prob_weight_factor * prob_maze[curX][curY + 1], ((curX, curY + 1), distance + 1)))
            prev[(curX, curY + 1)] = current

        if curX + 1 < dimension and maze_copy[curX + 1][curY] != 1 and maze_copy[curX + 1][curY] != 5 and maze_copy[curX + 1][curY] != 7:
            if prob_maze[curX + 1][curY] >= 0 and prob_maze[curX + 1][curY] < 0.3:
                prob_weight_factor = (distance / 5)
            elif prob_maze[curX + 1][curY] >= 0.3 and prob_maze[curX + 1][curY] < 0.6:
                prob_weight_factor = distance
            else:
                prob_weight_factor = 2 * distance
            heapq.heappush(fringe, ( distance + 1 + prob_weight_factor * prob_maze[curX + 1][curY], ((curX + 1, curY), distance + 1)))
            prev[(curX + 1, curY)] = current        

        if current != start: # mark cell as visited
            maze_copy[curX][curY] = 5
    
    return 'No Solution', maze_copy

"""
This function calculates the euclidean distance between two points

Input: point 1, point 2
Output: euclidean distance between those points
"""
def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    return np.sqrt(np.power(x2 - x1, 2) + np.power(y2 - y1, 2))

"""
This function calculates the number of nodes explored by A*

Input: maze
Output: explored nodes
"""
def explored_nodes(maze):
    # count number of explored nodes
    dimension = maze.shape[0]
    num_explored_nodes = 0
    for x in range(0, dimension):
        for y in range(0, dimension):
            if (x == 0 and y == 0) or (x == dimension - 1 and y == dimension - 1): #ignore start and goal
                continue
            if maze[x][y] == 5 or maze[x][y] == 6: # if the cell is marked as the optimal path or was seen during A*, increase number of explored by 1
                num_explored_nodes += 1
    return num_explored_nodes    