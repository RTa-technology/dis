"""
iachara API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the iachara API.
:copyright: (c) 2022-present RTa_technology
:license: MIT, see LICENSE for more details.
"""

__title__ = 'iachara'
__author__ = 'RTa_technology'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present RTa_technology'
__version__ = '1.0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .adapter import Adapter, AiohttpAdapter, RequestsAdapter
from .transfer import Transfer

__all__ = [
  'Adapter',
  'RequestsAdapter',
  'AiohttpAdapter',
  'Transfer',
]
