# Advent of Code 2022
# Day 12

import re
import heapq

WIDTH = 162 # 8 # 162
HEIGHT = 41 # 5 # 41
START = 3240 # 0 # 3240
END = 3377 # 21 # 3377
IMPASSABLE = 2 * WIDTH * HEIGHT + 1

def height(c):
    heights = 'abcdefghijklmnopqrstuvwxyz'
    return heights.find(c)

def heuristic(s):
    global WIDTH
    global END
    sx = s % WIDTH
    sy = s // WIDTH
    ex = END % WIDTH
    ey = END // WIDTH
    return abs(ex - sx) + abs(ey - sy)

def neighborsOf(s):
    global WIDTH
    sx = s % WIDTH
    sy = s // WIDTH
    neighbors = []
    if sx - 1 >= 0:
        neighbors.append(s - 1)
    if sx + 1 < WIDTH:
        neighbors.append(s + 1)
    if sy - 1 >= 0:
        neighbors.append(s - WIDTH)
    if sy + 1 < HEIGHT:
        neighbors.append(s + WIDTH)
#    print('Neighbors of {s}:'.format(s=s), neighbors)

    return neighbors

def reconstructPath(maze, cameFrom, start, end):
    path = []
    while end != start:
        path.insert(0, end)
        end = cameFrom[end]
    path.insert(0, end)
    return path

def cost(maze, n, neighbor):
    if maze[neighbor] - maze[n] <= 1:
        d = 1
    else:
        d = IMPASSABLE
    return d


def aStar(maze, start, goal, h):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = []
    heapq.heappush(openSet, (h(start), start))

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = [0 for i in range(0, WIDTH*HEIGHT)]

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    # For second part, this is made global as an optimization
    gScore = [ IMPASSABLE for i in range(0, WIDTH * HEIGHT) ]
    gScore[start] = 0

    while len(openSet) > 0:
#        print("open:", openSet)
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current = openSet[0]    # openset is a priority queue
        n = current[1]
        if n == goal:
            return reconstructPath(maze, cameFrom, start, n)

        heapq.heappop(openSet) # Remove(current)

#        print("current:", n)
#        print("gscore:", gScore)
#        print("path:", reconstructPath(maze, cameFrom, start, n))
        neighbors = neighborsOf(n)
#        print("costs:", [cost(maze, n, neighbor) for neighbor in neighbors])
        for neighbor in neighbors:
            # d(current,neighbor) is the weight of the edge from current to neighbor
            d = cost(maze, n, neighbor)

            # tentative_gScore is the distance from start to the neighbor through current
            tentative_gScore = gScore[n] + d

            # If this path to neighbor is better than any previous one. Record it!
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = n
                gScore[neighbor] = tentative_gScore
                fScore = tentative_gScore + h(neighbor)
                if neighbor not in openSet:
                    heapq.heappush(openSet, (fScore, neighbor))

    # Open set is empty but goal was never reached
    return []

# Read the file

file = open('day12-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

maze = []

for line in lines:
    line = line.strip()
    maze.extend(line)

if maze[START] != 'S':
    raise Exception("Invalid START at {start}: {a} vs {e}.".format(start=START, a=maze[START], e='S'))
maze[START] = 'a'
if maze[END] != 'E':
    raise Exception("Invalid END at {end}: {a} vs {e}.".format(end=END, a=maze[END], e='E'))
maze[END] = 'z'
maze = [ height(c) for c in maze ]

#print("Maze:", maze)

bestScore = IMPASSABLE
bestStart = 0
for i in range(0,len(maze)):
    if maze[i] == 0:
        path = aStar(maze, i, END, heuristic)
        if path:
#            print("Path:", path)
#            print("Cost:", len(path)-1)
            if len(path) - 1 < bestScore:
                bestStart = i
                bestScore = len(path) - 1
print("Best start:", bestStart)
print("Best score:", bestScore)
#print(gScore)
