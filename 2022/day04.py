from utils import splittedinput

data = splittedinput("day04", ',')

assignments = []
for elf1, elf2 in data:
    elf1min, elf1max = elf1.split('-')
    elf2min, elf2max = elf2.split('-')
    assignments.append((range(int(elf1min), int(elf1max)+1), range(int(elf2min), int(elf2max)+1)))
# pprint(assignments)

fully_contains_pairs = [(elf1, elf2) for elf1, elf2 in assignments
                        if set(elf1).issubset(elf2) or set(elf2).issubset(elf1)]
print(f"Part one: {len(fully_contains_pairs)}")

overlap_pairs = [(elf1, elf2) for elf1, elf2 in assignments
                 if set(elf1).intersection(elf2)]
print(f"Part two: {len(overlap_pairs)}")

