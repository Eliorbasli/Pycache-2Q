import time
from .twoqueue_cache import TwoQueueCache
from .constants import SECOND, KB_8, KB_64
from .block import Block


class AdaptiveCache(TwoQueueCache):
    def __init__(self, file_reader, cache_size_mb=10):
        super().__init__(file_reader, cache_size_mb)
        self.patterns = {}

    def read(self, offset: int, size: int) -> bytes:
        result = super().read(offset, size)

        if size == KB_8:
            aligned = (offset // KB_64) * KB_64
            now = time.time()

            if aligned in self.patterns:
                last_time, count = self.patterns[aligned]
                if now - last_time < 5 * SECOND:
                    self.patterns[aligned] = (now, count + 1)
                    
                    if count + 1 >= 2:
                        self._prefetch_64kb(aligned)
                else:
                    self.patterns[aligned] = (now, 1)
            else:
                self.patterns[aligned] = (now, 1)

        return result

    def _prefetch_64kb(self, aligned_offset):
        key = (aligned_offset, KB_64)
        if key not in self.q1 and key not in self.q2:
            try:
                data = self.reader.read(aligned_offset, KB_64)
                block = Block(aligned_offset, KB_64, data)
                self._add_to_q1(block)
            except:
                pass
