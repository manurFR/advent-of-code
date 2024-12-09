from pprint import pprint
import string
from utils import readinput, timeit

TESTDATA = ["2333133121414131402"]

FREE = "."
FILE = "F"

SYMBOLS = string.digits + string.ascii_uppercase


def displaydisk(disk, pointer):
    # print(' '.join(f"<{SYMBOLS[sid] if sid is not None else ''}>{stype}/{sid if sid is not None else ''}/{ssiz}" 
                #    for stype, sid, ssiz in disk))
    line = ''.join((SYMBOLS[sid] if stype == FILE else '.') * ssize for stype, sid, ssize in disk)
    print(f"{pointer:>2}  ", line, f"[{len(line)}]")


def checksum(disk):
    pos = 0
    chk = 0
    for space in disk:
        if space[0] == FILE:
            for i in range(space[2]):
                chk += space[1] * (pos + i)
        pos += space[2]
    return chk


def get(disk, sid):
    return [idx for idx in range(len(disk)) if disk[idx][1] == sid][-1]


def defragment(disk, only_full=False):
    curr_sid = disk[len(disk) - 1][1]
    while curr_sid > 0:
        idx_curr_sid = get(disk, curr_sid)
        _, _, spacesize = disk[idx_curr_sid]

        # displaydisk(disk, curr_sid)

        # find free-space to move the file to, starting from the beginning of the disk
        for idx_freespace in range(0, idx_curr_sid):
            if disk[idx_freespace][0] == FREE and disk[idx_freespace][2] > 0:
                # print(curr_sid, idx_freespace, disk[idx_freespace][2], "<", spacesize)
                if only_full and disk[idx_freespace][2] < spacesize:
                    continue
                break
        else:
            # no freespace found
            curr_sid -= 1
            continue

        free_blocks = disk[idx_freespace][2]

        remaining_file = max(0, spacesize - free_blocks)

        # let's free the file from its original place
        if remaining_file > 0:
            disk[idx_curr_sid] = (FILE, curr_sid, remaining_file)
            disk.insert(idx_curr_sid + 1, (FREE, None, spacesize - remaining_file))
        else:
            disk[idx_curr_sid] = (FREE, None, spacesize)

        # let's insert the file at idx_freespace, surrounded by freespaces
        disk[idx_freespace] = (FREE, None, 0)
        disk.insert(idx_freespace + 1, (FILE, curr_sid, spacesize - remaining_file))
        disk.insert(idx_freespace + 2, (FREE, None, max(0, free_blocks - spacesize)))

        if remaining_file == 0:
            curr_sid -= 1

    return disk


@timeit
def part1(data):
    # odd-indexed are file blocks ; even-indexed are free space blocks
    diskmap = [int(b) for b in data[0]]
    # [(<type>, <id file>, <nb_blocks>), ...] // type = FILE|FREE ; free-spaces get no id
    diskspace = [(FILE if idx % 2 == 0 else FREE, 
                  idx // 2 if idx % 2 == 0 else None, 
                  space) 
                  for idx, space in enumerate(diskmap)]
    
    disk = defragment(diskspace, only_full=False)

    return checksum(disk)


@timeit
def part2(data):
    # odd-indexed are file blocks ; even-indexed are free space blocks
    diskmap = [int(b) for b in data[0]]
    # [(<type>, <id file>, <nb_blocks>), ...] // type = FILE|FREE ; free-spaces get no id
    diskspace = [(FILE if idx % 2 == 0 else FREE, 
                  idx // 2 if idx % 2 == 0 else None, 
                  space) 
                  for idx, space in enumerate(diskmap)]

    disk = defragment(diskspace, only_full=True)

    return checksum(disk)


# Tests
def test_part1():
    assert part1(TESTDATA) == 1928


def test_part2():
    assert part2(TESTDATA) == 2858


if __name__ == "__main__":
    data = readinput(2024, "09")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
