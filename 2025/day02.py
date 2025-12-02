from utils import readinput, timeit


def prepare(data) -> list[tuple[str, str]]:
    return [item.split("-") for item in data]


TESTDATA = prepare(("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,"
                    "38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124").split(","))


@timeit
def part1(data):
    """An invalid ID is "any ID which is made only of some sequence of digits repeated twice".
       like 11 or 446446.
       The max length of the sequence (called digits here) is half the length of the longest lastid in the input data."""
    maxlen = max(len(lastid) for _, lastid in data) // 2
    
    invalid_ids = []
    
    # take any integer from 1 to 99 or 999 or 9999 etc with a number of digits 9 equal to maxlen
    for i in range(1, 10**maxlen):
        digits = str(i) + str(i)  # build the possible invalid ID by repeating the digits twice
        for firstid, lastid in data:  # for each range...
            if int(firstid) <= int(digits) <= int(lastid):  # ...check if the invalid ID is in the range
                invalid_ids.append(int(digits))
                break
    
    return sum(invalid_ids)


@timeit
def part2(data):
    invalid_ids = []
    
    for firstid, lastid in data:
        # for each range, loop over every ID in the range...
        for pid in range(int(firstid), int(lastid) + 1):
            stri = str(pid)
            # since the repeated sequence must be at least twice, it's maximum length is len(stri) // 2
            #  ...loop over every possible length for the repeated sequence
            for digits_size in range(1, len(stri) // 2 + 1):
                digits = stri[:digits_size]  # take the first characters in the ID of the size of the sequence we're testing
                if stri == digits * (len(stri) // digits_size):  # check if the whole ID is made of the sequence repeated N times
                    invalid_ids.append(pid)
                    break
                
    return sum(invalid_ids)
            

# Tests
def test_part1():
    assert part1(TESTDATA) == 1227775554


def test_part2():
    assert part2(TESTDATA) == 4174379265


if __name__ == "__main__":
    data = prepare(readinput(2025, "02")[0].split(","))
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
