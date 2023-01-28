#:==========================================
# Sphinx Documentation Builder Configuration
#:==========================================


#########
# Imports

from datetime import date
from pathlib import Path
import sys


#############
# Change Path

sys.path.insert(0, str(Path('.').parent.parent))
sys.path.append(str(Path('./_ext').resolve()))


#####################
# Project Information

project = 'adorable'
copyright = f'{date.today().year}, phoenixR'
author = 'phoenixR'
release = '0.1.3.post1'


###############
# Configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    
    'sphinx_copybutton',
    'sphinx_inline_tabs',
    'sphinxcontrib.repl',
    'sphinxcontrib.spelling',
    'sphinxemoji.sphinxemoji',
    
    'colored',
]

extlinks = dict(
    pylib = ('https://docs.python.org/3/library/%s.html', '%s'),
    pyfn = ('https://docs.python.org/3/library/functions.html#%s', '%s'),
    piplib = ('https://pypi.org/project/%s', '%s')
)

####################
# TODO Configuration

todo_include_todos = True
todo_emit_warnings = True

#######################
# Autodoc Configuration

autodoc_default_options = dict.fromkeys('''
    members
    inherited-members
    undoc-members
    '''.split(),
    True
)
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autoclass_content = 'both'

####################
# REPL Configuration

repl_mpl_disable = True


########################
# Spelling Configuration

spelling_ignore_contributor_names = False
spelling_show_suggestions = True
spelling_word_list_filename = '_static/spelling_wordlist.txt'


############
# Find Files

templates_path = ['_templates']
exclude_patterns = []


###########################
# HTML Output Configuration

html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['css/style.css']
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/phoenixr-codes/adorable",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/adorable",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <image xlink:href="https://pypi.org/static/images/logo-small.95de8436.svg" width="16" height="16"/>
                </svg>
            """,
            "class": "",
        }
    ]
}


