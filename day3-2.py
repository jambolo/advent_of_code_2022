# Advent of Code 2022
# Day 3, part 2

priorities = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Read the file

file = open('day3-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

sum = 0
i = 0
while i < len(lines):
    line1 = sorted(lines[i].strip())
    line2 = sorted(lines[i+1].strip())
    line3 = sorted(lines[i+2].strip())

    count1 = len(line1)
    count2 = len(line2)
    count3 = len(line3)

    i1 = 0
    i2 = 0
    i3 = 0
    found = ''
    while not found and i1 < count1 and i2 < count2 and i3 < count3:
        while (line1[i1] < line2[i2] or line1[i1] < line3[i3]) and i1 < count1:
            i1 += 1
        while (line2[i2] < line1[i1] or line2[i2] < line3[i3]) and i2 < count2:
            i2 += 1
        while (line3[i3] < line1[i1] or line3[i3] < line2[i2]) and i3 < count3:
            i3 += 1
        if line1[i1] == line2[i2] and line2[i2] == line3[i3]:
            found = line1[i1]

    if not found:
        raise Exception("Unable to find common letter")
    
    priority = priorities.index(found) + 1

    print('line1={line1}, line2={line2}, line3={line3}, common={found}, priority={priority}'.format(line1=''.join(line1), line2=''.join(line2), line3=''.join(line3),found=found, priority=priority))
    sum = sum + priority

    i += 3

print('Sum of priorities: {sum}'.format(sum=sum))
