from pprint import pprint
import re
import sys
import time
from utils import inputparts, str2intlist

data = inputparts("day05")
# data = inputparts("day05-example")

# almanac = {src: {"dest": dest,
#                  "mappings": [(startsrc, endsrc, startdest, rangelen), ...]
#                 },
#            src: ...
# }

seeds = []
almanac = {}
for part in data:
    if match := re.match(r"seeds: (.*)", part[0]):
        seeds = str2intlist(match.group(1))
        continue

    if match := re.match(r"(\w+)-to-(\w+) map:", part[0]):
        src = match.group(1)
        dest = match.group(2)

        mappings = []
        for r in part[1:]:
            startdest, startsrc, rangelen = str2intlist(r)
            endsrc = startsrc + rangelen

            mappings.append((startsrc, endsrc, startdest, rangelen))

        # sort the mappings by ascending startsrc
        almanac[src] = {"dest": dest, "mappings": sorted(mappings, key=lambda m: m[0])}

# print(seeds)
# pprint(almanac)

def find_min_location(input_seed_ranges):
    current_category = "seed"
    current_ranges = set(input_seed_ranges)
    while current_category in almanac:  # stop at end of chain, ie 'location'
        print(f"{current_category} ({len(current_ranges)} ranges)...")
        dest_category = almanac[current_category]['dest']
        mappings = almanac[current_category]['mappings']
        next_ranges = set()
        orphan_ranges = set()  # ranges that were not covered by a mapping
        # print(current_ranges)
        while current_ranges:
            current_start, current_end = current_ranges.pop()
            mapped = False
            for startsrc, endsrc, startdest, rangelen in mappings:  # reminder: mappings is ordered !
                # we're not interested by the mappings that don't cover our range
                if endsrc <= current_start:
                    continue
                if startsrc >= current_end:
                    break

                # 1) range entirely in the mapping
                if current_start >= startsrc and current_end <= endsrc:
                    next_ranges.add((startdest + (current_start - startsrc), 
                                     startdest + (current_end - startsrc)))
                    mapped = True
                
                # 2) start of range in the mapping
                elif startsrc <= current_start <= endsrc <= current_end:
                    next_ranges.add((startdest + (current_start - startsrc), 
                                     startdest + rangelen))
                    mapped = True
                    # add the end of the range to the stuff to check
                    current_ranges.add((endsrc, current_end))
                    
                # 3) mapping strictly inside of range
                elif current_start < startsrc and endsrc < current_end:
                    next_ranges.add((startdest, startdest + rangelen))
                    mapped = True
                    # start of the range is orphan
                    orphan_ranges.add((current_start, startsrc))
                    # end of the range must be checked
                    current_ranges.add((endsrc, current_end))

                # 4) end of range in the mapping
                elif current_start <= startsrc <= current_end <= endsrc:
                    next_ranges.add((startdest, startdest + (current_end - startsrc)))
                    mapped = True
                    # start of the range is orphan
                    orphan_ranges.add((current_start, startsrc))

            if not mapped:
                # no mappings cover the range
                orphan_ranges.add((current_start, current_end))

        # "Any source numbers (ie orphan range) that aren't mapped correspond to the same destination number."
        next_ranges.update(orphan_ranges)
        
        # print(f"{current_category}: {current_val} => {dest_category}: {dest_val}")

        current_category = dest_category
        current_ranges = next_ranges

    # here current_ranges = location ranges
    # print(sorted(current_ranges, key=lambda r: r[0]))
    return min(current_ranges, key=lambda r: r[0])

min_loc_1 = find_min_location([(s, s+1) for s in seeds])
# pprint(chains_part_one)
print(f"Part one: {min_loc_1[0]}")

# print(seeds)
seeds_ranges = []
for i in range(0, len(seeds), 2):
    startseed = seeds[i]
    endseed = seeds[i] + seeds[i+1]
    seeds_ranges.append((startseed, endseed))
# print(seeds_ranges)

start_time = time.time()
min_loc_2 = find_min_location(seeds_ranges)
end_time = time.time()
print(f"Part two: {min_loc_2[0]} ({time.time() - start_time} seconds)")