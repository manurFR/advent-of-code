import re
from utils import readinput

TESTDATA = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

PATTERN = re.compile(r"(mul|do|don't)\((?:(\d{1,3}),(\d{1,3}))?\)")


def part1(data):
    return sum(int(m[2]) * int(m[3]) for m in PATTERN.finditer(data) if m[1] == "mul")


def part2(data):
    total = 0
    enabled = True
    for m in PATTERN.finditer(data):
        match m[1]:
            case "mul" if enabled:
                total += int(m[2]) * int(m[3])
            case "do":
                enabled = True
            case "don't":
                enabled = False
    return total


# Tests
def test_part1():
    assert part1(TESTDATA) == 161


def test_part2():
    assert part2(TESTDATA) == 48


if __name__ == "__main__":
    rawdata = readinput(2024, "03")
    data = ''.join(rawdata)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
