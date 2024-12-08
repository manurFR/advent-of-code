from utils import splittedinput

TESTDATA = [line.split() for line in """
...
""".strip().splitlines()]


def part1(data):
    return 0


def part2(data):
    return 0


# Tests
def test_part1():
    assert part1(TESTDATA) == -1


def test_part2():
    assert part2(TESTDATA) == 0


if __name__ == "__main__":
    data = splittedinput(0000, "XX")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
