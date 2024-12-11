#%%
import math
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor

inp = "125 17"
#%%
with open('D11_inp.txt') as fl:
	inp = fl.read()
#%%
data = list(map(int, inp.split(" ")))
#%% md
# part 1, bruteforced
#%%
from itertools import *
from functools import cache

def blink(n: int) -> list[int]:
	if n == 0: return [1]
	d = len(str(n))
	if d%2 == 0:
		return [int(str(n)[:d//2]), int(str(n)[d//2:])]
	return [2024*n]
#%%
next = data
for i in range(25):
	next = list(chain.from_iterable(map(blink, next)))

#%%
print(len(next))
#%% md
# part 2, cached + recursive
#%%
def n_digits(num: int) -> int:
	return int(math.log10(num)) + 1
#%%
@cache
def n_blink_size(num: int, blinks: int) -> int:
	if blinks == 1: return 1 if num == 0 or n_digits(num) % 2 == 1 else 2
	
	if num == 0: return n_blink_size(1, blinks - 1)
	if n_digits(num) % 2 == 1: return n_blink_size(num*2024, blinks-1)
	
	brk = n_digits(num) // 2
	return n_blink_size(int(str(num)[:brk]), blinks-1) + n_blink_size(int(str(num)[brk:]), blinks-1)

#%%
print(sum(map(lambda x: n_blink_size(x, 75), data)))