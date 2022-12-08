# Advent of Code 2022
# Day 5, part 2

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
    for i in range(0, len(piles)):
        print(' {i}  '.format(i=i+1), end='')
    print('')

# Read the file

file = open('day05-input.txt', mode = 'r', encoding = 'utf-8-sig')
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
#drawPiles(piles)

# Process the move commands: move {count} from {from} to {to}
# Move commands start at line 10

moveRe = 'move (\d+) from (\d+) to (\d+)'
i = 10
while i < len(lines):
    line = lines[i].strip()
    match = re.search(moveRe, line)
    count = int(match.group(1))
    iFrom = int(match.group(2)) - 1
    iTo = int(match.group(3)) - 1
#    print('move {count} from {iFrom} to {iTo}'.format(count=count, iFrom=iFrom+1, iTo=iTo+1))

    # Move the crates
    piles[iTo].extend(piles[iFrom][-count:])
    piles[iFrom] = piles[iFrom][:-count]

    i = i + 1

# Draw the result
#drawPiles(piles)

# List the tops of the piles as specified
for pile in piles:
    print('{crate}'.format(crate=pile[-1]), end='')
print('')
