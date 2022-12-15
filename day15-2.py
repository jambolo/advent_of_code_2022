# Advent of Code 2022
# Day 15

import json
import re

FILE_NAME = 'day15-input.txt'


def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def distance(x0, y0, x1, y1):
    return abs(x1 - x0) + abs(y1 - y0)

# Read the file.
lines = readFile(FILE_NAME)

# Load the sensors and beacons

sensors = []

for line in lines:
    match = re.search('Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
    sx = int(match.group(1))
    sy = int(match.group(2))
    bx = int(match.group(3))
    by = int(match.group(4))

    sensors.append({
        "sensor" : {
            "x" : sx,
            "y" : sy
        },
        "beacon" : {
            "x" : bx,
            "y" : by
        },
        "distance" : distance(sx, sy, bx, by)
    })

minX = 0
maxX = 4000000
minY = 0
maxY = 4000000

#print("minX=", minX, "minY=", minY, "maxX=", maxX, "maxY=", maxY)

#exclude all points within beacon range
groups = [[[minX, maxX]]]*(maxY - minY + 1)

for s in sensors:
    sx = s["sensor"]["x"]
    sy = s["sensor"]["y"]
    d = s["distance"]
    for r in range(max(minY, sy - d), min(maxY+1, sy + d + 1)):
        group = groups[r]
        if group:
            new_group = []
            offset = d - abs(r - sy)
            for g in group:
                if g[1] < sx - offset or sx + offset < g[0]:
                    new_group.append(g)
                elif sx - offset <= g[0] and g[1] <= sx + offset:
                    pass # remove it
                elif g[0] < sx - offset and sx + offset < g[1]:
                    new_group.extend([[g[0], sx - offset - 1], [sx + offset + 1, g[1]]])
                elif g[0] < sx - offset and g[1] <= sx + offset:
                    new_group.append([g[0], sx - offset - 1])
                elif sx - offset <= g[0] and sx + offset < g[1]:
                    new_group.append([sx + offset + 1, g[1]])
            groups[r] = new_group

# non-excluded groups
for i in range(0, len(groups)):
    if groups[i]:
        print("frequency =", i + groups[i][0][0] * 4000000)

