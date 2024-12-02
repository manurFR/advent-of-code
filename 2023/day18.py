import re
import time

from utils import EAST, NORTH, SOUTH, WEST, readinput
from shapely import Polygon, Point

D = {'U': NORTH, 'D': SOUTH, 'L': WEST, 'R': EAST}

test = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
""".splitlines()

test2 = """R 3 (#012345)
U 2 (#012345)
L 5 (#012345)
D 2 (#012345)
R 1 (#012345)
""".splitlines()

# data = test
# data = test2
data = readinput(2023, 'day18')

def display(grid):
    print('\n'.join(''.join(row) for row in grid))
    print()

pattern = re.compile(r"(\w) (\d+) \(\#(.*)\)")

def dig_edge(instructions):
    terrain = [['#']]

    curry, currx = (0, 0)
    edge = [(curry, currx)]

    for direction, meters in instructions:
        nexty = curry + D[direction][0] * meters
        nextx = currx + D[direction][1] * meters
        # print(f"{direction} {meters} => {nexty=} {nextx=}")

        # grow the terrain if needed
        while nexty < 0:
            terrain.insert(0, ['.' for y in range(len(terrain[0]))])
            curry += 1
            nexty += 1
            for idx in range(len(edge)):
                edge[idx] = (edge[idx][0] + 1, edge[idx][1])
        while nextx < 0:
            for row in terrain:
                row.insert(0, '.')
            currx += 1
            nextx += 1
            for idx in range(len(edge)):
                edge[idx] = (edge[idx][0], edge[idx][1] + 1)
        while len(terrain) < nexty + 1:
            terrain.append(['.' for y in range(len(terrain[0]))])
        while len(terrain[0]) < nextx + 1:
            for row in terrain:
                row.append('.')

        # dig the whole trench to the end
        while curry != nexty or currx != nextx:
            curry = curry + D[direction][0]
            currx = currx + D[direction][1]
            terrain[curry][currx] = '#'
            edge.append((curry, currx))

        # display(terrain)
    return terrain, edge

def dig_interior(terrain, edge):
    display(terrain)
    poly = Polygon(edge)

    starttime = time.time()
    nb_dug = len(edge) - 1  # the edge volume at the start, minus the starting point that is present twice
    for y in range(len(terrain)):
        for x in range(len(terrain[0])):
            p = Point(y, x)
            if poly.contains(p):
                terrain[y][x] = '#'
                nb_dug += 1
    endtime = time.time()
    display(terrain)

    return nb_dug, endtime - starttime




instr_part1 = []
hexa_instr = []

for line in data:
    if (match := pattern.match(line)):
        direction, meters, hexa = match.groups()
        instr_part1.append((direction, int(meters)))
        hexa_instr.append(hexa)

t1, e1 = dig_edge(instr_part1)
nb1, time1 = dig_interior(t1, e1)
print(f"Part one: {nb1} ({time1:.4} sec)")

instr_part2 = []

for hexa in hexa_instr:
    match hexa[-1]:
        case '0':
            direction = 'R'
        case '1':
            direction = 'D'
        case '2':
            direction = 'L'
        case '3':
            direction = 'U'
    meters = int(hexa[:5], 16)
    instr_part2.append((direction, meters))


def dig_edge2(instructions):
    # chunks of continuous symbols in both dimensions
    #  for example if dimx = [1, 3, 2, 3] and terrain[0] = ['#', '.', '#', '.'], 
    #  the digging row is actually: #...##...
    dimy, dimx = [1,4,5,5,5], [1,]  # chunks of continuous symbols in both dimensions
    terrain = [['#'], ['.'], ['.'], ['.'], ['.']]

    curry, currx = (0, 0)
    edge = [(0, 0)]

    for direction, meters in instructions:
        # grow the terrain if needed
        nexty = curry + D[direction][0] * meters
        nextx = currx + D[direction][1] * meters
        print(f"{direction} {meters} => {nexty=} {nextx=}")

        if nexty < 0:
            dimy.insert(0, -nexty)
            terrain.insert(0, ['.' for x in dimx])
            curry -= nexty
            # nexty = 0
            for idx in range(len(edge)):
                edge[idx] = (edge[idx][0] + 1, edge[idx][1])
        if nextx < 0:
            dimx.insert(0, -nextx)
            for row in terrain:
                row.insert(0, '.')
            currx -= currx
            # nextx = 0
            for idx in range(len(edge)):
                edge[idx] = (edge[idx][0], edge[idx][1] + 1)
        if nexty + 1 > sum(dimy):
            dimy.append(nexty + 1 - sum(dimy))
            terrain.append(['.' for x in dimx])
        if nextx + 1 > sum(dimx):
            dimx.append(nextx + 1 - sum(dimx))
            for row in terrain:
                row.append('.')

        print(f"{dimy=}")

        # dig the trench, determine if a chunk should be splitted
        total = 0
        for idx, chunk in enumerate(dimy):
            total = total + chunk
            print(f"{idx=} {chunk=} {total=}")
            if total > curry + 1:
                # next_chunk = dimy[idx + 1]
                # print(f"{next_chunk=}")
                if meters < chunk:
                    # split in dim
                    dimy[idx] = chunk - meters
                    dimy.insert(idx, meters)
                    # split in terrain
                    terrain.insert(idx, ['.'])
                # dig
                terrain[idx][0] = '#'
                edge.append((idx, 0))
                meters -= chunk
                print(f"{dimy=}")
                display(terrain)
            if total > nexty:
                break

        curry, currx = nexty, nextx

        # while curry != nexty or currx != nextx:
            # curry = curry + D[direction][0]
            # currx = currx + D[direction][1]
            # terrain[curry][currx] = '#'
            # edge.append((curry, currx))

        # display(terrain)
    return terrain, edge

# t2, e2 = dig_edge2(instr_part2)
# print(len(e2))        
