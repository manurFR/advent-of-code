import re
from utils import readinput

test = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

# data = test
data = readinput('day15')[0]

seq = data.split(',')

def hash_algo(string):
    val = 0
    for c in string:
        val += ord(c)
        val = (val * 17) % 256
    return val

# print(hash_algo('HASH'))

print(f"Part one: {sum(hash_algo(part) for part in seq)}")

# print(f"cm={hash_algo('cm')} ot={hash_algo('ot')}")

boxes = [[] for _ in range(256)]

pattern = re.compile(r"(\w+)([-=])(\d*)")

for step in seq:
    if (match := pattern.match(step)):
        label, op, foc = match.groups()
        boxid = hash_algo(label)
        currbox = boxes[boxid]
        currlabels = [t[0] for t in currbox]
        if op == '-':
            if label in currlabels:
                idx = currlabels.index(label)
                del currbox[idx]
        elif op == '=':
            focal_length = int(foc)
            if label in currlabels:
                idx = currlabels.index(label)
                currbox[idx] = (label, focal_length)
            else:
                currbox.append((label, focal_length))
        # print(boxid, currbox)

powers = []
for boxid, currbox in enumerate(boxes):
    for lensid, lens in enumerate(currbox):
        powers.append((boxid + 1) * (lensid + 1) * lens[1])

print(f"Part two: {sum(powers)}")
