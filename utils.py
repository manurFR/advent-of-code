from collections import deque
from functools import wraps
import os
from queue import PriorityQueue
import re
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Optional
from unittest.mock import patch


# ----- Grid manipulation -----
# Grids are lists of list of (generally) one character
#  The first dimension is y, the vertical ; the second is x, the horizontal

# increments in (y, x) when going to each direction
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)
NW = (-1, -1)
NE = (-1, 1)
SW = (1, -1)
SE = (1, 1)
DIRECTIONS = [NORTH, NE, EAST, SE, SOUTH, SW, WEST, NW]  # clockwise


def find(grid: list[list[Any]], val: Any) -> list[tuple[int, int]]:
    """Find every occurences of val in grid. Return their positions [(y, x), ...]."""
    return [(y, x) for y in range(len(grid)) for x in range(len(grid[y])) if grid[y][x] == val]


def fwd(pos, dirn, step=1):
    """From a pos (y, x) point, return the coordinates of the point 'step' units in direction dirn
       Warning: this function do not know the data grid and do not check if the new position is valid!"""
    y, x = pos
    dy, dx = dirn
    return y + step * dy, x + step * dx


def clockwise(dirn, step):
    """each unit of step is a rotation of 45°, so clockwise(NORTH, 1) == NE and clockwise(NORTH, 2) == EAST"""
    idx = DIRECTIONS.index(dirn)
    newidx = idx + step
    while newidx >= len(DIRECTIONS):
        newidx -= len(DIRECTIONS)
    while newidx < 0:
        newidx += len(DIRECTIONS)
    return DIRECTIONS[newidx]


def ingrid(data, pos):
    """Ingrid will tell you if position pos (y, x) is inside the grid 'data'"""
    y, x = pos
    return 0 <= x < len(data[0]) and 0 <= y < len(data)


def display(grid):
    print('\n'.join(''.join(map(str, row)) for row in grid))
    print()


def breadth_first_search(grid: list[list], startpos: tuple, 
                         adjacencyrule: Callable[[list[list], tuple], list[tuple]], 
                         endrule: Callable[[list[list], tuple], bool],
                         include_head: bool = True) -> list[list]:
    """Explore the grid from a starting position and return all the valid paths.
        Use BFS when you need to find ALL the valid paths.

        - adjacencyrule must be a function f(grid, currpos) -> list[tuple[int, int]]
          that return, for a position currpos, the next valid positions on the path
        - endrule must be a function f(grid, currpos) -> bool that return True if the
          current position marks the end of a path
        - include_head is a boolean (default True) that indicated if the position marking
          the end of a path (ie. when endrule() returns True) should be included in the path;
           set to True if endrule() can detect the end point of a path (included),
           set to False if endrule() can only detect invalid positions, when we are already out of a valid path
      IMPORTANT: this function returns ALL the valid paths that lead from the starting
       position to an end point. If you need only the unique end points, apply a set() on them.
    """
    winpaths = []
    queue = deque()

    queue.append((startpos, [startpos]))  # current_vertex, path

    while queue:
        currpos, path = queue.popleft()

        if endrule(grid, currpos):
            if not include_head:
                path.pop()
            winpaths.append(path)
            continue

        for nextpos in adjacencyrule(grid, currpos):
            # not: no "if nextpos not in visited" in this implementation, we return ALL valid paths
            if nextpos not in path:
                queue.append((nextpos, path + [nextpos]))

    return winpaths


