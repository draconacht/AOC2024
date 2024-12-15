#%%
from functools import *
from itertools import *
from operator import *
from typing import NamedTuple

class XY(NamedTuple):
	x: int 
	y: int
	
	def __add__(self, other):
		return XY(self.x + other.x, self.y + other.y)
	def __mul__(self, other: int):
		return XY(self.x * other, self.y * other)
	def __rmul__(self, other: int):
		return XY(self.x * other, self.y * other)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

class XYPair(NamedTuple):
	a: XY
	b: XY
	
	def __eq__(self, other):
		return self.a == other.a and self.b == other.b or self.b == other.a and self.a == other.b
	def __hash__(self):
		return hash(tuple(sorted(self)))

#%%
inp = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
#%%
with open("D15_inp.txt") as fl:
	inp = fl.read()
#%%
layout, actions = inp.split("\n\n")
layout = [list(row) for row in layout.splitlines()]
actions = list(actions.replace("\n",""))
dirs = [XY(-1, 0), XY(0, 1), XY(1, 0), XY(0, -1)]  # N E S W
dmap = {"^": dirs[0], ">": dirs[1], "v": dirs[2], "<": dirs[3]}
#%% md
# part 1
#%%
bot = XY(-1, -1)
walls = set()
blocks = set()
movements = []

for i, row in enumerate(layout):
	for j, cell in enumerate(row):
		if cell == "@":
			bot = XY(i, j)
		if cell == "#":
			walls.add(XY(i, j))
		if cell == "O":
			blocks.add(XY(i, j))
	
for action in actions:
	movements.append(dmap[action])
#%%
pos = bot
for movement in movements:
	next_pos = bot + movement
	if next_pos in walls: continue
	
	if next_pos in blocks:
		impact = next_pos
		while impact in blocks:
			impact += movement
		if impact in walls: continue
		else:
			blocks.remove(next_pos)
			blocks.add(impact)
	
	bot = next_pos
#%%
for i, row in enumerate(layout):
	for j, cell in enumerate(row):
		if XY(i, j) in walls: print("#", end="")
		elif XY(i, j) in blocks: print("O", end="")
		elif bot == XY(i, j): print("@", end="")
		else: print(".", end="")
	print("")

#%%
print(sum(100*block.x + block.y for block in blocks))
#%% md
# part 2
#%%
bot = XY(-1, -1)
walls = set()
blocks = set()
movements = []

for i, row in enumerate(layout):
	for j, cell in enumerate(row):
		if cell == "@":
			bot = XY(i, 2*j)
		if cell == "#":
			walls.update([XY(i, 2*j), XY(i, 2*j+1)])
		if cell == "O":
			blocks.add(XYPair(XY(i, 2*j), XY(i, 2*j+1)))

for action in actions:
	movements.append(dmap[action])
#%%
for movement in movements:
	next_pos = bot + movement
	
	anti_b_buf = set()
	b_buf = set()

	if movement.y != 0:  # horizontal movement follows similar logic as before
		impact = next_pos
		while XYPair(impact, impact+movement) in blocks:
			anti_b_buf.add(XYPair(impact, impact+movement))
			b_buf.add(XYPair(impact+movement, impact+2*movement))
			impact += 2*movement
		if impact in walls: continue

	if movement.x != 0:
		impact, next_impact = [], [next_pos]
		walled = False
		b_buf, anti_b_buf = set(), set()
		
		while next_impact and not walled:
			impact, next_impact = next_impact, []
			for point in impact:
				if point in walls:
					walled = True
					break
					
				if (old := XYPair(point, point+XY(0, 1))) in blocks:
					new_ = XYPair(point+movement, point+movement+XY(0, 1))
				elif (old := XYPair(point, point+XY(0, -1))) in blocks:
					new_ = XYPair(point+movement, point+movement+XY(0, -1))
				else: continue
				
				anti_b_buf.add(old)
				b_buf.add(new_)
				next_impact += [*new_]
		
		if walled: continue
		
	blocks = (blocks - anti_b_buf) | b_buf
	bot = next_pos
#%%
def print_boxes():
	for i, row in enumerate(layout):
		for j in range(2*len(row)):
			if XY(i, j) in walls: print("#", end="")
			elif XYPair(XY(i, j), XY(i, j+1)) in blocks: print("[", end="")
			elif XYPair(XY(i, j), XY(i, j-1)) in blocks: print("]", end="")
			elif bot == XY(i, j): print("@", end="")
			else: print(".", end="")
		print("")

#%%
print(sum(100*sorted(block)[0].x + sorted(block)[0].y for block in blocks))
