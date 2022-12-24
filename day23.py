# Advent of Code 2022
# Day 23

import copy
import re

PART_2 = True
TEST = False

if PART_2:
    NUMBER_OF_ROUNDS = 2000000000
else:
    NUMBER_OF_ROUNDS = 10

if TEST:
    FILE_NAME = 'day23-test.txt'
else:
    FILE_NAME = 'day23-input.txt'

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def replaceAtIndex(s, i, c):
    return s[:i] + c + s[i+len(c):]

def computeExtents(elves):
    minX = elves[0][0]
    maxX = elves[0][0]
    minY = elves[0][1]
    maxY = elves[0][1]
    for e in elves:
        if e[0] < minX:
            minX = e[0]
        if e[0] > maxX:
            maxX = e[0]
        if e[1] < minY:
            minY = e[1]
        if e[1] > maxY:
            maxY = e[1]
    return (minX, maxX, minY, maxY)

def printMap(elves):
    (minX, maxX, minY, maxY) = computeExtents(elves)
    width = maxX - minX + 1
    height = maxY - minY + 1
    map = []
    for y in range(0, height):
        map.append('.'*width)
    for e in elves:
        map[e[1]-minY] = replaceAtIndex(map[e[1]-minY], e[0]-minX, '#')
    for row in map:
        print(row)

def alone(e, elves):
    return (
            [e[0]-1, e[1]-1] not in elves and [e[0], e[1]-1] not in elves and [e[0]+1, e[1]-1] not in elves
        and [e[0]-1, e[1]  ] not in elves                                 and [e[0]+1, e[1]  ] not in elves
        and [e[0]-1, e[1]+1] not in elves and [e[0], e[1]+1] not in elves and [e[0]+1, e[1]+1] not in elves
    )

def canMove(e, elves, template, i):
    t = template[i]
    return (
            [e[0]+t[0][0], e[1]+t[0][1]] not in elves
        and [e[0]+t[1][0], e[1]+t[1][1]] not in elves
        and [e[0]+t[2][0], e[1]+t[2][1]] not in elves
    )

def proposedMovement(e, template, i):
    t = template[i]
    return [e[0]+t[3][0], e[1]+t[3][1]]


# Read the file.
lines = readFile(FILE_NAME)

elves = []
for y in range(0, len(lines)):
    for x in range(0, len(lines[y])):
        if lines[y][x] == '#':
            elves.append([x, y])
if TEST:
    print("elves=", elves)
    print('Starting positions:')
    printMap(elves)

proposalTemplate = [
    [[-1, -1], [ 0, -1], [+1, -1], [ 0, -1]],
    [[-1, +1], [ 0, +1], [+1, +1], [ 0, +1]],
    [[-1, -1], [-1,  0], [-1, +1], [-1,  0]],
    [[+1, -1], [+1,  0], [+1, +1], [+1,  0]]
]

first = 0

for round in range(0, NUMBER_OF_ROUNDS):
    proposed = []
    # Propose movement
    for e in elves:
        if alone(e, elves):
            proposed.append([])
        elif canMove(e, elves, proposalTemplate, (first + 0) % 4):
            proposed.append(proposedMovement(e, proposalTemplate, (first + 0) % 4))
        elif canMove(e, elves, proposalTemplate, (first + 1) % 4):
            proposed.append(proposedMovement(e, proposalTemplate, (first + 1) % 4))
        elif canMove(e, elves, proposalTemplate, (first + 2) % 4):
            proposed.append(proposedMovement(e, proposalTemplate, (first + 2) % 4))
        elif canMove(e, elves, proposalTemplate, (first + 3) % 4):
            proposed.append(proposedMovement(e, proposalTemplate, (first + 3) % 4))
        else:
            proposed.append([])

    # Resolve
    stationaryCount = 0
    for i in range(0, len(elves)):
        p = proposed[i]
        if p:
            count = 0
            for j in range(0, len(elves)):
                if j != i and proposed[j] == p:
                    count += 1
            if count == 0:
                elves[i] = p
        else:
            stationaryCount += 1
    if PART_2:
        if stationaryCount == len(elves):
            print("Nobody moved in round", round+1)
            break

    if TEST:
        print("Round", round + 1)
        printMap(elves)
    elif PART_2 and round % 10 == 9:
        print("Round:", round + 1, ", Stationary count:", stationaryCount)

    first += 1

if not PART_2:
    (minX, maxX, minY, maxY) = computeExtents(elves)

    emptySpaces = (maxX - minX + 1) * (maxY - minY + 1) - len(elves)
    print("empty spaces =", emptySpaces)
