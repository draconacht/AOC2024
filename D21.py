#%%
numpad = ["789","456", "123", " 0A"]
dirpad = [" ^A","<v>"]

from collections import defaultdict
from functools import *
from itertools import *
from operator import *
from typing import NamedTuple

class XY(NamedTuple):
	x: int
	y: int

	def __add__(self, other):
		return XY(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return XY(self.x - other.x, self.y - other.y)
	def __mul__(self, other: int):
		return XY(self.x * other, self.y * other)
	def __rmul__(self, other: int):
		return XY(self.x * other, self.y * other)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __abs__(self):
		return abs(self.x) + abs(self.y)
	
# my logic worked fine for part 1, but some part 2 corrections borrowed from 
# https://www.reddit.com/r/adventofcode/comments/1hjgyps/2024_day_21_part_2_i_got_greedyish/
@cache
def diff_dir(start, end):
	out = ""
	diff = end - start
	if start.x == 0 and end == XY(1, 0):  # down before left to avoid gap
		out += "v" * diff.x
		out += "<" * -diff.y
	elif start == XY(1, 0):  # right before up to avoid gap
		out += ">" * diff.y
		out += "^" * -diff.x
	else:
		if diff.y < 0: out += "<" * -diff.y
		if diff.x > 0: out += "v" * diff.x
		if diff.x < 0: out += "^" * -diff.x
		if diff.y > 0: out += ">" * diff.y
	return out

@cache
def diff_num(start, end):
	out = ""
	diff = end - start
	
	if start + XY(0, diff.y) == XY(3, 0):  # go up before left to avoid gap
		out += "^" * -diff.x
		out += "<" * -diff.y
	elif start + XY(diff.x, 0) == XY(3, 0):  # go right before down to avoid gap 
		out += ">" * diff.y
		out += "v" * diff.x
	else:
		if diff.y < 0: out += "<" * -diff.y
		if diff.x > 0: out += "v" * diff.x
		if diff.x < 0: out += "^" * -diff.x
		if diff.y > 0: out += ">" * diff.y
	return out
		

#%%
inps = ["029A", "980A", "179A", "456A", "379A"]
#%%
with open("D21_inp.txt") as fl:
	inps = fl.read().splitlines()
#%%
num_map = {}
dir_map = {}

for i, row in enumerate(numpad):
	for j, num in enumerate(row):
		num_map[num] = XY(i, j)

for i, row in enumerate(dirpad):
	for j, dir_ in enumerate(row):
		dir_map[dir_] = XY(i, j)
#%% md
# part 1
#%%
@cache
def shortest_path(start: XY, end: XY, depth: int):
	if depth <= 1:
		return diff_dir(start, end)+"A"

	curr_layer = diff_dir(start, end)+"A"
	if depth == 3:
		curr_layer = diff_num(start, end)+"A"
	
	path = ""
	for first, second in pairwise("A"+curr_layer):
		path += shortest_path(dir_map[first], dir_map[second], depth-1)
	return path
	
#%%
complexity = 0
for code in inps:
	p0, p1, p2 = "", "", ""
	for first, second in pairwise("A"+code):
		p2 += shortest_path(num_map[first], num_map[second], 3)
	complexity += len(p2)*int(code[:-1])
print(complexity)

#%% md
# part 2
#%%
@cache
def len_shortest_path(start: XY, end: XY, depth: int):
	if depth <= 1:
		return len(diff_dir(start, end))+1

	curr_layer = diff_dir(start, end)+"A"
	if depth == 26:
		curr_layer = diff_num(start, end)+"A"

	path = 0
	for first, second in pairwise("A"+curr_layer):
		path += len_shortest_path(dir_map[first], dir_map[second], depth-1)
	return path

#%%
complexity = 0
for code in inps:
	p2 = 0
	for first, second in pairwise("A"+code):
		p2 += len_shortest_path(num_map[first], num_map[second], 26)
	complexity += p2*int(code[:-1])

print(complexity)
