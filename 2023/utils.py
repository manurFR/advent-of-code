import os
from pathlib import Path


AOC2023 = Path(os.path.dirname(os.path.abspath(__file__)))
INPUTS_DIR = AOC2023 / "inputs"

# increments in (y, x) when going to each direction
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

def readinput(day):
    """Returns a list, with just each line as an item"""
    with (INPUTS_DIR / day).open("r") as f:
        return [line.strip() for line in f.readlines()]


def splittedinput(day, sep=None):
    """Each item is a line but as a list of the elements splitted around sep
    (if sep=None, splitted around clusters of whitespaces)"""
    return [line.split(sep) for line in readinput(day)]


def inputparts(day):
    """Input is splitted in sections (parts) separated by empty lines."""
    parts = []
    current = []
    for line in readinput(day):
        if not line:
            if current:
                parts.append(current)
                current = []
        else:
            current.append(line)
    if current:
        parts.append(current)
    return parts


def columnarinput(day, convert_rows=None):
    data = []
    for line in readinput(day):
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
