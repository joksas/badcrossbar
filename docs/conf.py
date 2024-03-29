import os
import sys

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "badcrossbar"
copyright = "2022, Dovydas Joksas"
author = "Dovydas Joksas"
release = "1.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_book_theme"
default_role = "literal"
html_theme_options = {
    "single_page": True,
    "repository_url": "https://github.com/joksas/badcrossbar",
    "use_repository_button": True,
    "use_download_button": False,
    "use_fullscreen_button": False,
}
