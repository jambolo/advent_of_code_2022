# Advent of Code 2022
# Day 21

import re

PART_1 = False
TEST = False
if TEST:
    FILE_NAME = 'day21-test.txt'
else:
    FILE_NAME = 'day21-input.txt'

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def evaluate(monkeys, name):
    m = monkeys[name]
    if "value" in m:
        return m["value"]
    else:
        op = m["op"]
        operand0 = m["operands"][0]
        operand1 = m["operands"][1]
        if m["op"] == '+':
            return evaluate(monkeys, operand0) + evaluate(monkeys, operand1)
        elif m["op"] == '-':
            return evaluate(monkeys, operand0) - evaluate(monkeys, operand1)
        elif m["op"] == '*':
            return evaluate(monkeys, operand0) * evaluate(monkeys, operand1)
        elif m["op"] == '/':
            return evaluate(monkeys, operand0) / evaluate(monkeys, operand1)
        elif m["op"] == '=':
            return evaluate(monkeys, operand0) == evaluate(monkeys, operand1)
        else:
            raise Exception("invalid operator")

def findPath(monkeys, node, name):
    m = monkeys[node]
    if node == name:
        return [name]
    if "value" in m:
        return None
    path = findPath(monkeys, m["operands"][0], name)
    if not path:
        path = findPath(monkeys, m["operands"][1], name)
    if not path:
        return None
    newPath = path.copy()
    newPath.insert(0, node)
    return newPath

def invert(monkeys, name, path, goal):
    if name == "humn":
        return goal
    m = monkeys[name]
    if m["operands"][0] not in pathToHumn:
        operand0 = evaluate(monkeys, m["operands"][0])
        if m["op"] == '+':
            humn = invert(monkeys, m["operands"][1], pathToHumn, goal - operand0)
        elif m["op"] == '-':
            humn = invert(monkeys, m["operands"][1], pathToHumn, operand0 - goal)
        elif m["op"] == '*':
            humn = invert(monkeys, m["operands"][1], pathToHumn, goal / operand0)
        elif m["op"] == '/':
            humn = invert(monkeys, m["operands"][1], pathToHumn, operand0 / goal)
        elif m["op"] == '=':
            humn = invert(monkeys, m["operands"][1], pathToHumn, operand0 if goal else -operand0)
    else:
        operand1 = evaluate(monkeys, m["operands"][1])
        if m["op"] == '+':
            humn = invert(monkeys, m["operands"][0], pathToHumn, goal - operand1)
        elif m["op"] == '-':
            humn = invert(monkeys, m["operands"][0], pathToHumn, goal + operand1)
        elif m["op"] == '*':
            humn = invert(monkeys, m["operands"][0], pathToHumn, goal / operand1)
        elif m["op"] == '/':
            humn = invert(monkeys, m["operands"][0], pathToHumn, goal * operand1)
        elif m["op"] == '=':
            humn = invert(monkeys, m["operands"][0], pathToHumn, operand1 if goal else -operand1)
    return humn

# Read the file.
lines = readFile(FILE_NAME)

monkeys = {}
for line in lines:
    match = re.search('([a-z]{4})\: (\d+|([a-z]{4}) ([\+\-\*\/]) ([a-z]{4}))', line)
    if match.group(3):
        monkey = { "op" : match.group(4), "operands" : [match.group(3), match.group(5)] }
    else:
        monkey = { "value" : int(match.group(2)) }
    monkeys[match.group(1)] = monkey

root = monkeys["root"]

if PART_1:
    value = evaluate(monkeys, "root")
    print("Root yells: ", value)
else:
    root["op"] = '='


    n = "humn"
    testPath = ["humn"]
    while n != "root":
        for m in monkeys:
            if "value" not in monkeys[m]:
                if n in monkeys[m]["operands"]:
                    n = m
                    testPath.append(m)
                    break

    pathToHumn = findPath(monkeys, "root", "humn")

    if root["operands"][0] not in pathToHumn:
        goal = evaluate(monkeys, root["operands"][0])
        humn = invert(monkeys, root["operands"][1], pathToHumn, goal)
    else:
        goal = evaluate(monkeys, root["operands"][1])
        humn = invert(monkeys, root["operands"][0], pathToHumn, goal)
    print("humn =", humn)
    monkeys["humn"]["value"] = humn
    print("success =", evaluate(monkeys, "root"))

