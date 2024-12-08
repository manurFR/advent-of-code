import itertools
import operator
from utils import convert, splittedinput, timeit

TESTDATA = [line.split() for line in """
3267: 81 40 27
190: 10 19
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip().splitlines()]


def find_valid_calibrations(data, operators):
    # [(<test value>, <numbers>), ...]
    equations = [(int(eq[0].rstrip(':')), convert(eq[1:], int)) for eq in data]

    total_calibration = 0
    for test_val, numbers in equations:
        nb_operators = len(numbers) - 1
        # for example if nb_operators = 3, this generates all possibilies : +++, ++*, +**, +*+, ***, **+, *++, *+*
        combinations = itertools.product(*([operators] * nb_operators)) 
        for comb_ops in combinations:
            curr = numbers[0]
            # curr will hold the intermediate value of applying the current operator to the previous curr 
            #   and the new number ; each curr will be kept in a list, only the last one (the final total)
            #   is interesting to us
            # PS: couldn't make this work with reduce()... :( thankfully the walrus operator saved the day
            total = [curr := op(curr, numbers[idx + 1]) for idx, op in enumerate(comb_ops)][-1]
            if total == test_val:
                total_calibration += total
                break

    return total_calibration


def part1(data):
    operators = (operator.add, operator.mul)
    return find_valid_calibrations(data, operators)


@timeit
def part2(data):
    operators = (operator.add, operator.mul, lambda a, b: int(str(a) + str(b)))
    return find_valid_calibrations(data, operators)


# Tests
def test_part1():
    assert part1(TESTDATA) == 3749


def test_part2():
    assert part2(TESTDATA) == 11387


if __name__ == "__main__":
    data = splittedinput(2024, "07")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