def a_star_search(grid: list[list], startpos: tuple, goalpos: tuple,
                  adjacencyrule: Callable[[list[list], tuple], list[tuple]],
                  heuristic_distance: Callable[[tuple, tuple], int]) -> list:
    """Explore the grid from a starting position and the shortest path to goalpost.
        Use A* when you need to find only the shortest path. It's faster than BFS in most cases.

        - adjacencyrule must be a function f(grid, currpos) -> list[tuple[int, int]]
          that return, for a position currpos, the next valid positions on the path
        - heuristic_distance must be a function f(pos1, pos2) -> int that returns
          an estimation of the maximum distance between pos1 and pos2.
            => for 4-connected grids (N,E,S,W) use manhattan distance
            => for 8-connected grids (adding NE,SE,SW,NW) use octile distance

        Note: if this cannot find a path (because the way to goalpost is blocked), we return []

        see http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        and https://github.com/riscy/a_star_on_grids
    """
    open_list = PriorityQueue()
    open_list.put((0, startpos))
    closed_list = []

    g_scores = {startpos: 0}  # distance from startpos to key
    parent = {startpos: None}  # previous position on the path

    while not open_list.empty():
        _, currpos = open_list.get()
        closed_list.append(currpos)

        if currpos == goalpos:
            path = []
            while currpos:
                path.append(currpos)
                currpos = parent[currpos]
            return path[::-1]  # reverse to start with startpos

        for nextpos in adjacencyrule(grid, currpos):
            g = g_scores[currpos] + 1
            if nextpos not in g_scores or g < g_scores[nextpos]:
                g_scores[nextpos] = g
                h = heuristic_distance(nextpos, goalpos)
                f = g + h
                open_list.put((f, nextpos))
                parent[nextpos] = currpos
    
    return []


def manhattan(pos1: tuple, pos2: tuple) -> int:
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])


def printdot():
    print(".", end="", flush=True)


# ----- Input file manipulation ----

def convert(listval: list, conv: Optional[type]) -> list:
    """Convert array to 'conv' type, but handle None (no conversion) gracefully."""
    if conv is None:
        return listval
    else:
        return list(map(conv, listval))


def inputdir(year: str) -> Path:
    return Path(os.path.dirname(os.path.abspath(__file__))) / year / "inputs"


def readinput(year: int, day: str, conv: Optional[type]=None) -> list[str]:
    """Returns a list, with just each line as an item"""
    with (inputdir(str(year)) / day).open("r") as f:
        data = convert([line.strip() for line in f.readlines()], conv)
    print(f"...Parsed {len(data)} lines from input file {str(year)}/{day}")
    return data


def splittedinput(year: int, day: str, sep: Optional[str|int]=None, conv: Optional[type]=None) -> list[list[str|Any]]:
    """Each item is a line but as a list of the elements splitted around sep
       - if sep=None, splitted around clusters of whitespaces
       - if sep is an integer N, the items will be strings of N consecutive characters
         example: with sep=1, the line "ABCD" will be splitted to ['A', 'B', 'C', 'D'] 
                  with sep=2,  "   "      "    "    "     "     " ['AB', 'CD']  etc.
    """
    if isinstance(sep, int):
        return [convert(re.findall(rf".{{1,{sep}}}", line), conv) for line in readinput(year, day)]
    else:
        return [convert(line.split(sep), conv) for line in readinput(year, day)]


def inputparts(year: int, day: str) -> list[list[str]]:
    """Input is splitted in sections (parts) separated by empty lines."""
    parts = []
    current = []
    for line in readinput(year, day):
        if not line:
            if current:
                parts.append(current)
                current = []
        else:
            current.append(line)
    if current:
        parts.append(current)
    return parts


def columnarinput(year: int, day: str, convert_rows: dict[str, type]={}):
    data = []
    for line in readinput(year, day):
        items = line.split()
        key = items[0].replace(':', '')
        for idx, col in enumerate(items[1:]):
            if convert_rows and key in convert_rows:
                col = convert_rows[key](col)
            if len(data) <= idx:
                data.append({key: col})
            else:
                data[idx].update({key: col})
    return data


def str2intlist(intstr, sep=None):
    """Convert a string of numbers separated by sep (defaut: whitespaces) 
    to a list of integers"""
    return list(map(int, intstr.split(sep)))


# ----- Misc -----

def timeit(f: Callable) -> Callable:
    """ Compute execution time of a function. """
    @wraps(f)
    def wrap(*args, **kw):
        t0 = perf_counter()
        result = f(*args, **kw)
        t1 = perf_counter()
        if os.environ.get("PYTEST_VERSION") is None:
            print(f'[TIMER] function:{f.__name__}() took {round(t1 - t0, 4)} second(s) to complete')
        return result
    return wrap

# ----- Tests -----
# python -m pytest utils.py

