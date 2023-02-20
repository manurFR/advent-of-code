from utils import readinput

data = readinput("day06")

signal = data[0]


def find_distinct_chars(text, nb_char):
    for idx in range(0, len(text)-nb_char+1):
        if len(set(text[idx:idx+nb_char])) == nb_char:
            return idx + nb_char, text[idx:idx+nb_char]


assert find_distinct_chars("ababcdefgh", 4) == (6, "abcd")

pos, marker = find_distinct_chars(signal, 4)
print(f"Part one: {pos} ({marker})")

pos, marker = find_distinct_chars(signal, 14)
print(f"Part two: {pos} ({marker})")
