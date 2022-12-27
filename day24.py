# Advent of Code 2022
# Day 24

import heapq
import itertools

uniqueId = itertools.count()

PART_1 = False
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
t0 = 0


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
        c = (b["start"][1] + (t + t0) * b["d"]) % width
        map[r] = replaceAt(map[r], c, '#')
    for b in verticalBlizzards:
        r = (b["start"][0] + (t + t0) * b["d"]) % height
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
        if 0 < i <= height * width and eR == r:
            row = replaceAt(row, eC, 'E')
        print('|' + row + '|')
    row = '+' + '#' * (width - 1) + ".+"
    if i > width * height:
        row = replaceAt(row, width - 2, 'E')
    print(row)


def nodeIndex(r, c):
    return r * width + c + 1


def createGraph(map):
    graph = []

    # Add start node
    node = [startIndex]     # Not moving is an option, but it still costs 1
    if map[0][0] != '#':
        node.append(nodeIndex(0, 0))   # Include the only node adjacent to the start node if it is open
    graph.append(node)

    # Add map nodes
    for r in range(0, height):
        for c in range(0, width):
            node = []
            for r1, c1 in ((r, c), (r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
                if 0 <= r1 < height and 0 <= c1 < width and map[r1][c1] != '#':
                    node.append(nodeIndex(r1, c1))
            graph.append(node)

    # Add goal node
    node = [goalIndex]     # Append the goal node last, index is width*height + 1
    if map[height - 1][width - 1] != '#':
        node.append(nodeIndex(height - 1, width - 1))   # Include the only node adjacent to the goal node if it is open
    graph.append(node)     # Append the goal node last, index is width*height + 1

    # Always able to reach start and goal nodes
    graph[nodeIndex(0, 0)].append(startIndex)
    graph[nodeIndex(height - 1, width - 1)].append(goalIndex)

    return graph


def h(i):
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
        assert len(maps) == j
        maps.append(createMap(j))
        graph = createGraph(maps[j])
        assert len(graphs) == j
        graphs.append(graph)
    return graphs[t][i]


def dynamicAStar(start, goal, h, neighborsOf):
    openSet = []
    predecessors = {}
    gScore = set()

    # Initially, only the start node is known.
    heapq.heappush(openSet, (h(start), 0, start))
    gScore.add((0, start))

    while len(openSet) > 0:
        # Get the next node. < 0 indicates a replaced entry
        _, t0, n = openSet[0]
        heapq.heappop(openSet)  # Remove the current node

        # If the goal is reached, then return the path by iteratively looking up the goal's predecessors
        if n == goal:
            path = []
            end = goal
            t = t0
            while t != 0:
                path.insert(0, end)
                t, end = predecessors[(t, end)]
            path.insert(0, start)
            return path

        t1 = t0 + 1
        neighbors = neighborsOf(t1, n)
        for neighbor in neighbors:
            if (t1, neighbor) not in gScore:
                predecessors[(t1, neighbor)] = (t0, n)        # Any path to the neighbor should go through n
                gScore.add((t1, neighbor))
                fScore = t1 + h(neighbor)
                heapq.heappush(openSet, (fScore, t1, neighbor))

    # The open set is empty but goal was never reached. That means that there is no path from start to goal.
    return []


# Read the file.
lines = []
lines = readFile(FILE_NAME)

# Load the blizzards

width = len(lines[0].rstrip()) - 2
height = len(lines) - 2
startIndex = 0
goalIndex = width * height + 1

for r in range(0, height):
    line = lines[r + 1].rstrip()[1:-1]
    for c in range(0, width):
        x = line[c]
        if x == '<':
            blizzard = {"start": (r, c), "d": -1}
            horizontalBlizzards.append(blizzard)
        elif x == '>':
            blizzard = {"start": (r, c), "d": 1}
            horizontalBlizzards.append(blizzard)
        elif x == '^':
            blizzard = {"start": (r, c), "d": -1}
            verticalBlizzards.append(blizzard)
        elif x == 'v':
            blizzard = {"start": (r, c), "d": 1}
            verticalBlizzards.append(blizzard)
        elif x == '.':
            pass
        else:
            raise Exception("invalid map character")

maps.append(createMap(0))
graphs.append(createGraph(maps[0]))

path = dynamicAStar(startIndex, goalIndex, h, neighborsOf)
print("length of shortest path is", len(path) - 1)

if not PART_1:
    first = len(path) - 1
    t0 = first
    maps = [createMap(0)]
    graphs = [createGraph(maps[0])]
    path = dynamicAStar(goalIndex, startIndex, h, neighborsOf)
    second = len(path) - 1
    print("second:", second)
    t0 = first + second
    maps = [createMap(0)]
    graphs = [createGraph(maps[0])]
    path = dynamicAStar(startIndex, goalIndex, h, neighborsOf)
    third = len(path) - 1
    print("third:", third)
    print("Total time: ", first + second + third)