def test_find():
    grid = [[c for c in line] for line in """
.....
.X...
..*.X
X....
....X
""".strip().splitlines()]
    assert find(grid, "X") == [(1, 1), (2, 4), (3, 0), (4, 4)]
    assert find(grid, "*") == [(2, 2)]
    assert find(grid, "$") == []


def test_fwd():
    assert fwd((1, 1), NORTH) == (0, 1)
    assert fwd((1, 1), SE) == (2, 2)
    assert fwd((3, 3), WEST, step=3) == (3, 0)
    assert fwd((3, 3), NW, step=2) == (1, 1)


def test_clockwise():
    assert clockwise(NORTH, 1) == NE
    assert clockwise(NORTH, 2) == EAST
    assert clockwise(NORTH, 7) == NW
    assert clockwise(NORTH, 8) == NORTH
    assert clockwise(NORTH, 11) == SE
    assert clockwise(NORTH, -2) == WEST
    assert clockwise(NORTH, -18) == WEST


def test_ingrid():
    data = [[1 for x in range(5)] for y in range(5)]
    assert ingrid(data, (0, 0)) is True
    assert ingrid(data, (1, 1)) is True
    assert ingrid(data, (4, 0)) is True
    assert ingrid(data, (0, 4)) is True
    assert ingrid(data, (4, 4)) is True
    assert ingrid(data, (5, 4)) is False
    assert ingrid(data, (4, 5)) is False
    assert ingrid(data, (5, 5)) is False
    assert ingrid(data, (-1, 2)) is False
    assert ingrid(data, (2, -1)) is False


def test_convert():
    assert convert(["1", "2", "3"], None) == ["1", "2", "3"]
    assert convert(["1", "2", "3"], int) == [1, 2, 3]
    assert convert(["1", "2", "3"], float) == [1.0, 2.0, 3.0]
    assert convert([1, 2.330, "4"], str) == ["1", "2.33", "4"]


def test_inputdir():
    p = inputdir("2023")
    assert isinstance(p, Path)
    assert str(p).endswith("advent-of-code/2023/inputs")


@patch("utils.inputdir")
def test_readinput(inputdir, tmp_path, capsys):
    inputdir.return_value = tmp_path
    (tmp_path / "02").write_text("123\n456\n789")
    
    data = readinput(2023, "02", conv=int)
    assert data == [123, 456, 789]

    assert capsys.readouterr()[0].startswith("...Parsed 3 lines")


@patch("utils.inputdir")
def test_splittedinput_on_separator(inputdir, tmp_path):
    inputdir.return_value = tmp_path
    (tmp_path / "02").write_text("AB|CD\nE|F|GH\nIJKL")

    data = splittedinput(2023, "02", sep='|')
    assert data == [['AB', 'CD'], ['E', 'F', 'GH'], ['IJKL']]


@patch("utils.inputdir")
def test_splittedinput_on_whitespaces(inputdir, tmp_path):
    inputdir.return_value = tmp_path
    (tmp_path / "02").write_text("12   45\n6\t8\t  \t 11\n9876")

    data = splittedinput(2023, "02", sep=None, conv=int)
    assert data == [[12, 45], [6, 8, 11], [9876]]


@patch("utils.inputdir")
def test_splittedinput_with_length(inputdir, tmp_path):
    inputdir.return_value = tmp_path
    (tmp_path / "02").write_text("ABCD\nEFGH\nIJKL")

    data = splittedinput(2023, "02", sep=2)
    assert data == [['AB', 'CD'], ['EF', 'GH'], ['IJ', 'KL']]


@patch("utils.inputdir")
def test_inputparts(inputdir, tmp_path):
    inputdir.return_value = tmp_path
    (tmp_path / "02").write_text("ABCD\nEFGH\n\nIJKL")

    data = inputparts(2023, "02")
    assert data == [['ABCD', 'EFGH'], ['IJKL']]


# TODO test_columnarinput()


def test_str2intlist():
    assert str2intlist("1,12,123,99", sep=",") == [1, 12, 123, 99]
    assert str2intlist("1//12//123//99", sep="//") == [1, 12, 123, 99]
    assert str2intlist("1 12    123\t99", sep=None) == [1, 12, 123, 99]
