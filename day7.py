# Advent of Code 2022
# Day 7

import re

THRESHOLD      = 100000
TOTAL_SPACE    = 70000000
MINIMUM_UNUSED = 30000000

class Node:
    def __init__(self, name, size, parent=None):
        self.parent = parent
        self.name = name
        self.size = size
        self.nodes = []
        self.files = []

def cd(where, node):
    if where == '/':
        cwd = None
    elif where == '..':
        if node == root:
            raise Exception('cd .. at root')
        cwd = node.parent
    else:
        for n in node.nodes:
            if n.name == where:
                cwd = n
                break
    return cwd

def addNode(name, node):
    found = False
    for n in node.nodes:
        if n.name == name:
            found = True
            break
    if not found:
        node.nodes.append(Node(name, 0, cwd))

def addFile(name, size, node):
    found = False
    for n in node.files:
        if n.name == name:
            found = True
            break
    if not found:
        node.files.append(Node(name, size))
        n = node
        while n:
            n.size += size
            n = n.parent

def findNodesUnderThreshold(node, result):
    if node.size <= THRESHOLD:
        result.append(node)
    for n in node.nodes:
        findNodesUnderThreshold(n, result)
    
def findSmallestNode(node, minimum):
    best = 0
    for n in node.nodes:
        size = findSmallestNode(n, minimum)
        if size >= minimum and (not best or size < best):
            best = size
    if node.size >= minimum and (not best or node.size < best):
        best = node.size
    return best
 
def drawFileSystem(node, spaces):
    print('{s}{name}: {size}'.format(s=spaces, name=node.name, size=node.size))
    for n in node.nodes:
        drawFileSystem(n, spaces + '  ')
    for f in node.files:
        print('{s}  {name}: {size}'.format(s=spaces, name=f.name, size=f.size))

# Read the file

file = open('day7-input.txt', mode = 'r', encoding = 'utf-8-sig')
lines = file.readlines()
file.close()

root = Node('/', 0)
cwd = root

i = 0
while i < len(lines):
    line = lines[i].strip()
    i = i + 1

    # Determine what the command is
    if line[0] != '$':
        raise Exception('Command expected at line {i}. Found this: {c}'.format(i=i, c=line))

    command = line[2:]
    if command[:2] == 'cd':
        where = command[3:]
        cwd = cd(where, cwd)
        if not cwd:
            cwd = root
    elif command == 'ls':
        while i < len(lines) and lines[i][0] != '$':
            line = lines[i].strip()
            i = i + 1
            if line[:3] == 'dir':
                addNode(line[4:], cwd)
            else:
                match = re.search('(\d+)\s+(.+)', line)
                size = int(match.group(1))
                name = match.group(2)
                addFile(name, size, cwd)
    else:
        raise Exception('Unknown command at line {i}. Found this: {c}'.format(i=i+1, c=command))


drawFileSystem(root, '')

# Part 1 solution

result = []
findNodesUnderThreshold(root, result)

total = 0
for r in result:
    total += r.size

print('Total of nodes: {total}'.format(total=total))

# Part 2 solution

used = root.size
unused = TOTAL_SPACE - used
needed = MINIMUM_UNUSED - unused

print('used={used}, unused={unused}, needed={needed}'.format(used=used, unused=unused, needed=needed))

best = findSmallestNode(root, needed)
print('Best node to delete has size of {best}'.format(best=best))
