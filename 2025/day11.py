from shapely import total_bounds
from ntpath import pathsep
from networkx.algorithms.tests.test_swap import path
from numpy.char import find, count
from networkx.generators import cubical_graph
from IPython.lib.latextools import genelatex
import pytest
from utils import splittedinput, timeit, breadth_first_search
import graphlib
import networkx

TESTDATA = [row.split() for row in """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip().splitlines()]

TESTDATA2 = [row.split() for row in """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip().splitlines()]


def parse_devices(data, startpos) -> dict[str, list[str]]:
    assert len([row for row in data if row[0] == f'{startpos}:']) == 1
    devices = {}
    for row in data:
        assert ':' == row[0][-1]
        device = row[0][:-1]
        devices[device] = row[1:]
    return devices


def bfs_devices(devices: dict[str, list[str]], startpos: str, endpos: str) -> list[list[str]]:
    """BFS to find all paths from startpos to endpos in devices graph"""
    def adjacency(devices, currpos):
        """return, for a position currpos, the next valid positions"""
        return devices.get(currpos, [])
    
    def endrule(devices, currpos):
        """return True if currpos is an end position"""
        return currpos == endpos
    
    paths = breadth_first_search(
        grid=devices,  # ty:ignore[invalid-argument-type]
        startpos=startpos,  # ty:ignore[invalid-argument-type]
        adjacencyrule=adjacency,
        endrule=endrule,
    )
    
    return paths


@timeit
def part1(data):
    devices= parse_devices(data, startpos='you')
    
    paths = bfs_devices(devices, startpos="you", endpos='out')
    
    minlen = min(len(path) for path in paths)
    # print(f"One of the shortest paths: { [path for path in paths if len(path) == minlen][0] }")
    
    return len(paths)


def part2_fortest(data):
    devices = parse_devices(data, startpos='svr')
    
    G = networkx.DiGraph()
    for device, outputs in devices.items():
        for output in outputs:
            G.add_edge(device, output)
    
    paths = list(networkx.all_simple_paths(G, source='svr', target='out'))
    valid_paths = [p for p in paths if 'dac' in p and 'fft' in p]
    
    return len(valid_paths)


def find_paths(G, source, target):
    """Find all paths from source to target in graph G, 
       by applying the cutoff of the number of generations from source to target."""
    generations = networkx.topological_generations(G)
    source_gen, target_gen = 0, -1
    for idx, gen in enumerate(generations):
        if source in gen:
            source_gen = idx
        if target in gen:
            target_gen = idx
            break
    return list(networkx.all_simple_paths(G, source=source, target=target, cutoff=target_gen - source_gen + 1))


def count_paths_to_target(graph, target):
    """Given a DAG graph (DiGraph) and a target node,
       count the sum of distinct paths from each source node to the target node.
       Use memoization to avoid redundant calculations.
       
       Start with the target, which has 1 path to itself.
       Climb up to its predecessors (parents), each of which has one path to the target, and so on.
       When a parent has N children (successors) that have already been counted as "on a path", it means the parent has N paths to the target.
       By climbing up the graph in reverse topological order (leaves to root), we compute the number of paths for each node only once.
       """
    # Reverse the topological order so that the targets are first in line 
    #  and the sources happen afterwards => [::-1]
    # This way the "successors" of a node are actually its parents.
    rev_topological_order = list(networkx.topological_sort(graph))[::-1]
    
    path_counts = {}
    for node in rev_topological_order:
        if node == target:
            path_counts[node] = 1
        else:
            path_counts[node] = sum(path_counts.get(succ, 0) for succ in graph.successors(node))
    return path_counts


