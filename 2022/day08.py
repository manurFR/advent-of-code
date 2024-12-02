import math

from utils import readinput

data = readinput(2022, "day08")


def is_visible_from(tree, others):
    """A tree is visible if all other trees in a direction ('others') are smaller than it.
    Edge trees will have at least one empty 'others' sets, so we add 'not others' to ensure they are reported
    as visible."""
    return not others or all(tree > other for other in others)


def viewing_dist(tree, others):
    dist = 0
    for other in others:
        dist += 1
        if other >= tree:
            break
    return dist


assert viewing_dist(2, []) == 0
assert viewing_dist(2, [2, 2, 1]) == 1
assert viewing_dist(2, [3, 2, 1]) == 1
assert viewing_dist(2, [0, 1, 2]) == 3
assert viewing_dist(2, [1, 1, 1, 0]) == 4


# noinspection PyShadowingNames
def directions(x, y):
    """Returns lists of trees from (x,y) in each of the four directions : left, right, top, down,
       starting from (x,y) towards the edge."""
    return ([int(i) for i in reversed(data[y][:x])],                    # left
            [int(i) for i in data[y][x+1:]],                            # right
            [int(data[row][x]) for row in range(y-1, -1, -1)],          # up
            [int(data[row][x]) for row in range(y+1, len(data))]        # down
            )


# pprint(directions(3, 3))

visibles = []
for y in range(len(data)):
    for x in range(len(data[0])):
        val = int(data[y][x])
        if any(is_visible_from(val, others) for others in directions(x, y)):
            visibles.append((x, y))
            print('O', end='')
        else:
            print('.', end='')
    print()
print()
print(f"Part one: {len(visibles)}")

scenic_scores = [math.prod(
                    viewing_dist(int(data[y][x]), others)
                    for others in directions(x, y)
                 )
                 for x in range(len(data[0])) for y in range(len(data))]

print(f"Part two: {max(scenic_scores)}")
