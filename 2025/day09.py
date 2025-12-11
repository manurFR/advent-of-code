from shapely import GeometryCollection, LineString, Point, Polygon
from utils import splittedinput, timeit

TESTDATA = [list(map(int, row.split(','))) for row in """
11,1
11,7
9,7
9,5
2,5
2,3
7,3
7,1
""".strip().splitlines()]


def area(t1, t2):
    x1, y1 = t1
    x2, y2 = t2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

@timeit
def part1(data):
    max_area = 0    
    for idx1, p1 in enumerate(data):
        for p2 in data[idx1 + 1:]:
            rect_area = area(p1, p2)
            if rect_area > max_area:
                max_area = rect_area
    return max_area


def inside(tile, shape: Polygon) -> bool:
    p = Point(tile)
    return shape.boundary.contains(p) or shape.contains(p)


@timeit
def part2(data):
    shape = Polygon(data)
    
    # only consider x and y coordinates where a red tile is placed, those are the only points where the polygon border can change
    all_y = sorted(set(p[1] for p in data))
    all_x = sorted(set(p[0] for p in data))
    
    # precompute the inside status (True/False) for all coordinates
    inside_grid = [[inside((x, y), shape) for x in all_x] for y in all_y]
    print("inside_grid precomputed")
    
    max_area = 0
    for idx1, p1 in enumerate(data):
        for p2 in data[idx1 + 1:]:
            rect_area = area(p1, p2)
            if rect_area > max_area:
                # Check all tiles within the rectangle
                all_inside = True
                for id_x, x in enumerate(all_x):
                    if x < min(p1[0], p2[0]) or x > max(p1[0], p2[0]):
                        continue
                    for id_y, y in enumerate(all_y):
                        if y < min(p1[1], p2[1]) or y > max(p1[1], p2[1]):
                            continue
                        if not inside_grid[id_y][id_x]:
                            all_inside = False
                            break
                    if not all_inside:
                        break
                if all_inside:
                    max_area = rect_area
    
    return max_area


# Tests
def test_part1():
    assert part1(TESTDATA) == 50


def test_part2():
    assert part2(TESTDATA) == 24
    
    
def test_area():
    assert area((2, 5), (9, 7)) == 24
    assert area((7, 3), (2,3)) == 6
    

def test_inside():
    """
         5.#OOOO#
         ..1.2..O
         ..O.3.##
         4.#OOO#.
         .....6..
         ........
    """
    shape = Polygon([[2,2], [2,5], [7,5], [7,3], [6,3], [6,2]])
    assert inside((2,4), shape) is True  # "1" on border 
    assert inside((4,4), shape) is True  # "2" inside
    assert inside((4,3), shape) is True  # "3" inside
    assert inside((0,2), shape) is False  # "4" outside
    assert inside((0,5), shape) is False  # "5" outside
    assert inside((5,1), shape) is False  # "6" outside


if __name__ == "__main__":
    data = splittedinput(2025, "09", ",", conv=int)
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
