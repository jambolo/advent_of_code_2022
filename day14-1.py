# Advent of Code 2022
# Day 14, part 1

import json

FILE_NAME = 'day14-input.txt'

EMPTY = 0
ROCK = 1
SAND = 2

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def placeRocks(board, v0, v1, x0, y0):
    if v0[0] == v1[0]:
        # vertical
        x = v0[0] - x0
        for y in range(min(v0[1], v1[1]) - y0, max(v0[1], v1[1]) - y0 + 1):
            board[y][x] = ROCK
    else:
        # horizontal
        y = v0[1] - y0
        for x in range(min(v0[0], v1[0]) - x0, max(v0[0], v1[0]) - x0 + 1):
            board[y][x] = ROCK

def drawBoard(board):
    for row in board:
        for cell in row:
            if cell == EMPTY:
                print('.', end='')
            elif cell == ROCK:
                print('#', end='')
            elif cell == SAND:
                print('o', end='')
            else:
                raise Exception('Bad cell value')
        print('')


# Read the file
lines = readFile(FILE_NAME)

# Parse the input after converting it to json for easy parsing
multisegments = []
for line in lines:
    line = '[[' + line.strip() + ']]'
    line = line.replace('->', '],[')
    line = json.loads(line)
    multisegments.append(line)

# Find the limits of the board
min_x = multisegments[0][0][0]
min_y = 0
max_x = multisegments[0][0][0]
max_y = multisegments[0][0][1]
for m in multisegments:
    for vertex in m:
        if vertex[0] < min_x:
            min_x = vertex[0]
        if vertex[0] > max_x:
            max_x = vertex[0]
        if vertex[1] < min_y:
            min_y = vertex[1]
        if vertex[1] > max_y:
            max_y = vertex[1]

width = max_x - min_x + 1
height = max_y - min_y + 1

# Create the board
board = [[EMPTY]*width for i in range(0, height)]

for m in multisegments:
    v0 = m[0]
    for i in range(1, len(m)):
        v1 = m[i]
        placeRocks(board, v0, v1, min_x, min_y)
        v0 = v1

#drawBoard(board)

# Drop the sand

done = False
nSand = 0
while not done:
    x = 500 - min_x
    y = 0 - min_y

    blocked = False
    while x >= 0 and x < width and y < height and not blocked:
        # Falling straight down
        if y + 1 >= height or board[y + 1][x] == EMPTY:
            y += 1
            continue

        # Falling to the left
        if x - 1 < 0 or board[y+1][x-1] == EMPTY:
            y += 1
            x -= 1
            continue

        # Falling to the right
        if x + 1 >= width or board[y+1][x+1] == EMPTY:
            y += 1
            x += 1
            continue
        
        blocked = True
    
    if blocked:
        board[y][x] = SAND
        nSand += 1
    elif x < 0 or x >= width or y >= height:
        done = True

#drawBoard(board)

print('Number of grains of sand is', nSand)
