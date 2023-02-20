import string
import sys

from utils import readinput

data = readinput("day03")


def priority(item):
    """ ord('a') = 97  => 1
        ord('z') = 122 => 26
        ord('A') = 65  => 27
        ord('Z') = 90  => 52
    """
    assert item in string.ascii_letters
    if item in string.ascii_lowercase:
        return ord(item) - 96
    if item in string.ascii_uppercase:
        return ord(item) - 38


total_priorities = 0
for line in data:
    if len(line) % 2 == 1:
        print(f"bad: {line} {len(line)}")
        sys.exit(1)
    comp1 = set(line[:len(line)//2])
    comp2 = set(line[len(line)//2:])
    intersection = comp1.intersection(comp2)
    if len(intersection) != 1:
        print(f"<1> not 1 common item: {intersection}")
    common_item = intersection.pop()
    total_priorities += priority(common_item)
print(f"Part one: {total_priorities}")

total_groups = 0
for idx_gp in range(0, len(data), 3):
    elf1, elf2, elf3 = set(data[idx_gp]), set(data[idx_gp + 1]), set(data[idx_gp + 2])
    intersection = elf1.intersection(elf2, elf3)
    if len(intersection) != 1:
        print(f"<2> not 1 common item: {intersection}")
    common_item = intersection.pop()
    total_groups += priority(common_item)
print(f"Part two: {total_groups}")
