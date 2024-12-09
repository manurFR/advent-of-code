from collections import defaultdict
import copy
import itertools
from pprint import pprint
from utils import display, ingrid, splittedinput, timeit

TESTDATA = [[c for c in line] for line in """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip().splitlines()]


def get_antennas(data):
    antennas = defaultdict(list)  # {<name>: [<coord1>, ...]}
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] != '.':
                antennas[data[y][x]].append((y, x))
    return antennas


@timeit
def part1(data):
    antennas = get_antennas(data)

    # display(data)
    # pprint(antennas)

    antinodes = set()
    for letter in antennas:
        for ant1, ant2 in itertools.combinations(antennas[letter], 2):
            dy = ant2[0] - ant1[0]
            dx = ant2[1] - ant1[1]
            antinode1 = (ant1[0] - dy, ant1[1] - dx)
            antinode2 = (ant2[0] + dy, ant2[1] + dx)
            if ingrid(data, antinode1):
                antinodes.add(antinode1)
            if ingrid(data, antinode2):
                antinodes.add(antinode2)

    return len(antinodes)


@timeit
def part2(data):
    antennas = get_antennas(data)
    max_step = len(data)

    antinodes = set()
    for letter in antennas:
        for ant1, ant2 in itertools.combinations(antennas[letter], 2):
            # antinodes.add(ant1)
            # antinodes.add(ant2)
            dy = ant2[0] - ant1[0]
            dx = ant2[1] - ant1[1]
            for step in range(-max_step, max_step + 1):
                antinode = (ant1[0] - step * dy, ant1[1] - step * dx)
                if ingrid(data, antinode):
                    antinodes.add(antinode)
    
    # grid = copy.deepcopy(data)
    # for anode in antinodes:
    #     grid[anode[0]][anode[1]] = '#'
    # display(grid)

    return len(antinodes)


# Tests
def test_part1():
    assert part1(TESTDATA) == 14


def test_part2():
    assert part2(TESTDATA) == 34


if __name__ == "__main__":
    data = splittedinput(2024, "08", sep=1)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
