""" 
    von Neumann method to extract evenly weighted random bits
    from an unevenly weighted initial bit stream
    
    notice that on perfectly random, evenly weighted input of length n
    this method produces an output of length ~0.25n on average
    we lose ~50% of the initial information, then encode what remains
    according to an arbitrary schema (ie) 0 1 -> 1 and 1 0 -> 0
    
    input 011111 -> output 1
    input 010000 -> output 1 (!)
    filtering by von Neumann method discards extreme sequences
    what if extreme sequences represent salient physical data?
    
    input 010101 -> output 111
    input 101010 -> output 000 (!)
    sequences with identical behavior can appear as opposites
    filtering by von Neumann method can obscure salient behavior
"""
from contextlib import suppress
from secrets import randbits


ones = [1] * 100
zeros = [0] * 50

stream = ones + zeros

# using cryptographic randomness to 'shuffle'
indices = [randbits(32) for _ in stream]

# sort according to random indices
random_stream = [t[1] for t in sorted(zip(indices, stream))]

print('# initial stream')
print(random_stream)
print()


def von_neumann(stream):
    """ consider bits in successive pairs  
        if the bits are different keep the second """
    it = iter(stream)

    with suppress(StopIteration):
        while True:
            a, b = next(it), next(it)
            if a != b:
                yield b


filtered = [bit for bit in von_neumann(random_stream)]

print('# filtered stream')
print(filtered)
print()

print('# metrics')
initial = len(stream)
final = len(filtered)
ones = sum(filtered)
zeros = final - ones 
efficiency = final / initial

metrics = f'''\
ones : {ones}
zeros: {zeros}
efficiency: {efficiency:.0%}
'''

print(metrics)
