from pprint import pprint
from utils import splittedinput

CARDS = '23456789TJQKA'
CARDS_JOKER = 'J23456789TQKA'
TYPES = ('HighCard', 'OnePair', 'TwoPairs', 'ThreeOfAKind', 'FullHouse', 'FourOfAKind', 'FiveOfAKind')

data = splittedinput('day07')

# data = [
    # ['32T3K', '765'],
    # ['KK677', '28'],
    # ['KTJJT', '220'],
    # ['QQQJA', '483'],
    # ['T55J5', '684'],
# ]

test = [
    ['AAAAA', ''],
    ['AA8AA', ''],
    ['23332', ''],
    ['TTT98', ''],
    ['23432', ''],
    ['A23A4', ''],
    ['23456', ''],
]

def strength(card, joker=False):
    """0 to 12"""
    return CARDS_JOKER.index(card) if joker else CARDS.index(card) 

def identify(hand, joker=False, debug=False):
    assert len(hand) == 5
    distribution = [hand.count(c) for c in (CARDS_JOKER[1:] if joker else CARDS)]
    nb_jokers = hand.count('J') if joker else 0
    if debug:
        print(distribution, nb_jokers)
    match max(distribution) + nb_jokers:
        case 5:
            return 'FiveOfAKind'
        case 4:
            return 'FourOfAKind'
        case 3:
            # 3 and 2 cards identical with no joker, or two pairs + a joker
            if ((distribution.count(2) == 1 and nb_jokers == 0) or 
                (distribution.count(2) == 2 and nb_jokers == 1)):
                return 'FullHouse'
            else:
                return 'ThreeOfAKind'
        case 2:
            if distribution.count(2) == 2:
                return 'TwoPairs'
            else:
                return 'OnePair'
        case 1:
            return 'HighCard'
        
# for hand, bid in test:
    # print(f"{hand}: {identify(hand)}")

assert identify('AA8AA') == 'FourOfAKind'
assert identify('AA8AA', True) == 'FourOfAKind'
assert identify('TTT98') == 'ThreeOfAKind'
assert identify('TTT98', True) == 'ThreeOfAKind'
assert identify('23432') == 'TwoPairs'
assert identify('23432', True) == 'TwoPairs'
assert identify('23456') == 'HighCard'
assert identify('23456', True) == 'HighCard'

assert identify('KTJJT', True) == 'FourOfAKind'
assert identify('TTJJT', True) == 'FiveOfAKind'
assert identify('TTJ33', True) == 'FullHouse'
assert identify('T8J33') == 'OnePair'
assert identify('T8J33', True) == 'ThreeOfAKind'
assert identify('T8JJ3', True) == 'ThreeOfAKind'
assert identify('48JK3', True) == 'OnePair'

assert identify('J2TK7', True) == 'OnePair'
assert identify('22233', False) == 'FullHouse'
assert identify('22233', True) == 'FullHouse'

"""Using the power of tuple-comparisons, ie element by element in order.
Returns a tuple used for sorting, ie for comparing two hands
The first item is the type of the hand, as an int increasing from weakest to strongest hand
The next items are the strength of each successive card in the hand
"""
ordering_1 = lambda t: (TYPES.index(identify(t[0])), *[strength(c) for c in t[0]])

assert ordering_1(('23332', 1)) < ordering_1(('AAAAA', 1))  # because FullHouse < FiveOfAKind
assert ordering_1(('KTJJT', 1)) < ordering_1(('KK677', 1))  # because Ten < King (second card)
assert not ordering_1(('QQQJA', 1)) < ordering_1(('T55J5', 1))  # because Queen > Ten (first card)

hands = [(hand, int(bid)) for hand, bid in data]

sortedhands = sorted(hands, key=ordering_1)

print(f"Part one: {sum(bid * (rank + 1) for rank, (hand, bid) in enumerate(sortedhands))}")

# with Jokers
ordering_2 = lambda t: (TYPES.index(identify(t[0], joker=True)), 
                        *[strength(c, joker=True) for c in t[0]])

sortedhands_joker = sorted(hands, key=ordering_2)

# for hand, _ in sortedhands_joker:
    # print(hand, '*'*hand.count('J'), identify(hand, True))

print(f"Part two: {sum(bid * (rank + 1) for rank, (hand, bid) in enumerate(sortedhands_joker))}")
