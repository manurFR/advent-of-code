from collections import deque
from collections.abc import Callable
from pprint import pprint
from utils import EAST, NORTH, SOUTH, WEST, display, find, fwd, ingrid, splittedinput, timeit

TESTDATA = [[int(c) for c in line] for line in """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip().splitlines()]


def breadth_first_search(grid: list[list], startpos: tuple, 
                         adjacencyrule: Callable[[list[list], tuple], list[tuple]], 
                         endrule: Callable[[list[list], tuple], bool]) -> list[list]:
    """Explore the grid from a starting position and return all the valid paths.
        adjacencyrule must be a function f(grid, currpos) -> list[tuple[int, int]]
          that return, for a position currpos, return the valid next positions on the path
        endrule must be a function f(grid, currpos) -> bool that return True if the
          current position qualifies as the end point for a valid path
      IMPORTANT: this function returns ALL the valid paths that lead from the starting
       position to an end point. If you need only the unique end points, apply a set() on them.
    """
    winpaths = []
    visited = set()
    queue = deque()

    queue.append((startpos, [startpos]))  # current_vertex, path

    while queue:
        currpos, path = queue.popleft()
        visited.add(currpos)

        if endrule(grid, currpos):
            winpaths.append(path)

        for nextpos in adjacencyrule(grid, currpos):
            # not: no "if nextpos not in visited" in this implementation, we return ALL valid paths
            visited.add(nextpos)
            queue.append((nextpos, path + [nextpos]))

    return winpaths


def endrule(grid, currpos):
    y, x = currpos
    return grid[y][x] == 9


def adjacencyrule(grid, currpos):
    currheight = grid[currpos[0]][currpos[1]]
    nextpositions = []
    for dirn in (NORTH, EAST, SOUTH, WEST):
        nextpos = fwd(currpos, dirn)
        ny, nx = nextpos
        if ingrid(grid, nextpos) and grid[ny][nx] == currheight + 1:
            nextpositions.append(nextpos)
    return nextpositions


@timeit
def part1(data):
    trailheads = find(data, 0)
    # display(data)

    score = 0

    for thead in trailheads:
        goodtrails = breadth_first_search(data, thead, adjacencyrule, endrule)
        
        # print(thead)
        # for trail in goodtrails:
            # print(' '.join(f"{pos}>{data[pos[0]][pos[1]]}" for pos in trail))
        # print("------")

        tops = set(trail[-1] for trail in goodtrails)  # make unique
        score += len(tops)

    return score


@timeit
def part2(data):
    trailheads = find(data, 0)

    score = 0

    for thead in trailheads:
        goodtrails = breadth_first_search(data, thead, adjacencyrule, endrule)

        # don't make them unique
        score += len(goodtrails)

    return score


# Tests
def test_part1():
    assert part1(TESTDATA) == 36


def test_part2():
    assert part2(TESTDATA) == 81


if __name__ == "__main__":
    data = splittedinput(2024, "10", sep=1, conv=int)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
