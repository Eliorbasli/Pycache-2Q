from collections import OrderedDict
from .constants import KB_8, KB_64, BYTE
from .block import Block


class TwoQueueCache:
    """
    Two-Queue cache with Q1 (probationary) and Q2 (main).
    
    - Q1: 30% of cache, FIFO
    - Q2: 70% of cache, LRU
    - Ghost: Tracks evicted Q1 blocks
    """

    def __init__(self, file_reader, cache_size_mb=10):
        self.reader = file_reader
        
        total_bytes = cache_size_mb * BYTE * BYTE
        self.q1_max = int(total_bytes * 0.3)
        self.q2_max = int(total_bytes * 0.7)
        
        self.q1 = OrderedDict()
        self.q2 = OrderedDict()
        self.ghost = OrderedDict()
        
        self.q1_size = 0
        self.q2_size = 0
        
        # Stats
        self.hits = 0
        self.misses = 0
    
    def read(self, offset: int, size: int) -> bytes:
        """Read data from cache or file."""
        key = (offset, size)
        
        if key in self.q2:
            self.hits += 1
            self.q2[key].access_count += 1
            self.q2.move_to_end(key)
            return self.q2[key].data
        
        if size == KB_8:
            large_key = self._get_64kb_key(offset)
            if large_key in self.q2:
                self.hits += 1
                self.q2[large_key].access_count += 1
                self.q2.move_to_end(large_key)
                return self._extract_8kb(self.q2[large_key], offset)
        
        if key in self.q1:
            self.hits += 1
            block = self.q1.pop(key)
            self.q1_size -= block.size
            block.access_count += 1
            self._add_to_q2(block)
            return block.data
        
        if size == KB_8:
            large_key = self._get_64kb_key(offset)
            if large_key in self.q1:
                self.hits += 1
                block = self.q1.pop(large_key)
                self.q1_size -= block.size
                block.access_count += 1
                self._add_to_q2(block)
                return self._extract_8kb(block, offset)
        
        self.misses += 1

        data = self.reader.read(offset, size)
        block = Block(offset, size, data)
        
        if key in self.ghost:
            self.ghost.pop(key)
            self._add_to_q2(block)
        else:
            self._add_to_q1(block)
        
        return data
    
    def _add_to_q1(self, block):
        key = (block.offset, block.size)
        
        while self.q1_size + block.size > self.q1_max and self.q1:
            evict_key, evict_block = self.q1.popitem(last=False)
            self.q1_size -= evict_block.size

        
            if len(self.ghost) >= 1000:
                self.ghost.popitem(last=False)
        
            self.ghost[evict_key] = True
        
        self.q1[key] = block
        self.q1_size += block.size
    
    def _add_to_q2(self, block):
        key = (block.offset, block.size)
        
        while self.q2_size + block.size > self.q2_max and self.q2:
            evict_key, evict_block = self.q2.popitem(last=False)

            self.q2_size -= evict_block.size
        
        self.q2[key] = block
        self.q2_size += block.size
    
    def _get_64kb_key(self, offset):
        aligned = (offset // KB_64) * KB_64
        return (aligned, KB_64)
    
    def _extract_8kb(self, block, offset):
        rel_offset = offset - block.offset
        return block.data[rel_offset:rel_offset + KB_8]
    
    def stats(self) -> dict:
        """hit/miss statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': f'{hit_rate:.2f}%',
            'q1_blocks': len(self.q1),
            'q2_blocks': len(self.q2),
        }
