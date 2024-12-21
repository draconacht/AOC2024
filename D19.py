#%%
with open("D19_inp.txt") as fl:
  inp = fl.read()
#%%
inp="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
#%%
towels, _, designs = inp.partition("\n\n")
towels = set(towels.split(", "))
designs = designs.splitlines()
max_towel_size = max(map(len, towels))
#%%
towels, designs, max_towel_size
#%%
from functools import cache
from itertools import *

@cache
def feasible(lookup: str):
  for pre in accumulate(lookup):
    if len(pre) > max_towel_size: return False
    if pre not in towels: continue
    if lookup == pre: return True
    if feasible(lookup.removeprefix(pre)): return True
#%%
print(sum(map(feasible, designs)))
#%% md
# part 2
#%%
from functools import cache
from itertools import *


#%%
@cache
def n_feasibles(lookup: str):
  if not lookup: return 1
  toret = 0
  for pre in islice(accumulate(lookup), max_towel_size):
    if pre not in towels: continue
    toret += n_feasibles(lookup.removeprefix(pre))
  return toret
sum(map(n_feasibles, designs))