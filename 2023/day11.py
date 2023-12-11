import itertools
from pprint import pprint

from utils import readinput


test1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".splitlines()

# data = test1
data = readinput('day11')

# expanding universe ('E' is a unit of expansion)
space_temp = []
for row in data:
    if row[0] == '.' and len(set(row)) == 1:
        space_temp.append('E'*len(row))
    space_temp.append(row)

# print('\n'.join(space_temp))

space = [[] for row in space_temp]
for col in range(len(space_temp[0])):
    fullcol = [space_temp[y][col] for y in range(len(space_temp))]
    # print(col, ''.join(fullcol))
    if fullcol[0] in ('.', 'E') and set(fullcol).issubset(set(['.', 'E'])):
        for row in space:
            row.append('E')
    for y, row in enumerate(space):
        row.append(space_temp[y][col])

# identify galaxies
galaxies = [(y, x) for y in range(len(space)) for x in range(len(space[0])) if space[y][x] == '#']
# print(galaxies)

print('\n'.join(''.join(row) for row in space))

# prepare pairs of galaxies
pairs = list(itertools.combinations(range(len(galaxies)), 2))
# print(pairs)

# compute distances
def manhattan(start, end, expansion_ratio=None):
    curr = start
    length = 0
    starty, startx = start
    endy, endx = end
    while curr != end:
        newy, newx = curr
        if (dy := endy - newy) != 0:
            newy = newy + (1 if dy > 0 else -1)
        else:
            newx = newx + (1 if endx - newx > 0 else -1)
        # print(f"{start} {end} | {curr} {dy} {endx - startx} => ({newy}, {newx})")
        if expansion_ratio and space[newy][newx] == 'E':
            length += (expansion_ratio - 1)
        else:
            length += 1
        curr = (newy, newx)
    return length

dists1 = [manhattan(galaxies[start], galaxies[end]) for start, end in pairs]

# for p, d in zip(pairs, dists):
    # print(p, d)

print(f"Part one: {sum(dists1)}")

dists_exp100 = [manhattan(galaxies[start], galaxies[end], expansion_ratio=100) for start, end in pairs]
print(sum(dists_exp100))

dists2 = [manhattan(galaxies[start], galaxies[end], expansion_ratio=1000000) for start, end in pairs]
print(f"Part two: {sum(dists2)}")
