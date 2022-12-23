# Advent of Code 2022
# Day 22

import copy
import re

PART_1 = False
TEST = False

if TEST:
    FILE_NAME = 'day22-test.txt'
else:
    FILE_NAME = 'day22-input.txt'

NUMBER_OF_DIRECTIONS = 4
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
INITIAL_DIRECTION = RIGHT

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def replaceAtIndex(s, i, c):
    return s[:i] + c + s[i+len(c):]

def parseRoute(line):
    i = 0
    route = []
    while i < len(line):
        match = re.search('(\d+)|(R|L)', line[i:])
        token = match.group()
        if token == 'R' or token == 'L':
            route.append(token)
        else:
            route.append(int(token))
        i += match.span()[1]
    return route

def findRowExtents(map):
    extents = []
    for row in map["tiles"]:
        extents.append((len(row) - len(row.lstrip()), len(row)))
    return extents

def findColumnExtents(map):
    extents = []
    for c in range(0, map["width"]):
        start = 0
        end = map["height"]
        for r in range(0, map["height"]):
            if c < len(map["tiles"][r]) and map["tiles"][r][c] != ' ':
                start = r
                break
        for r in range(start+1, map["height"]):
            if c >= len(map["tiles"][r]) or map["tiles"][r][c] == ' ':
                end = r
                break
        extents.append((start, end))
    return extents

def findBlocks(map):
    blocks = []
    for r in range(0, map["height"]):
        row = map["tiles"][r]
        rowBlocks = []
        for c in range(map["rowExtents"][r][0], map["rowExtents"][r][1]):
            if row[c] == '#':
                rowBlocks.append(c)
        blocks.append(rowBlocks)

def printMap(map):
    for row in map["tiles"]:
        for c in row:
            print(c, end=' ')
        print('')

def printAnnotatedMap(map, myR, myC, direction):
    tiles = copy.deepcopy(map["tiles"])
    rowExtents = map["rowExtents"]
    columnExtents = map["columnExtents"]
    for r in range(0, map["height"]):
        row = tiles[r]
        if row[rowExtents[r][0]] != '#':
            row = replaceAtIndex(row, rowExtents[r][0], '|')
        if row[rowExtents[r][1]-1] != '#':
            row = replaceAtIndex(row, rowExtents[r][1]-1, '|')
        for c in range(rowExtents[r][0], rowExtents[r][1]):
            if (r == columnExtents[c][0] or r == columnExtents[c][1]-1) and row[c] != '#':
                row = replaceAtIndex(row, c, '-')
        tiles[r] = row
        if r == map["start"][0]:
            tiles[r] = replaceAtIndex(tiles[r], map["start"][1], 'A')
        if r == myR:
            tiles[r] = replaceAtIndex(tiles[r], myC, '>v<^'[direction])
        
    annotated = { "tiles" : tiles, "width" : map["width"], "height" : map["height"] }
    printMap(annotated)

def wrapRight(r, c):
    if TEST:
        match r // 4:
            case 0: # 1 -> 6
                return (3 - ((r -  0) - 4) +  8, 3 - ((c -  8)    ) + 12, LEFT)
            case 1: # 4 -> 6
                return (    ((c -  8) - 4) +  8, 3 - ((r -  4)    ) + 12, DOWN)
            case 2: # 6 -> 1
                return (3 - ((r -  8)    ) +  0, 3 - ((c - 12) - 4) +  8, LEFT)
            case _:
                raise Exception("invalid wrap row")
    else:
        match r // 50:
            case 0: # 0 -> 3
                return (49 - ((r -   0)     ) + 100, 49 - ((c - 100) - 50) +  50, LEFT)
            case 1: # 2 -> 0
                return (49 - ((c -  50) - 50) +   0,      ((r -  50)     ) + 100, UP)
            case 2: # 3 -> 0
                return (49 - ((r - 100)     ) +   0, 49 - ((c -  50) - 50) + 100, LEFT)
            case 3: # 5 -> 3
                return (49 - ((c -   0) - 50) + 100,      ((r - 150)     ) +  50, UP)
            case _:
                raise Exception("invalid wrap row")

def wrapDown(r, c):
    if TEST:
        match c // 4:
            case 0: # 2 -> 5
                return (3 - ((r -  4) - 4) +  8, 3 - ((c -  0)    ) +  8, UP)
            case 1: # 3 -> 5
                return (3 - ((c -  4)    ) +  8,     ((r -  4) - 4) +  8, RIGHT)
            case 2: # 5 -> 2
                return (3 - ((r -  8) - 4) +  4, 3 - ((c -  8)    ) +  0, UP)
            case 3: # 6 -> 2
                return (3 - ((c - 12)    ) +  4,     ((r -  8) - 4) +  0, RIGHT)
            case _:
                raise Exception("invalid wrap row")
    else:
        match c // 50:
            case 0: # 5 -> 0
                return (     ((r - 150) - 50) +   0,      ((c -   0)     ) + 100, DOWN)
            case 1: # 3 -> 5
                return (     ((c -  50)     ) + 150, 49 - ((r - 100) - 50) +   0, LEFT)
            case 2: # 0 -> 2
                return (     ((c - 100)     ) +  50, 49 - ((r -   0) - 50) +  50, LEFT)
            case _:
                raise Exception("invalid wrap row")

