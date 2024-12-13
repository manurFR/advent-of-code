from pprint import pprint
from utils import EAST, NORTH, SOUTH, WEST, breadth_first_search, display, fwd, ingrid, splittedinput, timeit

### This works on TESTDATA but not on real data... I give up today ;)

TESTDATA = [[c for c in line] for line in """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".strip().splitlines()]


@timeit
def part1(data):
    visited_plots = set()
    region = set()

    def adjacencyrule(grid, currpos):
        region.add(currpos)
        nextpositions = []
        for dirn in (NORTH, EAST, SOUTH, WEST):
            nextpos = fwd(currpos, dirn)
            if ingrid(grid, nextpos) and nextpos not in region:
                nextpositions.append(nextpos)
        return nextpositions
    
    # display(data)
    
    regions = []
    for y in range(len(data)):
        for x in range(len(data[y])):
            if (y, x) not in visited_plots:
                plant = data[y][x]

                def endrule(grid, currpos):
                    return grid[currpos[0]][currpos[1]] != plant

                # endrule can only detect when we're already out of a region, so don't include it (include_tail=False)
                breadth_first_search(data, (y, x), adjacencyrule, endrule, include_head=False)
                regions.append(sorted(list(region)))
                visited_plots |= region
                region = set()

    prices = []
    for reg in regions:
        plot = reg[0]
        plant = data[plot[0]][plot[1]]
        frontiers = 0
        for plot in reg:
            for dirn in (NORTH, EAST, SOUTH, WEST):
                nextpos = fwd(plot, dirn)
                if not ingrid(data, nextpos) or data[nextpos[0]][nextpos[1]] != plant:
                    frontiers += 1
        
        prices.append(len(reg) * frontiers)
        # print(plot, plant, reg, frontiers)

    return sum(prices)


@timeit
def part2(data):
    return 0


# Tests
def test_part1():
    assert part1(TESTDATA) == 1930


def test_part2():
    assert part2(TESTDATA) == 0


if __name__ == "__main__":
    data = splittedinput(2024, "12", sep=1)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
