from dataclasses import dataclass
import math
from pprint import pprint
import re
from utils import readinput

test1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

test2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".splitlines()

test3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".splitlines()

# data = test1
# data = test2
# data = test3
data = readinput('day08')

PATTERN = re.compile(r"(\w+) = \((\w+), (\w+)\)")

instructions = data[0]
assert all(c in ('L', 'R') for c in instructions)

@dataclass
class Node:
    name: str
    spec: tuple
    left: 'Node'
    right: 'Node'

# create the nodes with the left/right as strings for now
inventory = {}
for line in data[2:]:
    if match := PATTERN.match(line):
        curr, left, right = match.groups()
        n = Node(name=curr, spec=(left, right), left=None, right=None)
        inventory[curr] = n

# replace left/right by link to next node
for name, node in inventory.items():
    node.left = inventory[node.spec[0]]
    node.right = inventory[node.spec[1]]

# Part one
def walk_desert(starting_node, end_condition):
    if not starting_node:
        return -1
    nb_steps = 0
    currnode = starting_node
    while not end_condition(currnode.name):
        new_step = instructions[nb_steps % len(instructions)]
        if new_step == 'L':
            new_node = currnode.left
        elif new_step == 'R':
            new_node = currnode.right
        nb_steps += 1
        currnode = new_node
    return nb_steps, currnode.name

print(f"Part one: {walk_desert(inventory.get('AAA'), end_condition=lambda name: name == 'ZZZ')}")

# Part two
nb_steps = 0
startnodes = [inventory[n] for n in inventory.keys() if n.endswith('A')]
# compute the nb_steps of each starting node individually
steps = [walk_desert(n, end_condition=lambda name: name.endswith('Z')) for n in startnodes]
# this proves that the paths loop over themselves after <steps> steps
for idx, (_, endnode) in enumerate(steps):
    print(f"{startnodes[idx].name}=>{endnode} {inventory[endnode].spec}=={inventory[startnodes[idx].name].spec}")

print(f"Part two: {math.lcm(*[nb_steps for nb_steps, _ in steps])}")