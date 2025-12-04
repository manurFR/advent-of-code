from utils import DIRECTIONS, display, fwd, ingrid, splittedinput, timeit

TESTDATA = [[c for c in line] for line in """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip().splitlines()]


def find_accessible_rolls(data: list[list[str]]) -> list[tuple[int, int]]:
    copydata = [row[:] for row in data]
    list_rolls_accessible = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] != '@':
                continue
            count_rolls_around = 0
            for dirn in DIRECTIONS:
                cy, cx = fwd((y, x), dirn)
                if ingrid(data, (cy, cx)) and data[cy][cx] == '@':
                    count_rolls_around += 1
            if count_rolls_around < 4:
                list_rolls_accessible.append((y, x))
                copydata[y][x] = 'x'
    # display(copydata)
    
    return list_rolls_accessible

    
@timeit
def part1(data):
    list_rolls_accessible = find_accessible_rolls(data)
    
    return len(list_rolls_accessible)


@timeit
def part2(data):
    total_removed = 0
    while True:
        list_rolls_accessible = find_accessible_rolls(data)
        if not list_rolls_accessible:
            break
        for y, x in list_rolls_accessible:
            data[y][x] = '.'
        total_removed += len(list_rolls_accessible)
    
    return total_removed


# Tests
def test_part1():
    assert part1(TESTDATA) == 13


def test_part2():
    assert part2(TESTDATA) == 43


if __name__ == "__main__":
    data = splittedinput(2025, "04", sep=1)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
