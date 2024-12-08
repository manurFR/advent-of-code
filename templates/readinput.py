from utils import readinput, timeit

TESTDATA = """some
data"""


@timeit
def part1(data):
    return 0


@timeit
def part2(data):
    return 0


# Tests
def test_part1():
    assert part1(TESTDATA) == -1


def test_part2():
    assert part2(TESTDATA) == 0


if __name__ == "__main__":
    data = readinput(0000, "XX")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
