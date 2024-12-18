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
with open("D18_inp.txt") as fl:
  inp = fl.read()
len_x, len_y = 71, 71
t = 1024
#%%
inp = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
len_x, len_y = 7, 7
t = 12
#%%
data = set([XY(*map(int, row.split(','))) for row in inp.splitlines()][:t])
#%%
layer, next_layer = [], {XY(0, 0)}
dirs = [XY(0, 1), XY(1, 0), XY(0, -1), XY(-1, 0)]  # E S W N
dist = [[10**8]*len_y for _ in range(len_x)]
depth = -1

def in_bounds(xy: XY):
  return 0 <= xy.x < len_x and 0 <= xy.y < len_y

while next_layer:
  layer, next_layer = next_layer, set()
  depth += 1

  for node in layer:
    dist[node.x][node.y] = depth
    neighbours = [node+dir_ for dir_ in dirs]
    neighbours = [x for x in neighbours if in_bounds(x) and dist[x.x][x.y] == 10**8 and x not in data]
    next_layer.update(neighbours)
#%%
import seaborn as sns

max_val = max(max(x for x in row if x != 10**8) for row in dist)
rescaled = [[max_val*1.2 if val == 10**8 else val for val in row] for row in dist]

sns.heatmap(rescaled)
#%% md
# part 2
#%%
dist = []
def connected(n):
  global dist
  obs = set(data[:n])
  print(data[n-1])

  layer, next_layer = [], {XY(0, 0)}
  dirs = [XY(0, 1), XY(1, 0), XY(0, -1), XY(-1, 0)]  # E S W N
  dist = [[10**8]*len_y for _ in range(len_x)]
  depth = -1

  def in_bounds(xy: XY):
    return 0 <= xy.x < len_x and 0 <= xy.y < len_y

  while next_layer:
    layer, next_layer = next_layer, set()
    depth += 1

    for node in layer:
      dist[node.x][node.y] = depth
      neighbours = [node+dir_ for dir_ in dirs]
      neighbours = [x for x in neighbours if in_bounds(x) and dist[x.x][x.y] == 10**8 and x not in obs]
      next_layer.update(neighbours)

  return dist[-1][-1] != 10**8
#%%
# insert me doing binary search by hand here
#%%
connected(2883)
max_val = max(max(x if x != 10**8 else 0 for x in row) for row in dist)
rescaled = [[max_val*1.2 if val == 10**8 else val for val in row] for row in dist]

sns.heatmap(rescaled)