from dataclasses import dataclass

@dataclass
class Block:
    offset: int
    size: int
    data: bytes
    access_count: int = 0
