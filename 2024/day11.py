from collections import Counter
import copy
from functools import cache
import itertools
from time import perf_counter
from utils import splittedinput, timeit

TESTDATA = [[125, 17]]


@cache
def blinkstone(stone: int) -> tuple[int, ...]:
    """For one stone only"""
    if stone == 0:
        return (1,)
    strstone = str(stone)
    if len(str(strstone)) % 2 == 0:
        middle = len(strstone) // 2
        return int(strstone[:middle]), int(strstone[middle:])
    return (stone * 2024,)


def blink(stones: tuple[int, ...]) -> tuple[int, ...]:
    res = []
    for stone in stones:
        res.extend(blinkstone(stone))
    return tuple(res)

        
@cache
def blink25times(stones: tuple[int, ...]) -> tuple[int, ...]:
    for _ in range(25):
        stones = blink(stones)
    return stones


@timeit
def part1(data: list[list[int]], nb_blinks: int):
    stones = tuple(data[0])

    for _ in range(nb_blinks):
        stones = blink(stones)
            
    return stones


def summary(tstart, tnow, step, totalsteps, suffix=None):
    print(f" cache1: {blinkstone.cache_info().currsize} | cache25: {blink25times.cache_info().currsize} "
          f"| ETA: {(tnow - tstart) / step * (totalsteps - step) / 60:.3f} min{f' | {suffix}' if suffix else ''}")


@timeit
def part2(data, nb_blinks, chunksize):
    stones = tuple(data[0])

    stones_pass1 = blink25times(stones)
    stones_pass2 = []
    
    total_pass2 = 0

    tstart = perf_counter()
    nb_total = len(stones_pass1) // chunksize + 1
    for chnum, chunk in enumerate(itertools.batched(stones_pass1, chunksize)):
        chunk = blink25times(chunk)
        stones_pass2.append(chunk)
        total_pass2 += len(chunk)
        if chnum % 200 == 0:
            print(".", end="", flush=True)
            if chnum % 2000 == 0:
                t1 = perf_counter()
                summary(tstart, t1, chnum + 1, nb_total)

    t1 = perf_counter()
    summary(tstart, t1, nb_total, nb_total)
    print(f"step2 lasted: {(t1 - tstart):.3f} sec")
    print("-- step 3 --")

    totalstones = 0

    tstart = perf_counter()
    nb_total = total_pass2 // chunksize + 1
    for chnum, chunk in enumerate(itertools.batched(itertools.chain(*stones_pass2), chunksize)):
        chunk = blink25times(chunk)
        totalstones += len(chunk)
        if chnum % 500000 == 0:
            print(".", end="", flush=True)
            if chnum % 20000000 == 0:
                t1 = perf_counter()
                summary(tstart, t1, chnum + 1, nb_total, suffix=f"{totalstones = }")

    t1 = perf_counter()
    summary(tstart, t1, nb_total, nb_total)
    print(f"step3 lasted: {(t1 - tstart) / 60:.3f} min")
    print(totalstones)

    return totalstones


@timeit
def blink_with_counter(stones: list[int], nb_blinks: int) -> int:
    """Use Counters, not lists !
       Each generation is modelized with a Counter(): the key is a stone value, its count is the number of times 
       this stone happens.
    """
    cnt = Counter(stones)
    for _ in range(nb_blinks):
        new_cnt = Counter()
        for stone, qtty in cnt.items():
            newstones = blinkstone(stone)
            for s in newstones:
                new_cnt[s] += qtty
        cnt = new_cnt
    return sum(cnt.values())



# Tests
def test_part1():
    assert part1(copy.deepcopy(TESTDATA), 1) == (253000, 1, 7)
    assert part1(copy.deepcopy(TESTDATA), 2) == (253, 0, 2024, 14168)
    assert part1(copy.deepcopy(TESTDATA), 6) == (2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 
                                                 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2)
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 1) == 3
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 2) == 4
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 3) == 5
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 4) == 9
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 6) == 22


def test_part2():
    # assert part2(copy.deepcopy(TESTDATA), nb_blinks=25, chunksize=2) == 55312
    assert blink_with_counter(copy.deepcopy(TESTDATA)[0], 25) == 55312


if __name__ == "__main__":
    data = splittedinput(2024, "11", conv=int)
    print(f"Part 1: {len(part1(copy.deepcopy(data), 25))}")
    # this takes 15 minutes
    # print(f"Part 2: {part2(copy.deepcopy(data), nb_blinks=75, chunksize=2)}")
    # this takes 0.05 seconds :D (or 0.09 seconds without the @cache on blinkstone()...)
    print(f"Part 2: {blink_with_counter(copy.deepcopy(data)[0], 75)}")
