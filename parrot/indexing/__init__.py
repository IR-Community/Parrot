
import lucene
lucene.initVM()

from .index_builder import *

__all__ = [
    "build_index",
    "IndexBuilder"
]