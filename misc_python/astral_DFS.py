r"""
             _ 3
    0 - 1 - 2 
         \
          \ 
           4 - 5
          / 
     _ 6 -
    7

"""
G = {
    0: [1],
    1: [0, 2, 4],
    2: [1, 3],
    3: [2],
    4: [1, 5, 6],
    5: [4],
    6: [4, 7],
    7: [6]
}


def search_by_depth(graph, starting_node):
    """
        graph
            : dict[T, list[T]]

        starting_node
            : T

        yields
            > T

        raises
            ! TypeError

        T must be hashable
    """
    stack = list()
    stack.append(starting_node)

    found = {n: False for n in graph}

    while len(stack) > 0:
        node = stack.pop()
        found[node] = True
        stack.extend(n for n in graph[node] if not found[n])
        yield node


print(*search_by_depth(G, 0))
print(*search_by_depth(G, 7))

