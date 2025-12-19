"""
    +-----+
    !kDoSE¡
    +-----+
    weird or useful python snippets

"""

# -----------------------------------------------------------------------------
# a list can be a member of itself
l = list()
l.append('hello')
l.append(l)

assert l == ['hello', l]
assert id(l) == id(l[1])
assert l[1][1][1][1][0] == 'hello'


# -----------------------------------------------------------------------------
# insert alphabet chars into global dict
# remove quotes for clean use and output
class Str(str):
	def __repr__(self):
		return super().__repr__().strip("'")

for i in range(65, 91):
	c = chr(i)
	globals()[c] = Str(c)

# union
assert {A, B} | {B, C} == {A, B, C}
# intersect
assert {A, B} & {B, C} == {B}
# difference
assert {A, B, C} - {B, C} == {A}
# symmetric difference
assert {A, B, C, D} ^ {B, C} == {A, D}


# -----------------------------------------------------------------------------
# rename method on a builtin while maintaining metadata
from functools import wraps

class Dict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	@wraps(dict.setdefault)
	def get_or_default(self, key, default=None, /):
		return self.setdefault(key, default)


d = Dict()
v = d.setdefault(0)
assert v is None
w = d.get_or_default(1, 'value')
assert w == 'value'
# help(d.get_or_default)  # shows docs for setdefault


# -----------------------------------------------------------------------------
# define a class attribute that implements __set_name__
# TODO: part of descriptor protocol, use with __get__, __set__
class D:
    def __set_name__(self, owner, name):
        # print(f'{owner = }, {name = }')
        assert name == 'triggers_set_name'

nothing_happens = D()

class T:
    triggers_set_name = D()


# -----------------------------------------------------------------------------
# subclass string so == triggers a regex match
import re

class RegexEqual(str):
	def __eq__(self, pattern):
		return re.fullmatch(pattern, self)

x = 'hello'

match RegexEqual(x):
	case 'h.*o':
		print('yeop')
	case _:
		print('nope')

