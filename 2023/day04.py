from pprint import pprint
import re
from utils import readinput


data = readinput(2023, "day04")

# data = [
    # 'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
    # 'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
    # 'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
    # 'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
    # 'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
    # 'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'
# ]

PATTERN_CARDS = re.compile(r"Card\s+(\d+): ([^|]*) \| (.*)")

card_count = [1] * len(data)  # au départ 1 exemplaire de chaque carte
points = []
for line in data:
    if match := PATTERN_CARDS.match(line):
        id_raw, winning_raw, this_raw = match.groups()
        id_card = int(id_raw)
        winning = list(map(int, winning_raw.split()))
        this_card = list(map(int, this_raw.split()))

        actual_wins = [number for number in this_card if number in winning]
        # 1 actual => 1 ; 2 actuals => 2 ; 3 actuals => 4 pts ; 4 actuals : 8 pts ... soit 2^(<nb_actuals> - 1)
        if actual_wins:
            points.append(2 ** (len(actual_wins) - 1))
        # print(f"{id_card} {actual_wins} {2 ** (len(actual_wins) - 1) if actual_wins else 0}")

        # print(f"Card {id_card} wins {len(actual_wins)} new cards x {card_count[id_card - 1]} copies")
        for incr in range(len(actual_wins)):
            obtained_card_id = id_card + incr + 1
            if obtained_card_id <= len(data): # il n'y a pas de cartes d'id > 212 à gagner
                card_count[obtained_card_id - 1] += card_count[id_card - 1]
        # print(card_count)

print(f"Part one: {sum(points)}")
# print(card_count)
print(f"Part two: {sum(card_count)}")
