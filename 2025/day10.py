from dataclasses import dataclass
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


@timeit
def part1(data):
    """495 => too high"""
    machines = parse_manual(data)
    tot_presses = 0
    for machine in machines:
        target = machine.diagram
        booltarget = list(char == '#' for char in target)
        
        all_orders = [([False] * len(target), [])]  # [(current light status, buttons pressed to get here), ...]
        
        # only press each button once, since pressing it twice cancels its effect
        for _ in range(len(machine.buttons)):  # at most len(buttons) presses needed
            new_orders = []
            for currpos, buttons_pressed in all_orders:
                for button in machine.buttons:
                    if button in buttons_pressed:
                        continue  # don't press the same button twice
                    newpos = currpos[:]
                    for light_idx in button:
                        newpos[light_idx] = not newpos[light_idx]
                    if newpos == booltarget:
                        # Found a solution
                        tot_presses += len(buttons_pressed) + 1  # +1 for the current button

                        if DEBUG:
                            print(f"Machine with target '{target}' ({''.join('1' if char == '#' else '0' for char in target)}) "
                                f"and buttons [{', '.join(button2str(b, len(target)) for b in machine.buttons)}] "
                                f"solved in {len(buttons_pressed) + 1} presses :")                        
                            prev = [False] * len(target)
                            for b in buttons_pressed + [button]:
                                change = button2str(b, len(target))
                                new = [prev[i] ^ (i in b) for i in range(len(target))]
                                print(f"  {fmtlights(prev)} --[{change}]--> {fmtlights(new, change)}")
                                prev = new
                        
                        new_orders = []  # to break the outer loop as well
                        break
                    else:
                        new_orders.append((newpos, buttons_pressed + [button]))
                if not new_orders:
                    break  # break outer loop as well
            if not new_orders:
                break  # break outer loop as well
            all_orders = new_orders
               
    return tot_presses


@timeit
def part2(data):
    return 0


# Tests
def test_part1():
    assert part1(TESTDATA) == 7


def test_part2():
    assert part2(TESTDATA) == 0


def test_parse_manual():
    machines = parse_manual(TESTDATA)
    assert len(machines) == 3
    assert all(isinstance(m, Machine) for m in machines)
    assert machines[0].diagram == '.##.'
    assert machines[0].buttons == [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
    assert machines[0].joltages == [3, 5, 4, 7]
    

def assert_button2str():
    assert button2str([0, 2, 3], 5) == '!.!!.'
    assert button2str([], 4) == '....'
    assert button2str([1, 3], 4) == '.!.!'
    

def assert_fmtlights():
    assert fmtlights((True, False, True)) == '101'
    assert fmtlights((False, False, True), change='!.!') == f"{red('0')}0{red('1')}"


if __name__ == "__main__":
    data = readinput(2025, "10")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
