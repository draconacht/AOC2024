#%%
import re
from collections import namedtuple, Counter

XY = namedtuple('XY', ['x', 'y'])
Robot = namedtuple('Robot', ['p', 'v'])
#%%
with open('D14_inp.txt') as fl:
	inp = fl.read()
size = XY(101, 103)
#%%
inp = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
size = XY(11, 7)
#%%
inp_parse = re.compile(r'^p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)$')

robots = []
for line in inp.splitlines():
	vals = [int(x) for x in inp_parse.match(line).groups()]
	robots.append(Robot(XY(vals[0], vals[1]), XY(vals[2], vals[3])))
		
#%%
robots
#%% md
# part 1
#%%
q = [0, 0, 0, 0]
finals = set()
for robot in robots:
	final = XY((robot.p.x + 100*robot.v.x) % size.x, (robot.p.y + 100*robot.v.y) % size.y)
	finals.add(final)
	print(final)
	if final.x == size.x // 2 or final.y == size.y // 2: continue
	q[2 * (final.x > size.x // 2) + (final.y > size.y // 2)] += 1
#%%
from operator import mul
from functools import reduce

print(reduce(mul, q, 1))
#%% md
# part 2
#%%
for ctr in range(0, 10_000):
	filled = set()
	for robot in robots:
		next_ = XY((robot.p.x + ctr*robot.v.x) % size.x, (robot.p.y + ctr*robot.v.y) % size.y)
		filled.add(next_)
	
	buf = ""
	for y in range(size.y):
		for x in range(size.x):
			buf += "#" if XY(x, y) in filled else " "
		buf += "\n"
			
	with open('D14_out.txt', 'w') as fl:
		fl.write(buf)

#%%
