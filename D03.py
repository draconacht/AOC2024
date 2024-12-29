#%%
import re
from operator import *
from itertools import *
from functools import *

with open('D03_inp.txt') as fl:
	inp = fl.read()
#%% md
# part 1
#%%
numpairs = re.finditer(r"mul\((\d+),(\d+)\)", inp)
sum((lambda a, b: int(a) * int(b))(*pair.groups()) for pair in numpairs)

#%%
sum(reduce(mul, map(int, match.groups()), 1) for match in re.finditer(r"mul\((\d+),(\d+)\)", inp))
#%% md
# part 2
#%%
insns = re.findall(r"(do\(\)|don't\(\)|mul\(\d+,\d+\))", inp)
enabled = True
s = 0
for insn in insns:
	if insn == "do()":
		enabled = True
	if insn == "don't()":
		enabled = False
	if insn.startswith("mul") and enabled:
		nums = re.findall(r'\((\d+),(\d+)\)', insn)[0]
		s += int(nums[0]) * int(nums[1])
print(s)

#%%
i = iter(re.findall(r"(do\(\)|don't\(\)|mul\(\d+,\d+\))", inp))

s = 0
while (insn := next(i, None)) is not None:
	if insn.startswith("mul"):
		n = re.findall(r'\((\d+),(\d+)\)', insn)[0]
		s += int(n[0]) * int(n[1])
	if insn == "don't()":
		i = dropwhile(lambda ins: ins != "do()", i)
print(s)
#%%
valid_ranges = re.finditer(r"(?:^|do\(\))(.*?)(?:don't\(\)|$)", inp, re.DOTALL)
s = 0
for rang in valid_ranges:
	s += sum(reduce(mul, map(int, match.groups()), 1) for match in re.finditer(r"mul\((\d+),(\d+)\)", rang.groups(0)[0]))
s
#%%
sum(sum(reduce(mul, map(int, match.groups()), 1) for match in re.finditer(r"mul\((\d+),(\d+)\)", rang.groups(0)[0])) for rang in re.finditer(r"(?:^|do\(\))(.*?)(?:don't\(\)|$)", inp, re.DOTALL))