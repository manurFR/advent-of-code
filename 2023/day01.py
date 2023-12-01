from pprint import pprint
from utils import readinput

mapping = {'one': 1,
           'two': 2,
           'three': 3,
           'four': 4,
           'five': 5,
           'six': 6,
           'seven': 7,
           'eight': 8,
           'nine': 9}

def extract_digits(lines):
    return [[char for char in line if char.isdigit()] for line in lines]

def compute_calibrations(strings_digits):
    # si un seul chiffre, il sera doublé -- c'est la spec...
    return [10 * int(digits[0]) + int(digits[-1]) for digits in strings_digits]

data = readinput("day01")
print(f"Part one: {sum(compute_calibrations(extract_digits(data)))}")

def replace_text_numbers(line):
    """Do it one digit at a time from left to right, otherwise it fails because of cases like '...eightwo...'"""
    for pos in range(len(line)):
        for k, v in mapping.items():
            if line[pos:].startswith(k):
                line = line.replace(k, str(v), 1)
    return line

converted_data = [replace_text_numbers(line) for line in data]

# digits = extract_digits(converted_data)
# calibs = compute_calibrations(digits)
# for o, t, d, c in list(zip(data, converted_data, digits, calibs))[:20]:
    # print(o, t, d, c)

print(f"Part two: {sum(compute_calibrations(extract_digits(converted_data)))}")