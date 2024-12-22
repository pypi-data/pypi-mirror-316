"""
Zbinfigs
=====

Provides
  1. Methods to parse a zotero collection .csv and extract figures
  2. Methods to label and sort figures for image classification
  3. Machine learning recipes for semantic and image analysis

How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code, and a loose standing reference guide, available from
`the Zbinfigs homepage <https://update-link-here>`_.

The docstring examples assume that `zbinfigs` has been imported as ``zbf``::

  >>> import zbinfigs as zbf

Code snippets are indicated by three greater-than signs::

  >>> x = 42
  >>> x = x + 1

Use the built-in ``help`` function to view a function's docstring::

  >>> help(zbf.read_collection)
  ... # doctest: +SKIP

"""



__author__ = "Isaac Spackman"
__email__ = "ispackman@mines.edu"
__description__ = """
zbinfigs is a python code designed to facilitate classification of scholarly articles stored in zotero collections. 
The code input is a .csv exported from a zotero collection.
"""
__version__ = "0.1.7"
__license__ = "MIT"  
__status__ = "Development"  
__maintainer__ = "Isaac Spackman"
__maintainer_email__ = "ispackman@mines.edu"


from .collection import *  
from .utils import *       