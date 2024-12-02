import sys

from utils import readinput

F = "file"
D = "dir"

data = readinput(2022, "day07")


class Node(object):
    def __init__(self, typenode, namenode, parent=None, size=None):
        assert typenode in (F, D)
        self.typenode = typenode
        self.namenode = namenode
        self.parent = parent
        self.size = size
        self.children = {}

    def add_child(self, typenode, namenode, size=None):
        if namenode not in self.children:
            self.children[namenode] = Node(typenode, namenode, parent=pwd, size=size)

    def up(self):
        return self.parent if self.parent else self

    def down(self, child):
        return self.children.get(child, self)

    def compute_size(self):
        if self.typenode == D:
            self.size = sum(child.compute_size() for child in self.children.values())
        return self.size

    def filter_dirs(self, filterfunc, already_found=None):
        """Returns list of directories that verify the filterfunc condition on their size, sorted by ascending size"""
        if already_found is None:
            already_found = []
        if self.typenode == D:
            if filterfunc(self.size):
                already_found.append(self)
            for child in self.children.values():
                child.filter_dirs(filterfunc, already_found)
        return sorted(already_found, key=lambda directory: directory.size)

    def string_repr(self, indent=0):
        str_repr = f"{' ' * indent}" \
                   f"- {self.namenode} ({self.typenode}, size={str(self.size)})"
        for child in self.children.values():
            str_repr += "\n" + child.string_repr(indent + 2)
        return str_repr

    def __repr__(self):
        return self.string_repr()


root = Node(D, '/')
pwd = root  # start at /
ls_pending = False

for line in data:
    if line.startswith("$ cd"):
        ls_pending = False
        target = line[5:]
        if target == "..":
            pwd = pwd.up()
        elif target == "/":
            pwd = root
        else:
            pwd.add_child(D, namenode=target)
            pwd = pwd.down(target)
    elif line == "$ ls":
        ls_pending = True
    elif ls_pending:
        prefix, name = line.split()
        if prefix == "dir":
            pwd.add_child(D, namenode=name)
        else:
            pwd.add_child(F, namenode=name, size=int(prefix))
    else:
        print(f"ERROR on line {line}")
        sys.exit(1)


root.compute_size()
# pprint(root)

small_dirs = root.filter_dirs(lambda size: size <= 100000)
print(f"Part one: {sum(d.size for d in small_dirs)}")

total_ds = 70000000
free_ds = total_ds - root.size
to_delete_ds = 30000000 - free_ds

print(f"{to_delete_ds=}")
large_dirs = root.filter_dirs(lambda size: size >= to_delete_ds)
# pprint(large_dirs[0])
print(f"Part two: {large_dirs[0].size}")
