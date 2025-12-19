"""
    achieve arithmetic mean without using len
    use reduce to accumulate a count over some iterator
"""
from functools import reduce


# uses only func and iterable
def avg(it):
    f = lambda x, y: (x[0] + y[0], x[1] + y[1])
    total, count = reduce(f, ((x, 1) for x in it))
    return total / count

assert avg(range(10)) == 4.5


# alternate version with initial value tuple
def avg(it):
    f = lambda x, y: (x[0] + y, x[1] + 1)
    total, count = reduce(f, it, (0, 0))
    return total / count

assert avg(range(10)) == 4.5

