from itertools import pairwise
from utils import convert, splittedinput

TESTDATA = [convert(line.split(), int) for line in """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip().split("\n")]


def is_safe(report):
    # pairwise([1, 2, 3, 4]) == [(1, 2), (2, 3), (3, 4)]
    return all(prv < nxt and 0 < nxt - prv <= 3 for prv, nxt in pairwise(report)) or \
           all(prv > nxt and 0 < prv - nxt <= 3 for prv, nxt in pairwise(report))


def part1(data):
    safe_reports = [report for report in data if is_safe(report)]
    return len(safe_reports)


def part2(data):
    safe_reports = []
    for report in data:
        if is_safe(report):
            safe_reports.append(report)
        else:
            for idx in range(len(report)):
                dampened = report[0:idx] + report[idx + 1:]  # the report without the idx-th element
                if is_safe(dampened):
                    safe_reports.append(dampened)
                    break
        
    return len(safe_reports)


# Tests
def test_is_safe():
    assert is_safe([1, 3, 4, 7, 8]) is True
    assert is_safe([12, 10, 8, 5, 4, 3]) is True
    
    assert is_safe([2, 3, 4, 5, 4, 3]) is False
    assert is_safe([2, 3, 4, 4, 6]) is False
    assert is_safe([5, 10, 15, 20]) is False
    assert is_safe([66, 64, 62, 1]) is False


def test_part1():
    assert part1(TESTDATA) == 2


def test_part2():
    assert part2(TESTDATA) == 4


if __name__ == "__main__":
    data = splittedinput(2024, "02", conv=int)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")