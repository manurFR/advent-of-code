from dataclasses import dataclass
from pprint import pprint
import re

from utils import display, printdot, readinput, timeit

TESTDATA = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip().splitlines()

PATTERN = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


@dataclass
class Robot:
    rx: int
    ry: int
    vx: int
    vy: int
    grid_w: int
    grid_h: int

    def move(self):
        self.rx = (self.rx + self.vx) % self.grid_w
        self.ry = (self.ry + self.vy) % self.grid_h


def wait(robots, nb_seconds=1):
    for _ in range(nb_seconds):
        for rob in robots:
            rob.move()


def count_quadrant(xmin, xmax, ymin, ymax, robots):
    return len(list(1 for rob in robots if xmin <= rob.rx <= xmax and ymin <= rob.ry <= ymax))



def draw(grid, robots, counts=True):
    drawing = []
    for gy in range(grid[1]):
        line = []
        for gx in range(grid[0]):
            nb_robots = len(list(r for r in robots if r.rx == gx and r.ry == gy))
            if nb_robots > 0:
                line.append(str(nb_robots) if counts else "#")
            else:
                line.append(".")
        drawing.append(''.join(line))
    return drawing


@timeit
def part1(data, grid):
    gw, gh = grid
    robots = []
    for line in data:
        if match := PATTERN.match(line):
            robots.append(Robot(*(int(g) for g in match.groups()), grid_w=gw, grid_h=gh))
    
    # display(draw(grid, robots))
    # print("----")

    wait(robots, nb_seconds=100)
    
    # display(draw(grid, robots))

    # quadrant frontier
    fw, fh = gw // 2, gh // 2

    safety_factor = count_quadrant(0, fw - 1, 0, fh - 1, robots) * \
                    count_quadrant(fw + 1, gw - 1, 0, fh - 1, robots) * \
                    count_quadrant(0, fw - 1, fh + 1, gh - 1, robots) * \
                    count_quadrant(fw + 1, gw - 1, fh + 1, gh - 1, robots)

    return safety_factor


@timeit
def part2(data, grid):
    gw, gh = grid
    robots = []
    for line in data:
        if match := PATTERN.match(line):
            robots.append(Robot(*(int(g) for g in match.groups()), grid_w=gw, grid_h=gh))

    for sec in range(10000):
        wait(robots)

        drawing = draw(grid, robots, counts=False)

        if sec % 100 == 0:
            printdot()

        if any("############" in line for line in drawing):
            print()
            print(f"{sec + 1} seconds... found line ! =>")
            display(drawing)


# Tests
def test_part1():
    assert part1(TESTDATA, (11, 7)) == 12


# def test_part2():
    # assert part2(TESTDATA, (11, 7)) == 0


if __name__ == "__main__":
    data = readinput(2024, "14")
    print(f"Part 1: {part1(data, (101, 103))}")
    print(f"Part 2: {part2(data, (101, 103))}")
