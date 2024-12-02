import re
import sys
from utils import readinput

data = readinput(2023, "day02")

AVAILABLE_RED, AVAILABLE_GREEN, AVAILABLE_BLUE = 12, 13, 14

GAME_PATTERN = re.compile(r"Game (\d+): (.*)")
RED_PATTERN = re.compile(r"(\d+) red")
GREEN_PATTERN = re.compile(r"(\d+) green")
BLUE_PATTERN = re.compile(r"(\d+) blue")

possible_games = []
powers = []

for line in data:
    match = GAME_PATTERN.match(line)
    if not match:
        print(f"Line not matching: {line}")
        sys.exit(1)
    
    game_id = int(match.group(1))
    draws = match.group(2).split('; ')

    max_r, max_g, max_b = 0, 0, 0

    for d in draws:
        if match := RED_PATTERN.search(d):
            max_r = max(max_r, int(match.group(1)))
        if match := GREEN_PATTERN.search(d):
            max_g = max(max_g, int(match.group(1)))
        if match := BLUE_PATTERN.search(d):
            max_b = max(max_b, int(match.group(1)))

    if max_r <= AVAILABLE_RED and max_g <= AVAILABLE_GREEN and max_b <= AVAILABLE_BLUE:
        possible_games.append(game_id)

    powers.append(max_r * max_g * max_b)
    
# print(possible_games)
print(f"Part one: {sum(possible_games)}")
# print(powers)
print(f"Part two: {sum(powers)}")
