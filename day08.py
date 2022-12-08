# Advent of Code 2022
# Day 8

import re

SIZE = 99

# Read the file

file = open('day08-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

grid = []
for line in lines:
    line = line.strip()
    row = []
    for c in line:
        row.append(int(c))
    if len(row) != SIZE:
        raise Exception("Row is the wrong size. It is {actual}, but it should be {expected}.".format(actual=len(row), expected=SIZE))
    grid.append(row)
if len(grid) != SIZE:
    raise Exception("Wrong number of rows. It is {actual}, but it should be {expected}.".format(actual=len(grid), expected=SIZE))

count = 4 * (SIZE - 1) # count exterior cells
maxScore = 0

# Look at each interior cell

for i in range(1, SIZE-1):
    for j in range(1, SIZE-1):
        seen = False
        height = grid[i][j]

        # Check visibility from above
        if not seen:
            seen = True
            for k in range(0, i):
                if grid[k][j] >= height:
                    seen = False
                    break

        # Check visibility from below
        if not seen:
            seen = True
            for k in range(i+1, SIZE):
                if grid[k][j] >= height:
                    seen = False
                    break

        # Check visibility from left
        if not seen:
            seen = True
            for k in range(0, j):
                if grid[i][k] >= height:
                    seen = False
                    break

        # Check visibility from right
        if not seen:
            seen = True
            for k in range(j+1, SIZE):
                if grid[i][k] >= height:
                    seen = False
                    break

        # Count it if it can be seen
        if seen:
            count += 1

        # Check viewing score above
        viewAbove = 0
        for k in range(i-1, -1, -1):
            viewAbove += 1
            if grid[k][j] >= height:
                break

        # Check viewing score below
        viewBelow = 0
        for k in range(i+1, SIZE):
            viewBelow += 1
            if grid[k][j] >= height:
                break

        # Check viewing score left
        viewLeft = 0
        for k in range(j-1, -1, -1):
            viewLeft += 1
            if grid[i][k] >= height:
                break

        # Check viewing score right
        viewRight = 0
        for k in range(j+1, SIZE):
            viewRight += 1
            if grid[i][k] >= height:
                break

        score = viewAbove * viewBelow * viewLeft * viewRight
        if score > maxScore:
            maxScore = score
#        print('{above}{below}{left}{right} '.format(above=viewAbove, below=viewBelow, left=viewLeft, right=viewRight), end='')
#    print('')
print ('{count} trees can be seen.'.format(count=count))
print('{score} is the maximum score.'.format(score=maxScore))
