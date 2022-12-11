# Advent of Code 2022
# Day 11

import re

NUMBER_OF_ROUNDS = 10000
NUMBER_OF_MONKEYS = 8

def newWorry(value, op, divisor, worry):
    if value == 'old':
        operand = worry
    else:
        operand = int(value)
    if op == '+':
        worry += operand
    elif op == '*':
        worry *= operand
    else:
        raise Exception("Invalid operation:", op)
#    worry //= 3
    worry %= divisor
    return worry


# Read the file

file = open('day11-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

nMonkeys = 0
iLine = 0
monkeys = []
while iLine < len(lines):
    # Read monkey number
    match = re.findall('\d+', lines[iLine])
    iLine += 1
    if int(match[0]) != nMonkeys:
        raise Exception('Unexpected monkey {n}'.format(n=match[0]))
    
    # Read the monkey's starting items
    match = re.findall('\d+', lines[iLine])
    iLine += 1
    items = []
    for m in match:
        w = int(m)
        items.append([w for i in range (0, NUMBER_OF_MONKEYS)])
    
    # Read operation
    match = re.search('\s*Operation: new = old (.) (.+)', lines[iLine])
    iLine += 1
    op = match.group(1)
    value = match.group(2)

    # Read test
    match = re.findall('\d+', lines[iLine])
    iLine += 1
    test = int(match[0])
    match = re.findall('\d+', lines[iLine])
    iLine += 1
    trueAction = int(match[0])
    if trueAction == nMonkeys:
        raise Exception("Monkey throwing to self.")
    match = re.findall('\d+', lines[iLine])
    iLine += 1
    falseAction = int(match[0])
    if falseAction == nMonkeys:
        raise Exception("Monkey throwing to self.")
    
    monkey = {  "items" : items,
                "op" : op,
                "value" : value,
                "test" : test,
                "trueAction" : trueAction,
                "falseAction" : falseAction,
                "inspectionCount" : 0
             }
    monkeys.append(monkey)
    iLine += 1 # Skip blank line
    nMonkeys += 1
    
if nMonkeys != NUMBER_OF_MONKEYS:
    raise Exception('Expected {n} monkeys'.format(n=NUMBER_OF_MONKEYS))

#print(monkeys)

for round in range(1, NUMBER_OF_ROUNDS+1):
    for k in range(0, NUMBER_OF_MONKEYS):
        m = monkeys[k]
        for item in m["items"]:
            for i in range(0, len(item)): # for each monkey
                item[i] = newWorry(m["value"], m["op"], monkeys[i]["test"], item[i])

            if item[k] == 0:
                monkeys[m["trueAction"]]["items"].append(item)
            else:
                monkeys[m["falseAction"]]["items"].append(item)
        m["inspectionCount"] += len(m["items"])
        m["items"] = []

    # Update every 1000 rounds
    if round % 10 == 0:
        print("Round:", round)
        for k in range(0, NUMBER_OF_MONKEYS):
           print('Monkey {k} inpected {n} items'.format(k=k, n=monkeys[k]["inspectionCount"]), monkeys[k]["items"])


# Find the top 2
count1 = 0
count2 = 0
for m in monkeys:
    if m["inspectionCount"] > count1:
        count2 = count1
        count1 = m["inspectionCount"]
    elif m["inspectionCount"] > count2:
        count2 = m["inspectionCount"]

print("Monkey business =", count1 * count2)
