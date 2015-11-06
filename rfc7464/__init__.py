# Copyright (c) AUTHORS
# See LICENSE for details.

"""
rfc7464 -- stream JSON
"""

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .impl import emit, Parser  # noqa
