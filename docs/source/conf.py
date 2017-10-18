#!/usr/bin/env python3

import sphinx_rtd_theme


# Extensions
extensions = ['sphinx.ext.mathjax', 'sphinx.ext.todo']


# Basic file information
source_suffix = '.rst'
master_doc = 'index'


# Project information
project = 'PyPWA'
copyright = '2017, PyPWA Team'
author = 'PyPWA Team'
version = '2.3'
release = '2.3.0'


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
    'pointsize': '12pt',
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
