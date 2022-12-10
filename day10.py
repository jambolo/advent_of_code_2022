# Advent of Code 2022
# Day 10

import re

def drawPixel(oldX):
    global column
    global row
    if oldX-1 <= column and column <= oldX + 1:
        row += '#'
    else:
        row += '.'
    column += 1
    # Draw the row
    if len(row) == 40:
        print(row)
        row = ''
        column = 0


# Read the file

file = open('day10-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

cycle = 1
x = 1
epoch = 0
sum = 0
row = ''
column = 0

for line in lines:
    line = line.strip()

    oldX = x

    # Execute
    opcode = line[:4]
    if opcode == 'noop':
        drawPixel(oldX)
#        print('{c}: {x} noop'. format(c=cycle, x=x))
        cycle += 1
    elif opcode == 'addx':
        drawPixel(oldX)
        drawPixel(oldX)
#        print('{c}: {x} addx'. format(c=cycle, x=x))
        operand = int(line[5:])
        x += operand
#        print('{c}: {x} addx {v}'. format(c=cycle+1, x=x, v=operand))
        cycle += 2
    else:
        raise Exception('Unknown opcode: '+opcode)

    # Detect new epoch

    if (cycle+19) // 40 > epoch:
        epoch += 1
        strength = oldX * (epoch*40-20)
        sum += strength
#        print('Cycle {c}: strength={strength}, sum={sum}'.format(c=epoch*40-20, strength=strength, sum=sum))

print('Signal strength sum is {s}'.format(s=sum))
    
    