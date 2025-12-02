"""Demo usage of PyCache2Q."""
from pycache2q import AdaptiveCache, KB_8, KB_64
from pycache2q.file_reader import FileReader
from pycache2q.constants import KB_64, KB_8


def main():
    # Create test file
    with open('file.db', 'wb') as f:
        f.write(b'A' * (10 * 1024 * 1024))  # 10MB file
    
    # Initialize cache
    reader = FileReader('file.db')
    cache = AdaptiveCache(reader, cache_size_mb=2)
    
    # Simulate access pattern: 8KB then 64KB
    print("Reading 8KB at offset 0...")
    data1 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")
    
    print("\nReading 64KB at offset 0...")
    data2 = cache.read(0, KB_64)
    print(f"Stats: {cache.stats()}")
    
    print("\nReading 8KB at offset 0 again...")
    data3 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")

    print("\nReading 8KB at offset 0 again...")
    data4 = cache.read(0, KB_8)
    print(f"Stats: {cache.stats()}")
    
    print("\n✓ Done! Hit rate should be high.")


if __name__ == '__main__':
    main()