#%%
inp = list(map(int, "2333133121414131402"))
#%%
with open("D09_inp.txt") as fl:
	inp = list(map(int, fl.read()))
#%%
len(inp)
#%%
from itertools import *
#%% md
# part 1
#%%
plugs_rev = ((len(inp)//2-i, k) for i, k in enumerate(islice(reversed(inp), 0, len(inp), 2)))
plugs = enumerate(islice(inp, 0, len(inp), 2))
holes = islice(inp, 1, len(inp), 2)

hole_size = 0
plug_val, plug_size = 0, 0
r_plug_val, r_plug_size = len(inp), 0
checksum = 0
REVERSE_GEAR = True
path = ""
for i in count():
	while not(hole_size > 0 or plug_size > 0):
		if hole_size == 0 and REVERSE_GEAR:
			plug_val, plug_size = next(plugs, (-1, -1))
			print(">", plug_val, plug_size)
			REVERSE_GEAR = False
		if plug_size == 0 and not REVERSE_GEAR:
			hole_size = next(holes, -1)
			print("<", hole_size)
			REVERSE_GEAR = True
	while r_plug_size == 0 and REVERSE_GEAR:
		r_plug_val, r_plug_size = next(plugs_rev, (-1, -1))
		print("-", r_plug_val, r_plug_size)
		
	if plug_val == r_plug_val:
		if REVERSE_GEAR: break
		hole_size = r_plug_size
		REVERSE_GEAR = True
	if plug_val > r_plug_val:  break 
	
	if REVERSE_GEAR:
		checksum += i * r_plug_val
		path += str(r_plug_val) + "."
		hole_size, r_plug_size = hole_size - 1, r_plug_size -1
	else:
		checksum += i * plug_val
		path += str(plug_val) + "."
		plug_size -= 1
	# print(i, checksum)
print(checksum)
#%% md
# cleaned
#%%
plugs_rev = ((len(inp)//2-i, k) for i, k in enumerate(islice(reversed(inp), 0, len(inp), 2)))
plugs = enumerate(islice(inp, 0, len(inp), 2))
holes = islice(inp, 1, len(inp), 2)

hole_size = 0
plug_val, plug_size = 0, 0
r_plug_val, r_plug_size = len(inp), 0
checksum = 0
REVERSE_GEAR = True
path = ""
for i in count():
	while not(hole_size > 0 or plug_size > 0):
		if hole_size == 0 and REVERSE_GEAR:
			plug_val, plug_size = next(plugs, (-1, -1))
			REVERSE_GEAR = False
		if plug_size == 0 and not REVERSE_GEAR:
			hole_size = next(holes, -1)
			REVERSE_GEAR = True
	while r_plug_size == 0 and REVERSE_GEAR:
		r_plug_val, r_plug_size = next(plugs_rev, (-1, -1))
		
	if plug_val == r_plug_val:
		if REVERSE_GEAR: break
		hole_size = r_plug_size
		REVERSE_GEAR = True
	if plug_val > r_plug_val:  break 
	
	if REVERSE_GEAR:
		checksum += i * r_plug_val
		hole_size, r_plug_size = hole_size - 1, r_plug_size -1
	else:
		checksum += i * plug_val
		plug_size -= 1

#%% md
# part 2
#%%
plugs = inp[0::2]
holes = inp[1::2]
disk = []

for i, (plug, hole) in enumerate(batched(inp+[0], 2)):
	if plug: disk.append((i, plug))
	if hole: disk.append((-1, hole))
#%%
i = 0
while i < len(disk):
	i += 1
	r_val, r_size = disk[-i]
	if r_val < 0: continue
	for j, (v, h_size) in enumerate(disk[:-i]):
		if v != -1 or h_size < r_size: continue
		disk[j] = (r_val, r_size)
		disk[-i] = (-1, r_size)
		if h_size > r_size: disk.insert(j+1, (-1, h_size-r_size))
		break
#%%
i = 0
checksum = 0
for block_val, block_size in disk:
	if block_val <= 0: 
		i += block_size
		continue
	while block_size > 0:
		checksum += i * block_val
		i += 1
		block_size -= 1
print(checksum)
	