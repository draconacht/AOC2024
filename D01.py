#%%
with open('D01_inp.txt') as fl:
    inp_raw = fl.read()
#%%
inp_raw="""3   4
4   3
2   5
1   3
3   9
3   3"""
#%%
from operator import *
from functools import *
from itertools import *
from typing import Iterable

type Pair[T] = Iterable[T] # length not enforced, just doing for cleanness

inp: Iterable[Pair[int]] = (map(int, row.split()) for row in inp_raw.splitlines())
unsorted_lists: Pair[Iterable[int]] = zip(*inp)
sorted_lists: Pair[Iterable[int]] = map(sorted, unsorted_lists)
diff_sum: int = sum(map(abs, starmap(sub, zip(*sorted_lists))))
#%%
sum(map(abs, starmap(sub, zip(*map(sorted, zip(*(map(int, row.split()) for row in inp_raw.splitlines())))))))
#%%
from collections import Counter

inp: Iterable[Pair[int]] = (map(int, row.split()) for row in inp_raw.splitlines())
unsorted_lists: Pair[Iterable[int]] = zip(*inp)
ctrs: Pair[Counter[int]] = map(Counter, unsorted_lists)
c0, c1 = next(ctrs), next(ctrs)
diff_index: int = sum(c0.get(k, 0) * freq * k for k, freq in c1.items())
diff_index
#%%
call(lambda c0, c1: sum(c0.get(k, 0) * freq * k for k, freq in c1.items()), *map(Counter, zip(*(map(int, row.split()) for row in inp_raw.splitlines()))))
#%%
