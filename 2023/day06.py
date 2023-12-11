import math
from pprint import pprint
from utils import columnarinput, splittedinput


# data = columnarinput('day06-example', convert_rows={'Time': int, 'Distance': int})
data = columnarinput('day06', convert_rows={'Time': int, 'Distance': int})

# pprint(data)

def find_record_beats(races):
    record_beats = []
    for race in races:
        record_distance = race['Distance']
        race_time = race['Time']
        # if the case is not exactly half the race_time, count it twice since it has its symmetrical counterpart
        winning_cases = [1 if hold_time == (race_time / 2) else 2
                        for hold_time in range(1, 1 + race_time // 2)
                        if hold_time * (race_time - hold_time) > record_distance]
        # print(winning_cases)
        record_beats.append(sum(winning_cases))
    return record_beats

beats1 = find_record_beats(data)
print(beats1)
print(f"Part one: {math.prod(beats1)}")

# data = splittedinput('day06-example')
data = splittedinput('day06')

race_time = int(''.join(data[0][1:]))
record_distance = int(''.join(data[1][1:]))

races = [{'Time': race_time, 'Distance': record_distance}]
beats2 = find_record_beats(races)

print(beats2)
print(f"Part two: {beats2[0]}")