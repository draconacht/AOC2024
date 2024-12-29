#%%
with open("D06_inp.txt") as fl:
	inp = fl.read().splitlines()
#%%
pos = None 
obstacles = set()
for i, row in enumerate(inp):
  for j, cell in enumerate(row):
    if cell == "^":
      pos = (i, j)
    if cell == "#":
      obstacles.add((i, j))

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
#%% md
# part 1
#%%
visited = {pos}
x, y = pos
dd = 3  # N
dx, dy = DIRS[dd]
while 0 <= x < len(inp) and 0 <= y < len(inp[0]):
	visited.add((x, y))
	while (x+dx, y+dy) in obstacles:
		dd = (dd + 1) % 4
		dx, dy = DIRS[dd]
	x, y = x+dx, y+dy
print(len(visited))
#%% md
# part 2
#%%
def next_obstacle(x, y, dx, dy):
	#if (x, y, dx, dy) in cache:
	#  return cache[(x, y, dx, dy)]

	path = []
	while (x, y) not in obstacles:
		# print("@@", x, y)
		if not(0 <= x < len(inp) and 0 <= y < len(inp)): return (-1, -1)
		path.append((x, y))
		x += dx
		y += dy
	#for i, j in path:
	#  cache[(i, j, dx, dy)] = (x, y)
	return (x, y)
#%%
def will_cycle(x, y, dd):
	dx, dy = DIRS[dd]
	visited = set()
	while True:  # check for cycles from xi, yi
		# print("@", x, y, "+", dx, dy)
		if not (0 <= x < len(inp) and 0 <= y < len(inp[0])): return False  # reached boundary
		if (x, y, dx, dy) in visited: return True

		visited.add((x, y, dx, dy))
		ox, oy = next_obstacle(x, y, dx, dy)
		# print(">", ox, oy)

		if (ox, oy) == (-1, -1): return False  # reached boundary, no obstacle

		x, y = ox-dx, oy-dy
		while (x+dx, y+dy) in obstacles:
			dd = (dd + 1) % 4
			dx, dy = DIRS[dd]

#%%
x, y = pos
cyclers = set()
visited = set()
dd = 3
dx, dy = DIRS[dd]
while 0 <= x < len(inp) and 0 <= y < len(inp[0]):
	visited.add((x, y))
	while (x+dx, y+dy) in obstacles:
		dd = (dd + 1) % 4
		dx, dy = DIRS[dd]
	if (x + dx, y + dy) not in visited and len(inp) > x + dx >= 0 and len(inp[0]) > y + dy >= 0:
		obstacles.add((x+dx, y+dy))  # not an obstacle already, obviously.
		if will_cycle(x, y, (dd+1)%4):
			cyclers.add((x+dx, y+dy))
		obstacles.remove((x+dx, y+dy))
	x, y = x + dx, y + dy

#%%
print(len(cyclers))