#%%
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

#%%
with open("D16_inp.txt") as fl:
	inp = fl.read().replace("E", ".")
#%%
inp = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".replace("E", ".")
#%%
inp = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".replace("E", ".")
#%%
data = inp.splitlines()
len_x, len_y = len(data), len(data[0])
dirs = [XY(-1, 0), XY(0, 1), XY(1, 0), XY(0, -1)]  # N E S W
#%%
layer, next_layer = {}, {XY(len_x-2, 1): 1}
min_scores = {XY(x, y):10**8 for x, y in product(range(len_x), range(len_y))}
min_scores[XY(len_x-2, 1)] = 0
min_path = [[4]*len_y for _ in range(len_x)]

while next_layer:
	layer, next_layer = next_layer, {}
	for node, dir_ in layer.items():
		min_path[node.x][node.y] = dir_
		
		front = node + dirs[dir_]
		front_score = min_scores[node] + 1
		if data[front.x][front.y] == "." and min_scores[front] > front_score:
			next_layer[front] = dir_
			min_scores[front] = front_score
		
		right = node + dirs[(dir_ + 1) % 4]
		right_score = min_scores[node] + 1001
		if data[right.x][right.y] == "." and min_scores[right] > right_score:
			next_layer[right] = (dir_+1)%4
			min_scores[right] = right_score

		left = node + dirs[(dir_ - 1) % 4]
		left_score = min_scores[node] + 1001
		if data[left.x][left.y] == "." and min_scores[left] > left_score:
			next_layer[left] = (dir_-1)%4
			min_scores[left] = left_score
	
#%%
out = []
mval = max((x for x in min_scores.values() if x < 10**8))
for i in range(len_x):
	out.append([])
	for j in range(len_y):
		s = min_scores[XY(i, j)]
		s = 1.2*mval if s == 10**8 else s
		out[-1].append(s)
		
#%%
import seaborn as sns

sns.heatmap(out)
#%%
end = XY(1, len_y-2)
traceback = [(end, min_path[end.x][end.y], min_scores[end])]

while traceback[-1][0] != XY(len_x-2, 1):
	node, dir_, score = traceback[-1]
	next_ = node-dirs[dir_]
	traceback.append((next_, min_path[next_.x][next_.y], min_scores[next_]))

#%%
from collections import *
benches = {XY(x, y):False for x, y in product(range(len_x), range(len_y))}
stk = set()

@cache
def benchable(xy: XY, dir_, score):
	if data[xy.x][xy.y] == "#": 
		return False
	
	if (xy, dir_, score) in traceback:
		benches[xy] = True
		return True
	
	if (benchable_cached(xy + dirs[dir_], dir_, score+1) or 
			benchable_cached(xy + dirs[(dir_-1)%4], (dir_-1)%4, score+1001) or 
			benchable_cached(xy + dirs[(dir_+1)%4], (dir_+1)%4, score+1001)):
		benches[xy] = True
		return True

	return False

min_failing_score = defaultdict(lambda: min_scores[XY(1, len_y-2)])
def benchable_cached(xy, dir_, score):
	if score > min_failing_score[(xy, dir_)]:
		return False
	if xy in stk: return False
	
	stk.add(xy)
	toret = benchable(xy, dir_, score)
	stk.remove(xy)
	
	if toret is False: 
		min_failing_score[(xy, dir_)] = score
		
	return toret
		
#%%
stk
#%%
import sys
sys.setrecursionlimit(10_000)
for node, dir_, score in traceback:
	benchable_cached(node, dir_, score)

	benchable_cached(node + dirs[(dir_-1)%4], (dir_-1)%4, score+1001)
	benchable_cached(node + dirs[(dir_+1)%4], (dir_+1)%4, score+1001)
	
#%%
len(stk)
#%%
len([pos for pos, exists in benches.items() if exists])
#%%
