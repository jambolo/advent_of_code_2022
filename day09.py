# Advent of Code 2022
# Day 9

import re

NUMBER_OF_KNOTS = 10

def drawBoard(knots, minx, miny, maxx, maxy):
    knotNames = "H123456789"
    for y in range(maxy, miny-1, -1):
        for x in range(minx, maxx):
            found = False
            i = 0
            for k in knots:
                if x == k[0] and y == k[1]:
                    print(knotNames[i], end='')
                    found = True
                    break
                i += 1
            if not found:
                print('.', end='')
        print('')
    print('')

def follow(head, tail):
    dx = 0
    dy = 0
    if head[0] > tail[0] + 1:
        dx = 1
        if head[1] > tail[1]:
            dy = 1
        elif head[1] < tail[1]:
            dy = -1
    elif head[0] < tail[0] - 1:
        dx = -1
        if head[1] > tail[1]:
            dy = 1
        elif head[1] < tail[1]:
            dy = -1
    elif head[1] > tail[1] + 1:
        dy = 1
        if head[0] > tail[0]:
            dx = 1
        elif head[0] < tail[0]:
            dx = -1
    elif head[1] < tail[1] - 1:
        dy = -1
        if head[0] > tail[0]:
            dx = 1
        elif head[0] < tail[0]:
            dx = -1
    return (tail[0] + dx, tail[1] + dy)

# Read the file

file = open('day09-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

knots = []
for i in range(0, NUMBER_OF_KNOTS):
    knots.append((0, 0))

visited = { knots[NUMBER_OF_KNOTS-1] }

for line in lines:
    line = line.strip()

    match = re.search('(\w)\s+(\d+)', line)
    direction = match.group(1)
    distance = int(match.group(2))
    minx = 0
    miny = 0
    maxx = 5
    maxy = 4
    for i in range(0, distance):
        # Move the head
        if direction == 'U':
            knots[0] = (knots[0][0], knots[0][1] + 1)
        elif direction == 'D':
            knots[0] = (knots[0][0], knots[0][1] - 1)
        elif direction == 'R':
            knots[0] = (knots[0][0] + 1, knots[0][1])
        elif direction == 'L':
            knots[0] = (knots[0][0] - 1, knots[0][1])

        # Move the rest of the knots
        for i in range(1, NUMBER_OF_KNOTS):
            knots[i] = follow(knots[i-1], knots[i])

        visited.add(knots[NUMBER_OF_KNOTS-1])

#        drawBoard(knots, minx, miny, maxx, maxy)
print(knots)
print('Tail visited {n} different locations.'.format(n=len(visited)))
