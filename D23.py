#%%
inp="""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
#%%
with open("D23_inp.txt") as fl:
  inp = fl.read()
#%%
data = [x.split("-") for x in inp.splitlines()]
#%%
from collections import *

peers = defaultdict(set)
visited = set()
#%%
for peer0, peer1 in data:
  peers[peer0].add(peer1)
  peers[peer1].add(peer0)
#%%
cycles = set()
for node in peers:
  if not node.startswith('t'): continue

  for peer_1 in peers[node]:
    for peer_2 in peers[peer_1]:
      if peer_2 in peers[node]:
        cycles.add(tuple(sorted([node, peer_1, peer_2])))
#%%
len(cycles)
#%% md
# part 2
#%%
from functools import cache
checked = set()
party_cache = {}

def longest_party(node, party: frozenset):
  if party in party_cache: return party_cache[party]

  max_party = party.copy()
  # print(node, party)

  for peer in (peers[node] - party) - checked:
    if party - peers[peer]: continue 

    new_party = longest_party(peer, party | {peer})
    if len(new_party) > len(max_party):
      max_party = new_party


  # print(node, party, max_party)
  party_cache[party] = max_party
  return max_party
#%%
max_party = set()
checked = set()
for node in peers:
  checked.add(node)
  party = longest_party(node, frozenset([node]))
  # print(party)
  max_party = max(max_party, party, key=lambda x: len(x))
#%%
','.join(sorted(max_party))