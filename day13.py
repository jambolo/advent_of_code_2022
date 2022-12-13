# Advent of Code 2022
# Day 13

import json
import functools

FILE_NAME = 'day13-input.txt'

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def determineOrder(left, right):
    i = 0
    while i < len(left) and i < len(right):
        if type(left[i]) is int and type(right[i]) is int:
            order = left[i] - right[i]
            if order != 0:
                return order
        elif type(left[i]) is int and type(right[i]) is list:
            listified = [left[i]]
            order = determineOrder(listified, right[i])
            if order != 0:
                return order
        elif type(left[i]) is list and type(right[i]) is int:
            listified = [right[i]]
            order = determineOrder(left[i], listified)
            if order != 0:
                return order
        elif type(left[i]) is list and type(right[i]) is list:
            order = determineOrder(left[i], right[i])
            if order != 0:
                return order
        else:
            raise Exception("Invalid data type")
        i += 1

    return len(left) - len(right)

# Read the file
lines = readFile(FILE_NAME)

iLine = 0
iPair = 1
correctPairs = []

while iLine < len(lines):

    # Load a pair
    left = json.loads(lines[iLine])
    iLine += 1
    if iLine >= len(lines):
        break;

    right = json.loads(lines[iLine])
    iLine += 1
    iLine += 1 # skip blank line

#    print(left, "vs", right)

    # If it is in the correct order, save the index
    order = determineOrder(left, right)
    if order < 0:
        correctPairs.append(iPair)
#        print('Pair {i}: in order'.format(i=iPair))
#    elif order > 0:
#        print('Pair {i}: out of order'.format(i=iPair))
#    else:
#        print('Pair {i}: same'.format(i=iPair))
        
    iPair += 1

sum = 0
for p in correctPairs:
    sum += p

print('Sum of correct indexes =', sum)

all = [json.loads(line) for line in lines if len(line.strip()) > 0]
all.append([[2]])
all.append([[6]])
s = sorted(all, key=functools.cmp_to_key(determineOrder))

first = s.index([[2]]) + 1
last = s.index([[6]]) + 1

print('part 2 result is ', first * last)
