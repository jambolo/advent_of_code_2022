# Advent of Code 2022
# Day 5, part 1

import re

def drawPiles(piles):
    # First find the biggest pile
    max = 0
    for pile in piles:
        if len(pile) > max:
            max = len(pile)
    
    for i in range(max-1, -1, -1):
        for pile in piles:
            if i < len(pile):
                print('[{crate}] '.format(crate=pile[i]), end='')
            else:
                print('    ', end='')
        print('')

# Read the file

file = open('day5-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

# Parse the crates
# The firat 8 lines contain the crates. There are 9 piles.
# The contents of the crates start at column 1 and are every 4 characters apart

piles = [[], [], [], [], [], [], [], [], []]

for i in range(0, 8):
    line = lines[i].strip()
    for p in range(0, 9):
        if p * 4 + 1 >= len(line):
            break
        crate = line[p * 4 + 1]
        if crate != ' ':
            piles[p].insert(0, crate)

# Draw the piles
drawPiles(piles)

# Process the move commands: move {count} from {from} to {to}
# Move commands start at line 10

moveRe = 'move (\d+) from (\d+) to (\d+)'
i = 10
while i < len(lines):
    line = lines[i].strip()
    match = re.search(moveRe, line)
    count = int(match.group(1))
    fromPile = int(match.group(2)) - 1
    toPile = int(match.group(3)) - 1
#    print('move {count} from {fromPile} to {toPile}'.format(count=count, fromPile=fromPile+1, toPile=toPile+1))

    # Move the crates
    for j in range(0, count):
        crate = piles[fromPile].pop()
        piles[toPile].append(crate)

    i = i + 1

# Draw the result
drawPiles(piles)

# List the tops of the piles as specified
for pile in piles:
    print('{crate}'.format(crate=pile[-1]), end='')
print('')
