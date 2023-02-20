from utils import splittedinput

LOSS = -1
DRAW = 0
WIN = 1
SCORE_SHAPE = {'X': 1, 'Y': 2, 'Z': 3}
SCORE_OUTCOME = {LOSS: 0, DRAW: 3, WIN: 6}

OUTCOMES = {'A': {'X': DRAW, 'Y': WIN,  'Z': LOSS},
            'B': {'X': LOSS, 'Y': DRAW, 'Z': WIN},
            'C': {'X': WIN,  'Y': LOSS, 'Z': DRAW}}
INVERTED_OUTCOMES = {elf: {outcome: me for me, outcome in original.items()} for elf, original in OUTCOMES.items()}

data = splittedinput("day02")

score = 0
for elf, me in data:
    score += SCORE_SHAPE[me] + SCORE_OUTCOME[OUTCOMES[elf][me]]
print(f"Part one: {score}")

ORDER_MAPPING = {'X': LOSS, 'Y': DRAW, 'Z': WIN}

score = 0
for elf, order in data:
    expected_outcome = ORDER_MAPPING[order]
    me = INVERTED_OUTCOMES[elf][expected_outcome]
    score += SCORE_SHAPE[me] + SCORE_OUTCOME[expected_outcome]
print(f"Part two: {score}")
