#!/usr/bin/env python
# -*- coding: utf-8 -*-

INPUT = 347991


def find_layer(nb):
    if nb == 1:
        return 0
    layer = 0
    start = 1
    while True:
        layer += 1
        if nb <= start + 8*layer:
            return layer
        start += 8*layer

assert find_layer(1) == 0
assert find_layer(2) == 1
assert find_layer(9) == 1
assert find_layer(10) == 2
assert find_layer(21) == 2
assert find_layer(26) == 3

input_layer = find_layer(INPUT)
print("Layer of input : {0}".format(input_layer))
print("Dimensionality of this layer : {0}".format(2*input_layer + 1))

