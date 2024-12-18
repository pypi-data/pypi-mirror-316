# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import tattl
import datetime

project = "tattl"
author = "thcrt"
copyright = f"{datetime.date.today().year}, thcrt"
version = tattl.__version__
release = tattl.__version__

needs_sphinx = "8.1"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx_paramlinks",
    "sphinx.ext.autodoc.typehints",
    "sphinx_multiversion",
]

highlight_language = "python3"

nitpicky = True

maximum_signature_line_length = 80

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "furo"
html_theme_options = {
    "source_repository": "https://github.com/thcrt/tattl/",
    "source_branch": "main",
    "source_directory": "docs/",
}

html_title = f"{project} docs"
html_last_updated_fmt = "%b %d, %Y"

html_static_path = ["_static"]
html_css_files = ["css/versions.css"]
html_js_files = ["js/versions.js"]

add_function_parentheses = False

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

autodoc_class_signature = "separated"
paramlinks_hyperlink_param = "name"


def remove_module_docstring(app, what, name, obj, options, lines):
    if what == "module" and name == "tattl":
        del lines[:]


def setup(app):
    app.connect("autodoc-process-docstring", remove_module_docstring)
