# Advent of Code 2022
# Day 6

MARKER_SIZE = 14

def printMarker(buffer, i):
    s = '|'
    if i > 0:
        s += ''.join(buffer[i:])
        s += ''.join(buffer[:i])
    else:
        s += ''.join(buffer)
    s += '|'
    print(s)

#test = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'

file = open('day6-input.txt', 'r')

buffer = []
for i in range(0, MARKER_SIZE):
    buffer.append(' ')

i = 0
nUnique = 0
found = False
while not found:
    c = file.read(1)
#    c = test[i]
    if not c:
        break

    buffer[i%MARKER_SIZE] = c
    nUnique = nUnique + 1
    printMarker(buffer, (i+1) % MARKER_SIZE)

    for j in range(1, nUnique):
        if c == buffer[(i - j + MARKER_SIZE) % MARKER_SIZE]:
            nUnique = j
            break
    if nUnique >= MARKER_SIZE:
        found = True
    
    i = i + 1

file.close()

if found:
    print('buffer was found at position {i}'.format(i=i))
else:
    print('buffer was not found')
