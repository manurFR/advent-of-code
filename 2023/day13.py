from copy import deepcopy
import sys
from utils import inputparts

test = ["""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.""".splitlines(),
"""#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()]

# data = test
data = inputparts('day13')

def detect_vertical(ptrn, exclude=None):
    for mid in range(1, len(ptrn)):  # try symmetry at rows 1, 2, ..., len-1
        if exclude and mid == exclude:
            continue
        # if mid is close to the top or bottom, the other half of the symmetry is truncated, so take only the visible part
        t_size = min(mid, len(ptrn) - mid)
        if ptrn[mid - t_size : mid] == list(reversed(ptrn[mid : mid + t_size])):
            return mid
    return 0

def find_lines(ptrn, exclude=None):
    # horizontal : rotate the grid to test in vertical
    rotated_pattern = []
    for x in range(len(ptrn[0])):
        rotated_line = [ptrn[y][x] for y in range(len(ptrn) - 1, -1, -1)]
        rotated_pattern.append(''.join(rotated_line))

    # print('\n'.join(pattern))
    # print()
    # print(detect_vertical(h_pattern))
    # print(detect_vertical(pattern))
    # print("--")
    horiz_line = detect_vertical(rotated_pattern, exclude=exclude[0] if exclude else None)
    vert_line = detect_vertical(ptrn, exclude=exclude[1] if exclude else None)
    return horiz_line, vert_line


scores = []
scores_smudges = []
for pattern in data:
    h_line, v_line = find_lines(pattern)
    if v_line > 0:
        scores.append(100 * v_line)
    else:
        scores.append(h_line)
    # print('\n'.join(pattern))
    # print("------------------")

    for y in range(len(pattern)):
        found = False
        for x in range(len(pattern[0])):
            smudged = deepcopy(pattern)
            smudged[y] = smudged[y][0:x] + ('#' if smudged[y][x] == '.' else '.') + smudged[y][x+1:]
            # print('\n'.join(smudged))
            # print()
            h_smudged, v_smudged = find_lines(smudged, exclude=(h_line, v_line))
            if v_smudged > 0 and v_smudged != v_line:
                scores_smudges.append(100 * v_smudged)
                found = True
                break
            elif h_smudged > 0 and h_smudged != h_line:
                scores_smudges.append(h_smudged)
                found = True
                break
        if found:
            break
    else:
        print("problem!")

# print(scores)
print(f"Part one: {sum(scores)}")

# print(len(scores), len(scores_smudges))
# print(scores_smudges)
print(f"Part one: {sum(scores_smudges)}")
