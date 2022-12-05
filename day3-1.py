# Advent of Code 2022
# Day 3, part 1

priorities = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Read the file

file = open('day3-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

sum = 0

for line in lines:
    line = line.strip()
    count = int(len(line) / 2)
    if len(line) != count * 2:
        raise Exception("Invalid line length: {line}".format(line=line))
    compartment1 = sorted(line[:count])
    compartment2 = sorted(line[count:])

    i1 = 0
    i2 = 0
    found = ''
    while not found and i1 < count and i2 < count:
        while not found and compartment1[i1] <= compartment2[i2]:
            if compartment1[i1] == compartment2[i2]:
                found = compartment1[i1]
            else:
                i1 = i1 + 1
        i2 = i2 + 1
    if not found:
        raise Exception("Unable to find common letter in {line}".format(line=line))
    
    priority = priorities.index(found) + 1

    print('line={line}, compartment1={c1}, c2={c2}, common={found}, priority={priority}'.format(line=line, c1=''.join(compartment1), c2=''.join(compartment2), found=found, priority=priority))
    sum = sum + priority

print('Sum of priorities: {sum}'.format(sum=sum))
