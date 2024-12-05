#%%
from operator import *
from itertools import *
from functools import *
from collections import *
#%%
with open("D5_inp.txt") as fl:
	inp = fl.read()
#%%
inp = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
#%%
rules, _, tests = inp.partition('\n\n')
rules = [list(map(int, row.split('|'))) for row in rules.split('\n')]
tests = [list(map(int, row.split(','))) for row in tests.split('\n')]

#%%
print(rules)
print(tests)
#%%
descendents = defaultdict(set)
for parent, child in rules:
	descendents[parent].add(child)
#%% md
# part 1
#%%
sum(test[len(test)//2] for test in tests if all(parent not in descendents[child] for parent, child in pairwise(test)))
#%% md
# part 2
#%%
sum(sorted(test, key=cmp_to_key(lambda a, b: -1 if a not in descendents[b] else 1))[len(test)//2] for test in tests if\
				not	all(parent not in descendents[child] for parent, child in pairwise(test)))

#%%
s = 0
for test in tests:
	if all(parent not in descendents[child] for parent, child in pairwise(test)): continue
	for i in range(len(test)):
		for j in range(i):
			if test[j] in descendents[test[i]]:
				test.insert(j, test.pop(i))
				break
	s += test[len(test)//2]
s