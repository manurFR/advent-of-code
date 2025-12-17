from dataclasses import dataclass
from functools import cache
from itertools import combinations
from utils import readinput, timeit

DEBUG = False

ANSI_RED = "\u001b[31m"
ANSI_RESET = "\u001b[0m"

TESTDATA = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".strip().splitlines()

@dataclass
class Machine:
    diagram: list[str]
    buttons: list[list[int]]
    joltages: list[int]


def red(text: str) -> str:
    return f"{ANSI_RED}{text}{ANSI_RESET}"


def debug(msg: str = ""):
    if DEBUG:
        print(msg)


def parse_manual(data) -> list[Machine]:
    machines = []
    for line in data:
        parts = line.split(' ')
        assert len(parts) >= 3
        diagram = parts[0][1:-1]
        joltages = list(map(int, parts[-1][1:-1].split(',')))
        buttons = [[int(light) for light in bt[1:-1].split(',')] for bt in parts[1:-1]]
        machines.append(Machine(diagram=diagram, buttons=buttons, joltages=joltages))
    return machines


def fmtlights(lights: tuple[bool], change: str = None) -> str:
    """Format tuples like (True, False, True) into strings like '101', optionally highlighting changes in RED."""
    if change is None:
        return ''.join('1' if light else '0' for light in lights)
    else:
        bits = []
        for light, ch in zip(lights, change):
            bit = '1' if light else '0'
            if ch == '!':
                bit = red(bit)
            bits.append(bit)
        return ''.join(bits)
    

def button2str(button: list[int], length: int) -> str:
    """Format a button like [0, 2, 3] into a string like '!.!!.' (for length 5)."""
    return ''.join('!' if idx in button else '.' for idx in range(length))


def solve_diagram(target, buttons) -> list[list[list[int]]]:
    """Return all the sequences (first list) of successive button presses (second list) 
       that lead to the target diagram.
       Each button is coded as a list (the third one) of light indices it toggles.
       
       Each button can be pressed at most once in a sequence, since pressing it twice cancels its effect.
       And the order of presses does not matter, since toggling is commutative.
       So each possible sequence is actually one of the mathematical combinations of N buttons among the
       given list, for N between 0 and the total number of buttons.
    """
    booltarget = list(char == '#' for char in target)
    solving_sequences = []
    
    # Allow 0-button (empty) combination, which is needed for the all-even (all-off) case!
    button_combinations = [sorted(c) for nb_buttons in range(0, len(buttons) + 1) for c in combinations(buttons, nb_buttons)]  
    
    for sequence in button_combinations:
        lights = [False] * len(target)
        for button in sequence:
            for light_idx in button:
                lights[light_idx] = not lights[light_idx]
        if lights == booltarget:
            solving_sequences.append(sequence)

    return solving_sequences


@timeit
def part1(data):
    """495 => too high"""
    machines = parse_manual(data)
    tot_presses = 0
    for machine in machines:
        buttons_pressed_sequences = solve_diagram(machine.diagram, machine.buttons)
        shortest_sequence = min(buttons_pressed_sequences, key=len)
        tot_presses += len(shortest_sequence)
               
    return tot_presses

