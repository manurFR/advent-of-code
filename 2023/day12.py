from utils import str2intlist


test1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""".splitlines()

data = test1

for line in data:
    row, spec = line.split()
    damages = str2intlist(spec, sep=',')

    groups = []
    curr = ""
    for c in row:
        if not curr or c == curr[-1]:
            curr += c
        else:
            groups.append(curr)
            curr = c
    groups.append(curr)

    print(row, damages)
    corrected = []
    while len(corrected) < len(row):
        g = groups[0]
        if g[0] != '?':
            corrected.extend(list(g))
            groups.pop(0)
            print(corrected)
            continue
        if corrected and corrected[-1] == '#':
            corrected.append('.')
            if len(g) > 1:
                groups[0] = '?' * (len(g) - 1)
            else:
                groups.pop(0)
            print(corrected)
            continue
        assert damages
        dmg = damages.pop(0)
        if dmg <= len(g):
            corrected.extend('#' * dmg)
            print(corrected)
            if len(g) > dmg:
                groups[0] = '?' * (len(g) - dmg)
            else:
                groups.pop(0)
        else:
            corrected.extend('#' * len(g))
            print(corrected)
            groups.pop(0)
            damages.insert(0, '?' * (dmg - len(g)))
    print(''.join(corrected))