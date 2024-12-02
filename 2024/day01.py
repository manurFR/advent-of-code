import os
import pytest
from utils import splittedinput

# Part 1
def part1(data):
    left, right = zip(*data)
    left = sorted(int(n) for n in left)
    right = sorted(int(n) for n in right)
    return sum(abs(litem - ritem) for litem, ritem in zip(left, right))


# Tests
def test_part1():
    data = [line.split() for line in """
3   4
4   3
2   5
1   3
3   9
3   3
""".strip().split("\n")]
    assert part1(data) == 11


if __name__ == "__main__":
    pytest.main(["-q", "2024/" + os.path.basename(os.path.abspath(__file__))])

    data = splittedinput(2024, "01")
    print(f"Part 1: {part1(data)}")
