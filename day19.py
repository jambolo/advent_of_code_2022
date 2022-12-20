# Advent of Code 2022
# Day 19

import re

FILE_NAME = 'day19-input.txt'
PART = 2
NUMBER_OF_RESOURCE_TYPES = 4
NUMBER_OF_ROBOT_TYPES = NUMBER_OF_RESOURCE_TYPES
if PART == 1:
    TIME_LIMIT = 24
else:
    TIME_LIMIT = 32

def readFile(name):
    file = open(name, mode = 'r', encoding = 'utf-8-sig')
    lines = file.readlines()
    file.close()
    return lines

def collect(resources, robots):
    for i in range(0, NUMBER_OF_RESOURCE_TYPES):
        resources[i] += robots[i]

def spend(resources, blueprint):
    for i in range(0, NUMBER_OF_RESOURCE_TYPES):
        resources[i] -= blueprint[i]

def addState(states, state):
    removal = []
    for s in states:
        if s[0] >= state[0] and s[1] >= state[1] and s[2] >= state[2] and s[3] >= state[3] and s[4] >= state[4] and s[5] >= state[5] and s[6] >= state[6] and s[7] >= state[7]:
            return
        elif s[0] < state[0] and s[1] < state[1] and s[2] < state[2] and s[3] < state[3] and s[4] < state[4] and s[5] < state[5] and s[6] < state[6] and s[7] < state[7]:
            removal.append(s)
    if removal:
        for r in removal:
            states.remove(r)
    states.add(state)

# Read the file.
lines = readFile(FILE_NAME)

blueprints = []
for line in lines:
    match = re.search('Blueprint \d+: Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.', line)
    blueprints.append([
        (int(match.group(1)), 0, 0, 0),
        (int(match.group(2)), 0, 0, 0),
        (int(match.group(3)), int(match.group(4)), 0, 0),
        (int(match.group(5)), 0, int(match.group(6)), 0)
    ])

sum = 0
product = 1
if PART == 1:
    nBlueprints = len(blueprints)+1
else:
    nBlueprints = 3 + 1

for b in range(1, nBlueprints):
    blueprint = blueprints[b-1]
    states = set()
    states.add((1, 0, 0, 0, 0, 0 , 0, 0))
    for time in range(0, TIME_LIMIT):
        nextStates = set()
        for s in states:
            robots = [s[0], s[1], s[2], s[3]]
            resources = [s[4], s[5], s[6], s[7]]
            builds = []
            for r in range(0, NUMBER_OF_ROBOT_TYPES):
                if resources[0] >= blueprint[r][0] and resources[1] >= blueprint[r][1] and resources[2] >= blueprint[r][2]:
                    nRobotRs = robots[r]
                    if r >= 3 or nRobotRs < blueprint[1][r] or nRobotRs < blueprint[2][r] or nRobotRs < blueprint[3][r]:
                        builds.append(r)
            if len(builds) < NUMBER_OF_ROBOT_TYPES:
                # Try skip building if we can't build all types
                addState(nextStates, (robots[0], robots[1], robots[2], robots[3], resources[0] + robots[0], resources[1] + robots[1], resources[2] + robots[2], resources[3] + robots[3]))

            # Try with building one of each of the robots that can be built
            for k in builds:
                updatedResources = resources.copy()
                spend(updatedResources, blueprint[k])
                collect(updatedResources, robots)
                updatedRobots = robots.copy()
                updatedRobots[k] += 1
                addState(nextStates, (updatedRobots[0], updatedRobots[1], updatedRobots[2], updatedRobots[3], updatedResources[0], updatedResources[1], updatedResources[2], updatedResources[3]))
        states = nextStates
        print("  Time:", time, ", number states =", len(states))

    geodes = 0
    for s in states:
        if s[7] > geodes:
            geodes = s[7]
    print("Blueprint", b, ",", geodes, "geodes")
    quality = geodes * b
    sum += quality
    product *= geodes

print("Quality sum =", sum)
print("Geodes product =", product)
