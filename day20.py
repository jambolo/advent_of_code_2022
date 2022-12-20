# Advent of Code 2022
# Day 20

PART_1 = False
DEBUG = False
if DEBUG:
    FILE_NAME = 'day20-test.txt'
else:
    FILE_NAME = 'day20-input.txt'

if PART_1:
    NUMBER_OF_CYCLES = 1
else:
    KEY = 811589153
    NUMBER_OF_CYCLES = 10

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def move(data, src, count):
    element = data.pop(src)
    dst = src + count
    data.insert(dst % len(data), element)

# Read the file.
lines = readFile(FILE_NAME)

original = []
for line in lines:
    original.append(int(line))
size = len(original)

if DEBUG:
    print("Original:", original, "size=", size)

if not PART_1:
    original = [o * KEY for o in original]
    if DEBUG:
        print("Keyed:", original)

decrypted = []
for i in range(0, size):
    decrypted.append({ "value" : original[i], "position" : i })

for c in range(0, NUMBER_OF_CYCLES):
    for i in range(0, size):
        for k in range(0, size):
            if decrypted[k]["position"] == i:
                v = decrypted[k]["value"] 
                if v != 0:   # if 0, don't move
                    move(decrypted, k, v)
                    if DEBUG:
                        print("Move:", v, ":", [d["value"] for d in decrypted])
                break

result = [d["value"] for d in decrypted]

at = result.index(0)
x = result[(at + 1000) % size]
y = result[(at + 2000) % size]
z = result[(at + 3000) % size]

if DEBUG:
    print("Result:  ", result)

print("Coordinates: 0 at [", at, "],", x, "at [", (at + 1000) % size, "],", y, "at [", (at + 2000) % size, "],", z, "at [", (at + 3000) % size, "]")
sum = x + y + z
print("sum =", sum)
