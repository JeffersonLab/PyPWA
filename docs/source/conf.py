#!/usr/bin/env python3

from datetime import datetime
import sphinx_rtd_theme

from PyPWA import __version__, __release__, __author__

# Extensions
extensions = [
    'sphinx.ext.mathjax', 'sphinx.ext.todo',
    'sphinx.ext.autodoc', 'sphinx_autodoc_typehints',
    'sphinxcontrib.bibtex', 'recommonmark'
]


# Basic file information
source_suffix = ['.rst', '.md']
master_doc = 'index'


# Project information
project = 'PyPWA'
copyright = f'{datetime.now().year}, Norfolk State University'
author = __author__
version = __version__
release = __release__


# Sphinx Extra Options
language = None
exclude_patterns = []
pygments_style = 'sphinx'
todo_include_todos = False


# HTML settings
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
htmlhelp_basename = 'PyPWAdoc'


# LaTeX settings
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '11pt',
    'preamble': r'''
        \usepackage{charter}
        \usepackage[defaultsans]{lato}
        \usepackage{inconsolata}
    ''',
}
latex_documents = [
    (master_doc, 'PyPWA.tex', 'PyPWA Documentation', 'PyPWA Team', 'manual'),
]


# manpages settings
man_pages = [(master_doc, 'pypwa', 'PyPWA Documentation', [author], 1)]


# Biblitex info
texinfo_documents = [
    (
        master_doc, 'PyPWA', 'PyPWA Documentation',
        author, 'PyPWA', 'Python Partial Wave Analysis Toolkit.',
        'Scientific Studies'
    ),
]
