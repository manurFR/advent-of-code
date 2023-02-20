import copy
import re
from pprint import pprint

from utils import inputparts

starting, procedure = inputparts("day05")
# pprint(starting)
nb_stacks = int(starting[-1][-1])  # last char of last line
# parse starting stacks to list of list, extracting only crates' names or a space if no crate
parsed_starting = [[line[idx] for idx in range(1, nb_stacks * 4, 4) if idx < len(line)]
                   for line in starting[:-1]]
pprint(parsed_starting)
# transform this in a list with an element for each stack (~ vertical to horizontal)
ref_stacks = [
    [parsed_starting[level][stackid] for level in range(-1, -1 * len(parsed_starting) - 1, -1)
     if stackid < len(parsed_starting[level]) and parsed_starting[level][stackid].strip()]
    for stackid in range(nb_stacks)
]

regex = re.compile(r"move (\d+) from (\d+) to (\d+)")


def run_crane(stacks, crane_operation):
    new_stacks = copy.deepcopy(stacks)
    # pprint(list(''.join(s) for s in new_stacks))
    for step in procedure:
        match = regex.match(step)
        if match:
            nb_crates = int(match.group(1))
            src = int(match.group(2)) - 1  # our stacks structure is 0-indexed, while the text procedure is 1-indexed
            dst = int(match.group(3)) - 1

            crane_operation(new_stacks, nb_crates, src, dst)
    # pprint(list(''.join(s) for s in new_stacks))
    return new_stacks


# part one
def cm9000(stacks, nb_crates, src, dst):
    for _ in range(nb_crates):  # one crate at a time
        stacks[dst].append(stacks[src].pop())  # top crate is removed and put on top of dst stack


stacks1 = run_crane(ref_stacks, cm9000)
top1 = [s[-1] for s in stacks1]
print(f"Part one: {''.join(top1)}")


# part two
def cm9001(stacks, nb_crates, src, dst):
    # print(f"{nb_crates} {src} {dst} | {stacks[src]} | {stacks[src][-nb_crates:]} | {stacks[src][:-nb_crates]}")
    # import sys
    # sys.exit(0)
    stacks[dst].extend(stacks[src][-nb_crates:])  # all crates put on top of dst stack in one go (keeping their order)
    stacks[src] = stacks[src][:-nb_crates]  # same crates removed from top of src stack


stacks2 = run_crane(ref_stacks, cm9001)
top2 = [s[-1] for s in stacks2]
print(f"Part two: {''.join(top2)}")
