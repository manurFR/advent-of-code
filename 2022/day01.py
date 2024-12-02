from utils import inputparts

data = inputparts(2022, "day01")

calories = [sum(int(c) for c in part) for part in data]

print(f"Part one: {max(calories)}")
print(f"Part two: {sum(sorted(calories, reverse=True)[:3])}")