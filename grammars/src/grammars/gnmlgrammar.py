"""
    +-----+
    !kDoSE¡
    +-----+

    graph nav markup lang
"""
from parsimonious.grammar import Grammar
from parsimonious.nodes import Node

from grammars.igrammar import IGrammar


GNML_GRAMMAR = r'''
    gnml                = ws (node_def ws)*

    node_def            = node_start ws id ws contents ws node_end
    node_start          = "### NODE" sp newline
    id                  = "---" sp "id" sp ":" sp dotted_str sp newline
    contents            = (content ws)*
    content             = meta / tags / next / prev / doc_hash / prev_hash
    node_end            = "### ENDNODE" sp newline

    meta                = "---" sp "meta" sp ":" sp key_value_list* sp newline
    tags                = "---" sp "tags" sp ":" sp dotted_str_list* sp newline
    next                = "---" sp "next" sp ":" sp dotted_str_list* sp newline
    prev                = "---" sp "prev" sp ":" sp dotted_str_list* sp newline
    doc_hash            = "---" sp "doc_hash" sp ":" sp hex sp newline
    prev_hash           = "---" sp "prev_hash" sp ":" sp hex sp newline

    key_value_list      = key_value (sp "," sp key_value)*
    key_value           = dotted_str sp "=" sp dotted_str
    dotted_str_list     = dotted_str (sp "," sp dotted_str)*
    dotted_str          = str ( "." str )*

    str                 = ~r"[a-zA-Z0-9_]+"
    hex                 = ~r"[a-fA-F0-9]+"
    ws                  = ~r"[\r\n\t ]*"
    sp                  = ~r"[ \t]*"
    newline             = "\n"
'''

EXAMPLE_SOURCE = '''
### NODE
--- id: first.branch.22
--- meta: key1=value1, parent.child.key2=value2
--- tags: tag1, tag.two, three.four.five
--- next: first.branch.22, first.branch2.1
--- prev: first.branch.20
--- doc_hash: a1b2c3d4e5f6
--- prev_hash: fedcba987654
### ENDNODE

### NODE
--- id: some_node
--- tags: single.tag
--- tags: another
--- meta: version=0.2.3, author.name=kDoSE
--- next:
--- prev: 
### ENDNODE


### NODE

--- id: yeah

### ENDNODE
'''


def gnml_tree(source):
    """
        source
            : str
            : gnml-compliant source text

        returns
            > parsimonious.nodes.Node

        raises
            ! ValueError

    """
    tree = IGrammar(GNML_GRAMMAR).parse(source)
    return tree


if __name__ == '__main__':
    root = IGrammar(GNML_GRAMMAR).parse(EXAMPLE_SOURCE)
    assert isinstance(root, Node)
    assert root.full_text == EXAMPLE_SOURCE
    assert root.expr_name == 'gnml'
    assert root.end == len(EXAMPLE_SOURCE)

    assert gnml_tree(EXAMPLE_SOURCE) == root

    grammar = IGrammar(GNML_GRAMMAR)
    assert isinstance(grammar, Grammar)

    # Test dotted_str_list (used for tags, next, prev)
    source = 'first.second.third, yeah, yeah.again,nospace99'
    node = grammar['dotted_str_list'].parse(source)
    assert node.full_text == source
    assert node.expr_name == 'dotted_str_list'
    assert node.end == len(source)


