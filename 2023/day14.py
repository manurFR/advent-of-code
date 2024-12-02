from copy import deepcopy
from utils import readinput

test = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".splitlines()

# data = test
data = readinput(2023, 'day14')

data = [[c for c in row] for row in data]

def tilt(platform):  # to the NORTH
    for y in range(len(platform) - 1):
        for x in range(len(platform[0])):
            if platform[y][x] == '.':
                for uphill in range(y + 1, len(platform)):
                    if platform[uphill][x] == '#':
                        break
                    elif platform[uphill][x] == 'O':
                        platform[y][x] = 'O'
                        platform[uphill][x] = '.'
                        break

def compute_loads(platform):
    loads = []
    for y in range(len(platform)):
        unit_load = len(platform) - y
        for x in range(len(platform[0])):
            if platform[y][x] == 'O':
                loads.append(unit_load)
    return loads

def rotate(platform):
    """Rotate the platform 90° clockwise (so that WEST is now NORTH and so on)"""
    rotated_platform = []
    for x in range(len(platform[0])):
        rotated_line = [platform[y][x] for y in range(len(platform) - 1, -1, -1)]
        rotated_platform.append(rotated_line)
    return rotated_platform

def cycle(platform):
    for _ in range(4):
        tilt(platform)
        platform = rotate(platform)
    return platform

print('\n'.join(''.join(row) for row in data))

platform1 = deepcopy(data)

tilt(platform1)

print()
# print('\n'.join(''.join(row) for row in platform1))

loads1 = compute_loads(platform1)
# print(loads)

print(f"Part one: {sum(loads1)}")

# print('\n'.join(''.join(row) for row in rotate(data)))

platform2 = deepcopy(data)
# print('\n'.join(''.join(row) for row in platform2))
# print()

# A un moment, ca boucle, çàd ça revient à une position précédente après un cycle entier.
# Trouvons le moment exact où on reboucle sur une position déjà rencontrée.
keep = [deepcopy(platform2)]
while platform2 not in keep[:-1]:
    platform2 = cycle(platform2)
    keep.append(deepcopy(platform2))

# Maintenant on peut déterminer quand le cycle a commencé (à quelle itération on a rencontré
#  pour la première fois la position qu'on vient de retrouver)
start_cycle = keep[:-1].index(keep[-1])
# Et donc la longueur du cycle
cycle_freq = len(keep) - start_cycle - 1

print(f"{start_cycle=} {cycle_freq=}")

# Si on fait 50 cycles en tout, avec len(cycle)=11 start_cycle=3 et cycle_freq=7, la dernière fois qu'on 
# va retomber sur la position de début de cycle est l'index 10->17->24->31->38->45
# Le dernier cycle nous amène à l'index 49 (car on a commencé à 0) donc 49 - 45 = +4 après start_cycle
# Position de début du dernier cycle : NbTotalCycles - (len(keep) - 1)
# Donc le nb de steps en plus est obtenue en prenant le reste de la division par cycle_freq
surplus_steps = (1000000000 - (len(keep) - 1)) % cycle_freq

last_cycle = start_cycle + surplus_steps
last_platform2 = keep[last_cycle]

loads_part2 = compute_loads(last_platform2)
print(f"Part two: {sum(loads_part2)}")