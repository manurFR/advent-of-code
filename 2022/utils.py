
def readinput(day):
    with open(f"inputs/{day}", "r") as f:
        return [line.strip() for line in f.readlines()]


def splittedinput(day, sep=None):
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
