#%%
with open("D10_inp.txt") as fl:
	inp = fl.read()
#%%
from functools import *
from itertools import *
from operator import *

data = [list(map(int, x)) for x in inp.splitlines()]
x_len, y_len = len(data), len(data[0])
#%% md
# part 1
#%%
def get_trails(x, y, num):
	if not (0 <= x < x_len and 0 <= y < y_len): return set()
	if data[x][y] != num: return set()
	if num == 9:
		return {(x, y)}

	return set.union(*starmap(get_trails,[(x+1, y, num+1), (x-1, y, num+1), (x, y+1, num+1), (x, y-1, num+1)]))
#%%
trails = 0
for i in range(x_len):
	for j in range(y_len):
		trails += len(get_trails(i, j, 0))
print(trails)
#%% md
# part 2
#%%
def get_trails(x, y, num):
	if not (0 <= x < x_len and 0 <= y < y_len): return 0
	if data[x][y] != num: return 0
	if num == 9: return 1

	return sum(starmap(get_trails,[(x+1, y, num+1), (x-1, y, num+1), (x, y+1, num+1), (x, y-1, num+1)]))
#%%
trails = 0
for i in range(x_len):
	for j in range(y_len):
		trails += get_trails(i, j, 0)
print(trails)