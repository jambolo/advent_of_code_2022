# Advent of Code 2022
# Day 24

import heapq
import itertools

uniqueId = itertools.count()

PART_1 = True
TEST = False

if TEST:
    FILE_NAME = 'day24-test.txt'
else:
    FILE_NAME = 'day24-input.txt'

horizontalBlizzards = []
verticalBlizzards = []
maps = []
graphs = []
width = 0
height = 0
startIndex = 0
goalIndex = 0


def readFile(name):
    file = open(name, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines


def replaceAt(s, i, c):
    '''
    Replaces a portion of a string starting at the given index with another string

    Returns the new string

    s   - string to be replaced
    i   - index to start the replacement
    c   - replacement string
    '''
    if i >= 0:
        out = s[:i] + c + s[i + len(c):]
    else:
        return s[:i] + c + s[len(s) + i + len(c):]
    return out


def createMap(t):
    map = ['.' * width for r in range(0, height)]
    for b in horizontalBlizzards:
        r = b["start"][0]
        c = (b["start"][1] + t * b["d"]) % width
        map[r] = replaceAt(map[r], c, '#')
    for b in verticalBlizzards:
        r = (b["start"][0] + t * b["d"]) % height
        c = b["start"][1]
        map[r] = replaceAt(map[r], c, '#')
    return map


def printMap(map, i=-1):
    row = '+.' + '-' * (width - 1) + '+'
    if i == 0:
        row = replaceAt(row, 1, 'E')
    print(row)
    eR = (i - 1) // width
    eC = (i - 1) % width
    for r in range(0, height):
        row = map[r]
        if i > 0 and i <= height * width and eR == r:
            row = replaceAt(row, eC, 'E')
        print('|' + row + '|')
    row = '+' + '#' * (width - 1) + ".+"
    if i > width * height:
        row = replaceAt(row, width - 2, 'E')
    print(row)


def nodeIndex(r, c):
    return r * width + c + 1


def createGraph(map, t):
    graph = []
    node = [(startIndex, 1)]     # Not moving is an option, but it still costs 1
    if map[0][0] != '#':
        node.append((nodeIndex(0, 0), 1))   # Include the only node adjacent to the start node if it is open
    graph.append(node)     # Append the start node first
    for r in range(0, height):
        for c in range(0, width):
            node = []
            if map[r][c] != '#':
                node.append((nodeIndex(r, c), 1))    # Not moving is an option, but is still costs 1
            if r - 1 >= 0 and map[r - 1][c] != '#':
                node.append((nodeIndex(r - 1, c), 1))
            if c - 1 >= 0 and map[r][c - 1] != '#':
                node.append((nodeIndex(r, c - 1), 1))
            if c + 1 < width and map[r][c + 1] != '#':
                node.append((nodeIndex(r, c + 1), 1))
            if r + 1 < height and map[r + 1][c] != '#':
                node.append((nodeIndex(r + 1, c), 1))
            if (r + 1, c) == (height, width - 1):            # Don't forget the edge to the goal node
                node.append((goalIndex, 1))
            graph.append(node)
    graph.append([])     # Append the goal node last, index is width*height

    return graph


def h(t, i):
    if i == startIndex:             # start node
        cost = width + height
    elif i == goalIndex:            # goal node
        cost = 0
    else:
        r = i // width
        c = i % width
        cost = (width - 1 - c) + (height - 1 - r) + 1
    return cost


def neighborsOf(t, i):
    for j in range(len(graphs), t + 1):
        maps.append(createMap(j))
        graph = createGraph(maps[j], j)
        graphs.append(graph)
        if TEST:
            printMap(maps[j])
            print(graphs[j])

    return graphs[t][i]


def dynamicAStar(start, goal, h, neighborsOf):
    openSet = []
    predecessors = {}
    gScore = {}

    # Initially, only the start node is known.
    heapq.heappush(openSet, [h(0, start), 0, next(uniqueId), start])
    gScore[(0, start)] = 0

    while len(openSet) > 0:
        # Get the next node. < 0 indicates a replaced entry
        _, t0, _, n = openSet[0]
        heapq.heappop(openSet)  # Remove the current node
        while n < 0:
            _, t0, _, n = openSet[0]
            heapq.heappop(openSet)  # Remove the current node

        # If the goal is reached, then return the path by iteratively looking up the goal's predecessors
        if n == goal:
            path = []
            end = goal
            t = t0
            while end != start:
                path.insert(0, end)
                t, end = predecessors[(t, end)]
            path.insert(0, start)
            return path

        t1 = t0 + 1
        neighbors = neighborsOf(t1, n)
        for neighbor, d in neighbors:
            # distance from start to the neighbor through the current node
            tentative_gScore = gScore[(t0, n)] + d
            # If this path to neighbor is better than any previous one, then save it (replacing any other instances
            # already in the queue).
            if (t1, neighbor) not in gScore or tentative_gScore < gScore[(t1, neighbor)]:
                predecessors[(t1, neighbor)] = (t0, n)        # Any path to the neighbor should go through n
                gScore[(t1, neighbor)] = tentative_gScore
                fScore = tentative_gScore + h(t1, neighbor)
                # Invalidate any instances of the neighbor already in the queue
                for i in openSet:
                    if i[1] == t1 and i[3] == neighbor:
                        i[3] = -1
                # Add the new node to the open set
                heapq.heappush(openSet, [fScore, t1, next(uniqueId), neighbor])

    # The open set is empty but goal was never reached. That means that there is no path from start to goal.
    return []


# Read the file.
lines = readFile(FILE_NAME)

# Load the blizzards

width = len(lines[0].rstrip()) - 2
height = len(lines) - 2
startIndex = 0
goalIndex = width * height + 1

for r in range(0, height):
    line = lines[r + 1].rstrip()
    for c in range(0, width):
        x = line[c + 1]
        if x == '<':
            blizzard = {"start": (r, c), "d": width - 1}
            horizontalBlizzards.append(blizzard)
        elif x == '>':
            blizzard = {"start": (r, c), "d": 1}
            horizontalBlizzards.append(blizzard)
        elif x == '^':
            blizzard = {"start": (r, c), "d": height - 1}
            verticalBlizzards.append(blizzard)
        elif x == 'v':
            blizzard = {"start": (r, c), "d": 1}
            verticalBlizzards.append(blizzard)
        elif x == '.':
            pass
        else:
            raise Exception("invalid map character")

maps.append(createMap(0))
graphs.append(createGraph(maps[0], 0))
if TEST:
    printMap(maps[0])
    print(graphs[0])

path = dynamicAStar(startIndex, goalIndex, h, neighborsOf)
if TEST:
    for i in range(0, len(path) - 1):
        printMap(maps[i], path[i])

print("length of shortest path is", len(path) - 1)
