import copy
from utils import NORTH, clockwise, display, find, fwd, ingrid, splittedinput, timeit

TESTDATA = [[c for c in line] for line in """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".strip().splitlines()]


def explore(grid, start):
    dirn = NORTH
    curry, currx = start
    path = [(curry, currx, dirn)]
    while True:
        nexty, nextx = fwd((curry, currx), dirn)
        if not ingrid(grid, (nexty, nextx)):
            return unique_pos(path), "out"
        if grid[nexty][nextx] in ('#', 'O'):
            dirn = clockwise(dirn, 2)
        else:
            curry, currx = nexty, nextx
        if (curry, currx, dirn) in path:
            return unique_pos(path), "loop"
        path.append((curry, currx, dirn))


def part1(data):
    start = find(data, "^")[0]
    path, status = explore(data, start)
    assert status == "out"
    return path


def unique_pos(path):
    # set() in order to count only once the positions where the guard passed multiple times
    return set((y, x) for y, x, _ in path)


@timeit
def part2(data, path):  # 350 seconds, lol...
    steps = len(path)
    start = find(data, "^")[0]
    options = set()
    for idx, (curry, currx) in enumerate(path):
        if (idx + 1) % 100 == 0:
            print(f"{idx + 1} / {steps}")
        gridcopy = copy.deepcopy(data)
        gridcopy[curry][currx] = 'O'
        _, status = explore(gridcopy, start)
        if status == "loop":
            options.add((curry, currx))
    return len(options)


# Tests
def test_part1():
    assert len(part1(TESTDATA)) == 41


def test_part2():
    path = part1(TESTDATA)
    assert part2(TESTDATA, path) == 6

if __name__ == "__main__":
    data = splittedinput(2024, "06", sep=1)
    path = part1(data)
    print(f"Part 1: {len(path)}")
    print(f"Part 2: {part2(data, path)}")