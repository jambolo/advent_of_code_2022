# Advent of Code 2022
# Day 25

PART_1 = True
TEST = False

if TEST:
    FILE_NAME = 'day25-test.txt'
else:
    FILE_NAME = 'day25-input.txt'


def readFile(name):
    file = open(name, mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines


def to_int(s):
    n = 0
    for c in s:
        n = n * 5 + ("=-012".index(c) - 2)
    return n


def to_snafu(n):
    s = ''
    if n == 0:
        s = '0'
    while n != 0:
        n += 2
        s = "=-012"[n % 5] + s
        n = n // 5
    return s


# Read the file.
lines = []
lines = readFile(FILE_NAME)

numbers = [to_int(line.rstrip()) for line in lines]

sum = 0
for n in numbers:
    sum += n

print("sum:", sum)
print("enter: ", to_snafu(sum))
