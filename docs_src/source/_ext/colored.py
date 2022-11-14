import re

from docutils import nodes
from docutils.parsers import rst
from sphinx.addnodes import highlightlang


class ColoredDirective(rst.Directive):
    """
    Because I have no idea how to do nested elements
    this direvtive will return the text as is in a
    code block.
    https://stackoverflow.com/questions/74102792/nested-nodes-in-sphinx-extension
    """
    has_content = True
    
    def run(self):
        
        node = nodes.literal_block("",
            "\n".join(self.content)
        )
        
        
        return [
            #highlightlang(
            #    lang = "none",
            #    force = None,
            #    linenothreshold = -1
            #),
            node,
        ]

def setup(app):
    app.add_directive("colored", ColoredDirective)

