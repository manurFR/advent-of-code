from utils import readinput

data = readinput("day08")

visibles = []

# print(data[5])


def is_visible_from(val, others):
    """A tree is visible if all other trees in a direction ('others') are smaller than it.
    Edge trees will have at least one empty 'others' sets, so we add 'not others' to ensure they are reported
    as visible."""
    return not others or all(val > other for other in others)


def is_visible(x, y):
    val = data[y][x]
    left = set(data[y][:x])
    right = set(data[y][x+1:])
    up = set([data[row][x] for row in range(y)])
    down = set([data[row][x] for row in range(y+1, len(data))])
    # print(val, left, right, up, down)
    return (is_visible_from(val, left) or is_visible_from(val, right)
            or is_visible_from(val, up) or is_visible_from(val, down))


# print(is_visible(3, 3))


for y in range(len(data)):
    for x in range(len(data[0])):
        if is_visible(x, y):
            visibles.append((x, y))
            print('O', end='')
        else:
            print('.', end='')
    print()
print()

print(f"Part one: {len(visibles)}")