@timeit
def part2(data):
    devices = parse_devices(data, startpos='svr')
    
    G = networkx.DiGraph()
    for device, outputs in devices.items():
        for output in outputs:
            G.add_edge(device, output)
            
    # The graph (stored in day11_fullgraph.png) shows that the paths form a directed acyclic graph (DAG),
    #  with a series of 6 enlargments/blobs from 'svr' to 'out', and with 5 shrinked bottlenecks in between
    #  each of those blobs. The bottlenecks are comprised of 3 to 5 nodes at the maximum, while the blobs
    #  expand to 15 to 25 nodes in width (see the notion of generations in a DAG).
    # Computing the number of paths from 'svr' to 'out' directly is computationally too expensive.
    # Instead, we can split the path counting into smaller parts, by counting paths between key nodes.
    # First 'fft' is in the second blob, but with a direct, unique, path from the first bottleneck (top of 2nd blob) 
    #  to itself. The number of paths from 'svr' to 'fft' is computable.
    path_svr2fft = find_paths(G, source='svr', target='fft')
    
    # Next, 'dac' is in the 5th blob, with not too many paths to the last bottleneck. The number of paths from
    #  'dac' to 'out' is also computable (10425 paths).
    path_dac2out = find_paths(G, source='dac', target='out')
    
    # Finally, the number of paths from 'fft' to 'dac' is the most challenging, since there are two full 'blobs' and
    #  20 full generations in between. We have to use a memoization approach.
    path_counts = count_paths_to_target(G, target='dac')
    count_path_fft2dac = path_counts['fft']
    
    print(f"Number of paths from svr to fft: {len(path_svr2fft)}")
    print(f"Number of paths from fft to dac: {count_path_fft2dac}")
    print(f"Number of paths from dac to out: {len(path_dac2out)}")
    
    total_paths = len(path_svr2fft) * count_path_fft2dac * len(path_dac2out)
    
    return total_paths    
    
    # Number of paths from svr to fft: 5842
    # Number of paths from fft to dac: 5885737
    # Number of paths from dac to out: 10425
    # Product (total paths): 358458157650450


def check_dag(devices):
    """Check that the devices graph is a DAG (no cycles)"""
    reverse_graph = {}
    for device, outputs in devices.items():
        for output in outputs:
            reverse_graph.setdefault(output, []).append(device)

    dag = graphlib.TopologicalSorter(reverse_graph)
    try:
        dag.prepare()
        return True
    except graphlib.CycleError as e:
        print(f"Cycle detected: {e}")
        return False


# Tests
def test_part1():
    assert part1(TESTDATA) == 5


def test_part2():
    assert part2_fortest(TESTDATA2) == 2
    

def test_parse_devices():
    devices = parse_devices(TESTDATA, startpos='you')
    assert len(devices) == 10
    assert devices['you'] == ['bbb', 'ccc']
    assert devices['hhh'] == ['ccc', 'fff', 'iii']
    assert devices['ggg'] == ['out']
    
    
def test_graphs_are_DAGs():
    devices = parse_devices(TESTDATA2, startpos='svr')
    assert check_dag(devices) is True
    devices = parse_devices(splittedinput(2025, "11"), startpos='svr')
    assert check_dag(devices) is True
    

@pytest.mark.skip(reason="only do this once to generate the graph images")
def test_networkx():
    devices = parse_devices(TESTDATA2, startpos='svr')
    G = networkx.DiGraph()
    for device, outputs in devices.items():
        for output in outputs:
            G.add_edge(device, output)
    paths = list(networkx.all_simple_paths(G, source='svr', target='out'))
    graph = networkx.drawing.nx_pydot.to_pydot(G)
    graph.write_png('2025/day11_testdata2_graph.png')
    
    assert len(paths) == 8
    
    devices = parse_devices(splittedinput(2025, "11"), startpos='svr')
    G = networkx.DiGraph()
    for device, outputs in devices.items():
        for output in outputs:
            G.add_edge(device, output)
    for generation in networkx.topological_generations(G):
        print(generation)

    graph = networkx.drawing.nx_pydot.to_pydot(G)
    
    graph.get_node('svr')[0].set_style('filled')
    graph.get_node('svr')[0].set_fillcolor('red')
    graph.get_node('out')[0].set_style('filled')
    graph.get_node('out')[0].set_fillcolor('red')
    graph.get_node('you')[0].set_style('filled')
    graph.get_node('you')[0].set_fillcolor('blue')
    graph.get_node('dac')[0].set_style('filled')
    graph.get_node('dac')[0].set_fillcolor('green')
    graph.get_node('fft')[0].set_style('filled')
    graph.get_node('fft')[0].set_fillcolor('green')
    
    graph.write_png('2025/day11_fullgraph.png')


if __name__ == "__main__":
    data = splittedinput(2025, "11")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
