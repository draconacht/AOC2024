#%%
import re
from operator import *
from itertools import *
from functools import *

with open('D3_inp.txt') as fl:
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
		# theres also a cool way to do this with dropwhile and iterators
		enabled = False
	if insn.startswith("mul") and enabled:
		nums = re.findall(r'\((\d+),(\d+)\)', insn)[0]
		s += int(nums[0]) * int(nums[1])
print(s)

#%%
valid_ranges = re.finditer(r"(?:^|do\(\))(.*?)(?:don't\(\)|$)", inp, re.DOTALL)
s = 0
for rang in valid_ranges:
	s += sum(reduce(mul, map(int, match.groups()), 1) for match in re.finditer(r"mul\((\d+),(\d+)\)", rang.groups(0)[0]))
s
#%%
sum(sum(reduce(mul, map(int, match.groups()), 1) for match in re.finditer(r"mul\((\d+),(\d+)\)", rang.groups(0)[0])) for rang in re.finditer(r"(?:^|do\(\))(.*?)(?:don't\(\)|$)", inp, re.DOTALL))
