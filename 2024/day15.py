from utils import EAST, NORTH, SOUTH, WEST, breadth_first_search, display, find, fwd, inputparts, printdot, timeit

SMALL_WAREHOUSE = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########
""".strip().splitlines()
SMALL_MOVES = ["<^^>>>vv<v>>v<<"]

LARGER_WAREHOUSE = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########
""".strip().splitlines()
LARGER_MOVES = """
<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip().splitlines()

BUG_WAREHOUSE = """
##########
#........#
#........#
#..O.#...#
#..OO....#
#...O....#
#...@....#
#........#
##########
""".strip().splitlines()
BUG_MOVES = ["<<<^^^><v>vv>>^"]


MAPDIR = {'^': NORTH, 'v': SOUTH, '<': WEST, '>': EAST}


def push(grid, pos, dirn) -> bool:
    what = grid[pos[0]][pos[1]]
    match what:
        case '.':
            return True
        case '#':
            return False
        case box if box in "O[]":
            # recursive: we check the next position until we meet a wall or a free space
            if box == 'O' or dirn in (WEST, EAST):
                nextpos = fwd(pos, dirn)
                pushable = push(grid, nextpos, dirn)
                if pushable:
                    grid[nextpos[0]][nextpos[1]] = grid[pos[0]][pos[1]]
                return pushable
            else:  # box in "[]" and dirn in (NORTH, SOUTH)
                # not recursive; we use a BFS to find all the "heads" of the pushing movement and
                #  we push only if ALL of them are a free space '.'
                def adjacents(grid, currpos):
                    newpos = [fwd(currpos, dirn)]  # the dirn taken from the arguments of push()
                    what = grid[currpos[0]][currpos[1]]
                    if what == '[':
                        newpos.append(fwd(currpos, EAST))
                    elif what == ']':
                        newpos.append(fwd(currpos, WEST))
                    return newpos
                
                def ending(grid, currpos):
                    what = grid[currpos[0]][currpos[1]]
                    return what not in "[]"
                
                paths = breadth_first_search(grid, pos, adjacents, ending, include_head=True)
                heads = set(path[-1] for path in paths)
                if all(grid[h[0]][h[1]] == '.' for h in heads):
                    # pushable! the order is important: if dirn is NORTH, we start from the top 
                    #   and copy the boxes up one position ; if dirn is SOUTH we start from the bottom
                    #   and copy down one position => see the reverse argument
                    boxes = sorted(list(set(p for path in paths for p in path[:-1])), 
                                   reverse=(dirn == SOUTH))
                    for boxchar in boxes:
                        nextpos = fwd(boxchar, dirn)
                        grid[nextpos[0]][nextpos[1]] = grid[boxchar[0]][boxchar[1]]
                        grid[boxchar[0]][boxchar[1]] = '.'
                    return True
                else:
                    return False
        case _:
            return False


@timeit
def part1(warehouse: list[str], moves):
    moves = ''.join(moves)
    grid = [[c for c in line] for line in warehouse]

    robot = find(grid, '@')[0]

    # display(grid)

    for m in moves:
        dirn = MAPDIR[m]
        newpos = fwd(robot, dirn)
        if res := push(grid, newpos, dirn):
            grid[robot[0]][robot[1]] = '.'
            grid[newpos[0]][newpos[1]] = '@'
            robot = newpos
        # print()
        # print(f" --- dirn: {m} - pushable: {res} ---")
        # display(grid)

    return sum(100 * box[0] + box[1] for box in find(grid, 'O'))


@timeit
def part2(warehouse, moves):
    moves = ''.join(moves)
    map2 = {'#': "##", 'O': "[]", '.': "..", '@': "@."}
    grid = [[c for orig in line for c in map2[orig]] for line in warehouse]

    robot = find(grid, '@')[0]

    # print(robot)
    # display(grid)

    for m in moves:
        dirn = MAPDIR[m]
        newpos = fwd(robot, dirn)
        if res := push(grid, newpos, dirn):
            grid[robot[0]][robot[1]] = '.'
            grid[newpos[0]][newpos[1]] = '@'
            robot = newpos

    return sum(100 * box[0] + box[1] for box in find(grid, '['))


# Tests
def test_part1():
    assert part1(SMALL_WAREHOUSE, SMALL_MOVES) == 2028
    assert part1(LARGER_WAREHOUSE, LARGER_MOVES) == 10092


def test_part2():
    assert part2(SMALL_WAREHOUSE, SMALL_MOVES) == 1751
    assert part2(LARGER_WAREHOUSE, LARGER_MOVES) == 9021
    assert part2(BUG_WAREHOUSE, BUG_MOVES) == 1631


if __name__ == "__main__":
    warehouse, moves = inputparts(2024, "15")
    print(f"Part 1: {part1(warehouse, moves)}")
    print(f"Part 2: {part2(warehouse, moves)}")
