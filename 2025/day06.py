from utils import readinput, splittedinput, timeit

TESTDATA = """
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
""".strip().splitlines()


@timeit
def part1(data):
    # preprocessing by splitting on clusters of whitespace (like splittedinput()) since here we ignore alignment
    data = [line.split() for line in data]
    
    assert all(char in "*+" for char in data[-1]), "Invalid operator line"
    total = 0
    for idx in range(len(data[0])):
        operator = data[-1][idx]
        coltotal = 1 if operator == "*" else 0
        for row in data[:-1]:
            val = int(row[idx])
            if operator == "*":
                coltotal *= val
            elif operator == "+":
                coltotal += val
        # print(f"Column {idx}: operator {operator}, column total {coltotal}")
        total += coltotal
    return total


@timeit
def part2(data):
    # splitting must be more careful to preserve alignment of numbers
    # Transpose data to get columns
    columns = list(zip(*data))
    # Find indices where all rows have a space (i.e., separator columns)
    sep_indices = [i for i, col in enumerate(columns) if all(c == " " for c in col)]
    # Add -1 and len(data[0]) for easier slicing
    split_points = [-1] + sep_indices + [len(data[0])]
    # For each line, split into segments between separator columns, preserving spaces
    new_data = []
    for line in data:
        segments = [line[split_points[i]+1:split_points[i+1]] for i in range(len(split_points)-1)]
        new_data.append(segments)
    data = new_data
    # transpose again to get problems as rows
    data = list(zip(*data))    
    
    total = 0
    for problem in data:
        operator = problem[-1].strip()
        problemtotal = 1 if operator == "*" else 0
        
        maxlen = max(len(number) for number in problem[:-1])
        rotated_numbers = []
        for idx in range(maxlen):
            rotated_number = "".join(number[len(number) - 1 - idx] for number in problem[:-1] if len(number) >= 1 + idx)
            rotated_numbers.append(int(rotated_number))
        
        # print(f"Problem rotated numbers {rotated_numbers}, operator {operator}")
        
        for number in rotated_numbers:
            val = int(number)
            if operator == "*":
                problemtotal *= val
            elif operator == "+":
                problemtotal += val
        # print(f"Problem : operator {operator}, rotated numbers {rotated_numbers}, total {problemtotal}")
        total += problemtotal
    return total


# Tests
def test_part1():
    assert part1(TESTDATA) == 4277556


def test_part2():
    assert part2(TESTDATA) == 3263827


if __name__ == "__main__":
    data = readinput(2025, "06")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")