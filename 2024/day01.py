from collections import Counter

from utils import splittedinput

TESTDATA = [line.split() for line in """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip().split("\n")]

def parselists(data):
    left, right = zip(*data)
    left = sorted(int(n) for n in left)
    right = sorted(int(n) for n in right)
    return left, right


# Part 1
def part1(data):
    left, right = parselists(data)
    return sum(abs(litem - ritem) for litem, ritem in zip(left, right))


def part2(data):
    left, right = parselists(data)
    counter_right = Counter(right)
    return sum(n * counter_right[n] for n in left)


# Tests
def test_part1():
    assert part1(TESTDATA) == 11


def test_part2():
    assert part2(TESTDATA) == 31


if __name__ == "__main__":
    data = splittedinput(2024, "01")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
