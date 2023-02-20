#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

with open('myfile.csv') as csvfile:
    reader = csv.reader(csvfile, skipinitialspace=True)  # remove the spaces after the commas
    result = {}  # or collections.OrderedDict() if the output order is important
    for row in reader:
        if row[0] in result:
            result[row[0]].extend(row[1:])  # do not include the key again
        else:
            result[row[0]] = row

    for row in result.values():
        print(', '.join(row))
