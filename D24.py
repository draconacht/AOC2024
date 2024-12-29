#%%
with open("D24_inp.txt") as fl:
    inp = fl.read()
#%%
inp = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
#%%
from collections import namedtuple

Command = namedtuple('Command', ['opcode', 'i0', 'i1', 'out'])

start_state, _, commands = inp.partition('\n\n')
start_state = {line.partition(":")[0]:int(line.rpartition(": ")[-1]) for line in start_state.splitlines()}

cmd = []
for command in commands.splitlines():
    tokens = command.split(" ")
    cmd.append(Command(tokens[1], tokens[0], tokens[2], tokens[-1]))

#%%
start_state, cmd
#%%
from collections import *

deps = defaultdict(list)
for command in cmd:
    deps[command.out].append(command)

#%%
from operator import *
from functools import cache

ops = {'XOR': xor, 'OR': or_, 'AND': and_}

@cache
def fetch(reg):
    if reg in start_state: return start_state[reg]

    toret = False
    for opc, i0, i1, _ in deps[reg]:
        toret |= ops[opc](fetch(i0), fetch(i1))

    return toret

#%%
zs = {}
for z in (k for k in deps.keys() if k.startswith('z')):
    zs[z] = fetch(z)
#%%
int(''.join(str(x[1]) for x in sorted(zs.items(), reverse=True)), base=2)
#%%
zs
#%%
from itertools import *

it = list(start_state.items())
x, y = [a[1] for a in it[:len(it)//2]], [a[1] for a in it[len(it)//2:]]
x, y
#%%
def X(i): return x[i]
def Y(i): return y[i]
def Z(i): return zs[f'z{i:02}']

def S(i):
    return (X(i) ^ Y(i)) ^ C(i)

@cache
def C(i):
    if i == 0: return 0
    if i == 1: return X(0) & Y(0)
    return ((X(i-1) ^ Y(i-1)) & C(i-1)) | (X(i-1) & Y(i-1)) 
#%%
for i in range(len(it)//2):
    if S(i) != Z(i):
        print(i, S(i), '::', C(i), '||', Z(i))
#%%
import graphviz

graph = graphviz.Digraph(format='png')

for node, connections in deps.items():
    buf = [*connections]
    while buf:
        conn = buf.pop()
        hub = f"{conn.opcode} {conn.i0} {conn.i1}"
        graph.edge(hub, conn.out)
        graph.edge(conn.i0, hub)
        graph.edge(conn.i1, hub)
#%%
deps.items()
#%%
graph.render("out.png")  # from the graph i just verified the ripple carry adder manually lol