from utils import splittedinput, timeit

TESTDATA = [list(map(int, row.split(','))) for row in """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip().splitlines()]


def dist3d(a, b):
    # let's ignore sqrt for performance
    return (b[2] - a[2])**2 + (b[1] - a[1])**2 + (b[0] - a[0])**2


def prepare_distances(data):
    """ Build the half matrix of distances, but store them as a dict 
        with each distance as key and the list of point pairs at that distance as value
    """
    distances = {}  # {distance: [(i1, j1), (i2, j2), ...]}
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            d = dist3d(data[i], data[j])
            if d not in distances:
                distances[d] = []
            distances[d].append((i, j))
    return distances


def connect_boxes(data: list[list[list[int]]], distances: dict[int: list[tuple[list[int], list[int]]]], end_condition: callable) -> list[list[int]]:
    """ Connect boxes based on distances until end_condition is met.
        Returns the list of circuits (each circuit is a list of point indices).
    """
    circuits = [[i] for i in range(len(data))]  # each circuit starts with one point
    nb_connections = 0
    
    p1, p2 = -1, -1
    while len(distances) > 0 and not end_condition(circuits, nb_connections):
        nb_connections += 1
        min_dist = min(distances.keys())
        p1, p2 = distances[min_dist][0]
        if any(True for c in circuits if p1 in c and p2 in c):
            # both points already in the same circuit
            del distances[min_dist]
            continue
        # find the circuits containing p1 and p2
        idx_p1 = next(idx for idx, c in enumerate(circuits) if p1 in c)
        idx_p2 = next(idx for idx, c in enumerate(circuits) if p2 in c)
        # merge circuits
        circuits[idx_p1].extend(circuits[idx_p2])
        del circuits[idx_p2]
        del distances[min_dist]
    
    return circuits, (p1, p2)


@timeit
def part1(data, stop_at: int):
    distances = prepare_distances(data)
    
    circuits, _ = connect_boxes(
        data, 
        distances, 
        end_condition=lambda circuits, nb_connections: nb_connections >= stop_at
    )
    
    # extract the size of the circuits, sort it in descending order
    circuit_sizes = sorted([len(c) for c in circuits], reverse=True)
    # print(f"Circuit sizes: {circuit_sizes}")
    
    # for i, c in enumerate(circuits):
    #     print(f"Circuit {i+1}:")
    #     for idx in c:
    #         print(f"  {data[idx]}") 

    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


@timeit
def part2(data):
    distances = prepare_distances(data)
    circuits, (last_p1, last_p2) = connect_boxes(
        data, 
        distances, 
        end_condition=lambda circuits, nb_connections: len(circuits) == 1  # stop when all points are connected
    )
    
    return data[last_p1][0] * data[last_p2][0]


# Tests
def test_part1():
    assert part1(TESTDATA, stop_at=10) == 40


def test_part2():
    assert part2(TESTDATA) == 25272
    
    
def test_dist3d():
    assert dist3d((0,0,0), (1,1,1)) == 3
    assert dist3d((1,2,3), (4,5,6)) == 27


if __name__ == "__main__":
    data = splittedinput(2025, "08", ",", conv=int)
    print(f"Part 1: {part1(data, stop_at=1000)}")
    print(f"Part 2: {part2(data)}")
