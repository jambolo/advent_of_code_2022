# Advent of Code 2022
# Day 4

import re

# regex for parsing lines
regex = '(\d+)-(\d+),(\d+)-(\d+)'

# Read the file

file = open('day4-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

containCount = 0
intersectCount = 0

for line in lines:
    line = line.strip()

    match = re.search(regex, line)
    low1 = int(match.group(1))
    high1 = int(match.group(2))
    low2 = int(match.group(3))
    high2 = int(match.group(4))
#    print('{low1}-{high1},{low2}-{high2}'.format(low1=low1, high1=high1, low2=low2, high2=high2))

    if low1 <= high2 and low2 <= high1:
        intersectCount = intersectCount + 1

    if (low1 <= low2 and high1 >= high2) or (low2 <= low1 and high2 >= high1):
        containCount += 1

print('Number of contained ranges is {count}'.format(count=containCount))
print('Number of intersecting ranges is {count}'.format(count=intersectCount))
