# Copyright (c) Moshe Zadka
# See LICENSE for details.
import os
import sys

up = os.path.dirname(os.path.dirname(__file__))
sys.path.append(up)

import rfc7464 as module

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]
master_doc = 'index'
project = 'rfc7464'
copyright = '2015, Moshe Zadka'
author = 'Moshe Zadka'
version = module.__version__
release = module.__version__
