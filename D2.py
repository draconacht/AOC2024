#%%
from functools import *
from operator import *
from itertools import *
from collections import Counter
#%%
with open('D2_inp.txt') as fl:
	inp = ((int(x) for x in row.split()) for row in fl.readlines())
diffs = map(lambda row: list(starmap(sub, pairwise(row))), inp)
safes = filter(lambda row: ((max(row) > 0) == (min(row) > 0)) and all(map(lambda x: 0 < abs(x) <= 3, row)) , diffs)
n_safes = sum(1 for _ in safes)
n_safes

#%%
with open('D2_inp.txt') as fl:
	inp = ((int(x) for x in row.split()) for row in fl.readlines())
sum(1 for _ in filter(lambda row: ((max(row) > 0) == (min(row) > 0)) and all(map(lambda x: 0 < abs(x) <= 3, row)), map(lambda row: list(starmap(sub, pairwise(row))), inp)))
#%%
with open('D2_inp.txt') as fl:
	inp = ((int(x) for x in row.split()) for row in fl.readlines())
diffss = (list(starmap(sub, pairwise(row))) for row in inp)
diff_possibilities = ([diffs, diffs[1:], diffs[:-1]]+ [diffs[0:i-1]+[diffs[i-1]+diffs[i]]+diffs[i+1:] for i in range(1, len(diffs))] for diffs in diffss)
n_safes = sum(1 for _ in safes)
n_safes
#%%
with open('D2_inp.txt') as fl:
	inp = ((int(x) for x in row.split()) for row in fl.readlines())
sum(1 for _ in filter(lambda posss: any(((max(poss) > 0) == (min(poss) > 0)) and all(0 < abs(x) <= 3 for x in poss) for poss in posss), ([diffs, diffs[1:], diffs[:-1]]+ [diffs[0:i-1]+[diffs[i-1]+diffs[i]]+diffs[i+1:] for i in range(1, len(diffs))] for diffs in (list(starmap(sub, pairwise(row))) for row in inp)))) 
