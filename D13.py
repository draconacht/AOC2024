#%%
import re
from collections import namedtuple
from itertools import *

with open('D13_inp.txt') as fl:
	inp = fl.read()
#%%

Machine = namedtuple('Machine', ['a', 'b', 'prize'])
Button = namedtuple('Button', ['x', 'y'])
Prize = namedtuple('Prize', ['x', 'y'])

get_xy = re.compile(r'^.X.(\d+), Y.(\d+).$')
#%%
machines = []

for batch in batched(inp.splitlines(), 4):
	a = Button(*map(int, re.match(get_xy, batch[0]).groups()))
	b = Button(*map(int, re.match(get_xy, batch[1]).groups()))
	prize = Prize(*map(int, re.match(get_xy, batch[2]).groups()))
	# prize = Prize(10000000000000 + prize.x, 10000000000000 + prize.y)  # uncomment for part 2
	machines.append(Machine(a, b, prize))

#%%
s = 0
for a, b, prize in machines:
  x = (prize.x * b.y - prize.y * b.x) / (a.x * b.y - b.x * a.y)
  y = (prize.y * a.x - prize.x * a.y) / (a.x * b.y - b.x * a.y)
  if int(x) != x or int(y) != y:
    continue
  s += 3 * x + y

# %%
print(int(s))