def wrapLeft(r, c):
    if TEST:
        match r // 50:
            case 0: # 1 -> 3
                return (3 - ((c -  8) + 4) +  4,     ((r -  0)    ) +  4, DOWN)
            case 1: # 2 -> 6
                return (    ((c -  0) + 4) +  8, 3 - ((r -  4)    ) + 12, UP)
            case 2: # 5 -> 3
                return (    ((c -  8) + 4) +  4, 3 - ((r -  8)    ) +  4, UP)
            case _:
                raise Exception("invalid wrap row")
    else:
        match r // 50:
            case 0: # 1 -> 4
                return (49 - ((r -   0)     ) + 100, 49 - ((c -  50) + 50) +   0, RIGHT)
            case 1: # 2 -> 4
                return (49 - ((c -  50) + 50) + 100,      ((r -  50)     ) +   0, DOWN)
            case 2: # 4 -> 1
                return (49 - ((r - 100)     ) +   0, 49 - ((c -   0) + 50) +  50, RIGHT)
            case 3: # 5 -> 1
                return (49 - ((c -   0) + 50) +   0,      ((r - 150)     ) +  50, DOWN)
            case _:
                raise Exception("invalid wrap row")

def wrapUp(r, c):
    if TEST:
        match c // 4:
            case 0: # 2 -> 1
                return (3 - ((r -  4) + 4) +  0, 3 - ((c -  0)    ) +  8, DOWN)
            case 1: # 3 -> 1
                return (    ((c -  4)    ) +  0, 3 - ((r -  4) + 4) +  8, RIGHT)
            case 2: # 1 -> 2
                return (3 - ((r -  0) + 4) +  4, 3 - ((c -  8)    ) +  0, DOWN)
            case 3: # 6 -> 4
                return (3 - ((c - 12)    ) +  4,     ((r -  8) + 4) +  8, LEFT)
            case _:
                raise Exception("invalid wrap row")
    else:
        match c // 50:
            case 0: # 4 -> 2
                return (     ((c -   0)     ) +  50, 49 - ((r - 100) + 50) +  50, RIGHT)
            case 1: # 1 -> 5
                return (     ((c -  50)     ) + 150, 49 - ((r -   0) + 50) +   0, RIGHT)
            case 2: # 0 -> 5
                return (     ((r -   0) + 50) + 150,      ((c - 100)     ) +   0, UP)
            case _:
                raise Exception("invalid wrap row")

def turnRight(direction):
    return (direction + 1) % NUMBER_OF_DIRECTIONS

def turnLeft(direction):
    return (direction - 1) % NUMBER_OF_DIRECTIONS

def moveRight(map, r, c):
    d = RIGHT
    r1 = r
    c1 = c + 1
    d1 = d
    if c1 >= map["rowExtents"][r1][1]:
        if PART_1:
            c1 = map["rowExtents"][r1][0]
        else:
            (r1, c1, d1) = wrapRight(r1, c1)
    if map["tiles"][r1][c1] != '#':
        return (r1, c1, d1)
    else:
        return (r, c, d)

def moveDown(map, r, c):
    d = DOWN
    r1 = r + 1
    c1 = c
    d1 = d
    if r1 >= map["columnExtents"][c1][1]:
        if PART_1:
            r1 = map["columnExtents"][c1][0]
        else:
            (r1, c1, d1) = wrapDown(r1, c1)
    if map["tiles"][r1][c1] != '#':
        return (r1, c1, d1)
    else:
        return (r, c, d)

def moveLeft(map, r, c):
    d = LEFT
    r1 = r
    c1 = c - 1
    d1 = d
    if c1 < map["rowExtents"][r1][0]:
        if PART_1:
            c1 = map["rowExtents"][r1][1] - 1
        else:
            (r1, c1, d1) = wrapLeft(r1, c1)
    if map["tiles"][r1][c1] != '#':
        return (r1, c1, d1)
    else:
        return (r, c, d)

def moveUp(map, r, c):
    d = UP
    r1 = r - 1
    c1 = c
    d1 = d
    if r1 < map["columnExtents"][c1][0]:
        if PART_1:
            r1 = map["columnExtents"][c1][1] - 1
        else:
            (r1, c1, d1) = wrapUp(r1, c1)
    if map["tiles"][r1][c1] != '#':
        return (r1, c1, d1)
    else:
        return (r, c, d)

# Read the file.
lines = readFile(FILE_NAME)

map = {}
tiles = []
i = 0
width = 0
while lines[i].rstrip():
    line = lines[i].rstrip()
    tiles.append(line)
    if len(line) > width:
        width = len(line)
    i += 1
height = len(tiles)

map = { "tiles" : tiles, "width" : width, "height" : height }

i += 1 # skip the blank line

route = parseRoute(lines[i].rstrip())

if TEST:
    printMap(map)
    print(route)

start = len(map["tiles"][0]) - len(map["tiles"][0].lstrip())
if TEST:
    print("start = ", start)

map["start"] = (0, start)

# Analysis

map["rowExtents"] = findRowExtents(map)
map["columnExtents"] = findColumnExtents(map)
blocks = findBlocks(map)

if TEST:
    printAnnotatedMap(map, -1, -1, -1)

r = 0
c = start
direction = INITIAL_DIRECTION
for step in route:
    if type(step) is int:
        for i in range(0, step):
            match direction:
                case 0: # right
                    (r, c, direction) = moveRight(map, r, c)
                case 1: # down
                    (r, c, direction) = moveDown(map, r, c)
                case 2: # left
                    (r, c, direction) = moveLeft(map, r, c)
                case 3: # up
                    (r, c, direction) = moveUp(map, r, c)
                case _:
                    raise Exception("invalid direction")
    elif type(step) is str:
        if step == 'R':
            direction = turnRight(direction)
        elif step == 'L':
            direction = turnLeft(direction)
        else:
            raise Exception("invalid turn")
    if TEST:
        print("step =", step)
        printAnnotatedMap(map, r, c, direction)

password = 1000 * (r + 1) + 4 * (c + 1) + direction
print ("password =", password)
