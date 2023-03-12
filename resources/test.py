import os

fname = './agents_for_testing.txt'
with open(fname, mode = 'r', encoding = 'utf-8') as f:
    agents = f.readlines()


agents  = [a.strip() for a in agents] # Remove leading and trailing spaces
agents  = [a for a in agents if len(a) <= 256] # Remore unually large ones

sz = 0
szi = 0
for i, line in enumerate(agents):
    if len(line)> sz:
        sz = len(line)
        szi = i


print(sz, szi)