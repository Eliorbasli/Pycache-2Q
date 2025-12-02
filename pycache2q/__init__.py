from .block import Block
from .constants import KB_8, KB_64, SECOND
from .twoqueue_cache import TwoQueueCache
from .adaptive_cache import AdaptiveCache

__all__ = [
    "Block",
    "KB_8",
    "KB_64",
    "SECOND",
    "TwoQueueCache",
    "AdaptiveCache",
]



# """PyCache2Q - Two-Queue Cache System"""

# __version__ = "0.1.0"

# from .cache import TwoQueueCache, AdaptiveCache, KB_8, KB_64
# from .file_reader import FileReader

# __all__ = ['TwoQueueCache', 'AdaptiveCache', 'FileReader', 'KB_8', 'KB_64']