import time
from utils import readinput
from shapely import Polygon, Point

# increments in (y, x) when going to each direction
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

OPPOSITES = {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}

PIPES = {  # which direction are joined by each kind of pipe
    '|': [NORTH, SOUTH],
    '-': [WEST, EAST],
    'L': [NORTH, EAST],
    'J': [NORTH, WEST],
    '7': [SOUTH, WEST],
    'F': [SOUTH, EAST],
}

test1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".splitlines()

test2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".splitlines()

# data = test1
# data = test2
data = readinput(2023, 'day10')

display = [[c for c in row] for row in data]  # initialize
DISP_REPLACE = {NORTH: '^', SOUTH: 'v', EAST: '>', WEST: '<'}

start = None
for y in range(len(data)):
    for x in range(len(data[0])):
        if data[y][x] == 'S':
            start = (y, x)
            break
    if start:
        break

def walk(pos, step):
    """Walk for position pos by doing a step.
    Returns the new position + the next direction 
    when following the pipe in this new position, ie. the next step"""
    y, x = pos
    stepy, stepx = step
    if y + stepy < 0 or y + stepy >= len(data) or x + stepx < 0 or x + stepx >= len(data[0]):
        return None, None
    new_pos = (y + stepy, x + stepx)
    new_pos_symbol = get_symbol(new_pos)
    coming_from = OPPOSITES[step]
    # print(f"walk({pos}, {step}) => new_pos={new_pos} [symbol={new_pos_symbol}], coming_from={coming_from}")
    if new_pos_symbol in PIPES:
        # the directions connected by the pipe at new position
        next_steps = PIPES[get_symbol(new_pos)][:]  # make a copy !
        if coming_from in next_steps:
            next_steps.remove(coming_from)
            display[y + stepy][x + stepx] = DISP_REPLACE[next_steps[0]]
            return new_pos, next_steps[0]
        else:
            return new_pos, None
    else:
        return new_pos, None

def get_symbol(pos):
    return data[pos[0]][pos[1]]

print(f"start={start}")
# print(walk((1, 1), EAST))  # expected (1, 2), (-1, 0) with test data

# find the neighbours of the starting position, ie. the two adjacent pipes that connect back to it
neighbours = []
starting_steps = []
for step in (NORTH, EAST, SOUTH, WEST):
    neighbour, _ = walk(start, step)
    # try the next direction if we were going outside the grid or the adjacent cell is not a pipe
    if neighbour and get_symbol(neighbour) in PIPES:
        # print(f"neighbour={neighbour} [symbol={get_symbol(neighbour)}]")
        neighbour_pipes = PIPES[get_symbol(neighbour)]
        # print(f"neighbour_pipes={neighbour_pipes}, opposite={OPPOSITES[step]}")
        if OPPOSITES[step] in neighbour_pipes:
            neighbours.append(neighbour)
            starting_steps.append(step)

# print(neighbours)
# print(starting_steps)
assert len(neighbours) == 2

# let's walk in two directions simultaneously
pos_dir1, pos_dir2 = start, start
step_dir1, step_dir2 = starting_steps
path_dir1, path_dir2 = [], []
while len(path_dir1) == 0 or path_dir1[-1] != path_dir2[-1]:
    next_pos_dir1, next_step_dir1 = walk(pos_dir1, step_dir1)
    next_pos_dir2, next_step_dir2 = walk(pos_dir2, step_dir2)
    path_dir1.append(next_pos_dir1)
    path_dir2.append(next_pos_dir2)
    pos_dir1, step_dir1 = next_pos_dir1, next_step_dir1
    pos_dir2, step_dir2 = next_pos_dir2, next_step_dir2

# displaying the two paths
display[path_dir1[-1][0]][path_dir1[-1][1]] = '*'  # arrival
for row in display:
    print(''.join(row))
print()

print(f"Part one: {len(path_dir1)}")

loop = [start]
loop.extend(path_dir1)
loop.extend(reversed(path_dir2[:-1]))
loop.append(start)

poly = Polygon(loop)

starttime = time.time()
nb_enclosed = 0
for y in range(len(data)):
    for x in range(len(data[0])):
        p = Point(y, x)
        if poly.contains(p):
            display[y][x] = 'I'
            nb_enclosed += 1
endtime = time.time()

for row in display:
    print(''.join(row))
print()

print(f"Part two: {nb_enclosed} ({endtime - starttime} seconds)")
