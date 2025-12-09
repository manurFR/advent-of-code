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


def closest_pair(distances):
    min_dist = float('inf')
    min_pair = (-1, -1)
    for i in range(len(distances)):
        for j in range(i + 1, len(distances)):
            if distances[i][j] < min_dist:
                min_dist = distances[i][j]
                min_pair = (i, j)
    return min_pair, min_dist


@timeit
def part1(data, stop_at: int):
    # build the half matrix of distances
    n = len(data)
    distances = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            distances[i][j] = dist3d(data[i], data[j])

    # print(' '.join(f"{i:>7}" for i in range(n)))
    # print('\n'.join(' '.join(f"{distances[i][j]:>7}" if j > i else f"{distances[j][i]:>7}" for j in range(n)) for i in range(n)))
    
    circuits = [[i] for i in range(n)]  # each circuit starts with one point
    nb_connections = 0
    
    ignore_pairs = set()
    while nb_connections < stop_at:
        (p1, p2), _ = closest_pair(distances)
        if any(True for c in circuits if p1 in c and p2 in c):
            # both points already in the same circuit
            nb_connections += 1
            # print(f"Points {data[p1]} and {data[p2]} are already connected. Skipping. Total connections: {nb_connections}.")
            distances[p1][p2] = float('inf')  # ignore this pair next time
            continue
        # find the circuits containing p1 and p2
        idx_p1 = next(idx for idx, c in enumerate(circuits) if p1 in c)
        idx_p2 = next(idx for idx, c in enumerate(circuits) if p2 in c)
        # merge circuits
        circuits[idx_p1].extend(circuits[idx_p2])
        del circuits[idx_p2]
        nb_connections += 1
        distances[p1][p2] = float('inf')  # ignore this pair next time
        # print(f"Connected points {data[p1]} and {data[p2]} with distance {min_dist}. Total connections: {nb_connections}. "
        #       f"Circuit sizes: {sorted([len(c) for c in circuits], reverse=True)}")
        
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
    return 0


# Tests
def test_part1():
    assert part1(TESTDATA, stop_at=10) == 40


def test_part2():
    assert part2(TESTDATA) == 0
    
    
def test_dist3d():
    assert dist3d((0,0,0), (1,1,1)) == 3
    assert dist3d((1,2,3), (4,5,6)) == 27
    

def test_closest_pair():
    distances = [
        [0, 6, 4, 9],
        [0, 0, 2, 3],
        [0, 0, 0, 5],
        [0, 0, 0, 0]
    ]
    assert closest_pair(distances) == ((1, 2), 2)


if __name__ == "__main__":
    data = splittedinput(2025, "08", ",", conv=int)
    print(f"Part 1: {part1(data, stop_at=1000)}")
    print(f"Part 2: {part2(data)}")
