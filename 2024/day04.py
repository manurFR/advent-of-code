from utils import DIRECTIONS, NE, NW, SE, SW, clockwise, fwd, ingrid, splittedinput

TESTDATA = list(map(list, """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip().splitlines()))


def find_word(data, word, startpos, dirn):
    """Given a startpos (y, x), return True if 'word' is starting at startpos and is present following direction dir"""
    starty, startx = startpos
    # startpos doesn't hold the first character of word
    if not word or data[starty][startx] != word[0]:
        return False
    for step in range(1, len(word)):
        newy, newx = fwd(startpos, dirn, step)
        # word doesn't fit grid in that direction
        if not ingrid(data, (newy, newx)):
            return False
        # the letter is not the expected one
        if data[newy][newx] != word[step]:
            return False
    return True


def part1(data):
    count_XMAS = 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            for dirn in DIRECTIONS:
                if char == 'X' and find_word(data, "XMAS", (y, x), dirn):
                    count_XMAS += 1
    return count_XMAS


def part2(data):
    count_X_MAS = 0
    obliques = [NE, SE, SW, NW]
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            for dirn in obliques:
                if char == 'M' and find_word(data, "MAS", (y, x), dirn):
                    # the reciprocal MAS forming the cross can be either 90° clockwise or anti-clockwise
                    clock, anti = clockwise(dirn, 2), clockwise(dirn, -2)
                    # the 'A' is always the center of rotation
                    dy, dx = dirn
                    posA = (y + dy, x + dx)
                    # if this is an X-MAS, the other branch MUST have the following properties:
                    #  - starts either one step clock or anti from the A
                    #  - runs in the opposite direction
                    clockwiseM, anticlockM = fwd(posA, clock), fwd(posA, anti)
                    if ((ingrid(data, clockwiseM) and find_word(data, "MAS", clockwiseM, anti)) or
                        (ingrid(data, anticlockM) and find_word(data, "MAS", anticlockM, clock))):
                        count_X_MAS += 1
    # each cross had been counted twice, so divide by 2
    return count_X_MAS // 2


# Tests
def test_part1():
    assert part1(TESTDATA) == 18


def test_part2():
    assert part2(TESTDATA) == 9


if __name__ == "__main__":
    data = splittedinput(2024, "04", sep=1)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")