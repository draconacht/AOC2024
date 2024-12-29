#%%
inp = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
#%%
with open("D08_inp.txt") as fl:
	inp = fl.read()
#%%
data = inp.splitlines()
#%% md
# part 1
#%%
from collections import defaultdict
from itertools import *
from functools import *

antinodes = set()
nodes = defaultdict(list)
for i, row in enumerate(data):
	for j, cell in enumerate(row):
		if cell == ".": continue
		antinodes.update(filter((lambda xy: 0 <= xy[0] < len(data) and 0 <= xy[1] < len(row)), 
														chain.from_iterable(((x+(x-i), y+ (y-j)),(i-(x-i) , j-(y-j))) for x, y	in nodes[cell])))
		nodes[cell].append((i, j))
		
#%%
print(len(antinodes))
#%% md
# part 2
#%%
from math import gcd

antinodes = set()
nodes = defaultdict(list)
for i, row in enumerate(data):
	for j, cell in enumerate(row):
		if cell == ".": continue
		for x0, y0 in nodes[cell]:
			g = gcd(x0-i, y0-j)
			dx, dy = (x0-i)/g, (y0-j)/g
			
			ctr = 0
			while 0 <= i + ctr * dx < len(data) and 0 <= j + ctr * dy < len(row):
				antinodes.add((i + ctr * dx, j + ctr * dy))
				ctr += 1

			ctr = 1
			while 0 <= i - ctr * dx < len(data) and 0 <= j - ctr * dy < len(row):
				antinodes.add((i - ctr * dx, j - ctr * dy))
				ctr += 1
		nodes[cell].append((i, j))

#%%
print(len(antinodes))
#%%
otext = ""
for i, row in enumerate(data):
	for j, cell in enumerate(row):
		if (i, j) in antinodes: otext += "*"
		else: otext += cell
		otext += "  "
	otext += "\n"
with open("D8_out.txt", "w+") as fl:
	fl.write(otext)
				
#%%
