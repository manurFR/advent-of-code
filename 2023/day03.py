from pprint import pprint
from utils import readinput


data = readinput("day03")

# data = [
    # '...*..120....',
    # '.562....#64..',
    # '33........$18',
    # '.489......55#',
    # '...24*896....'
# ]

# data = [
    # '467..114..',
    # '...*......',
    # '..35..633.',
    # '......#...',
    # '617*......',
    # '.....+.58.',
    # '..592.....',
    # '......755.',
    # '...$.*....',
    # '.664.598..' 
# ]

engine = [[char for char in line] for line in data]

def is_adjacent(number_coords, symbol_coords):
    row, startx, endx = number_coords # 138, 11, 15
    symb_row, symb_x = symbol_coords  # 138, 14
    return (
        # adjacent on previous row, including diagonically
        (symb_row == row - 1 and symb_x >= startx - 1 and symb_x <= endx) or
        # adjacent on same row, previous and next characters
        (symb_row == row and (symb_x == startx - 1 or symb_x == endx)) or
        # adjacent on new row, including diagonically
        (symb_row == row + 1 and symb_x >= startx - 1 and symb_x <= endx)
    )

def find_parts(numbers, symbols):
    part_numbers = []
    for number, number_coords in numbers:
        for _, symbol_coords in symbols:
            if is_adjacent(number_coords, symbol_coords):
                part_numbers.append(number)
                break
    return part_numbers

def find_gears(numbers, symbols):
    ratios = []
    for symbol, symbol_coords in symbols:
        if symbol != '*':
            continue
        part_numbers = []
        # print(symbol, symbol_coords)
        for number, number_coords in numbers:
            # consider only the numbers on the rows above, below or the same row as the gear
            if number_coords[0] < symbol_coords[0] - 1 or number_coords[0] > symbol_coords[0] + 1:
                continue
            # print(number, number_coords)
            if is_adjacent(number_coords, symbol_coords):
                part_numbers.append(number)
        # print(part_numbers)
        if len(part_numbers) == 2:
            # print(f"{part_numbers[0]} * {part_numbers[1]}")
            ratios.append(part_numbers[0] * part_numbers[1])
    return ratios


numbers = []  # [(number, (row, startx, endx))]
symbols = []  # [(<symbol>, (row, x)), ...]

for y in range(len(engine)):
    digits = None
    startx = None
    for x in range(len(engine[0])):
        if engine[y][x].isdigit():
            if digits:
                digits.append(engine[y][x])
            else:
                digits = [engine[y][x]]
                startx = x
        else:
            if digits:  # a number just ended
                numbers.append((int(''.join(digits)), (y, startx, x)))
                digits = None
                startx = None
            if engine[y][x] != '.' and not engine[y][x].isspace():  # found a symbol
                symbols.append((engine[y][x], (y, x)))
    if digits:  # we reached the end of a row and a number just ended
        numbers.append((int(''.join(digits)), (y, startx, x)))

# print("numbers")
# pprint(numbers)
# print("symbols")
# pprint(symbols)

part_numbers = find_parts(numbers, symbols)
gear_ratios = find_gears(numbers, symbols)
# pprint(numbers)

# print(part_numbers)
print(f"Part one: {sum(part_numbers)}")
# print(gear_ratios)
print(f"Part two: {sum(gear_ratios)}")
