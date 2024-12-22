#%%
inp = [1, 2, 3, 2024]
#%%
with open("D22_inp.txt") as fl:
	inp = [int(x) for x in fl.read().splitlines()]
#%%
def mix(n0: int, n1: int):
	return n0 ^ n1

def prune(n: int):
	return n & ((1 << 24) - 1)

def shuffle(n: int):
	n = prune(mix(n, 64*n))
	n = prune(mix(n, n//32))
	return prune(mix(n, 2048*n))
#%% md
# part 1
#%%
total = 0
for secret in inp:
	s = secret
	for i in range(2000):
		s = shuffle(s)
	total += s
print(total)

#%% md
# part 2
#%%
from collections import deque

sales = []
for secret in inp:
	sales.append({})
	subseq = deque()
	s_prev, s = secret%10, secret
	for i in range(4):
		s = shuffle(s)
		subseq.append(s%10-s_prev%10)
		s_prev = s
	sales[-1][tuple(subseq)] = s%10
	
	for i in range(1997):
		s = shuffle(s)
		subseq.append(s%10-s_prev%10)
		subseq.popleft()
		if not sales[-1].get(tuple(subseq)): sales[-1][tuple(subseq)] = s%10
		s_prev = s
#%%
all_subseqs = set.union(*(set(x.keys()) for x in sales))
#%%
print(max(sum(sale.get(subseq, 0) for sale in sales) for subseq in all_subseqs))