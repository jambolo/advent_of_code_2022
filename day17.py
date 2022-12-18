# Advent of Code 2022
# Day 17

FILE_NAME = 'day17-input.txt'
BOARD_WIDTH = 7

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def collision(board, restingHeight, rock, r, c):
    if r < 0:
        return True
        
    for y in range(min(rock["height"], restingHeight-r)):
        for x in range(rock["width"]):
            if board[r + y][c + x] == 1 and rock["shape"][y][x] == 1:
                return True
    return False
        
def drawRockOnBoard(board, rock, r, c):
    if rock["height"] + r > len(board):
        raise Exception("bad rock placement")
    for y in range(rock["height"]):
        for x in range(rock["width"]):
            if rock["shape"][y][x] == 1:
                board[r + y][c + x] = 1

def drawBoard(board):
    for y in range(len(board) - 1, -1, -1):
        row = ""
        for x in range(BOARD_WIDTH):
            if board[y][x] == 1:
                row += '#'
            else:
                row += '.'
        print('+' + row + '+')
    print("+-------+")


rocks = [
    {
        "width" : 4,
        "height" : 1,
        "shape" : [[1, 1, 1, 1]]
    },
    {
        "width" : 3,
        "height" : 3,
        "shape" : [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    },
    {
        "width" : 3,
        "height" : 3,
        "shape" : [[1, 1, 1], [0, 0, 1], [0, 0, 1] ]
    },
    {
        "width" : 1,
        "height" : 4,
        "shape" : [[1], [1], [1], [1]]
    },
    {
        "width" : 2,
        "height" : 2,
        "shape" : [[1, 1], [1, 1]]
    }
]

# Read the file.
lines = readFile(FILE_NAME)

jets = lines[0].strip()

board = []
lowest = [0]*BOARD_WIDTH
jetsIndex = 0
skipped = 0
signatures = []
heights = []
cycleLength = 0
round = 0
while round < 1000000000000:
    restingHeight = len(board)
    rock = rocks[round % len(rocks)]
    r = restingHeight + 3
    c = 2

    if cycleLength == 0:
        if restingHeight > 8:
            signature = {
                "r": round % len(rocks),
                "j": jetsIndex % len(jets),
                "b": [
                    board[restingHeight-1],
                    board[restingHeight-2], 
                    board[restingHeight-3], 
                    board[restingHeight-4], 
                    board[restingHeight-5], 
                    board[restingHeight-6], 
                    board[restingHeight-7], 
                    board[restingHeight-8]
                ]
            }
            try:
                j = signatures.index(signature)
            except ValueError:
                signatures.append(signature)
                heights.append(restingHeight)
            else:
                # We have a cycle
                cycleLength = round - j
                print("Cycle from", j, "to", round, ", length:", cycleLength)
                cycles = (1000000000000 - round) // cycleLength
                skippedIterations = cycles * cycleLength
                skippedRows = (restingHeight - heights[j]) * cycles
                round += skippedIterations
                print("Skipped: cycles=", cycles, ", iterations=", skippedIterations, ", rows=", skippedRows);
        else:
            signatures.append([])
            heights.append(restingHeight)


    stopped = False
    while not stopped:
        # Apply the jet
        jet = jets[jetsIndex % len(jets)]
        jetsIndex += 1 
        if jet == '<':
            if c > 0:
                newC = c - 1
                if not collision(board, restingHeight, rock, r, newC):
                    c = newC
        elif jet == '>':
            if c + rock["width"] < BOARD_WIDTH:
                newC = c + 1
                if not collision(board, restingHeight, rock, r, newC):
                    c = newC
        else:
            raise Exception("Invalid jet: {j}".format(j=jet))

        # Fall one space
        newR = r - 1
        if not collision(board, restingHeight, rock, newR, c):
            r = newR
        else:
            stopped = True
            for i in range((r + rock["height"] - restingHeight)):
                board.append([0, 0, 0, 0, 0, 0, 0])
            drawRockOnBoard(board, rock, r, c)
    round = round + 1
#    drawBoard(board)

print("highest = ", len(board) + skippedRows)