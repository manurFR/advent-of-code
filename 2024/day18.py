import copy
from utils import (EAST, NORTH, SOUTH, WEST, a_star_search, display, 
                   fwd, ingrid, manhattan, printdot, splittedinput, timeit)

TESTDATA = [[int(c) for c in line.split(',')] for line in """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip().splitlines()]
TEST_GRIDSIZE = 7
DATA_GRIDSIZE = 71


def adjacents(grid, currpos):
    next_positions = []
    for dirn in (NORTH, EAST, SOUTH, WEST):
        candidate = fwd(currpos, dirn) 
        if ingrid(grid, candidate) and grid[candidate[0]][candidate[1]] != '#':
            next_positions.append(candidate)
    return next_positions


@timeit
def part1(data, gridsize, nb_corruptions):
    grid = [['.'] * gridsize for _ in range(gridsize)]
    # corrupt
    for cx, cy in data[:nb_corruptions]:
        grid[cy][cx] = '#'

    # display(grid)

    startpos = (0, 0)

    path = a_star_search(grid, startpos, goalpos=(gridsize - 1 , gridsize -1),
                         adjacencyrule=adjacents,
                         heuristic_distance=manhattan)

    for y, x in path:
        grid[y][x] = 'O'
    display(grid)

    return len(path) - 1  # remove the starting position from the count


@timeit
def part2(data, gridsize, nb_corruptions):
    grid = [['.'] * gridsize for _ in range(gridsize)]
    # corrupt
    for cx, cy in data[:nb_corruptions]:
        grid[cy][cx] = '#'

    # display(grid)

    startpos = (0, 0)

    path = a_star_search(grid, startpos, goalpos=(gridsize - 1 , gridsize -1),
                         adjacencyrule=adjacents,
                         heuristic_distance=manhattan)

    count_recompute = 0
    for idx, (cx, cy) in enumerate(data[nb_corruptions:]):
        grid[cy][cx] = '#'

        if (cy, cx) in path:  # only recalculate the path if a new byte just blocked the previous best one
            path = a_star_search(grid, startpos, goalpos=(gridsize - 1 , gridsize -1),
                                 adjacencyrule=adjacents,
                                 heuristic_distance=manhattan)
            count_recompute += 1
        
            if path == []:
                break

        if (idx + 1) % 10 == 0:
            printdot()
            if (idx + 1) % 200 == 0:
                print(f" {idx + nb_corruptions} / {len(data)}")
    else:
        print("\nnot found!")
        return (0, 0)

    print(f" found at line {idx + 1}!  (with {count_recompute} recomputes)")
    return cx, cy


# Tests
def test_part1():
    assert part1(TESTDATA, TEST_GRIDSIZE, nb_corruptions=12) == 22


def test_part2():
    assert part2(TESTDATA, TEST_GRIDSIZE, nb_corruptions=12) == (6, 1)


if __name__ == "__main__":
    data = splittedinput(2024, "18", sep=',', conv=int)
    print(f"Part 1: {part1(data, DATA_GRIDSIZE, nb_corruptions=1024)}")
    print(f"Part 2: {part2(data, DATA_GRIDSIZE, nb_corruptions=1024)}")
