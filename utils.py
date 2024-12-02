import os
from pathlib import Path
from typing import Optional


# increments in (y, x) when going to each direction
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)


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


def splittedinput(year: int, day: str, sep: Optional[str]=None, conv: Optional[type]=None) -> list[list[str]]:
    """Each item is a line but as a list of the elements splitted around sep
    (if sep=None, splitted around clusters of whitespaces)"""
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
