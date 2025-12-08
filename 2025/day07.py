import copy
from utils import SOUTH, breadth_first_search, display, find, fwd, ingrid, splittedinput, timeit

TESTDATA = [[c for c in line] for line in """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip().splitlines()]


@timeit
def part1(data):
    grid = copy.deepcopy(data)
    splits = 0
    beams = find(grid, "S")
    # print(f"Initial beams: {beams=}")
    # display(grid)
    step = 1
    while beams and all(b[0] < len(grid) - 1 for b in beams):
        newbeams = []
        for b in beams:
            next = fwd(b, SOUTH)
            if ingrid(grid, next):
                ny, nx = next
                if grid[ny][nx] == ".":
                    grid[ny][nx] = "|"
                    newbeams.append(next)
                elif grid[ny][nx] == "^":
                    splits += 1
                    bx = nx - 1
                    if ingrid(grid, (ny, bx)) and (ny, bx) not in beams:
                        grid[ny][bx] = "|"
                        newbeams.append((ny, bx))
                    bx = nx + 1
                    if ingrid(grid, (ny, bx)) and (ny, bx) not in beams:
                        grid[ny][bx] = "|"
                        newbeams.append((ny, bx));
        beams = newbeams
        step += 1
        # print(f"After step: {beams=}")
    display(grid)
    return splits


@timeit
def part2(data):
    grid = copy.deepcopy(data)
    beams = find(grid, "S")
    # this keeps track of how many ways we can reach each x position at the current y level
    timelines = {beams[0][1]: 1}  # {x: nb_paths_to_here}
    step = 1
    while beams and all(b[0] < len(grid) - 1 for b in beams):
        newbeams = []
        for b in beams:
            next = fwd(b, SOUTH)
            if ingrid(grid, next):
                ny, nx = next
                if grid[ny][nx] == ".":
                    newbeams.append(next)
                    grid[ny][nx] = timelines.get(nx, 0)
                    # don't change timelines for nx, just carry forward
                elif grid[ny][nx] == "^":
                    bx = nx - 1
                    if ingrid(grid, (ny, bx)):
                        newbeams.append((ny, bx))
                        # add the number of ways to reach nx- from the number of ways to reach nx
                        timelines[bx] = timelines.get(bx, 0) + timelines.get(nx, 0)
                        grid[ny][bx] = timelines.get(bx, 0)
                    bx = nx + 1
                    if ingrid(grid, (ny, bx)):
                        newbeams.append((ny, bx))
                        # add the number of ways to reach nx+1 from the number of ways to reach nx
                        timelines[bx] = timelines.get(bx, 0) + timelines.get(nx, 0)
                        grid[ny][bx] = timelines.get(bx, 0)
                    timelines[nx] = 0
        beams = newbeams
        step += 1
        # print(f"After step: {beams=}")
    # display(grid)
    return sum(timelines.values())


# Tests
def test_part1():
    assert part1(TESTDATA) == 21


def test_part2():
    assert part2(TESTDATA[:]) == 40


if __name__ == "__main__":
    data = splittedinput(2025, "07", sep=1)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
