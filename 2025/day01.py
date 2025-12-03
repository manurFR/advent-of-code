from utils import readinput


TESTDATA = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""".strip().split("\n")


def turn_dial(current, direction, amount):
    if direction == "L":
        current -= amount
    elif direction == "R":
        current += amount
    return current


def part1(data):
    dial_points = [50]
    for line in data:
        direction = line[0]
        amount = int(line[1:])
        dial = turn_dial(dial_points[-1], direction, amount) % 100
        dial_points.append(dial)
    return dial_points.count(0)


def part2(data):
    dial = 50
    count_passed_zero = 0
    for line in data:
        direction = line[0]
        amount = int(line[1:])

        # each full cycle of 100 passes the zero tick once
        count_passed_zero += amount // 100

        remainder = amount % 100
        if remainder > 0:
            if direction == "R":
                if dial + remainder > 99:
                    count_passed_zero += 1
                dial = (dial + remainder) % 100
            elif direction == "L":
                if dial - remainder <= 0 and dial > 0:  # if we started from zero, we don't count it again
                    count_passed_zero += 1
                dial = (dial - remainder) % 100
        
        # if count_passed_zero <= 100:
            # print(f"{line} {dial} {count_passed_zero}")
    return count_passed_zero


# Tests


def test_part1():
    assert part1(TESTDATA) == 3


def test_part2():
    assert part2(TESTDATA) == 6
    assert part2(["R1000"]) == 10
    assert part2(["L500"]) == 5
    assert part2(["R50", "L50", "L50", "R50"]) == 2
    assert part2(["L50", "L557", "R57", "L362", "L49"]) == 11


if __name__ == "__main__":
    data = readinput(2025, "01")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
