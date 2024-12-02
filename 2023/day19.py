import itertools
from pprint import pprint
import re
import time

from utils import inputparts

test = ["""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}
""".splitlines(),
"""{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines()]

# data = test
data = inputparts(2023, 'day19')

cond_pattern = re.compile(r"(\w)([\<\>])(\d+)")

workflows = {}
for line in data[0]:
    if (match := re.match(r"(\w+)\{(.*)\}", line)):
        wf, rules = match.groups()
        rules = rules.split(',')
        wf_spec = []
        for r in rules:
            if ':' in r:
                cond, target = r.split(':')
                if (matchcond := cond_pattern.match(cond)):
                    category, op, val = matchcond.groups()
                    assert category in list('xmas')
                    val = int(val)
                    wf_spec.append((category, op, val, target))
            else:
                wf_spec.append((None, None, None, r))
        workflows[wf] = wf_spec

parts = []
for line in data[1]:
    spec = [r.split('=') for r in line.strip("{}").split(',')]
    ratings = {t[0]: int(t[1]) for t in spec}
    parts.append(ratings)

# pprint(parts)

def process(part):
    wf = 'in'
    while wf in workflows:
        rules = workflows[wf]
        for category, op, val, target in rules:
            if not category:  # terminal rule
                wf = target
                break
            score = part[category]
            match op:
                case '<':
                    if score < val:
                        wf = target
                        break
                case '>':
                    if score > val:
                        wf = target
                        break
    # if wf == 'R':
        # print(f"rejected: {p}")
    return wf == 'A'

accepted = [p for p in parts if process(p)]

# pprint(accepted)
def sumratings(part):
    return sum(part[k] for k in 'xmas')

print(f"Part one: {sum(sumratings(p) for p in accepted)}")

# part two
splits = {'x': [],  #  splits are [included, excluded[
          'm': [],
          'a': [],
          's': []}

for line in data[0]:
    if (match := re.match(r"(\w+)\{(.*)\}", line)):
        wf, rules = match.groups()
        rules = rules.split(',')
        for r in rules:
            if ':' in r:
                cond, target = r.split(':')
                if (matchcond := cond_pattern.match(cond)):
                    category, op, val = matchcond.groups()
                    assert category in list('xmas')
                    if op == '>':
                        splits[category].append(int(val) + 1)
                    else:
                        splits[category].append(int(val))

for category in 'xmas':
    splits[category] = sorted(list(set(splits[category])))
    splits[category].insert(0, 1)

# pprint([(c, splits[c]) for c in 'xmas'])
print(f"nb combinations: {len(splits['x'])*len(splits['m']*len(splits['a']*len(splits['s'])))}")

def next_rating(r, val):
    idxval = splits[r].index(val)
    if len(splits[r]) == idxval + 1:
        return 4001
    return splits[r][idxval + 1]

def covered(x, m, a, s):
    """Nb different combinations between (x, m, a, s) and the next split"""
    next_x = next_rating('x', x)
    next_m = next_rating('m', m)
    next_a = next_rating('a', a)
    next_s = next_rating('s', s)
    return (next_x - x) * (next_m - m) * (next_a - a) * (next_s - s)

combinations = itertools.product(*[splits[c] for c in 'xmas'])

starttime = time.time()
nb_combinations_covered = 0
for x, m, a, s in combinations:
    if process({'x': x, 'm': m, 'a': a, 's': s}):
        # print(f"accepted: {x} {m} {a} {s}")
        nb_combinations_covered += covered(x, m, a, s)
endtime = time.time()

# from 256.000 billions of combinations, I get down to only 6 billions, but it's still too much
# I give up. 
# Maybe one should process the tree of rules starting with 'in' with a different 'splits' on each branch
#  instead of having a single 'splits' for every case ?

print(f"Part two: {nb_combinations_covered} ({endtime - starttime:.4} sec)")