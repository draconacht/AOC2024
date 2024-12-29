#%%
from time import sleep

inp = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
#%%
with open('D07_inp.txt') as fl:
	inp = fl.read()
#%%
tests = []
for line in inp.splitlines():
	target, _, pieces = line.partition(': ')
	tests.append((int(target), [int(piece) for piece in pieces.split(" ")]))
#%%
tests
#%%
from functools import *

s = 0
for target, pieces in tests:
	acc = [(pieces[0], False)]
	path = [str(pieces[0])]
	while acc[-1][0] < target:
		while len(acc) < len(pieces):   # upstack
			if (x := acc[-1][0] * pieces[len(acc)]) <= target:
				path.append(f"*{pieces[len(acc)]}")
				acc.append((x, False))
			elif (x := acc[-1][0] + pieces[len(acc)]) <= target:
				path.append(f"+{pieces[len(acc)]}")
				acc.append((x, True))
			else: break
		if acc[-1][0] < target or len(acc) < len(pieces):  # downstack
			while acc[-1][1]: 
				acc.pop()
				path.pop()
			acc.pop()
			path.pop()
			if len(acc) == 0: break
			path.append(f"+{pieces[len(acc)]}")
			acc.append((acc[-1][0] + pieces[len(acc)], True))
		if acc[-1][0] == target and len(acc) == len(pieces):
			# print(target, reduce(lambda x, y: eval(str(x)+str(y)), path, ""), pieces, path, all(str(x) == y[1:] for x,y in zip(pieces[1:], path[1:])), len(pieces) == len(path))
			s += target
print(s)
#%% md
# part 1 clean
#%%
s = 0
for target, pieces in tests:
	acc = [(pieces[0], False)]
	while acc[-1][0] < target:
		while len(acc) < len(pieces):   # upstack
			if (x := acc[-1][0] * pieces[len(acc)]) <= target: acc.append((x, False))
			elif (x := acc[-1][0] + pieces[len(acc)]) <= target: acc.append((x, True))
			else: break
		if acc[-1][0] < target or len(acc) < len(pieces):  # downstack
			while acc[-1][1]: acc.pop()
			acc.pop()
			if len(acc) == 0: break
			acc.append((acc[-1][0] + pieces[len(acc)], True))
		if acc[-1][0] == target and len(acc) == len(pieces):
			s += target
print(s)

#%% md
# part 2
#%%
from math import log10
s = 0
def int_concat(a, b):
	return int(b + a * pow(10, int(log10(b))+1))
	
for target, pieces in tests:
	# print(target, pieces)
	acc = pieces[0]
	tasks = [[pieces[0]]]
	while tasks:
		if len(tasks) == len(pieces):
			if target in tasks[-1]:
				s += target
				break
			tasks.pop()
			
		while tasks and not tasks[-1]: tasks.pop()  # downstack
		if not tasks: break
		acc = tasks[-1].pop()
		
		t = []  # upstack
		if (x := acc * pieces[len(tasks)]) <= target: t.append(x)
		if (x := acc + pieces[len(tasks)]) <= target: t.append(x)
		if (x := int(f"{acc}{pieces[len(tasks)]}")) <= target: t.append(x)
		# if (x := int_concat(acc, pieces[len(tasks)])) <= target: t.append(x)
		tasks.append(sorted(t))
		# print(tasks)
print(s)
