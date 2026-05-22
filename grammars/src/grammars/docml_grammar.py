"""
    DOCML - Simplified Document Markup Language (v3)
    Flat, no nesting. Designed to be the content portion of GNML nodes.
"""
import json
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


DOCML_GRAMMAR = r'''
    docml           = ws (block ws)*
    block           = text_block / math_block / img_block

    text_block      = "<text" attrs tag_end text_content "</text>"
    math_block      = "<math" attrs tag_end math_content "</math>"
    img_block       = "<img"  attrs tag_end img_content  "</img>"

    cap_block       = "<cap" attrs tag_end raw_text "</cap>"
    ref_block       = "<ref=" quoted_str ">" raw_text "</ref>"

    # Flat content - no block nesting
    text_content    = (ws (raw_text / cap_block) ws)*
    math_content    = (ws (raw_text / ref_block / cap_block) ws)*
    img_content     = (ws (raw_text / cap_block) ws)*

    attrs           = (ws1 attr)*
    attr            = src_attr / ref_attr / flag_attr
    src_attr        = "src=" quoted_str
    ref_attr        = "ref=" quoted_str
    flag_attr       = "centered" / "top" / "bottom" / "inline"

    tag_end         = ws ">"
    quoted_str      = "\"" ~r"[^\"]*" "\""
    raw_text        = ~r"[^<]+"
    ws1             = ~r"[\r\n\t ]+"
    ws              = ~r"[\r\n\t ]*"
'''


class DocMLVisitor(NodeVisitor):
    def visit_docml(self, node, visited_children):
        blocks = []
        for item in visited_children[1]:          # each (block ws) pair
            if item and isinstance(item, list) and item[0]:
                blocks.append(item[0])
        return blocks

    def visit_block(self, node, visited_children):
        return visited_children[0]

    def visit_text_block(self, node, visited_children):
        attrs = visited_children[1] or {}
        content = visited_children[3]
        return {"tag": "text", "attrs": attrs, "content": content}

    def visit_math_block(self, node, visited_children):
        attrs = visited_children[1] or {}
        content = visited_children[3]
        return {"tag": "math", "attrs": attrs, "content": content}

    def visit_img_block(self, node, visited_children):
        attrs = visited_children[1] or {}
        content = visited_children[3]
        return {"tag": "img", "attrs": attrs, "content": content}

    def visit_cap_block(self, node, visited_children):
        attrs = visited_children[1] or {}
        text = str(visited_children[3] or "").strip()
        return {"tag": "cap", "attrs": attrs, "text": text}

    def visit_ref_block(self, node, visited_children):
        ref_id = visited_children[1]
        text = str(visited_children[3] or "").strip()
        return {"tag": "ref", "ref": ref_id, "text": text}

    def visit_text_content(self, node, visited_children):
        return self._flatten(visited_children)

    def visit_math_content(self, node, visited_children):
        return self._flatten(visited_children)

    def visit_img_content(self, node, visited_children):
        return self._flatten(visited_children)

    def _flatten(self, children):
        result = []
        for group in children:
            if isinstance(group, list) and len(group) >= 2:
                item = group[1]                     # the actual raw_text / cap / ref
                if item is not None:
                    result.append(item)
        return result

    def visit_raw_text(self, node, visited_children):
        return node.full_text.strip() if node.full_text else ""

    def visit_attrs(self, node, visited_children):
        attr_dict = {}
        for child in visited_children:
            if child:
                attr = child[0] if isinstance(child, list) else child
                if isinstance(attr, tuple):
                    attr_dict[attr[0]] = attr[1]
                else:
                    attr_dict[attr] = True
        return attr_dict

    def visit_attr(self, node, visited_children):
        return visited_children[0]

    def visit_src_attr(self, node, visited_children):
        return ("src", visited_children[1])

    def visit_ref_attr(self, node, visited_children):
        return ("ref", visited_children[1])

    def visit_flag_attr(self, node, visited_children):
        return node.full_text

    def visit_quoted_str(self, node, visited_children):
        return node.full_text.strip('"')

    def generic_visit(self, node, visited_children):
        return visited_children or None


# ─────────────────────────────────────────────────────────────
REVISED_EXAMPLE_DOCML = '''
<text src="intro.txt">
    This text is appended to the loaded text file.
    <cap bottom>Fig 1. Intro Equation</cap>
</text>

<img src="diagram.png" centered>
    <cap top>System Diagram</cap>
    FFD8FFE000104A464946
    AABBCCDDEEFF
</img>

<math src="deriv.tex" centered ref="(23.2)">
    <cap bottom>Full Derivation Steps</cap>
</math>

<text>
    Just a normal text block without a source.
</text>

<math>
    <ref="24">
        $\nabla^bF_{ab}=0$
    </ref>
    <ref="25">$F_{ab}=F_{[ab]}$</ref>
</math>
'''


if __name__ == '__main__':
    grammar = Grammar(DOCML_GRAMMAR)
    tree = grammar.parse(REVISED_EXAMPLE_DOCML)

    visitor = DocMLVisitor()
    parsed_output = visitor.visit(tree)

    print(json.dumps(parsed_output, indent=2))
    print("\n✅ DOCML parsing succeeded!")

