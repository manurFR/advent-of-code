from utils import EAST, NORTH, SOUTH, WEST, readinput
import sys

SYMBOL = {NORTH: '^', SOUTH: 'v', WEST: '<', EAST: '>'}
ROTATIONS_SLASH = {NORTH: EAST, EAST: NORTH, SOUTH: WEST, WEST: SOUTH}
ROTATIONS_ANTI = {NORTH: WEST, EAST: SOUTH, SOUTH: EAST, WEST: NORTH}

strdir = {NORTH: 'NORTH', SOUTH: 'SOUTH', WEST: 'WEST', EAST: 'EAST'}

test = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""".splitlines()

# data = test
data = readinput('day16')

original = [[c for c in row] for row in data]

def display(grid):
    print('\n'.join(''.join(row) for row in grid))

def rotate(direction, mirror):
    return ROTATIONS_SLASH[direction] if mirror == '/' else ROTATIONS_ANTI[direction]
    
assert rotate(NORTH, '\\') == WEST
assert rotate(WEST, '\\') == NORTH
assert rotate(SOUTH, '/') == WEST
assert rotate(EAST, '/') == NORTH

def diffract(direction, splitter):
    if splitter == '|' and direction in (WEST, EAST):
        return NORTH, SOUTH
    elif splitter == '-' and direction in (NORTH, SOUTH):
        return EAST, WEST
    else:
        return (direction,)

def energize(starty, startx, direction):
    schematics = [[c for c in row] for row in data]
    energies = [[[] for c in row] for row in data]

    beams = [(starty, startx, direction)]

    while beams:
        newbeams = []
        for y, x, direction in beams:
            nexty = y + direction[0]
            nextx = x + direction[1]
            if nexty < 0 or nexty >= len(original) or nextx < 0 or nextx >= len(original[0]):
                continue  # the beam gets lost out of the grid
            nextsymbol = original[nexty][nextx]
            if nextsymbol == '.':
                nextenergies = energies[nexty][nextx]
                if len(nextenergies) == 0:  # a beam has never passed here
                    nextenergies.append(direction)
                    schematics[nexty][nextx] = SYMBOL[direction]
                    newbeams.append((nexty, nextx, direction))
                elif direction not in nextenergies:  # some beam have already passed here but not in the same direction
                    nextenergies.append(direction)
                    schematics[nexty][nextx] = str(len(nextenergies))
                    newbeams.append((nexty, nextx, direction))
                else:  # a beam in the same direction has already passed here ; it's a loop, lose the beam and do nothing
                    pass
            elif nextsymbol in ('/', '\\'):
                energies[nexty][nextx].append(direction)
                direction = rotate(direction, nextsymbol)
                newbeams.append((nexty, nextx, direction))
            elif nextsymbol in ('|', '-'):
                energies[nexty][nextx].append(direction)
                directions = diffract(direction, nextsymbol)
                for d in directions:
                    newbeams.append((nexty, nextx, d))
        beams = newbeams
        # print([(y, x, strdir[d]) for y, x, d in beams])
        # display(schematics)
        # print()
    
    energizing = [['#' if len(tile) > 0 else '.' for tile in row] for row in energies]
    return sum(1 for row in energizing for tile in row if tile == '#')

nb_energized_1 = energize(0, -1, EAST) # starting with one beam at (0, -1) going eastward

print(f"Part one: {nb_energized_1}")

energized_part2 = []
energized_part2.extend(energize(-1, x, SOUTH) for x in range(len(original[0])))  # top row
energized_part2.extend(energize(len(original), x, NORTH) for x in range(len(original[0])))  # bottom row
energized_part2.extend(energize(y, -1, EAST) for y in range(len(original)))  # leftmost column
energized_part2.extend(energize(y, len(original[0]), WEST) for y in range(len(original)))  # rightmost column

print(f"Part two: {max(energized_part2)}")
