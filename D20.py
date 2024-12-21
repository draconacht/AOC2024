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
with open("D20_inp.txt") as fl:
  inp = fl.read()

THRESHOLD = 100
THRESHOLD_2 = 100
#%%
inp="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

THRESHOLD = 12
THRESHOLD_2 = 72
#%%
data = inp.splitlines()
len_x, len_y = len(data), len(data[0])

dirs = [XY(0, 1), XY(1, 0), XY(0, -1), XY(-1, 0)]  # E S W N

#%%
start, end = None, None 
scores = [[10 ** 8] * len_y for _ in range(len_x)]

for i, row in enumerate(data):
  for j, cell in enumerate(row):
    if cell == 'S': start = XY(i, j)
    if cell == 'E': end = XY(i, j)

def in_bounds(xy: XY):
  return 0 <= xy.x < len_x and 0 <= xy.y < len_y
#%%
layer, next_layer = set(), {start}
depth = -1
n_skips = 0

while next_layer:
  layer, next_layer = next_layer, set()
  depth += 1 

  for node in layer:
    if data[node.x][node.y] == '#': continue
    scores[node.x][node.y] = min(scores[node.x][node.y], depth)
    neighbours = [node+dir_ for dir_ in dirs]
    neighbours = [x for x in neighbours if in_bounds(x) and scores[x.x][x.y] > depth]
    next_layer.update(neighbours)

    skips = [node + 2*dir_ for dir_ in dirs]
    skips = [scores[node.x][node.y] - scores[x.x][x.y] - 2 for x in skips if in_bounds(x) and data[x.x][x.y] != '#']
    n_skips += len([skip for skip in skips if skip >= THRESHOLD])
print(n_skips)

#%%
scoremax = 1.2 * max(max(cell if cell < 10 ** 8 else 0 for cell in row) for row in scores)
for i, j in product([*range(len_x)], [*range(len_y)]):
  if scores[i][j] == 10 ** 8:
    scores[i][j] = scoremax
#%%
import seaborn as sns

sns.heatmap(scores)
#%% md
# part 2
#%%
def parse_bbox(i, j):
  depth = -1
  layer, next_layer = set(), {XY(i, j)} 

  score_start = scores[i][j]
  ends = []

  visited = set()
  while depth < 20:
    layer, next_layer = next_layer, set()
    depth += 1

    for node in layer:
      if node in visited: continue
      visited.add(node)
      
      if data[node.x][node.y] != '#' and scores[node.x][node.y] - (score_start + depth) >= THRESHOLD_2: 
        ends.append(node)

      neighbours = [node+ dir_ for dir_ in dirs]
      neighbours = [x for x in neighbours if in_bounds(x)]
      next_layer.update(neighbours)

  return ends
#%%
layer, next_layer = set(), {start}
depth = -1

ends = defaultdict(lambda: list())
while next_layer:
  layer, next_layer = next_layer, set()
  depth += 1

  for node in layer:
    print(node)
    ends[node] += parse_bbox(node.x, node.y)
    neighbours = [node+ dir_ for dir_ in dirs]
    neighbours = [x for x in neighbours if in_bounds(x) and scores[x.x][x.y] > depth and data[node.x][node.y] != '#']
    next_layer.update(neighbours)

#print("\n".join(map(str, ends.items())))
print(sum(map(len, ends.values())))