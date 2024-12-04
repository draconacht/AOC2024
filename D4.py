#%%
from itertools import *
from operator import *
from functools import *

with open("D4_inp.txt") as f:
	inp = f.read().splitlines()
#%%
inp = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".splitlines()
inp
#%%
CHECK = "XMAS"
DIRS = [partial((lambda x, y, start, steps: (start[0]+ steps * x, start[1]+ steps * y)), a, b) for (a,b) in product (range (-1, 2), range(-1, 2))]

found = 0
for i, j in product(range(len(inp)), range(len(inp[0]))):
	if inp[i][j] == CHECK[0]:
		for direction in DIRS: 
			steps = 1
			while True:
				if steps == len(CHECK):
					found += 1
					break
				next_x, next_y = direction((i, j), steps)
				if not (0 <= next_x < len(inp) and 0 <= next_y < len(inp[0])): break
				if inp[next_x][next_y] != CHECK[steps]: break 
				# print(next_x, next_y, inp[next_x][next_y], CHECK[steps])
				steps += 1
				
#%%
found
#%%
V = [a for a in range(3)]
T = [(lambda: a) for a in range(3)]
U = [partial((lambda x: x), a) for a in range(3)]
print([t() for t in T])
print([v for v in V])
print([u() for u in U])
#%%
found = 0
	
for i, j in product(range(1, len(inp)-1), range(1, len(inp[0])-1)):
	if inp[i][j] == "A":
		D1 = f"{inp[i-1][j-1]}{inp[i][j]}{inp[i+1][j+1]}"
		D2 = f"{inp[i-1][j+1]}{inp[i][j]}{inp[i+1][j-1]}"
		if D1 in ('SAM', 'MAS') and D2 in ('SAM', 'MAS'):
			found += 1

#%%
found = sum(1 for x in starmap(
	(lambda i, j: f"{inp[i-1][j-1]}{inp[i][j]}{inp[i+1][j+1]}" in ('SAM', 'MAS') and f"{inp[i-1][j+1]}{inp[i][j]}{inp[i+1][j-1]}" in ('SAM', 'MAS')), 
	product(range(1, len(inp)-1), range(1, len(inp[0])-1) )
) if x)

#%%
found
#%%
