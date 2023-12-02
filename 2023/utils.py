import os
from pathlib import Path


AOC2023 = Path(os.path.dirname(os.path.abspath(__file__)))
INPUTS_DIR = AOC2023 / "inputs"

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
