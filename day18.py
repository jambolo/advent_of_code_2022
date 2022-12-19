# Advent of Code 2022
# Day 18

import re

FILE_NAME = 'day18-input.txt'

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

# Read the file.
lines = readFile(FILE_NAME)

# load the cubes
maxX = 0
maxY = 0
maxZ = 0

cubes = set()
for line in lines:
    match = re.search('(\d+),(\d+),(\d+)', line)
    x = int(match.group(1))
    y = int(match.group(2))
    z = int(match.group(3))

    if x > maxX: maxX = x
    if y > maxY: maxY = y
    if z > maxZ: maxZ = z
    cubes.add((x, y, z))

print(len(cubes), "cubes.")
print("Extents:", (0, 0, 0), (maxX, maxY, maxZ))

nSurfaces = 0
for x,y,z in cubes:
    candidates = [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    for c in candidates:
        if c not in cubes:
            nSurfaces += 1

print("Number of open surfaces = ", nSurfaces)

outside = set()
test = set()
for x in range(0, maxX + 1):
    for y in range(0, maxY + 1):
        if (x, y, 0) not in cubes:
            outside.add((x, y, 0))
            test.add((x, y, 1))
        if (x, y, maxZ) not in cubes:
            outside.add((x, y, maxZ))
            test.add((x, y, maxZ - 1))

for x in range(0, maxX + 1):
    for z in range(0, maxZ + 1):
        if (x, 0, z) not in cubes:
            outside.add((x, 0, z))
            test.add((x, 1, z))
        if (x, maxY, z) not in cubes:
            outside.add((x, maxY, z))
            test.add((x, maxY - 1, z))

for y in range(0, maxY + 1):
    for z in range(0, maxZ + 1):
        if (0, y, z) not in cubes:
            outside.add((0, y, z))
            test.add((1, y, z))
        if (maxX, y, z) not in cubes:
            outside.add((maxX, y, z))
            test.add((maxX - 1, y, z))

while len(test) > 0:
    t = test.pop()
    if t not in cubes and t not in outside:
        outside.add(t)
        test.add((t[0]-1, t[1], t[2]))
        test.add((t[0]+1, t[1], t[2]))
        test.add((t[0], t[1]-1, t[2]))
        test.add((t[0], t[1]+1, t[2]))
        test.add((t[0], t[1], t[2]-1))
        test.add((t[0], t[1], t[2]+1))

for x in range(0, maxX + 1):
    for y in range(0, maxY + 1):
        for z in range(0, maxZ + 1):
            if (x, y, z) not in outside:
                cubes.add((x, y, z))

print(len(cubes), "cubes.")

nSurfaces = 0
for x,y,z in cubes:
    candidates = [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    for c in candidates:
        if c not in cubes:
            nSurfaces += 1

print("Number of open surfaces = ", nSurfaces)
