#%%
inp="""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
#%%
with open("D25_inp.txt") as fl:
    inp = fl.read()
#%%
import numpy as np

locks = []
keys = []
for chunk in inp.split('\n\n'):
    pieces = np.array([0]*5)
    vals = np.transpose([list(x) for x in chunk.splitlines()])
    for i in range(5):
        for cell in vals[i]:
            if cell == vals[i][0]:
                pieces[i] += 1
    if vals[0][0] == '#':
        locks.append(pieces-1)
    else:
        keys.append(6-pieces)

#%%
fits = 0
for lock in locks:
    for key in keys:
        if all(lock + key < 6):
            fits += 1
print(fits)