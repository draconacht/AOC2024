#%%
with open("D17_inp.txt") as fl:
	inp = fl.read().splitlines()
#%%
inp = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0""".splitlines()
#%%
inp = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0""".splitlines()
#%%
reg = {0: 0, 1: 0, 2: 0}
state = {0: "A", 1: "0", 2: "0"}
pc = 0
buf = []
ctr = 0

for i in range(3):
	reg[i] = int(inp[i].rpartition(': ')[-1])
program_raw = [int(x) for x in inp[-1].rpartition(': ')[-1].split(',')]
#%%
print(reg)
print(program_raw)
#%%
def adv(cval: int):
	val = reg.get(cval-4, cval)
	reg[0] >>= val

def bxl(val: int):
	reg[1] ^= val

def bst(cval: int):
	val = reg.get(cval-4, cval)
	reg[1] = val & 0b111

def jnz(val: int):
	global pc
	if reg[0]: pc = val - 2

def bxc(_: int):
	reg[1] ^= reg[2]

def out(cval: int):
	val = reg.get(cval-4, cval)
	buf.append(val & 0b111)

def bdv(cval: int):
	val = reg.get(cval-4, cval)
	reg[1] = reg[0] >> val

def cdv(cval: int):
	val = reg.get(cval-4, cval)
	reg[2] = reg[0] >> val

#%%
ops = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]
pc = 0
buf = []

while pc + 1 < len(program_raw):
	opc, param = program_raw[pc], program_raw[pc+1]
	ops[opc](param)
	pc += 2
	
print(",".join(map(str, buf)))
#%%
program_raw
#%% md
# part 2
#%%
program_raw
#%%
def f(a):  # only works for my input, simplify other as needed
	b = (a & 7) ^ 4
	c = a >> b
	b = (b ^ c) ^ 4
	return b & 7

def satisfactory(pre_a, height):
	if height == len(program_raw):
		return pre_a
	
	for i in range(8):
		test = (pre_a << 3) + i
		target = program_raw[-1-height]
		if f(test) == target:
			ret = satisfactory(test, height+1)
			if ret: return ret
	return 0
#%%
i = 156985331222018
reg = {0: i, 1: 0, 2: 0}
pc = 0
buf = []

while pc + 1 < len(program_raw):
	opc, param = program_raw[pc], program_raw[pc+1]
	ops[opc](param)
	pc += 2
	
print(buf)
print(",".join(map(str, buf)))

#%%
