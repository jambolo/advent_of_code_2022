# Advent of Code 2022
# Day 15

import json
import re

FILE_NAME = 'day15-input.txt'
ROW = 2000000


def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def distance(x0, y0, x1, y1):
    return abs(x1 - x0) + abs(y1 - y0)

def drawBoard(sensors, minX, minY, maxX, maxY):
    for r in range(minY, maxY + 1):
        for c in range(minX, maxX + 1):
            a = '.'
            for s in sensors:
                if s["sensor"]["x"] == c and s["sensor"]["y"] == r:
                    a = 'S'
                    break
                elif s["beacon"]["x"] == c and s["beacon"]["y"] == r:
                    a = 'B'
                    break
            print(a, end='')
        print('')
    

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

#print(sensors)

# Determine the extents of the map

minX = sensors[0]["sensor"]["x"]
maxX = sensors[0]["sensor"]["x"]
minY = sensors[0]["sensor"]["y"]
maxY = sensors[0]["sensor"]["y"]
for s in sensors:
    sx = s["sensor"]["x"]
    sy = s["sensor"]["y"]
    bx = s["beacon"]["x"]
    by = s["beacon"]["y"]
    d = s["distance"]
    if minX > sx - d:
        minX = sx - d
    if maxX < sx + d:
        maxX = sx + d
    if minY > sy - d:
        minY = sy - d
    if maxY < sy + d:
        maxY = sy + d
    if minX > bx - d:
        minX = bx - d
    if maxX < bx + d:
        maxX = bx + d
    if minY > by - d:
        minY = by - d
    if maxY < by + d:
        maxY = by + d

#print("minX=", minX, "minY=", minY, "maxX=", maxX, "maxY=", maxY)
#drawBoard(sensors, minX, minY, maxX, maxY)

nImpossible = 0
for c in range(minX, maxX + 1):
    impossible = False
    for s in sensors:
        if distance(c, ROW, s["sensor"]["x"], s["sensor"]["y"]) <= s["distance"]:
            impossible = True
            break
    if impossible:
        for s in sensors:
            if ROW == s["beacon"]["y"] and c == s["beacon"]["x"]:
                impossible = False
                break
    if impossible:
        nImpossible += 1

print("Impossible points in row {r}:".format(r=ROW), nImpossible)
