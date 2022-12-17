# Advent of Code 2022
# Day 16, part 2

import re
import heapq

FILE_NAME = 'day16-input.txt'
TIME_LIMIT = 26
IMPASSABLE = -1

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines


def reconstructPath(cameFrom, start, end):
    path = []
    while end != start:
        path.insert(0, end)
        end = cameFrom[end]
    path.insert(0, end)
    return path

def aStar(start, goal, nodes):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    openSet = []
    heapq.heappush(openSet, (0, start))

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start
    # to n currently known.
    cameFrom = ['']*len(nodes)

    # For node n, gScore[n] is the cost of the cheapest path from start to n currently known.
    gScore = {}
    for n in nodes:
        gScore[n] = len(nodes)
    gScore[start] = 0

    while len(openSet) > 0:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current = openSet[0]    # openset is a priority queue
        n = current[1]
        if n == goal:
            return gScore[n]

        heapq.heappop(openSet) # Remove(current)

        neighbors = nodes[n]["next"]
        for neighbor in neighbors:
            # If this path to neighbor is better than any previous one. Record it!
            if gScore[n] + 1 < gScore[neighbor]:
                gScore[neighbor] = gScore[n] + 1
                if neighbor not in openSet:
                    heapq.heappush(openSet, (gScore[neighbor], neighbor))

    # Open set is empty but goal was never reached
    return IMPASSABLE

# Finds the highest flow from the given node within the time limit
def findBestFlow(nodes, times, mPath, ePath, mTime, eTime):
    bestFlow = 0
    bestMPath = []
    bestEPath = []
    if mTime < eTime:
        here = mPath[-1]
        for m in nodes:
            if nodes[m]["flow"] > 0 and m not in mPath and m not in ePath:
                newMTime = mTime + times[(here, m)] + 1
                if newMTime < TIME_LIMIT:
                    flow = nodes[m]["flow"] * (TIME_LIMIT - newMTime)
                    mPath.append(m)
                    (xFlow, xMPath, xEPath) = findBestFlow(nodes, times, mPath, ePath, newMTime, eTime)
                    mPath.pop()
                    if (flow + xFlow > bestFlow):
                        bestFlow = flow + xFlow
                        bestMPath = [{ "node": m, "time": newMTime, "flow": flow, "xFlow": xFlow }]
                        bestMPath.extend(xMPath)
                        bestEPath = xEPath
    else:
        here = ePath[-1]
        for e in nodes:
            if nodes[e]["flow"] > 0 and e not in mPath and e not in ePath:
                newETime = eTime + times[(here, e)] + 1
                if newETime < TIME_LIMIT:
                    flow = nodes[e]["flow"] * (TIME_LIMIT - newETime)
                    ePath.append(e)
                    (xFlow, xMPath, xEPath) = findBestFlow(nodes, times, mPath, ePath, mTime, newETime)
                    ePath.pop()
                    if (flow + xFlow > bestFlow):
                        bestFlow = flow + xFlow
                        bestEPath = [{ "node": e, "time": newETime, "flow": flow, "xFlow": xFlow }]
                        bestEPath.extend(xMPath)
                        bestMPath = xMPath

    return (bestFlow, bestMPath, bestEPath)

# Read the file.
lines = readFile(FILE_NAME)

nodes = {}

# Process the lines"next"
for line in lines:
    line = line.strip()
    match = re.search('Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (([A-Z]{2},? ?)+)', line)
    nodes[match.group(1)] = { "flow" : int(match.group(2)), "next" : re.split(', ', match.group(3)) }

# Determine the cost between nodes
times = {}
for n0 in nodes:
    if nodes[n0]["flow"] > 0 or n0 == "AA":
        for n1 in nodes:
            if nodes[n1]["flow"] > 0:
                if n0 == n1:
                    times[(n0,n1)] = 0
                else:
                    d = aStar(n0, n1, nodes)
                    if d == IMPASSABLE:
                        raise Exception("Impassable from", n0, "to", n1)
                    times[(n0,n1)] = d

# Go through all possible 26 minute paths from AA
mPath = ['AA']
ePath = ['AA']
mTime = 0
eTime = 0
(bestFlow, bestMPath, bestEPath) = findBestFlow(nodes, times, mPath, ePath, mTime, eTime)

print("Path:", bestMPath)
print("Path:", bestEPath)
print("Maximum flow = ", bestFlow)