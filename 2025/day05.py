from utils import LinkedList, inputparts, timeit

TESTDATA = [
"""
3-5
10-14
16-20
12-18
""".strip().splitlines(),
"""
1
5
8
11
17
32
""".strip().splitlines()]

TESTP2 = """
200-300
100-101
1-1
2-2
3-3
1-3
1-3
2-2
50-70
10-10
98-99
99-99
99-99
99-100
1-1
2-1
100-100
100-100
100-101
200-300
201-300
202-300
250-251
98-99
100-100
100-101
1-101
""".strip().splitlines()


@timeit
def part1(data):
    raw_ranges, ingredients = data
    ranges = [list(map(int, r.split("-"))) for r in raw_ranges]
    
    count_fresh = 0
    for ingredient in ingredients:
        value = int(ingredient)
        for r in ranges:
            if r[0] <= value <= r[1]:
                count_fresh += 1
                break
        
    return count_fresh


@timeit
def part2(data):
    raw_ranges, _ = data
    # parse ranges as list of [min, max] and sort by min value
    sorted_ranges = sorted([list(map(int, r.split("-"))) for r in raw_ranges], key=lambda rg: rg[0])
    
    # print()
    # print(f"Source ranges : {sorted_ranges}")
    
    # a linked list with pointers to nodes is ideal to loop over ranges while removing some 
    #   (dict do not allow it, lists are tricky with indices)
    lranges = LinkedList(sorted_ranges)
       
    # merge ranges that overlap or touch
    pointer = lranges.head
    while pointer is not None:
        curr_range = pointer.value
        otherpointer = pointer.next
        while otherpointer is not None:
            othermin, othermax = otherpointer.value
            if othermin <= curr_range[1] + 1:
                # overlap or touch
                curr_range[1] = max(curr_range[1], othermax)
                lranges.remove(otherpointer)
            otherpointer = otherpointer.next
        pointer = pointer.next

    ranges = lranges.to_list()
    
    # print(f"Merged source ranges into {len(ranges)} ranges:")
    # print(ranges)
                 
    total_fresh = sum(rmax - rmin + 1 for rmin, rmax in ranges)

    return total_fresh


# Tests
def test_part1():
    assert part1(TESTDATA) == 3


def test_part2():
    assert part2(TESTDATA) == 14
    assert part2([["0-100", "1-100"], None]) == 101
    assert part2([TESTP2, None]) == 202


if __name__ == "__main__":
    data = inputparts(2025, "05")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