@cache  # needs tuples instead of lists to be hashable
def solve_joltages(joltages: tuple[int, ...], buttons: tuple[tuple[int, ...], ...]) -> int:
    # Base case: all joltages are zero
    if all(j == 0 for j in joltages):
        return 0

    # 1) Find the button presses that lead to the parity of the target
    target_str = '.'.join(str(joltage) for joltage in joltages)
    target_parity = ['#' if joltage % 2 == 1 else '.' for joltage in joltages]
    debug(f"** ({target_str}) > parity {''.join(target_parity)}")
    sequences_to_parity = solve_diagram(target_parity, buttons)
    debug(f"**   ({len(sequences_to_parity)} possible sequences to parity: {' | '.join(str(seq) for seq in sequences_to_parity)})")
    
    # If there are no sequences to parity, this configuration is impossible
    if not sequences_to_parity:
        return float('inf')

    # Now for each sequence, compute the number of presses needed to reach the target
    min_presses = float('inf')
    for seq in sequences_to_parity:
        # 2) Reverse-apply these presses to the target to get the joltage pattern with only even joltages
        intermediate_target = list(joltages)
        for button in seq:
            for light_idx in button:
                intermediate_target[light_idx] -= 1
        intermediate_str = '.'.join(str(j) for j in intermediate_target)
        
        # 3) Let's try to solve and if we can't, halve the target and try again
        if any(j < 0 for j in intermediate_target):
            debug(f"** Intermediate target with negative value(s) {intermediate_target}, skipping")
            continue
        debug(f"** ({target_str}) '-> {seq} => {len(seq)} presses (+) evens {intermediate_str}")
        if intermediate_target == [0] * len(joltages):  # works because 1//2 = 0
            debug(f"** Ending recursion at target {joltages} with {len(seq)} presses to parity")
            min_presses = min(min_presses, len(seq))
            continue
        
        half_joltages = [joltage // 2 for joltage in intermediate_target]
        half_joltages_str = '.'.join(str(j) for j in half_joltages)
        debug(f"** ({target_str}) '-> 2 (x) {half_joltages_str}")
        solve_half = solve_joltages(tuple(half_joltages), buttons)
        if solve_half == float('inf'):
            continue
        presses_for_seq = 2 * solve_half + len(seq)
        debug(f"** => Nb presses to {joltages} found: 2 * {solve_half} + {len(seq)} = {presses_for_seq} (sequence to parity: {seq})")
        if presses_for_seq < min_presses:
            min_presses = presses_for_seq
            debug(f"** => New minimum presses found: {presses_for_seq} (sequence to parity: {seq})")
    return min_presses


@timeit
def part2(data):
    machines = parse_manual(data)
    tot_presses = 0
    
    # A* and BFS take too long and never finish, so let's use tenthmascot algorithm.
    #  https://www.reddit.com/r/adventofcode/comments/1pk87hl/2025_day_10_part_2_bifurcate_your_way_to_victory/
    #  I'm more confortable with a solution that reuses part1 than with a solver, which I'm not familiar with.
    
    for machine in machines:
        debug()
        presses = solve_joltages(tuple(machine.joltages), tuple(tuple(button) for button in machine.buttons))
        debug(f"** Total presses for machine with joltages {machine.joltages}: {presses}")
        debug()
        tot_presses += presses
    
    return tot_presses


# Tests
def test_part1():
    assert part1(TESTDATA) == 7


def test_part2():
    assert part2([TESTDATA[0]]) == 10
    assert part2([TESTDATA[1]]) == 12
    assert part2([TESTDATA[2]]) == 11
    assert part2(TESTDATA) == 33
    assert part2(["[..##.#] (0,1,2,5) (0,1,5) (0,5) (2,4) (2,3,5) (0,3,4) {223,218,44,22,9,239}"]) == 248


def test_parse_manual():
    machines = parse_manual(TESTDATA)
    assert len(machines) == 3
    assert all(isinstance(m, Machine) for m in machines)
    assert machines[0].diagram == '.##.'
    assert machines[0].buttons == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    assert machines[0].joltages == [3, 5, 4, 7]
    

def test_button2str():
    assert button2str([0, 2, 3], 5) == '!.!!.'
    assert button2str([], 4) == '....'
    assert button2str([1, 3], 4) == '.!.!'
    

def test_fmtlights():
    assert fmtlights((True, False, True)) == '101'
    assert fmtlights((False, False, True), change='!.!') == f"{red('0')}0{red('1')}"
    

def test_solve_diagram():
    buttons = [[0, 2], [1, 2], [0, 1]]
    target = '##.'
    sequences = solve_diagram(target, buttons)
    assert len(sequences) == 2
    assert sorted(sequences) == sorted([[ [0,2], [1,2] ], [ [0,1] ]])


if __name__ == "__main__":
    data = readinput(2025, "10")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
