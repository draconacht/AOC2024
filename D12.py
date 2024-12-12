#%%
with open("D12_inp.txt") as fl:
	inp = fl.read()
#%%
inp = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOOE"""
#%%
inp="""AAAA
BBCD
BBCC
EEEC"""
#%%
inp="""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""
#%%
inp="""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""
#%%
inp = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
#%%
data = inp.splitlines()
len_x, len_y = len(data), len(data[0])
#%%
def scan_subgraph(i, j) -> tuple[int, int]:
	target = data[i][j]
	buf = [(i, j)]
	area, perimeter = 0, 0

	while buf:
		x, y = buf.pop()
		if not (0 <= x < len_x and 0 <= y < len_y): continue
		if visited[x][y] or data[x][y] != target: continue
		visited[x][y] = True
		neighbourhood = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]

		perimeter += sum(1 for (i_, j_) in neighbourhood if not (0 <= i_ < len_x and 0 <= j_ < len_y) or data[i_][j_] != target)
		area += 1
		buf.extend(neighbourhood)

	return (area, perimeter)
#%%
visited = [[False]*len_y for _ in range(len_x)]
price = 0
for i in range(len_x):
	for j in range(len_y):
		if not(visited[i][j]):
			area, perimeter = scan_subgraph(i, j)
			price += area * perimeter
print(price)

#%% md
# part 2
#%%
import time
from colorama import *

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # CW - E, S, W, N

def oob(x, y):
	return not (0 <= x < len_x and 0 <= y < len_y)

def crawl_out(x, y) -> int:
	target = data[x][y]
	edges = 0
	dir_ = 1
	start = None

	while (x, y, dir_) != start:
		if start is None: start = (x, y, dir_)
		#print("@@", x, y, "ESWN"[dir_])
		crawled_out.add((x, y, dir_))
		wall_x, wall_y = x+DIRS[(dir_+1)%4][0], y+DIRS[(dir_+1)%4][1]
		if not oob(wall_x, wall_y) and data[wall_x][wall_y] == target:  # when possible, hug right wall
			dir_ = (dir_+1)%4
			#print("+<")
			edges += 1
			if (x, y, dir_) == start: break
		else:
			next_x, next_y = x+DIRS[dir_][0], y+DIRS[dir_][1]
			if oob(next_x, next_y) or data[next_x][next_y] != target:  # at an end, turn CCW till you have room to # move
				dir_ = (dir_-1)%4
				#print("+>")
				edges += 1
				if (x, y, dir_) == start: break
				continue

		#print(x, y, "ESWN"[dir_])
		if start is None: start = (x, y, dir_)
		crawled_out.add((x, y, dir_))
		dx, dy = DIRS[dir_]
		x, y = x+dx, y+dy

	print("~", x, y, "ESWN"[dir_], edges, target)
	return edges

def crawl_in(x, y) -> int:
	target = data[x][y]
	edges = 0
	dir_ = 1
	start = None

	while (x, y, dir_) != start:
		crawled_in.add((x, y, dir_))
		if start is None: start = (x, y, dir_)
		wall_x, wall_y = x+DIRS[(dir_-1)%4][0], y+DIRS[(dir_-1)%4][1]
		if not oob(wall_x, wall_y) and data[wall_x][wall_y] == target:  # when possible, hug right wall
			dir_ = (dir_-1)%4
			edges += 1
		else:
			next_x, next_y = x+DIRS[dir_][0], y+DIRS[dir_][1]
			if oob(next_x, next_y) or data[next_x][next_y] != target:  # at an end, turn CCW till you have room to # 
			# move
				dir_ = (dir_+1)%4
				edges += 1
				continue


		#print(x, y, "ESWN"[dir_])
		dx, dy = DIRS[dir_]
		x, y = x+dx, y+dy

	# print("&", x, y, "ESWN"[dir_], edges, target)
	return edges


#%%
def scan_crawl_subgraph(i, j) -> tuple[int, int]:
	target = data[i][j]
	buf = [(i, j)]


	neighbourhood = [(i+1, j), (i, j+1), (i-1, j), (i, j-1)]
	if all(oob(x, y) or data[x][y] != target for x, y in neighbourhood):
		return 1, 4
	area, edges = 0, crawl_out(i, j)

	while buf:
		x, y = buf.pop()
		#print("+", x, y, buf)
		if oob(x, y): continue
		if visited[x][y] or data[x][y] != target: continue
		visited[x][y] = True
		
		area += 1

		neighbourhood = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
		
		if not oob(x, y+1) and data[x][y+1] != target and not (x, y, 3) in crawled_out and not (x, y, 1) in crawled_in:
			#print("/")
			edges += crawl_in(x, y)
			#print("/", edges)
		
		buf.extend(((x,y) for (x,y) in neighbourhood if not oob(x, y) and data[x][y] == target and not visited[x][y]))

	return (area, edges)

#%%
from itertools import chain

data = inp.splitlines()
d = [[x for x in row] for row in data]
len_x, len_y = len(data), len(data[0])
visited = [[False]*len_y for _ in range(len_x)]
crawled_out = set()
crawled_in = set()
price = 0
for i in range(len_x):
	for j in range(len_y):
		if not(visited[i][j]):
			area, edges = scan_crawl_subgraph(i, j)
			print(area, edges)
			price += edges * area
print(price)

#%%
with open('D12_out.txt', 'w+') as fl:
	fl.write('\\n'.join([''.join(row) for row in d]))