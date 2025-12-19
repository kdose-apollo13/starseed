"""
    wolfram rules printed like barbarian
"""
light = '\u9608'
dark = '  '

rule_110 = {
    (dark, dark, dark): light,
    (dark, dark, light): dark,
    (dark, light, dark): dark,
    (dark, light, light): light,
    (light, dark, dark): dark,
    (light, dark, light): dark,
    (light, light, dark): dark,
    (light, light, light): light
}

rule_30 = {
    (dark, dark, dark): light,
    (dark, dark, light): light,
    (dark, light, dark): light,
    (dark, light, light): dark,
    (light, dark, dark): dark,
    (light, dark, light): dark,
    (light, light, dark): dark,
    (light, light, light): light
}


def compute_next(prev, rule):
    for i, _ in enumerate(prev):
        try:
            yield rule[prev[i - 1], prev[i], prev[i + 1]]
        except IndexError:
            yield light
        

display = lambda l: print(''.join(l))

line = [light] * 40 + [dark] + [light] * 40
display(line)

for i in range(38):
    line = list(compute_next(line, rule_30))
    display(line)

