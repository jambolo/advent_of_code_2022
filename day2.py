# Advent of Code 2022
# Day 2

PART = 2

ROCK = 1
PAPER = 2
SCISSORS = 3

WIN = 6
DRAW = 3
LOSS = 0

abcMap = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}

xyzMap1 = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

xyzMap2 = {
    "X": LOSS,
    "Y": DRAW,
    "Z": WIN
}

outcomes = [
    { "me": ROCK, "them": ROCK, "outcome": DRAW },
    { "me": ROCK, "them": PAPER, "outcome": LOSS },
    { "me": ROCK, "them": SCISSORS, "outcome": WIN },
    { "me": PAPER, "them": ROCK, "outcome": WIN },
    { "me": PAPER, "them": PAPER, "outcome": DRAW },
    { "me": PAPER, "them": SCISSORS, "outcome": LOSS },
    { "me": SCISSORS, "them": ROCK, "outcome": LOSS },
    { "me": SCISSORS, "them": PAPER, "outcome": WIN },
    { "me": SCISSORS, "them": SCISSORS, "outcome": DRAW }
]

def parseLine1(line):
    line = line.strip()
    moves = line.split()
    theirs = abcMap[moves[0]]
    mine = xyzMap1[moves[1]]
    return [theirs, mine]

def parseLine2(line):
    line = line.strip()
    moves = line.split()
    theirs = abcMap[moves[0]]
    outcome = xyzMap2[moves[1]]
    return [theirs, outcome]

def outcome(me, them):
    for o in outcomes:
        if me == o["me"] and them == o["them"]:
            return o["outcome"]
    raise Exception("outcome: invalid parameters.")

def chooseMyMove(them, outcome):
    for o in outcomes:
        if them == o["them"] and outcome == o["outcome"]:
            return o["me"]
    raise Exception("chooseMyMove: invalid parameters.")

# Read the file

file = open('day2-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

myFinal = 0
theirFinal = 0
for line in lines:
    if PART == 1:
        [theirMove, myMove] = parseLine1(line)
        myOutcome = outcome(myMove, theirMove)
        theirOutcome = outcome(theirMove, myMove)
    elif PART == 2:
        [theirMove, myOutcome] = parseLine2(line)
        myMove = chooseMyMove(theirMove, myOutcome)
        theirOutcome = outcome(theirMove, myMove)
    else:
        raise Exception('Invalid PART value')
        
    round = {
        "mine": myMove,
        "theirs": theirMove,
        "myScore": myMove + myOutcome,
        "theirScore": theirMove + theirOutcome
    }
    myFinal += round["myScore"]
    theirFinal += round["theirScore"]

    print('{line}: {round}, myFinal={myFinal}, theirFinal = {theirFinal}'.format(line=line.strip(), round=round, myFinal=myFinal, theirFinal=theirFinal))

print('Final Score: me - {myFinal}, them - {theirFinal}'.format(myFinal=myFinal, theirFinal=theirFinal))
