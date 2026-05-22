from textwrap import dedent

from unittest import main, TestCase
from klab.ututils import Spec, Runner

from parsimonious.nodes import Node
from parsimonious.exceptions import ParseError

from grammars.igrammar import IGrammar

from grammars.gnmlgrammar import GNML_GRAMMAR, EXAMPLE_SOURCE, gnml_tree



class test_gnml_grammar_basics(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)
        self.example_source = EXAMPLE_SOURCE

    def test_parse_returns_node(self):
        tree = self.grammar.parse(self.example_source)
        self.asrt(isinstance(tree, Node))
        self.equa(tree.expr_name, 'gnml')

    def test_full_example_source_parses_cleanly(self):
        tree = gnml_tree(self.example_source)
        self.asrt(tree is not None)
        self.equa(tree.full_text.strip(), self.example_source.strip())

    def test_minimal_node_with_only_id(self):
        source = dedent('''
            ### NODE
            --- id: minimal.node
            ### ENDNODE
            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))


class test_gnml_dotted_identifiers(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)

    def test_dotted_str_supports_dots(self):
        source = 'first.second.third'
        node = self.grammar['dotted_str'].parse(source)
        self.asrt(isinstance(node, Node))
        self.equa(node.full_text, source)

    def test_dotted_str_list(self):
        source = 'alpha.beta, gamma, delta.epsilon.phi'
        node = self.grammar['dotted_str_list'].parse(source)
        self.asrt(isinstance(node, Node))
        self.equa(node.full_text, source)

    def test_dotted_id_in_node(self):
        source = dedent('''
            ### NODE
            --- id: deep.nested.id.123
            --- tags: tag.one, tag.two.three
            --- next: next.one, next.two.four
            ### ENDNODE
            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))


class test_gnml_meta_and_tags(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)

    def test_meta_with_dotted_keys(self):
        source = dedent('''
            ### NODE
            --- id: meta.test
            --- meta: simple.key=value.with.dots, another.key=simple.value
            ### ENDNODE
            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))

    def test_empty_meta_and_tags_allowed(self):
        source = dedent('''
            ### NODE
            --- id: empty.fields
            --- meta:
            --- tags:
            --- next:
            --- prev:
            ### ENDNODE
            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))


class test_gnml_hashes(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)

    def test_doc_hash_and_prev_hash(self):
        source = dedent('''
            ### NODE
            --- id: hash.test.node
            --- doc_hash: a1b2c3d4e5f67890
            --- prev_hash: fedcba9876543210
            ### ENDNODE
            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))


class test_gnml_whitespace_and_empty_lines(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)

    def test_extra_newlines_and_spaces(self):
        source = dedent('''

            ### NODE

            --- id: whitespace.test

            --- meta: key1 = value1 , key2=value2

            --- tags:   tag1  ,  tag.two  

            ### ENDNODE

            ''')
        tree = self.grammar.parse(source)
        self.asrt(isinstance(tree, Node))


class test_gnml_error_cases(Spec):
    def setUp(self):
        self.grammar = IGrammar(GNML_GRAMMAR)

    def test_missing_id_raises_error(self):
        source = dedent('''
            ### NODE
            --- tags: missing.id
            ### ENDNODE
            ''')
        with self.rais((ValueError, ParseError)):
            self.grammar.parse(source)

    def test_invalid_identifier(self):
        source = dedent('''
            ### NODE
            --- id: invalid@identifier
            ### ENDNODE
            ''')
        with self.rais((ValueError, ParseError)):
            self.grammar.parse(source)


if __name__ == '__main__':
    main(testRunner=Runner)
