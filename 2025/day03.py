from utils import readinput, timeit

TESTDATA = """987654321111111
811111111111119
234234234234278
818181911112111""".strip().split("\n")


@timeit
def part1(data):
    outputs = []
    for bank in data:
        first = max(bank[:-1])
        pos_first = bank.index(first)
        last = max(bank[pos_first + 1:])
        joltage = int(f"{first}{last}")
        outputs.append(joltage)
    return sum(outputs)
    

@timeit
def part2(data):
    size = 12
    outputs = []
    for bank in data:
        joltage = []
        currpos = 0
        for i in range(size, 0, -1):  # 12 to 1
            segment = bank[currpos:-i + 1] if i != 1 else bank[currpos:]
            digit = max(segment)
            joltage.append(digit)
            # print(f"{i=}, {currpos=}, {segment=}, joltage={"".join(joltage)}")
            currpos += segment.index(digit) + 1
        outputs.append(int("".join(joltage)))
    
    return sum(outputs)


# Tests
def test_part1():
    assert part1(TESTDATA) == 357


def test_part2():
    assert part2(TESTDATA) == 3121910778619


if __name__ == "__main__":
    data = readinput(2025, "03")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
