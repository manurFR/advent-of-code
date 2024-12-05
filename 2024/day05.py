from collections import defaultdict
from pprint import pprint
from utils import inputparts, str2intlist


def verify(ordering: dict[int, list[int]], idxcurr: int, update: list[int]) -> bool:
    """Considering rules specified by 'ordering', this check if the item of index 'idxcurr' 
       is valid in the given 'update'.
       If the value at 'idxcurr' is an integer N
       - The values before idxcurr should NOT be in the list of values expected after, 
          ie. the list key N points to in 'ordering'
       - The values after idxcurr should NOT be in the list of values expected before,
          ie. the keys that point to a list containing N in 'ordering'
       example:
       ordering = {12: [48, 53], 32: [12]} => an item 12 should not have 48 or 53 before it 
                                              and should not have 32 after
    """
    assert 0 <= idxcurr < len(update)
    val = update[idxcurr]
    # check values before
    if idxcurr > 0:
        expected_after = ordering.get(val, [])
        if any(after for after in expected_after if after in update[:idxcurr]):
            return False
    # check values after
    if idxcurr < len(update) - 1:
        expected_before = [before for before, afters in ordering.items() for after in afters if after == val]
        if any(before for before in expected_before if before in update[idxcurr + 1:]):
            return False
    return True


def is_correct(update, ordering):
    return all(verify(ordering, idxcurr, update) for idxcurr in range(len(update)))


def sum_of_middle(updates):
    assert all(len(upd) % 2 == 1 for upd in updates)  # all updates should contain an odd number of pages
    return sum(upd[len(upd) // 2] for upd in updates)


def part1(data):
    raw_rules, raw_updates = data
    rules = [str2intlist(r, '|') for r in raw_rules]
    updates = [str2intlist(u, ',') for u in raw_updates]

    # {<before>: [<after>, <after>, ...]}
    ordering = defaultdict(list)
    for before, after in rules:
        ordering[before].append(after)
    # pprint(ordering)

    correct_updates = [upd for upd in updates if is_correct(upd, ordering)]

    # all updates should contain an odd number of pages
    assert all(len(cu) % 2 == 1 for cu in correct_updates)

    return sum_of_middle(correct_updates), \
           {"updates": updates, "ordering": ordering, "correct_updates": correct_updates}


def part2(context):
    updates = context["updates"]
    ordering = context["ordering"]
    correct_updates = context["correct_updates"]

    incorrect_updates = [upd for upd in updates if upd not in correct_updates]

    for upd in incorrect_updates:
        while not is_correct(upd, ordering):
            for before, afters in ordering.items():
                for after in afters:
                    if before in upd and after in upd:
                        if (idx_before := upd.index(before)) > (idx_after := upd.index(after)):
                            upd[idx_before] = after
                            upd[idx_after] = before

    return sum_of_middle(incorrect_updates)


# Tests
def test_part1():
    data = inputparts(2024, "05-test")
    assert part1(data)[0] == 143


def test_part2():
    data = inputparts(2024, "05-test")
    _, context = part1(data)
    assert part2(context) == 123


def test_verify():
    assert verify(ordering={1: [2, 3], 2: [4, 5], 3: [5], 4: [8]}, idxcurr=2, update=[1, 2, 3, 4, 5]) is True
    assert verify(ordering={1: [2, 3], 2: [4, 5], 3: [5], 4: [8]}, idxcurr=2, update=[1, 2, 8, 4, 5]) is False
    assert verify(ordering={1: [2, 3], 2: [4, 5], 3: [5], 4: [8]}, idxcurr=2, update=[1, 4, 2, 3, 5]) is False


def test_sum_of_middle():
    assert sum_of_middle([[1, 2, 3], [4, 5, 6, 7, 8], [7, 10, 99]]) == 18


if __name__ == "__main__":
    data = inputparts(2024, "05")
    res_p1, context = part1(data)
    print(f"Part 1: {res_p1}")
    print(f"Part 2: {part2(context)}")
